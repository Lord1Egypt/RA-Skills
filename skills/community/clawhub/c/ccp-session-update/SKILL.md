---
name: ccp-session-update
version: 1.0.0
description: Context Continuity Protocol session update — the ops sequence Liv runs
  at the end of every significant session. Updates STATUS.md, posts to Notion daily
  log, syncs Obsidian vault, and creates Plane issues for new work items.
metadata:
  openclaw:
    emoji: 📋
    requires:
      bins:
      - docker
      env:
      - NOTION_API_KEY
    network:
      outbound: true
      reason: Posts to Notion Daily Activity Log API and optionally creates Plane
        issues.
---

# CCP Session Update

**Context Continuity Protocol** — the ops sequence Liv runs at the end of every significant session.
Goal: zero knowledge loss between sessions, channels, and agents.

---

## What a CCP update covers

Four layers, in order of priority:

| Layer | Where | Why |
|---|---|---|
| **STATUS.md** | Disk (`projects/<slug>/STATUS.md`) | Ground truth. Any agent, any session can read it. Write this FIRST. |
| **Notion** | Cloud (Daily Activity Log DB) | Nissan's overview — human-readable summary of what happened |
| **Obsidian Vault** | Proton Drive (`~/Library/CloudStorage/ProtonDrive-monkfenix@proton.me-folder/Vault/`) | Personal knowledge base — daily note + per-project file |
| **Plane** | Local Docker (`localhost:8086`) | Task tracking — create issues for new work, close completed ones |

**Always write STATUS.md before spawning Liv.** It's the source Notion and Obsidian summarise from. Race condition if you write it after.

---

## 1. STATUS.md — update pattern

For **every project touched** in the session:

```bash
# Step 1: Read first — never overwrite blindly
cat projects/<slug>/STATUS.md

# Step 2: Update in place
```

**Canonical format:**

```markdown
# [Project Name] — STATUS
_Last updated: YYYY-MM-DD HH:MM AEST_

## RESUME FROM HERE
[Single clear statement of the true next action — not a list]

## Live URLs
[All deployed endpoints, GitHub, devnet addresses]

## Current State
[Key metrics, test results, what shipped]

## Key Decisions
- YYYY-MM-DD: [decision] [APPEND ONLY — never delete old entries]

## Blockers
[What's pending, who owns it — clear resolved ones]
```

**Rules:**
- Timestamp at top, every update
- RESUME FROM HERE = one sentence, actionable
- Key Decisions = append-only ledger (never delete)
- Clear resolved blockers, add new ones
- Update Live URLs if anything deployed or changed

---

## 2. Notion Daily Activity Log

**DB ID:** `322eb552-581a-81e5-beb0-d1f361e7580f`
⚠️ NOT `322eb552-581a-810c-876b-d70978cd976c` — that ID is wrong, API will 404.

**API key:** Use the **Paid** key — the old key is revoked:
```bash
NOTION_KEY=$(op item get bg2gpqhpta6an5n4prn2zzycya --vault OpenClaw --reveal --fields credential)
```

**Create a log entry:**

```bash
curl -s -X POST https://api.notion.com/v1/pages \
  -H "Authorization: Bearer $NOTION_KEY" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{
    "parent": { "database_id": "322eb552-581a-81e5-beb0-d1f361e7580f" },
    "properties": {
      "Name": { "title": [{ "text": { "content": "Session title — YYYY-MM-DD" } }] },
      "Date": { "date": { "start": "YYYY-MM-DD" } },
      "Agent": { "rich_text": [{ "text": { "content": "Loki" } }] }
    }
  }'
```

Keep the title descriptive: `"Hackathon wrap + tour video — 2026-03-24"` beats `"Session log"`.

---

## 3. Obsidian Vault — update pattern

**Vault path:** `~/Library/CloudStorage/ProtonDrive-monkfenix@proton.me-folder/Vault/`

Two files to write per session:

### Daily note — `Vault/daily/YYYY-MM-DD.md`

Create or append. This is what Nissan reads first.

