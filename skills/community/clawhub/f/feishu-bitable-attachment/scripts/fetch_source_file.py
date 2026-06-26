"""
Fetch source file module.

Responsibilities:
- Support source_type = local (copy from local path)
- Support source_type = url (download from URL)
- Support source_type = feishu_message (download from Feishu message attachment)
- Save source file to local temp directory
- Return: local_file_path, filename, mime_type, file_size
"""

import os
import tempfile
import shutil
from typing import Dict, Any, Optional
from dataclasses import dataclass

import requests

from common import (
    log,
    make_request,
    get_tenant_access_token,
    get_feishu_base_url,
    detect_mime_type,
    get_file_size,
    SkillFileNotFoundError,
    SkillDownloadError,
    SkillInputError,
)


@dataclass
class FetchResult:
    """Result of fetching source file."""
    local_file_path: str
    filename: str
    mime_type: str
    file_size: int


def fetch_source_file(source: Dict[str, Any], app_id: Optional[str] = None, app_secret: Optional[str] = None) -> FetchResult:
    """
    Fetch source file based on source type.

    Args:
        source: Source config with 'type' and 'ref' fields
            - type: "local", "url", or "feishu_message"
            - ref: file path, URL, or dict with file_key
        app_id: Feishu app ID (required for feishu_message type)
        app_secret: Feishu app secret (required for feishu_message type)

    Returns:
        FetchResult with local file path and metadata

    Raises:
        SkillInputError: If source type is invalid or required params missing
        SkillFileNotFoundError: If local file doesn't exist
        SkillDownloadError: If download fails
    """
    source_type = source.get("type")
    ref = source.get("ref")

    if not source_type:
        raise SkillInputError("Source 'type' is required. Must be one of: local, url, feishu_message")
    if ref is None:
        raise SkillInputError("Source 'ref' is required")

    if source_type == "local":
        return _fetch_local(ref)
    elif source_type == "url":
        return _fetch_url(ref)
    elif source_type == "feishu_message":
        if not app_id or not app_secret:
            raise SkillInputError("Feishu message source requires app_id and app_secret")
        return _fetch_feishu_message(ref, app_id, app_secret)
    else:
        raise SkillInputError(
            f"Invalid source type: '{source_type}'. Must be one of: local, url, feishu_message"
        )


def _fetch_local(file_path: str) -> FetchResult:
    """
    Fetch file from local path.

    Args:
        file_path: Absolute path to local file

    Returns:
        FetchResult with copied file path

    Raises:
        SkillFileNotFoundError: If file doesn't exist
    """
    # Normalize path (expand ~)
    file_path = os.path.expanduser(file_path)

    if not os.path.exists(file_path):
        raise SkillFileNotFoundError(f"Local file not found: {file_path}")

    if not os.path.isfile(file_path):
        raise SkillInputError(f"Path is not a file: {file_path}")

    # Get filename
    filename = os.path.basename(file_path)

    # Create temp directory and copy file
    temp_dir = tempfile.mkdtemp(prefix="feishu_bitable_")
    temp_file_path = os.path.join(temp_dir, filename)

    shutil.copy2(file_path, temp_file_path)

    file_size = get_file_size(temp_file_path)
    log.info(f"Copied local file to temp: {temp_file_path} ({file_size} bytes)")

    return FetchResult(
        local_file_path=temp_file_path,
        filename=filename,
        mime_type=detect_mime_type(file_path),
        file_size=file_size
    )


