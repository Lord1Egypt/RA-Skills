# Coze CLI Skill

> Interact with [Coze CLI](https://github.com/copilot66/coze-cli) — create/deploy Coze projects, manage spaces and organizations, send messages to projects, generate images/audio/video, and automate Coze workflows via terminal.

## Overview

This skill enables AI agents to interact with **Coze CLI** (`@coze/cli`), the official command-line tool for Coze/Cozeflow development. It supports project creation, deployment, messaging, multimedia generation, and space management via terminal commands.

**Trigger phrases**: `coze`, `coze cli`, `扣子 CLI`, or any coze command execution.

---

## Installation

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
coze org list
coze org use <organization_id>

coze space list
coze space use <space_id>
```

---

## Core Commands

### Create a Project

```bash
coze code project create --message "创建一个数据分析 Web 应用" --type web
coze code project create --message "创建一个客服机器人" --type agent --wait
```

**Supported types**: `agent`, `workflow`, `app`, `skill`, `web`, `miniprogram`, `assistant`

### Send Message to Project

```bash
coze code message send "修复登录页面的样式问题" -p <project_id>

# With local file context
coze code message send "重构 @src/utils.ts 中的代码" -p <project_id>

# Via pipe
cat error.log | coze code message send "分析这个错误日志" -p <project_id>
```

### Deploy Project

```bash
coze code deploy <project_id>           # deploy
coze code deploy <project_id> --wait    # wait for completion
coze code deploy status <project_id>    # check status
```

### Manage Environment Variables

```bash
coze code env list -p <project_id>                  # dev env
coze code env list -p <project_id> --env prod       # prod env
coze code env set API_KEY xxx -p <project_id>      # set
coze code env delete API_KEY -p <project_id>       # delete
```

### Multimedia Generation

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
```

---

## Environment Variables (CI/CD)

| Variable | Description |
|----------|-------------|
| `COZE_ORG_ID` | Organization ID |
| `COZE_SPACE_ID` | Space ID |
| `COZE_PROJECT_ID` | Project ID (for message commands) |
| `COZE_CONFIG_FILE` | Custom config file path |

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
coze config set base_url https://api.coze.cn
```

---

## Quick Command Templates

```bash
# Full init flow
npm install -g @coze/cli && \
coze auth login --oauth && \
coze org list && coze org use <org_id> && \
coze space list && coze space use <space_id>

# Create + wait + deploy
coze code project create --message "<需求描述>" --type <type> --wait && \
coze code deploy <project_id> --wait && \
coze code preview <project_id>

# Batch query projects
coze code project list --format json | jq '.[] | select(.type=="agent") | .name'
```

---

## File Structure

```
coze-cli/
├── README.md              # This file
├── SKILL.md               # OpenClaw skill definition
└── references/
    └── commands.md        # Full command reference
```

---

## References

- [Coze CLI Official Docs](https://docs.coze.cn/developer_guides/coze_cli)
- [Coze CLI Quickstart](https://docs.coze.cn/developer_guides/coze_cli_quickstart)
