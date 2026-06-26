# CC-Bridge — OpenClaw ↔ Claude Code CLI Bridge

[中文](#中文文档) | [English](#english-documentation)

---

## 中文文档

### 简介

**CC-Bridge** 是一个 OpenClaw Skill，让你通过 QQ、Telegram 等任意聊天渠道，远程操作一个**真正的、交互式的 Claude Code 终端会话**。

不是简单的 API 调用或任务委派——而是像你坐在电脑前打开终端输入 `claude` 一样的完整体验。

### 工作原理

```
你的手机 (QQ/Telegram/...)
     │
     ▼
  OpenClaw Agent (接收消息)
     │
     ▼
  CC-Bridge Skill (tmux 桥接)
     │
     ▼
  Claude Code CLI (真实终端会话)
     │
     ▼
  CC-Bridge (捕获输出 → 返回给你)
```

核心技术：
- **tmux** 维持持久化终端会话（关掉手机对话也不会断）
- **pipe-pane** 实时监控输出变化
- **capture-pane** 获取干净的渲染文本（无 ANSI 转义码）
- **send-keys** 模拟键盘输入（包括方向键导航审批菜单）

### 前置条件

| 依赖 | 说明 |
|------|------|
| [OpenClaw](https://github.com/nicepkg/openclaw) | v2026.3.0+ |
| [Claude Code CLI](https://docs.anthropic.com/en/docs/claude-code) | 已安装并登录（`claude` 命令可用） |
| tmux | macOS: `brew install tmux`，Linux: `apt install tmux` |
| bash | 4.0+（macOS 自带 zsh 可用，脚本指定 bash） |

### 安装

将 `cc-bridge` 目录放到 OpenClaw 的 skills 目录下：

```bash
# 方式 1：直接克隆
git clone https://github.com/your-username/cc-bridge.git \
  ~/.openclaw/workspace/skills/cc-bridge

# 方式 2：手动复制
cp -r cc-bridge ~/.openclaw/workspace/skills/
```

验证安装：
```bash
openclaw skills list
# 应该看到: ✓ ready │ 📦 cc-bridge
```

### 快速开始

| 你发送 | 效果 |
|--------|------|
| `启动cc` | 启动 Claude Code 会话 |
| 任意消息 | 转发给 Claude Code |
| `y` / `1` / `是` | 同意 CC 的工具审批 |
| `n` / `3` / `否` | 拒绝 CC 的工具审批 |
| `/plan` | 切换 CC 到 Plan 模式 |
| `/model sonnet` | 切换 CC 的模型 |
| `关闭cc` | 关闭会话 |

### 完整命令列表

| 命令 | 说明 |
|------|------|
| `启动cc` / `开启cc` / `/cc start` | 启动新的 CC 会话 |
| `关闭cc` / `退出cc` / `/cc stop` | 关闭会话 |
| `重启cc` / `/cc restart` | 重启会话 |
| `cc状态` / `/cc status` | 查看会话状态 |
| `/cc peek` | 查看终端原始画面（最近50行） |
| `/cc history [N]` | 查看最近 N 行对话历史 |
| `/plan`、`/model`、`/compact` 等 | CC 自身的斜杠命令，直接透传 |

### 审批操作

当 CC 需要执行命令、读写文件等需要权限的操作时，会弹出审批菜单。你只需回复：

| 你的回复 | 含义 |
|----------|------|
| `y` / `是` / `好` / `1` / `同意` | 同意（仅本次） |
| `2` / `允许` / `一直允许` | 允许（本项目永久） |
| `n` / `否` / `不` / `3` / `拒绝` | 拒绝 |
| `取消` / `cancel` | 取消操作 |

### 长任务处理

对于大型任务（如 "重构整个项目"），bridge 会自动使用 5 分钟超时。如果超时后 CC 仍在工作：

1. 发 `/cc peek` 查看当前进度
2. 发 `/cc history 200` 查看完整历史
3. CC 完成后再发消息会获取新的输出

### 功能覆盖对比

| Claude Code 原生功能 | CC-Bridge 支持 | 说明 |
|---------------------|:--------------:|------|
| 发送消息/提问 | ✅ | 完整支持 |
| 代码编辑/生成 | ✅ | 完整支持 |
| 文件读写 | ✅ | 通过审批后完整支持 |
| 命令行执行 | ✅ | 通过审批后完整支持 |
| 工具审批 (Yes/No/Allow) | ✅ | 方向键模拟 TUI 菜单 |
| 所有斜杠命令 (`/plan` `/model` `/diff` `/vim` ...) | ✅ | 全部透传 |
| 权限模式切换 (Shift+Tab) | ✅ | `key shift+tab` |
| 模型快速切换 (Alt+P) | ✅ | `key alt+p` |
| 扩展思考切换 (Alt+T) | ✅ | `key alt+t` |
| Ctrl+C 中断 | ✅ | `interrupt` 命令 |
| Ctrl+B 后台任务 | ✅ | `key ctrl+b` |
| Ctrl+L 清屏 | ✅ | `key ctrl+l` |
| Esc+Esc 回退/检查点 | ✅ | `key esc+esc` |
| 方向键/Tab/Enter/Space | ✅ | `key` 命令 |
| 多文件编辑 | ✅ | CC 原生能力 |
| Git 操作 | ✅ | CC 原生能力 |
| MCP 服务器 | ✅ | CC 自身配置 |
| Bash 模式 (`!` 前缀) | ✅ | 通过 `send` 直接发送 |
| 实时流式输出 | ⚠️ | 批量轮询（~2.4s 延迟），非逐字流式 |
| 多行输入 | ⚠️ | 可用 `\` + Enter，但无 Shift+Enter |
| `@` 文件引用补全 | ❌ | 无法触发终端内补全菜单 |
| 图片粘贴/查看 | ❌ | 文本通道限制 |
| 视觉 diff 渲染/颜色 | ❌ | 纯文本输出，无颜色高亮 |

### 技术细节

- tmux 会话名：`ccb_<session_id>`（自动清理特殊字符）
- 滚动缓冲区：50,000 行（长对话不丢内容）
- 输出检测：日志文件大小连续稳定 3 次（间隔 0.8s）视为完成
- 默认超时：90 秒，`--long` 模式：300 秒
- Claude Code 二进制：`$CLAUDE_BIN`（默认 `~/.local/bin/claude`）

### 常见问题

**Q: 需要 Anthropic API Key 吗？**
A: 不需要。CC-Bridge 使用你本地已登录的 Claude Code CLI，走 OAuth 认证。

**Q: 可以同时开多个会话吗？**
A: 可以。每个 OpenClaw 渠道（QQ 私聊/群/Telegram 对话）各自独立。

**Q: CC 断了怎么办？**
A: 发 `重启cc` 即可。

**Q: 支持 Windows 吗？**
A: 目前仅支持 macOS 和 Linux（依赖 tmux）。Windows 需要 WSL。

---

## English Documentation

### Overview

**CC-Bridge** is an OpenClaw Skill that lets you operate a **real, interactive Claude Code terminal session** remotely through any chat channel — QQ, Telegram, Discord, etc.

This is not a simple API call or task delegation — it's the full Claude Code CLI experience, as if you were sitting at your computer typing `claude` in a terminal.

### How It Works

```
Your Phone (QQ/Telegram/...)
     │
     ▼
  OpenClaw Agent (receives message)
     │
     ▼
  CC-Bridge Skill (tmux bridge)
     │
     ▼
  Claude Code CLI (real terminal session)
     │
     ▼
  CC-Bridge (captures output → sends back to you)
```

Core technology:
- **tmux** maintains persistent terminal sessions (survives disconnects)
- **pipe-pane** monitors output changes in real-time
- **capture-pane** captures clean rendered text (no ANSI escape codes)
- **send-keys** simulates keyboard input (including arrow-key navigation for approval menus)

### Prerequisites

| Dependency | Notes |
|-----------|-------|
| [OpenClaw](https://github.com/nicepkg/openclaw) | v2026.3.0+ |
| [Claude Code CLI](https://docs.anthropic.com/en/docs/claude-code) | Installed and logged in (`claude` command available) |
| tmux | macOS: `brew install tmux`, Linux: `apt install tmux` |
| bash | 4.0+ |

### Installation

Place the `cc-bridge` directory in OpenClaw's skills directory:

```bash
# Option 1: Clone directly
git clone https://github.com/your-username/cc-bridge.git \
  ~/.openclaw/workspace/skills/cc-bridge

# Option 2: Manual copy
cp -r cc-bridge ~/.openclaw/workspace/skills/
```

Verify installation:
```bash
openclaw skills list
# Should show: ✓ ready │ 📦 cc-bridge
```

### Quick Start

| You Send | Effect |
|----------|--------|
| `启动cc` (Start CC) | Launch Claude Code session |
| Any message | Forwarded to Claude Code |
| `y` / `1` | Approve CC's tool request |
| `n` / `3` | Deny CC's tool request |
| `/plan` | Switch CC to Plan mode |
| `/model sonnet` | Switch CC's model |
| `关闭cc` (Stop CC) | Close session |

### Full Command Reference

| Command | Description |
|---------|-------------|
| `启动cc` / `/cc start` | Start a new CC session |
| `关闭cc` / `/cc stop` | Stop the session |
| `重启cc` / `/cc restart` | Restart the session |
| `cc状态` / `/cc status` | Check session status |
| `/cc peek` | View raw terminal screen (last 50 lines) |
| `/cc history [N]` | View last N lines of conversation history |
| `/plan`, `/model`, `/compact`, etc. | CC's own slash commands, passed through directly |

### Approval Handling

When CC needs permission to execute commands, read/write files, etc., an approval menu appears. Simply reply:

| Your Reply | Meaning |
|-----------|---------|
| `y` / `1` / `yes` | Approve (this time only) |
| `2` | Allow (permanently for this project) |
| `n` / `3` / `no` | Deny |
| `cancel` / `esc` | Cancel |

### Long Task Handling

For large tasks (e.g., "refactor the entire project"), the bridge automatically uses a 5-minute timeout. If CC is still working after timeout:

1. Send `/cc peek` to check current progress
2. Send `/cc history 200` to view full history
3. Send another message after CC finishes to get new output

### Feature Coverage

| Claude Code Native Feature | CC-Bridge Support | Notes |
|---------------------------|:-----------------:|-------|
| Send messages / ask questions | ✅ | Full support |
| Code editing / generation | ✅ | Full support |
| File read/write | ✅ | Full support after approval |
| Command execution | ✅ | Full support after approval |
| Tool approval (Yes/No/Allow) | ✅ | Arrow-key TUI menu simulation |
| All slash commands (`/plan` `/model` `/diff` `/vim` ...) | ✅ | Full passthrough |
| Permission mode cycling (Shift+Tab) | ✅ | `key shift+tab` |
| Quick model switch (Alt+P) | ✅ | `key alt+p` |
| Extended thinking toggle (Alt+T) | ✅ | `key alt+t` |
| Ctrl+C interrupt | ✅ | `interrupt` command |
| Ctrl+B background tasks | ✅ | `key ctrl+b` |
| Ctrl+L clear screen | ✅ | `key ctrl+l` |
| Esc+Esc rewind/checkpoint | ✅ | `key esc+esc` |
| Arrow keys / Tab / Enter / Space | ✅ | `key` command |
| Multi-file editing | ✅ | CC native capability |
| Git operations | ✅ | CC native capability |
| MCP servers | ✅ | CC's own config |
| Bash mode (`!` prefix) | ✅ | Send directly via `send` |
| Real-time streaming output | ⚠️ | Batch polling (~2.4s delay), not character-by-character |
| Multi-line input | ⚠️ | `\` + Enter works, no Shift+Enter |
| `@` file mention autocomplete | ❌ | Cannot trigger terminal autocomplete menu |
| Image paste / viewing | ❌ | Text channel limitation |
| Visual diff rendering / colors | ❌ | Plain text output, no color highlighting |

### Technical Details

- tmux session name: `ccb_<session_id>` (special characters auto-sanitized)
- Scrollback buffer: 50,000 lines (no content loss in long sessions)
- Output detection: log file size stable for 3 consecutive checks (0.8s interval)
- Default timeout: 90s, `--long` mode: 300s
- Claude Code binary: `$CLAUDE_BIN` (defaults to `~/.local/bin/claude`)

### FAQ

**Q: Do I need an Anthropic API Key?**
A: No. CC-Bridge uses your locally logged-in Claude Code CLI with OAuth authentication.

**Q: Can I run multiple sessions?**
A: Yes. Each OpenClaw channel (QQ DM/group, Telegram chat) is independent.

**Q: What if CC crashes?**
A: Send `重启cc` (or restart via `/cc restart`).

**Q: Windows support?**
A: Currently macOS and Linux only (requires tmux). Windows users need WSL.

---

## Project Structure

```
cc-bridge/
├── SKILL.md              # Skill metadata & agent instructions
├── LICENSE               # MIT License
├── README.md             # This file
├── scripts/
│   └── cc-bridge.sh      # Core bridge script (start/send/approve/stop/...)
├── references/
│   └── usage.md          # User-facing quick reference (Chinese)
└── docs/                 # Additional documentation
```

## License

MIT License — see [LICENSE](./LICENSE) for details.
