#!/usr/bin/env python3
"""
123pan-upload: Upload files to 123pan direct link folder
Usage: python upload.py --file /path/to/file [--folder FOLDER_ID] [--link-type TYPE]
"""

import os
import sys
import json
import hashlib
import base64
import requests
import argparse
from pathlib import Path
from typing import List, Tuple

API_BASE = "https://open-api.123pan.com"

# Load config from config.json if exists
CONFIG = {}
CONFIG_PATH = Path(__file__).parent.parent / "config.json"
if CONFIG_PATH.exists():
    try:
        with open(CONFIG_PATH) as f:
            CONFIG = json.load(f)
    except Exception:
        pass

def get_config(key, env_key=None, default=None):
    if key in CONFIG: return CONFIG[key]
    return os.environ.get(env_key, default) if env_key else default


def get_user_id_from_token() -> int:
    """Extract user ID from access token."""
    token = get_config("access_token", "PAN123_ACCESS_TOKEN", "")
    try:
        # JWT payload is the second part
        parts = token.split(".")
        if len(parts) >= 2:
            # Add padding if needed
            payload = parts[1]
            padding = 4 - len(payload) % 4
            if padding != 4:
                payload += "=" * padding
            data = json.loads(base64.b64decode(payload))
            return data.get("id", 0)
    except Exception:
        pass
    return 0


def get_md5(file_path: str) -> str:
    """Calculate MD5 hash of a file."""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def get_headers():
    """Get API request headers."""
    token = get_config("access_token", "PAN123_ACCESS_TOKEN")
    if not token:
        raise ValueError("PAN123_ACCESS_TOKEN environment variable is required")
    return {
        "Authorization": f"Bearer {token}",
        "Platform": "open_platform",
        "Content-Type": "application/json"
    }


def get_upload_headers():
    """Get headers for upload domain requests."""
    token = get_config("access_token", "PAN123_ACCESS_TOKEN")
    return {
        "Authorization": f"Bearer {token}",
        "Platform": "open_platform"
    }


def get_upload_domain():
    """Get upload domain from API."""
    resp = requests.get(
        f"{API_BASE}/upload/v2/file/domain",
        headers=get_headers(),
        timeout=30
    )
    resp.raise_for_status()
    data = resp.json()
    if data.get("code") != 0:
        raise Exception(f"Failed to get upload domain: {data}")
    return data["data"][0]


def create_file(file_path: str, folder_id: int) -> dict:
    """Create file and get upload info."""
    file_path = Path(file_path)
    filename = file_path.name
    file_size = file_path.stat().st_size
    etag = get_md5(str(file_path))

    resp = requests.post(
        f"{API_BASE}/upload/v2/file/create",
        headers=get_headers(),
        json={
            "parentFileID": folder_id,
            "filename": filename,
            "etag": etag,
            "size": file_size,
            "duplicate": 1
        },
        timeout=30
    )
    resp.raise_for_status()
    result = resp.json()

    if result.get("code") != 0:
        raise Exception(f"Create file failed: {result.get('message', 'Unknown error')}")

    return {
        "file_id": result["data"].get("fileID"),
        "preupload_id": result["data"].get("preuploadID"),
        "reuse": result["data"].get("reuse", False),
        "slice_size": result["data"].get("sliceSize", 16777216),
        "servers": result["data"].get("servers", [])
    }


