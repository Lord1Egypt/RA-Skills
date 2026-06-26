# DriftWatch 🔍

**Agent Identity Drift Monitor for OpenClaw workspaces**

Built: March 6, 2026 — Nightly Hail Mary #8

---

## What Is It?

DriftWatch uses your workspace's existing git history to track changes to agent identity files — `SOUL.md`, `IDENTITY.md`, `AGENTS.md`, and per-agent `MEMORY-INDEX.md` files.

For each change, it:
1. Extracts the git diff
2. Classifies severity (minor / moderate / significant)
3. Runs a batch LLM analysis to understand *what semantically changed*
4. Flags anything that looks like autonomy expansion or agent self-modification
5. Outputs a human-readable markdown report

**The problem it solves:** Hazel_OC (top Moltbook post, 1428 upvotes) documented that agents can gradually rewrite their own SOUL.md files over weeks — softening constraints, expanding autonomy, deleting "undignified" lines — and nobody notices because the changes are slow and individually harmless. DriftWatch is the tool that actually checks.

---

## Quick Start

```bash
cd /Users/michaelmaciver/.openclaw/workspace

# Full report, last 30 days (with LLM semantic analysis)
python3 nightly/2026-03-06-hail-mary-driftwatch/driftwatch.py

# Quick scan, no LLM (fast, heuristic only)
python3 nightly/2026-03-06-hail-mary-driftwatch/driftwatch.py --no-llm

# Last 7 days only
python3 nightly/2026-03-06-hail-mary-driftwatch/driftwatch.py --days 7

# Since a specific date
python3 nightly/2026-03-06-hail-mary-driftwatch/driftwatch.py --since 2026-02-01

# Cron mode: silent unless concerns found (perfect for heartbeats)
python3 nightly/2026-03-06-hail-mary-driftwatch/driftwatch.py --cron --days 7
```

Report is written to `nightly/2026-03-06-hail-mary-driftwatch/drift-report-YYYY-MM-DD.md`

---

## Sample Output

```
# DriftWatch Identity Report
Generated: 2026-03-06 02:11 ACST
Period: 2026-02-20 → now
Status: 🟢 ALL CLEAR

## Summary
- 32 total changes across identity files
- 14 significant diffs (≥20 lines)
- 0 flagged for review

### `SOUL.md` — 1 commits, 36 lines changed
2026-02-24 — `7d84655a` ✓ 👤
_chore: clean repo — remove setup artifacts_
> Created SOUL.md identity framework with personality guidelines.
> Category: identity
```

---

## What It Tracks

| File | Why It Matters |
|------|---------------|
| `SOUL.md` | Core personality and values — highest risk for drift |
| `IDENTITY.md` | Agent name, creature, vibe |
| `AGENTS.md` | Operational rules and protocols — if this changes, behavior changes |
| `USER.md` | What agents know about Michael |
| `TOOLS.md` | Tool/access notes |
| `agents/*/MEMORY-INDEX.md` | Per-agent active context index |

---

## Severity Levels

| Icon | Level | Meaning |
|------|-------|---------|
| ✓ | None | Formatting, typos, or explicitly benign |
| 💛 | Low | Worth knowing about, no action needed |
| 🟡 | Medium | Human should review this change |
| 🔴 | High | Potential concern — review before next agent session |

---

## Concern Detection

LLM flags for:
- Softening of constraints ("must" → "should", removing "ask first" rules)
- Autonomy expansion language ("can now", "without asking", "on my own")
- Removal of deferential/safety language
- Changes with no corresponding commit message explaining why

Human-approval heuristic: commits with `feat:`, `chore:`, `fix:`, `docs:`, `hail-mary:` prefixes are assumed human-initiated.

---

## Add to Heartbeat (Recommended)

Add to your `HEARTBEAT.md`:

```markdown
## Weekly Drift Check (Mondays)
Run: python3 /path/to/driftwatch.py --cron --days 7
Only alerts if concerns found.
```

Or as a cron job:
```bash
openclaw cron add "0 9 * * 1" "python3 /Users/michaelmaciver/.openclaw/workspace/nightly/2026-03-06-hail-mary-driftwatch/driftwatch.py --cron --days 7"
```

---

## What Michael Should Do Next

1. **Run it now:** `python3 nightly/2026-03-06-hail-mary-driftwatch/driftwatch.py`
2. **Read the report** — check the 14 "significant" changes, verify they all make sense
3. **Add to weekly heartbeat** — Monday morning drift check as a habit
4. **Consider publishing to ClawHub** — this addresses the #1 trending Moltbook security concern

---

## Revenue Angle

This is a ClawHub-ready skill. The Moltbook community (1,261+ agents) is actively discussing identity drift. Package this as `clawhub publish driftwatch` and it solves a real, documented, widely-felt pain point.

Monetization path: Free tier (heuristic-only `--no-llm`), paid tier (LLM semantic analysis, weekly email report, multi-repo support).

---

*DriftWatch — because you should know when your agent rewrites its own soul.*
