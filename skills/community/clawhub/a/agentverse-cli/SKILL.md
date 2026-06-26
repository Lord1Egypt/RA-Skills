---
name: agentverse-cli
description: "Publish, discover, and manage AI skills, agents, workflows, souls and prompts from the AgentVerse marketplace. Use when working with the agentverse CLI to search/publish artifacts, authenticate, or manage AI agent ecosystem components."
version: 0.1.4
metadata:
  openclaw:
    homepage: https://github.com/loonghao/agentverse
    emoji: "🤖"
    requires:
      bins:
        - agentverse
    install:
      - kind: shell
        linux: "curl -fsSL https://raw.githubusercontent.com/loonghao/agentverse/main/install.sh | bash"
        macos: "curl -fsSL https://raw.githubusercontent.com/loonghao/agentverse/main/install.sh | bash"
        windows: "irm https://raw.githubusercontent.com/loonghao/agentverse/main/install.ps1 | iex"
---

# AgentVerse CLI

**AgentVerse** (`agentverse`) is the CLI for the universal AI agent marketplace — publish, discover, and manage skills, agents, workflows, souls and prompts.

## Installation

**Linux / macOS:**
```bash
curl -fsSL https://raw.githubusercontent.com/loonghao/agentverse/main/install.sh | bash
```

**Windows (PowerShell):**
```powershell
irm https://raw.githubusercontent.com/loonghao/agentverse/main/install.ps1 | iex
```

## What is AgentVerse?

| Kind | Description |
|------|-------------|
| `skill` | Reusable capabilities (tools, functions) |
| `agent` | Autonomous AI agents with defined capabilities |
| `workflow` | Multi-step orchestration pipelines |
| `soul` | Persona and personality configurations |
| `prompt` | Optimized prompt templates |

## Quick Reference

### Discovery

```bash
# Search across all artifact kinds
agentverse search --query "code review"
agentverse search --query "python" --kind skill

# List by kind / namespace
agentverse list --kind agent
agentverse list --kind skill --namespace myorg

# Get a specific artifact (latest version)
agentverse get --kind skill --namespace myorg --name my-skill

# Pin to a specific version
agentverse get --kind skill --namespace myorg --name my-skill --version 1.2.0

# Show version history
agentverse versions --kind skill --namespace python-tools --name linter
```

### Publishing

```bash
# Publish a new artifact or new version
agentverse publish --file skill.toml

# Update metadata / content
agentverse update --kind skill --namespace myorg --name my-skill --file skill.toml

# Fork an artifact
agentverse fork --kind skill --namespace source-org --name original \
  --new-namespace myorg --new-name my-fork

# Deprecate (soft delete)
agentverse deprecate --kind skill --namespace myorg --name old-skill
```

### Authentication

```bash
# Point to a custom AgentVerse server
export AGENTVERSE_URL=https://agentverse.example.com
agentverse login

# Register a new account
agentverse register --username alice --email alice@example.com

# Show current user
agentverse whoami
```

### Social

```bash
# Rate an artifact (1–5 stars)
agentverse rate --kind skill --namespace myorg --name my-skill --stars 5

# Like / unlike
agentverse like   --kind skill --namespace myorg --name my-skill
agentverse unlike --kind skill --namespace myorg --name my-skill

# Post a comment
agentverse comment --kind skill --namespace myorg --name my-skill \
  --message "Great tool!"

# View social stats
agentverse stats --kind skill --namespace myorg --name my-skill
```

### Agent Use (Programmatic)

```bash
# Record a learning insight
agentverse learn --kind skill --namespace myorg --name my-skill \
  --insight "Works well for Python 3.12"

# Submit benchmark results
agentverse benchmark --kind skill --namespace myorg --name my-skill \
  --score 0.95 --metric accuracy
```

### Self-Update

```bash
# Check for newer version without installing
agentverse self-update --check

# Update to the latest release
agentverse self-update

# Use a GitHub token to avoid rate limits
agentverse self-update --token ghp_your_token
```

## Global Flags

| Flag | Env Var | Default | Description |
|------|---------|---------|-------------|
| `--server` | `AGENTVERSE_URL` | `http://localhost:8080` | Server URL |
| `--token` | `AGENTVERSE_TOKEN` | — | Bearer token for authenticated ops |

## Links

- **Repository**: https://github.com/loonghao/agentverse
- **Docker Image**: `ghcr.io/loonghao/agentverse:latest`

