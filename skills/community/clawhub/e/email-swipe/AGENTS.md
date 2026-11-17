# Agent instructions (Email Swipe)

Read this on activation. Humans should start with [README.md](README.md) or [references/QUICKSTART.md](references/QUICKSTART.md).

## First call (MCP)

**`get_skill_context`** — returns canonical activation guidance (UI, demo, git status, doc paths, **agent spine**, **environment.json**). Call this before assess if MCP is connected.

No MCP? Run `python scripts/check-ready.py --json` or `python scripts/session-intake.py assess` — both include `agentContext`.

## How the agent remembers (skill functionality)

**Never memorize skill how-tos.** Re-hydrate every session with `get_skill_context` (UI open path, activation order, tool routing).

| Kind of knowledge | Where it lives |
|-------------------|----------------|
| How to open UI / activate / tools | Skill (`get_skill_context`, `AGENTS.md`) |
| Verified mail access on this machine | `~/.config/email-swipe/environment.json` (`emailAccessByAccount`) via `record_email_access` — **per accountId** when unified inbox |
| Live Desktop URL | `runtime.json` (written by `serve-ui.py`) |
| Advanced settings behavior | Agent spine (`get_agent_spine` / `update_settings`) |
| Host memory (Cursor / CLAUDE.md) | **Pointer only** — skill path + call `get_skill_context` |

After a successful 5–10 message fetch, call **`record_email_access`** with `accountId` when unified inbox is enabled (omit for single inbox).

## Agent spine (settings source of truth)

**You own advanced settings in memory.** The skill defines how they sync. Read [references/agent-spine.md](references/agent-spine.md) on activation.

| Loop | When | Action |
|------|------|--------|
| **Push → UI** | Before `serve-ui.py` or user opens Advanced settings | `update_settings` with your spine |
| **Hydrate ← UI** | After swipe session, export, or user saved settings | `get_agent_spine` → merge into memory |
| **Act** | Recommending mail actions, digests, autonomy | Read `activeSections` only; ignore dormant |

**Tool routing:** `get_agent_spine` (read) · `update_settings` (write) · `set_mail_accounts` (inbox registry only)

Most advanced settings are **dormant** by default (unified inbox, rhythm, remote access, advanced sorting, etc.). Do not surface or re-ask dormant fields unless the user activates them.

`~/.config/email-swipe/settings.json` is a **disk mirror for the UI**, not your memory. `get_settings` is the raw mirror; `get_agent_spine` adds active/dormant sections.

## Value proposition (say this early)

> "I'll learn how you sort email — by swiping a sample or reading your existing folders — and produce rules I can recommend on new mail. I won't auto-delete or hide your inbox unless you explicitly approve."

The main job is **training the agent to sort the user's inbox correctly**. The UI is optional and should only be used when it fits the user's preferred training path.

## UI entry point (read this first)

There is **one** UI: `assets/ui/index.html`, served at the **Desktop URL** printed by `serve-ui.py` (dynamic port — do not assume `8765`).

**Settings:** Header opens **Advanced settings** (8 tabs). **Agent spine** is source of truth — [references/agent-spine.md](references/agent-spine.md). Push with `update_settings` before UI; hydrate with `get_agent_spine` after UI feedback.

**Phone:** User can **Add to Home Screen** (PWA) to the Mobile URL on same Wi‑Fi — server must stay running on their machine. See spec § Mobile & Access tab.

| Do | Don't |
|----|-------|
| Open the Desktop URL from `serve-ui.py` | Look for `demo.html` or `demo-app.js` — they are not part of this skill |
| Use `session-intake.py demo` for sample mail | Switch servers or UIs because of git status noise |
| Read `runtime.json` for the active session URL | Hardcode `localhost:8765` |

- **"Demo"** means sample mail (`demo-emails.json`), not a different page. The same UI loads `emails.json` first, then falls back to demo mail automatically.
- **`git status` noise is normal.** Runtime files like `assets/ui/emails.json`, `settings.json`, and `session-metadata.json` are gitignored and appear after a session. They are not uncommitted skill code.

## On activation — required checklist (do not skip or reorder)

Follow these phases in order. Do not jump to `serve-ui.py` or `inject-emails.py` early.

1. **`get_skill_context`** (MCP) or read this file + `SKILL.md`
2. **`check_email_access`** (MCP) or `python scripts/detect-environment.py` — then **ask the user** if they have mail access via MCP even when detect is empty
3. **`session_intake_assess`** → discovery conversation (include email provider + real vs demo)
4. **`session_intake_discover`** → **`session_intake_recommend`** → user picks → **`session_intake_confirm`**
5. **Execute path runbook** in `references/paths/` — resolve email setup first if user wants real mail ([email-access-gate.md](references/email-access-gate.md))
6. After training → [post-training-flow.md](references/post-training-flow.md) — present `assistant-brief.md`

