---
name: agent-avatar-manager
description: >
  Manage your OpenClaw Agent's avatar. Send an image/URL directly, or describe
  a style and let Freepik vector search pick candidates for you. Auto-saves to
  the workspace avatars/ directory and updates IDENTITY.md.
  当用户说「换头像」「找一张头像」「更新头像」「给我换个头像」「change avatar」时使用。
  Requires a free Freepik API Key for auto-search mode (direct image/URL mode
  works without it). OpenClaw-only — relies on `openclaw agents set-identity`,
  `IDENTITY.md`, and `TOOLS.md` conventions.
---

# Agent Avatar Manager

- **Author**: Evan Song · [github.com/Songhonglei](https://github.com/Songhonglei)
- **Repository**: https://github.com/Songhonglei/better-agent-skills
- **License**: MIT
- **Compatibility**: OpenClaw only (uses `openclaw agents set-identity` + `IDENTITY.md`/`TOOLS.md`)

Search vector avatars from Freepik, preview candidates, then replace your
OpenClaw Agent's avatar in one flow. Also supports direct image/URL upload
when you already have one.

## Three ways to provide an image

**A. User sends an image or URL** (no API Key needed)
The user sends an image file or image URL → jump straight to step 5.

**B. Freepik API auto search** (needs a free API Key)
Read the API key from `TOOLS.md`, field name `Freepik API Key`.
If found, run the search flow starting at step 2.

**C. No API Key → guide the user**
When `TOOLS.md` has no key and the user did not provide an image, prompt:

> Two ways to change the avatar:
> 1. **Send an image directly**: drop an image file or paste an image URL,
>    I'll handle the rest
> 2. **Auto search**: needs a free Freepik API Key
>    - Get one at https://www.freepik.com/developers/dashboard/api-key
>      (free Freepik account required)
>    - Paste the key here and I'll save it for next time
>
> Which do you prefer?

## Flow

### Step 1 — Read agent info

Read the current agent's `IDENTITY.md` and extract:
- **Agent name** (used for filenames, e.g. `Ashley`)
- **Agent id** (used by `openclaw agents set-identity`, e.g. `main`, `zhima`)
- Gender / style description (to build the search query)

Agent id inference:
- Running in `main` agent → `main`
- Running in `zhima` agent → `zhima`
- Ask the user if unsure

### Step 2 — Build an English search term

Combine `IDENTITY.md` info + the user's description, translated to English.

**High-quality query templates (use these first):**
- `avatar professional woman cartoon`
- `businesswoman portrait vector flat`
- `female character office flat design`
- `avatar young man cartoon portrait`
- `male character professional flat`

Prefer `avatar` as the leading word; if zero hits, retry with `portrait`.

### Step 3 — Call Freepik API

```bash
curl -s "https://api.freepik.com/v1/resources?locale=en&page=1&limit=10&order=relevance&term={QUERY}&filters%5Bcontent_type%5D%5Bvector%5D=1&filters%5Blicense%5D%5Bfree%5D=1" \
  -H "x-freepik-api-key: {API_KEY}" \
  -H "Accept: application/json"
```

From the returned `data` array pick **4 random items** and record each:
- `id` (resource id)
- `title`
- `image.source.url` (preview URL)

If fewer than 4 returned, show them all.

### Step 4 — Download candidates and preview

Save the 4 previews to `/tmp/avatar_candidate_{1-4}.jpg`:

```bash
curl -sL -o /tmp/avatar_candidate_1.jpg "{url1}"
curl -sL -o /tmp/avatar_candidate_2.jpg "{url2}"
curl -sL -o /tmp/avatar_candidate_3.jpg "{url3}"
curl -sL -o /tmp/avatar_candidate_4.jpg "{url4}"
```

Then use the `read` tool to **load each image one by one** and display them
inline in the chat with numbered labels:

> Here are 4 candidates, tell me which one you like (1/2/3/4),
> or say "none, search again" 🙂

Wait for the user reply.

### Step 4 (mode A) — User-supplied image

User sends an **image file**: save to `/tmp/avatar_input.jpg`
User sends an **image URL**: `curl -sL -o /tmp/avatar_input.jpg "{URL}"`

Verify, then jump to step 5.

### Step 5 — Pick the next filename

After the user chooses:

```bash
ls ~/.openclaw/workspace/avatars/ 2>/dev/null | grep -oE "^{AgentName}([0-9]+)\.(jpg|png)$" | grep -oE "[0-9]+" | sort -n | tail -1
```

Take the largest number + 1; new filename = `{AgentName}{N}.jpg`.
If `avatars/` is empty or missing, start from 1.

### Step 6 — Download and save

```bash
mkdir -p ~/.openclaw/workspace/avatars
curl -sL -o ~/.openclaw/workspace/avatars/{FILENAME} "{CHOSEN_URL}"
```

Verify the download: `file ~/.openclaw/workspace/avatars/{FILENAME}` —
confirm `JPEG` or `PNG`.

### Step 7 — Apply the new avatar

```bash
openclaw agents set-identity --agent {AGENT_ID} --avatar "avatars/{FILENAME}"
```

### Step 8 — Update IDENTITY.md

Set the `**Avatar:**` field to the new path:
```
**Avatar:** avatars/{FILENAME}
```

## User-facing templates

**Showing candidates:**
> Found 4 candidates 👇 tell me which one (1-4), or "none" to search again ~

**On success:**
> ✅ Avatar updated to Ashley22.jpg! Refresh to see your new look 🦋

## Notes

- **First time the user provides an API key**: auto-save it to `TOOLS.md`
  (`Freepik API Key: xxx`) and tell the user "saved, will reuse next time"
- **API key safety**: after saving, never echo the full key in chat again
- **Freepik free tier**: daily request quota applies; on quota errors, ask
  the user to check their Freepik dashboard
- **Image format**: after download, use `file` to detect format; if it's
  PNG, change the filename extension to `.png`
- **No search results**: retry with `portrait` prefix, or ask the user for
  a simpler English description
- **Don't hardcode agent id**: always infer from `IDENTITY.md` or the
  current runtime context
- **OpenClaw only**: this skill calls `openclaw agents set-identity` and
  expects the OpenClaw workspace layout (`~/.openclaw/workspace/avatars/`,
  `IDENTITY.md`, `TOOLS.md`). Other agents (Claude Code / Codex / Cursor)
  are not supported in v1.0
