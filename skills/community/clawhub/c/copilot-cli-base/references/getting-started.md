---
title: "Getting Started"
source:
  - https://docs.github.com/en/copilot/concepts/agents/copilot-cli/about-copilot-cli
  - https://docs.github.com/en/copilot/how-tos/copilot-cli/set-up-copilot-cli/install-copilot-cli
  - https://docs.github.com/en/copilot/how-tos/copilot-cli/set-up-copilot-cli/configure-copilot-cli
category: reference
---

Setup, installation, authentication, and configuration for GitHub Copilot CLI — a terminal-native AI coding agent.

## What Copilot CLI Is

Terminal AI agent that answers questions, writes/debugs code, interacts with GitHub, and completes multi-step tasks autonomously. Available with all Copilot plans (org admins must enable CLI policy).

**OS:** Linux, macOS, Windows (PowerShell 6+, WSL). **Default model:** Claude Sonnet 4.5 (changeable via `/model` or `--model`).

**Modes:** Ask/execute (default), **plan mode** (Shift+Tab — builds structured implementation plan before code), and programmatic (`-p`). Context is auto-compacted at 95% token limit for virtually infinite sessions; use `/compact` manually or `/context` to visualize token usage.

## Installation

### npm (all platforms)
```bash
npm install -g @github/copilot
# Prerelease: npm install -g @github/copilot@prerelease
# If ignore-scripts=true: npm_config_ignore_scripts=false npm install -g @github/copilot
```

### Homebrew (macOS/Linux)
```bash
brew install copilot-cli    # prerelease: copilot-cli@prerelease
```

### WinGet (Windows)
```bash
winget install GitHub.Copilot    # prerelease: GitHub.Copilot.Prerelease
```

### Install Script (macOS/Linux)
```bash
curl -fsSL https://gh.io/copilot-install | bash
# Custom: VERSION="v0.0.369" PREFIX="$HOME/custom" bash
```

### Download from GitHub.com
Download executables directly from the [`copilot-cli` releases](https://github.com/github/copilot-cli/releases/). Unpack and run.

### Update
```bash
copilot update
```

**Prerequisites:** Active Copilot subscription, Node.js 22+ (npm method).

## Authentication

**Credential lookup order:** `COPILOT_GITHUB_TOKEN` → `GH_TOKEN` → `GITHUB_TOKEN` → OAuth keychain → `gh auth token` fallback.

| Token type | Prefix | Supported |
|-----------|--------|-----------|
| OAuth (device flow) | `gho_` | Yes (default via `/login`) |
| Fine-grained PAT | `github_pat_` | Yes (needs **Copilot Requests** perm) |
| GitHub App user-to-server | `ghu_` | Yes |
| Classic PAT | `ghp_` | **No** |

### OAuth Login
```bash
copilot login                    # or /login inside CLI
copilot login --host HOSTNAME    # GitHub Enterprise Cloud
```

### CI/CD Auth
Create fine-grained PAT with **Copilot Requests** permission, then: `export COPILOT_GITHUB_TOKEN=<token>`

### Credential Storage
macOS: Keychain · Windows: Credential Manager · Linux: libsecret (fallback: plaintext in `config.json`)

### Account Management
`/user` show · `/user list` · `/user switch` · `/logout`

## Configuration

Settings cascade: user < repository < local. CLI flags and env vars have highest precedence.

| Scope | Location |
|-------|----------|
| User | `~/.copilot/config.json` (override with `COPILOT_HOME`) |
| Repository | `.github/copilot/settings.json` (commit to repo) |
| Local | `.github/copilot/settings.local.json` (gitignore this) |

### Key Config Options

| Key | Default | Description |
|-----|---------|-------------|
| `trusted_folders` | `[]` | Pre-trusted directories |
| `model` | varies | AI model |
| `theme` | `"auto"` | `"auto"`, `"dark"`, `"light"` |
| `effortLevel` | `"medium"` | `low`, `medium`, `high`, `xhigh` |
| `hooks` | -- | Inline hook definitions |
| `disableAllHooks` | `false` | Disable all hooks |
| `allowed_urls` / `denied_urls` | `[]` | URL allow/deny lists |

**No `copilot config set`** — edit `~/.copilot/config.json` manually or use `/model` for model selection.

### Trusted Directories

On session start, CLI asks to trust the current directory. Options: session only, permanently, or exit.

- Edit: `config.json` → `trusted_folders` array
- Mid-session: `/add-dir PATH`, `/list-dirs`, `/cwd PATH`
- **`--yolo` does NOT bypass the trust prompt** — pre-trust in config for automation

## Tool Permissions

| Flag | Effect |
|------|--------|
| `--allow-all-tools` | Skip all tool approval |
| `--allow-tool=TOOL` | Allow specific tool |
| `--deny-tool=TOOL` | Block tool (highest precedence) |
| `--available-tools=TOOL` | Restrict to only these tools |
| `--allow-all` / `--yolo` | All tools + paths + URLs |

During an interactive session, use the `/allow-all` or `/yolo` slash commands to enable all permissions.

**Format:** `Kind(argument)` — argument optional.

| Kind | Examples |
|------|----------|
| `shell` | `shell(git push)`, `shell(git:*)`, `shell` |
| `write` | `write`, `write(src/*.ts)` |
| `read` | `read`, `read(.env)` |
| `url` | `url(github.com)`, `url(https://*.github.com)` |
| `memory` | `memory` |
| MCP-SERVER | `github(create_issue)`, `MyMCP` |

Deny always overrides allow. `:*` matches command stem + space.

```bash
# Allow git except push
copilot --allow-tool='shell(git:*)' --deny-tool='shell(git push)'
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `COPILOT_HOME` | Config directory (default `~/.copilot`) |
| `COPILOT_MODEL` | Default model |
| `COPILOT_ALLOW_ALL` | `true` for full permissions |
| `COPILOT_GITHUB_TOKEN` | Auth token (highest precedence) |
| `GH_TOKEN` / `GITHUB_TOKEN` | Auth tokens (lower precedence) |
| `COPILOT_EDITOR` | Editor (after `$VISUAL`, `$EDITOR`) |
| `COPILOT_CUSTOM_INSTRUCTIONS_DIRS` | Additional instruction dirs |
| `COPILOT_SKILLS_DIRS` | Additional skill dirs |

## Path & URL Permissions

| Flag | Effect |
|------|--------|
| `--allow-all-paths` | Access any path |
| `--disallow-temp-dir` | Block temp directory |
| `--allow-all-urls` | Access any URL |
| `--allow-url=DOMAIN` / `--deny-url=DOMAIN` | Per-domain URL control |

**Path scope:** By default, CLI can access CWD, its subdirectories, and system temp dir. Path detection for shell commands has limitations — custom env vars like `$MY_PROJECT_DIR` are not expanded.

**URL scope:** HTTP and HTTPS are treated as different protocols and require separate approval. URL permissions can be persisted per-session or permanently.
