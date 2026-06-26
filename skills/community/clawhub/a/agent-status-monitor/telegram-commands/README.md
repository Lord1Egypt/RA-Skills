# Telegram /agents_monitor 命令

为 Telegram Bot 添加 `/agents_monitor` 命令支持。

## 📋 功能

在 Telegram 中发送 `/agents_monitor` 命令，快速检查本地 AI 开发工具（Claude Code、OpenCode、OpenClaw 等）的运行状态。

## 🔧 安装方式

### 方式 1：通过 Completions 配置（推荐）

Completions 文件已自动创建在：
```
~/.openclaw/workspace/completions/agents_monitor.completion.json
```

重启 Gateway 即可生效：
```bash
openclaw gateway restart
```

### 方式 2：在 BotFather 中注册命令

1. 在 Telegram 中与 [@BotFather](https://t.me/BotFather) 对话
2. 发送 `/mybots` 选择你的 Bot
3. 发送 `/setcommands`
4. 输入命令列表：

```
agents_monitor - 检查本地 AI Agent 运行状态
status - 查看 Agent 状态
```

## 📱 使用方法

在 Telegram 中发送：

```
/agents_monitor
```

或使用触发词：
- "检查 agent 状态"
- "查看 agent 状态"
- "检查 Claude Code 状态"
- "opencode 状态"

## 📊 输出示例

```
🤖 Agent 状态报告

========================================
   Agent Status Monitor
========================================

--- 进程状态 ---
● Claude Code: 🔥 工作中 (2 分钟内有更新) · 13 个会话
● OpenClaw: 🔥 工作中 (2 分钟内有更新) · 3 个会话
● OpenCode: 💤 闲置 (最近无更新) · 1 个会话
○ Cursor IDE: 未运行

========================================
```

## ⚠️ 注意事项

1. **需要执行权限** - 确保脚本有执行权限：
   ```bash
   chmod +x ~/.openclaw/workspace/skills/agent-status-monitor/scripts/*.sh
   ```

2. **超时设置** - 命令执行超时时间为 30 秒，如果检测超时请检查系统负载

3. **仅限私聊** - 建议在私聊中使用，避免在群聊中暴露系统信息

## 🐛 故障排除

**问题：命令无响应**
```bash
# 检查 Gateway 是否运行
openclaw gateway status

# 查看日志
openclaw logs --tail 50
```

**问题：权限错误**
```bash
# 添加执行权限
chmod +x ~/.openclaw/workspace/skills/agent-status-monitor/scripts/*.sh
```

**问题：找不到脚本**
```bash
# 验证脚本路径
ls -la ~/.openclaw/workspace/skills/agent-status-monitor/scripts/
```

## 📄 文件结构

```
telegram-commands/
├── README.md                  # 本文档
├── agents_monitor.plugin.json # 插件配置（备用）
├── index.js                   # 命令处理器（备用）
└── install.js                 # 安装脚本（备用）
```

实际配置位于：
```
~/.openclaw/workspace/completions/agents_monitor.completion.json
```

## 📝 更新日志

- **v1.0** - 初始版本
  - 支持 `/agents_monitor` 命令
  - 通过 completions 系统实现
  - 错误处理和超时保护
