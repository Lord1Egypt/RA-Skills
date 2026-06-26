#!/usr/bin/env python3
"""
colab_drive.py — Upload/download files between local machine and Colab runtime via Google Drive API.

This avoids the interactive drive.mount() by using the Drive REST API directly
with the same OAuth credentials used for Colab.

Usage:
    # Upload a file to Drive (for Colab to read)
    python3 colab_drive.py upload local_file.py --folder colab-workspace

    # Download a file from Drive (after Colab writes it)
    python3 colab_drive.py download "checkpoint.pt" --output ./checkpoint.pt

    # List files in a Drive folder
    python3 colab_drive.py list --folder colab-workspace

Inside Colab scripts, use these helpers to read/write Drive:
    # At the START of your Colab script:
    from google.colab import auth
    auth.authenticate_user()
    
    # Then use gdown or the Drive API:
    from google.colab import drive
    drive.mount('/content/drive')  # Works after authenticate_user()
"""

import argparse
import json
import os
import sys

VENV_PYTHON = os.path.join(os.path.dirname(__file__), ".colab-venv", "bin", "python")
if os.path.exists(VENV_PYTHON) and sys.executable != VENV_PYTHON:
    os.execv(VENV_PYTHON, [VENV_PYTHON] + sys.argv)

import requests
from google.auth.transport.requests import Request as GoogleRequest
from google.auth.transport import requests as google_requests
from google.oauth2.credentials import Credentials

TOKEN_PATH = os.path.expanduser("~/.colab-mcp-auth-token.json")
SCOPES = [
    "https://www.googleapis.com/auth/userinfo.profile",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/colaboratory",
    "https://www.googleapis.com/auth/drive.file",
    "openid",
]

DRIVE_API = "https://www.googleapis.com/drive/v3"
DRIVE_UPLOAD_API = "https://www.googleapis.com/upload/drive/v3"


def get_session():
    if not os.path.exists(TOKEN_PATH):
        print(f"Error: No auth token at {TOKEN_PATH}", file=sys.stderr)
        sys.exit(1)
    creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    if not creds.valid and creds.expired and creds.refresh_token:
        creds.refresh(GoogleRequest())
        with open(TOKEN_PATH, "w") as f:
            f.write(creds.to_json())
    return google_requests.AuthorizedSession(creds)


def find_or_create_folder(session, name):
    """Find or create a Drive folder by name.
    
    With drive.file scope, we can only see files created by this app.
    So first try to find, and if 403 or empty, create.
    """
    # Search for existing folder (may 403 with drive.file scope if not created by us)
    try:
        resp = session.get(f"{DRIVE_API}/files", params={
            "q": f"name='{name}' and mimeType='application/vnd.google-apps.folder' and trashed=false",
            "fields": "files(id,name)",
        })
        if resp.ok:
            files = resp.json().get("files", [])
            if files:
                return files[0]["id"]
    except Exception:
        pass

    # Create folder (drive.file scope allows creating new files)
    resp = session.post(f"{DRIVE_API}/files", json={
        "name": name,
        "mimeType": "application/vnd.google-apps.folder",
    })
    resp.raise_for_status()
    folder_id = resp.json()["id"]
    print(f"Created Drive folder: {name} (id={folder_id})", file=sys.stderr)
    return folder_id


def upload_file(session, local_path, folder_name="colab-workspace"):
    """Upload a file to a Drive folder."""
    folder_id = find_or_create_folder(session, folder_name)
    filename = os.path.basename(local_path)

    # Multipart upload
    metadata = {"name": filename, "parents": [folder_id]}
    with open(local_path, "rb") as f:
        resp = session.post(
            f"{DRIVE_UPLOAD_API}/files?uploadType=multipart",
            files={
                "metadata": ("metadata", json.dumps(metadata), "application/json"),
                "file": (filename, f),
            },
        )
    resp.raise_for_status()
    file_id = resp.json()["id"]
    print(f"Uploaded: {filename} → Drive/{folder_name}/ (id={file_id})")
    return file_id


