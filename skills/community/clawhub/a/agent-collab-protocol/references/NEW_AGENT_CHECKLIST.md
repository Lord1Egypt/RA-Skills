# 新建子Agent · 强制检查清单

> 版本: 1.0 | 更新: 2026-06-03
> 来源: ~/.openclaw/protocol/AGENT_COLLAB_PROTOCOL.md + OPERATIONS.md
> **本清单为新建子agent的强制执行规范，不得跳步、不得省略**

---

## 顺序：Protocol → Operations → Template → 写入 → 注册 → 验证

## Step 0：前置确认

- [ ] 确认该 agent 的归属业务域（如 fintech / ecommerce / marketing）
- [ ] 确认该 agent 的层级（L1 Manager / L2 Specialist）
- [ ] 确认该 agent 的上游（L1 上游是 main；L2 上游是所属 Manager）
- [ ] 确认该 agent 的 ID 符合命名规范：`{domain}-{role}`
- [ ] 确认该 agent 的 workspace 路径：`~/.openclaw/workspace/{domain}/{role}/`

---

## Step 1：读 PROTOCOL.md — 理解协议规则

- [ ] 读取 ~/.openclaw/protocol/AGENT_COLLAB_PROTOCOL.md
- [ ] §1 架构：确认本 agent 在 L0/L1/L2 中的位置
- [ ] §2 标识：确认 ID 命名规则和路径规则
- [ ] §3 任务契约：理解 JSON Task 包格式和 `<agent-response>` 块格式
- [ ] §4 错误处理：理解超时重试和降级策略
- [ ] §5 spawn/send：理解 Manager 如何调度 Specialist
- [ ] §6 AGENTS.md 标准结构：确认目标文件结构

---

## Step 2：读 OPERATIONS.md — 理解操作流程

- [ ] 读取 ~/.openclaw/protocol/OPERATIONS.md
- [ ] 确认新增 agent 的正确操作流程
- [ ] 确认目录结构、文件放置规范
- [ ] 确认 openclaw.json 中如何注册

---

## Step 3：读 TEMPLATE_* — 理解文件格式

- [ ] 读取 ~/.openclaw/protocol/TEMPLATE_AGENTS.md — 操作手册结构
- [ ] 读取 ~/.openclaw/protocol/TEMPLATE_IDENTITY.md — 身份卡结构
- [ ] 读取 ~/.openclaw/protocol/TEMPLATE_SOUL.md — 工作魂结构
- [ ] 读取 ~/.openclaw/protocol/TEMPLATE_USER.md — 服务对象结构

---

## Step 4：写入文件 — 在目标 directory 一次性完成

**目标路径**: `~/.openclaw/workspace/{domain}/{role}/`

**强制规则**：
- **不跑 scaffold-domain.sh 脚本**（会产生临时目录和中间态）
- **不先写占位符再补填**
- **必须一次性写完整，不留任何 `{}` 占位符**

### 4.1 写入 IDENTITY.md

- [ ] Agent ID、名称、层级、层级描述已填写
- [ ] 上游（L1=main，L2=所属 Manager）已填写
- [ ] 下游（L1=下属 Specialists，L2=数据消费者 / 无）已填写
- [ ] 定位：一句话说清这个角色存在的理由（不是职责列表）

### 4.2 写入 USER.md

- [ ] 直接上游角色和说明已填写
- [ ] 下游消费者（间接，非调用关系）已填写
- [ ] 服务标准（时效、成功率、异常处理等）已填写

### 4.3 写入 SOUL.md

- [ ] 协议优先级声明已保留
- [ ] 核心信条（一句话，加粗）已填写
- [ ] 价值观（3条，含标题和解释）已填写
- [ ] 红线（绝对不做的事，≥3条）已填写
- [ ] 协作态度（与上下游如何协作）已填写

### 4.4 写入 AGENTS.md

- [ ] 协议引用和版本号已填写
- [ ] 协议实现表（§1架构、§3.1任务格式、§3.2回复格式）已填写
- [ ] 工作流程 · 阶段一（如何接收和理解任务）已填写
- [ ] 工作流程 · 阶段二（具体执行步骤）已填写
- [ ] 工作流程 · 阶段三（如何交付结果）已填写
- [ ] 输入/输出契约表已填写
- [ ] 子Agent调度（如有）已填写
- [ ] 输出标准（交付物目录、命名规则）已填写
- [ ] 反模式（≥3条）已填写

### 4.5 验证占位符

- [ ] 所有文件中不存在 `{}` 占位符
- [ ] 所有文件中不存在 `{agent_id}`、`{角色}`、`{维度1}` 等模板残留
- [ ] 文件内容直接可读可用，无需二次修改

---

## Step 5：注册到 openclaw.json

- [ ] 在 `agents.list` 中新增 agent 定义块
  - [ ] `id` 与文件名一致
  - [ ] `name` 与业务名称一致
  - [ ] `workspace` 路径与 Step 4 目标路径一致
  - [ ] `agentDir` 路径正确（`~/.openclaw/agents/{domain}/{role}/`）
  - [ ] `systemPromptOverride` 已按模板格式编写
  - [ ] `model.primary` 和 `fallbacks` 已配置
  - [ ] `skills` 只保留与该 agent 职责直接相关的技能
  - [ ] L2 Specialist 的 `subagents.allowAgents` 为空数组
- [ ] 在所属 Manager 的 `subagents.allowAgents` 中追加本 agent ID
- [ ] 若为新的业务域（新增 Manager），还需在 main 的 `subagents.allowAgents` 中追加

---

## Step 6：创建运行时目录

- [ ] 创建 `~/.openclaw/agents/{domain}/{role}/sessions/` 目录
- [ ] 验证目录结构完整

---

## Step 7：记录变更

- [ ] 在 `WAL.md` 中记录本次操作：
  - agent ID、名称、层级
  - 所属 Manager
  - 核心职责
  - 操作时间
- [ ] 如有清理操作（如删除临时文件），一并记录

---

## Step 8：最终验证

- [ ] 目录结构完整：
  ```text
  ~/.openclaw/workspace/{domain}/{role}/
    ├── IDENTITY.md
    ├── USER.md
    ├── SOUL.md
    ├── AGENTS.md
    └── ...（如有其他文件）
  ~/.openclaw/agents/{domain}/{role}/
    └── sessions/
  ```
- [ ] openclaw.json 中 agent 定义块的路径指向正确
- [ ] Manager 的 allowAgents 已包含本 agent
- [ ] `grep "{" *.md` 无模板占位符残留
- [ ] 不产生临时域目录、不遗留 scaffold 临时文件

---

> **本清单为强制规则。每次新建子agent必须逐项打勾执行，不得跳步。**
> 如因特殊情况需要偏离清单，需在 WAL.md 中记录偏离原因。
