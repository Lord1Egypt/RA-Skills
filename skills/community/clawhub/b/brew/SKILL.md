---
name: brew
description: Manage Homebrew end-to-end on macOS, including detecting whether Homebrew is installed, understanding formula vs cask, updating metadata and packages, installing/uninstalling software, searching/listing package state, cleanup/autoremove, diagnostics, and Brewfile workflows. Use when users ask to update brew, install or remove apps/tools with brew, check outdated packages, fix brew errors, export/sync package setup, or verify Homebrew environment health.
---

# Homebrew

## Overview
Use this skill to run Homebrew operations safely and consistently on macOS. Start by checking whether Homebrew exists, then perform package lifecycle tasks (update/install/uninstall/verify) based on user intent.

## Quick Start Workflow
1. Confirm platform compatibility (Homebrew tasks here are for macOS).
2. Detect whether Homebrew is installed.
3. If missing, report clearly and ask whether to install Homebrew first.
4. If present, execute the requested brew operation.
5. Verify the result and report concise next steps.

## Detect Homebrew Installation (Required First Step)
Run in this order:

```bash
command -v brew
brew --version
```

Interpretation:
- `command -v brew` returns a path (for example `/opt/homebrew/bin/brew` or `/usr/local/bin/brew`) → Homebrew installed.
- Command not found or non-zero exit → Homebrew not installed.

If not installed, reply with:
- “Homebrew is not installed on this Mac.”
- Ask whether to proceed with installation.
- If user agrees, run Homebrew’s official installer:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

## Core Concepts (From Homebrew Manpage)
- **formula**: package definition built from source or bottle (`brew install <formula>`).
- **cask**: prebuilt app/binary package (`brew install --cask <cask>`).
- Prefer formula for developer tools and cask for desktop apps.

## Common Operations

### Update Homebrew
Use when user says “更新 brew / update brew / upgrade brew itself”.

```bash
brew update
brew --version
```

Optional follow-up for packages (ask or infer from request):

```bash
brew upgrade
brew cleanup
```

### Install Packages
1. Determine install type:
   - CLI/tool/library: formula (`brew install <name>`)
   - App: cask (`brew install --cask <name>`)
2. Install.
3. Verify installation (`brew list --versions <name>` or open app checks for casks).

Examples:

```bash
brew install wget
brew install --cask iterm2
```

### Uninstall Packages
1. Confirm target package name.
2. Uninstall with correct type.
3. Verify removal.

Examples:

```bash
brew uninstall wget
brew uninstall --cask iterm2
```

### Status and Discovery
Use when user asks “what do I have / what can I install / what is outdated”.

```bash
brew search <keyword>
brew list
brew list --cask
brew info <name>
brew outdated
```

### Cleanup and Dependency Maintenance
Use after large upgrades/uninstalls or when disk cleanup is requested.

```bash
brew cleanup
brew autoremove --dry-run
brew autoremove
```

Run `--dry-run` first when safety matters.

### Brewfile (Environment Sync / Backup)
Use when user wants to export or reproduce package setup.

```bash
brew bundle dump --file Brewfile
brew bundle check --file Brewfile
brew bundle install --file Brewfile
```

## Intent → Command Mapping (Fast Routing)
Use this table to convert natural-language requests into reliable brew commands.

- “更新 brew 本身 / 更新索引” → `brew update`
- “升级已安装的软件” → `brew upgrade` (optionally `brew upgrade --cask` when user focuses on apps)
- “清理缓存和旧版本” → `brew cleanup`
- “安装命令行工具 xxx” → `brew install <xxx>`
- “安装桌面应用 xxx” → `brew install --cask <xxx>`
- “卸载命令行工具 xxx” → `brew uninstall <xxx>`
- “卸载桌面应用 xxx” → `brew uninstall --cask <xxx>`
- “查找有没有 xxx” → `brew search <xxx>`
- “看看装了什么” → `brew list` / `brew list --cask`
- “查看 xxx 详情” → `brew info <xxx>`
- “看哪些过期了” → `brew outdated`
- “导出当前环境” → `brew bundle dump --file Brewfile`
- “按 Brewfile 同步环境” → `brew bundle install --file Brewfile`

## Failure Handling Playbook
When commands fail, capture the key error and apply the minimal safe fix path.

1. Run diagnostics:

```bash
brew doctor
brew config
```

2. If package not found:

```bash
brew update
brew search <name>
```

3. If download/network errors: retry once after `brew update`; report mirror/network suspicion.
4. If permission/path conflicts: report exact path/conflict line and ask before destructive fixes.
5. If cask already installed or link conflicts: prefer explicit overwrite/reinstall only with user confirmation.

## Helpful Diagnostic Commands
Use these when user asks for status, troubleshooting, or package discovery.

```bash
brew doctor
brew config
brew search <keyword>
brew list
brew list --cask
brew outdated
brew info <name>
```

## Response Style
- Report exactly what was run and what changed.
- For failed installs/uninstalls, include the key error line and a concrete retry/fix step.
- Keep output concise; avoid dumping full logs unless user asks.
