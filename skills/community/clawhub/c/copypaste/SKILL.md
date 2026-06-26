---
name: copypaste-cloud
emoji: 📋
description: "Read and create pastes on copy-paste.cloud. Fetch recent public pastes, retrieve a paste by ID, or publish new content via the public API."
version: 1.0.0
homepage: https://github.com/orti99/copypaste

metadata:
  clawdbot:
    requires:
      env:
        - COPYPASTE_API_KEY
      bins:
        - curl
        - jq
    primaryEnv: COPYPASTE_API_KEY
    files:
      - scripts/get_recent.sh
      - scripts/get_paste.sh
      - scripts/create_paste.sh
---

# copy-paste.cloud

Interact with [copy-paste.cloud](https://copy-paste.cloud) — a lightweight, public pastebin.
Use this skill to read recent public pastes, look up a paste by ID, or publish new content.

An API key is required for reading recent pastes and creating new ones.
Generate your key at [copy-paste.cloud/developer](https://copy-paste.cloud/developer).

---

## When to Use

Activate this skill when the user:
- Asks to **post**, **paste**, **share**, or **publish** a snippet, code block, or text to copy-paste.cloud
- Asks to **read**, **fetch**, **get**, or **show** a paste from copy-paste.cloud (by ID or recent)
- Mentions a URL like `https://copy-paste.cloud/<id>` and wants the content retrieved
- Asks "what's on copy-paste.cloud lately?" or similar

---

## Actions

### 1. Get recent public pastes

Returns the 10 most recent public pastes (sorted newest first).

```bash
bash scripts/get_recent.sh
```

Output: formatted list of paste IDs, titles, languages, and a content preview.

---

### 2. Get a paste by ID

Retrieve the full content and metadata of any public paste.

```bash
bash scripts/get_paste.sh <paste-id>
```

- `paste-id` — the UUID from the paste URL, e.g. `3f2a1c9e-...`

Output: title, language, tags, author, creation date, and full content.

---

### 3. Create a new paste

Publish text or code as a new public paste.

```bash
bash scripts/create_paste.sh \
  --content "your text here" \
  [--title "optional title"] \
  [--language python|javascript|...] \
  [--tags "tag1,tag2"] \
  [--private] \
  [--burn-after-read] \
  [--expires-in-hours 24]
```

Supported languages: `bash`, `c`, `cpp`, `csharp`, `css`, `dockerfile`, `go`, `html`,
`java`, `javascript`, `json`, `kotlin`, `markdown`, `php`, `python`, `ruby`, `rust`,
`sql`, `swift`, `typescript`, `xml`, `yaml`. Omit for plain text.

Output: the URL of the newly created paste.

---

## Configuration

Set your API key as an environment variable:

```bash
export COPYPASTE_API_KEY=cp_your_key_here
```

Generate a key at **https://copy-paste.cloud/developer** after signing in.

---

## External Endpoints

| URL | Method | Data sent |
|-----|--------|-----------|
| `https://api.copy-paste.cloud/api/v1/pastes/recent` | GET | API key (header) |
| `https://api.copy-paste.cloud/api/v1/pastes/{id}` | GET | paste ID (path) |
| `https://api.copy-paste.cloud/api/v1/pastes` | POST | API key (header), paste content, metadata |

---

## Security & Privacy

- Your `COPYPASTE_API_KEY` is sent as a Bearer token to `api.copy-paste.cloud` only.
- Paste content you create is sent to `api.copy-paste.cloud` and stored on copy-paste.cloud servers.
- No data is written to your local filesystem.
- Private pastes (`--private`) are only visible to your account; all others are public.
- Burn-after-read pastes (`--burn-after-read`) are deleted from the server after first view.
