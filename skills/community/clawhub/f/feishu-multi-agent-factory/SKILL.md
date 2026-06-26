---
name: feishu-multi-agent-factory
description: "批量配置 OpenClaw 多 agent + 飞书 channel。当用户说「添加 agent」「新建 agent」「配置飞书」「批量创建 agent」「添加新机器人」时触发。通过对话引导收集信息，一键写入 openclaw.json 并初始化工作区。"
metadata:
---

# Agent Factory — 多 agent 批量配置向导

通过对话快速创建新 agent，自动完成所有配置：
- 写入 `openclaw.json`（agents / feishu accounts / bindings）
- 创建 workspace 目录 + IDENTITY.md 等基础文件
- 创建 agentDir + defaults.json + auth-profiles.json

## 核心脚本

```
~/.openclaw/workspace/skills/feishu-multi-agent-factory/scripts/setup_agents.py
```

## 对话示例

**用户说：**
```
帮我创建2个 agent：
1. id: painter，图片处理专家🌞，飞书 AppId: <PAINTER_APP_ID>，Secret: <PAINTER_SECRET>
2. id: take，行业资讯抓手👋，飞书 AppId: <TAKE_APP_ID>，Secret: <TAKE_SECRET>
```

**你的回应（先 dry-run 确认）：**
```
好的，我来预览一下即将创建的配置：

▶ 🌞 图片处理专家 (id: painter)
  • workspace → ~/.openclaw/workspace-painter/
  • agentDir  → ~/.openclaw/agents/painter/agent/
  • 飞书 account 'painter' 已配置

▶ 👋 行业资讯抓手 (id: take)
  • workspace → ~/.openclaw/workspace-take/
  • agentDir  → ~/.openclaw/agents/take/agent/
  • 飞书 account 'take' 已配置

确认执行吗？
```

**用户确认后执行，回应：**
```
✅ 创建: 2 个
新 agents: painter, take

请运行 `openclaw configure` 为各 agent 配置 API key。
已重启 gateway，两个飞书机器人上线后即可收发消息。
```

---

## 安全说明

- **App Secret 不回显**：收到 Secret 后不在对话中重复展示，确认预览时只显示 AppId
- **Secret 脱敏输出**：脚本日志只显示 Secret 前 4 位（如 `R1T8****`）
- **凭据仅写入本地**：所有凭据只写入 `~/.openclaw/openclaw.json`，不上传、不外传
- **id 严格校验**：只允许小写字母、数字、连字符，防止路径穿越攻击

## 对话流程

### 第一步：收集信息

用户说想添加新 agent 时，按以下格式引导（可批量，一次多个）：

```
我需要以下信息来创建 agent：

1. **Agent ID**（英文小写，如 `coder`、`hr-bot`）
2. **中文名称**（如「代码专家」）
3. **Emoji**（如 💻）
4. **飞书 App ID**（格式：cli_xxxxxxxx）
5. **飞书 App Secret**
6. **简介**（可选）

可以一次提供多个，直接列出来就行。
```

### 第二步：确认预览（dry-run）

收到信息后，先 dry-run 预览，确认无误再执行：

```bash
python3 ~/.openclaw/workspace/skills/feishu-multi-agent-factory/scripts/setup_agents.py \
  --dry-run \
  --config '<JSON>'
```

### 第三步：执行创建

用户确认后，正式执行并重启 gateway：

```bash
python3 ~/.openclaw/workspace/skills/feishu-multi-agent-factory/scripts/setup_agents.py \
  --config '<JSON>' \
  --restart
```

## JSON 格式

```json
{
  "agents": [
    {
      "id": "coder",
      "name": "代码专家",
      "emoji": "💻",
      "description": "负责写代码和 code review",
      "feishu_app_id": "<YOUR_APP_ID>",
      "feishu_app_secret": "<YOUR_APP_SECRET>"
    },
    {
      "id": "hr-bot",
      "name": "HR 助手",
      "emoji": "👔",
      "feishu_app_id": "<YOUR_APP_ID>",
      "feishu_app_secret": "<YOUR_APP_SECRET>"
    }
  ]
}
```

## 其他命令

### 查看当前所有 agents

```bash
python3 ~/.openclaw/workspace/skills/feishu-multi-agent-factory/scripts/setup_agents.py --list
```

### 删除某个 agent（仅移除配置，不删目录）

```bash
python3 ~/.openclaw/workspace/skills/feishu-multi-agent-factory/scripts/setup_agents.py --remove <id>
```

## 自动完成的事项清单

每个新 agent 执行完成后会自动：

| 步骤 | 内容 |
|------|------|
| ✅ workspace 目录 | `~/.openclaw/workspace-{id}/` |
| ✅ IDENTITY.md | 包含名称、emoji、描述 |
| ✅ SOUL / AGENTS / TOOLS.md | 基础工作区文件 |
| ✅ agentDir | `~/.openclaw/agents/{id}/agent/` |
| ✅ defaults.json | 继承全局模型配置 |
| ✅ auth-profiles.json | 从 main agent 复制 |
| ✅ agents.list | 写入 openclaw.json |
| ✅ feishu accounts | 写入 openclaw.json |
| ✅ bindings | agent ↔ feishu account |
| ✅ agentToAgent.allow | 加入协作白名单 |

## 飞书 App 说明

每个 agent 对应一个独立的飞书机器人应用（需在飞书开放平台预先创建）。

需要的权限（在飞书开放平台开通）：
- `im:message` — 收发消息
- `im:message.group_at_msg` — 群消息 @ 机器人

连接模式默认为 `websocket`（长连接），无需公网 IP。

## 常见问题

**Q: 飞书凭据在哪里找？**
飞书开放平台 → 我的应用 → 选择应用 → 凭证与基础信息 → App ID / App Secret

**Q: 创建后 agent 没反应？**
确认已运行 `openclaw gateway restart`，并在飞书开放平台确认机器人已上线。

**Q: 想给某个 agent 单独设置模型？**
创建完成后编辑 `~/.openclaw/agents/{id}/agent/defaults.json`，修改 `model.primary`。
