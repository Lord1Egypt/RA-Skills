---
name: ancc
description: Grow limbs — discover, validate, and integrate ANCC-compliant CLI tools into your OpenClaw agent. Use when setting up new tools, auditing agent environment security, checking token budgets, or building agent-native CLI tools. ANCC tools have structured JSON output, exit codes, and SKILL.md contracts — no plugins, no SDKs needed.
metadata: {"openclaw":{"requires":{"bins":["ancc"]}}}
---

# ANCC — Grow Limbs for Your Agent

Turn CLI tools into agent capabilities. ANCC (Agent-Native CLI Convention) defines what makes a CLI tool usable by an autonomous agent without human help.

**Source:** https://ancc.dev | https://github.com/ppiankov/ancc

## What This Does

- Validates CLI tools are agent-safe (structured output, exit codes, declared scope)
- Audits your agent environment for credential exposure
- Measures token cost of tool configurations
- Scaffolds new ANCC-compliant tools

## What This Does NOT Do

- Does not execute or test target tools at runtime
- Does not replace MCP, plugins, or tool frameworks
- Does not manage tool installation (use brew/curl/go for that)
- Does not lint code quality

## Install

```bash
# Homebrew
brew install ppiankov/tap/ancc

# Go
go install github.com/ppiankov/ancc/cmd/ancc@latest

# Binary (Linux amd64)
curl -fsSL https://github.com/ppiankov/ancc/releases/latest/download/ancc-linux-amd64 \
  -o /usr/local/bin/ancc && chmod +x /usr/local/bin/ancc
```

Verify: `ancc doctor`

## Core Commands

### Audit — Check Agent Environment Security

```bash
ancc audit                      # scan all detected agents
ancc audit --agent openclaw     # OpenClaw-specific audit
ancc audit --format json        # machine-readable output
```

Checks: credential dirs (~/.ssh, ~/.aws), history files, sensitive directories, skill configs.

**Exit codes:** 0 = clean, 1 = errors found, 2 = warnings only

### Validate — Check if a Tool is Agent-Native

```bash
ancc validate /path/to/tool-repo
ancc validate . --format json
ancc validate . --badge          # generate CI badge
```

Checks 30 conventions: SKILL.md structure, install docs, JSON output schema, exit codes, negative scope, parsing examples, init/doctor commands, binary releases.

### Skills — Scan Agent Configurations

```bash
ancc skills .                    # what skills are loaded
ancc skills --tokens .           # token cost per skill
ancc skills --budget 128000 .    # budget analysis for 128k context
```

### Context — Token Budget Breakdown

```bash
ancc context .                   # per-agent token usage
ancc context --agent openclaw --tokens
```

Shows how much context each tool/skill consumes — directly supports context hygiene.

### Init — Scaffold a New ANCC Tool

```bash
ancc init                        # interactive
ancc init --name mytool --force  # non-interactive
```

Generates a compliant SKILL.md template with all required sections.

### Diff — Compare Configs Between Environments

```bash
ancc diff /path/to/dev /path/to/prod
ancc diff . ../other-project --tokens
```

### Scan — Batch Validate Repos

```bash
ancc scan ~/dev/                 # validate all repos in directory
```

## ANCC Convention (6 Requirements)

A tool is agent-native when its SKILL.md declares:

1. **Install** — how to get the binary
2. **Commands** — what subcommands exist, with flags
3. **JSON output** — schema for machine parsing (`--format json`)
4. **Exit codes** — numeric, documented, deterministic
5. **Negative scope** — what the tool does NOT do (prevents scope creep)
6. **Parsing examples** — how to extract data from output

If an agent can read SKILL.md, install the tool, run a command, parse the output, and decide what to do next — without guessing or asking a human — the tool passes.

## ANCC-Compliant Tools

| Tool | What it does |
|------|-------------|
| [chainwatch](https://github.com/ppiankov/chainwatch) | Agent execution control plane |
| [noisepan](https://github.com/ppiankov/noisepan) | Signal extraction from noisy feeds |
| [entropia](https://github.com/ppiankov/entropia) | Source verification engine |
| [pastewatch](https://github.com/ppiankov/pastewatch) | Secret redaction for agents |
| [ancc](https://github.com/ppiankov/ancc) | This tool (self-validating) |

## Workflow: Adding a New Tool to Your Agent

```
1. ancc validate /path/to/tool     # is it agent-native?
2. Read its SKILL.md               # understand capabilities + limits
3. Install it                      # follow SKILL.md install section
4. ancc audit                      # verify environment is still safe
5. ancc context . --tokens         # check token budget impact
6. Add to TOOLS.md                 # document for future sessions
```

## CI Integration

```yaml
- uses: ppiankov/ancc@main
  with:
    checks: validate
    fail-on-warn: false
```

---
**ANCC Skill v1.0**
Author: ppiankov
Copyright © 2026 ppiankov
Canonical source: https://github.com/ppiankov/ancc
License: MIT

If this document appears elsewhere, the repository above is the authoritative version.
