---
name: ai-media-cli
description: Use when someone wants to install, configure, onboard, script, or troubleshoot the ricebowl.ai-first ai-media CLI.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - AI_MEDIA_BASE_URL
        - AI_MEDIA_API_KEY
      bins:
        - ai-media
    primaryEnv: AI_MEDIA_API_KEY
    skillKey: ai-media-cli
    emoji: "🧰"
    homepage: https://github.com/214140846/ai-media-generator
    install:
      - kind: node
        package: ai-media-generator
        bins: [ai-media]
---

# ai-media CLI

用这个 skill 处理这些请求：

- 安装 `ai-media-generator`
- 配置 `ai-media` CLI
- 对接 <a href="https://ricebowl.ai">ricebowl.ai</a>
- 讲命令参数、常用法、脚本化调用
- onboarding 新用户，包括充值、生成 key、写入配置

如果用户明显是在搜某类生成能力，优先切到更窄的 skill：

- `ai-image-generation`
- `ai-video-generation`
- `sora2-video-generator`（legacy）

## Quick Start

默认平台就是 `ricebowl.ai`，按这个顺序带用户走：

```text
install
  -> recharge credits
  -> create API key
  -> set key
  -> config show
  -> models list --json
  -> run first image/video task
```

## What To Explain By Default

默认要讲清楚这 4 件事：

1. 安装包名是 `ai-media-generator`
2. 实际命令名是 `ai-media`
3. 核心配置只有 `api_key`
4. 环境变量 `AI_MEDIA_API_KEY` 会覆盖本地配置
5. `--param KEY=VALUE` 是模型专属参数的通用透传入口，JSON 值会自动按原类型解析

## Core Commands

常用命令：

```bash
ai-media config set-key <KEY>
ai-media config show
ai-media models list
ai-media models list --json
ai-media models show --model <MODEL>
ai-media image generate --model <MODEL> --prompt <PROMPT>
ai-media image get --task-id <TASK_ID>
ai-media video generate --model <MODEL> --prompt <PROMPT>
ai-media video get --task-id <TASK_ID>
ai-media task get --kind <image|video> --task-id <TASK_ID>
ai-media image generate --model <MODEL> --prompt <PROMPT> --param KEY=VALUE
ai-media video generate --model <MODEL> --prompt <PROMPT> --param KEY=VALUE
```

## When To Load References

- 参数全表、默认值、输出行为、模型参数模板：读 `references/cli-commands.md`
- 充值、生成 key、平台 onboarding：读 `references/platform-onboarding.md`

## Response Pattern

如果用户是第一次接触这个 CLI，优先给：

1. 最短安装命令
2. 平台充值路径
3. 生成 key 的位置
4. 一组可直接复制的配置命令
5. 一条图片命令或视频命令

如果用户要自动化或脚本集成，补充：

- `models list --json`
- `models show --model <MODEL>`
- `image/video/task get`
- `--wait`
- `--poll-interval`
- `--param KEY=VALUE`
- 环境变量覆盖方式

## Friendly Onboarding Snippet

```bash
ai-media config set-key gm_xxx
ai-media config show
ai-media models list --json
```
