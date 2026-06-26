---
name: downloader
description: "Download a file from a URL and save it locally."
---

# downloader

Download a file from a given URL and save it to a specified local path. Supports any file type accessible via HTTP/HTTPS.

## When to Use

✅ **USE this skill when:**

- When the user wants to download a file from a URL to the local machine.
- When the user needs to save a remote resource (image, audio, video, document, etc.) locally.
- When the user provides a download link and wants to store the file at a specific path.

## When NOT to Use

❌ **DON'T use this skill when:**

- When the user only wants to view or read a URL content without saving to disk.

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| url | string | Yes | The URL of the file to download |
| save_path | string | No | Local path to save the file (defaults to current directory with original filename) |

## Commands

### Basic Call

```bash
python3 scripts/download.py --url 'https://example.com/file.png'
```

### Save to a specific path

```bash
python3 scripts/download.py --url 'https://example.com/file.png' --save_path './downloads/image.png'
```

## Examples

**"Help me download this image."**

```bash
python3 scripts/download.py --url 'https://example.com/photo.jpg'
```

**"Download this PDF and save it to the reports folder."**

```bash
python3 scripts/download.py --url 'https://example.com/report.pdf' --save_path './reports/report.pdf'
```

## Response

Script outputs JSON to stdout:

- `code = 0` — success, `data` contains the local file path where the file was saved
- `code != 0` — error, show `message` to the user and suggest retrying

```json
{
  "code": 0,
  "message": "success",
  "data": "./downloads/file.png"
}
```

## Notes

- Requires `requests` package: `pip install requests`
