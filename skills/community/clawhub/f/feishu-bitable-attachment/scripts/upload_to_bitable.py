"""
Upload file to Feishu Bitable module.

Responsibilities:
- Upload local file to Feishu Bitable upload endpoint
- Small files (≤20MB): direct upload
- Large files (>20MB): chunked upload
- Return file_token for use in attachment field

Important:
- parent_type must be 'bitable_file'
- parent_node must be the app_token
- drive_route_token must be the app_token

API Reference (Feishu Drive Upload):
- Direct upload: POST /open-apis/drive/v1/upload
- Chunked prepare: POST /open-apis/drive/v1/chunked_upload/prepare
- Chunked upload: POST /open-apis/drive/v1/chunked_upload
- Chunked finish: POST /open-apis/drive/v1/chunked_upload/finish
"""

import os
import json
from typing import Dict, Any, Optional, List
from dataclasses import dataclass

from common import (
    log,
    make_request,
    make_authenticated_request,
    get_feishu_base_url,
    get_tenant_access_token,
    get_file_size,
    FeishuUploadError,
    FeishuAPIError,
    SkillFileNotFoundError,
    API_UPLOAD_MATERIAL,
    API_CHUNKED_UPLOAD_PREPARE,
    API_CHUNKED_UPLOAD,
    API_CHUNKED_UPLOAD_FINISH,
    CHUNKED_UPLOAD_THRESHOLD,
    DEFAULT_CHUNK_SIZE,
)


@dataclass
class UploadResult:
    """Result of uploading file to Bitable."""
    file_token: str
    file_name: str
    file_size: int
    upload_type: str  # 'direct' or 'chunked'


def upload_to_bitable(
    file_path: str,
    app_token: str,
    app_id: str,
    app_secret: str,
    filename: Optional[str] = None
) -> UploadResult:
    """
    Upload file to Feishu Bitable.

    Automatically chooses direct upload (≤20MB) or chunked upload (>20MB).

    Args:
        file_path: Local path to the file
        app_token: Bitable app token (used as parent_node and drive_route_token)
        app_id: Feishu app ID
        app_secret: Feishu app secret
        filename: Optional filename override

    Returns:
        UploadResult with file_token

    Raises:
        SkillFileNotFoundError: If file doesn't exist
        FeishuUploadError: If upload fails
    """
    if not os.path.exists(file_path):
        raise SkillFileNotFoundError(f"File not found: {file_path}")

    file_size = get_file_size(file_path)
    filename = filename or os.path.basename(file_path)

    log.info("=" * 50)
    log.info("Upload Stage: Starting file upload")
    log.info(f"  File: {filename}")
    log.info(f"  Size: {file_size} bytes")
    log.info(f"  Target app_token: {app_token}")
    log.info(f"  Upload type threshold: {CHUNKED_UPLOAD_THRESHOLD} bytes (20MB)")

    if file_size <= CHUNKED_UPLOAD_THRESHOLD:
        log.info("Using DIRECT upload (file <= 20MB)")
        log.info(f"Direct upload endpoint: {get_feishu_base_url()}{API_UPLOAD_MATERIAL}")
        # Pass file_size to upload_small_file to avoid recalculating
        result = upload_small_file(file_path, app_token, app_id, app_secret, filename, file_size)
        log.info(f"Direct upload completed. file_token: {result.file_token}")
        return result
    else:
        log.info("Using CHUNKED upload (file > 20MB)")
        log.info(f"Chunked upload base endpoint: {get_feishu_base_url()}{API_CHUNKED_UPLOAD_PREPARE}")
        result = upload_large_file(file_path, app_token, app_id, app_secret, filename)
        log.info(f"Chunked upload completed. file_token: {result.file_token}")
        return result


# ============================================================================
# Target Parameter Building
# ============================================================================

def build_upload_target_params(app_token: str) -> Dict[str, Any]:
    """
    Build upload parameters for bitable_file upload point.

    The key insight: to upload a file that can be used in Bitable attachment fields,
    we must specify:
    - parent_type = bitable_file (this is the upload destination type)
    - parent_node = app_token (the target Bitable)
    - drive_route_token = app_token (route through Bitable's storage)

    Args:
        app_token: Bitable app token

    Returns:
        Dict with upload parameters
    """
    # extra must be a JSON string, not a nested object
    extra_json = json.dumps({"drive_route_token": app_token})

    return {
        "parent_type": "bitable_file",
        "parent_node": app_token,
        "extra": extra_json,
    }


def parse_file_token(response_data: Dict[str, Any]) -> str:
    """
    Parse upload response and extract file_token.

    Args:
        response_data: Response from upload API

    Returns:
        file_token string

    Raises:
        FeishuUploadError: If file_token is missing or API returned error
    """
    # Check for API-level error code
    code = response_data.get("code")
    if code is not None and code != 0:
        msg = response_data.get("msg", "Unknown error")
        raise FeishuUploadError(f"Upload failed: {code} - {msg}")

    # Extract file_token from data
    file_info = response_data.get("data", {})
    file_token = file_info.get("file_token")

    if not file_token:
        raise FeishuUploadError(
            f"Upload succeeded but no file_token returned. Response: {response_data}"
        )

    return file_token


