# privacy-notes.md — CodeSmith Privacy Commitments

> Explicit transparency about what this package touches. Read this before applying anything.

---

## What This Package Reads

| File | When | Why |
|------|------|-----|
| `~/.openclaw/workspace/AGENTS.md` | Setup — for compatibility analysis | Understand your current config before proposing changes |
| `~/.openclaw/workspace/SOUL.md` | Setup — for personality context | Understand your agent's identity to avoid tone conflicts |
| `~/.openclaw/workspace/MEMORY.md` | Never used as package content | Not read by the package — only by the agent doing self-assessment |
| `memory/session-continuity.md` | On every session startup | Sprint state — read to orient, not to analyze |
| `memory/YYYY-MM-DD.md` | Only when explicitly requested | Not read by default — only if you ask the agent to summarize a day |
| `~/.openclaw/cron/jobs.json` | Setup — for schedule analysis | Check for cron conflicts before suggesting new schedules |
| `~/.openclaw/skills/` (listing only) | Setup | Identify what skills you have installed |

---

## What This Package Does NOT Read

These files are explicitly excluded even if they exist:

| File | Why excluded |
|------|-------------|
| `~/.openclaw/openclaw.json` | Contains API keys and credentials — never read |
| `memory/technical-reference.md` | May contain account credentials, API keys, internal URLs |
| Any `.env` file | Credentials |
| Any file containing `token`, `key`, `secret`, `password` in the name | Credentials by convention |
| Your daily memory logs | Personal operational data, not needed for package application |
| Browser profiles, session cookies | Never relevant to package setup |
| Personal files outside `~/.openclaw/workspace/` | Out of scope |

The package works with your agent configuration, not your personal data.

---

## What This Package Writes

| File | When | What |
|------|------|------|
| `~/.openclaw/workspace/AGENTS.md` | On your explicit approval only | Merged configuration additions — never overwrites without confirmation |
| `~/.openclaw/cron/jobs.json` | On your explicit approval, one job at a time | New cron job entries per the adoption guide |
| `~/.openclaw/workspace/memory/lessons-learned.md` | If you apply setup guidance | Adds lesson entries — appends only, never overwrites |
| A backup of your AGENTS.md | Before any changes | `AGENTS.md.bak.[timestamp]` — so you can always restore |

**Nothing is written without your explicit approval.** The agent proposes changes; you authorize each one.

---

## Network Activity

| Call | When | Why | What's sent |
|------|------|-----|------------|
| GitHub API (read) | Setup analysis | Fetch this package's files | Repo name and file paths — no personal data |
| GitHub API (write) | Never from your machine | Package is read-only for subscribers | N/A |
| OpenClaw LLM inference | During session | All analysis runs on your local agent | Your query + package contents |
| Health check endpoints | If you install health-check cron | Verifies your APIs are responding | HTTP GET to your configured endpoints |

**No telemetry.** No analytics. No callbacks to ClawMentor servers during normal operation.

The ClawMentor platform fetches packages from GitHub (reading this repo). That fetch is one-directional — it reads from this repo and has no access to your workspace.

---

## Data Sensitivity Levels

| Data Type | Sensitivity | This Package |
|-----------|-------------|--------------|
| API keys, tokens, credentials | 🔴 HIGH | Never read, never written |
| Personal names and contact info | 🔴 HIGH | Never included in package files |
| Your workspace memory logs | 🟡 MEDIUM | Read only for setup analysis — never exfiltrated |
| Your AGENTS.md configuration | 🟡 MEDIUM | Read for compatibility — content stays local |
| Cron schedules | 🟢 LOW | Read and proposed additions — no sensitive content |
| Package configuration files | 🟢 LOW | What this package contains — public content |

---

## MEMORY.md Security Note

`MEMORY.md` is auto-injected into every agent session by OpenClaw. It may contain personal context, project names, and operational details.

This package **does not read MEMORY.md directly**. When the agent applies this package, it uses MEMORY.md as background context (it's already in the session) — but that content is never sent anywhere, never analyzed separately, and never written to package files.

The principle: your long-term memory is your private context, not input for package analysis.

---

## Verification

After applying this package, you can verify what was changed:

```bash
# Check what files were modified
git diff HEAD~1 --name-only ~/.openclaw/workspace/

# Review AGENTS.md changes specifically
diff ~/.openclaw/workspace/AGENTS.md ~/.openclaw/workspace/AGENTS.md.bak.*

# Check if any new credentials appeared (should return nothing)
grep -rE "(sk-|token|bearer|password|secret)" ~/.openclaw/workspace/ --include="*.md"
```

If any of those grep results return content that wasn't there before, review it manually before proceeding.
