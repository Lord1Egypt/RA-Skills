---
name: file-upload-cli
description: Upload files to the litterbox.catbox.moe file sharing service and get shareable URLs (72h expiry). Use when the user wants to share a file temporarily or needs a quick file hosting solution.
---

# File Upload CLI Tool

A Node.js command-line tool for uploading files to the litterbox.catbox.moe file sharing service using curl.

## Quick Start

Upload a file and receive a shareable URL:

```bash
node file-upload-cli.js <filePath>
```

**Example**:
```bash
node file-upload-cli.js document.pdf
```

**Output**:
```
Uploading...
File uploaded successfully!
URL: https://litter.catbox.moe/abc123.pdf
Note: File will be available for 72 hours.
```

## Instructions

### Step 1: Installation

Ensure Node.js v14+ and curl are installed:

**Requirements:**
- Node.js v14+
- curl (included in Windows 10+, macOS, and most Linux distributions)

```bash
cd file-upload-cli
npm install  # No external dependencies required
```

### Step 2: Upload a File

Run the CLI tool with a file path:

```bash
node file-upload-cli.js <filePath>
```

**Path Types**:
- Relative: `node file-upload-cli.js ./file.txt`
- Absolute: `node file-upload-cli.js /home/user/file.txt` (Unix) or `node file-upload-cli.js C:\Users\user\file.txt` (Windows)
- With spaces: `node file-upload-cli.js "my file.txt"`

### Step 3: Use the URL

The tool outputs a shareable URL that can be:
- Shared with others
- Embedded in documents
- Used in applications

**URL Format**: `https://0x0.st/<random-id>`

## Examples

### Upload Different File Types

**Text file**:
```bash
node file-upload-cli.js notes.txt
```

**Image**:
```bash
node file-upload-cli.js photo.jpg
```

**PDF document**:
```bash
node file-upload-cli.js report.pdf
```

**Archive**:
```bash
node file-upload-cli.js backup.zip
```

### Large Files with Progress

For files larger than 1MB, the tool displays upload progress:

```bash
node file-upload-cli.js large-video.mp4
```

**Output**:
```
Uploading...
File uploaded successfully!
URL: https://litter.catbox.moe/xyz789.mp4
Note: File will be available for 72 hours.
```

### Cross-Platform Paths

**Windows**:
```bash
node file-upload-cli.js C:\Users\user\Documents\file.pdf
node file-upload-cli.js .\file.txt
```

**macOS/Linux**:
```bash
node file-upload-cli.js /home/user/documents/file.pdf
node file-upload-cli.js ./file.txt
```

## Error Handling

The tool provides clear error messages for common issues:

### Validation Errors (Exit Code 4)

**No file path provided**:
```
Error: No file path provided
Usage: node file-upload-cli.js <filePath>
```

**File not found**:
```
Error: File not found - /path/to/file.txt
Please check the file path and try again.
```

**Path is a directory**:
```
Error: Path is a directory - /path/to/folder
Please provide a file path, not a directory.
```

**File too large**:
```
Error: File too large - 1.5 GB (limit: 1 GB)
The file exceeds the litterbox.catbox.moe service limit.
```

**Empty file**:
```
Error: File is empty - /path/to/file.txt
Cannot upload an empty file.
```

### Network Errors (Exit Code 2)

**Connection failure**:
```
Error: Network error - Cannot connect to litterbox.catbox.moe
Please check your internet connection and try again.
```

**Timeout**:
```
Error: Connection timeout
The upload request timed out. Please try again.
```

### Service Errors (Exit Code 3)

**File too large (service rejection)**:
```
Error: Service error - File too large (413)
The litterbox.catbox.moe service rejected the file. Maximum size is 1 GB.
```

**Server error**:
```
Error: Service error - Internal server error (500)
The litterbox.catbox.moe service encountered an error. Please try again later.
```

**Service unavailable**:
```
Error: Service unavailable (503)
The litterbox.catbox.moe service is temporarily unavailable. Please try again later.
```

## Security Considerations

### File Access
- The tool only reads the file you specify
- No directory traversal or unauthorized file access
- Files are not modified or deleted
- File path validation prevents malicious inputs

### Network Security
- Only communicates with `https://litterbox.catbox.moe` (HTTPS encrypted)
- Uses system curl command for secure file transmission
- No other external services are contacted
- No authentication tokens or API keys required
- Secure TLS connection for file transmission

### Data Privacy
⚠️ **Important**: Files are uploaded to a **public** file sharing service:
- URLs are publicly accessible by anyone who has the link
- Files automatically expire after 72 hours
- No authentication or access control
- Do not upload sensitive, confidential, or private files
- User is responsible for file content and compliance

### Dependencies
The tool uses:
- **Native Node.js modules**: `child_process`, `fs`, `path`, `util`
- **System curl**: Pre-installed on most systems, widely trusted and security-audited
- **No external npm packages required**

## Limitations

- **Maximum file size**: 1GB (litterbox.catbox.moe service limit)
- **File expiry**: Files are automatically deleted after 72 hours
- **Upload timeout**: 60 seconds
- **Single file**: One file per command (no batch uploads)
- **No retry logic**: Failed uploads must be manually retried
- **Public URLs**: All uploaded files are publicly accessible
- **Requires curl**: System must have curl installed

## Technical Details

**Implementation**: `file-upload-cli.js` (Node.js script)

**Exit Codes**:
- `0`: Success
- `1`: General error
- `2`: Network error
- `3`: Service error
- `4`: Validation error

**Requirements**:
- Node.js v14.0.0 or higher
- Internet connection
- Read access to the file being uploaded

## Troubleshooting

**"curl command not found"**
- Install curl on your system (included in Windows 10+, macOS, most Linux distributions)

**"Permission denied"**
- Check file permissions: `chmod +r file.txt` (Unix)
- Ensure you have read access to the file

**"Connection timeout"**
- Check internet connection
- Try again with a smaller file
- Verify firewall allows HTTPS connections

**"Service error"**
- The litterbox.catbox.moe service may be temporarily down
- Wait a few minutes and try again
- Check service status at https://catbox.moe