def download_file(session, filename, folder_name="colab-workspace", output=None):
    """Download a file from Drive by name."""
    query = f"name='{filename}' and trashed=false"
    if folder_name:
        folder_id = find_folder(session, folder_name)
        if not folder_id:
            print(f"Folder '{folder_name}' not found on Drive.", file=sys.stderr)
            return None
        query += f" and '{folder_id}' in parents"

    resp = session.get(f"{DRIVE_API}/files", params={
        "q": query,
        "fields": "files(id,name,size,modifiedTime)",
        "orderBy": "modifiedTime desc",
    })
    resp.raise_for_status()
    files = resp.json().get("files", [])
    if not files:
        print(f"Not found: {filename}", file=sys.stderr)
        return None

    file_id = files[0]["id"]
    out_path = output or filename

    resp = session.get(f"{DRIVE_API}/files/{file_id}", params={"alt": "media"})
    resp.raise_for_status()
    with open(out_path, "wb") as f:
        f.write(resp.content)
    print(f"Downloaded: {filename} → {out_path} ({len(resp.content)} bytes)")
    return out_path


def find_folder(session, name):
    """Find a Drive folder by name. Returns None if not found (no side effects)."""
    try:
        resp = session.get(f"{DRIVE_API}/files", params={
            "q": f"name='{name}' and mimeType='application/vnd.google-apps.folder' and trashed=false",
            "fields": "files(id,name)",
        })
        if resp.ok:
            files = resp.json().get("files", [])
            if files:
                return files[0]["id"]
    except Exception:
        pass
    return None


def list_files(session, folder_name="colab-workspace"):
    """List files in a Drive folder."""
    folder_id = find_folder(session, folder_name)
    if not folder_id:
        print(f"Folder '{folder_name}' not found on Drive.", file=sys.stderr)
        return
    resp = session.get(f"{DRIVE_API}/files", params={
        "q": f"'{folder_id}' in parents and trashed=false",
        "fields": "files(id,name,size,modifiedTime,mimeType)",
        "orderBy": "modifiedTime desc",
    })
    resp.raise_for_status()
    for f in resp.json().get("files", []):
        size = f.get("size", "?")
        print(f"  {f['name']:<40} {size:>10}  {f.get('modifiedTime', '')[:19]}")


# ─── Colab-side helpers (to embed in scripts) ───────────────────────────────

COLAB_DRIVE_SETUP = """
# === Drive persistence helpers ===
# Run this at the START of your Colab script to enable Drive access.
import os, subprocess

def save_to_drive(local_path, drive_folder='colab-workspace'):
    \"\"\"Save a file from Colab runtime to Google Drive.\"\"\"
    from google.colab import drive
    if not os.path.exists('/content/drive'):
        from google.colab import auth
        auth.authenticate_user()
        drive.mount('/content/drive')
    dest = f'/content/drive/MyDrive/{drive_folder}'
    os.makedirs(dest, exist_ok=True)
    import shutil
    shutil.copy2(local_path, dest)
    print(f'Saved: {local_path} → {dest}/')

def load_from_drive(filename, drive_folder='colab-workspace', local_path=None):
    \"\"\"Load a file from Google Drive to Colab runtime.\"\"\"
    from google.colab import drive
    if not os.path.exists('/content/drive'):
        from google.colab import auth
        auth.authenticate_user()
        drive.mount('/content/drive')
    src = f'/content/drive/MyDrive/{drive_folder}/{filename}'
    if not os.path.exists(src):
        print(f'Not found on Drive: {src}')
        return None
    dest = local_path or f'/tmp/{filename}'
    import shutil
    shutil.copy2(src, dest)
    print(f'Loaded: {src} → {dest}')
    return dest
"""


def main():
    parser = argparse.ArgumentParser(description="Upload/download files to/from Google Drive for Colab")
    sub = parser.add_subparsers(dest="command")

    p_up = sub.add_parser("upload", help="Upload file to Drive")
    p_up.add_argument("path", help="Local file to upload")
    p_up.add_argument("--folder", default="colab-workspace", help="Drive folder name")

    p_down = sub.add_parser("download", help="Download file from Drive")
    p_down.add_argument("filename", help="File name on Drive")
    p_down.add_argument("--folder", default="colab-workspace", help="Drive folder name")
    p_down.add_argument("--output", "-o", help="Local output path")

    p_list = sub.add_parser("list", help="List files in Drive folder")
    p_list.add_argument("--folder", default="colab-workspace", help="Drive folder name")

    p_helpers = sub.add_parser("helpers", help="Print Colab-side Drive helper code")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == "helpers":
        print(COLAB_DRIVE_SETUP)
        return

    session = get_session()

    if args.command == "upload":
        upload_file(session, args.path, args.folder)
    elif args.command == "download":
        download_file(session, args.filename, args.folder, args.output)
    elif args.command == "list":
        list_files(session, args.folder)


if __name__ == "__main__":
    main()