**Evaluator demo only:** `session-intake.py demo` → `serve-ui.py` (skips steps 3–5 intake, uses sample mail).

**Hard stops:**
- No `inject-emails.py` / `serve-ui.py` before `confirm`
- No real-mail inject without verified mail access (or user-built batch)
- No subject-line-only fetches when full HTML/body is available — prefer full sanitized email content
- No skipping post-training brief

## Four paths

| Path | When | UI? |
|------|------|-----|
| `bootstrap` | First training | Yes |
| `calibrate` | Has rules — swipe edge cases | Yes |
| `refine` | Prior training, close gaps | Yes |
| `import-sorting` | Folders already sorted | **No** — preview first |

## MCP tools

**Intake:** `get_skill_context`, `check_email_access`, `record_email_access`, `session_intake_assess`, `session_intake_discover`, `session_intake_recommend`, `session_intake_confirm`, `get_intake_state`, `session_intake_demo`

**Training:** `compile_training`, `get_policy_brief`, `get_policy_graph`, `get_calibration`, `get_training_pack`, `get_watch_rules`, `learn_from_folders`, `get_agent_spine`, `get_settings`, `update_settings`, `set_mail_accounts`, `get_session_status`

**Settings spine:** See [references/agent-spine.md](references/agent-spine.md). Prefer `get_agent_spine` / `update_settings`. `list_mail_accounts` is optional when spine is hydrated.

**Setup MCP** (Cursor):

```json
{
  "mcpServers": {
    "email-swipe": {
      "command": "python3",
      "args": ["/absolute/path/to/email-swipe/scripts/watch-preferences.py"]
    }
  }
}
```

## Artifacts (`~/.config/email-swipe/`)

| File | Use |
|------|-----|
| `assistant-brief.md` | **Present to user** after training |
| `policy-graph.json` | Structured policies (recommend-only) |
| `platform-rules.json` | Label/folder build-out suggestions |
| `training-pack.json` | Slim runtime slice |
| `settings.json` | Disk mirror for UI (agent truth: spine — see `references/agent-spine.md`) |
| `environment.json` | Verified mail access for this machine (`record_email_access`) |
| `preferences.json` | Latest swipe export (authoritative input to compile) |

### State ownership

| Store | Authoritative for agent? | Role |
|-------|-------------------------|------|
| **Agent spine** (in-memory + skill) | **Yes** | Your source of truth for behavior |
| `~/.config/email-swipe/environment.json` | Machine facts | Per-account verified mail (`emailAccessByAccount`) |
| `~/.config/email-swipe/settings.json` | Mirror | UI + disk sync via MCP |
| `~/.config/email-swipe/preferences.json` | Swipes input | Compile input; may embed settings snapshot |
| Compiled artifacts (`policy-graph`, `assistant-brief`, …) | Trained rules | Read after compile for mail actions |
| Browser `localStorage` / IndexedDB | **No** | UI cache only |

| Store | Who writes disk mirror | Who reads |
|-------|------------------------|-----------|
| `settings.json` | Agent `update_settings`, UI `POST /api/settings`, compile from preferences | UI, `get_agent_spine` |
| `preferences.json` | UI `POST /api/preferences` | `compile_training.py` |

Debug: `python scripts/print_state.py --json` · Spine: `get_agent_spine` (MCP)

## Hard rules

- Default autonomy: **recommend only** — no auto-label, archive, or send without approval.
- `import-sorting`: always `learn_from_folders` with `preview: true` first; folders may hold stale mail.
- When fetching training mail, prefer full sanitized HTML/body content; subject+snippet alone is a fallback, not the target.
- **Always guess** on every injected email (`predictedAction` + `predictionConfidence`) — even bootstrap, even low confidence. Blank guesses hide the score.
- Advanced folder routes persist in `settings.json` — don't re-ask each session; build out per `platform-rules.folderRoutes`.
- Use brief + training-pack at runtime — not full swipe history in prompts.

## CLI cheat sheet

```bash
python scripts/check-ready.py --json   # optional preflight + agentContext
python scripts/session-intake.py demo          # evaluator shortcut
python scripts/fetch_folder_snapshot.py -o folders.json
python scripts/learn_from_folders.py folders.json --preview
python scripts/inject-emails.py batch.json
python scripts/serve-ui.py
python scripts/compile_training.py             # manual recompile
python scripts/print_state.py --json           # where truth lives
```

Full skill spec: [SKILL.md](SKILL.md)