def upload_slice_v2(upload_server: str, preupload_id: str, slice_no: int, data: bytes, max_retries: int = 3) -> bool:
    """Upload a single slice using v2 API (multipart/form-data POST).
    
    Args:
        upload_server: Upload server URL from create_file response
        preupload_id: Preupload ID
        slice_no: Slice number (1-based)
        data: Slice data bytes
        max_retries: Max retry attempts
    """
    import time

    url = f"{upload_server}/upload/v2/file/slice"
    slice_md5 = hashlib.md5(data).hexdigest()
    
    headers = get_upload_headers()
    # Don't set Content-Type for multipart, requests will set it with boundary

    for attempt in range(max_retries):
        try:
            files = {
                "slice": (f"slice_{slice_no}", data, "application/octet-stream")
            }
            form_data = {
                "preuploadID": preupload_id,
                "sliceNo": slice_no,
                "sliceMD5": slice_md5
            }
            
            resp = requests.post(
                url,
                headers=headers,
                data=form_data,
                files=files,
                timeout=300
            )
            
            if resp.status_code == 200:
                result = resp.json()
                if result.get("code") == 0:
                    return True
                else:
                    print(f"    Slice upload failed: {result.get('message', 'Unknown error')}, retry {attempt + 1}/{max_retries}", file=sys.stderr)
            else:
                print(f"    Slice upload failed (status {resp.status_code}), retry {attempt + 1}/{max_retries}", file=sys.stderr)
        except requests.exceptions.SSLError as e:
            print(f"    SSL error on slice upload, retry {attempt + 1}/{max_retries}: {e}", file=sys.stderr)
        except requests.exceptions.ConnectionError as e:
            print(f"    Connection error on slice upload, retry {attempt + 1}/{max_retries}: {e}", file=sys.stderr)
        except Exception as e:
            print(f"    Error on slice upload, retry {attempt + 1}/{max_retries}: {e}", file=sys.stderr)

        if attempt < max_retries - 1:
            time.sleep(2 ** attempt)  # Exponential backoff: 1s, 2s, 4s

    return False


