<!-- License: MIT License (c) 2024 perrykono-debug -->

# SKILL.md

**License:** MIT  
**Copyright:** 2026 perrykono-debug

---

---
name: a2a-gateway
description: |
  A2A Gateway 是 OpenClaw Agent 网络的协作总线（Agent Service Bus）。
  当用户提到以下场景时使用此 skill：
  (1) 注册/管理/查询 Agent 能力目录（Agent Card）
  (2) 发起跨 Agent 任务委托、路由、追踪
  (3) 查询/分析 Agent 协作审计日志和链路
  (4) 检查 Agent 在线状态和健康状况
  (5) 设计 A2A/Agent 协作架构
  (6) 管理 OpenClaw 多 Agent 网络
  核心功能模块：Agent Registry / Capability Router / Task Center / Audit Trail / Health Check
---

# A2A Gateway — Agent Service Bus

## 定位

OpenClaw Agent 网络的协作基础设施层。
所有 Agent 的发现、注册、委托、追踪、审计都经过它。

```
用户
 ↓
[其他 Agent / 驾驶舱]
 ↓
A2A Gateway（灵枢）
 ↓
招商助手 | 企服助手 | 招商智库 | ...
```

## 五大模块

### ① Agent Registry（注册中心）

管理 OpenClaw Agent 的 Agent Card，类似 A2A 协议中的 Agent Card 机制。

**Agent Card 结构**：
```json
{
  "agent_id": "招商助手",
  "name": "招商助手",
  "description": "产业园招商运营助手",
  "skills": ["客户分析", "招商周报", "企业画像"],
  "capabilities": ["客户风险评估", "产业链分析"],
  "status": "online",
  "updated_at": "2026-06-07T10:00:00Z",
  "created_at": "2026-06-07T10:00:00Z"
}
```

**CLI 用法**：
```bash
# 注册 Agent
python3 scripts/registry.py register <agent_id> <name> <description> <skills_csv>

# 查询
python3 scripts/registry.py get <agent_id>

# 列出全部
python3 scripts/registry.py list

# 按技能搜索
python3 scripts/registry.py find <keyword>

# 从 openclaw.json 同步
python3 scripts/registry.py sync <openclaw.json路径>
```

### ② Capability Router（能力路由）

核心模块：识别用户意图 → 匹配最佳 Agent → 创建委托任务。

**路由流程**：
```
用户请求 → 意图解析（关键词匹配） → 搜索 Registry
         → 选中最佳 Agent → 创建 Task → 返回 task_id
```

**CLI 用法**：
```bash
python3 scripts/router.py <from_agent> "<user_intent>"
# 例如: python3 scripts/router.py 招商驾驶舱 "分析客户流失风险"
```

**MVP 说明**：当前使用关键词匹配。
升级路径：LLM 意图分类 → Agent 能力图谱。

### ③ Task Center（任务中心）

管理跨 Agent 委托任务的生命周期。

**任务状态机**：
```
PENDING → RUNNING → COMPLETED
                  → FAILED
       → CANCELLED
```

**CLI 用法**：
```bash
# 创建任务
python3 scripts/task_center.py create <from> <to> <skill> "<description>"

# 查询
python3 scripts/task_center.py get <task_id>
python3 scripts/task_center.py list [--status RUNNING] [--from from_agent] [--to to_agent]

# 更新状态
python3 scripts/task_center.py update <task_id> <new_status> [--result 'json'] [--error 'msg']

# 健康检查：查超时任务
python3 scripts/task_center.py stuck [threshold_minutes]
```

### ④ Audit Trail（协作审计链）

记录每次委托的完整链路，支持 trace_id 串联多跳协作。

**CLI 用法**：
```bash
# 记录审计事件
python3 scripts/audit.py record <trace_id> <from> <to> <skill> [--status success|failure]
                                       [--duration 8.5] [--error "错误信息"]

# 查询日志
python3 scripts/audit.py query [--trace_id trace_xxx] [--from from] [--to to] [--limit 50]

# 获取完整链路图
python3 scripts/audit.py trace <trace_id>

# 统计
python3 scripts/audit.py stats [days]
```

**链路图示例**：
```text
招商驾驶舱 → 招商助手 → 企服助手 → 招商智库
```

### ⑤ Health Check（健康检测）

每小时检查所有注册 Agent 的在线状态。

**状态类型**：`online` / `offline` / `error` / `stale`（超过24h未更新）/ `unknown`

**CLI 用法**：
```bash
python3 scripts/health.py check      # 检查全部
python3 scripts/health.py report      # 驾驶舱友好报告
python3 scripts/health.py status <agent_id>  # 单个状态
```

## 数据目录

```
~/.qclaw/workspace-a2a-gateway/
├── registry/agent_cards.json   # Agent 能力目录
├── tasks/tasks.json            # 任务状态库
├── audit/audit_log.json        # 协作审计链
└── health/health_status.json   # 健康状态快照
```

## 与报告框架的对应关系

| 报告概念 | A2A Gateway 模块 |
|---------|----------------|
| Agent Card | Agent Registry |
| Task 对象 | Task Center |
| 协作审计链 | Audit Trail |
| 能力发现/路由 | Capability Router |
| Agent 存活检测 | Health Check |
| Agent Link（信任锚） | Audit Trail + Registry 联合实现 |

## 常见操作示例

**场景：用户从驾驶舱发起"客户流失风险分析"**

1. Router 接收请求
2. 在 Registry 中搜索匹配 `["客户分析","风险评估"]` 的 Agent → 找到 `招商助手`
3. Task Center 创建任务 `task_xxx`，状态 `PENDING`
4. 返回 `task_id` 给驾驶舱
5. 任务执行完成后，Audit Trail 记录完整链路

**场景：检查协作健康**
```bash
python3 scripts/task_center.py stuck 60
python3 scripts/audit.py stats 7
python3 scripts/health.py report
```
