---
name: cleanup-reporter
description: Scan your machine for large directories, duplicate files, and stale resume files.
homepage: https://github.com/MalavyaRaval/cleanup-reporter
metadata:
  clawdbot:
    emoji: "🧹"
  requires:
    env: []
  files: ["scripts/*"]
---

# Cleanup Reporter Skill

This skill helps you identify disk space hogs, duplicate files, and stale data on your machine.

## Tools
- `ncdu`: Visual disk usage analyzer
- `rdfind`: Duplicate file finder

## Usage
- Run `cleanup-reporter-scan` to perform a scan and generate a report.
- It will create a report file in `~/reports/cleanup_report_YYYY-MM-DD.md`.

## External Endpoints
- None. This skill operates entirely locally.

## Security & Privacy
- **What leaves the machine:** Nothing.
- **What is accessed:** Local directories `/mnt/c/Users/malav` for scanning.
- **Data persistence:** Only the generated markdown report and `rdfind` temp files are written to disk.

## Model Invocation Note
This skill is invoked autonomously by OpenClaw when triggered by the user to perform cleanup tasks.

## Trust Statement
By using this skill, you allow the agent to scan your local file system. Only install if you trust the agent's access to your local files.
