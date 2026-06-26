---
name: dropbox
description: |
  Dropbox API integration with managed OAuth. Files, folders, search, metadata, and cloud storage.
  Use this skill when users want to manage files and folders in Dropbox, search content, or work with file metadata.
  For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
  Requires network access and valid Maton API key.
metadata:
  author: maton
  version: "1.0"
  clawdbot:
    emoji: 🧠
    homepage: "https://maton.ai"
    requires:
      env:
        - MATON_API_KEY
---

# Dropbox

Access the Dropbox API with managed OAuth authentication. Manage files and folders, search content, retrieve metadata, and work with file revisions.

## Quick Start

```bash
# List files in root folder
python <<'EOF'
import urllib.request, os, json
data = json.dumps({"path": ""}).encode()
req = urllib.request.Request('https://gateway.maton.ai/dropbox/2/files/list_folder', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## Base URL

```
https://gateway.maton.ai/dropbox/2/{endpoint}
```

The gateway proxies requests to `api.dropboxapi.com` (for most endpoints) or `content.dropboxapi.com` (for upload/download endpoints) and automatically injects your OAuth token. The routing is handled automatically based on the endpoint path.

**Important:** Dropbox API v2 uses POST for all endpoints with JSON request bodies.

**Content Endpoints:** Upload and download endpoints use a different request format where file content is sent as the raw request body and parameters are passed in the `Dropbox-API-Arg` header as JSON. The gateway handles routing to the correct Dropbox host automatically.

## Authentication

All requests require the Maton API key in the Authorization header:

```
Authorization: Bearer $MATON_API_KEY
```

**Environment Variable:** Set your API key as `MATON_API_KEY`:

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

### Getting Your API Key

1. Sign in or create an account at [maton.ai](https://maton.ai)
2. Go to [maton.ai/settings](https://maton.ai/settings)
3. Copy your API key

## Connection Management

Manage your Dropbox OAuth connections at `https://ctrl.maton.ai`.

