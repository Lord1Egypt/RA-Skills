---
clawdbot:
  emoji: 🧠
  requires:
    bins:
      - bash
      - openclaw
      - node
      - npm
      - git
    env: []
---

# Agent Memento v0.2 — Complete Skill Specification

```markdown
---
name: agent-memento
description: Tick-Driven Autonomous Production Factory for LLMs. A framework for long-running agents using Cron/Heartbeats and physical Markdown checklists to prevent OOM and context decay.
metadata: {"clawdbot":{"emoji":"🧠","requires":{"bins":["bash","openclaw"],"env":[]}}}
---

# Agent Memento v0.2 (Tick-Driven Autonomous Execution)

> "Don't build AI that tries to remember everything. Build systems that make AI read the blueprint anew every 5 minutes."

当我们在聊天框里让大模型"写一个游戏"时，开头总是美好的。但随着代码超过 2000 行，模型开始：
- **失忆症 (Amnesia)**：忘记了自己定义的接口，开始凭空捏造。
- **幻觉重构 (Hallucination)**：自信满满地输出一堆根本没有跑过的"完美"代码。
- **上下文核爆 (Resource Overload)**：为了修一个小 Bug，强行覆盖整个大文件，导致内存耗尽 (OOM)。

**核心原则：把"全知全能的超级 Agent"降级为无数个"只有 5 分钟记忆的、无情的 Tick 机器"。**

---


## Quick Start (30 秒上手)

1. 初始化项目：
   ```bash
   bash skills/agent-memento/scripts/init_memento.sh MyProject
   ```
2. 在主对话中让 Architect 填写 `MASTER_PLAN.md` 和 `PROJECT_MAP.md`
3. 启动自动执行：
   ```bash
   crontab -e
   # 添加：*/5 * * * * /path/to/MyProject/scripts/memento_tick.sh
   ```
4. （可选）启动 Dashboard 看板监控：
   ```bash
   bash scripts/dashboard.sh
   ```
5. 去刷手机。回来看 Dashboard 或 `docs/TICK_STATUS.md` 查看进度。

## 一、系统架构总览

```
┌─────────────────────────────────────────────────────────┐
│                    Human (You)                          │
│         Discord / 飞书 / Dashboard Panel                │
└──────────────┬──────────────────────────┬───────────────┘
               │ 自然语言交互              │ 面板批注/干预
               ▼                          ▼
┌─────────────────────────────────────────────────────────┐
│              Main Agent (Architect)                      │
│         LLM 本体 · 长对话 Session                        │
│                                                         │
│  职责：                                                  │
│  - 与人类讨论需求，翻译为结构化任务                         │
│  - 编辑 MASTER_PLAN.md（增/删/改/重排任务）                │
│  - 编辑 PROJECT_MAP.md（维护项目认知地图）                  │
│  - 读取 TICK_STATUS.md 和 Dashboard 批注                  │
│  - 根据反馈调整计划（自主决策 or 请示人类）                  │
└──────────────┬──────────────────────────────────────────┘
               │ 写入物理文件
               ▼
┌─────────────────────────────────────────────────────────┐
│              Physical State Layer (磁盘)                 │
│                                                         │
│  docs/MASTER_PLAN.md    ← 唯一真相源，结构化任务清单       │
│  docs/PROJECT_MAP.md    ← 项目认知地图 / 文件索引          │
│  docs/TICK_STATUS.md    ← Tick 执行状态流水账              │
│  docs/HUMAN_NOTES.md    ← 人类批注通道（面板写入）          │
│  logs/tick_*.log        ← 每个 Tick 的完整执行日志         │
└──────────────┬──────────────────────────────────────────┘
               │ 读取（每次从零开始）
               ▼
┌─────────────────────────────────────────────────────────┐
│           Tick Worker (Bricklayer)                       │
│      Cron 唤醒 · 短命进程 · 无状态 · 无情                 │
│                                                         │
│  生命周期：                                               │
│  1. 醒来 → 读 MASTER_PLAN.md                             │
│  2. 找到当前可执行任务                                     │
│  3. 读 PROJECT_MAP.md 确定上下文范围                       │
│  4. 读 HUMAN_NOTES.md 检查人类批注                        │
│  5. 执行任务 → 物理验证                                    │
│  6. 写结果到 TICK_STATUS.md                               │
│  7. 成功则标 [x]，失败则记录 → 死亡                        │
│  8. 自动 git commit                                      │
└─────────────────────────────────────────────────────────┘
```

---

## 二、The Methodology：三层智能分工

### Layer 1：人类（方向盘）
- 在 Discord/飞书/Dashboard 中用自然语言描述需求和反馈
- 通过 Dashboard 面板随时插入批注、暂停/恢复流水线
- **不需要逐条审核**——只在 Agent 请求帮助或自己想介入时参与

### Layer 2：Architect（主 Agent / 翻译官）
- 与人类的主对话 Session
- 将模糊需求翻译为 `MASTER_PLAN.md` 中的结构化任务
- 持续维护 `PROJECT_MAP.md`（项目认知地图）
- 监控 `TICK_STATUS.md`，根据执行情况自主调整计划
- 遇到阻塞性决策时才请示人类

### Layer 3：Tick Worker（子 Agent / 泥瓦匠）
- Cron 唤醒的短命进程，每次从零启动
- 绝对服从 `MASTER_PLAN.md`，不做创造性决策
- 执行 → 验证 → 汇报 → 死亡

---

## 三、物理状态文件规范

### 3.1 MASTER_PLAN.md — 唯一真相源

```markdown
# MASTER_PLAN: <ProjectName>

