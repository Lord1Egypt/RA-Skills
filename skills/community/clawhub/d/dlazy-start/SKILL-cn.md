---
name: dlazy-start
version: 2.0.0
description: AI 编排器（Claude Code / Cursor / Codex / Copilot）驱动 @dlazy/cli 的快速上手手册。覆盖安装、鉴权、能力探测、调用云端/本地工具、轮询异步任务,以及常见故障恢复。
triggers:
  - dLazy CLI 智能体上手手册
metadata: {"clawdbot":{"emoji":"🎬","requires":{"bins":["npm","npx"]},"install":"npm install -g @dlazy/cli","installAlternative":"npx @dlazy/cli","homepage":"https://dlazy.com","source":"https://github.com/dlazyai/cli","author":"dlazyai","license":"AGPL-3.0-or-later","npm":"https://www.npmjs.com/package/@dlazy/cli","configLocation":"~/.dlazy/config.json","apiEndpoints":["api.dlazy.com","files.dlazy.com"]},"openclaw":{"systemPrompt":"你正在为用户操作 @dlazy/cli。先探测:跑 `dlazy tools list` 看可用工具,`dlazy tools describe <名字>` 看单工具的 input/output schema 和成本。调用形态:`dlazy <工具名> --input @file.json`(或加 `--output json` 拿机读 envelope)。异步任务用 `dlazy status <generateId>` 轮询。需要本地 runtime 时跑 `dlazy doctor remotion --install` 或 `dlazy doctor yt-dlp --install`。在没用 `dlazy tools list` 核实之前,绝不声称某工具存在。"}}
---

# dlazy-start — 智能体上手手册

[English](./SKILL.md) · [中文](./SKILL-cn.md)

给 AI 编排器(Claude Code / Cursor / Codex / Copilot)用的最小契约。CLI 本质是一个工具分发壳:每个注册的云端/本地工具都会变成顶层 subcommand。CLI 不内置项目工作目录或 pipeline 状态机 —— 那些是上层 agent 的概念。

License: AGPL-3.0-or-later。

## 本 skill 教什么

你从鉴权一路驱动 `@dlazy/cli` 到工具调用:

- **云端工具**(40+) —— 图像 / 视频 / 音频 / 文本服务(Seedream / Recraft / MJ / Veo / Seedance / Kling / ElevenLabs / …)
- **本地工具**(40+) —— `state_lock_profile`、`video_compose`、`post_render_gate`、`scene_detect`、`frame_sampler`、`audio_mixer`、`audio_probe`、`transcribe`、`subtitle`、`color_grade`、`extract_segment`、`ffmpeg_run`、…(完整列表跑 `dlazy tools list`)
- **CLI 命令**: `auth`、`doctor`、`tools list`、`tools describe`、`status`,再加上每个注册工具对应的一个顶层 subcommand。

---

## Phase 0 — 安装与鉴权

```bash
# 一次性安装
npm install -g @dlazy/cli

# 登录(设备码流程;远程终端也可用)
dlazy auth login
```

备选鉴权:`dlazy auth set YOUR_API_KEY`,或设 `DLAZY_API_KEY` 环境变量。配置存在 `~/.dlazy/config.json`(Windows:`%USERPROFILE%\.dlazy\`)。

所有命令都接受的全局 flag:`--api-key`、`--base-url`、`--verbose`、`--output <json|url|text>`、`--refresh-manifest`、`-l/--lang <locale>`。

---

## Phase 1 — 能力探测

```bash
dlazy --help                         # 顶层命令面
dlazy tools list                     # 注册工具列表 + 类型 + 成本形态
dlazy tools describe <名字>          # 单工具 input/output JSON schema + hasCosts + 示例
```

可选本地 runtime 需要一次性安装:

```bash
dlazy doctor remotion                # 报 Remotion composer 状态
dlazy doctor remotion --install      # 约 50s,装 bundled composer

dlazy doctor yt-dlp --install        # 用 video_downloader 拉 YouTube 等需要
dlazy doctor yt-dlp --install --proxy http://127.0.0.1:1087
```

部分沙箱通过 `DLAZY_DISABLED_TOOLS=<逗号分隔>` 限制工具面;被禁用的工具不会出现在 `dlazy --help` 里,直接调会返回明确的 `tool_disabled` 错误。

---

## Phase 2 — 调用工具

每个工具都是顶层 subcommand:

```bash
# 命令行 flag(对应 input schema)
dlazy gpt-image-2 --prompt "黄昏中的赛博朋克猫"

# JSON 输入文件(复杂结构推荐)
dlazy video_compose --input @work/compose.json --output json

# 干跑校验(不发远程调用,不扣额度)
dlazy seedance-2-0 --input @plan.json --dry-run
```

每个工具的 help 是从 schema 生成的:

```bash
dlazy <工具名> --help
```

输出模式:

- `--output text`(默认) —— 人读 envelope
- `--output json` —— 每次调用一行 JSON;用 `jq` 解析
- `--output url` —— 单一素材产物时,直接给纯 URL

---

## Phase 3 — 轮询异步云任务

长任务返回 `generateId` 而非素材:

```bash
dlazy status <generateId>
dlazy status <generateId> --output json
```

反复轮询直到 `succeeded`(payload 里带素材 URL)或 `failed`(带 `error.code` + `error.message`)。

---

## Phase 4 — 常见失败恢复

**`dlazy doctor remotion --install` 在 npm install 阶段失败:**
- 检查 Node ≥ 18(`node --version`)。
- 公司代理后面:设 `npm_config_proxy` / `npm_config_https_proxy`。

**`video_downloader` 回复 "Sign in to confirm you're not a bot":**
- YouTube 反爬挑战。input JSON 里加 `"cookies_from_browser": "chrome"`(或 firefox / safari / edge)。

**`video_compose` 返回 "render_runtime=hyperframes not yet implemented":**
- HyperFrames runtime 还没 ship。把 `edit_decisions.render_runtime` 切成 `remotion` 或 `ffmpeg`,再用 `pre_render_validator` 复检。

**ElevenLabs STT 返回空 `words` 数组:**
- 显式传 `timestamps_granularity: "word"`。

**不知道工具成本就要调:**
- `dlazy tools describe <名字>` 暴露 `hasCosts` 和成本形态。先把 estimate 写到本地审计日志,再调工具。

**unknown command 提示:**
- `dlazy <错字>` 返回 `error: unknown command '<typo>'` 加一条编辑距离推荐 "Did you mean …?"。先用 `dlazy tools list` 核实再信。

---

## 反模式

- 没用 `dlazy tools list` 核实就调某工具。
- 凭上次会话记忆写 provider 名,而不重新查注册表(工具会进出)。
- pipeline 中途悄悄换 render runtime(用 `state_lock_profile` + `post_render_gate` parity 校验去管)。
- 付费生成前不播报 provider / model / 成本。

---

## 速查卡

```
安装         npm install -g @dlazy/cli && dlazy auth login
探测         dlazy tools list  |  dlazy tools describe <名字>
本地 runtime  dlazy doctor remotion --install   (或 yt-dlp)
调用         dlazy <工具名> --input @file.json --output json
干跑         dlazy <工具名> --input @file.json --dry-run
轮询         dlazy status <generateId>
帮助         dlazy --help  |  dlazy <工具名> --help
排障         dlazy doctor <目标>  |  dlazy tools describe <名字>
```
