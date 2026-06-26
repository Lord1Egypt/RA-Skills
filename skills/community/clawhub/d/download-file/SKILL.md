---
name: download-file
description: Download large files from HTTP/HTTPS URLs with resume support, progress monitoring, and timeout handling
metadata:
  {"openclaw": {"requires": {"bins": ["curl"]}, "emoji": "📥"}}
---

# 📥 Large File Downloader

## When to Use

Use this skill when downloading files from HTTP/HTTPS URLs, especially large files (>100MB).

**Typical scenarios:**
- Downloading software installers (DMG, EXE, ZIP)
- Downloading large datasets
- Downloading video/audio files
- Downloading documents/PDFs
- Any file download from URL

**Trigger keywords:**
- "download this file"
- "save this DMG"
- "download from this URL"
- "get this file"
- "帮我下载 xxx" (Chinese)

---

## Core Principles

### ⚠️ Must-Follow Best Practices

1. **Always use background execution** - Never run large downloads synchronously
2. **Always set timeout** - Configure reasonable timeout based on file size
3. **Always support resume** - Use `curl -C -` for resumable downloads
4. **Always show progress** - Use `--progress-bar` flag
5. **Always verify results** - Check file size after download completes

---

## Standard Process

### Step 1: Start Download (Background Mode)

```bash
exec(
  command="curl -L -C - --progress-bar -o <destination_path> <URL>",
  background=true,
  timeout=600
)
```

**Parameter explanation:**
- `-L` - Follow redirects
- `-C -` - Resume partial download
- `--progress-bar` - Show progress bar
- `-o` - Output file path
- `background=true` - **Critical!** Run in background to avoid timeout
- `timeout=600` - 10 minutes timeout (adjust based on file size)

### Step 2: Monitor Progress

```bash
process(action="poll", sessionId="<session_id>")
```

Poll periodically to check download progress until completion.

### Step 3: Verify Result

```bash
exec(command="ls -lh <file_path>")
```

Check:
- File exists
- File size is reasonable
- File is complete (compare MD5/SHA if available)

---

## Complete Examples

### Example 1: Download DMG File (215MB)

**User:** "Download https://github.com/example/app/releases/download/v1.0/app.dmg"

**Agent action:**

```json
{
  "tool": "exec",
  "command": "curl -L -C - --progress-bar -o ~/Downloads/app.dmg https://github.com/example/app/releases/download/v1.0/app.dmg",
  "background": true,
  "timeout": 600
}
```

**Returns:** `{status: "running", sessionId: "xxx"}`

Then poll periodically:

```json
{
  "tool": "process",
  "action": "poll",
  "sessionId": "xxx"
}
```

After download completes, verify:

```json
{
  "tool": "exec",
  "command": "ls -lh ~/Downloads/app.dmg && file ~/Downloads/app.dmg"
}
```

### Example 2: Download Small File (<50MB)

For small files, simplified handling is acceptable:

```bash
exec(command="curl -L -o ~/Downloads/small.pdf https://example.com/small.pdf", timeout=120)
```

Small files can run synchronously, but still set timeout.

---

## Timeout Reference

| File Size | Recommended Timeout |
|-----------|-------------------|
| < 50MB | 120 seconds (2 min) |
| 50-200MB | 300 seconds (5 min) |
| 200-500MB | 600 seconds (10 min) |
| 500MB-1GB | 1200 seconds (20 min) |
| > 1GB | 1800 seconds (30 min) or more |

---

## Error Handling

### Common Errors & Solutions

**1. Download interrupted**
```bash
# Re-run same command, curl -C - will resume automatically
curl -L -C - --progress-bar -o file.zip <URL>
```

**2. Permission denied**
```bash
# Ensure destination directory is writable
mkdir -p ~/Downloads
```

**3. Redirect failed**
```bash
# Use -L flag to follow redirects
curl -L -o file.zip <URL>
```

**4. Network timeout**
```bash
# Increase timeout or use --retry
curl -L --retry 3 --connect-timeout 30 -o file.zip <URL>
```

---

## Advanced Options

### Multi-threaded Download (aria2)

If aria2 is available, use multi-threading for faster downloads:

```bash
exec(
  command="aria2c -x 16 -s 16 -k 1M --continue -o ~/Downloads/file.zip <URL>",
  background=true,
  timeout=600
)
```

### Full Flow with Progress Monitoring

```bash
# 1. Start download
exec(command="curl -L -C - --progress-bar -o ~/Downloads/file.zip <URL>", background=true, timeout=600)

# 2. Poll every 30 seconds
process(action="poll", sessionId="xxx")

# 3. Verify after completion
exec(command="ls -lh ~/Downloads/file.zip")

# 4. Optional: Calculate checksum
exec(command="md5sum ~/Downloads/file.zip")
```

---

## Security Considerations

1. **Download from trusted sources only** - Verify URL origin
2. **Check file type** - Use `file` command to verify
3. **Scan for viruses** - If needed, scan after download
4. **Don't overwrite important files** - Check if destination exists

---

## Related Skills

- `feishu-send-file` - Send downloaded file to Feishu
- `file-read` - Read downloaded file content
- `video-frames` - Extract frames if video file

---

## Troubleshooting

If download fails, follow these steps:

1. **Check network connectivity**
   ```bash
   curl -I <URL>
   ```

2. **Check disk space**
   ```bash
   df -h ~/Downloads
   ```

3. **View detailed error**
   ```bash
   curl -v -o /dev/null <URL>
   ```

4. **Try alternative tool**
   ```bash
   wget --continue <URL>
   ```

---

**Remember: Always use `background=true` for large file downloads!** 🎯
