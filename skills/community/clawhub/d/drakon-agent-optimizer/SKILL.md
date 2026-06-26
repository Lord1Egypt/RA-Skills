---
name: agent-optimizer
description: >
  CLI tool that audits OpenClaw config files for misconfigurations, token waste,
  security issues, and stale auth. Reads local JSON config files only. No data
  leaves the machine. No API keys required. No network calls except one-time
  license activation and npm update check.
license: SEE LICENSE IN LICENSE.md
metadata:
  author: Drakon Systems
  version: 0.8.1
  category: devtools
  tags:
    - openclaw-audit
    - openclaw-security
    - openclaw-optimize
    - config-audit
    - security-scanner
    - token-optimization
    - fleet-management
    - cost-estimation
    - devtools
    - cli
  source: https://github.com/Drakon-Systems-Ltd/agent-optimizer
  homepage: https://drakonsystems.com/products/agent-optimizer
  npm: https://www.npmjs.com/package/@drakon-systems/agent-optimizer
  verified_publisher: Drakon Systems Ltd
  publisher_github: https://github.com/Drakon-Systems-Ltd
  npm_audit: clean
  openclaw:
    requires:
      - node>=20
    credentials:
      primary: none
      note: >
        No API keys or secrets required. The tool reads local config files only.
        Fleet SSH audit uses the user's existing SSH config (~/.ssh/config) and
        keys — no credentials are stored, transmitted, or prompted for by the tool.
    config_paths:
      - ~/.openclaw/openclaw.json
      - ~/.openclaw/agents/main/agent/auth-profiles.json
      - ~/.openclaw/agents/main/agent/models.json
      - ~/.openclaw/workspace/ (skills, hooks, extensions scanned for patterns)
    network:
      - "One-time HTTPS call to drakonsystems.com/api/agent-optimizer/activate on license activation only"
      - "HTTPS call to registry.npmjs.org on agent-optimizer update only"
      - "No telemetry, no analytics, no phone-home during audit/scan/optimize"
    data_handling:
      - "All analysis is local — no config data, audit results, or file contents leave the machine"
      - "License stored locally at ~/.agent-optimizer/license.json (RSA-signed JWT, verified offline)"
      - "Config snapshots stored locally at ~/.agent-optimizer/snapshots/"
    fleet_ssh:
      - "Fleet audit runs `cat ~/.openclaw/openclaw.json` over SSH on each host"
      - "Uses the user's existing SSH config and keys — no key storage or prompting"
      - "Requires Fleet or Lifetime license"
install:
  command: npm install -g @drakon-systems/agent-optimizer
  runtime: node
  minVersion: "20"
  note: >
    Installs the `agent-optimizer` CLI globally via npm. No account or API key
    needed. The free audit reads ~/.openclaw/openclaw.json and related config
    files to check for misconfigurations. Security scan reads skills/, hooks/,
    and extensions/ directories for suspicious patterns (billing, injection,
    obfuscation). Nothing is transmitted off-machine.
---

# Agent Optimizer by Drakon Systems

**Audit, optimize, and secure OpenClaw AI agent deployments.**

70+ checks across 15 auditor modules. Free to install and run.

## What It Reads (and doesn't)

**Reads (local files only):**
- `~/.openclaw/openclaw.json` — model config, heartbeat, compaction, plugins
- `~/.openclaw/agents/*/agent/auth-profiles.json` — token expiry checks (does NOT extract or transmit keys)
- `~/.openclaw/agents/*/agent/models.json` — legacy override detection
- Workspace `skills/`, `hooks/`, `extensions/` — pattern-matched for billing/injection/obfuscation signatures

**Does NOT:**
- Send any data off-machine (no telemetry, no analytics)
- Store or prompt for API keys, SSH keys, or provider credentials
- Modify any files unless `--fix` or `optimize` is run with a license (creates backup first)
- Make network calls during audit/scan (only `activate` and `update` touch the network)

## Fleet SSH Audit

The `fleet --hosts` command runs `cat ~/.openclaw/openclaw.json` over SSH on each listed host using your existing `~/.ssh/config` entries. It does not store, copy, or prompt for SSH keys. Requires Fleet or Lifetime license.

## Quick Start

```bash
npm install -g @drakon-systems/agent-optimizer
agent-optimizer audit          # Free — 70+ checks
agent-optimizer scan           # Free — malware + billing scan
agent-optimizer optimize --dry-run  # Free — preview optimizations
```

## Auditor Modules (15)

Model Config, Auth Profiles, Cost Estimator, Token Efficiency, Cache Efficiency,
Bootstrap Files, Security Scanner, Plugins, Legacy Overrides, Tool Permissions,
Provider Failover, Channel Security, Memory Search, Local Models, Security Advisories.

## Pricing

| Tier | Price | Key Features |
|------|-------|-------------|
| Free | £0 | Full audit, first 3 fix instructions, scan, preview |
| Solo | £29 | All fixes unlocked, auto-fix, optimize profiles |
| Fleet | £79 | SSH fleet audit, per-host comparison |
| Lifetime | £149 | Everything + 12mo updates + priority support |

Purchase: [drakonsystems.com/products/agent-optimizer](https://drakonsystems.com/products/agent-optimizer)
