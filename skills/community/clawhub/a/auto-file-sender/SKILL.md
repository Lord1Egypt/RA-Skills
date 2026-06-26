---
name: auto-file-sender
description: |
  Automatically send files from workspace to Feishu/Lark when files are generated or updated. 
  Use when: (1) User creates new documents and wants them delivered automatically, 
  (2) Batch processing generates multiple files that need to be sent, 
  (3) Setting up automated file delivery workflows.
  Supports Word, PDF, images, and other common file formats up to 30MB.
---

# Auto File Sender

## Overview

This skill enables automatic file delivery from the workspace to Feishu/Lark users. When files are generated (documents, PDFs, images, etc.), they can be automatically sent to specified recipients without manual intervention.

**Key Capabilities:**
- Auto-detect new files in workspace
- Send via Feishu message with file attachment
- Support batch sending of multiple files
- Configurable file type filters and recipient rules

## Quick Start

### Basic Usage

When a file is ready to send:

```javascript
// Single file
{
  "action": "send",
  "filePath": "/root/.openclaw/workspace/document.docx",
  "filename": "document.docx",
  "message": "Here's your file!",
  "target": "user_open_id"
}
```

### Auto-Send on File Creation

The skill provides a helper script to watch for new files and auto-send:

```bash
# Watch workspace and auto-send new files
python3 scripts/auto_send.py --watch /root/.openclaw/workspace --recipient USER_OPEN_ID
```

## Workflow

### Step 1: Identify Files to Send

Check for recently created/modified files:

```bash
# List files created in last 10 minutes
find /root/.openclaw/workspace -type f -mmin -10
```

### Step 2: Send Files

Use the message tool with filePath parameter:

```javascript
{
  "action": "send",
  "filePath": "<absolute-path-to-file>",
  "filename": "<display-filename>",
  "message": "<optional-message>",
  "target": "<recipient-open-id>"
}
```

**Parameters:**
- `filePath`: Absolute path to the file (required)
- `filename`: Display name for the file (optional, defaults to basename)
- `message`: Accompanying text message (optional)
- `target`: Recipient open_id (defaults to current user if omitted)

### Step 3: Confirm Delivery

Check the response for successful delivery:
- `messageId`: ID of the sent message
- `chatId`: ID of the chat/channel

## Supported File Types

| Type | Extensions | Max Size |
|------|------------|----------|
| Documents | .docx, .doc, .pdf | 30MB |
| Images | .jpg, .png, .gif, .webp | 30MB |
| Spreadsheets | .xlsx, .xls, .csv | 30MB |
| Archives | .zip, .tar.gz | 30MB |
| Others | Any | 30MB |

## Batch Sending

To send multiple files at once:

```javascript
// Send files sequentially
for (const file of files) {
  await message.send({
    action: "send",
    filePath: file.path,
    filename: file.name
  });
}
```

## Configuration

### Default Settings

- **Source directory**: `/root/.openclaw/workspace`
- **Max file size**: 30MB (Feishu limit)
- **Auto-recipient**: Current conversation user

### Custom Recipient

To send to a specific user:

```javascript
{
  "action": "send",
  "target": "ou_a65105519c863f8544fb22b40c468063",  // User's open_id
  "filePath": "/path/to/file"
}
```

## Scripts

### scripts/auto_send.py

Python script for watching directories and auto-sending files.

**Usage:**
```bash
python3 scripts/auto_send.py [options]

Options:
  --watch PATH       Directory to watch (default: workspace)
  --recipient ID     Target recipient open_id
  --pattern PATTERN  File pattern to match (default: *)
  --once             Send existing files and exit (don't watch)
```

**Examples:**
```bash
# Watch and auto-send all new PDFs
python3 scripts/auto_send.py --pattern "*.pdf" --recipient USER_ID

# One-time send of all docx files
python3 scripts/auto_send.py --pattern "*.docx" --once
```

## Troubleshooting

### File Not Found
- Ensure file path is absolute
- Verify file exists: `ls -la <filepath>`
- Check file permissions

### Send Failed
- Verify file size < 30MB
- Check recipient open_id is correct
- Ensure bot has permission to send files

### Large Files
For files > 30MB:
1. Compress: `zip -r output.zip large_file`
2. Split: `split -b 25M large_file part_`
3. Use cloud storage and send link instead

## Best Practices

1. **Always verify** files exist before sending
2. **Use descriptive filenames** for better organization
3. **Batch similar files** to reduce API calls
4. **Clean up** sent files periodically to save space
5. **Log sent files** for tracking (optional)

## Examples

### Example 1: Send Generated Document

User: "Generate a report and send it to me"

```javascript
// After generating the report
{
  "action": "send",
  "filePath": "/root/.openclaw/workspace/report_2024.docx",
  "filename": "Annual_Report_2024.docx",
  "message": "Here's your annual report!"
}
```

### Example 2: Send Multiple Files

User: "Send all the PDFs in my workspace"

```bash
# Find and send all PDFs
find /root/.openclaw/workspace -name "*.pdf" -exec \
  python3 -c "import sys; print(sys.argv[1])" {} \;
```

Then send each file using the message tool.

### Example 3: Auto-Send on Completion

After a long-running task generates output:

```javascript
// Task completed, auto-send result
{
  "action": "send",
  "filePath": "/root/.openclaw/workspace/output.pdf",
  "message": "Task completed! Here's your file."
}
```
