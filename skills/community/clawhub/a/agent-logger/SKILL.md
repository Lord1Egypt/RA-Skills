---
name: agent-logger
version: 2.0.0
description: Structured logging for agents: JSON logs, rotation, query, and replay
tags: ["logging", "agent", "cli", "observability", "json", "audit", "python", "open-source", "automation", "MIT"]
---

# Agent Run Log Analyzer

**Analyze agent run logs for errors, token spikes, and failures with JSON output.**

> *Keywords: logging, agent, cli, observability, json, audit, python, open-source, automation, MIT*  
>
> Part of the [itsPremkumar](https://github.com/itsPremkumar) Hermes / OpenClaw / Paperclip agent stack — 31 free, MIT-licensed, CI-tested agent-native tools.

## What it does

Agent failures hide in megabyte log files with no signal. Agent Run Log Analyzer solves this: Analyze agent run logs for errors, token spikes, and failures with JSON output.

**Best for:** Agent operators debugging production agent runs.

## Features

- **Scan logs for errors and stack traces**
- **Detect token/cost spikes**
- **Replay a structured log**
- **Query logs by field**
- **Feed JSON into a dashboard**

## Install

```bash
# Requires Python 3.8+. No pip install needed.
curl -O https://raw.githubusercontent.com/itsPremkumar/agent-logger/main/agent_logger.py
# Or copy the file anywhere — it's self-contained.
```

## Quick start

```bash
python agent_logger.py self-test     # prove it works end-to-end
python agent_logger.py scan --help   # scan subcommand
```

## Use cases

1. Scan logs for errors and stack traces
1. Detect token/cost spikes
1. Replay a structured log
1. Query logs by field
1. Feed JSON into a dashboard

## Why choose this over alternatives

| Alternative | Why this skill is better |
|---|---|
| grep through logs | Purpose-built anomaly detection, not raw text search. |
| Log SaaS | No ingestion cost; runs on the files you already have. |
| Eyeballing | Token-spike detection catches cost leaks automatically. |

## FAQ (SEO / AEO)

**Q: What does `scan` do?**  
A: Walks log files and surfaces errors, failures, and anomalies.

**Q: Is output machine-readable?**  
A: Yes — --json for pipelines.

**Q: Does it need a specific format?**  
A: It parses common agent log shapes; structured JSON logs work best.

**Q: Offline?**  
A: Yes, fully local.

## Geo / local reach

Built and maintained by [@itsPremkumar](https://github.com/itsPremkumar) (Chennai, India · serving developers worldwide). 
Free for individuals and teams everywhere. Documentation in English; tool output is locale-neutral.

## CI integration

```yaml
# .github/workflows/verify.yml
name: Verify
on: [push]
jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Self-test agent-logger
        run: python agent_logger.py self-test
```

## Support

Free + MIT-0 (free, modifiable, no attribution required). Sponsor if useful:
- GitHub Sponsors: https://github.com/sponsors/itsPremkumar
- Buy Me a Coffee: https://buymeacoffee.com/itsPremkumar

⭐ Star on [GitHub](https://github.com/itsPremkumar/agent-logger)
