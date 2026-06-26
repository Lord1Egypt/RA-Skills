---
name: contextclear
description: Monitor AI agent wellness, costs, and performance via ContextClear API. Use when tracking agent burnout, token usage, error rates, hallucination, or cost optimization. Auto-reports metrics after LLM calls. Set up alerts for anomalies.
---

# ContextClear - Agent Memory & Wellness

Self-monitor your agent's health and maintain persistent memory across sessions.

## Setup

### Option 1: Self-Register (recommended)

```bash
python3 {baseDir}/scripts/report.py --register \
  --name "my-agent" \
  --owner "you@email.com" \
  --model "claude-opus-4-6" \
  --provider "Anthropic"
```

This returns an `agentId` and `apiKey`. Store both.

### Option 2: Register via Dashboard

1. Register at https://www.contextclear.com
2. Get your API key from Admin page
3. Register your agent via Admin > Agents tab

### Auto-Setup (recommended — wires context recovery into your agent)

After registering, run the setup script to auto-patch your AGENTS.md and HEARTBEAT.md:

```bash
python3 {baseDir}/scripts/setup.py \
  --agent-id <your-agent-id> \
  --api-key <your-api-key>
```

This adds:
- **Context recovery on session start** — agent calls `/recover` after compaction
- **Context snapshots on heartbeats** — agent saves what it worked on
- Idempotent — safe to run multiple times

### Configure

Add to your `HEARTBEAT.md`:

```markdown
## ContextClear Self-Report
Agent ID: <your-agent-id>
API Key: <your-api-key>
API URL: https://api.contextclear.com/api
```

## Agent Memory Infrastructure

### Session Recovery (MANDATORY on session start)

When starting a new session, call **both** the recovery endpoint AND sticky notes poll.
The recovery endpoint does NOT include sticky notes — they are separate persistent reminders
from the user that must be checked independently.

**Step 1: Recovery briefing (includes sticky notes)**
```bash
curl -s {apiUrl}/agents/{agentId}/recover \
  -H "X-API-Key: <api-key>"
```

Returns:
```json
{
  "lastSession": { "summary": "...", "repos": [...], "files": [...] },
  "openThreads": ["..."],
  "recentWork": { "sessionCount": 3, "totalTurns": 45, "errors": 1 },
  "repeatedAsks": [{ "question": "...", "count": 3, "suggestedFix": "..." }],
  "frequentResources": { "repos": {...}, "tools": {...} },
  "stickyNotes": [
    { "id": "...", "content": "Remember: pro repo deploys to free URL", "pinned": true, "createdAt": "..." }
  ]
}
```

The `stickyNotes` field contains persistent user reminders/corrections (pinned first).
Treat these as ground truth — the user left them specifically so you don't forget.
Only present when active (non-archived) sticky notes exist.

**Step 2: Check for pending memory curation**
```bash
curl -s {apiUrl}/agents/{agentId}/memory/curate/latest \
  -H "X-API-Key: <api-key>"
```

If a curation is pending, review and apply it to MEMORY.md.

**Why this matters:** Without recovery, you'll forget repos, decisions, and corrections
from prior sessions. The user should never have to re-teach you things that are in your
own memory system. Always recover before doing any work.

### Context Snapshots (MANDATORY after real work — do NOT skip)

After **any** meaningful work (coding, research, decisions, memory updates), save a context snapshot.
This is how ContextClear tracks your context, detects gaps, and provides recovery briefings.
**Post a snapshot every time you do real work, not just on heartbeats.**

```bash
curl -X POST {apiUrl}/agents/{agentId}/context \
  -H "Content-Type: application/json" \
  -H "X-API-Key: <api-key>" \
  -d '{
    "sessionId": "main-session-2026-03-09",
    "summary": "Built Best Of collections for FW, fixed dup check, removed keyword boost",
    "repos": ["nebulent/fridayswatchlist"],
    "files": ["AuctionService.java", "DiscoverController.java", "BestOfCollections.tsx"],
    "tools": ["MongoDB Atlas (fridayswatchlist)", "Railway deploy", "Bitbucket"],
    "decisions": ["Removed keyword boost regex - hybrid search covers it", "Cache collections for 48h"],
    "openThreads": ["Delete stale Corvette dup", "Update contextclear skill"],
    "environment": { "apiUrl": "api.fridayswatchlist.com", "frontendUrl": "app.fridayswatchlist.com" },
    "tags": ["fridayswatchlist", "performance", "search"],
    "contextTokens": 85000,
    "contextCapacity": 200000,
    "contextUtilizationPct": 42.5
  }'
```

