---
name: agentic-beehive-mcp
description: "蜂巢动态调度中枢 MCP Server — 为 AI Agent 提供态势感知、分支调度、外在群落管理。金鱼脑模型的体外记忆和群体能力骨架。"
metadata:
  { "openclaw": { "emoji": "🐝", "requires": { "bins": ["python3", "pip"] } } }
---

# Agentic Beehive MCP Server

蜂巢动态调度中枢 — 态势感知、分支调度、外在群落管理

## 安装

```bash
# 1. 安装到 OpenClaw skills 目录
clawhub install agentic-beehive-mcp

# 2. 创建 Python 虚拟环境
cd ~/.openclaw/workspace/skills/skills/agentic-beehive-mcp
python3 -m venv .venv
source .venv/bin/activate
pip install fastmcp

# 3. 在 openclaw.json 中注册 MCP server
# 添加到 mcp.servers：
# "agentic-beehive": {
#   "command": "<skill-path>/.venv/bin/python",
#   "args": ["<skill-path>/server.py"]
# }

# 4. 重启 gateway
openclaw gateway restart
```

## 工具清单（12个）

### 🏠 蜂巢工具（内部）
- `skill_list` — 列出蜂巢所有分支及其状态
- `skill_query` — 根据任务描述推荐分支和范式
- `skill_update` — 更新分支状态/效果评分
- `skill_evolve` — 触发分支进化（添加新能力）

### 🌍 生态工具（外部）
- `colony_list` — 列出所有已注册的外在群落
- `colony_register` — 注册新群落（hive/flower_field/manuka_grove/river）
- `colony_poll` — 探测群落状态
- `colony_forage` — 从群落采蜜（取数据）

### 📡 态势工具（全局）
- `status_summary` — 蜂巢全局态势摘要
- `status_decide` — 范式判断（任务交付 vs 状态维持）
- `alert_add` — 添加告警
- `alert_resolve` — 解决告警

## 蜂巢生态位

| 类型 | 生态位 | 含义 |
|------|--------|------|
| `hive` | 🏠 另一个蜂巢 | 其他 Agent 集群 |
| `flower_field` | 🌼 油菜花群落 | 数据源 |
| `manuka_grove` | 🌿 麦卢卡树丛 | 专业知识 |
| `river` | 🌊 河流 | 流式信息 |

## 设计哲学

- **采蜜**：按需从外在群落取数据
- **酿蜜**：将原始数据加工成决策和知识
- **分蜂**：集群自我进化，扩展新分支或新群落

## 对金鱼脑模型的意义

MiniMax 等短上下文模型无法自主维持记忆和态势感知。
beehive 是它的体外骨架：
- 忘了在干什么 → `status_summary`
- 忘了有什么能力 → `skill_list`
- 不知道该用什么 → `skill_query` + `status_decide`
- 需要外部数据 → `colony_forage`
