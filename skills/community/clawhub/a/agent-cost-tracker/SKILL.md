---
name: agent-cost-tracker
version: 2.0.0
description: Track LLM API spending per agent/session with budget alerts and CSV export
tags: ["cost", "tracking", "llm", "budget", "cli", "finance", "python", "open-source", "agent", "automation", "MIT"]
---

# LLM Cost & Token Tracker

**Estimate and tally LLM API spending per agent/session with budget alerts and CSV export.**

> *Keywords: cost, tracking, llm, budget, cli, finance, python, open-source, agent, automation, MIT*  
>
> Part of the [itsPremkumar](https://github.com/itsPremkumar) Hermes / OpenClaw / Paperclip agent stack — 31 free, MIT-licensed, CI-tested agent-native tools.

## What it does

Token spend balloons silently across agents and models with no per-agent accountability. LLM Cost & Token Tracker solves this: Estimate and tally LLM API spending per agent/session with budget alerts and CSV export.

**Best for:** Founders, finops, and agent operators running multi-agent LLM workloads on GPT/Claude/Gemini.

## Features

- **Estimate cost before sending a prompt**
- **Tally spend from agent run logs**
- **Set per-agent budget alerts**
- **Export a CSV for finance**
- **Compare model pricing at a glance**

## Install

```bash
# Requires Python 3.8+. No pip install needed.
curl -O https://raw.githubusercontent.com/itsPremkumar/agent-cost-tracker/main/agent_cost_tracker.py
# Or copy the file anywhere — it's self-contained.
```

## Quick start

```bash
python agent_cost_tracker.py self-test     # prove it works end-to-end
python agent_cost_tracker.py tally --help   # tally subcommand
python agent_cost_tracker.py estimate --help   # estimate subcommand
```

## Use cases

1. Estimate cost before sending a prompt
1. Tally spend from agent run logs
1. Set per-agent budget alerts
1. Export a CSV for finance
1. Compare model pricing at a glance

## Why choose this over alternatives

| Alternative | Why this skill is better |
|---|---|
| Cloud billing dashboards | Per-agent, per-session granularity you control locally. |
| Mental math on token counts | Price tables + estimation remove the guesswork. |
| Spreadsheet tracking | CSV export drops straight into your existing finance stack. |

## FAQ (SEO / AEO)

**Q: Which models are supported?**  
A: gpt-* (OpenAI), claude-* (Anthropic), gemini-* (Google) with built-in price tables.

**Q: Where does it get tokens?**  
A: From agent run logs (tally) or from --prompt/--completion estimates.

**Q: Does it call the API?**  
A: No. It is an estimator/tally from logs and inputs; no network calls.

**Q: Can I export to CSV?**  
A: Yes — CSV export is built in for spreadsheets and BI tools.

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
      - name: Self-test agent-cost-tracker
        run: python agent_cost_tracker.py self-test
```

## Support

Free + MIT-0 (free, modifiable, no attribution required). Sponsor if useful:
- GitHub Sponsors: https://github.com/sponsors/itsPremkumar
- Buy Me a Coffee: https://buymeacoffee.com/itsPremkumar

⭐ Star on [GitHub](https://github.com/itsPremkumar/agent-cost-tracker)