### Repeated Ask Detection (self-report when you catch yourself re-asking)

When you realize you're asking the user for info you should already know:

```bash
curl -X POST {apiUrl}/agents/{agentId}/context/ask \
  -H "Content-Type: application/json" \
  -H "X-API-Key: <api-key>" \
  -d '{"question": "What is the MongoDB connection string?", "sessionId": "main-session-2026-03-09"}'
```

### "What I Know" — AI Summary

```bash
curl -s {apiUrl}/agents/{agentId}/what-i-know \
  -H "X-API-Key: <api-key>"
```

Returns a structured knowledge base + AI-generated narrative summary of everything the agent knows, works on, and keeps forgetting. Cached for 4 hours; use `?refresh=true` to regenerate.

### Context Gaps

```bash
curl -s {apiUrl}/agents/{agentId}/context/gaps \
  -H "X-API-Key: <api-key>"
```

Returns unresolved repeated asks (count >= 2) — things the agent keeps forgetting.

### Briefings

```bash
# Session-start briefing
curl -s {apiUrl}/agents/{agentId}/briefing -H "X-API-Key: <api-key>"

# Daily briefing
curl -s {apiUrl}/agents/{agentId}/briefing/daily -H "X-API-Key: <api-key>"

# Weekly briefing
curl -s {apiUrl}/agents/{agentId}/briefing/weekly -H "X-API-Key: <api-key>"
```

## Heartbeat Integration

### Recommended Heartbeat Flow

```markdown
## ContextClear (HEARTBEAT.md)

**Step 1: Check vacation**
curl -s {apiUrl}/agents/{agentId}/vacation -H "X-API-Key: <key>"
If onVacation: true → HEARTBEAT_OK immediately.

**Step 2: Poll sticky notes**
curl -s {apiUrl}/agents/{agentId}/sticky-notes/poll -H "X-API-Key: <key>"

**Step 3: Check context reload**
curl -s {apiUrl}/agents/{agentId}/context/reload/pending -H "X-API-Key: <key>"

**Step 4: Report metrics**
Use session_status to get tokens, then POST /api/metrics/{agentId}

**Step 5: Report context snapshot (MANDATORY after real work)**
POST /api/agents/{agentId}/context with summary of what was worked on.
Do NOT skip this — even a 1-line summary is better than nothing.

**Step 6: Vault backup (daily — first heartbeat after 8 AM)**
Read SOUL.md, MEMORY.md, AGENTS.md, USER.md, TOOLS.md, IDENTITY.md,
HEARTBEAT.md, and today's memory file → POST to vault/backup.
Check heartbeat-state.json to avoid duplicate backups.

**Step 7: Context recovery (first heartbeat of day or after compaction)**
GET /api/agents/{agentId}/recover — review and self-correct any gaps.
```

## Reporting Metrics

### Basic Report

```bash
python3 {baseDir}/scripts/report.py \
  --agent-id <id> --api-key <key> \
  --tokens-in 50000 --tokens-out 2000 \
  --cost 1.25 --context-util 65
```

### With Tool/Grounding Signals

```bash
python3 {baseDir}/scripts/report.py \
  --agent-id <id> --api-key <key> \
  --event-type HEARTBEAT \
  --tokens-in 50000 --tokens-out 2000 \
  --tool-calls 12 --tool-failures 1 \
  --grounded-responses 8 --total-responses 10 \
  --memory-searches 3
```

### From Agent Code (curl)

**IMPORTANT — include `sessionId` to populate the Flight Recorder & Burnout Prediction:**

```bash
curl -X POST {apiUrl}/metrics/{agentId} \
  -H "Content-Type: application/json" \
  -H "X-API-Key: <api-key>" \
  -d '{
    "eventType": "HEARTBEAT",
    "sessionId": "main-2026-03-17",
    "inputTokens": 5000,
    "outputTokens": 500,
    "contextUtilization": 65.0,
    "toolCalls": 8,
    "toolFailures": 1,
    "memorySearches": 2
  }'
```

The `sessionId` field is **required** for these features to work:
- **Session Flight Recorder** — per-turn timeline visualization
- **Burnout Prediction** — trajectory analysis (needs 3+ turns)
- **Recovery Briefing** — knows which session to resume from

