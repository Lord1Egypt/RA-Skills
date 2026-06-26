# Agent Status Monitor

监控本地 AI 开发工具 Agent（Claude Code、OpenCode、OpenClaw、Cursor 等）的运行状态和活动状态。

[English](README.md) | 简体中文

![agent-status-monitor](https://socialify.git.ci/willin/agent-status-monitor/image?description=1&forks=1&name=1&owner=1&pattern=Circuit+Board&stargazers=1&theme=Auto)


## 🚀 快速开始

### 安装方式

#### 方式 1：通过 ClawHub 安装

```bash
clawhub install agent-status-monitor
```

#### 方式 2：使用 npx 安装

```bash
npx skills add willin/agent-status-monitor
```

#### 方式 3：从 GitHub 克隆或下载

```bash
# 克隆仓库
git clone https://github.com/willin/agent-status-monitor.git
cd agent-status-monitor

# 复制到 OpenClaw workspace
cp -r . ~/.openclaw/workspace/skills/agent-status-monitor/

# 添加执行权限
chmod +x ~/.openclaw/workspace/skills/agent-status-monitor/scripts/*.sh
```

### 使用方法

**方法 1：运行主脚本**
```bash
~/.openclaw/workspace/skills/agent-status-monitor/scripts/check-agents.sh
```

**方法 2：在 OpenClaw 中触发**

> ⚠️ **注意**：避免单独使用"检查 agent 状态"，这可能会触发 OpenClaw 内置的会话状态功能。

```
agents_monitor
检查 Claude Code 状态
查看 opencode 是否在运行
监控开发工具
agent 监控
```

**方法 3：单独检查某个 Agent**
```bash
./scripts/check-claude-code.sh    # 检查 Claude Code
./scripts/check-openclaw.sh       # 检查 OpenClaw
./scripts/check-opencode.sh       # 检查 OpenCode
./scripts/check-cursor.sh         # 检查 Cursor IDE
```

## 📊 输出示例

```
========================================
   Agent Status Monitor
========================================

--- 进程状态 ---
--- Claude Code 状态 ---
● Claude Code: 🔥 工作中 (2 分钟内有更新) · 13 个会话

--- OpenClaw 状态 ---
● OpenClaw: 🔥 工作中 (2 分钟内有更新) · 3 个会话

--- OpenCode 状态 ---
● OpenCode: 💤 闲置 (未使用) · 1 个会话

--- Cursor IDE 状态 ---
○ Cursor IDE: 未运行

========================================
```

## 📋 状态说明

| 状态 | 图标 | 含义 |
|------|------|------|
| 工作中 | 🔥 | 2 分钟内有会话文件更新 |
| 等待中 | ⏳ | 10 分钟内有更新（可能在思考/等待 API） |
| 闲置 | 💤 | 超过 10 分钟无更新，或未使用 |
| 未运行 | ○ | 进程不存在 |

## 🔧 支持的 Agent

| Agent | 进程检测 | 会话检测 | 会话目录 |
|-------|----------|----------|----------|
| Claude Code | ✅ | ✅ | `~/.claude/projects/` |
| OpenClaw | ✅ | ✅ | `~/.openclaw/agents/` |
| OpenCode | ✅ | ✅ | `~/.local/state/opencode/` |
| Cursor IDE | ✅ | ❌ | N/A |

## 📁 项目结构

```
agent-status-monitor/
├── README.md                       # 英文文档
├── README.zh-CN.md                 # 中文文档（本文件）
├── LICENSE                         # MIT License
├── SKILL.md                        # OpenClaw 技能定义
├── scripts/
│   ├── check-agents.sh             # 主脚本（调用所有检测）
│   ├── check-claude-code.sh        # Claude Code 检测
│   ├── check-openclaw.sh           # OpenClaw 检测
│   ├── check-opencode.sh           # OpenCode 检测
│   └── check-cursor.sh             # Cursor IDE 检测
└── references/
    └── agent-commands.md           # 各 Agent 命令参考
```

## 🛠️ 自定义扩展

### 添加新的 Agent 检测

在 `scripts/` 目录创建新脚本：

```bash
#!/bin/bash
# check-your-agent.sh
SESSIONS_DIR="$HOME/.your-agent/sessions"
# ... 实现检测逻辑
```

然后更新 `check-agents.sh` 调用它。

### 调整时间阈值

修改各个脚本中的时间判断：
- `mmin -2` - 工作中阈值（默认 2 分钟）
- `mmin -10` - 等待中阈值（默认 10 分钟）

## ⚠️ 注意事项

1. **仅本地检测** - 只检测本地运行的 Agent，不涉及云端服务
2. **只读操作** - 不会修改或控制任何 Agent
3. **文件系统依赖** - 基于会话文件修改时间，需要读取权限
4. **误报排除** - 已排除 macOS 系统进程（如 CursorUIViewService）
5. **触发词** - 使用特定触发词如 `agents_monitor` 或"检查 Claude Code 状态"，避免与 OpenClaw 内置会话状态混淆

## ❓ 常见问题

**Q: 为什么说"检查 agent 状态"显示的是 OpenClaw 会话信息？**

A: OpenClaw 内置了会话状态功能。要使用本技能，请使用特定触发词：
- ✅ `agents_monitor`
- ✅ "检查 Claude Code 状态"
- ✅ "opencode 在运行吗"
- ❌ "检查 agent 状态"（会触发内置功能）

## 🐛 故障排除

**问题：显示"未运行"但 Agent 实际在运行**
```bash
# 手动检查进程
ps aux | grep -i "<agent 名>" | grep -v grep

# 检查会话目录是否存在
ls -la ~/.claude/projects/  # Claude Code 示例
```

**问题：脚本没有执行权限**
```bash
chmod +x ~/.openclaw/workspace/skills/agent-status-monitor/scripts/*.sh
```

## 📝 更新日志

- **v1.0** - 初始版本
  - 支持 Claude Code、OpenCode、OpenClaw、Cursor IDE
  - 基于会话文件修改时间判断活动状态
  - 模块化脚本设计，易于扩展

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件
