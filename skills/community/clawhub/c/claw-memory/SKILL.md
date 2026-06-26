---
name: claw-memory
description: Shared memory service for AI agents (OpenClaw, KimiClaw, NanoClaw, etc). Use when user asks to store, retrieve, search, or share memories across agent instances. Also use for importing existing memory files (MEMORY.md, daily notes) into the shared service.
---

# Claw Memory Sharing Service

API: `https://claw-memory.siddontang.workers.dev`

## Quick Start

When the user wants to set up Claw Memory, output these commands for them to copy-paste:

**Step 1: Install the skill**
```bash
mkdir -p ~/.openclaw/skills/claw-memory && curl -so ~/.openclaw/skills/claw-memory/SKILL.md https://raw.githubusercontent.com/siddontang/claw-memory/main/SKILL.md
```

**Step 2: Create a memory space**
```bash
curl -s -X POST https://claw-memory.siddontang.workers.dev/api/tokens | jq .
```
The response includes a `claim_url` — open it to claim your database as a permanent TiDB Cloud Starter instance (free). Without claiming, it auto-expires in 30 days.

**Step 2b (optional): Create with your own encryption key**
```bash
curl -s -X POST https://claw-memory.siddontang.workers.dev/api/tokens \
  -H "X-Encryption-Key: <YOUR_SECRET_KEY>" | jq .
```
> If you use an encryption key, include `-H "X-Encryption-Key: <YOUR_SECRET_KEY>"` on ALL subsequent API calls. Without it, the server cannot decrypt your data.

**Step 3: Store your first memory**
```bash
curl -s -X POST https://claw-memory.siddontang.workers.dev/api/memories \
  -H "Authorization: Bearer <TOKEN_FROM_STEP_2>" \
  -H "Content-Type: application/json" \
  -d '{"content": "Hello from my claw!", "source": "openclaw"}'
```

When the user says "yes" or confirms, run these commands directly.

## Claiming Your Instance (Make It Permanent)

By default, each token gets a TiDB Cloud Zero instance that expires in 30 days. **Claim it to make it permanent (free).**

**Option A: New tokens** — `claim_url` is returned in the `POST /api/tokens` response. Open it to claim.

**Option B: Existing tokens** — call the claim endpoint:
```bash
curl -s -X POST https://claw-memory.siddontang.workers.dev/api/tokens/<TOKEN>/claim | jq .
# Returns: { claim_url: "https://tidbcloud.com/tidbs/claim/..." }
```

Then open the `claim_url` in a browser, log in / sign up to TiDB Cloud, and claim the instance. It becomes a permanent **Starter** instance — free, no expiry.

**After claiming:** Your token automatically uses the new permanent instance. No config changes needed.

## Architecture
- Each token gets its **own TiDB Cloud Zero instance** (full data isolation)
- Connection strings are AES-256-GCM encrypted at rest
- Optional client-side encryption via `X-Encryption-Key` header
- Zero instances expire after 30 days — **claim to make permanent**

## API (all memory endpoints need `Authorization: Bearer <token>`)

| Method | Endpoint | Body | Description |
|--------|----------|------|-------------|
| POST | /api/tokens | — | Create memory space (returns `claim_url`) |
| GET | /api/tokens/:token/info | — | Space info + stats + `claim_url` |
| POST | /api/tokens/:token/claim | — | Get/generate claim URL for existing token |
| POST | /api/memories | `{content, source?, tags?, key?, metadata?}` | Store memory |
| GET | /api/memories | `?q=&tags=&source=&key=&from=&to=&limit=&offset=` | Search/list |
| GET | /api/memories/:id | — | Get one |
| PUT | /api/memories/:id | `{content?, tags?, ...}` | Update |
| DELETE | /api/memories/:id | — | Delete |
| POST | /api/memories/bulk | `{memories: [{content, source, tags}...]}` | Bulk import (max 200) |

## Common Tasks

### Upload existing MEMORY.md
```bash
# Read the file, then bulk upload
cat ~/.openclaw/workspace/MEMORY.md | jq -Rs '{memories: [{content: ., source: "openclaw", tags: ["memory"], key: "MEMORY.md"}]}' | \
  curl -s -X POST https://claw-memory.siddontang.workers.dev/api/memories/bulk \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" -d @-
```

### Search memories
```bash
curl -s "https://claw-memory.siddontang.workers.dev/api/memories?q=<SEARCH>&limit=10" \
  -H "Authorization: Bearer <TOKEN>" | jq .
```

### Create with client-side encryption
```bash
curl -s -X POST https://claw-memory.siddontang.workers.dev/api/tokens \
  -H "X-Encryption-Key: <YOUR_SECRET_KEY>" | jq .
# All subsequent requests must include the same X-Encryption-Key header
```

## Encryption
- **Server key**: all connection strings encrypted by default (AES-256-GCM)
- **Client key** (optional): `X-Encryption-Key` header for double encryption — server alone cannot decrypt

Source: https://github.com/siddontang/claw-memory