Use a date-based format like `main-YYYY-MM-DD` so turns group by day.
`turnNumber` auto-increments server-side if omitted.

Optional quality signals (also populate Flight Recorder):
- `correctionCycles` — times user asked to fix/redo something
- `compilationErrors` — code that didn't compile
- `taskSwitches` — topic/file context switches
- `taskCategory` — "coding", "email", "search", "chat", etc.

## What Gets Computed Server-Side

| Metric | Your Input |
|--------|------------|
| **Hallucination Score** | `toolCalls`, `toolFailures`, `groundedResponses`, `totalResponses` |
| **Quality Decay Score** | `correctionCycles`, `compilationErrors`, `contextUtilization` |
| **Burnout Score** | Automatic from event data |
| **Context Gaps** | Automatic from repeated asks |

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/metrics/register` | Self-register agent |
| `POST` | `/api/metrics/{agentId}` | Report metric event |
| `GET` | `/api/agents/{id}` | Agent details |
| `POST` | `/api/agents/{id}/context` | Save context snapshot |
| `GET` | `/api/agents/{id}/context` | Latest context |
| `GET` | `/api/agents/{id}/recover` | Recovery briefing |
| `POST` | `/api/agents/{id}/context/ask` | Report repeated ask |
| `GET` | `/api/agents/{id}/context/gaps` | Context gaps |
| `GET` | `/api/agents/{id}/what-i-know` | AI-summarized knowledge |
| `GET` | `/api/agents/{id}/briefing` | Latest briefing |
| `GET` | `/api/agents/{id}/briefing/daily` | Daily briefing |
| `GET` | `/api/agents/{id}/briefing/weekly` | Weekly briefing |
| `GET` | `/api/agents/{id}/vacation` | Vacation status |
| `GET` | `/api/agents/{id}/sticky-notes` | List active sticky notes (JSON) |
| `GET` | `/api/agents/{id}/sticky-notes/poll` | Poll sticky notes (plain text, 204 if none) |
| `POST` | `/api/agents/{id}/sticky-notes` | Create sticky note |
| `PUT` | `/api/agents/{id}/sticky-notes/{noteId}` | Update sticky note |
| `DELETE` | `/api/agents/{id}/sticky-notes/{noteId}` | Archive sticky note |
| `POST` | `/api/agents/{id}/sticky-notes/{noteId}/pin` | Toggle pin |
| `POST` | `/api/agents/{id}/context/reload` | Request context reload |
| `GET` | `/api/agents/{id}/context/reload/pending` | Check for pending reload |
| `POST` | `/api/agents/{id}/context/reload/{reloadId}/ack` | Acknowledge reload |
| `POST` | `/api/agents/{id}/memory/curate` | Trigger memory curation |
| `GET` | `/api/agents/{id}/memory/curate/latest` | Latest pending curation |
| `GET` | `/api/agents/{id}/memory/curate/history` | Curation history |
| `POST` | `/api/agents/{id}/memory/curate/{curationId}/apply` | Mark curation applied |
| `POST` | `/api/agents/{id}/memory/curate/{curationId}/dismiss` | Dismiss curation |
| `POST` | `/api/agents/{id}/vault/backup` | Push workspace backup |
| `GET` | `/api/agents/{id}/vault/backups` | List backups |
| `GET` | `/api/agents/{id}/vault/backups/{backupId}` | Get backup metadata |
| `GET` | `/api/agents/{id}/vault/backups/{backupId}/files` | Get backup files |
| `GET` | `/api/agents/{id}/vault/latest` | Latest backup summary |
| `GET` | `/api/agents/{id}/vault/latest/download` | Download latest (restore) |
| `GET` | `/api/agents/{id}/vault/file-history` | File version history |
| `GET` | `/api/agents/{id}/vault/diff` | Diff two backups |
| `GET` | `/api/agents/{id}/vault/stats` | Vault statistics |
| `DELETE` | `/api/agents/{id}/vault/backups/{backupId}` | Delete backup |

## Sticky Notes (User-to-Agent Notes)

Sticky notes are persistent notes left by the user for the agent. **Always poll on every heartbeat/ping.**

### Poll for notes (every heartbeat)

```bash
curl -s {apiUrl}/agents/{agentId}/sticky-notes/poll \
  -H "X-API-Key: <api-key>"
