gh-triage

Proactive GitHub issues/PR triage and lightweight fixes.

What it does

- Periodically (cron) scans configured repositories for new issues and PRs
- Labels, comments, and assigns based on simple rules (area labels, `needs-info`, `triage-needed`)
- Can apply small fixes automatically (typo fixes, formatting, missing issue templates) when enabled
- Emits a report and creates follow-up tasks for maintainers

Files

- index.js — main skill entrypoint (node)
- package.json — dependencies and scripts
- SKILL.md — this file
- config.example.json — configuration template for repos, tokens, rules

Security

- Requires a GitHub token with repo access. Keep secrets out of the repo; provide via environment variables or the host secret store.

Usage

- Install by placing the folder in workspace/skills and follow project conventions
- Configure repos and rules in config.json (copy config.example.json)
- Run with: node index.js or integrate with OpenClaw skill loader

License: MIT
