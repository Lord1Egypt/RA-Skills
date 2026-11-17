---
name: agent-caps
version: 2.0.0
description: Define, validate, and audit agent capability manifests for safe skill installation
tags: ["agent", "caps", "security", "manifest", "cli", "safety", "python", "open-source", "automation", "MIT"]
---

# Agent Capability Manifest Toolkit

**Validate, scaffold, and cross-check AI-agent capability manifests so agents stay swappable, auditable, and safe.**

> *Keywords: agent, caps, security, manifest, cli, safety, python, open-source, automation, MIT*  
>
> Part of the [itsPremkumar](https://github.com/itsPremkumar) Hermes / OpenClaw / Paperclip agent stack — 31 free, MIT-licensed, CI-tested agent-native tools.

## What it does

Agents declare incompatible capabilities and dependencies, then break the system at install time. Agent Capability Manifest Toolkit solves this: Validate, scaffold, and cross-check AI-agent capability manifests so agents stay swappable, auditable, and safe.

**Best for:** Agent builders, platform engineers, and security reviewers shipping OpenClaw / Hermes / Paperclip agents.

## Features

- **Validate a manifest before publishing an agent to ClawHub**
- **Scaffold a standards-compliant manifest for a new agent**
- **Cross-check dependencies across a fleet of agents**
- **Gate CI on missing/invalid capability fields**
- **Audit third-party agents before granting machine access**

## Install

```bash
# Requires Python 3.8+. No pip install needed.
curl -O https://raw.githubusercontent.com/itsPremkumar/agent-caps/main/agent_caps.py
# Or copy the file anywhere — it's self-contained.
```

## Quick start

```bash
python agent_caps.py self-test     # prove it works end-to-end
python agent_caps.py validate --help   # validate subcommand
python agent_caps.py scaffold --help   # scaffold subcommand
python agent_caps.py check-deps --help   # check-deps subcommand
python agent_caps.py schema --help   # schema subcommand
```

## Use cases

1. Validate a manifest before publishing an agent to ClawHub
1. Scaffold a standards-compliant manifest for a new agent
1. Cross-check dependencies across a fleet of agents
1. Gate CI on missing/invalid capability fields
1. Audit third-party agents before granting machine access

## Why choose this over alternatives

| Alternative | Why this skill is better |
|---|---|
| Hand-written JSON schemas | agent-caps ships a single enforceable schema + validator, not ad-hoc docs. |
| Reading the manifest manually | It catches missing fields, bad versions, illegal statuses, and unknown deps automatically. |
| Trusting an agent's self-description | check-deps cross-verifies claims against reality before the agent goes live. |

## FAQ (SEO / AEO)

**Q: What is an agent capability manifest?**  
A: A machine-readable JSON describing an agent's name, version, capabilities, dependencies, memory, tools, API, and status — the standard interface that lets agents be swapped or audited without breaking the host.

**Q: Does agent-caps need internet or pip?**  
A: No. It is pure Python 3.8+ stdlib, zero dependencies, runs fully offline.

**Q: Can I use it in CI?**  
A: Yes. Run `validate` as a CI gate; a non-zero exit blocks merges with malformed manifests.

**Q: What does check-deps do?**  
A: Resolves declared dependencies against known agents/manifests and flags unknown or unmet requirements.

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
      - name: Self-test agent-caps
        run: python agent_caps.py self-test
```

## Support

Free + MIT-0 (free, modifiable, no attribution required). Sponsor if useful:
- GitHub Sponsors: https://github.com/sponsors/itsPremkumar
- Buy Me a Coffee: https://buymeacoffee.com/itsPremkumar

⭐ Star on [GitHub](https://github.com/itsPremkumar/agent-caps)