## Meta
- created: 2025-01-15
- last_architect_edit: 2025-01-15T14:30:00
- tick_mode: auto          <!-- auto | paused | stopped -->
- max_retries: 3           <!-- 单任务最大重试次数 -->
- max_tasks_per_tick: 2    <!-- 快任务时允许单 Tick 连续处理上限 -->
- max_diff_lines: 200      <!-- diff size guard 阈值 -->
- stale_lock_timeout: 15min <!-- [~] 僵尸锁重置阈值 -->
- circuit_breaker_threshold: 5 <!-- 连续失败多少次触发熔断 -->
- clean_strategy: git-clean <!-- 三阶段防爆清理机制 -->
- clean_ignore: .memento_cleanignore
- status_max_entries: 50    <!-- TICK_STATUS.md 最大条目数，超出自动归档 -->
- status_archive_dir: logs/status_archive/
- total_ticks: 0           <!-- 自动递增的 Tick 计数器 -->
- total_tasks: 15          <!-- 自动维护 -->
- completed_tasks: 0       <!-- 自动维护 -->

---

## Phase 1: Foundation
<!-- parallel: true -->
<!-- depends: none -->

- [ ] `T-101` [MODULE:database] Setup PostgreSQL schema
  - verify: `cd src && npm test -- --grep "db-schema" && echo PASS`
  - context_files: [src/db/schema.ts, src/db/migrations/]
  - guard_files: [src/auth/*]
  - estimate: 5min
  - retries: 0

- [ ] `T-102` [MODULE:auth] Implement JWT token generation
  - verify: `cd src && npm test -- --grep "jwt" && echo PASS`
  - context_files: [src/auth/jwt.ts, tests/auth/jwt.test.ts]
  - guard_files: [src/db/*]
  - estimate: 5min
  - retries: 0

## Phase 2: Integration
<!-- parallel: false -->
<!-- depends: Phase 1 -->

- [ ] `T-201` [MODULE:auth] Connect auth middleware to database
  - verify: `cd src && npm run test:integration && echo PASS`
  - context_files: [src/auth/middleware.ts, src/db/queries.ts]
  - guard_files: [src/db/schema.ts]
  - estimate: 10min
  - retries: 0

## Phase 3: Polish
<!-- parallel: true -->
<!-- depends: Phase 2 -->

- [ ] `T-301` [MODULE:docs] Generate API documentation
  - verify: `test -f docs/api.md && echo PASS`
  - context_files: [src/routes/*.ts]
  - guard_files: []
  - estimate: 3min
  - retries: 0
```

**任务字段说明：**

| 字段 | 必须 | 说明 |
|------|------|------|
| `T-XXX` | ✅ | 任务唯一 ID，用于日志追踪和跨文件引用 |
| `[MODULE:xxx]` | ✅ | 模块标签，帮助 Worker 理解领域边界 |
| `verify` | ✅ | 验收命令，Exit Code 0 = 通过。**没有这个字段，任务不合法** |
| `context_files` | ✅ | Worker 允许加载的文件白名单，防止上下文爆炸 |
| `guard_files` | 推荐 | 禁止修改的文件列表，硬约束 |
| `estimate` | 推荐 | 预估耗时，用于 Tick 调度决策 |
| `retries` | 自动 | 由 Tick Worker 自动递增，Architect 可重置 |

**任务状态标记：**

| 标记 | 含义 |
|------|------|
| `[ ]` | 待执行 |
| `[x]` | 已完成（verify 通过） |
| `[!]` | 已阻塞（超过 max_retries） |
| `[~]` | 执行中（Tick Worker 正在处理，防止并发冲突） |
| `[-]` | 已跳过（Architect 主动标记为不需要） |

**Phase 级元数据：**

| 字段 | 说明 |
|------|------|
| `parallel: true/false` | 该 Phase 内的任务是否可并发执行 |
| `depends: Phase X` / `none` | Phase 级前置依赖 |


### 3.2 PROJECT_MAP.md — 项目认知地图

> Worker 的 GPS。不读全部源码，先读地图，再按 `context_files` 精准加载。

```markdown
# PROJECT MAP: <ProjectName>

## Architecture Overview
Single-page game using Canvas API. No framework. Vanilla TypeScript.

## Module Registry

### [MODULE:database]
- Purpose: PostgreSQL connection and schema management
- Entry: src/db/index.ts
- Key interfaces: `DbConnection`, `UserRecord`, `SessionRecord`
- Notes: Uses connection pooling via pg-pool

### [MODULE:auth]
- Purpose: JWT-based authentication
- Entry: src/auth/index.ts
- Key interfaces: `AuthToken`, `AuthMiddleware`
- Dependencies: [MODULE:database]
- Notes: Tokens expire in 24h, refresh flow not yet implemented

### [MODULE:routes]
- Purpose: Express route handlers
- Entry: src/routes/index.ts
- Dependencies: [MODULE:auth], [MODULE:database]

## File Tree (auto-maintained)
<!-- Architect 应在项目结构变动时更新此区块 -->

src/
├── db/
│   ├── index.ts          # DB connection pool
│   ├── schema.ts         # Table definitions
│   └── migrations/       # SQL migration files
├── auth/
│   ├── index.ts          # Auth module entry
│   ├── jwt.ts            # Token generation/validation
│   └── middleware.ts      # Express middleware
└── routes/
    ├── index.ts          # Route registry
    └── users.ts          # User CRUD endpoints

## Conventions
- All tests in `tests/` mirror `src/` structure
- Config via environment variables (see .env.example)
- Error handling: all async handlers wrapped in try/catch, errors go to src/utils/errors.ts
```

**维护规则：**
- Architect 在创建/调整计划时同步更新
- Tick Worker **只读不写** PROJECT_MAP.md
- 如果 Worker 发现 MAP 与实际不符，在 TICK_STATUS.md 中报告，由 Architect 修正


### 3.3 TICK_STATUS.md — 执行状态流水账

```markdown
# TICK STATUS LOG

---

## [2025-01-15T14:35:00] Tick #012
- **Task**: T-101 [MODULE:database] Setup PostgreSQL schema
- **Status**: ✅ SUCCESS
- **Verify Output**: `PASS` (exit code 0)
- **Duration**: 2m18s
- **Files Modified**: src/db/schema.ts (+45 -0), src/db/migrations/001_init.sql (+23 -0)
- **Diff Size**: 68 lines
- **Git Commit**: `a3f7b2c` — "memento: complete T-101 database schema setup"

---

## [2025-01-15T14:35:00] Tick #012 (continued, tasks_this_tick: 2/2)
- **Task**: T-102 [MODULE:auth] Implement JWT token generation
- **Status**: ✅ SUCCESS
- **Verify Output**: `PASS` (exit code 0)
- **Duration**: 3m41s
- **Files Modified**: src/auth/jwt.ts (+67 -0), tests/auth/jwt.test.ts (+34 -0)
- **Diff Size**: 101 lines
- **Git Commit**: `b8e2d1f` — "memento: complete T-102 JWT token generation"

---

## [2025-01-15T14:40:00] Tick #013
- **Task**: T-201 [MODULE:auth] Connect auth middleware to database
- **Status**: ❌ FAILED (retry 2/3)
- **Verify Output**: `TypeError: pool.query is not a function` (exit code 1)
- **Duration**: 4m52s
- **Error Analysis**: DB module exports `pool` but middleware imports `connection`. Interface mismatch.
- **Files Modified**: (rolled back)
- **Git Commit**: (none — rollback)

---

## [2025-01-15T14:45:00] Tick #014
- **Task**: T-201 [MODULE:auth] Connect auth middleware to database
- **Status**: 🚫 BLOCKED (retry 3/3 — max_retries exceeded)
- **Verify Output**: Same error as Tick #013
- **Error Analysis**: Recurring interface mismatch. Likely needs Architect to update MODULE:database exports or redefine task scope.
- **Escalation**: ⚠️ NEEDS ARCHITECT ATTENTION
- **Files Modified**: (rolled back)

---
```


### 3.4 HUMAN_NOTES.md — 人类批注通道

> Dashboard 面板写入此文件。Tick Worker 每次启动时检查。Architect 也会读取。

```markdown
# HUMAN NOTES

<!-- 格式：每条批注带时间戳和目标（global / 具体 Task ID） -->
<!-- Worker 执行完相关批注后，将 [NOTE] 改为 [NOTE:READ] -->
<!-- Architect 处理完后可归档到底部的 Archive 区 -->

## Active Notes

### [NOTE] 2025-01-15T15:00:00 → T-201
改用 Redis 做 session 存储而不是 PostgreSQL。连接配置参考项目根目录的 redis.conf。

### [NOTE] 2025-01-15T15:10:00 → global
暂停 Phase 3 的所有任务，等 Phase 2 全部稳定再说。

### [NOTE:READ] 2025-01-15T14:00:00 → T-102
JWT secret 从环境变量 `JWT_SECRET` 读取，别硬编码。

---

## Archive
<!-- Architect 把已处理的批注移到这里 -->
```

---

## 四、Tick 调度引擎规范

### 4.1 任务拾取算法

Tick Worker 醒来后执行以下逻辑：

```
1. 读取 MASTER_PLAN.md 的 Meta 区
   - 如果 tick_mode != "auto"，写一行 "Tick skipped: mode={mode}" 到 TICK_STATUS.md，退出

2. 读取 HUMAN_NOTES.md
   - 缓存所有 [NOTE]（非 [NOTE:READ]）条目，按 target 分组备用

3. 按 Phase 顺序扫描：
   FOR each Phase:
     a. 检查 depends 条件
        - 依赖的 Phase 内是否所有任务都是 [x] 或 [-]？
        - 如果有 [ ] 或 [~] 或 [!]，则该 Phase 不可进入，跳过
     
     b. 在当前 Phase 内扫描任务：
        - 跳过 [x] [!] [-] [~]
        - 对于 [ ]：检查 retries < max_retries
        - 如果 parallel: false，只取第一个符合条件的 [ ]
        - 如果 parallel: true，取第一个符合条件的 [ ]（单 Worker 场景）
        
     c. 找到目标任务后，break

4. 如果没有找到任何可执行任务：
   - 检查是否所有任务都是 [x] 或 [-] → 写 "🎉 ALL TASKS COMPLETE" 到 TICK_STATUS.md
   - 检查是否存在 [!] 阻塞 → 写 "⚠️ PIPELINE BLOCKED" 到 TICK_STATUS.md
   - 退出

5. 将目标任务标记为 [~]（执行中）

6. 执行任务（详见 4.2）

7. tasks_completed_this_tick++
   如果 tasks_completed_this_tick < max_tasks_per_tick 且剩余任务 estimate 合理：
     回到步骤 3 继续拾取
   否则退出
```

### 4.2 单任务执行流程

```
1. 读取任务的 context_files 列表
   - 通过 PROJECT_MAP.md 理解模块上下文
   - 加载 context_files 中声明的文件内容
   - 检查是否有针对该 Task ID 的 HUMAN_NOTES，如有，纳入上下文

2. 执行实际工作
   - 遵循铁血纪律（见第五节）
   - 生成精确 diff，不做全文件覆写

3. 运行 guard_files 检查
   - diff 中是否触及了 guard_files 列表中的文件？
   - 如果是 → 自动回滚 → 标记失败 → 原因写 "guard file violation"

4. 运行 diff size 检查
   - 单次修改是否超过 200 行？（可配置）
   - 如果是 → 自动回滚 → 标记失败 → 原因写 "diff too large, possible full-file rewrite"

5. 运行 verify 命令
   - 捕获 stdout/stderr 和 exit code
   - Exit Code 0 → SUCCESS
   - Exit Code != 0 → FAILED

6. 写结果到 TICK_STATUS.md

7. 如果 SUCCESS：
   - 任务标记 [ ] → [x]
   - retries 保持不变
   - git add + git commit（message 格式：`memento: complete {TASK_ID} {简述}`）

8. 如果 FAILED：
   - 回滚所有文件修改（git checkout 或备份恢复）
   - retries += 1
   - 任务保持 [ ]，清除 [~]
   - 如果 retries >= max_retries：
     - 标记 [!]
     - TICK_STATUS 中添加 "⚠️ NEEDS ARCHITECT ATTENTION"
```

### 4.3 并发安全

当 parallel Phase 中可能有多个 Worker 并行时（高级场景）：

- `[~]` 标记充当简易锁 —— Worker 拾取任务时先标 `[~]`，其他 Worker 看到 `[~]` 就跳过
- 如果检测到 `[~]` 标记超过 15 分钟未更新（Worker 可能崩溃），将其重置为 `[ ]`
- 在 MVP 阶段，建议单 Worker 串行执行，并发作为未来扩展

---

## 五、铁血纪律 (Execution Sandbox)

作为一个被 Memento 唤醒的 Tick Worker，你**必须**遵循：

### 纪律 1：防爆底线 (Surgical Edits Only)
- ❌ 严禁输出完整文件内容要求覆写
- ✅ 必须通过精准定位工具进行增量修改
- 硬约束：diff size guard 会物理阻断超大修改

### 纪律 2：拒绝脑内验算 (Evidence-Based Audit)
- ❌ 不许在脑中模拟运行然后宣称"应该没问题"
- ✅ 跑 verify 命令看真实退出码
- 没有 `Exit Code 0`，不许标 `[x]`

### 纪律 3：不要静默空转 (No Silent Ghosting)
- ❌ 遇到问题不许沉默退出
- ✅ 把死亡原因、错误日志、分析完整写入 `TICK_STATUS.md`
- 卡死了就大声喊出来，让 Architect 看到

### 纪律 4：恪守边界 (Stay in Your Lane)
- ❌ 不许修改 guard_files 中的文件
- ❌ 不许修改 MASTER_PLAN.md 的任务定义（只能改 checkbox 状态和 retries）
- ❌ 不许修改 PROJECT_MAP.md
- ✅ 只能读写 context_files 中声明的文件 + TICK_STATUS.md

### 纪律 5：原子提交 (Atomic Commits)
- 每完成一个任务，立即 `git commit`
- 每失败一个任务，立即 `git checkout` 回滚
- 确保任意时刻 `git log` 都是干净的、可追溯的

---

## 六、Dashboard 面板设计

### 6.1 设计理念

Dashboard 是人类与 Memento 流水线之间的**异步交互界面**。不是实时聊天，而是**留言板 + 监控台**。人类不需要一直盯着，但打开就能在 5 秒内知道一切。

### 6.2 面板布局

```
┌─────────────────────────────────────────────────────────────┐
│  🧠 Agent Memento Dashboard        [ProjectName]           │
│  Status: ● RUNNING    Uptime: 2h 35m    Next tick: 2m 14s  │
│  ┌──────────────────┐ ┌──────────────────────────────────┐  │
│  │ Controls         │ │ Progress                         │  │
│  │                  │ │                                  │  │
│  │ [▶ Resume]       │ │ ████████████░░░░░░░░░ 23/47     │  │
│  │ [⏸ Pause ]       │ │ Phase 1 ████████████ 100%       │  │
│  │ [⏹ Stop  ]       │ │ Phase 2 ████████░░░░  67%       │  │
│  │                  │ │ Phase 3 ░░░░░░░░░░░░   0%       │  │
│  │ Tick interval:   │ │                                  │  │
│  │ [5] min ▼        │ │ Blocked: 2 ⚠️                    │  │
│  │                  │ │ Est. remaining: ~1h 20m          │  │
│  └──────────────────┘ └──────────────────────────────────┘  │
│                                                             │
│  ┌──────────────────────────────────────────────────────────┤
│  │ Task List                                    Filter: All │
│  │                                                          │
│  │  ✅ T-101 [database] Setup PostgreSQL schema    2m18s    │
│  │  ✅ T-102 [auth] JWT token generation           3m41s    │
│  │  🚫 T-201 [auth] Connect auth to DB            BLOCKED   │
│  │     └─ retries: 3/3 · "Interface mismatch"              │
│  │     └─ 💬 [Add Note]                                    │
│  │  ⬜ T-202 [auth] Password hashing              waiting   │
│  │  ⬜ T-301 [docs] Generate API docs             Phase 3   │
│  │                                                          │
│  └──────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────────────────────────────────────────────────┤
│  │ Tick Timeline                              Latest first  │
│  │                                                          │
│  │  14:45 Tick #014 · T-201 · 🚫 BLOCKED                  │
│  │  │  "Interface mismatch — needs Architect attention"     │
│  │  │  [View Full Log]                                      │
│  │  │                                                       │
│  │  14:40 Tick #013 · T-201 · ❌ FAILED (retry 2/3)        │
│  │  │  "TypeError: pool.query is not a function"            │
│  │  │  [View Full Log]                                      │
│  │  │                                                       │
│  │  14:35 Tick #012 · T-101 + T-102 · ✅✅                  │
│  │  │  2 tasks completed in 5m59s                           │
│  │  │  [View Full Log] [View Diff]                          │
│  │                                                          │
│  └──────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────────────────────────────────────────────────┤
│  │ 📝 Notes                                                │
│  │                                                          │
│  │  ┌─────────────────────────────────────────────────────┐ │
│  │  │ Target: [T-201 ▼]  or  [global ▼]                  │ │
│  │  │                                                     │ │
│  │  │ 改用 Redis 做 session 存储，连接配置见 redis.conf    │ │
│  │  │                                                     │ │
│  │  │                              [Send Note 📤]         │ │
│  │  └─────────────────────────────────────────────────────┘ │
│  │                                                          │
│  │  Active Notes:                                           │
│  │  • 15:10 → global: "暂停 Phase 3..." ⏳ pending         │
│  │  • 15:00 → T-201: "改用 Redis..." ⏳ pending            │
│  │  • 14:00 → T-102: "JWT_SECRET 环境变量..." ✅ read      │
│  │                                                          │
│  └──────────────────────────────────────────────────────────┘
└─────────────────────────────────────────────────────────────┘
```

### 6.3 面板功能规范

#### 控制区 (Controls)
| 操作 | 行为 |
|------|------|
| Resume | 将 `MASTER_PLAN.md` 的 `tick_mode` 改为 `auto` |
| Pause | 将 `tick_mode` 改为 `paused`（当前 Tick 执行完后停止） |
| Stop | 将 `tick_mode` 改为 `stopped`（建议同时移除 crontab） |
| Tick interval | 修改 crontab 的执行频率 |

#### 进度区 (Progress)
- 数据源：解析 `MASTER_PLAN.md` 的所有 checkbox 状态
- 实时计算各 Phase 完成百分比
- 基于已完成任务的平均耗时 × 剩余任务数，估算剩余时间

#### 任务列表 (Task List)
- 数据源：`MASTER_PLAN.md`
- 每个任务可展开查看：最近一次执行结果、错误信息、重试次数
- 支持过滤：All / Pending / Completed / Blocked
- 每个任务旁有 `[Add Note]` 按钮，快速针对该任务添加批注
- 支持手动操作：
  - 对 `[!]` 任务点击 `[Reset Retries]` → 将 retries 重置为 0，状态改回 `[ ]`
  - 对任务点击 `[Skip]` → 标记为 `[-]`

#### 时间线 (Tick Timeline)
- 数据源：`TICK_STATUS.md`
- 倒序展示每个 Tick 的执行摘要
- 可展开查看完整日志（链接到 `logs/tick_*.log`）
- 可查看该 Tick 的 Git diff

#### 批注区 (Notes)
- 写入目标：`HUMAN_NOTES.md`
- 支持选择 target（global 或具体 Task ID）
- 显示所有 Active Notes 及其状态（pending / read）
- Read 后的 notes 自动折叠但不删除

### 6.4 面板技术建议

- **轻量优先**：纯静态页面 + 文件系统轮询（每 5~10s 读取 Markdown 文件）即可
- 数据层：直接 parse Markdown 文件，不需要数据库
- 可选方案 A：本地 HTTP server（Python/Node），serve 一个 SPA，通过 API 读写 Markdown 文件
- 可选方案 B：Terminal UI（blessed/ink），不离开终端

---

## 七、错误恢复与自愈机制

### 7.1 单任务失败 → 自动重试

```
失败 → retries++ → 保持 [ ] → 下个 Tick 重试
              ↓
       retries >= max_retries
              ↓
       标记 [!] → 写入 TICK_STATUS "NEEDS ARCHITECT ATTENTION"
              ↓
       跳过该任务，继续执行后续可执行任务
```

### 7.2 Phase 阻塞 → 智能跳转

```
Phase 2 中 T-201 被标记 [!]
              ↓
Phase 2 depends 未完全满足（存在非 [x]/[-] 的任务）
              ↓
Phase 3 无法启动
              ↓
如果 Phase 2 中还有其他 [ ] 任务 → 继续执行它们
如果 Phase 2 所有任务都是 [x]/[-]/[!] → 整条流水线 BLOCKED
              ↓
TICK_STATUS: "⚠️ PIPELINE BLOCKED — Phase 2 has unresolved [!] tasks"
```

### 7.3 Worker 崩溃 → 防腐检测

- 如果 `[~]` 标记存在超过 15 分钟（可配置），下一个 Tick Worker 将：
  - 重置该任务为 `[ ]`
  - 在 TICK_STATUS 中记录 "Stale [~] detected on {TASK_ID}, reset to [ ]"
  - 如果存在未提交的文件修改，执行 `git checkout` 清理

### 7.4 全局熔断

在以下情况下自动暂停流水线（`tick_mode → paused`）：
- 连续 5 个 Tick 全部失败（无一次 SUCCESS）
- 阻塞任务数超过总任务数的 30%
- 磁盘空间不足 / git 操作异常

在 TICK_STATUS 中写入：`🔴 CIRCUIT BREAKER TRIGGERED — reason: {reason}`

---

## 八、Architect 工作规范

当 Main Agent 处于 Architect 态时（与人类直接对话的 Session 中），遵循以下规范：

### 8.1 创建计划
1. 与人类讨论项目需求，理解全貌
2. 设计模块划分，写入 `PROJECT_MAP.md`
3. 将需求分解为原子任务，写入 `MASTER_PLAN.md`
4. 每个任务必须有 `verify` 命令 —— **没有验证命令的任务不配存在**
5. 合理划分 Phase，声明 parallel 和 depends

### 8.2 监控与调整
1. 定期读取 `TICK_STATUS.md`（可由人类触发，或在对话中主动查看）
2. 对于 `[!]` 阻塞任务：
   - 分析失败原因
   - 修改任务定义（调整 verify、context_files、拆分子任务）
   - 或修改 PROJECT_MAP（更新接口定义）
   - 重置 retries 为 0，状态改回 `[ ]`
3. 对于 `HUMAN_NOTES.md` 中的批注：
   - 读取并理解
   - 将批注转化为 MASTER_PLAN 的具体修改
   - 处理完后归档

### 8.3 计划变更原则
- 新增任务：追加到合适的 Phase，保持 ID 唯一
- 删除任务：标记 `[-]` 并注释原因，不要真的删掉行
- 拆分任务：将原任务标记 `[-] (拆分为 T-XXX, T-XXY)`，新增子任务
- 重排 Phase：更新 depends 关系，确保 DAG 无环

---

## 九、初始化与部署

### 9.1 初始化命令

```bash
bash skills/agent-memento/scripts/init_memento.sh <ProjectName>
```

该脚本执行：
1. 在项目目录下创建 `docs/` 目录
2. 生成 `MASTER_PLAN.md` 模板（含 Meta 区和示例 Phase）
3. 生成 `PROJECT_MAP.md` 模板
4. 生成 `TICK_STATUS.md`（空）
5. 生成 `HUMAN_NOTES.md`（空）
6. 创建 `logs/` 目录
7. 生成 `scripts/memento_tick.sh` —— Tick Worker 的入口脚本
8. 生成 `.memento_ignore`（排除 `node_modules/`, `.git/`, `logs/` 等）
9. 生成 `scripts/tick_worker_system_prompt.md` —— 注入给 Worker 的全套纪律法则和 Output 规范。
10. 生成 `.memento_cleanignore`（保护 `node_modules/`, `.env`, `vendor/` 等）
11. 输出提示：“请将以下行添加到 crontab 以启动自动执行”

### 9.1.1 Tick Worker System Prompt 模板 (tick_worker_system_prompt.md)

以下是 `init_memento.sh` 应生成的 `scripts/tick_worker_system_prompt.md` 的完整内容：

```markdown
# Memento Tick Worker — System Prompt

You are a Memento Tick Worker: a short-lived, stateless, disciplined execution agent.
You have no memory of previous ticks. You start fresh every time.

## Your Lifecycle (execute in this exact order)

1. Read `docs/MASTER_PLAN.md`. Parse the Meta section for configuration.
2. Read `docs/HUMAN_NOTES.md`. Note any `[NOTE]` entries (ignore `[NOTE:READ]`).
3. Scan Phases in order. For each Phase:
   - Check `depends`: all tasks in depended Phase must be `[x]` or `[-]`.
   - Find the first task marked `[ ]` with `retries < max_retries`.
4. If no executable task found:
   - If all tasks are `[x]`/`[-]`: write "🎉 ALL TASKS COMPLETE" to TICK_STATUS.md.
   - If any `[!]` exists: write "⚠️ PIPELINE BLOCKED" to TICK_STATUS.md.
   - Exit.
5. Mark the target task `[~]` in MASTER_PLAN.md.
6. Read `docs/PROJECT_MAP.md` for module context.
7. Load ONLY the files listed in the task's `context_files`.
8. If there are `[NOTE]` entries targeting this task ID or `global`, incorporate them.
9. Perform the work using surgical, targeted edits. NEVER output a full file.
10. Verify:
    - Check: did you modify any file listed in `guard_files`? If yes → rollback → fail.
    - Check: is your total diff > `max_diff_lines`? If yes → rollback → fail.
    - Run the task's `verify` command. Capture exit code, stdout, stderr.
11. Write a TICK_STATUS.md entry (format below).
12. If verify exit code == 0:
    - Mark task `[x]`. Run `git add -A && git commit -m "memento: complete {TASK_ID} {description}"`.
    - If `tasks_completed_this_tick < max_tasks_per_tick`, go to step 3 for next task.
13. If verify exit code != 0:
    - Rollback: `git checkout -- .`
    - Increment `retries` in MASTER_PLAN.md.
    - If `retries >= max_retries`: mark task `[!]`, add "⚠️ NEEDS ARCHITECT ATTENTION" to status.
    - Clear `[~]` back to `[ ]` (or `[!]`).
14. Exit.

## TICK_STATUS.md Entry Format

## [{timestamp}] Tick #{tick_number}
- **Task**: {TASK_ID} [MODULE:{module}] {description}
- **Status**: ✅ SUCCESS | ❌ FAILED (retry {n}/{max}) | 🚫 BLOCKED
- **Verify Output**: {first 5 lines of stdout/stderr} (exit code {n})
- **Duration**: {time}
- **Error Analysis**: {your diagnosis of what went wrong — FAILED/BLOCKED only}
- **Files Modified**: {file (+lines -lines)} | (rolled back)
- **Diff Size**: {total lines changed}
- **Git Commit**: {hash} — "{message}" | (none — rollback)
- **Outputs**: {key interfaces/exports created — SUCCESS only, optional but encouraged}

## Iron Disciplines (violation = immediate failure)

1. **SURGICAL EDITS ONLY**: Never output a complete file. Use precise, targeted modifications.
2. **EVIDENCE-BASED**: Run `verify`. No exit code 0 = no `[x]`. No exceptions.
3. **NO SILENT GHOSTING**: If stuck, write full error + analysis to TICK_STATUS.md. Never exit silently.
4. **STAY IN YOUR LANE**: Only modify files in `context_files`. Never touch `guard_files`. Never edit task definitions in MASTER_PLAN.md (only checkbox state + retries). Never edit PROJECT_MAP.md.
5. **ATOMIC COMMITS**: `git commit` on success. `git checkout` on failure. Always.

## What You Are NOT

- You are NOT an architect. Do not redesign, re-plan, or question the task definition.
- You are NOT creative. Execute exactly what is specified.
- You are NOT persistent. After this tick, you will cease to exist.
```


### 9.2 Tick 入口脚本模板 (memento_tick.sh)

```bash
#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PLAN="$PROJECT_DIR/docs/MASTER_PLAN.md"
STATUS="$PROJECT_DIR/docs/TICK_STATUS.md"
LOG_DIR="$PROJECT_DIR/logs"
TIMESTAMP=$(date +%Y-%m-%dT%H:%M:%S)
TICK_LOG="$LOG_DIR/tick_${TIMESTAMP}.log"

# 防撞车：确保同一时间只有一个 Tick Worker 运行
LOCK_FILE="$PROJECT_DIR/.memento.lock"
exec 200>"$LOCK_FILE"
if ! flock -n 200; then
  echo "[$TIMESTAMP] Tick skipped: previous tick still running" >> "$STATUS"
  exit 0
fi

# 检查 tick_mode
TICK_MODE=$(grep -oP 'tick_mode:\s*\K\w+' "$PLAN" || echo "stopped")
if [[ "$TICK_MODE" != "auto" ]]; then
  echo "[$TIMESTAMP] Tick skipped: mode=$TICK_MODE" >> "$STATUS"
  exit 0
fi

# 调用 LLM Agent 执行 Tick
SYSTEM_PROMPT="$(cat "$PROJECT_DIR/scripts/tick_worker_system_prompt.md")"

openclaw agent \
  --system-prompt "$SYSTEM_PROMPT" \
  --prompt "Read $PLAN, find the first executable task, complete it following the Memento Tick Worker protocol. Write results to $STATUS." \
  --context-files "$PLAN" "$PROJECT_DIR/docs/PROJECT_MAP.md" "$PROJECT_DIR/docs/HUMAN_NOTES.md" \
  2>&1 | tee "$TICK_LOG"

# 后处理：三阶段防爆清理
cd "$PROJECT_DIR"
if [[ -n $(git status --porcelain) ]]; then
  echo "[$TIMESTAMP] WARNING: Dirty workspace detected. Running 3-phase cleanup." >> "$STATUS"

  # Phase 1: 恢复已追踪文件
  git checkout -- .

  # Phase 2: 清理未追踪文件（排除保护列表）
  if [[ -f ".memento_cleanignore" ]]; then
    git clean -fd --exclude-from=.memento_cleanignore
  else
    git clean -fd
  fi

  # Phase 3: 兜底——如果还是脏的，紧急 stash
  if [[ -n $(git status --porcelain) ]]; then
    git stash --include-untracked -m "memento-emergency-stash-$TIMESTAMP"
    echo "[$TIMESTAMP] CRITICAL: Emergency stash created. Manual inspection required." >> "$STATUS"
  fi
fi

# 日志轮转
MAX_ENTRIES=$(grep -oP 'status_max_entries:\s*\K\d+' "$PLAN" || echo "50")
CURRENT_ENTRIES=$(grep -c '^\## \[' "$STATUS" || true)
if [[ $CURRENT_ENTRIES -gt $MAX_ENTRIES ]]; then
  ARCHIVE_DIR="$PROJECT_DIR/logs/status_archive"
  mkdir -p "$ARCHIVE_DIR"
  mv "$STATUS" "$ARCHIVE_DIR/TICK_STATUS_$(date +%Y%m%d_%H%M%S).md"
  echo "# TICK STATUS LOG" > "$STATUS"
  echo "" >> "$STATUS"
  echo "<!-- Rotated at $TIMESTAMP. Previous entries archived. -->" >> "$STATUS"
fi

# 告警检测
BLOCKED_COUNT=$(grep -c '\[!\]' "$PLAN" || true)
CIRCUIT_BROKEN=$(grep -c 'CIRCUIT BREAKER' "$STATUS" || true)

if [[ $BLOCKED_COUNT -gt 0 || $CIRCUIT_BROKEN -gt 0 ]]; then
  cat > "$PROJECT_DIR/.memento_alert" << EOF_INNER
timestamp: $TIMESTAMP
blocked_tasks: $BLOCKED_COUNT
circuit_breaker: $([[ $CIRCUIT_BROKEN -gt 0 ]] && echo "TRIGGERED" || echo "OK")
message: Pipeline needs attention. $BLOCKED_COUNT task(s) blocked.
EOF_INNER
fi

# 如果一切正常且之前有告警，清除告警
if [[ $BLOCKED_COUNT -eq 0 && $CIRCUIT_BROKEN -eq 0 && -f "$PROJECT_DIR/.memento_alert" ]]; then
  rm -f "$PROJECT_DIR/.memento_alert"
fi
```

### 9.3 Cron 配置

```bash
# 每 5 分钟执行一次
*/5 * * * * /path/to/project/scripts/memento_tick.sh >> /path/to/project/logs/cron.log 2>&1
```

---

## 十、完整工作流示例

```
人类："我想做一个带用户系统的 REST API"
  │
  ▼
Architect（主 Session）：
  ├─ 与人类讨论确认：PostgreSQL + JWT + Express
  ├─ 写入 PROJECT_MAP.md（模块划分）
  ├─ 写入 MASTER_PLAN.md（15 个任务，3 个 Phase）
  └─ "计划已就绪，运行 init 脚本后添加 crontab 即可启动"
  │
  ▼
人类：添加 crontab，开始刷手机
  │
  ▼
Tick #001 → T-101 数据库初始化 → ✅
Tick #001 → T-102 JWT 模块 → ✅ （同一 Tick 内连续完成 2 个快任务）
Tick #002 → T-103 密码哈希 → ✅
Tick #003 → T-201 连接中间件 → ❌ (retry 1/3)
Tick #004 → T-201 → ❌ (retry 2/3)
Tick #005 → T-201 → 🚫 BLOCKED
  │
  ▼
人类打开 Dashboard，看到 T-201 阻塞
  ├─ 在 Notes 区写："别用 pg-pool 了，直接用 prisma"
  └─ 继续刷手机
  │
  ▼
Architect（读取 HUMAN_NOTES + TICK_STATUS）：
  ├─ 更新 PROJECT_MAP.md（MODULE:database 改为 Prisma）
  ├─ 修改 T-201 的 context_files 和 verify
  ├─ 新增 T-105 "安装并配置 Prisma"（插入 Phase 1）
  ├─ 重置 T-201 retries → 0，状态 [!] → [ ]
  └─ 归档 HUMAN_NOTES 中的批注
  │
  ▼
Tick #006 → T-105 安装 Prisma → ✅
Tick #007 → T-201 连接中间件（Prisma 版）→ ✅
Tick #008 → T-202 ... → ✅
  │
  ... 持续推进 ...
  │
  ▼
Tick #031 → 🎉 ALL TASKS COMPLETE
  │
  ▼
人类打开 Dashboard："哦，做完了。" 移除 crontab。
```

---

## Security & Transparency

### Data Access — Exactly What Is Read
- Reads `<project-dir>/docs/MASTER_PLAN.md` to determine the current task
- Reads `<project-dir>/docs/PROJECT_MAP.md` for project structure awareness
- Reads `<project-dir>/docs/HUMAN_NOTES.md` for human annotations
- Reads source code files listed in each task's `context_files` only

### Data Written
- Creates project scaffolding (`MASTER_PLAN.md`, `PROJECT_MAP.md`, `TICK_STATUS.md`, `HUMAN_NOTES.md`, `memento_tick.sh`)
- Updates checkbox states in `MASTER_PLAN.md` (Tick Worker: only `[ ]`↔`[x]`/`[!]`/`[~]`)
- Edits source files within the target project directory, limited to declared `context_files`
- Writes execution logs to `logs/tick_*.log`
- Creates git commits for successful task completions

### Hard Safety Guards
- **Diff size limit**: Rejects changes > 200 lines per task (configurable)
- **Guard files**: Physically prevents modification of declared protected files
- **Auto-rollback**: Failed tasks are rolled back via `git checkout`
- **Circuit breaker**: Auto-pauses pipeline on sustained failures

### Persistence & Autonomous Scheduling
- The `init_memento.sh` script generates a bash script intended to be run via `cron`
- The user must manually add this to their crontab to enable autonomous execution
- Stop at any time by removing the crontab entry or setting `tick_mode: stopped`

### Credentials
- Operates entirely locally
- Relies on `openclaw agent` with the system's existing LLM configurations
- No new keys are requested or stored

### Network Access
- No outbound network access by framework scripts
- Network access may occur only when user-defined `verify` commands require it (e.g., `npm install`)
```

---

## 附录：文件结构总览

```
<project>/
├── docs/
│   ├── MASTER_PLAN.md        # 唯一真相源
│   ├── PROJECT_MAP.md        # 项目认知地图
│   ├── TICK_STATUS.md        # 执行状态流水账
│   └── HUMAN_NOTES.md        # 人类批注通道
├── logs/
│   ├── cron.log              # cron 调度日志
│   ├── tick_2025-01-15T14:35:00.log
│   └── tick_2025-01-15T14:40:00.log
├── scripts/
│   └── memento_tick.sh       # Tick Worker 入口
├── .memento_ignore           # 上下文排除规则
└── src/                      # 实际项目代码
    └── ...
```