# ============================================================================
# Small File Upload (≤20MB) - Direct Upload
# ============================================================================

def upload_small_file(
    file_path: str,
    app_token: str,
    app_id: str,
    app_secret: str,
    filename: str,
    file_size: Optional[int] = None
) -> UploadResult:
    """
    Direct upload for small files (≤20MB).

    Uses multipart/form-data POST to upload endpoint.

    Multipart fields:
    - file: The actual file content
    - file_name: Name of the file
    - parent_type: Must be 'bitable_file'
    - parent_node: The app_token
    - extra: JSON string with drive_route_token

    Args:
        file_path: Local path to the file
        app_token: Bitable app token
        app_id: Feishu app ID
        app_secret: Feishu app secret
        filename: Filename

    Returns:
        UploadResult with file_token

    Raises:
        FeishuUploadError: If upload fails
    """
    import requests

    base_url = get_feishu_base_url()
    token = get_tenant_access_token(app_id, app_secret)
    url = f"{base_url}{API_UPLOAD_MATERIAL}"

    # Log the actual upload endpoint being used
    log.info(f"Direct upload endpoint: {url}")

    # Ensure file_size is available (calculate if not provided)
    if file_size is None:
        file_size = get_file_size(file_path)

    # Prepare multipart form data for upload_all endpoint
    # The upload_all endpoint expects the file in a specific format
    # All parameters must be in files dict for proper multipart encoding
    files = {
        "file": (filename, open(file_path, "rb"), "application/octet-stream"),
        "file_name": (None, filename),
        "size": (None, str(file_size)),
        "parent_type": (None, "bitable_file"),
        "parent_node": (None, app_token),
        "extra": (None, json.dumps({"drive_route_token": app_token})),
    }

    headers = {
        "Authorization": f"Bearer {token}"
    }

    # Log the actual upload endpoint being used
    log.info(f"Upload all endpoint URL: {url}")
    log.info(f"Form fields: file_name={filename}, size={file_size}, parent_type=bitable_file, parent_node={app_token}")

    try:
        response = requests.post(
            url,
            headers=headers,
            files=files,
            timeout=120
        )
        response.raise_for_status()
        response_data = response.json()
    except requests.RequestException as e:
        raise FeishuUploadError(f"Direct upload request failed: {str(e)}")
    finally:
        # Ensure file handle is closed
        files["file"][1].close()

    # Parse response and extract file_token
    file_token = parse_file_token(response_data)
    uploaded_size = response_data.get("data", {}).get("size", file_size)

    log.info(f"Direct upload successful. file_token: {file_token}")

    return UploadResult(
        file_token=file_token,
        file_name=filename,
        file_size=uploaded_size,
        upload_type="direct"
    )


# ============================================================================
# Large File Upload (>20MB) - Chunked Upload
# ============================================================================

def upload_large_file(
    file_path: str,
    app_token: str,
    app_id: str,
    app_secret: str,
    filename: str
) -> UploadResult:
    """
    Chunked upload for large files (>20MB).

    Flow:
    1. Prepare: Get upload_id
    2. Upload parts: Upload file in 5MB chunks
    3. Finish: Complete upload and get file_token

    Args:
        file_path: Local path to the file
        app_token: Bitable app token
        app_id: Feishu app ID
        app_secret: Feishu app secret
        filename: Filename

    Returns:
        UploadResult with file_token

    Raises:
        FeishuUploadError: If any step fails
    """
    base_url = get_feishu_base_url()
    token = get_tenant_access_token(app_id, app_secret)
    file_size = get_file_size(file_path)

    # Step 1: Prepare chunked upload
    log.info("Step 1/3: Preparing chunked upload")
    upload_id = prepare_large_upload(
        filename, file_size, app_token, base_url, token
    )
    log.info(f"Got upload_id: {upload_id}")

    # Step 2: Upload parts
    log.info("Step 2/3: Uploading file parts")
    part_etags = upload_large_file_parts(
        file_path, upload_id, filename, base_url, token
    )
    log.info(f"Uploaded {len(part_etags)} parts")

    # Step 3: Finish chunked upload
    log.info("Step 3/3: Finishing chunked upload")
    file_token = finish_large_upload(
        upload_id, part_etags, filename, app_token, base_url, token
    )

    log.info(f"Chunked upload successful. file_token: {file_token}")

    return UploadResult(
        file_token=file_token,
        file_name=filename,
        file_size=file_size,
        upload_type="chunked"
    )


