---
name: 123pan-upload
description: Upload files to 123pan (123云盘) and generate shareable links. Use when users need to upload files to 123pan and get links for sharing. Supports short share links (privacy-friendly) or direct download links. Works with small files (under 1GB) via single-step upload.
---

# 123pan-upload

Upload files to 123云盘 and generate shareable links. Supports both short links (privacy-friendly) and direct download links.

## ⚠️ Security Notice

**Before using WebDAV/rclone features, read this:**

1. **Rclone Config Isolation** (Important)
   - By default, scripts may read `~/.config/rclone/rclone.conf`
   - This file may contain credentials for other cloud services
   - **Recommendation**: Use dedicated rclone config:
     ```bash
     # Create isolated config
     rclone config --config ~/123pan-rclone.conf
     
     # Use it with the skill
     export RCLONE_CONFIG="$HOME/123pan-rclone.conf"
     ```

2. **Credential Storage**
   - Use environment variables (not hardcoded in files)
   - Or use `.env` file (add to `.gitignore`)
   - Never commit credentials to version control

3. **Upload Timeouts**
   - Large files involve long-running API verification
   - May take 30-90 seconds after upload completes
   - Script includes automatic retry logic

## Configuration

### Required for API Uploads

```bash
export PAN123_ACCESS_TOKEN="your_access_token"
export PAN123_DIRECT_FOLDER_ID="your_folder_id"
```

- `PAN123_ACCESS_TOKEN`: Get from <https://www.123pan.com/dashboard/dev>
- `PAN123_DIRECT_FOLDER_ID`: The numeric ID of a folder with direct link enabled

### Optional for WebDAV Uploads (>10GB files)

```bash
export PAN123_WEBDAV_USER="your_webdav_username"
export PAN123_WEBDAV_PASS="your_webdav_password"
export RCLONE_BIN="/path/to/rclone"  # Optional, defaults to system PATH
export RCLONE_CONFIG="$HOME/123pan-rclone.conf"  # Recommended for isolation
```

### WebDAV Setup

1. Login to <https://www.123pan.com>
2. Go to: Account → Third-party Mount → WebDAV Authorization
3. Create an app to get WebDAV credentials
4. **Important**: Set up isolated rclone config:
   ```bash
   # This creates a config file that only contains 123pan
   rclone config --config ~/123pan-rclone.conf
   # Follow prompts to add "123pan-webdav" remote
   
   # Export the config path
   export RCLONE_CONFIG="$HOME/123pan-rclone.conf"
   ```

## Quick Start

```bash
# Default: returns short share link (recommended)
python scripts/upload.py --file /path/to/file

# Get direct link instead
python scripts/upload.py --file /path/to/file --short-link=false
```

## Usage

### Default (Short Link)

Returns privacy-friendly short link:
```bash
python scripts/upload.py --file /path/to/file.txt
# Output: https://www.123pan.com/s/xxxxx
```

### Direct Link (Long URL)

Returns direct download link (contains user ID in URL):
```bash
python scripts/upload.py --file /path/to/file.txt --short-link=false
```

### Specify Target Folder

```bash
python scripts/upload.py --file /path/to/file.txt --folder 30767843
```

## Output Format

### Short Link (Default)
```json
{
  "success": true,
  "file_id": 12345678,
  "filename": "example.zip",
  "size": 10485760,
  "link": "https://www.123pan.com/s/xxxxx",
  "link_type": "short_link"
}
```

### Direct Link
```json
{
  "success": true,
  "file_id": 12345678,
  "filename": "example.zip",
  "size": 10485760,
  "link": "https://xxx.v.123pan.cn/xxx/xxx/example.zip",
  "link_type": "direct_link"
}
```

## API Workflow

1. **Get upload domain** - Call `/upload/v2/file/domain` to get upload server
2. **Upload file** - POST to `/upload/v2/file/single/create` (<1GB files)
3. **Create share link** (default) - POST `/api/v1/share/create` for short link
4. **Get direct link** (optional) - GET `/api/v1/direct-link/url?fileID={id}`

## Privacy Note

- **Short links** (`--short-link`): Privacy-friendly format, no user ID exposed in URL
- **Direct links**: Contain user ID and full path, less private but allows direct download

## Limitations

- Single upload limit: 1GB per file for single-step upload
- Chunked upload supports up to 10GB per file (API limit)
- Requires folder with direct link enabled

## Large Files (>10GB)

For files larger than 10GB, use WebDAV instead:

### Option 1: Simple WebDAV Upload
```bash
# Set up environment first
export PAN123_WEBDAV_USER="your_user"
export PAN123_WEBDAV_PASS="your_pass"
export RCLONE_CONFIG="$HOME/123pan-rclone.conf"  # Isolated config

python scripts/upload_rclone.py --file /path/to/large/file --verify
```

### Option 2: WebDAV Upload + Auto Link Generation
```bash
export PAN123_ACCESS_TOKEN="your_token"
export PAN123_WEBDAV_USER="your_user"
export PAN123_WEBDAV_PASS="your_pass"
export RCLONE_CONFIG="$HOME/123pan-rclone.conf"

# Upload via WebDAV, then use API to find file and generate direct link
python scripts/upload_webdav_link.py --file /path/to/large/file

# Generate share link instead
python scripts/upload_webdav_link.py --file /path/to/large/file --link-type share
```

**Note:** WebDAV uploads may take 30-90 seconds to appear in API listings due to indexing delays.

- API details: [references/api-reference.md](references/api-reference.md)
