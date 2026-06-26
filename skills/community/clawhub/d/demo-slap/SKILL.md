---
name: demo-slap
description: Generate CS2 highlights and fragmovies from demos using the Demo-Slap API, with optional Leetify integration and Demo-Slap match history fallback to select recent matches. Use when a user asks to record a highlight, render a clip, make a fragmovie, clip a round, or turn a CS2 demo into MP4 video.
metadata:
  {
    "openclaw": {
      "requires": {
        "env": ["DEMOSLAP_API_KEY"],
        "bins": ["python3", "openclaw"]
      }
    }
  }
---

# Demo-Slap Highlight Skill

Generate MP4 highlights and fragmovies from CS2 demos.

This skill is designed for OpenClaw environments where background jobs, local helper scripts, and chat-aware delivery are available. It uses Python 3 scripts and the `requests` package for HTTP API access.

Expected runtime inputs:
- Required: `DEMOSLAP_API_KEY`
- Optional: `LEETIFY_API_KEY`
- Optional deployment helper: `DEMO_SLAP_WATCHDOG_JOB_ID`

## Scripts

Run bundled scripts relative to the skill root, usually from `scripts/`.

### Demo-Slap
| Script | Purpose |
|--------|---------|
| `demo_slap_matches.py` | List recent matches from Demo-Slap `/public-api/matches` |
| `demo_slap_resolve.py` | Try to resolve replay/demo URL from Demo-Slap match history by index; fail clearly if the API exposes only `jobId` |
| `demo_slap_match_pick.py` | Pick a Demo-Slap match by index and return structured match info including `jobId` |
| `demo_slap_analyze.py` | Submit a demo for analysis, poll until done, output highlights JSON |
| `demo_slap_render.py` | Render one or more highlights, poll until done, output clip URL |
| `demo_slap_common.py` | Shared utilities (config, API calls, state) |

### Leetify
| Script | Purpose |
|--------|---------|
| `leetify/leetify_matches.py` | List recent matches |
| `leetify/leetify_resolve.py` | Resolve replay URL by username + match index |
| `leetify/leetify_save_id.py` | Save username -> Steam64 ID mapping |
| `leetify/leetify_common.py` | Shared Leetify utilities |

### Match source selection
- Prefer Leetify for recent match discovery when `LEETIFY_API_KEY` is available.
- If `LEETIFY_API_KEY` is not configured but `DEMOSLAP_API_KEY` is available, use Demo-Slap match history from `/public-api/matches`.
- Swagger: `https://api-doc.demo-slap.net/`
- Treat Demo-Slap match history as the fallback discovery path for listing matches and selecting an existing analyzed match or replay context before analyze/render.

## Runtime files

Use these files as optional local runtime state during execution:
- `data/state.json`
- `data/highlights.json`
- `data/history.log`
- `data/steam_ids.json`
- `data/config.json`

These files are runtime helpers for local operation and are not required to understand or inspect the skill package itself.

`state.json` tracks the current operation:
```json
{
  "status": "idle|analyzing|rendering|done|error",
  "job_id": "...",
  "render_job_id": "...",
  "chat_id": "telegram:182314856",
  "clip_urls": {"highlight_id": "https://..."},
  "progress": "polling 3/30",
  "last_completed_op": "analyze|render",
  "notification": {
    "sent": false,
    "sent_at": null,
    "last_attempt_at": null,
    "error": null
  },
  "updated_at": "ISO timestamp"
}
```

## Workflow

### 1. Find the match
Preferred path when `LEETIFY_API_KEY` is available:
```bash
python3 scripts/leetify/leetify_matches.py <USERNAME> [--limit 10]
```

Fallback path when `LEETIFY_API_KEY` is missing but `DEMOSLAP_API_KEY` is available:
```bash
python3 scripts/demo_slap_matches.py [<USERNAME>] [--limit 10]
```
- uses Demo-Slap `/public-api/matches`
- use the Demo-Slap swagger docs at `https://api-doc.demo-slap.net/` if schema details are needed
- if `<USERNAME>` is provided and mapped, filter matches to that player's Steam ID when possible
- after the user picks a match, run:
```bash
python3 scripts/demo_slap_match_pick.py [<USERNAME>] --match-index <N>
```
- treat the returned `jobId` as the primary handle for downstream Demo-Slap operations

### 2. Resolve replay URL
Preferred path when using Leetify:
```bash
python3 scripts/leetify/leetify_resolve.py <USERNAME> --match-index <N>
```