def _fetch_url(url: str) -> FetchResult:
    """
    Download file from URL.

    Args:
        url: Download URL

    Returns:
        FetchResult with downloaded file path

    Raises:
        SkillDownloadError: If download fails
    """
    log.info(f"Downloading file from URL: {url}")

    try:
        response = requests.get(url, stream=True, timeout=120)
        response.raise_for_status()
    except requests.RequestException as e:
        raise SkillDownloadError(f"Failed to download from URL: {str(e)}")

    # Extract filename from Content-Disposition header or URL
    filename = _extract_filename_from_response(response, url)

    # Create temp directory
    temp_dir = tempfile.mkdtemp(prefix="feishu_bitable_")
    temp_file_path = os.path.join(temp_dir, filename)

    # Download file
    total_size = 0
    with open(temp_file_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
            total_size += len(chunk)

    log.info(f"Downloaded {total_size} bytes to {temp_file_path}")

    return FetchResult(
        local_file_path=temp_file_path,
        filename=filename,
        mime_type=response.headers.get("Content-Type", "application/octet-stream"),
        file_size=total_size
    )


def _extract_filename_from_response(response: requests.Response, url: str) -> str:
    """
    Extract filename from Content-Disposition header or URL.

    Args:
        response: HTTP response
        url: Original URL

    Returns:
        Filename string
    """
    # Try Content-Disposition header first
    content_disposition = response.headers.get("Content-Disposition", "")
    if content_disposition:
        # Parse filename from Content-Disposition
        for part in content_disposition.split(";"):
            part = part.strip()
            if part.startswith("filename="):
                filename = part.split("=", 1)[1].strip("\"'")
                return filename
            if part.startswith("filename*="):
                # RFC 5987 encoding (e.g., utf-8''filename.ext)
                filename = part.split("=", 1)[1].strip("\"'")
                if "'" in filename:
                    parts = filename.split("''", 1)
                    if len(parts) == 2:
                        return parts[1]

    # Fall back to URL
    filename = os.path.basename(url.split("?")[0])
    if filename and filename != "/":
        return filename

    # Default filename
    return "downloaded_file"


def _fetch_feishu_message(ref: Dict[str, Any], app_id: str, app_secret: str) -> FetchResult:
    """
    Download file from Feishu message attachment.

    The ref should contain:
    - file_key: The file key from the message (required)
    - filename: Optional filename override
    - message_id: Optional message ID (for future use)

    Note on Feishu message attachments:
    - File messages contain a file_key that can be used with Drive API
    - The Drive API provides file info and download endpoints
    - This implementation uses the standard Drive file download endpoint

    Args:
        ref: Dict with file_key and optional filename
        app_id: Feishu app ID
        app_secret: Feishu app secret

    Returns:
        FetchResult with downloaded file path

    Raises:
        SkillInputError: If file_key is missing
        SkillDownloadError: If download fails
    """
    log.info("Fetching file from Feishu message")

    # Parse ref
    if isinstance(ref, str):
        # If ref is a string, treat it as file_key
        file_key = ref
        filename = None
    elif isinstance(ref, dict):
        file_key = ref.get("file_key") or ref.get("fileToken")
        filename = ref.get("filename")
        # message_id and download_url are reserved for future use
    else:
        raise SkillInputError("Feishu message ref must be a string file_key or dict with file_key")

    if not file_key:
        raise SkillInputError("file_key is required for Feishu message source")

    # Get tenant access token
    token = get_tenant_access_token(app_id, app_secret)
    base_url = get_feishu_base_url()

    # Step 1: Try to get file info from Drive API (optional, for filename)
    if not filename:
        try:
            file_info_url = f"{base_url}/open-apis/drive/v1/files/{file_key}"
            file_info_response = make_request(
                "GET",
                file_info_url,
                headers={"Authorization": f"Bearer {token}"}
            )
            file_info = file_info_response.get("data", {})
            filename = file_info.get("name") or file_info.get("file_name")
            if filename:
                log.info(f"Retrieved filename from Drive API: {filename}")
        except Exception as e:
            log.warning(f"Could not get file info: {e}")

    # Use default filename if still not found
    if not filename:
        filename = f"feishu_attachment_{file_key[:16]}"

    # Step 2: Download the file
    # Feishu Drive API provides a download endpoint
    download_url = f"{base_url}/open-apis/drive/v1/files/{file_key}/download"

    log.info(f"Downloading from Feishu Drive: {file_key}")

    try:
        response = requests.get(
            download_url,
            headers={"Authorization": f"Bearer {token}"},
            stream=True,
            timeout=120
        )
        response.raise_for_status()
    except requests.RequestException as e:
        raise SkillDownloadError(f"Failed to download from Feishu message: {str(e)}")

    # Create temp directory
    temp_dir = tempfile.mkdtemp(prefix="feishu_bitable_")
    temp_file_path = os.path.join(temp_dir, filename)

    # Download file
    total_size = 0
    with open(temp_file_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
            total_size += len(chunk)

    log.info(f"Downloaded {total_size} bytes from Feishu message to {temp_file_path}")

    return FetchResult(
        local_file_path=temp_file_path,
        filename=filename,
        mime_type=detect_mime_type(temp_file_path),
        file_size=total_size
    )


def cleanup_temp_file(file_path: str) -> None:
    """
    Clean up temporary file and directory.

    Args:
        file_path: Path to the temporary file
    """
    try:
        # Get parent directory
        temp_dir = os.path.dirname(file_path)

        # Remove file
        if os.path.exists(file_path):
            os.remove(file_path)

        # Remove directory if it's our temp dir
        if temp_dir and "feishu_bitable" in temp_dir and os.path.exists(temp_dir):
            try:
                os.rmdir(temp_dir)
            except OSError:
                # Directory may not be empty, ignore
                pass

        log.info(f"Cleaned up temp file: {file_path}")
    except Exception as e:
        log.warning(f"Failed to clean up temp file {file_path}: {e}")
