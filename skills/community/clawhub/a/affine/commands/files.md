# File Attachments

---

## File Module

### upload

Upload a file attachment.

```bash
affine-cli file upload [options]
```

| Option | Short | Required | Description |
|--------|-------|----------|-------------|
| --file | -f | No* | File path to upload. Either --file or --content required |
| --content | -c | No* | Base64 or plain text content |
| --filename | -n | No | File name. Uses filename from --file or "content" |
| --content-type | - | No | MIME type (e.g., `image/png`, `application/pdf`) |
| --workspace | -w | No | Workspace ID |

*Either `--file` or `--content` is required.

**Examples:**
```bash
# Upload from file
affine-cli file upload --file ./document.pdf

# Upload with custom name
affine-cli file upload --file ./image.png --filename "photo.png"

# Upload text content
affine-cli file upload --content "Hello world" --filename "hello.txt" --content-type "text/plain"
```

### delete

Delete a file attachment.

```bash
affine-cli file delete [options]
```

| Option | Short | Required | Description |
|--------|-------|----------|-------------|
| --id | -i | **Yes** | Blob ID (attachment ID) |
| --permanently | -p | No | Permanently delete. Default: soft delete |
| --workspace | -w | No | Workspace ID |

### clean

Clean up soft-deleted files to free storage space.

```bash
affine-cli file clean [options]
```

| Option | Short | Required | Description |
|--------|-------|----------|-------------|
| --workspace | -w | No | Workspace ID |