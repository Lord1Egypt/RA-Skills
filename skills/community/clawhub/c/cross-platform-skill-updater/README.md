# Skill Updater

Cross-platform skill updater for AI coding tools and local skill ecosystems.

`Skill Updater` 用于检查并更新本地已安装的 skills，重点覆盖两类常见安装方式：

- `git` 工作树型安装
- `.skill-lock.json` 锁文件驱动的展开式安装

它的设计目标是让同一套检查和更新流程尽可能复用于 Claude Code、Cursor、VS Code Copilot、Gemini CLI、Codex CLI、OpenCode、OpenClaw 等环境。

## Features

- 同时支持 `check` 和 `update` 两个统一入口
- 同时支持 `git` 来源与 `.skill-lock.json` 来源
- 默认扫描当前项目和常见用户级全局目录
- 对 `dirty`、`ahead`、`diverged`、来源异常等风险场景默认只报告不覆盖
- 锁文件型更新前自动备份，并在更新后刷新 `skillFolderHash` 与 `updatedAt`
- 支持结构化 JSON 输出，便于被其他脚本或自动化流程消费
- 支持更短的自然语言触发词，适合 skill 驱动平台直接调用

## Supported Platforms

第一版默认覆盖这些平台常见的 skill 目录约定：

- Claude Code
- Cursor
- VS Code Copilot
- Gemini CLI
- Codex CLI
- OpenCode
- OpenClaw

默认扫描范围包括：

- 当前项目下的 `.claude`、`.cursor`、`.agents`、`.codex`、`.github`、`.gemini`、`.opencode`
- 用户主目录下的对应全局目录
- `~/.openclaw/skills`
- `~/.openclaw/workspace/skills`

## Installation

### Install from ClawHub

```bash
clawhub install cross-platform-skill-updater
```

### Install from GitHub

```bash
git clone https://github.com/ViccWang/skill-updater.git
```

GitHub repository: [ViccWang/skill-updater](https://github.com/ViccWang/skill-updater)

## Quick Start

### CLI

```bash
sh skills/skill-updater/scripts/skill-updater check
sh skills/skill-updater/scripts/skill-updater update
sh skills/skill-updater/scripts/skill-updater check --json
sh skills/skill-updater/scripts/skill-updater check --source pbakaus/impeccable
sh skills/skill-updater/scripts/skill-updater update --path ~/.agents
sh skills/skill-updater/scripts/skill-updater check --path ~/.openclaw/workspace
```

### Natural Language Prompts

这些短句更适合作为 skill 触发词：

- 查 skill 更新
- 更新 skill
- 检查 skills
- 同步 skills
- 看看哪些 skill 要更新
- 更新 GitHub 装的 skills
- 检查 OpenClaw skills
- 检查全局 skills
- 只看有风险的 skill
- 输出 skill 状态 JSON
- 检查 `pbakaus/impeccable`

更明确一点的说法也可以：

- 检查当前项目和全局目录里的 skills
- 更新所有安全可更新的 skills
- 只检查 `~/.agents` 下面的 skills
- 只检查 `~/.openclaw/workspace` 里的 skills
- 只看 `pbakaus/impeccable` 这批 skill 的状态

## How It Works

### `check`

- 只检测，不写本地内容
- 输出每个 skill 的来源、当前状态、当前版本信息和最新版本信息

### `update`

- 只更新“可安全更新”的目标
- `git` 型来源只允许 fast-forward 或精确 tag 切换
- 锁文件型来源默认先备份，再覆盖目录并刷新锁文件字段

## Status Model

常见状态包括：

- `up-to-date`
- `update-available`
- `dirty`
- `ahead`
- `diverged`
- `modified-locally`
- `missing-source`
- `missing-local-skill`
- `lock-invalid`
- `unsupported`
- `update-failed`

默认策略是：遇到风险状态只报告，不强制覆盖。

## Limitations

- 第一版不做后台自动更新
- 第一版不内置定时任务
- 第一版只正式支持 `.skill-lock.json` 这一类锁文件格式
- 对没有来源记录的普通目录，不会做猜测式更新
- 如果本机网络、代理或 GitHub 访问异常，会返回可解释错误而不是静默跳过

## Development

### Run Tests

```bash
python3 -m unittest skills/skill-updater/tests/test_skill_updater.py
```

### Project Layout

```text
skill-updater/
  SKILL.md
  README.md
  LICENSE
  agents/openai.yaml
  scripts/skill-updater
  scripts/skill_updater.py
  tests/test_skill_updater.py
```

## License

Released under the [MIT License](./LICENSE).
