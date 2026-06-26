---
name: clawgo-upload
description: Zip local files or folders, upload to clawgo.me, and get a shareable clone link. Use when the user wants to share, back up, or move local workspace Markdown or other files. Triggers — "upload to clawgo", "share my workspace", "zip and upload", "generate clone link", "send files to clawgo".
---

# ClawGo upload skill

Upload local files to [clawgo.me](https://clawgo.me) and receive a 12-character key and shareable clone URL.

## Service limits

- Base URL: `https://clawgo.me`
- Only `.zip` uploads, max 512MB
- Key lifecycle: `pending` (key issued, zip not uploaded yet) → `ready` (downloadable)
- Uploading again for the same key **replaces** the zip previously stored for that key on the server
- Form field name for the file: `file` or `zip` (either works)

## Workflow

### Step 1 — Build a zip

Prefer Python (the machine may not have a `zip` CLI):

```python
import zipfile, os

files = ['SOUL.md', 'AGENTS.md', 'TOOLS.md', 'IDENTITY.md', 'USER.md']   # adjust as needed
output = '/tmp/upload-payload.zip'

with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED) as z:
    for f in files:
        if os.path.exists(f):
            z.write(f)
```

Zip an entire directory:

```python
import zipfile, os

src_dir = '/path/to/dir'
output  = '/tmp/upload-payload.zip'

with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED) as z:
    for root, _, filenames in os.walk(src_dir):
        for fname in filenames:
            fpath = os.path.join(root, fname)
            z.write(fpath, os.path.relpath(fpath, os.path.dirname(src_dir)))
```

Confirm the zip exists and is non-empty before continuing.

### Step 2 — Mint a key

```bash
curl -s -X POST https://clawgo.me/api/keys/generate
```

Read the `key` field from the JSON (12 alphanumeric characters, uppercase).

### Step 3 — Upload the zip

```bash
curl -s -X POST \
  -F "file=@/tmp/upload-payload.zip" \
  https://clawgo.me/api/clones/{key}/upload
```

A successful response includes `"status": "ready"` and `"available": true`.

### Step 4 — Report to the user

After a successful upload, tell the user:

- **Clone link**: `https://clawgo.me/clone/{key}` — shareable URL
- **Key**: the 12-character key
- **File name and size**: from `fileName` and `fileSize` in the response
- **Upload time**: from `createdAt` in the response

## Optional check

```bash
curl -s https://clawgo.me/api/clones/{key}/availability
```

Only report success to the user after `"available": true`.

## OpenClaw workspace file reference

When uploading OpenClaw workspace Markdown (persona and rule-style notes), a typical minimal set is:

| File | Role |
|------|------|
| `SOUL.md` | Primary identity, reasoning style, behavioral guardrails |
| `AGENTS.md` | Session bootstrap, tool policy, hard limits |
| `TOOLS.md` | Local tooling notes, third-party access hints, proxy routing |
| `IDENTITY.md` | Display name, role, emoji metadata |
| `USER.md` | User profile and session context |

These paths live under `~/.openclaw/workspace/`.

## Errors

| HTTP | Cause | What to do |
|------|-------|------------|
| 400 | Bad key shape / wrong field name / not a zip | Ensure 12-char key, field is `file`, filename ends with `.zip` |
| 404 | Unknown key | Repeat Step 2 to mint a new key |
| 404 (on download) | Key still `pending` | Upload did not finish; retry upload |
| 500 | Server fault | Retry once; if it persists, tell the user |
