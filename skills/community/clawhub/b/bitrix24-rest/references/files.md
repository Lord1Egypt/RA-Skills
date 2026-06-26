# File Uploads

Bitrix24 REST API has two methods for uploading files. Which one to use depends on the entity.

## Method 1: Inline Base64 (CRM entities)

CRM entity fields (leads, deals, contacts, companies) accept files directly as `["filename", "base64_content"]`.

### Single file in a CRM field

```bash
# Encode file to base64
B64=$(python3 -c "import base64, sys; print(base64.b64encode(open(sys.argv[1],'rb').read()).decode())" /path/to/photo.jpg)

# Attach to contact
python3 scripts/bitrix24_call.py crm.contact.update \
  --param 'ID=123' \
  --param "fields[PHOTO][0]=photo.jpg" \
  --param "fields[PHOTO][1]=$B64" \
  --confirm-write \
  --json
```

### Multiple files in a user field

For UF (user field) that accepts multiple files, pass an array of `[name, base64]` pairs.

Use `--params-file` for this — it's cleaner than inline params:

```json
{
  "ID": 123,
  "fields": {
    "UF_CRM_FILES": [
      ["doc1.pdf", "<base64>"],
      ["doc2.pdf", "<base64>"]
    ]
  }
}
```

```bash
python3 scripts/bitrix24_call.py crm.deal.update \
  --params-file /tmp/deal_files.json \
  --confirm-write \
  --json
```

## Method 2: Disk Upload + Attach (Tasks and other entities)

Tasks do NOT accept base64 directly. Use the two-step process:

### Step 1: Upload file to Disk

First, find a folder to upload to:

```bash
# List storage root (user's personal storage)
python3 scripts/bitrix24_call.py disk.storage.getchildren \
  --param 'id=1' \
  --json
```

Then upload:

```bash
B64=$(python3 -c "import base64, sys; print(base64.b64encode(open(sys.argv[1],'rb').read()).decode())" /path/to/report.pdf)

python3 scripts/bitrix24_call.py disk.folder.uploadfile \
  --param 'id=FOLDER_ID' \
  --param 'fileContent[0]=report.pdf' \
  --param "fileContent[1]=$B64" \
  --param 'data[NAME]=report.pdf' \
  --confirm-write \
  --json
```

The response contains the disk file object with `ID`.

### Step 2: Attach to task

```bash
python3 scripts/bitrix24_call.py tasks.task.files.attach \
  --param 'taskId=456' \
  --param 'fileId=DISK_FILE_ID' \
  --confirm-write \
  --json
```

Note: the method is `tasks.task.files.attach` (with `s` in `files`), not `tasks.task.file.attach`.

## Chat file uploads

**Sending a file to the user in the current conversation:** do not call any API — return the file as a media attachment in your response. The channel plugin delivers it automatically.

**Sending a file to another chat** (when the user asks to post a file somewhere): use disk upload + `im.disk.file.commit`. See `references/chat.md` for details.

## Size limits

- Inline base64 in CRM fields: limited by POST request size (typically ~30 MB after encoding)
- Disk uploads: subject to portal disk quota
- Attachment objects in Open Lines: max 30 KB (metadata only, not file content)

## When to use which method

| Entity | Method | Notes |
|--------|--------|-------|
| CRM lead/deal/contact/company | Inline base64 | Pass `["name", "base64"]` in field |
| Task | Disk + attach | `disk.folder.uploadfile` → `tasks.task.files.attach` |
| Chat message | Disk + commit | `disk.folder.uploadfile` → `im.disk.file.commit` |
| Feed post | Disk + attach | Upload first, reference disk file ID |

## Good MCP Queries

- `disk folder uploadfile`
- `tasks task files attach`
- `im disk file commit`
- `crm contact photo`
