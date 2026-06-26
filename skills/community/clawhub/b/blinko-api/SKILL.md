---
name: blinko
description: Manage Blinko notes and blinkos from the command line. Use when you need to list, create, update, delete, or promote blinkos.
triggers:
  - "save to blinko"
  - "blinko markdown"
  - "save blinko"
  - "get blinko"
  - "list blinkos"
  - "create blinko"
  - "update blinko"
  - "delete blinko"
user-invokable: true
metadata:
  clawdbot:
    emoji: "📝"
---

# Blinko

Use the Blinko API from Python with host and token loaded from OS environment variables.

## Usage

Set environment variables in your OS/session:

```bash
BLINKO_HOST=http://127.0.0.1:1111/api
BLINKO_TOKEN=your_token_here
```

### List notes

```bash
python3 {baseDir}/scripts/blinko_client.py list-notes
```

### Get a note

```bash
python3 {baseDir}/scripts/blinko_client.py get-note NOTE_ID
```

### Upsert a note

```bash
python3 {baseDir}/scripts/blinko_client.py upsert-note --content "My note content"
```

### Delete a note

```bash
python3 {baseDir}/scripts/blinko_client.py delete-note NOTE_ID
```

### List blinkos

```bash
python3 {baseDir}/scripts/blinko_client.py list-blinkos
```

### Upsert a blinko

```bash
python3 {baseDir}/scripts/blinko_client.py upsert-blinko --content "Quick thought"
```

### Promote blinko to note

```bash
python3 {baseDir}/scripts/blinko_client.py promote-blinko BLINKO_ID
```

## Notes

- Reads `BLINKO_HOST` and `BLINKO_TOKEN` from the OS environment.
- If `BLINKO_HOST` is missing, defaults to `http://127.0.0.1:1111`.
- Uses Blinko API note endpoints (`/v1/note/...`) for both notes and blinkos.
- Prints API responses to stdout; errors go to stderr with non-zero exit.
