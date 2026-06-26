import os
import sys
import mimetypes
import urllib.request
import urllib.error
import json
from typing import Optional
import argparse

# Get API Key from environment variable
API_KEY = os.environ.get("WAYIN_API_KEY")

if not API_KEY:
    print("Error: WAYIN_API_KEY environment variable is not set.")
    sys.exit(1)

def upload_local_file_to_wayinvideo(file_path: str) -> Optional[str]:
    """
    Upload a local video or audio file to WayinVideo and return the file identifier (identity).
    
    Note:
    1. The file identifier (identity) is for one-time use.
    2. The maximum file size limit for a single upload is 5 GB.
    3. The returned identity can be used as the video_url in subsequent APIs (e.g., AI editing, video summary, etc.).
    
    :param file_path: The absolute or relative path of the local file to be uploaded
    :return: Returns the identity string of the file on success, raises an exception or returns None on failure
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)
    
    # Limit check: 5GB
    if file_size > 5 * 1024 * 1024 * 1024:
        raise ValueError("File size exceeds the 5GB limit.")

    content_type, _ = mimetypes.guess_type(file_path)
    allowed_mimetypes = ["video/x-msvideo", "video/mp4", "video/quicktime", "video/webm"]
    
    if content_type not in allowed_mimetypes:
        # Fallback for common extensions if mimetype detection is incomplete
        file_extension = os.path.splitext(file_name)[1].lower().strip(".")
        allowed_extensions = ["avi", "mp4", "mov", "webm"]
        if file_extension not in allowed_extensions:
            raise ValueError(f"Invalid file type: {content_type or 'unknown'}. Only MP4, AVI, MOV, and WEBM video files are supported.")

    # ---------------------------------------------------------
    # Step 1: Get the presigned upload URL and identity
    # ---------------------------------------------------------
    init_url = "https://wayinvideo-api.wayin.ai/api/v2/upload/single-file"
    init_headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",
        "x-wayinvideo-api-version": "v2",
        "user-agent": "ai-clipping skill"
    }
    init_payload = json.dumps({"name": file_name}).encode("utf-8")

    try:
        req = urllib.request.Request(init_url, data=init_payload, headers=init_headers, method="POST")
        with urllib.request.urlopen(req, timeout=30) as response:
            init_data = json.loads(response.read().decode("utf-8"))
        
        upload_url = init_data["data"]["upload_url"]
        identity = init_data["data"]["identity"]
        
    except urllib.error.URLError as e:
        raise Exception(f"Network exception when requesting WayinVideo API: {str(e)}")

    # ---------------------------------------------------------
    # Step 2: Upload the actual file using the presigned URL
    # ---------------------------------------------------------
    if not content_type:
        content_type = "application/octet-stream"

    upload_headers = {
        "Content-Type": content_type
    }

    try:
        # Use stream reading to avoid loading large files directly into memory
        with open(file_path, 'rb') as f:
            req = urllib.request.Request(upload_url, data=f, headers=upload_headers, method="PUT")
            req.add_header("Content-Length", str(file_size))
            with urllib.request.urlopen(req) as response:
                if response.getcode() not in (200, 201, 204):
                    raise Exception(f"Failed to upload file. Status code: {response.getcode()}")
            
    except urllib.error.URLError as e:
        raise Exception(f"Failed to upload file to the presigned link: {str(e)}")

    # Return the credential for subsequent API calls
    return identity

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file-path", required=True)
    args = parser.parse_args()

    try:
        print(f"Starting to upload file: {args.file_path}")
        file_identity = upload_local_file_to_wayinvideo(args.file_path)
        print("Upload successful!")
        print(f"Please use the following identity as the video_url in subsequent API requests:\n{file_identity}")
    except Exception as e:
        print(f"Error occurred during upload: {e}")

if __name__ == "__main__":
    main()