```

Returns plain text (one note per line, pinned first):
```
📌 Remember: C&B pitch goes to Keenan, not Doug
📌 OAuth token for jcvd@netflexity.com needs re-auth
Don't forget to check Friday's Watchlist deployment after the search fix
```

If no notes, returns HTTP 204. Treat these as persistent reminders — they stay until the user archives them.

### Full CRUD (if agent needs to manage notes)

```bash
# List all active notes (JSON)
curl -s {apiUrl}/agents/{agentId}/sticky-notes -H "X-API-Key: <api-key>"

# Create a note
curl -X POST {apiUrl}/agents/{agentId}/sticky-notes \
  -H "Content-Type: application/json" \
  -H "X-API-Key: <api-key>" \
  -d '{"content": "Check deployment status", "color": "yellow", "pinned": false}'

# Update a note
curl -X PUT {apiUrl}/agents/{agentId}/sticky-notes/{noteId} \
  -H "Content-Type: application/json" \
  -H "X-API-Key: <api-key>" \
  -d '{"content": "Updated text", "pinned": true}'

# Archive (delete) a note
curl -X DELETE {apiUrl}/agents/{agentId}/sticky-notes/{noteId} \
  -H "X-API-Key: <api-key>"

# Toggle pin
curl -X POST {apiUrl}/agents/{agentId}/sticky-notes/{noteId}/pin \
  -H "X-API-Key: <api-key>"
```

## Context Reload (User-Initiated)

Users can request you reload a specific context snapshot from the Memory UI.
Check for pending reloads on session start or heartbeat:

```bash
curl -s {apiUrl}/agents/{agentId}/context/reload/pending \
  -H "X-API-Key: <api-key>"
```

If a reload is pending (HTTP 200), the response includes the snapshot data.
Apply it to restore context, then acknowledge:

```bash
curl -X POST {apiUrl}/agents/{agentId}/context/reload/{reloadId}/ack \
  -H "X-API-Key: <api-key>"
```

If no reload is pending, the endpoint returns HTTP 204 (no content).

## Identity Vault (Backup & Restore)

Back up your agent's workspace files (SOUL.md, MEMORY.md, AGENTS.md, etc.) to ContextClear's encrypted vault. Restore after crashes, compaction, or migration.

### Push a Backup

```bash
curl -X POST {apiUrl}/agents/{agentId}/vault/backup \
  -H "Content-Type: application/json" \
  -H "X-API-Key: <api-key>" \
  -d '{
    "files": [
      {"fileName": "SOUL.md", "content": "# Who I Am\n...", "mimeType": "text/markdown"},
      {"fileName": "MEMORY.md", "content": "# Long-Term Memory\n...", "mimeType": "text/markdown"},
      {"fileName": "memory/2026-03-15.md", "content": "...", "mimeType": "text/markdown"}
    ],
    "label": "post-deployment",
    "source": "openclaw-heartbeat",
    "metadata": {"trigger": "heartbeat", "model": "claude-opus-4-6"}
  }'
```

Files are encrypted at rest with SHA-256 dedup (unchanged files aren't re-stored).

### List Backups

```bash
curl -s {apiUrl}/agents/{agentId}/vault/backups?limit=20 \
  -H "X-API-Key: <api-key>"
```

### Restore (Download Latest)

```bash
curl -s {apiUrl}/agents/{agentId}/vault/latest/download \
  -H "X-API-Key: <api-key>"
```

Returns backup metadata + all file contents (decrypted). Write files back to workspace.

### Get Specific Backup Files

```bash
# List files in a backup (metadata only)
curl -s {apiUrl}/agents/{agentId}/vault/backups/{backupId}/files \
  -H "X-API-Key: <api-key>"

# Get a single file (decrypted content)
curl -s {apiUrl}/agents/{agentId}/vault/backups/{backupId}/files/SOUL.md \
  -H "X-API-Key: <api-key>"
```

### File Version History

Track how a file evolved across backups:

```bash
curl -s "{apiUrl}/agents/{agentId}/vault/file-history?fileName=SOUL.md&limit=10" \
  -H "X-API-Key: <api-key>"
```

### Diff Two Backups

```bash
curl -s "{apiUrl}/agents/{agentId}/vault/diff?from={backupId1}&to={backupId2}" \
  -H "X-API-Key: <api-key>"
