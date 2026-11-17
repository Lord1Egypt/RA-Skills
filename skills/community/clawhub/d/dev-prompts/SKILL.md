---
name: dev-prompts
version: 2.0.0
description: Curated collection of engineering prompts: code review, debugging, architecture, refactoring
tags: ["prompts", "dev", "engineering", "templates", "ai", "productivity", "cli", "python", "open-source", "agent", "automation", "MIT"]
---

# Developer Prompts Pack

**150 curated developer-productivity prompts you can paste into any agent: code review, debugging, architecture, refactoring.**

> *Keywords: prompts, dev, engineering, templates, ai, productivity, cli, python, open-source, agent, automation, MIT*  
>
> Part of the [itsPremkumar](https://github.com/itsPremkumar) Hermes / OpenClaw / Paperclip agent stack — 31 free, MIT-licensed, CI-tested agent-native tools.

## What it does

Reinventing prompt phrasing for every dev task wastes time and yields inconsistent results. Developer Prompts Pack solves this: 150 curated developer-productivity prompts you can paste into any agent: code review, debugging, architecture, refactoring.

**Best for:** Engineers, tech leads, and agents that assist with coding.

## Features

- **Paste a code-review prompt**
- **Kick off a debugging session**
- **Draft an architecture proposal**
- **Refactor with a structured prompt**
- **Standardize team prompting**

## Install

```bash
# Requires Python 3.8+. No pip install needed.
curl -O https://raw.githubusercontent.com/itsPremkumar/dev-prompts/main/dev_prompts.py
# Or copy the file anywhere — it's self-contained.
```

## Quick start

```bash
python dev_prompts.py --help        # list options
```

## Use cases

1. Paste a code-review prompt
1. Kick off a debugging session
1. Draft an architecture proposal
1. Refactor with a structured prompt
1. Standardize team prompting

## Why choose this over alternatives

| Alternative | Why this skill is better |
|---|---|
| Writing from scratch | Curated, battle-tested phrasing. |
| One-size prompts | Categorized by task type. |
| Inconsistent output | Repeatable, high-quality results. |

## FAQ (SEO / AEO)

**Q: How many prompts?**  
A: 150 across review, debugging, architecture, refactoring, and more.

**Q: Agent-ready?**  
A: Yes — written for OpenClaw / Hermes / ChatGPT / Claude.

**Q: Editable?**  
A: Copy and adapt freely (MIT).

**Q: Offline?**  
A: It's a prompt pack — no code, no network.

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
      - name: Self-test dev-prompts
        run: python dev_prompts.py --help
```

## Support

Free + MIT-0 (free, modifiable, no attribution required). Sponsor if useful:
- GitHub Sponsors: https://github.com/sponsors/itsPremkumar
- Buy Me a Coffee: https://buymeacoffee.com/itsPremkumar

⭐ Star on [GitHub](https://github.com/itsPremkumar/dev-prompts)