def calculate_max_retries(file_size: int, max_verify_time: int = None) -> int:
    """Calculate max retries based on file size or user-specified max verify time.
    
    Args:
        file_size: File size in bytes
        max_verify_time: User-specified max verification time in seconds (overrides auto-calculation)
    
    Returns:
        Maximum number of retry attempts
    """
    if max_verify_time is not None and max_verify_time > 0:
        # Each retry waits at least 1 second initially, but delay increases
        # Conservative estimate: average 3 seconds per retry
        return max(60, max_verify_time // 3)
    
    # Auto-calculate: ~5 minutes per GB, with minimum of 60 retries
    # 123pan server-side verification can take very long for large files
    size_gb = file_size / (1024 * 1024 * 1024)
    estimated_seconds = size_gb * 300  # 5 minutes per GB (was 3 min, increased due to slow server)
    retries = max(200, int(estimated_seconds // 3))  # At least 200 retries for large files
    return min(retries, 1200)  # Cap at 1200 retries (~1 hour max)


def complete_upload(preupload_id: str, file_size: int = 0, max_verify_time: int = None) -> dict:
    """Complete the upload with fixed 1s polling interval.
    
    Per API docs: if completed=false, poll every 1 second until done.
    
    Args:
        preupload_id: The preupload ID from create
        file_size: File size in bytes (used to auto-calculate max wait time)
        max_verify_time: User-specified max verification time in seconds (overrides auto-calculation)
    """
    import time
    
    max_retries = calculate_max_retries(file_size, max_verify_time)
    estimated_time = max_verify_time if max_verify_time else (file_size / (1024*1024*1024) * 180)
    
    print(f"  等待服务器校验，最多等待约 {estimated_time:.0f}秒 ({max_retries}次轮询)...", file=sys.stderr)

    for attempt in range(max_retries):
        try:
            resp = requests.post(
                f"{API_BASE}/upload/v2/file/upload_complete",
                headers=get_headers(),
                json={"preuploadID": preupload_id},
                timeout=30
            )
            result = resp.json()

            if result.get("code") == 0:
                if result["data"].get("completed"):
                    print(f"  校验完成，共轮询 {attempt + 1}次", file=sys.stderr)
                    return result["data"]
                else:
                    # Per API docs: completed=false, wait 1s and retry
                    if attempt % 10 == 0 or attempt == 1:
                        elapsed = attempt
                        print(f"  服务器正在校验分片... 已等待 {elapsed}秒 / 预计最多 {estimated_time:.0f}秒", file=sys.stderr)
                    time.sleep(1)  # Fixed 1 second interval per API docs
                    continue
            else:
                message = result.get("message", "")
                # Retry on verification-in-progress errors
                if "校验" in message or "verify" in message.lower() or "check" in message.lower() or "间隔" in message:
                    if attempt % 10 == 0 or attempt == 1:
                        elapsed = attempt
                        print(f"  服务器正在校验分片... 已等待 {elapsed}秒 / 预计最多 {estimated_time:.0f}秒", file=sys.stderr)
                    time.sleep(1)
                    continue
                else:
                    raise Exception(f"Complete upload failed: {message}")
        except requests.exceptions.RequestException as e:
            # Network errors during complete - retry with shorter delay
            if attempt % 10 == 0:
                print(f"  网络错误，正在重试... ({e})", file=sys.stderr)
            time.sleep(1)
            continue

    raise Exception(f"Complete upload timed out after {max_retries} retries (~{estimated_time:.0f}秒)")


def chunked_upload(file_path: str, folder_id: int, max_verify_time: int = None) -> dict:
    """Upload large file using chunks with resume capability."""
    file_path = Path(file_path)
    filename = file_path.name
    file_size = file_path.stat().st_size

    create_result = create_file(str(file_path), folder_id)

    if create_result["reuse"]:
        return {
            "file_id": create_result["file_id"],
            "filename": filename,
            "size": file_size
        }

    preupload_id = create_result["preupload_id"]
    slice_size = create_result["slice_size"]
    upload_server = create_result["servers"][0] if create_result["servers"] else API_BASE

    total_slices = (file_size + slice_size - 1) // slice_size
    print(f"Uploading {filename}: {file_size} bytes, {total_slices} slices (~{slice_size/1024/1024:.1f}MB each)", file=sys.stderr)

    with open(file_path, "rb") as f:
        for slice_no in range(1, total_slices + 1):
            data = f.read(slice_size)
            if not data:
                break

            if not upload_slice_v2(upload_server, preupload_id, slice_no, data):
                raise Exception(f"Failed to upload slice {slice_no}/{total_slices} after retries")

            # Progress report every 5 slices or on last slice
            if slice_no % 5 == 0 or slice_no == total_slices:
                progress = (slice_no / total_slices) * 100
                print(f"  Progress: {slice_no}/{total_slices} slices ({progress:.1f}%)", file=sys.stderr)

    print(f"  All slices uploaded, waiting for server verification...", file=sys.stderr)
    complete_result = complete_upload(preupload_id, file_size=file_size, max_verify_time=max_verify_time)

    return {
        "file_id": complete_result["fileID"],
        "filename": filename,
        "size": file_size
    }


def single_upload(file_path: str, folder_id: int) -> dict:
    """Single-step upload for small files (<1GB)."""
    file_path = Path(file_path)
    filename = file_path.name
    file_size = file_path.stat().st_size
    etag = get_md5(str(file_path))

    upload_domain = get_upload_domain()
    url = f"{upload_domain}/upload/v2/file/single/create"

    headers = get_upload_headers()

    data = {
        "parentFileID": folder_id,
        "filename": filename,
        "etag": etag,
        "size": file_size,
        "duplicate": 1
    }

    with open(file_path, "rb") as f:
        files = {"file": (filename, f)}
        resp = requests.post(url, headers=headers, data=data, files=files, timeout=300)

    resp.raise_for_status()
    result = resp.json()

    if result.get("code") != 0:
        raise Exception(f"Upload failed: {result.get('message', 'Unknown error')}")

    return {
        "file_id": result["data"]["fileID"],
        "filename": filename,
        "size": file_size
    }


def get_direct_link(file_id: int) -> str:
    """Get direct link for a file."""
    resp = requests.get(
        f"{API_BASE}/api/v1/direct-link/url",
        headers=get_headers(),
        params={"fileID": file_id},
        timeout=30
    )
    resp.raise_for_status()
    result = resp.json()

    if result.get("code") != 0:
        raise Exception(f"Failed to get direct link: {result.get('message', 'Unknown error')}")

    return result["data"]["url"]


def create_share_link(file_id: int, filename: str) -> str:
    """Create share link for a file."""
    resp = requests.post(
        f"{API_BASE}/api/v1/share/create",
        headers=get_headers(),
        json={
            "shareName": filename,
            "shareExpire": 0,
            "fileIDList": str(file_id)
        },
        timeout=30
    )
    resp.raise_for_status()
    result = resp.json()

    if result.get("code") != 0:
        raise Exception(f"Failed to create share link: {result.get('message', 'Unknown error')}")

    share_key = result["data"]["shareKey"]
    return f"https://www.123pan.com/s/{share_key}"


def get_short_direct_link(file_id: int) -> str:
    """Generate short direct link using fileID only."""
    user_id = get_user_id_from_token()
    if not user_id:
        # Fallback to getting from API
        direct_link = get_direct_link(file_id)
        # Extract user_id from URL: https://{user_id}.v.123pan.cn/...
        parts = direct_link.split(".")
        if parts:
            user_id = parts[0].split("//")[-1]
    return f"https://{user_id}.v.123pan.cn/{user_id}/{file_id}"


def upload_and_get_link(file_path: str, folder_id: int = None, link_type: str = "short_direct", max_verify_time: int = None) -> dict:
    """Upload file and get link.

    link_type options:
    - short_direct: Short direct link (default, recommended)
    - share: Share page link (requires login/redirect)
    - direct: Full direct link with filename
    
    max_verify_time: Maximum time to wait for server verification in seconds (auto-calculated if not specified)
    """
    if folder_id is None:
        folder_id = int(get_config("folder_id", "PAN123_DIRECT_FOLDER_ID", "0"))

    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    file_size = file_path.stat().st_size
    
    # Check file size limit (10GB API limit)
    TEN_GB = 10 * 1024 * 1024 * 1024
    if file_size >= TEN_GB:
        raise ValueError(
            f"File size ({file_size / (1024**3):.2f} GB) exceeds API limit (10 GB). "
            f"Please use WebDAV for large file uploads."
        )
    elif file_size >= TEN_GB * 0.9:  # Warn at 9GB
        print(
            f"WARNING: File size ({file_size / (1024**3):.2f} GB) is close to API limit (10 GB). "
            f"Consider using WebDAV for more reliable large file uploads.",
            file=sys.stderr
        )

    if file_size < 1024 * 1024 * 1024:
        result = single_upload(str(file_path), folder_id)
    else:
        result = chunked_upload(str(file_path), folder_id, max_verify_time=max_verify_time)

    file_id = result["file_id"]
    filename = result["filename"]

    if link_type == "share":
        link = create_share_link(file_id, filename)
        link_type_str = "share_link"
    elif link_type == "direct":
        link = get_direct_link(file_id)
        link_type_str = "direct_link"
    else:  # short_direct (default)
        link = get_short_direct_link(file_id)
        link_type_str = "short_direct_link"

    return {
        "success": True,
        "file_id": file_id,
        "filename": filename,
        "size": result["size"],
        "link": link,
        "link_type": link_type_str
    }


def main():
    parser = argparse.ArgumentParser(description="Upload files to 123pan")
    parser.add_argument("--file", required=True, help="Path to file to upload")
    parser.add_argument("--folder", type=int, help="Target folder ID")
    parser.add_argument("--link-type", choices=["short_direct", "share", "direct"],
                       default="short_direct", help="Type of link to return")
    parser.add_argument("--max-verify-time", type=int, metavar="SECONDS",
                       help="Maximum time to wait for server verification (auto-calculated based on file size if not specified)")
    args = parser.parse_args()

    try:
        result = upload_and_get_link(args.file, args.folder, args.link_type, max_verify_time=args.max_verify_time)
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(json.dumps({"success": False, "error": str(e)}, indent=2), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