### List Connections

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=dropbox&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Create Connection

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'dropbox'}).encode()
req = urllib.request.Request('https://ctrl.maton.ai/connections', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Get Connection

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections/{connection_id}')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**Response:**
```json
{
  "connection": {
    "connection_id": "{connection_id}",
    "status": "ACTIVE",
    "creation_time": "2026-02-09T23:34:49.818074Z",
    "last_updated_time": "2026-02-09T23:37:09.697559Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "dropbox",
    "metadata": {}
  }
}
```

Open the returned `url` in a browser to complete OAuth authorization.

### Delete Connection

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections/{connection_id}', method='DELETE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Specifying Connection

If you have multiple Dropbox connections, specify which one to use with the `Maton-Connection` header:

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({"path": ""}).encode()
req = urllib.request.Request('https://gateway.maton.ai/dropbox/2/files/list_folder', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
req.add_header('Maton-Connection', '{connection_id}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

If omitted, the gateway uses the default (oldest) active connection.

## API Reference

### Users

#### Get Current Account

```bash
POST /dropbox/2/users/get_current_account
Content-Type: application/json

null
```

**Response:**
```json
{
  "account_id": "dbid:AAA-AdT84WzkyLw5s590DbYF1nGomiAoO8I",
  "name": {
    "given_name": "John",
    "surname": "Doe",
    "familiar_name": "John",
    "display_name": "John Doe",
    "abbreviated_name": "JD"
  },
  "email": "john@example.com",
  "email_verified": true,
  "disabled": false,
  "country": "US",
  "locale": "en",
  "account_type": {
    ".tag": "basic"
  },
  "root_info": {
    ".tag": "user",
    "root_namespace_id": "11989877987",
    "home_namespace_id": "11989877987"
  }
}
```

#### Get Space Usage

```bash
POST /dropbox/2/users/get_space_usage
Content-Type: application/json

null
```

**Response:**
```json
{
  "used": 538371,
  "allocation": {
    ".tag": "individual",
    "allocated": 2147483648
  }
}
```

### Files and Folders

#### List Folder

```bash
POST /dropbox/2/files/list_folder
Content-Type: application/json

{
  "path": "",
  "recursive": false,
  "include_deleted": false,
  "include_has_explicit_shared_members": false
}
```

Use empty string `""` for the root folder.

**Optional Parameters:**
- `recursive` - Include contents of subdirectories (default: false)
- `include_deleted` - Include deleted files (default: false)
- `include_media_info` - Include media info for photos/videos
- `limit` - Maximum entries per response (1-2000)

**Response:**
```json
{
  "entries": [
    {
      ".tag": "file",
      "name": "document.pdf",
      "path_lower": "/document.pdf",
      "path_display": "/document.pdf",
      "id": "id:Awe3Av8A8YYAAAAAAAAABQ",
      "client_modified": "2026-02-09T19:58:12Z",
      "server_modified": "2026-02-09T19:58:13Z",
      "rev": "016311c063b4f8700000002caa704e3",
      "size": 538371,
      "is_downloadable": true,
      "content_hash": "6542845d7b65ffc5358ebaa6981d991bab9fda194afa48bd727fcbe9e4a3158b"
    },
    {
      ".tag": "folder",
      "name": "Documents",
      "path_lower": "/documents",
      "path_display": "/Documents",
      "id": "id:Awe3Av8A8YYAAAAAAAAABw"
    }
  ],
  "cursor": "AAVqv-MUYFlM98b1QpFK6YaYC8L1s39lWjqbeqgWu4un...",
  "has_more": false
}
```

#### Continue Listing Folder

```bash
POST /dropbox/2/files/list_folder/continue
Content-Type: application/json

{
  "cursor": "AAVqv-MUYFlM98b1QpFK6YaYC8L1s39lWjqbeqgWu4un..."
}
```

Use when `has_more` is true in the previous response.

#### Get Metadata

```bash
POST /dropbox/2/files/get_metadata
Content-Type: application/json

{
  "path": "/document.pdf",
  "include_media_info": false,
  "include_deleted": false,
  "include_has_explicit_shared_members": false
}
```

**Response:**
```json
{
  ".tag": "file",
  "name": "document.pdf",
  "path_lower": "/document.pdf",
  "path_display": "/document.pdf",
  "id": "id:Awe3Av8A8YYAAAAAAAAABQ",
  "client_modified": "2026-02-09T19:58:12Z",
  "server_modified": "2026-02-09T19:58:13Z",
  "rev": "016311c063b4f8700000002caa704e3",
  "size": 538371,
  "is_downloadable": true,
  "content_hash": "6542845d7b65ffc5358ebaa6981d991bab9fda194afa48bd727fcbe9e4a3158b"
}
```

#### Create Folder

```bash
POST /dropbox/2/files/create_folder_v2
Content-Type: application/json

{
  "path": "/New Folder",
  "autorename": false
}
```

**Response:**
```json
{
  "metadata": {
    "name": "New Folder",
    "path_lower": "/new folder",
    "path_display": "/New Folder",
    "id": "id:Awe3Av8A8YYAAAAAAAAABw"
  }
}
```

#### Copy File or Folder

```bash
POST /dropbox/2/files/copy_v2
Content-Type: application/json

{
  "from_path": "/source/file.pdf",
  "to_path": "/destination/file.pdf",
  "autorename": false
}
```

**Response:**
```json
{
  "metadata": {
    ".tag": "file",
    "name": "file.pdf",
    "path_lower": "/destination/file.pdf",
    "path_display": "/destination/file.pdf",
    "id": "id:Awe3Av8A8YYAAAAAAAAACA"
  }
}
```

#### Move File or Folder

```bash
POST /dropbox/2/files/move_v2
Content-Type: application/json

{
  "from_path": "/old/location/file.pdf",
  "to_path": "/new/location/file.pdf",
  "autorename": false
}
```

**Response:**
```json
{
  "metadata": {
    ".tag": "file",
    "name": "file.pdf",
    "path_lower": "/new/location/file.pdf",
    "path_display": "/new/location/file.pdf",
    "id": "id:Awe3Av8A8YYAAAAAAAAACA"
  }
}
```

#### Delete File or Folder

```bash
POST /dropbox/2/files/delete_v2
Content-Type: application/json

{
  "path": "/file-to-delete.pdf"
}
```

**Response:**
```json
{
  "metadata": {
    ".tag": "file",
    "name": "file-to-delete.pdf",
    "path_lower": "/file-to-delete.pdf",
    "path_display": "/file-to-delete.pdf",
    "id": "id:Awe3Av8A8YYAAAAAAAAABQ"
  }
}
```

#### Get Temporary Download Link

```bash
POST /dropbox/2/files/get_temporary_link
Content-Type: application/json

{
  "path": "/document.pdf"
}
```

**Response:**
```json
{
  "metadata": {
    "name": "document.pdf",
    "path_lower": "/document.pdf",
    "path_display": "/document.pdf",
    "id": "id:Awe3Av8A8YYAAAAAAAAABQ",
    "size": 538371,
    "is_downloadable": true
  },
  "link": "https://uc785ee484c03b6556c091ea4491.dl.dropboxusercontent.com/cd/0/get/..."
}
```

The link is valid for 4 hours.

### File Upload

**Note:** Upload endpoints use a different request format. File content is sent as the raw request body, and parameters are passed in the `Dropbox-API-Arg` header as JSON. The gateway automatically routes these to `content.dropboxapi.com`.

#### Upload File (up to 150 MB)

```bash
POST /dropbox/2/files/upload
Content-Type: application/octet-stream
Dropbox-API-Arg: {"path": "/test.txt", "mode": "add", "autorename": true, "mute": false}

<file contents>
```

**Parameters (in Dropbox-API-Arg header):**
- `path` (required) - Path in Dropbox where the file will be saved
- `mode` - Write mode: `add` (default), `overwrite`, or `update` with rev
- `autorename` - If true, rename file if there's a conflict (default: false)
- `mute` - If true, don't notify desktop app (default: false)
- `strict_conflict` - If true, be more strict about conflicts (default: false)

**Response:**
```json
{
  "name": "test.txt",
  "path_lower": "/test.txt",
  "path_display": "/test.txt",
  "id": "id:Awe3Av8A8YYAAAAAAAAABw",
  "client_modified": "2026-04-14T10:00:00Z",
  "server_modified": "2026-04-14T10:00:01Z",
  "rev": "016311c063b4f8700000002caa704e4",
  "size": 1024,
  "is_downloadable": true,
  "content_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
}
```

#### Upload Large Files (Upload Session)

For files larger than 150 MB, use upload sessions. Files can be up to 350 GB.

**Step 1: Start Session**

```bash
POST /dropbox/2/files/upload_session/start
Content-Type: application/octet-stream
Dropbox-API-Arg: {"close": false}

<first chunk of file content>
```

**Response:**
```json
{
  "session_id": "AAAAAAAAAAFxxxxxxxxxxxxxxx"
}
```

**Step 2: Append Data (repeat as needed)**

```bash
POST /dropbox/2/files/upload_session/append_v2
Content-Type: application/octet-stream
Dropbox-API-Arg: {"cursor": {"session_id": "AAAAAAAAAAFxxxxxxxxxxxxxxx", "offset": 10000000}, "close": false}

<next chunk of file content>
```

The `offset` must match the total bytes uploaded so far.

**Step 3: Finish Session**

```bash
POST /dropbox/2/files/upload_session/finish
Content-Type: application/octet-stream
Dropbox-API-Arg: {"cursor": {"session_id": "AAAAAAAAAAFxxxxxxxxxxxxxxx", "offset": 50000000}, "commit": {"path": "/large_file.zip", "mode": "add", "autorename": true}}

<final chunk of file content, can be empty>
```

**Response:** Same as regular upload endpoint.

#### Finish Multiple Upload Sessions (Batch)

Complete multiple upload sessions in one call:

```bash
POST /dropbox/2/files/upload_session/finish_batch
Content-Type: application/json

{
  "entries": [
    {
      "cursor": {
        "session_id": "AAAAAAAAAAFxxxxxxxxxxxxxxx",
        "offset": 50000000
      },
      "commit": {
        "path": "/file1.zip",
        "mode": "add",
        "autorename": true
      }
    },
    {
      "cursor": {
        "session_id": "AAAAAAAAAAFyyyyyyyyyyyyyyy",
        "offset": 30000000
      },
      "commit": {
        "path": "/file2.zip",
        "mode": "add",
        "autorename": true
      }
    }
  ]
}
```

**Response (async job):**
```json
{
  ".tag": "async_job_id",
  "async_job_id": "dbjid:AAAAAAAAAA..."
}
```

Check status with `/files/upload_session/finish_batch/check`.

#### Check Batch Status

```bash
POST /dropbox/2/files/upload_session/finish_batch/check
Content-Type: application/json

{
  "async_job_id": "dbjid:AAAAAAAAAA..."
}
```

**Response (in progress):**
```json
{
  ".tag": "in_progress"
}
```

**Response (complete):**
```json
{
  ".tag": "complete",
  "entries": [
    {
      ".tag": "success",
      "name": "file1.zip",
      "path_lower": "/file1.zip",
      "path_display": "/file1.zip",
      "id": "id:Awe3Av8A8YYAAAAAAAAABw"
    },
    {
      ".tag": "success",
      "name": "file2.zip",
      "path_lower": "/file2.zip",
      "path_display": "/file2.zip",
      "id": "id:Awe3Av8A8YYAAAAAAAAABx"
    }
  ]
}
```

### File Download

#### Download File

```bash
POST /dropbox/2/files/download
Dropbox-API-Arg: {"path": "/document.pdf"}
```

**Response:** Raw file contents with metadata in `Dropbox-API-Result` response header.

#### Download Folder as ZIP

```bash
POST /dropbox/2/files/download_zip
Dropbox-API-Arg: {"path": "/folder"}
```

**Response:** ZIP file contents. Note: folders larger than 20 GB or with more than 10,000 files cannot be downloaded as ZIP.

#### Export File

Export a file from Dropbox (e.g., Paper docs to markdown):

```bash
POST /dropbox/2/files/export
Dropbox-API-Arg: {"path": "/document.paper"}
```

#### Get Preview

```bash
POST /dropbox/2/files/get_preview
Dropbox-API-Arg: {"path": "/document.docx"}
```

**Response:** PDF preview of the file.

#### Get Thumbnail

```bash
POST /dropbox/2/files/get_thumbnail_v2
Dropbox-API-Arg: {"resource": {".tag": "path", "path": "/photo.jpg"}, "format": "jpeg", "size": "w128h128"}
```

**Thumbnail Sizes:**
- `w32h32`, `w64h64`, `w128h128`, `w256h256`, `w480h320`, `w640h480`, `w960h640`, `w1024h768`, `w2048h1536`

### Search

#### Search Files

```bash
POST /dropbox/2/files/search_v2
Content-Type: application/json

{
  "query": "document",
  "options": {
    "path": "",
    "max_results": 100,
    "file_status": "active",
    "filename_only": false
  }
}
```

**Response:**
```json
{
  "has_more": false,
  "matches": [
    {
      "highlight_spans": [],
      "match_type": {
        ".tag": "filename"
      },
      "metadata": {
        ".tag": "metadata",
        "metadata": {
          ".tag": "file",
          "name": "document.pdf",
          "path_display": "/document.pdf",
          "path_lower": "/document.pdf",
          "id": "id:Awe3Av8A8YYAAAAAAAAABw"
        }
      }
    }
  ]
}
```

#### Continue Search

```bash
POST /dropbox/2/files/search/continue_v2
Content-Type: application/json

{
  "cursor": "..."
}
```

### File Revisions

#### List Revisions

```bash
POST /dropbox/2/files/list_revisions
Content-Type: application/json

{
  "path": "/document.pdf",
  "mode": "path",
  "limit": 10
}
```

**Response:**
```json
{
  "is_deleted": false,
  "entries": [
    {
      "name": "document.pdf",
      "path_lower": "/document.pdf",
      "path_display": "/document.pdf",
      "id": "id:Awe3Av8A8YYAAAAAAAAABQ",
      "client_modified": "2026-02-09T19:58:12Z",
      "server_modified": "2026-02-09T19:58:13Z",
      "rev": "016311c063b4f8700000002caa704e3",
      "size": 538371,
      "is_downloadable": true
    }
  ],
  "has_more": false
}
```

#### Restore File

```bash
POST /dropbox/2/files/restore
Content-Type: application/json

{
  "path": "/document.pdf",
  "rev": "016311c063b4f8700000002caa704e3"
}
```

### Tags

#### Get Tags

```bash
POST /dropbox/2/files/tags/get
Content-Type: application/json

{
  "paths": ["/document.pdf", "/folder"]
}
```

**Response:**
```json
{
  "paths_to_tags": [
    {
      "path": "/document.pdf",
      "tags": [
        {
          ".tag": "user_generated_tag",
          "tag_text": "important"
        }
      ]
    },
    {
      "path": "/folder",
      "tags": []
    }
  ]
}
```

#### Add Tag

```bash
POST /dropbox/2/files/tags/add
Content-Type: application/json

{
  "path": "/document.pdf",
  "tag_text": "important"
}
```

Returns `null` on success.

**Note:** Tag text must match pattern `[\w]+` (alphanumeric and underscores only, no hyphens or spaces).

#### Remove Tag

```bash
POST /dropbox/2/files/tags/remove
Content-Type: application/json

{
  "path": "/document.pdf",
  "tag_text": "important"
}
```

Returns `null` on success.

### Batch Operations

#### Delete Batch

```bash
POST /dropbox/2/files/delete_batch
Content-Type: application/json

{
  "entries": [
    {"path": "/file1.pdf"},
    {"path": "/file2.pdf"}
  ]
}
```

Returns async job ID. Check status with `/files/delete_batch/check`.

#### Copy Batch

```bash
POST /dropbox/2/files/copy_batch_v2
Content-Type: application/json

{
  "entries": [
    {"from_path": "/source/file1.pdf", "to_path": "/dest/file1.pdf"},
    {"from_path": "/source/file2.pdf", "to_path": "/dest/file2.pdf"}
  ],
  "autorename": false
}
```

#### Move Batch

```bash
POST /dropbox/2/files/move_batch_v2
Content-Type: application/json

{
  "entries": [
    {"from_path": "/old/file1.pdf", "to_path": "/new/file1.pdf"},
    {"from_path": "/old/file2.pdf", "to_path": "/new/file2.pdf"}
  ],
  "autorename": false
}
```

## Pagination

Dropbox uses cursor-based pagination. When `has_more` is true, use the `/continue` endpoint with the returned cursor.

```python
import os
import requests

headers = {
    'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}',
    'Content-Type': 'application/json'
}

# Initial request
response = requests.post(
    'https://gateway.maton.ai/dropbox/2/files/list_folder',
    headers=headers,
    json={'path': '', 'limit': 100}
)
result = response.json()
all_entries = result['entries']

# Continue while has_more is True
while result.get('has_more'):
    response = requests.post(
        'https://gateway.maton.ai/dropbox/2/files/list_folder/continue',
        headers=headers,
        json={'cursor': result['cursor']}
    )
    result = response.json()
    all_entries.extend(result['entries'])

print(f"Total entries: {len(all_entries)}")
```

## Code Examples

### JavaScript

```javascript
const response = await fetch(
  'https://gateway.maton.ai/dropbox/2/files/list_folder',
  {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ path: '' })
  }
);
const data = await response.json();
console.log(data.entries);
```

### Python

```python
import os
import requests

response = requests.post(
    'https://gateway.maton.ai/dropbox/2/files/list_folder',
    headers={
        'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}',
        'Content-Type': 'application/json'
    },
    json={'path': ''}
)
data = response.json()
print(data['entries'])
```

### Python (Create Folder and Search)

```python
import os
import requests

headers = {
    'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}',
    'Content-Type': 'application/json'
}

# Create folder
response = requests.post(
    'https://gateway.maton.ai/dropbox/2/files/create_folder_v2',
    headers=headers,
    json={'path': '/My New Folder', 'autorename': False}
)
folder = response.json()
print(f"Created folder: {folder['metadata']['path_display']}")

# Search for files
response = requests.post(
    'https://gateway.maton.ai/dropbox/2/files/search_v2',
    headers=headers,
    json={'query': 'document'}
)
results = response.json()
print(f"Found {len(results['matches'])} matches")
```

### Python (Upload File)

```python
import os
import json
import requests

# Upload a small file (up to 150 MB)
file_path = '/path/to/local/file.txt'
dropbox_path = '/uploaded_file.txt'

with open(file_path, 'rb') as f:
    response = requests.post(
        'https://gateway.maton.ai/dropbox/2/files/upload',
        headers={
            'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}',
            'Content-Type': 'application/octet-stream',
            'Dropbox-API-Arg': json.dumps({
                'path': dropbox_path,
                'mode': 'add',
                'autorename': True
            })
        },
        data=f
    )
result = response.json()
print(f"Uploaded: {result['path_display']} ({result['size']} bytes)")
```

### Python (Upload Large File with Session)

```python
import os
import json
import requests

CHUNK_SIZE = 4 * 1024 * 1024  # 4 MB chunks
file_path = '/path/to/large/file.zip'
dropbox_path = '/large_file.zip'

with open(file_path, 'rb') as f:
    file_size = os.path.getsize(file_path)
    
    # Start session
    chunk = f.read(CHUNK_SIZE)
    response = requests.post(
        'https://gateway.maton.ai/dropbox/2/files/upload_session/start',
        headers={
            'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}',
            'Content-Type': 'application/octet-stream',
            'Dropbox-API-Arg': json.dumps({'close': False})
        },
        data=chunk
    )
    session_id = response.json()['session_id']
    offset = len(chunk)
    
    # Append remaining chunks
    while True:
        chunk = f.read(CHUNK_SIZE)
        if not chunk:
            break
        
        if offset + len(chunk) < file_size:
            # More chunks to come
            requests.post(
                'https://gateway.maton.ai/dropbox/2/files/upload_session/append_v2',
                headers={
                    'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}',
                    'Content-Type': 'application/octet-stream',
                    'Dropbox-API-Arg': json.dumps({
                        'cursor': {'session_id': session_id, 'offset': offset},
                        'close': False
                    })
                },
                data=chunk
            )
            offset += len(chunk)
        else:
            # Final chunk - finish session
            response = requests.post(
                'https://gateway.maton.ai/dropbox/2/files/upload_session/finish',
                headers={
                    'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}',
                    'Content-Type': 'application/octet-stream',
                    'Dropbox-API-Arg': json.dumps({
                        'cursor': {'session_id': session_id, 'offset': offset},
                        'commit': {
                            'path': dropbox_path,
                            'mode': 'add',
                            'autorename': True
                        }
                    })
                },
                data=chunk
            )
            result = response.json()
            print(f"Uploaded: {result['path_display']} ({result['size']} bytes)")
            break
```

## Notes

- All Dropbox API v2 endpoints use HTTP POST method
- Most endpoints use JSON request bodies (Content-Type: application/json)
- Upload/download endpoints use binary content (Content-Type: application/octet-stream) with parameters in `Dropbox-API-Arg` header
- The gateway automatically routes content endpoints to `content.dropboxapi.com`
- Use empty string `""` for the root folder path
- Paths are case-insensitive but case-preserving
- File IDs (e.g., `id:Awe3Av8A8YYAAAAAAAAABQ`) persist even when files are moved or renamed
- Tag text must match pattern `[\w]+` (alphanumeric and underscores only)
- Temporary download links expire after 4 hours
- Rate limits are generous and per-user
- Maximum file size for single upload: 150 MB (use upload sessions for larger files up to 350 GB)
- IMPORTANT: When piping curl output to `jq` or other commands, environment variables like `$MATON_API_KEY` may not expand correctly in some shell environments

## Error Handling

| Status | Meaning |
|--------|---------|
| 400 | Missing Dropbox connection or bad request |
| 401 | Invalid or missing Maton API key |
| 404 | Resource not found |
| 409 | Conflict (path doesn't exist, already exists, etc.) |
| 429 | Rate limited |
| 4xx/5xx | Passthrough error from Dropbox API |

Error responses include details:
```json
{
  "error_summary": "path/not_found/...",
  "error": {
    ".tag": "path",
    "path": {
      ".tag": "not_found"
    }
  }
}
```

### Troubleshooting: Invalid API Key

**When you receive an "Invalid API key" error, ALWAYS follow these steps before concluding there is an issue:**

1. Check that the `MATON_API_KEY` environment variable is set:

```bash
echo $MATON_API_KEY
```

2. Verify the API key is valid by listing connections:

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## Resources

- [Dropbox HTTP API Overview](https://www.dropbox.com/developers/documentation/http/overview)
- [Dropbox Developer Portal](https://www.dropbox.com/developers)
- [Dropbox API Explorer](https://dropbox.github.io/dropbox-api-v2-explorer/)
- [DBX File Access Guide](https://developers.dropbox.com/dbx-file-access-guide)
