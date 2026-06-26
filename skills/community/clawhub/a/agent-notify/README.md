# Agent Notify

> Cross-platform notification sound & taskbar flash for AI coding agents (Claude Code, OpenClaw, Codex, Kiro, Cursor, etc.)
>
> AI 编码 Agent 跨平台提示音与任务栏闪烁通知（支持 Claude Code、OpenClaw、Codex、Kiro、Cursor 等）

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-brightgreen.svg)]()

---

## The Problem / 痛点

When using AI coding agents, you switch to other windows while waiting. Without notifications, you keep checking back manually.

使用 AI 编码 Agent 时，等待期间你会切到其他窗口。没有通知，只能反复手动查看。

## The Solution / 解决方案

**Agent Notify** adds sound alerts + visual notifications to your AI coding agent. You always know when it needs you. Supports Claude Code, OpenClaw, Codex, Kiro, Cursor, and more.

**Agent Notify** 为你的 AI 编码 Agent 添加声音提醒 + 视觉通知，让你随时知道它何时需要你。支持 Claude Code、OpenClaw、Codex、Kiro、Cursor 等。

---

## Demo

![Demo](assets/demo-placeholder.png)
<!-- TODO: Replace with actual demo GIF -->

---

## Features / 功能

| Feature | Windows | macOS | Linux |
|---------|---------|-------|-------|
| Confirmation sound | SystemSounds | afplay | paplay/aplay |
| Completion sound | SystemSounds | afplay | paplay/aplay |
| Taskbar flash | FlashWindowEx | Dock bounce | notify-send |
| Custom sounds | .wav | .aiff/.mp3 | .oga/.wav |
| Configurable | Yes | Yes | Yes |

---

## Install / 安装

```bash
git clone https://github.com/Miluer-tcq/agent-notify.git
cp -r agent-notify ~/.claude/skills/
```

Then type in your agent / 然后在你的 Agent 中输入:

```
提示音
```
or / 或
```
notify
```

---

## Setup Modes / 配置模式

### 1. Quick Setup / 一键配置 (Recommended)

Auto-detect OS, install defaults. Done in seconds.

自动检测系统，使用默认设置，秒级完成。

### 2. Custom Setup / 自定义配置

Choose trigger events, sounds, flash count interactively.

交互式选择触发事件、音效、闪烁次数。

---

## Trigger Words / 触发词

**Chinese:** `提示音` `通知提醒` `声音提醒` `消息提醒` `任务提醒` `完成提醒` `配置提示音` `设置提示音` `开启提示音` `关闭提示音` `通知声音`

**English:** `notify` `notification sound` `alert sound` `sound alert` `claude code notify` `setup notification` `configure notify` `enable notification` `disable notification` `task alert` `completion sound` `bell` `beep` `sound notification` `notification setup`

---

## Configuration / 配置

Config file: `$AGENT_HOME/notify-config.json` (e.g., `~/.claude/notify-config.json`)

```json
{
  "hooks": {
    "Notification": { "enabled": true, "type": "confirm" },
    "Stop": { "enabled": true, "type": "done" }
  },
  "sounds": {
    "confirm": "",
    "done": "",
    "error": ""
  },
  "taskbar": {
    "flashCount": 5,
    "enabled": true
  }
}
```

### Custom Sounds / 自定义音效

```json
{
  "sounds": {
    "confirm": "/path/to/confirm.wav",
    "done": "/path/to/done.wav"
  }
}
```

---

## Uninstall / 卸载

Type / 输入: `关闭提示音` or `disable notification`

---

## Troubleshooting / 常见问题

| Issue | Solution |
|-------|----------|
| No sound (Windows) | Check system volume & sound scheme |
| No sound (macOS) | Check volume & notification permissions |
| No sound (Linux) | `sudo apt install pulseaudio-utils libnotify-bin` |
| Hooks not working | Restart your agent after configuration |

---

## Project Structure / 项目结构

```
agent-notify/
+-- skill.md                 # Skill definition
+-- scripts/
|   +-- notify-windows.ps1   # Windows notification
|   +-- notify-macos.sh      # macOS notification
|   +-- notify-linux.sh      # Linux notification
+-- config/
|   +-- default.json         # Default config
+-- publish/                  # Platform publish configs
+-- assets/                   # Demo screenshots
+-- README.md
+-- LICENSE                   # GPL-3.0
```

---

## License / 许可证

[GPL-3.0](LICENSE)

## Author / 作者

**Miluer-tcq** — [GitHub](https://github.com/Miluer-tcq)
