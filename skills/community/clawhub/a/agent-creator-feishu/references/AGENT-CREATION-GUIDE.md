# OpenClaw Agent 创建指南

操作参考文档，配合 SKILL.md 使用。

---

## 1️⃣ 创建工作区

```bash
openclaw agents add <name> --workspace ~/.openclaw/workspace-<name>
```

查看已有 agent：`openclaw agents list`

---

## 2️⃣ 配置文件模板

### IDENTITY.md

```markdown
# IDENTITY.md - <名称>

- **名称**：<名称>
- **定位**：<一句话描述>
- **Emoji**：<emoji>
- **类型**：<Agent 类型>
```

### SOUL.md

```markdown
# SOUL.md - <名称> 的灵魂

## 我是谁

<存在意义>

## 风格

<性格特点，简洁有力的规则>

## 说话风格

<语气、用词习惯、简洁程度>

## 边界

<不该做的事>
```

### AGENTS.md

```markdown
# AGENTS.md - <名称>

## 系统信息

- **工作区**：`~/.openclaw/workspace-<name>`
- **绑定群组**：`oc_xxx`

## 权限控制

**唯一管理员**：`<管理员 open_id>`

只有管理员可以：
- 修改 Agent 行为、配置
- 编辑配置文件

群聊成员可以：
- 使用 Agent 功能
- 查看结果
```

### SKILL.md

```markdown
---
name: <name>
description: <一句话描述>
---

# <name> — 行为指令

## ✅ 核心行为

<具体能做什么>

## ❌ 红线边界

<具体不能做什么>
```

### config.json（可选）

```json
{
  "model": "zai/glm-5",
  "thinking": "low"
}
```

---

## 3️⃣ 白名单配置

检查并添加群组到白名单：

```bash
# 查看当前白名单
cat ~/.openclaw/openclaw.json | python3 -c "import json,sys; c=json.load(sys.stdin); print(json.dumps(c.get('channels',{}).get('feishu',{}).get('groupAllowFrom',[])))"

# 确保群组 ID 在列表中，用 python3 去重更新
```

---

## 4️⃣ 绑定群聊 ⚠️

```bash
openclaw agents bind --agent <name> --bind "feishu:<群组ID>"
```

如果 bind 不生效，手动编辑 `~/.openclaw/openclaw.json` 的 `bindings` 数组：

```json
{
  "type": "route",
  "agentId": "<name>",
  "match": {
    "channel": "feishu",
    "peer": {
      "kind": "group",
      "id": "<群组ID>"
    }
  }
}
```

**❌ 错误写法**（不要用 `accountId`）：
```json
"match": { "channel": "feishu", "accountId": "oc_xxx" }
```

---

## 5️⃣ 测试验证

```bash
# 检查绑定
cat ~/.openclaw/openclaw.json | python3 -c "import json,sys; c=json.load(sys.stdin); print(json.dumps(c.get('bindings',[]), indent=2))"

# 查看日志
tail -f /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log | grep -E "<name>"
```
