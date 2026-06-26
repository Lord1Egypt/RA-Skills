# Agentic Beehive MCP Server

蜂巢动态调度中枢 — 态势感知、分支调度、外在群落管理

## 启动

```bash
# 已注册为 OpenClaw MCP server，Gateway 启动时自动拉起
# 手动测试：
cd ~/.openclaw/workspace/skills/skills/agentic-engineering/mcp-server
source .venv/bin/activate
python server.py
```

## 工具清单（12个）

### 🏠 蜂巢工具（内部）

| 工具 | 说明 |
|------|------|
| `skill_list` | 列出蜂巢所有分支及其状态 |
| `skill_query` | 根据任务描述推荐分支和范式 |
| `skill_update` | 更新分支状态/效果评分 |
| `skill_evolve` | 触发分支进化（添加新能力） |

### 🌍 生态工具（外部）

| 工具 | 说明 |
|------|------|
| `colony_list` | 列出所有已注册的外在群落 |
| `colony_register` | 注册新群落（hive/flower_field/manuka_grove/river） |
| `colony_poll` | 探测群落状态 |
| `colony_forage` | 从群落采蜜（取数据） |

### 📡 态势工具（全局）

| 工具 | 说明 |
|------|------|
| `status_summary` | 蜂巢全局态势摘要 |
| `status_decide` | 范式判断（任务交付 vs 状态维持） |
| `alert_add` | 添加告警 |
| `alert_resolve` | 解决告警 |

## 状态模型

- **存储**：SQLite (`beehive.db`)，WAL 模式
- **表**：branches, colonies, alerts, evolution_log
- **分支自动同步**：启动时从 SKILL.md 定义同步到 DB

## 外在群落类型

| 类型 | 生态位 | 含义 |
|------|--------|------|
| `hive` | 🏠 另一个蜂巢 | 其他 Agent 集群 |
| `flower_field` | 🌼 油菜花群落 | 数据源 |
| `manuka_grove` | 🌿 麦卢卡树丛 | 专业知识 |
| `river` | 🌊 河流 | 流式信息 |

## 交互规则

- **采蜜**：`colony_forage` 按需取数据
- **酿蜜**：`skill_query` + `status_decide` 加工成决策
- **分蜂**：`skill_evolve` 自我进化扩展

## 版本

- 1.0.0 — 2026-05-13 初始版本
