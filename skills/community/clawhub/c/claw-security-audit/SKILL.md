---
name: claw-security-audit
description: Read-only security audit of an OpenClaw install - hardcoded secrets, risky gateway settings, file permissions, exposed ports, keys, risky skills. JSON + HTML report, secret values never shown.
---

# OpenClaw Security Audit

Use when the user asks to audit, harden, or security-check their OpenClaw setup.

1. Run `python audit.py` (or `python3 audit.py`) from this skill folder. Needs Python 3.8+ only; no packages.
   - Console only, no report files: `python audit.py --no-report`
   - One check: `python audit.py --check SEC001`; list checks: `python audit.py --list-checks`
   - Scan a git repo for leaked keys: `python audit.py --check SEC003 --git-repo <path>`
   - Custom paths: copy `config.example.json`, edit, run `python audit.py -c config.json`
2. Read the console summary. Exit code 0 = clean, 1 = failures, 2 = warnings only, 64 = bad arguments.
3. Explain each FAIL/WARNING with its remediation line. Never print or paste secret values from the user's files; the report already hides them.
4. Do not change any file automatically. Propose fixes and apply them only after the user agrees.
5. Remind the user the report lists file paths of their setup: keep it private and do not commit it.
