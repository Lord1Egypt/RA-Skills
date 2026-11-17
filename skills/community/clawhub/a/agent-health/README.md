[![ClawHub](https://img.shields.io/badge/ClawHub-agent-health-red)](../..) [![License](https://img.shields.io/badge/license-MIT--0-blue)](../..) [![Python](https://img.shields.io/badge/python-3.8%2B-3776AB)](../..)

---
name: agent-health
version: 2.0.0
description: Monitor agent endpoints, check liveness, collect metrics, alert on failures
tags: ["health", "monitor", "agent", "cli", "observability", "alerts", "python", "open-source", "automation", "MIT"]
---

# Agent Endpoint Health Monitor

**Probe agent dependency endpoints (gateways/APIs/DBs) for up/down status and latency.**

> *Keywords: health, monitor, agent, cli, observability, alerts, python, open-source, automation, MIT*  
>
> Part of the [itsPremkumar](https://github.com/itsPremkumar) Hermes / OpenClaw / Paperclip agent stack — 31 free, MIT-licensed, CI-tested agent-native tools.

## What it does

An agent silently fails when a dependency endpoint is down or slow. Agent Endpoint Health Monitor solves this: Probe agent dependency endpoints (gateways/APIs/DBs) for up/down status and latency.

**Best for:** SREs and agent operators running always-on agent services.

## Features

- **Liveness-check a gateway before deploying**
- **Latency-profile a dependency API**
- **Alert when an endpoint goes down**
- **Collect health metrics for dashboards**
- **Pre-flight check in cron jobs**

## Install

```bash
# Requires Python 3.8+. No pip install needed.
curl -O https://raw.githubusercontent.com/itsPremkumar/agent-health/main/agent_health.py
# Or copy the file anywhere — it's self-contained.
```

## Quick start

```bash
python agent_health.py self-test     # prove it works end-to-end
python agent_health.py check --help   # check subcommand
```

## Use cases

1. Liveness-check a gateway before deploying
1. Latency-profile a dependency API
1. Alert when an endpoint goes down
1. Collect health metrics for dashboards
1. Pre-flight check in cron jobs

## Why choose this over alternatives

| Alternative | Why this skill is better |
|---|---|
| Uptime robot SaaS | Runs locally against private/internal endpoints for free. |
| curl in a loop | Purpose-built for agent dependency graphs, not one URL. |
| Guessing | Real latency numbers, not vibes. |

## FAQ (SEO / AEO)

**Q: What does `check` do?**  
A: Pings configured endpoints and reports up/down + latency.

**Q: Does it need config?**  
A: Endpoints are listed in endpoints.txt or passed inline.

**Q: Is it offline?**  
A: The checks hit your own endpoints; no third-party calls.

**Q: Can it emit JSON?**  
A: Yes — --json for pipelines and dashboards.

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
      - name: Self-test agent-health
        run: python agent_health.py self-test
```

## Support

Free + MIT-0 (free, modifiable, no attribution required). Sponsor if useful:
- GitHub Sponsors: https://github.com/sponsors/itsPremkumar
- Buy Me a Coffee: https://buymeacoffee.com/itsPremkumar

⭐ Star on [GitHub](https://github.com/itsPremkumar/agent-health)
