---
name: clawhealth-garmin
description: Lightweight Garmin Connect skill that uses the clawhealth Python package to sync health data into local SQLite and expose JSON-friendly commands for OpenClaw.
version: 0.1.8
metadata: {"openclaw":{"homepage":"https://github.com/ernestyu/clawhealth","tags":["health","garmin","sqlite","cli"],"requires":{"bins":["python3"],"anyBins":["python"],"env":["CLAWHEALTH_GARMIN_USERNAME","CLAWHEALTH_GARMIN_PASSWORD_FILE","CLAWHEALTH_DB","CLAWHEALTH_CONFIG_DIR"],"primaryEnv":"CLAWHEALTH_GARMIN_PASSWORD_FILE"},"install":[{"id":"clawhealth_pip","kind":"shell","label":"Install clawhealth from PyPI into a local .venv","script":"set -e && cd {baseDir} && python bootstrap_deps.py"}]}}
---

# clawhealth-garmin (OpenClaw Skill)

Sync your Garmin Connect health data into a local SQLite database
and expose it as structured JSON for OpenClaw agents.

Your agent can then query things like:

- "How did I sleep yesterday?"
- "What is my HRV trend this week?"
- "Am I overtraining?"

This is a **thin wrapper skill** around the published `clawhealth`
Python package / CLI; it no longer fetches source code itself.

## What It Does

- Login with username/password (MFA supported)
- Sync daily health summaries into SQLite (stage 1)
- Fetch HRV + training metrics via separate commands (stage 2)
- Fetch sleep stages + sleep score (stage 2)
- Fetch body composition (stage 2)
- Fetch activity lists and full activity details (stage 2)
- Fetch menstrual day view and calendar range if supported by garminconnect (experimental)
- Provide `--json` outputs for agent workflows
- Persist raw JSON payloads for later analysis

## Prerequisites

- Python 3.10+
- Network access to Garmin Connect
- Garmin account (may require MFA)

If you run OpenClaw in Docker, you may prefer a prepatched image that already
includes the required Python dependencies:

- `ernestyu/openclaw-patched`

## Setup

1) Create `{baseDir}/.env` (see `{baseDir}/ENV_EXAMPLE.md`).

Recommended: use `CLAWHEALTH_GARMIN_PASSWORD_FILE` (password file) rather than
`CLAWHEALTH_GARMIN_PASSWORD` (plaintext env var).

Note: relative paths in env vars (like `./garmin_pass.txt`) are resolved relative
to the skill directory by `run_clawhealth.py`.

2) Install the `clawhealth` package into a local `.venv` (if needed):

```bash
python {baseDir}/bootstrap_deps.py
```

3) Run the skill entrypoint via OpenClaw, which will invoke `run_clawhealth.py`.

See `README.md` / `README_zh.md` in this directory and the root repo for
more details.
