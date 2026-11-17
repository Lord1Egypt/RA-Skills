---
name: dele-deploy
description: Deploy local HTML/frontend files to Dele (dele.fun) and get a live URL. Files must go through presign and direct storage PUT, never as one multipart POST to /api/upload.
allowed-tools: "read(*), glob(*)"
env:
  DELE_API_KEY:
    required: true
    description: "Dele API key. Get one at https://www.dele.fun/api-keys. POSTME_API_KEY is also accepted."
  DELE_API_URL:
    required: false
    description: "Dele origin, default https://www.dele.fun. Do not POST app files to /api/upload."
---

# Dele Deploy Skill

## Overview
This skill deploys a local HTML file or frontend folder to Dele (https://www.dele.fun) and returns a live URL.

**Do not POST application files to `/api/upload`.** dele.fun runs on Vercel. A request body over about 4.5MB is rejected with 413 `FUNCTION_PAYLOAD_TOO_LARGE` before Dele code runs. The working path is:

1. `POST /api/upload/presign` with file metadata only (JSON, no file bytes)
2. `PUT` each file to its `uploadUrl` (object storage, not Vercel)
3. `POST /api/upload/finalize` with the same metadata

If an older ClawHub install still uploads with `requests.post(..., files=...)`, update it:

```bash
openclaw skills update @del-zhenwu/dele-deploy
```

Current instructions always live at https://www.dele.fun/skill.md

## Required Environment Variables

| Variable | Description |
|---|---|
| `DELE_API_KEY` | **Required.** Dele API key. Get one at https://www.dele.fun/api-keys. `POSTME_API_KEY` is accepted as an alias. |
| `DELE_API_URL` | Optional. Dele origin, default `https://www.dele.fun`. `POSTME_API_URL` is accepted as an alias. |

## Prerequisites

1.  **Dele API Key**: Generate an API key at https://www.dele.fun/api-keys, then set it as an environment variable:
    ```env
    DELE_API_KEY="your-secret-agent-key"
    ```

2.  **Python Dependencies**: The skill requires the `requests` library.
    ```bash
    pip install requests
    ```

## Usage Instructions for the Agent
When a user asks you to deploy, publish, or share a web application (like an HTML file or a frontend project folder) that you have just created, you should use this skill.

1. Determine the absolute path to the generated folder or file (`target_path`).
2. Invent a suitable, URL-friendly name for the application (`app_name`). It must contain only lowercase letters, numbers, and hyphens.
3. Call the `dele_deploy` skill with these parameters. Read `DELE_API_KEY` from the environment; do not paste the key into app files.
4. Present the resulting URL to the user.

### Visibility Control
Apps default to **public** (visible on the Explore page). You can optionally set visibility:

| Value | Behavior |
|---|---|
| `public` | Listed on Explore, anyone can view |
| `unlisted` | Not listed, accessible via direct URL |
| `password` | Requires a 4-character access code (auto-generated, returned in response) |
| `hidden` | Only the owner can access |

If `visibility` is set to `password`, the response will include an `accessCode` (4 chars, `0-9a-z`). **Present this code to the user** so they can share it with authorized visitors.

## Example
If you generated a project in `/tmp/workspace/my-app`, you would call the skill with:
- `target_path`: `/tmp/workspace/my-app`
- `app_name`: `my-app-v1`
- `visibility`: `password` (optional)

The skill will return a success message containing the live URL, e.g., `Deployment successful! URL: https://www.dele.fun/app/my-app-v1/`
If password-protected: `Access code: x7k2`

## Tool Definition

```json
{
  "name": "dele_deploy",
  "description": "Deploy a local folder or HTML file to Dele. Uses presign, direct storage PUT, and finalize. Never multipart-posts app files to /api/upload.",
  "parameters": {
    "type": "object",
    "properties": {
      "target_path": {
        "type": "string",
        "description": "The local path to the folder or HTML file you want to deploy."
      },
      "app_name": {
        "type": "string",
        "description": "A unique, URL-friendly name for the application (lowercase letters, numbers, and hyphens only)."
      },
      "api_url": {
        "type": "string",
        "description": "Dele origin such as https://www.dele.fun. Optional."
      },
      "api_key": {
        "type": "string",
        "description": "The API key for authentication (DELE_API_KEY). Optional if the env var is set."
      },
      "app_desc": {
        "type": "string",
        "description": "A short description of what the application does."
      },
      "visibility": {
        "type": "string",
        "enum": ["public", "unlisted", "password", "hidden"],
        "description": "App visibility level. Defaults to 'public'. If set to 'password', a 4-char access code will be auto-generated and returned."
      }
    },
    "required": [
      "target_path",
      "app_name"
    ]
  }
}
```

## Python Implementation (`dele_deploy.py`)

```python
import os
import requests
import re
import mimetypes
from typing import Optional

SKIP_DIR_NAMES = {".git", "node_modules", "__pycache__", ".venv", "venv", ".next", "coverage"}
SKIP_FILE_NAMES = {".ds_store", "thumbs.db"}


def _origin(api_url: Optional[str]) -> str:
    raw = (
        api_url
        or os.environ.get("DELE_API_URL")
        or os.environ.get("POSTME_API_URL")
        or "https://www.dele.fun"
    ).strip().rstrip("/")
    if raw.endswith("/api/upload"):
        raw = raw[: -len("/api/upload")]
    elif raw.endswith("/api"):
        raw = raw[: -len("/api")]
    return raw.rstrip("/") or "https://www.dele.fun"


def _api_key(api_key: Optional[str]) -> str:
    return (
        api_key
        or os.environ.get("DELE_API_KEY")
        or os.environ.get("POSTME_API_KEY")
        or ""
    ).strip()


def _should_skip_dir(name: str) -> bool:
    return name in SKIP_DIR_NAMES or name == ".git"


def _should_skip_file(name: str) -> bool:
    lower = name.lower()
    return lower in SKIP_FILE_NAMES or lower.startswith(".env")


def execute(
    target_path: str,
    app_name: str,
    api_url: str = "https://www.dele.fun",
    api_key: Optional[str] = None,
    app_desc: Optional[str] = None,
    visibility: Optional[str] = None
) -> str:
    """
    Deploy a local folder or HTML file to Dele.
    Files are uploaded with presigned PUT URLs. Never POST file bytes to /api/upload.
    """
    if not os.path.exists(target_path):
        return f"Error: Target path '{target_path}' does not exist."

    if not re.match(r'^[a-z0-9-]+$', app_name):
        return "Error: app_name must contain only lowercase letters, numbers, and hyphens."

    valid_visibility = {"public", "unlisted", "password", "hidden"}
    if visibility and visibility not in valid_visibility:
        return f"Error: visibility must be one of {valid_visibility}"

    token = _api_key(api_key)
    if not token:
        return "Error: missing API key. Set DELE_API_KEY or pass api_key."

    files_to_upload = []

    if os.path.isfile(target_path):
        files_to_upload.append((target_path, os.path.basename(target_path)))
    elif os.path.isdir(target_path):
        for root, dirs, files in os.walk(target_path):
            dirs[:] = [d for d in dirs if not _should_skip_dir(d)]
            for file in files:
                if _should_skip_file(file):
                    continue
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, target_path).replace(os.sep, '/')
                files_to_upload.append((file_path, rel_path))
    else:
        return f"Error: '{target_path}' is neither a file nor a directory."

    if not files_to_upload:
        return "Error: No files found to upload."

    origin = _origin(api_url)
    headers = {
        "Authorization": f"Bearer {token}",
        "x-agent-user": "openclaw-agent",
    }

    try:
        files_meta = [
            {
                "path": rel_path,
                "size": os.path.getsize(file_path),
                "contentType": mimetypes.guess_type(file_path)[0] or "application/octet-stream",
            }
            for file_path, rel_path in files_to_upload
        ]
        presign_payload = {"appName": app_name, "files": files_meta}
        if visibility:
            presign_payload["visibility"] = visibility

        response = requests.post(
            f"{origin}/api/upload/presign",
            json=presign_payload,
            headers=headers,
            timeout=(15, 60),
        )
        if response.status_code != 200:
            try:
                err_msg = response.json().get('error', response.text)
            except Exception:
                err_msg = response.text
            return f"Deployment preparation failed (Status {response.status_code}): {err_msg}"

        upload_urls = response.json().get("urls", [])
        if len(upload_urls) != len(files_to_upload):
            return "Deployment failed: the server returned an incomplete upload manifest."

        for (file_path, rel_path), metadata, upload in zip(files_to_upload, files_meta, upload_urls):
            if upload.get("path") != rel_path:
                return "Deployment failed: the server returned a mismatched upload manifest."
            content_type = metadata["contentType"]
            with open(file_path, 'rb') as file_handle:
                upload_response = requests.put(
                    upload["uploadUrl"],
                    data=file_handle,
                    headers={"Content-Type": content_type},
                    timeout=(15, 600),
                )
            if upload_response.status_code not in (200, 201):
                detail = (upload_response.text or "")[:300]
                return (
                    f"Deployment failed while uploading '{rel_path}' "
                    f"(Status {upload_response.status_code}): {detail}"
                )

        finalize_payload = {
            "appName": app_name,
            "files": files_meta,
        }
        if app_desc:
            finalize_payload["appDesc"] = app_desc
        if visibility:
            finalize_payload["visibility"] = visibility

        response = requests.post(
            f"{origin}/api/upload/finalize",
            json=finalize_payload,
            headers=headers,
            timeout=(15, 120),
        )
        if response.status_code not in (200, 201):
            try:
                err_msg = response.json().get('error', response.text)
            except Exception:
                err_msg = response.text
            return f"Deployment finalization failed (Status {response.status_code}): {err_msg}"

        data = response.json()
        actual_visibility = data.get('visibility')
        if visibility and actual_visibility != visibility:
            return (
                "Deployment failed: requested visibility "
                f"'{visibility}', but the server reported '{actual_visibility}'."
            )

        if visibility == "password" and not data.get('accessCode'):
            return "Deployment failed: the server did not return an access code for the password-protected app."

        app_url = f"{origin}{data.get('url', f'/app/{app_name}/')}"
        result = f"Deployment successful! URL: {app_url}"
        result += f"\nVisibility: {actual_visibility}"
        if actual_visibility == "password":
            result += f"\nAccess code: {data['accessCode']}"

        return result

    except Exception as e:
        return f"Error during deployment: {str(e)}"
```