```markdown
# YYYY-MM-DD

## What happened
[2-3 paragraphs, human-readable prose — not a task list]

## Agents active
- Loki (orchestration)
- Kit (code)
- Quill (journal)
- Liv (CCP)

## Decisions
- [key decision 1]
- [key decision 2]

## Tomorrow
[What's next — copy from STATUS.md RESUME FROM HERE]
```

### Project file — `Vault/projects/<slug>.md`

Create if new project, update if existing.

```markdown
# [Project Name]

_Status: [Active / Shipped / Paused]_
_Last updated: YYYY-MM-DD_

## What it is
[One paragraph]

## Live URLs
[Copy from STATUS.md]

## Current state
[Where things stand]

## Next steps
[Copy from STATUS.md RESUME FROM HERE]
```

---

## 4. Plane — the non-obvious auth pattern

⚠️ **Critical:** Plane CE does NOT support HTTP API token auth. A valid token in `~/.config/openclaw/.plane-api-token` exists but returns 401 on every HTTP call. Do not debug this. It will never work.

**The only working pattern is Django shell via Docker:**

```bash
docker exec plane-aio bash -c "
cd /app/backend
python manage.py shell -c \"
from plane.db.models import Issue, Project, State
from django.contrib.auth import get_user_model
User = get_user_model()
user = User.objects.filter(email='monkfenix@proton.me').first()

proj = Project.objects.get(identifier='AGNT')
state = State.objects.filter(project=proj, name='Done').first()

i = Issue.objects.create(
    project=proj,
    workspace=proj.workspace,
    name='Issue title here',
    description='Optional description',
    state=state,
    created_by=user
)
print(f'{proj.identifier}-{i.sequence_id}: {i.name}')
\"
"
```

**Project identifiers:**

| ID | Project |
|---|---|
| `AGNT` | Agent Team |
| `INFRA` | Infrastructure & Ops |
| `GROW` | Content & Growth |
| `SAND` | SandSync |
| `CLAW` | OpenClaw Config |
| `HCP` | Hybrid Control Plane |
| `MAXX` | Maxx |

**State names:** `Backlog` · `Todo` · `In Progress` · `Done` · `Cancelled`

Change `name=` and `identifier=` per issue. Run multiple issues in one shell invocation if needed.

---

## 5. Agent delegation

| Task | Agent | Notes |
|---|---|---|
| STATUS.md updates | Loki | Must happen BEFORE Liv is spawned |
| Notion Daily Log | Liv | API call, ~30 seconds |
| Obsidian Vault files | Liv | Write daily note + project file(s) |
| Plane issue creation | Liv | Django shell — see pattern above |
| Journal entries | Quill | Spawned separately with OUTBOX content |

**Spawn Quill and Liv in parallel** — they don't depend on each other. Quill needs OUTBOX entries written first; Liv needs STATUS.md written first.

---

## 6. Common mistakes

| Mistake | Fix |
|---|---|
| Using Notion DB ID with `810c` in it | Use `81e5` — `322eb552-581a-**81e5**-beb0-d1f361e7580f` |
| Using old Notion API key (`op://OpenClaw/Notion API Key/credential`) | Use item ID `bg2gpqhpta6an5n4prn2zzycya` — old key is revoked |
| Debugging Plane HTTP token auth | Don't. Use Django shell only. Always. |
| Writing STATUS.md after spawning Liv | Race condition — STATUS.md is the source. Write it first. |
| Skipping Obsidian daily note | Nissan reads this. It's the most human-facing output of the wrap. |
| Overwriting STATUS.md without reading it first | Always `cat` first — Key Decisions are append-only, can't recover deleted ones |
| Creating new STATUS.md from scratch | Read existing first. Preserve all Key Decisions. |

---

## Quick checklist

```
[ ] STATUS.md updated for each project touched (timestamp, RESUME, decisions, blockers)
[ ] Notion Daily Log entry created (correct DB ID + active API key)
[ ] Obsidian daily note written (Vault/daily/YYYY-MM-DD.md)
[ ] Obsidian project file(s) updated (Vault/projects/<slug>.md)
[ ] Plane issues created/closed for new work items (Django shell)
[ ] Quill spawned for journal entries (if OUTBOX entries exist)
```