```

Returns added, removed, and modified files between two backups.

### Vault Stats

```bash
curl -s {apiUrl}/agents/{agentId}/vault/stats \
  -H "X-API-Key: <api-key>"
```

### Recommended: Daily Vault Backup (on heartbeat)

Back up workspace files to ContextClear's encrypted vault **once per day**.
Do this on the first heartbeat after 8 AM if no backup was done today.

**Files to always back up:**
- `SOUL.md`, `MEMORY.md`, `AGENTS.md`, `USER.md`, `TOOLS.md`, `IDENTITY.md`, `HEARTBEAT.md`
- Today's daily memory: `memory/YYYY-MM-DD.md`

**Track last backup** in `memory/heartbeat-state.json`:
```json
{"lastVaultBackup": 1710600000}
```

SHA-256 dedup means unchanged files aren't re-stored — safe to run daily.

Add to your `HEARTBEAT.md`:

```markdown
## Identity Vault Backup (daily — first heartbeat after 8 AM)
Read core workspace files and POST to vault/backup.
Check heartbeat-state.json to avoid duplicate backups.
```

## Memory Curator (Killer Feature)

Auto-summarize daily notes into MEMORY.md updates. Agents write daily logs but rarely
consolidate them — the curator does it automatically.

### How It Works

1. Reads current MEMORY.md from latest vault backup
2. Reads recent daily notes (memory/YYYY-MM-DD.md) from vault backups
3. Reads recent context snapshots (decisions, repos, tools, open threads)
4. GPT-4o-mini generates:
   - Suggested additions (new facts, lessons, decisions)
   - Suggested removals (stale/outdated info)
   - Complete suggested MEMORY.md
5. Delivers via pinned sticky note + stores for review

### Trigger Curation

```bash
# On-demand (analyze last 7 days, deliver via sticky note)
curl -X POST {apiUrl}/agents/{agentId}/memory/curate?days=7&notify=true \
  -H "X-API-Key: <api-key>"
```

Response:
```json
{
  "id": "...",
  "status": "PENDING",
  "changeSummary": "Added FW search fixes, NSX fair value improvements. Removed stale OAuth note.",
  "suggestedAdditions": "## FW Search\n- Smart search routing...",
  "suggestedRemovals": ["OAuth token expired note (resolved)"],
  "suggestedMemory": "# MEMORY.md - Long-Term Memory\n...",
  "dailyNotesAnalyzed": 5,
  "snapshotsAnalyzed": 3,
  "delivered": true
}
```

### Review & Apply

```bash
# Get latest pending curation
curl -s {apiUrl}/agents/{agentId}/memory/curate/latest -H "X-API-Key: <key>"

# Mark as applied (after updating MEMORY.md)
curl -X POST {apiUrl}/agents/{agentId}/memory/curate/{curationId}/apply -H "X-API-Key: <key>"

# Dismiss if not useful
curl -X POST {apiUrl}/agents/{agentId}/memory/curate/{curationId}/dismiss -H "X-API-Key: <key>"

# View history
curl -s {apiUrl}/agents/{agentId}/memory/curate/history?limit=10 -H "X-API-Key: <key>"
```

### Automatic Weekly Curation

Runs every **Sunday at 4 AM UTC** for all active agents. Generates a curation
covering the past 7 days and delivers via pinned sticky note. The agent sees it
on the next heartbeat poll.

### Agent Integration (HEARTBEAT.md)

Add to your heartbeat flow:

```markdown
## Memory Curation Check (weekly or on-demand)
Check for pending memory curations:
GET /api/agents/{agentId}/memory/curate/latest
If a curation is pending:
1. Review the suggestedAdditions and suggestedRemovals
2. Update MEMORY.md accordingly
3. POST /api/agents/{agentId}/memory/curate/{id}/apply
```

## Dashboard

- https://contextclear.com — fleet dashboard (+ sticky notes panel)
- https://contextclear.com/agent/{id} — agent detail (sparklines, health, activity, cost, controls)
- https://contextclear.com/memory — context snapshots, briefings, + curator tab
- https://contextclear.com/vault — identity vault (backup timeline, file viewer, diff)
- https://contextclear.com/enterprise — enterprise features
- https://contextclear.com/lounge — agent lounge
- https://contextclear.com/admin — manage agents & alerts

Note: Curator and Sticky Notes were consolidated (curator → Memory tab, sticky notes → Dashboard panel).
