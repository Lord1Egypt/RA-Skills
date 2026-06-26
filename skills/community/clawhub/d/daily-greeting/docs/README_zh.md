# Daily Greeting Skill

> [!TIP]
> 给你的 OpenClaw Agent 赋予个性！它们每天早上自动向用户发送个性化问候。

<!-- Language Navigation -->
[English](../README.md) | [中文](README_zh.md)

---

## 功能介绍

你的 Agent 和你一起醒来！每天早上（或按你的计划），每个 Agent 都会向绑定频道发送个性化问候：

- 🤖 **Agent 个性** - 每条问候都符合 Agent 的人设
- 🌐 **用户语言** - 使用用户偏好的语言发送问候
- 📊 **相关信息** - 根据 Agent 角色提供状态更新、进度、提醒等

## 功能特性

| | |
|--------|---------|
| ⚡ **自动触发** | 支持启动时（BOOT.md）或定时（OpenClaw cron） |
| 🛡️ **无重复** | 状态持久化防止重复发送 |
| 🌐 **任意频道** | Discord、飞书、Telegram 等 |
| 🎨 **角色驱动** | 每个 Agent 有自己的问候风格 |
| 🧹 **干净卸载** | 完全清除，无残留文件 |

## 快速开始

### 一键安装

将以下命令发送给 OpenClaw：

```
请执行 daily-greeting 安装指南：
https://raw.githubusercontent.com/shz2050/daily-greeting/main/guide.md
```

OpenClaw 会自动处理一切。

### 手动安装

```bash
# 克隆仓库
git clone https://github.com/shz2050/daily-greeting.git

# 复制到 OpenClaw 技能目录
cp -r daily-greeting ~/.openclaw/skills/daily-greeting

# 赋予脚本执行权限
chmod +x ~/.openclaw/skills/daily-greeting/scripts/greeting.sh
```

## 自动触发配置

BOOT.md（启动时）和 OpenClaw cron（定时）默认同时启用。状态检查防止重复发送。

**BOOT.md（启动时触发）：**

```bash
# 找到工作区
ls ~/.openclaw/workspace/

# 创建/编辑 BOOT.md
nano ~/.openclaw/workspace/BOOT.md
```

添加以下内容：

````markdown
# BOOT.md

<!-- daily-greeting:start -->
请执行每日问候：
```bash
bash ~/.openclaw/skills/daily-greeting/scripts/greeting.sh run
```

执行后，仅回复：`NO_REPLY`。
<!-- daily-greeting:end -->
````

**OpenClaw Cron（定时触发）：**

```bash
openclaw cron add \
  --name "daily-greeting" \
  --cron "0 9 * * 1-5" \
  --session isolated \
  --message "bash ~/.openclaw/skills/daily-greeting/scripts/greeting.sh run" \
  --wake now
```

默认：每个工作日早上 9 点

查看/修改：
```bash
openclaw cron list
```

**记录安装信息：**

```bash
bash ~/.openclaw/skills/daily-greeting/scripts/greeting.sh install ~/.openclaw/workspace/BOOT.md
```

## 常用命令

```bash
# 手动执行问候
bash ~/.openclaw/skills/daily-greeting/scripts/greeting.sh run

# 查看状态
bash ~/.openclaw/skills/daily-greeting/scripts/greeting.sh status

# 重置状态（允许重新执行）
bash ~/.openclaw/skills/daily-greeting/scripts/greeting.sh reset

# 卸载
bash ~/.openclaw/skills/daily-greeting/scripts/greeting.sh uninstall
```

## 配置

编辑 `config.json` 自定义行为：

```json
{
  "enabled": true,
  "workingDaysOnly": true,
  "delayMs": 3000,
  "excludeAgents": ["main"],
  "triggerMessage": "Please send a daily greeting to your bound channel. Requirements: 1) Compose the greeting in the user's preferred language (infer from channel history and user context); 2) Include relevant status information based on your agent role and ongoing tasks with the user (e.g., if you're a todo agent, summarize progress and today's priorities; if you're a diary agent, mention ongoing projects); 3) Use message tool to send to your bound channel; 4) End conversation after sending"
}
```

| 配置项 | 类型 | 默认值 | 描述 |
|--------|------|--------|------|
| `enabled` | boolean | `true` | 启用/禁用技能 |
| `workingDaysOnly` | boolean | `true` | 仅在工作日触发（周一至周五） |
| `delayMs` | number | `3000` | 执行前延迟（毫秒） |
| `excludeAgents` | array | `["main"]` | 排除的 Agent |
| `triggerMessage` | string | (见上方) | 发送给每个 Agent 的消息 |

## 工作原理

```
Gateway 启动 / Cron 触发
    ↓
greeting.sh 运行
    ↓
读取配置 → 检查工作日 → 检查今日是否已执行
    ↓
对每个绑定的 Agent：
    - Agent 发送个性化问候到绑定频道
    ↓
状态保存到 data/state.json
```

## 卸载

```bash
bash ~/.openclaw/skills/daily-greeting/scripts/greeting.sh uninstall
```

这将移除：
1. BOOT.md 条目（仅标记部分）
2. OpenClaw cron 任务
3. 技能目录

## 环境要求

- OpenClaw Gateway
- Bash 4.0+
- jq（JSON 解析）

## 许可证

MIT 许可证 - 详见 LICENSE 文件。

## 支持

如有问题，请提交 GitHub issue。
