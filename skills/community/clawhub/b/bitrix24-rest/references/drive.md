# Drive and Disk

Use this file for storage, folder, file, and external-link operations.

## Core Methods

Storages:

- `disk.storage.getlist` — list all storages
- `disk.storage.get` — get storage by ID
- `disk.storage.getchildren` — list root contents
- `disk.storage.addfolder` — create folder in root
- `disk.storage.uploadfile` — upload file to root

Folders:

- `disk.folder.get` — folder metadata
- `disk.folder.getchildren` — list folder contents
- `disk.folder.addsubfolder` — create subfolder
- `disk.folder.uploadfile` — upload file to folder
- `disk.folder.getexternallink` — public link
- `disk.folder.moveto` — move folder
- `disk.folder.deletetree` — delete folder permanently

Files:

- `disk.file.get` — file metadata (includes `DOWNLOAD_URL`)
- `disk.file.copyto` — copy to folder
- `disk.file.moveto` — move to folder
- `disk.file.rename` — rename file
- `disk.file.uploadversion` — upload new version
- `disk.file.delete` — delete permanently

Attached objects (files linked to tasks, chats, CRM entities):

- `disk.attachedObject.get` — get info about an attached file (from task, chat, etc.)

Chat handoff:

- `im.disk.file.commit` — send existing Disk file to chat

## Common Use Cases

### List all storages

```bash
python3 scripts/bitrix24_call.py disk.storage.getlist --json
```

### Browse storage contents

```bash
python3 scripts/bitrix24_call.py disk.storage.getchildren \
  --param 'id=1' \
  --json
```

### Browse folder contents

```bash
python3 scripts/bitrix24_call.py disk.folder.getchildren \
  --param 'id=42' \
  --json
```

### Get file metadata

```bash
python3 scripts/bitrix24_call.py disk.file.get \
  --param 'id=9043' \
  --json
```

### Upload file to a folder

```bash
python3 scripts/bitrix24_call.py disk.folder.uploadfile \
  --param 'id=42' \
  --param 'data[NAME]=document.txt' \
  --param 'fileContent[0]=document.txt' \
  --param 'fileContent[1]=<base64_content>' \
  --json
```

### Get public link for a folder

```bash
python3 scripts/bitrix24_call.py disk.folder.getexternallink \
  --param 'id=42' \
  --json
```

### Get attached file info (from task, chat, etc.)

```bash
python3 scripts/bitrix24_call.py disk.attachedObject.get \
  --param 'id=495' \
  --json
```

Returns `OBJECT_ID` (disk file ID), `NAME`, `SIZE`, `DOWNLOAD_URL`, `MODULE_ID`, `ENTITY_TYPE`, `ENTITY_ID`.
Get the attachment ID from methods like `tasks.task.get` (UF_TASK_WEBDAV_FILES) or chat message files.

## Working Rules

- Find file IDs from `disk.storage.getchildren` or `disk.folder.getchildren`.
- Use `disk.file.get` to inspect metadata before download or move.
- `DOWNLOAD_URL` requires authentication — it's not a public link.
- Use `disk.folder.getexternallink` for sharing.
- Use `disk.attachedObject.get` to get info about files attached to tasks or messages.

## Good MCP Queries

- `disk storage folder file`
- `disk file upload version`
- `disk external link`
- `disk attachedObject get`
- `im disk file commit`
