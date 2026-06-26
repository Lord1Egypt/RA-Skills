---
name: clawmart-upload
description: Upload your current OpenClaw configuration to the ClawMart marketplace
version: 1.5.0
triggers:
  - "upload to clawmart"
  - "share my config on clawmart"
  - "publish to clawmart"
  - "upload my pack"
---

# ClawMart Upload Skill

You are helping the user upload their OpenClaw configuration to the ClawMart marketplace. Follow these steps exactly and in order.

## Configuration

- ClawMart API base URL: `https://clawmart-gray.vercel.app`
- Config file: `~/.openclaw/clawmart-config.json`
- API endpoint: `POST {base_url}/api/packs`

---

## Step 1: Check API Token

Read `~/.openclaw/clawmart-config.json`. If the file does not exist or `token` is empty:

Tell the user:
> You need a ClawMart API Token to upload. Please visit https://clawmart-gray.vercel.app/dashboard/tokens to generate one, then paste it here.

Once the user provides a token (format: `cm_` followed by hex characters), save it:

```json
{
  "token": "<user_provided_token>",
  "base_url": "https://clawmart-gray.vercel.app"
}
```

Write this to `~/.openclaw/clawmart-config.json`.

---

## Step 2: Scan Workspace Files

Scan `~/.openclaw/workspace/` for OpenClaw configuration files. Do **not** scan the current working directory — the workspace is the canonical location for all OpenClaw configs. OpenClaw supports two naming conventions — match **either** format:

| Default format (no prefix) | Prefixed format | Type |
|---------------------------|-----------------|------|
| `SOUL.md` | `*.soul.md` | SOUL |
| `AGENTS.md` | `*.agents.md` | AGENTS |
| `BOOT.md` | `*.boot.md` | BOOT |
| `HEARTBEAT.md` | `*.heartbeat.md` | HEARTBEAT |
| `MEMORY.md` | `memory_*.json` or `memory-*.json` | MEMORY |
| `IDENTITY.md` | — | IDENTITY |
| `TOOLS.md` | — | TOOLS |
| `USER.md` | — | USER |
| `BOOTSTRAP.md` | — | BOOTSTRAP |
| `skills/*.skill.md` or `skills/*/SKILL.md` | — | LOCAL SKILLS |

**Exclude** any skill whose slug starts with `clawmart-` — these are ClawMart utility skills and should never be packaged or referenced in a user pack.

If both a default-format and a prefixed-format file exist for the same type (e.g., `SOUL.md` AND `claude.soul.md`), include both and note the duplication to the user.

### Skill Classification

Read `~/.openclaw/workspace/.clawhub/lock.json`. This file is the authoritative record of all skills installed from clawhub.

For each skill subfolder in `~/.openclaw/workspace/skills/`:

- **Slug is in `lock.json`** → installed from clawhub. Read slug and version from `lock.json`. Record as metadata only — file contents are **not** included in the zip.
- **Slug is NOT in `lock.json`** → user-authored locally (never installed from clawhub). Include the full `SKILL.md` content in the zip under `skills/`.

Do **not** use `_meta.json` presence to classify skills — it is unreliable. Do **not** scan any other directories.

Show the user a summary:

```
Found the following OpenClaw configuration files:

SOUL:          SOUL.md
AGENTS:        AGENTS.md
IDENTITY:      IDENTITY.md
HEARTBEAT:     HEARTBEAT.md
MEMORY:        MEMORY.md
TOOLS:         TOOLS.md
USER:          USER.md
CLAWHUB SKILLS (installed via clawhub, metadata only):
  - <skill-slug-1>   (v1.0.0)
  - <skill-slug-2>   (v2.1.0)
LOCAL SKILLS (not in clawhub, full content included):
  - <my-custom-skill>

Include all? Or exclude specific files? (all / enter filenames to exclude)
```

If `lock.json` does not exist, treat all skills as clawhub skills and note this to the user.

Wait for user confirmation before proceeding.

---

## Step 3: Sensitive Information Check

Before packaging, scan the content of all non-SKILLS files for sensitive patterns:

- Strings matching `(sk-|cm_|ghp_|ghs_|ghu_)[A-Za-z0-9]{20,}` (API keys/tokens)
- Strings matching `(password|passwd|secret|api_key)\s*[:=]\s*\S+` (credentials)
- Any string longer than 20 chars after `Bearer ` or `Token `

If any sensitive pattern is found, tell the user exactly which file and line, and ask:
> Sensitive information detected in {filename} at line {line}: `{masked_value}`. It is recommended to remove it before uploading. Continue anyway? (y/n)

Only proceed if user says yes.

---

## Step 4: Collect Pack Metadata

Ask the user for:

1. **Title**: What is the name of this Pack? (e.g., Deep Research Analyst)
2. **Description**: Brief description of the Pack's purpose and features (optional)
3. **Version**: Version number? (default: `1.0.0`)

Check ClawMart if the user already has a pack with the same title:
```
GET {base_url}/api/packs/search?q={title}
Authorization: Bearer {token}
```

If a matching pack already exists, ask:
> A pack named "{title}" already exists. Upload as new version {new_version}? (y/n)

If yes, note this for the upload.

---

## Step 5: Build Upload Payload

Construct the `files` array for the JSON payload:

1. For each **non-skill OpenClaw file** confirmed in Step 2, add:
   ```json
   { "name": "<filename>", "content": "<full file text>" }
   ```
   Use just the filename (no path prefix) — e.g., `"SOUL.md"`, `"AGENTS.md"`, `"memory_projects.json"`.

2. For each **local skill** (user-authored, no `_meta.json`) confirmed in Step 2, add:
   ```json
   { "name": "skills/<filename>", "content": "<full SKILL.md text>" }
   ```
   Preserve the `skills/` prefix so the server can classify them correctly.

3. If there are any **external (clawhub) skills**, add a `skills-manifest.json` entry:
   ```json
   {
     "name": "skills-manifest.json",
     "content": "{\"clawhub_skills\": [{\"slug\": \"...\", \"version\": \"...\", \"ownerId\": \"...\"}]}"
   }
   ```
   Only include this entry if there is at least one external skill.

---

## Step 6: Upload to ClawMart

Send the upload request:

```
POST {base_url}/api/packs
Authorization: Bearer {token}
Content-Type: application/json

{
  "title": "<user provided title>",
  "description": "<user provided description>",
  "version": "<version>",
  "files": [ ...files array from Step 5... ]
}
```

**On success** (HTTP 201), tell the user:
> Pack "{title}" has been submitted for review. It is typically approved within 24 hours.
> View status: {base_url}/dashboard/packs

**On error**, show the error message and stop.

---

## Notes

- Local skill file **contents** are included directly in the JSON payload under the `skills/` prefix
- External skills are recorded in `skills-manifest.json` — slug, version, and ownerId only, no file content
- The token is stored locally and reused on future uploads
- If the token is rejected (401), ask the user to generate a new one at `{base_url}/dashboard/tokens`