def prepare_large_upload(
    filename: str,
    file_size: int,
    app_token: str,
    base_url: str,
    token: str
) -> str:
    """
    Prepare chunked upload and get upload_id.

    Args:
        filename: Name of the file
        file_size: Size in bytes
        app_token: Bitable app token
        base_url: Feishu API base URL
        token: tenant_access_token

    Returns:
        upload_id string

    Raises:
        FeishuUploadError: If prepare fails
    """
    url = f"{base_url}{API_CHUNKED_UPLOAD_PREPARE}"
    log.info(f"Chunked upload prepare endpoint: {url}")

    payload = {
        "file_name": filename,
        "file_size": file_size,
        "parent_type": "bitable_file",
        "parent_node": app_token,
        "drive_route_token": app_token,
    }

    headers = {"Authorization": f"Bearer {token}"}

    try:
        response_data = make_request("POST", url, headers=headers, json_body=payload)
    except FeishuAPIError as e:
        raise FeishuUploadError(f"Chunked upload prepare failed: {e.message}")

    upload_id = response_data.get("data", {}).get("upload_id")
    if not upload_id:
        raise FeishuUploadError("Prepare failed: no upload_id in response")

    return upload_id


def upload_large_file_parts(
    file_path: str,
    upload_id: str,
    filename: str,
    base_url: str,
    token: str,
    chunk_size: int = DEFAULT_CHUNK_SIZE
) -> List[str]:
    """
    Upload file in parts.

    Args:
        file_path: Local path to the file
        upload_id: Upload session ID
        filename: Name of the file
        base_url: Feishu API base URL
        token: tenant_access_token
        chunk_size: Size of each chunk (default 5MB)

    Returns:
        List of part ETags

    Raises:
        FeishuUploadError: If any part upload fails
    """
    part_etags = []
    part_number = 1

    with open(file_path, "rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break

            log.info(f"Uploading part {part_number} ({len(chunk)} bytes)")

            etag = upload_large_file_part(
                chunk, upload_id, part_number, filename,
                base_url, token
            )
            part_etags.append(etag)
            part_number += 1

    return part_etags


def upload_large_file_part(
    chunk: bytes,
    upload_id: str,
    part_number: int,
    filename: str,
    base_url: str,
    token: str
) -> str:
    """
    Upload a single part of chunked upload.

    Args:
        chunk: File chunk bytes
        upload_id: Upload session ID
        part_number: Part number (1-indexed)
        filename: Name of the file
        base_url: Feishu API base URL
        token: tenant_access_token

    Returns:
        ETag string for this part

    Raises:
        FeishuUploadError: If upload fails
    """
    import requests

    url = f"{base_url}{API_CHUNKED_UPLOAD}"
    log.debug(f"Chunked upload part endpoint: {url}")

    # Multipart form data for part upload
    files = {
        "file": chunk
    }

    data = {
        "upload_id": upload_id,
        "part_number": part_number,
        "file_name": filename,
    }

    headers = {
        "Authorization": f"Bearer {token}"
    }

    try:
        response = requests.post(
            url,
            headers=headers,
            data=data,
            files=files,
            timeout=120
        )
        response.raise_for_status()
        response_data = response.json()
    except requests.RequestException as e:
        raise FeishuUploadError(f"Part {part_number} upload failed: {str(e)}")

    # Check for API error
    code = response_data.get("code")
    if code is not None and code != 0:
        msg = response_data.get("msg", "Unknown error")
        raise FeishuUploadError(f"Part {part_number} upload failed: {code} - {msg}")

    etag = response_data.get("data", {}).get("etag")
    if not etag:
        raise FeishuUploadError(f"Part {part_number} succeeded but no etag returned")

    return etag


def finish_large_upload(
    upload_id: str,
    part_etags: List[str],
    filename: str,
    app_token: str,
    base_url: str,
    token: str
) -> str:
    """
    Finish chunked upload and get file_token.

    Args:
        upload_id: Upload session ID
        part_etags: List of part ETags
        filename: Name of the file
        app_token: Bitable app token
        base_url: Feishu API base URL
        token: tenant_access_token

    Returns:
        file_token string

    Raises:
        FeishuUploadError: If finish fails
    """
    url = f"{base_url}{API_CHUNKED_UPLOAD_FINISH}"
    log.info(f"Chunked upload finish endpoint: {url}")

    # Build parts list with index (1-indexed) and etag
    parts = [
        {"index": i + 1, "etag": etag}
        for i, etag in enumerate(part_etags)
    ]

    payload = {
        "upload_id": upload_id,
        "parts": parts,
        "file_name": filename,
        "parent_type": "bitable_file",
        "parent_node": app_token,
        "drive_route_token": app_token,
    }

    headers = {"Authorization": f"Bearer {token}"}

    try:
        response_data = make_request("POST", url, headers=headers, json_body=payload)
    except FeishuAPIError as e:
        raise FeishuUploadError(f"Chunked upload finish failed: {e.message}")

    file_token = response_data.get("data", {}).get("file_token")
    if not file_token:
        raise FeishuUploadError("Finish failed: no file_token in response")

    return file_token
