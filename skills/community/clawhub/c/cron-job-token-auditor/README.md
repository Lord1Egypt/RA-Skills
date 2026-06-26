# Cron Job Auditor (OpenClaw skill)

Advisory skill for **auditing OpenClaw Gateway cron jobs** and flagging opportunities to move recurring work to **OS-scheduled scripts** (e.g. systemd timers) that use **`openclaw message send`** without an LLM on each run—reducing token spend.

## What it is

- **Read-only guidance**: instructs the agent to classify jobs, apply heuristics, and produce a structured report.
- **Not included**: automatic edits to `jobs.json`, creation of systemd units, or deletion of crons. The user implements changes manually.

## Install (OpenClaw)

Copy this folder into your workspace skills directory (highest precedence for name conflicts):

```text
<workspace>/skills/cron-job-auditor/
```

Restart the Gateway or start a **new session** so skills reload (see OpenClaw docs for skills watcher).

Or use ClawHub when published:

```bash
npx clawhub@latest install cron-job-auditor
```

(Exact command may match your ClawHub CLI version.)

## Files

| File | Role |
|------|------|
| `SKILL.md` | Agent instructions + report template |
| `REFERENCE.md` | Glossary, payload hints, verification checklist |
| `LICENSE` | MIT-0 |

## Docs

- OpenClaw cron: [docs.openclaw.ai](https://docs.openclaw.ai) — search for **Cron jobs**
- CLI: `openclaw cron --help` (if available in your version)

## License

MIT-0 — see `LICENSE`.
