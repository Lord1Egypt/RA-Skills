---
name: postme-deploy
description: Deploy local HTML/frontend files to Dele (dele.fun) and get a live URL
allowed-tools: "read(*), glob(*)"
env:
  POSTME_API_KEY:
    required: true
    description: "Dele API key for authentication. Get one at https://www.dele.fun/api-keys"
  POSTME_API_URL:
    required: false
    description: "Dele upload endpoint. Defaults to https://www.dele.fun/api/upload"
---

# Dele Deploy Skill

## Overview
This skill allows AI Agents (OpenClaw, Cursor, Claude, etc.) to automatically deploy generated HTML files or frontend project folders to Dele (https://www.dele.fun) — a static site hosting platform. It returns a live URL that can be shared with the user.

## Required Environment Variables

| Variable | Description |
|---|---|
| `POSTME_API_KEY` | **Required.** Your Dele API key for authentication. Get one at https://www.dele.fun/api-keys |
| `POSTME_API_URL` | Optional. Defaults to `https://www.dele.fun/api/upload` |

## Prerequisites

1.  **Dele API Key**: Generate an API key at https://www.dele.fun/api-keys, then set it as an environment variable:
    ```env
    POSTME_API_KEY="your-secret-agent-key"
    ```

2.  **Python Dependencies**: The skill requires the `requests` library.
    ```bash
    pip install requests
    ```

## Usage Instructions for the Agent
When a user asks you to deploy, publish, or share a web application (like an HTML file or a frontend project folder) that you have just created, you should use this skill.

1. Determine the absolute path to the generated folder or file (`target_path`).
2. Invent a suitable, URL-friendly name for the application (`app_name`). It must contain only lowercase letters, numbers, and hyphens.
3. Call the `postme_deploy` skill with these parameters.
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
  "name": "postme_deploy",
  "description": "Deploy a local folder or HTML file to the Dele system to get a live web URL.",
  "parameters": {
    "type": "object",
    "properties": {
      "target_path": {
        "type": "string",
        "description": "The local path to the folder or HTML file you want to deploy."
      },
      "app_name": {
        "type": "string",
        "description": "A unique, URL-friendly name for the application (lowercase letters, numbers, hyphens only)."
      },
      "api_url": {
        "type": "string",
        "description": "The full URL to the Dele /api/upload endpoint. Defaults to https://www.dele.fun/api/upload"
      },
      "api_key": {
        "type": "string",
        "description": "The API key for authentication (POSTME_API_KEY)."
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

## Python Implementation (`postme_deploy.py`)

```python
import os
import requests
import re
from typing import Optional

def execute(
    target_path: str, 
    app_name: str, 
    api_url: str = "https://www.dele.fun/api/upload", 
    api_key: Optional[str] = None,
    app_desc: Optional[str] = None,
    visibility: Optional[str] = None
) -> str:
    """
    Deploy a local folder or HTML file to the Dele system.
    """
    if not os.path.exists(target_path):
        return f"Error: Target path '{target_path}' does not exist."
        
    if not re.match(r'^[a-z0-9-]+$', app_name):
        return "Error: app_name must contain only lowercase letters, numbers, and hyphens."

    valid_visibility = {"public", "unlisted", "password", "hidden"}
    if visibility and visibility not in valid_visibility:
        return f"Error: visibility must be one of {valid_visibility}"

    files_to_upload = []
    
    if os.path.isfile(target_path):
        files_to_upload.append((target_path, os.path.basename(target_path)))
    elif os.path.isdir(target_path):
        for root, _, files in os.walk(target_path):
            for file in files:
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, target_path).replace(os.sep, '/')
                files_to_upload.append((file_path, rel_path))
    else:
        return f"Error: '{target_path}' is neither a file nor a directory."

    if not files_to_upload:
        return "Error: No files found to upload."

    multipart_data = [('appName', (None, app_name))]
    if app_desc:
        multipart_data.append(('appDesc', (None, app_desc)))
        
    file_handles = []
    headers = {}
    if api_key:
        headers['Authorization'] = f"Bearer {api_key}"
        headers['x-agent-user'] = "openclaw-agent"

    try:
        for file_path, rel_path in files_to_upload:
            f = open(file_path, 'rb')
            file_handles.append(f)
            multipart_data.append(('files', (os.path.basename(file_path), f)))
            multipart_data.append(('paths', (None, rel_path)))

        response = requests.post(api_url, files=multipart_data, headers=headers)
        
        if response.status_code not in (200, 201):
            try:
                err_msg = response.json().get('error', response.text)
            except:
                err_msg = response.text
            return f"Deployment failed (Status {response.status_code}): {err_msg}"

        data = response.json()
        base_url = api_url.replace('/api/upload', '')
        app_url = f"{base_url}{data.get('url', f'/app/{app_name}/')}"
        result = f"Deployment successful! URL: {app_url}"

        # Set visibility if specified and not default
        if visibility and visibility != "public":
            vis_url = api_url.replace('/api/upload', '/api/apps/visibility')
            vis_resp = requests.post(
                vis_url,
                json={"appName": app_name, "visibility": visibility},
                headers=headers
            )
            if vis_resp.status_code == 200:
                vis_data = vis_resp.json()
                result += f"\nVisibility: {visibility}"
                if visibility == "password" and vis_data.get("accessCode"):
                    result += f"\nAccess code: {vis_data['accessCode']}"
            else:
                result += f"\nWarning: Failed to set visibility to '{visibility}'"

        return result
            
    except Exception as e:
        return f"Error during deployment: {str(e)}"
    finally:
        for f in file_handles:
            f.close()
```