When using Demo-Slap fallback:
```bash
python3 scripts/demo_slap_match_pick.py [<USERNAME>] --match-index <N>
```
- use the returned `jobId` as the selected match identifier
- if `demoUrl` is present, you may still use analyze-by-URL
- if `demoUrl` is absent, skip URL resolution and continue by API endpoints that accept the existing analyze `jobId`
- use `GET /public-api/analyze/{jobId}/status` and `GET /public-api/analyze/{jobId}/data` to inspect existing highlights
- if the user wants clips and highlights already exist, render directly from that `jobId`

### 3. Analyze in background
```bash
python3 -u scripts/demo_slap_analyze.py --url '<REPLAY_URL>' --username <USERNAME> --chat-id <CHAT_ID>
```

Run with `exec(background: true)` and keep the returned process/session id.

Optional deployment-specific watchdog pattern for OpenClaw environments:
- Use a watchdog only when background analyze/render work benefits from periodic delivery checks.
- Reuse an existing deployment watchdog when available instead of assuming a new persistent scheduler entry is always needed.
- If a deployment chooses to create or enable a watchdog through the built-in `cron` tool, keep it scoped to the active run and disable it again after terminal delivery.
- A 2 minute interval is a reasonable default.
- Use `scripts/demo_slap_watchdog.sh status|tail|job` only as a local helper for inspecting runtime state, logs, or deployment-specific job references.
- Treat `data/state.json` and `data/highlights.json` as the source of truth during runtime.

Agent workflow:
1. Choose the match source:
   - Leetify if `LEETIFY_API_KEY` exists
   - Demo-Slap `/public-api/matches` if `LEETIFY_API_KEY` is missing and `DEMOSLAP_API_KEY` exists
2. If using Leetify, resolve the replay URL and run analyze
3. If using Demo-Slap fallback, pick a match and inspect the returned `jobId`
4. If the selected Demo-Slap match already has analyze data, continue by `jobId` instead of forcing analyze-by-URL
5. Use or enable a deployment watchdog only when long-running analyze/render work benefits from it
6. Launch analyze or render and save the returned process/session id when applicable
7. Let the watchdog deliver the result when a deployment uses one
8. Disable the watchdog again after terminal delivery

### 4. Render in background
```bash
# Single highlight
python3 -u scripts/demo_slap_render.py <JOB_ID> <HIGHLIGHT_ID> --chat-id <CHAT_ID>

# Fragmovie
python3 -u scripts/demo_slap_render.py <JOB_ID> <ID1> <ID2> ... --fragmovie --chat-id <CHAT_ID>
```

Run with `exec(background: true)` and keep the returned process/session id.

Optional deployment-specific watchdog pattern for OpenClaw environments:
- Use a watchdog only when background analyze/render work benefits from periodic delivery checks.
- Reuse an existing deployment watchdog when available instead of assuming a new persistent scheduler entry is always needed.
- If a deployment chooses to create or enable a watchdog through the built-in `cron` tool, keep it scoped to the active run and disable it again after terminal delivery.
- A 2 minute interval is a reasonable default.
- Use `scripts/demo_slap_watchdog.sh status|tail|job` only as a local helper for inspecting runtime state, logs, or deployment-specific job references.
- Treat `data/state.json` and `data/highlights.json` as the source of truth during runtime.

Agent workflow:
1. Enable or reuse a deployment watchdog only when needed for the active run
2. Launch render and save the returned process/session id
3. Poll process output for the `Estimated finish:` line and tell the user the ETA if present
4. Let the watchdog deliver the result when one is in use
5. Disable the watchdog again after terminal delivery

**Critical:** set `<CHAT_ID>` from inbound metadata of the originating request. Treat hardcoded chat identifiers as local examples only, not as a reusable default.

### 5. Check status
Read `data/state.json`.

## Setup

### Map username to Steam ID
```bash
python3 scripts/leetify/leetify_save_id.py <USERNAME> <STEAM_64_ID>
```

### Configure API keys
Prefer environment variables:
- `DEMOSLAP_API_KEY` - required
- `LEETIFY_API_KEY` - optional, only for Leetify-backed match discovery
- `DEMO_SLAP_WATCHDOG_JOB_ID` - optional deployment-specific helper for watchdog inspection scripts

Source selection rules:
- If `LEETIFY_API_KEY` exists, use Leetify for match discovery.
- If `LEETIFY_API_KEY` is absent but `DEMOSLAP_API_KEY` exists, use Demo-Slap `/public-api/matches` for match discovery.
- `DEMOSLAP_API_KEY` is always required for analyze/render.

Optional local fallback for controlled self-hosted setups: put them in `data/config.json`.

## Support

For access and support, please join our Discord community: https://discord.gg/8nfh26W9wQ
