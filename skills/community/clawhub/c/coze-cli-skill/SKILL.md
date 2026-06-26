---
name: coze-cli
description: Interact with Coze CLI (@coze/cli) — create/deploy Coze projects, manage spaces and organizations, send messages to projects, generate images/audio/video, and automate Coze workflows via terminal. Triggered when user mentions "coze", "coze cli", "扣子 CLI", or any coze command execution.
---

# Coze CLI Skill

## Overview

This skill enables AI agents to interact with Coze CLI (`@coze/cli`) — the official command-line tool for Coze/Cozeflow development. It supports project creation, deployment, messaging, multimedia generation, and space management via terminal commands.

**Use this skill when**: The user wants to create/deploy Coze projects, manage spaces/orgs, generate images/audio/video, send messages to Coze projects, or automate Coze workflows via CLI.

## Quick Start

### Installation

```bash
npm install -g @coze/cli
coze --version   # verify
```

### Authentication

```bash
coze auth login --oauth   # opens browser for OAuth flow
coze auth status          # verify login
```

### Initial Setup

```bash
# Select organization
coze org list
coze org use <organization_id>

# Select workspace
coze space list
coze space use <space_id>
```

---

## Core Workflows

### Create a Project

```bash
# Natural language project creation
coze code project create --message "创建一个数据分析 Web 应用" --type web

# With wait (blocking until done)
coze code project create --message "创建一个客服机器人" --type agent --wait
```

**Supported types**: `agent`, `workflow`, `app`, `skill`, `web`, `miniprogram`, `assistant`

### List / Get Projects

```bash
coze code project list                          # all projects
coze code project list --type agent --type web  # filter by type
coze code project list --name "客服"            # search by name
coze code project get <project_id>              # detail
```

### Send Message to Project

```bash
coze code message send "修复登录页面的样式问题" -p <project_id>

# With local file context
coze code message send "重构 @src/utils.ts 中的代码" -p <project_id>

# Via pipe
cat error.log | coze code message send "分析这个错误日志" -p <project_id>

# Check status / cancel
coze code message status -p <project_id>
coze code message cancel -p <project_id>
```

### Deploy Project

```bash
coze code deploy <project_id>           # deploy
coze code deploy <project_id> --wait    # wait for completion
coze code deploy status <project_id>    # check status
```

### Preview Project

```bash
coze code preview <project_id>
```

### Manage Environment Variables

```bash
coze code env list -p <project_id>                   # dev env
coze code env list -p <project_id> --env prod        # prod env
coze code env set API_KEY xxx -p <project_id>         # set
coze code env delete API_KEY -p <project_id>          # delete
```

### Generate Multimedia

```bash
# Image
coze generate image "一只在太空漫步的猫"
coze generate image "未来城市" --output-path ./city.png --size 4K --no-watermark

# Audio
coze generate audio "你好，欢迎使用 Coze CLI"
coze generate audio "你好世界" --output-path ./hello.mp3 --audio-format ogg_opus

# Video
coze generate video create "一只跳舞的小猫"
coze generate video create "日落延时" --wait --output-path ./sunset.mp4 --resolution 1080p --duration 8
coze generate video status <task_id>
```

### Upload File

```bash
coze file upload ./document.pdf
```

---

## Output Format

```bash
# Text (default)
coze space list

# JSON (for scripting)
coze space list --format json
coze code project list --format json | jq '.[].name'
```

---

## CI/CD / Non-Interactive Use

```bash
export COZE_ORG_ID=<YOUR_ORG_ID>
export COZE_SPACE_ID=<YOUR_SPACE_ID>
export COZE_PROJECT_ID=<PROJECT_ID>

coze code deploy <project_id> --wait --format json
```

---

## Global Options

| Option | Description |
| --- | --- |
| `--format json\|text` | Output format (default: text) |
| `--no-color` | Disable ANSI colors |
| `--config <path>` | Custom config file |
| `--org-id <id>` | Override organization ID |
| `--space-id <id>` | Override space ID |
| `-p <project_id>` | Target project ID |
| `--verbose` | Verbose logging |
| `--debug` | Full diagnostic logs |

---

## Configuration

Config priority (high→low):
1. Environment variables (`COZE_ORG_ID`, `COZE_SPACE_ID`, etc.)
2. `--config` CLI flag
3. `COZE_CONFIG_FILE` env var
4. `.cozerc.json` in project dir
5. `~/.coze/config.json` global

```bash
coze config list
coze config get base_url
coze config set base_url https://api.coze.cn
```

---

## Detailed Command Reference

For the full command reference table, see:

→ **[references/commands.md](references/commands.md)**

Contains: auth, org/space, project CRUD, message, deploy, env, domain, skill, multimedia generation, file upload, config, completion, upgrade, CI/CD env vars, and quick command templates.
