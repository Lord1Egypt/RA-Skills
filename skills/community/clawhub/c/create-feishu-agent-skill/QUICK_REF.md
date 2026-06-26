# 飞书 Agent 快速参考卡

## 🚀 快速创建命令

```bash
# 使用脚本快速创建
~/.openclaw/workspace/skills/create-feishu-agent/create-feishu-agent.sh \
  <agent_name> "<显示名称>" <app_id> <app_secret>

# 示例
~/.openclaw/workspace/skills/create-feishu-agent/create-feishu-agent.sh \
  tech_expert "技术专家" cli_xxx xxxsecret
```

## 📁 目录结构

```
~/.openclaw/workspace/agents/<agent_name>/
├── SOUL.md       # ⭐ 人设文件（必需）
├── AGENTS.md     # 职责定义
├── MEMORY.md     # 长期记忆
└── memory/       # 记忆存储目录
```

## ⚙️ 关键配置项

| 配置项 | 说明 | 推荐值 |
|--------|------|--------|
| `groupPolicy` | 群聊策略 | `open` |
| `requireMention` | 是否需要@ | `false` |
| `connectionMode` | 连接模式 | `websocket` |

## 🔑 飞书权限

**必需权限：**
- `im:message` - 消息
- `im:message.group_msg` - 群消息
- `im:chat:read` - 读取群聊

**可选权限：**
- `bitable:app` - 多维表格
- `drive:file` - 云文档

## 📡 飞书事件订阅

**必需事件：**
- `im.message.receive_v1` - 接收消息

## 🔄 常用命令

```bash
# 重启 Gateway
openclaw gateway restart

# 查看 Agent 列表
openclaw agents list

# 查看日志
tail -f /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log | grep <agent_name>

# 检查配置
openclaw doctor
```

## ❌ 常见问题

| 问题 | 解决方案 |
|------|----------|
| 群消息收不到 | 检查 groupPolicy/requireMention 设置 |
| 机器人不回复 | 检查 SOUL.md 人设、模型配置 |
| 配置不生效 | 重启 gateway: `openclaw gateway restart` |

## 📝 SOUL.md 模板

```markdown
# SOUL.md - <名称>

## Core Truths
- 原则1
- 原则2

## What You Do
- 职责1
- 职责2

## Vibe
性格描述
```

---

*配合 SKILL.md 详细文档使用*
