# Agent Swarm Playbook：多 Agent 自动化编程最佳实践

> 基于 Elvis (OpenClaw Agent Swarm)、Peter Steinberger (Moltbot/Clawdbot) 的实践经验，结合我们自身硬件与订阅条件，**经 PolyGo 项目 18 个任务实战验证**的完整工作流。

---

## 目录

1. [设计哲学](#1-设计哲学)
2. [架构总览](#2-架构总览)
3. [硬件与软件配置](#3-硬件与软件配置)
4. [Agent 角色与分工](#4-agent-角色与分工)
5. [任务生命周期](#5-任务生命周期)
6. [任务拆解原则](#6-任务拆解原则)
7. [原子化提交策略](#7-原子化提交策略)
8. [并行开发模型](#8-并行开发模型)
9. [事件驱动监控](#9-事件驱动监控)
10. [Review 分级制度](#10-review-分级制度)
11. [失败与重试策略](#11-失败与重试策略)
12. [权限边界](#12-权限边界)
13. [任务状态持久化](#13-任务状态持久化)
14. [配置文件体系](#14-配置文件体系)
15. [Prompt 模板规范](#15-prompt-模板规范)
16. [信任阈值模型](#16-信任阈值模型)
17. [成本与资源分析](#17-成本与资源分析)
18. [实战经验与教训](#18-实战经验与教训)
19. [参考资料](#19-参考资料)

---

## 1. 设计哲学

### 1.1 核心理念

**"我看代码流动，而不是读代码。"** —— Peter Steinberger

开发者的角色从"写代码"转向"引导代码生成"。AI 负责实现细节，人类负责产品方向和架构决策。

### 1.2 三个原则

**原则一：编排层与执行层分离**

编排层（OpenClaw / 小明）持有业务上下文——客户需求、架构决策、历史教训。执行层（Codex / Claude Code）只看代码。两层各自加载最需要的上下文，避免 context window 被稀释。

> "Context windows are zero-sum. You have to choose what goes in. Fill it with code → no room for business context. Fill it with customer history → no room for the codebase." —— Elvis

**原则二：原子化一切**

一个任务 = 一个原子 commit。每个 commit 只做一件事。这是高频迭代的安全网——任何一次提交出问题，都能快速 `git revert`，不牵连其他功能。

> Peter 在 66 天内完成 8,297 次 commit，日均 127 次，平均每 11 分钟一次提交。项目没有失控，靠的就是原子化提交。

**原则三：事件驱动，不轮询**

Agent 完成任务后通过 git hook 和完成回调**立即通知**编排层，而不是靠定时轮询检测状态。这让整个流水线零延迟自动运转。

> 实战教训：最初用 cron 每 3 分钟轮询 tmux 状态，延迟高且不可靠。改为 post-commit hook + on-complete.sh 后，完成到下一步派发的延迟从分钟级降到秒级。

### 1.3 两种模式对比

| 维度 | Elvis 模式（PR 驱动） | Peter 模式（主干开发） |
|------|----------------------|----------------------|
| 分支策略 | 每个任务独立 worktree + PR | 所有 agent 直接在 main 工作 |
| 安全网 | PR review + CI | 原子 commit + git revert |
| 并发隔离 | worktree 物理隔离 | 文件级目录隔离 |
| 监控信号 | PR 创建 + CI 状态 | git hook 事件 + tmux 状态 |
| 适合场景 | 团队协作、需要审批流 | 个人/小团队、追求速度 |

**我们选择：Peter 模式。** 所有 agent 在 main 分支工作，不用 worktree 和 PR，原子 commit 作为安全网。原因：更简单、更快、更符合单人开发的实际需求。

---

## 2. 架构总览

```
┌─────────────────────────────────────────────────┐
│  人类（Telegram / MacBook Pro SSH）              │
│  • 提需求                                       │
│  • 收进度通知（自动推送）                         │
│  • 处理升级问题                                  │
└──────────────────┬──────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────┐
│  OpenClaw 编排层（Mac Mini）                     │
│  小明 = 调度中心                                 │
│                                                  │
│  职责：                                          │
│  • 理解需求，拆解为原子任务                       │
│  • 生成精确 prompt，派发给对应 agent              │
│  • 事件驱动监控：hook 触发 → 即时响应             │
│  • 按 review_level 分级验证                      │
│  • 自动解锁依赖，派发下游任务                     │
│  • Telegram 通知人类关键节点                      │
└──┬───────┬───────┬───────┬──────────┬───────────┘
   │       │       │       │          │
   ▼       ▼       ▼       ▼          ▼
┌──────┐┌──────┐┌──────┐┌───────┐┌──────────┐
│cc-   ││codex ││cc-   ││cc-    ││codex-    │
│plan  ││-1/-2 ││front ││review ││review    │
│      ││      ││end   ││       ││          │
│规划  ││后端  ││前端  ││审查CC ││审查Codex │
└──────┘└──────┘└──────┘└───────┘└──────────┘
```

### 2.1 事件驱动信息流

```
需求输入 → cc-plan 规划 → 任务列表 → active-tasks.json
  ↓
dispatch.sh 派发 → Agent 编码 → git commit
  ↓
post-commit hook 触发 → 写信号 + 唤醒编排层
  ↓
编排层验证 scope → 按 review_level 处理：
  full  → 派 review agent → on-complete.sh → 编排层评估
  scan  → 编排层自己看 diff
  skip  → 直接 done
  ↓
标记 done → update-task-status.sh 自动解锁下游 blocked→pending
         → openclaw system event 直接唤醒主 session
  ↓
全部完成 → on-complete.sh 发 swarm 总汇报（项目/任务数/commit 数/token 汇总）
```

---

## 3. 硬件与软件配置

### 3.1 硬件

| 设备 | 配置 | 角色 |
|------|------|------|
| Mac Mini | 16GB RAM | 主力：OpenClaw 编排 + 所有 agent 运行 |
| MacBook Pro | 24GB M3 | SSH 进 Mac Mini 监控进度 |

### 3.2 软件订阅

| 服务 | 计划 | 用途 |
|------|------|------|
| Claude Code | Max 会员 | 无限量：规划、前端编码、review |
| Codex | Pro 或 Business | 后端编码（gpt-5.4 high，云端执行，零本地 RAM） |
| OpenClaw | 已安装 | 编排调度 + Telegram 通知 |

### 3.3 实际 RAM 观察（PolyGo 项目，6 agent 并行）

| 进程 | 内存占用 |
|------|---------|
| macOS + 杂项 | ~3GB |
| OpenClaw Gateway | ~300MB |
| Claude Code × 3（plan/frontend/review） | ~1.2GB |
| Codex CLI × 2（codex-1 + codex-2） | ~400MB |
| 项目文件 + 编译 | ~2-3GB |
| **合计** | **~7.2GB，剩余 ~8.8GB 余量** |

---

## 4. Agent 角色与分工

### 4.1 模型选择原则

**Claude Code（贵，只用在需要深度推理的地方）：**
- 规划 / 架构决策 / 需求分析 → `cc-plan`
- 文档更新 → `cc-plan`
- **对外产品前端**（`ui_quality=external`，有真实用户的界面）→ `cc-frontend`
- 审查 Codex 写的后端代码 → `cc-review`

**Codex（多账号，额度充足，能用 Codex 就用 Codex）：**
- 后端实现 → `codex-1/2`
- **内部工具前端**（`ui_quality=internal`，管理后台/自用界面）→ `codex-1`（不单独开 `codex-frontend` session）
- 测试 → `codex-test`
- 部署 → `codex-deploy`
- 审查前端代码 → `codex-review`

### 4.2 Agent 配置与命名规则

**固定 Session（永不自动创建/销毁）：**

| Agent | tmux 会话 | 工具 | 职责 |
|-------|----------|------|------|
| **规划师** | `cc-plan` | Claude Code | 分析需求，拆解任务，确定里程碑和依赖 |
| **后端审查** | `cc-review` | Claude Code | 审查 Codex 写的后端代码（full review） |
| **前端审查** | `codex-review` | Codex | 审查前端代码（full/scan review） |

**动态 Session（按 swarm 生命周期维护）：**

| Agent | tmux 会话 | 工具 | 职责 | 上限 |
|-------|----------|------|------|------|
| **Codex 工程师 1~4** | `codex-1` ~ `codex-4` | Codex | 后端逻辑、API、策略引擎、DB、内部工具前端 | 4 |
| **外部前端** | `cc-frontend-1/2` | Claude Code | 对外产品页、高 UI 质量场景 | 2 |
| **测试** | `codex-test` | Codex | 里程碑单元测试 + 验收脚本 | 1 |
| **部署** | `codex-deploy` | Codex | 构建 + Nginx 部署 + 通知 | 1 |

> **命名规则写死**：不要手动改名，这是系统约定。

> **实战经验：** PolyGo 这类 internal UI 直接走 `codex-1`，把 Claude 额度留给 review 和 plan 更划算。

### 4.3 前端模型选择规则

`cc-plan` 在规划阶段输出 `ui_quality` 字段，编排层自动按此选模型：

```
ui_quality = "internal" → codex-1（管理后台、运营工具、数据看板）
ui_quality = "external" → cc-frontend（对外产品、用户界面、Landing page）
```

判断标准只有一条：**是否有真实用户看到**。没有真实用户看到的内部界面，一律按 `internal` 处理。

### 4.4 任务分配规则

```
后端逻辑 / API / 策略引擎 / DB / WebSocket  → codex-1 或 codex-2
内部管理后台 / 数据看板                       → codex-1
对外产品页 / 高 UI 质量页面                  → cc-frontend
规划 / 分析 / 方案设计                        → cc-plan
Codex 代码审查                               → cc-review
前端代码审查                                  → codex-review
里程碑测试（单元测试 + 验收脚本）             → codex-test
构建 + 部署                                   → codex-deploy
```

### 4.5 交叉 Review 规则

```
Codex 写的代码（后端）  → cc-review（Claude Code 审查）
前端代码               → codex-review（Codex 审查）
```

### 4.6 完成后清理规则

```
任务完成 → on-complete.sh 同步 agent-pool 状态
  检查 agent-pool.json 里的 tmux session 是否还活着
  已消失 session → 标记为 dead
  全部任务完成 → 自动关闭所有动态 session → 触发 codex-deploy
```

---

## 5. 任务生命周期

### 5.1 完整流程（v4 — 里程碑测试 + Nginx 部署）

```
Phase 1: 需求输入
  人类通过 Telegram 描述需求
  ↓
Phase 2: 规划
  小明 → cc-plan: 分析需求，输出结构化任务列表（JSON）
  产出: task id, scope, files, dependencies, review_level, milestone, estimated_minutes
  同时定义 milestones[]：每个里程碑包含 task_ids + test_scope
  同时输出 ui_quality: "internal" | "external"（决定前端用哪个模型）
  ↓
Phase 3: 项目初始化（首次）
  install-hooks.sh 安装 git post-commit hook（含编译门禁）
  配置 hooks.enabled + hooks.token（OpenClaw webhook）
  配置 swarm/notify-target + swarm/hook-token
  ↓
Phase 4: 任务注册
  写入 active-tasks.json，包含 milestones[] + tasks[]
  自动计算初始状态（pending/blocked）
  ↓
Phase 5: 派发执行
  dispatch.sh → flock 加锁 check-and-set 标记 running → 派发到 tmux agent
  自动附加：force-commit 兜底 + on-complete 回调 + heartbeat（防误报卡住）
  → Telegram 通知人类："🚀 T00X 已派发到 codex-1"
  可并行：文件 scope 不重叠的任务同时进行
  ↓
Phase 6: 编译门禁
  Agent commit → post-commit hook → tsc --noEmit + ESLint
  ├→ 全部通过 → git push + 写信号 + Telegram ✅
  └→ 失败 → git reset --soft（回退保留代码）
            → Telegram ❌ + 写 fail 信号 → Agent 继续修复
  ↓
Phase 7: 自动调度（全自动）
  Agent 命令结束 → on-complete.sh（幂等键去重）：
    1. update-task-status.sh 原子更新（flock + check-and-set）
    2. milestone-check.sh 检查当前里程碑是否全部 done
    3. POST /hooks/agent 触发隔离 agent turn（sonnet 模型）
    4. 隔离 agent 验证 scope → 按 review_level 处理 → dispatch 下一个 pending 任务
    5. deliver: true → Telegram 通知人类结果
  ↓
Phase 8: Review（仅 full 级别）
  full 🔴 → 隔离 agent 派 cross-review → 通过才标 done
  scan 🟡 → 隔离 agent 看 diff → 无明显问题确认 done
  skip 🟢 → 验证 scope 即 done
  ↓
Phase 9: 里程碑测试（milestone-check 触发）
  里程碑内全部任务 done → milestone-check.sh 触发 codex-test
  codex-test：
    1. 跑验收脚本（verify-phaseX.ts）
    2. 对 test_scope 内的模块写单元测试并跑通
    3. 汇报结果：pass → 里程碑 test_status = passed
               fail → 定位失败任务 → 返回对应 agent 修复
  ↓
Phase 10: 最终部署
  全部里程碑 test_status = passed → 触发 codex-deploy：
    git pull → npm run build → rsync 到 Nginx web root → nginx reload
    → Telegram："✅ 全部完成！测试地址：https://polygo.doai.run"
```

### 5.2 状态流转

```
pending → running → (按 review_level)
                   ├→ [skip/scan] → done
                   └→ [full] → reviewing → done
                                        ↘ running (修改)
              ↘ failed → retrying → running
                       ↘ escalated（通知人类）
blocked → pending（前置 done 后自动解锁）
```

### 5.3 Plan 三层规范

**三层分工：**

| 层 | 产出 | 负责方 |
|----|------|--------|
| Requirements | 需求文档 `docs/requirements/` | 编排层（C 档复杂任务） |
| Design | 设计文档 `docs/design/` | cc-plan（需代码探索时）；否则编排层直接写 |
| Plan / 任务拆解 | 任务列表、swarm prompt `docs/swarm/` | 永远由编排层负责 |

> cc-plan 定位收窄为"探索代码库 → 输出 docs/design/"，不负责需求整理和任务拆解。

**三档判断：**

```
A 档：目标和路径清楚 → 不写文档，prompt 直接放 docs/swarm/
B 档：目标清楚但方案需设计 → 写 docs/design/
C 档：复杂模糊，需求不确定 → 先写 docs/requirements/，再写 docs/design/
```

**文档目录（两个 repo 统一结构）：**

```
docs/
├── requirements/   ← C 档需求文档
├── design/         ← 设计文档（B/C 档）
└── swarm/          ← swarm prompt 和任务分析
```

---

## 6. 任务拆解原则

### 6.1 粒度标准

```
太粗 ❌  "实现交易模块"
         → agent 自由发挥，改一堆文件，commit 不原子

刚好 ✅  "新建 clob-ws.ts，实现 WebSocket 连接 + 心跳 + 缓存"
         → scope 明确，1-3 个文件，一个 commit 能说清

太细 ❌  "在 ws-client.ts 第 42 行加一个 try-catch"
         → 没必要用 agent，小明直接 edit 就行
```

### 6.2 拆解要素

每个原子任务必须包含：

| 要素 | 说明 | 示例 |
|------|------|------|
| **id** | 唯一标识 | T001 |
| **domain** | backend / frontend | backend |
| **scope** | 新建/修改/删除哪些文件 | create: clob-ws.ts |
| **description** | 一两句话说清楚 | 实现 CLOB WS 行情订阅客户端 |
| **technical_notes** | 技术细节 | 基于 ws-client.ts 封装... |
| **depends_on** | 前置任务 | [T001] |
| **review_level** | full / scan / skip | scan |
| **estimated_minutes** | 预估耗时 | 45 |

### 6.3 Review Level 分配指南

| Level | 适用场景 | 示例 |
|-------|---------|------|
| 🔴 `full` | 资金相关、签名认证、交易执行、风控、策略逻辑 | 下单API、止损逻辑 |
| 🟡 `scan` | 集成代码、数据持久化、中等复杂度 | WS客户端、DB CRUD |
| 🟢 `skip` | UI页面、脚本、CLI工具、低风险CRUD | 管理页面、验收脚本 |

---

## 7. 原子化提交策略

### 7.1 Conventional Commits 规范

```
feat:     新功能
fix:      修复 bug
refactor: 重构（不改变行为）
docs:     文档
test:     测试
chore:    构建/工具/依赖
```

### 7.2 Commit Message 格式

```
<type>(<scope>): <description>

feat(clob-ws): implement CLOB WebSocket orderbook client
fix(order-execution): improve nonce generation and type validation per review
feat(web-admin): add accounts management page and API
```

### 7.3 原子性要求

```
✅ 一个 commit 只解决一个问题
✅ 每个 commit 的项目都应该能编译通过
✅ commit 后立即 push（post-commit hook 自动处理）
✅ commit message 清晰描述变更内容

❌ 一个 commit 里既加功能又改 bug
❌ 一个 commit 改了 10 个不相关的文件
❌ commit message 是 "update" 或 "fix stuff"
```

### 7.4 实战数据

PolyGo 项目 18 个任务产出 24 个 commit（含 review 修复），平均每个 commit 200-400 行代码，scope 清晰可追溯。

---

## 8. 并行开发模型

### 8.1 策略：文件隔离并行

不同 agent 改不同文件，可以同时运行：

```
codex-1:      polygo-daemon/src/providers/clob-auth.ts
codex-2:      polygo-daemon/src/persistence/order-store.ts, position-store.ts
cc-frontend:  polygo-web-admin/src/app/accounts/

三组文件完全不重叠 → 零冲突风险 → 三路并行
```

### 8.2 并行规则

```
✅ 可以并行
  codex-1 改 providers/ + codex-2 改 persistence/ + cc-frontend 改 web-admin/
  T004(认证) + T007(持久化) + T018(账号页面) — 实测成功

❌ 不能并行
  两个 agent 同时改 src/types/index.ts
  两个 agent 同时改同一模块的不同文件
```

### 8.3 最大并行度

实测 PolyGo 项目：**3 路并行**（2 codex + 1 cc-frontend）效果最佳。
- 后端有 2 个 codex 轮流/并行，关键路径缩短 30%
- 前端 1 个 cc-frontend 足够（前端任务一般较少）
- 更多并行受限于依赖关系而非 agent 数量

---

## 9. 事件驱动监控

### 9.1 架构（v4 — Webhook + 双门禁 + 动态 Agent 管理）

```
┌─────────────────────────────────────────────────────────┐
│ 主路径（零延迟，全自动闭环）                               │
│                                                         │
│ Agent commit → post-commit hook                         │
│   → tsc --noEmit 编译检查（仅检查改动文件的错误）          │
│   ├→ 编译失败 → git reset --soft HEAD~1（回退，保留代码） │
│   │            → Telegram 通知 "❌ 编译失败"              │
│   └→ 编译通过 → ESLint 检查（web-admin 改动文件）         │
│       ├→ ESLint 失败 → git reset --soft HEAD~1           │
│       │               → Telegram 通知 "❌ ESLint 失败"   │
│       └→ ESLint 通过 → git push（自动）                  │
│                       → 写 commit 信号                   │
│                       → POST /hooks/wake                 │
│                       → Telegram 通知 "✅ Commit: ..."   │
│                                                         │
│ Agent 命令结束 → on-complete.sh                          │
│   → update-task-status.sh（原子更新状态 + tokens + 解锁） │
│   → update-agent-status.sh（标 agent idle）              │
│   → 同步 agent-pool 活性；全部完成时触发 cleanup           │
│   → POST /hooks/agent（触发隔离 agent turn）             │
│     → 隔离 agent（sonnet 模型）验证 scope                 │
│     → 按 review_level 处理                               │
│     → 自动 dispatch 下一个 pending 任务                   │
│     → deliver: true → Telegram 通知结果                  │
│   → Token 里程碑预警（5万/10万/20万 input tokens）        │
│   → Telegram 任务完成通知（含 token 消耗）                │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ 兜底路径（HEARTBEAT.md）                                  │
│                                                         │
│ health-check.sh: 检测卡住(>15min)/死亡/静默退出的 agent  │
│ 定期检查 signal 文件有无未处理事件                         │
└─────────────────────────────────────────────────────────┘
```

### 9.2 完整脚本一览

**核心流水线：**

| 脚本 | 触发方式 | 作用 |
|------|---------|------|
| `dispatch.sh` | 编排层调用 | 标记 running + 标 agent busy + tee 捕获输出 + **prompt 写 tmpfile（避免 shell 转义问题）** + force-commit + on-complete 回调 |
| `on-complete.sh` | agent 命令结束时 | 解析 token + 更新状态 + 标 agent idle + 同步 `agent-pool.json` 活性 + 全部完成时触发 cleanup + **直接 system event 唤醒主 session** + 里程碑预警 + **swarm 总汇报** + Telegram 通知 |
| `update-task-status.sh` | on-complete / dispatch 调用 | 原子更新 active-tasks.json（状态 + commit + tokens + **同步 blocked→pending 自动解锁**） |
| `update-agent-status.sh` | dispatch / on-complete 调用 | 更新 agent-pool.json 单个 agent 的 idle/busy/dead 状态 |
| `parse-tokens.sh` | on-complete 调用 | 解析 agent 输出 log，支持 Claude Code / Codex 两种格式，输出 JSON |
| `install-hooks.sh` | 项目初始化一次 | 安装 post-commit hook（tsc + ESLint 双门禁 + 自动 push） |

**Swarm 收尾与巡检：**

| 脚本 | 触发方式 | 作用 |
|------|---------|------|
| `check-memory.sh` | 手动调用 | 读取可用 RAM；ok(>4GB) / warn(2~4GB) / block(<2GB) |
| `health-check.sh` | HEARTBEAT.md 触发 | 巡检所有 running 任务：检测卡住(>15min)/死亡/静默退出 |
| `cleanup-agents.sh` | on-complete（全部完成时）| 关闭所有动态 session；保留 cc-plan/cc-review/codex-review |

### 9.3 主 Session 通知（v2.5 简化方案）

> **v2.5 重大变化：** 去掉了 `/hooks/agent` webhook 这一跳，改为直接唤醒主 session。

**on-complete.sh 完成后的调度链路：**

```
任务完成
  ↓
update-task-status.sh 原子更新（含自动解锁 blocked→pending）
  ↓
openclaw system event --text "Done: $TASK_ID $TASK_NAME" --mode now
  （直接唤醒主 session，主 session 负责 review + 派发下一个）
  ↓
openclaw message send → Telegram 备用通知
```

**为什么从 webhook 改为 system event（2026-03-19 重构）：**
- webhook `/hooks/agent` 链路不可靠（实测完成率 ~50%）：webhook agent 是隔离 session，读不到主 session 历史，派发决策质量差
- system event 直接唤醒主 session，主 session 有完整上下文，可靠性提升到 ~95%
- update-task-status.sh 内置同步解锁：task done → 立即把依赖它的 blocked 任务翻为 pending，无需 webhook agent 中转

**swarm 全部完成时的总汇报：**

on-complete.sh 在所有任务标为 `done` 时，自动发一条汇总通知：

```
✅ Swarm 全部完成！
项目: PolyGo | 任务: 18 完成 | Commits: 24 个
Tokens: input 715k / output 42k / cache_read 1.2M
```

用 `/tmp/agent-swarm-complete/*.sent` 做幂等去重，最后几个任务并发完成时不重复发。

### 9.4 编译门禁

post-commit hook 在 push 之前执行 `tsc --noEmit`：

```
Agent commit → hook 触发
  → 检测改动文件属于哪个子项目（polygo-daemon / polygo-web-admin）
  → 对该子项目执行 tsc --noEmit
  → 只检查改动文件的报错（忽略预存在的类型缺失如 @types/pg）
  ├→ 有新错误 → git reset --soft HEAD~1
  │            → 代码保留在工作区，agent 可以继续修
  │            → 写 compile_fail 信号
  │            → Telegram 通知 "❌ 编译失败，已回退"
  └→ 无新错误 → 正常 push
```

**设计要点：**
- **soft reset** 而不是 hard reset — 保留工作区让 agent 继续修复
- **只查新错误** — 不被项目预存在的类型问题干扰
- **按子项目检查** — monorepo 中只编译受影响的部分

### 9.5 ESLint 门禁（web-admin）

tsc 通过后，对 `polygo-web-admin` 的改动文件运行 ESLint：

```
commit 中有 polygo-web-admin/*.ts(x) → cd polygo-web-admin
  → npx eslint --max-warnings=0 <改动文件列表>
  ├→ 通过 → 继续执行
  └→ 失败 → git reset --soft HEAD~1
           → Telegram 通知 "❌ ESLint 失败，已回退"
           → 写 eslint_fail 信号
```

**设计要点：**
- **只检查改动文件** — 不全量扫，秒级完成
- **`--max-warnings=0`** — warning 也算失败，强制干净代码
- **daemon 不跑** — polygo-daemon 无 ESLint 配置，不强加
- **顺序：tsc → ESLint → push** — 两道门禁都过才推送

### 9.5 信号文件格式

`/tmp/agent-swarm-signals.jsonl`，每行一个 JSON：

```jsonl
{"event":"commit","hash":"eb332f6","message":"feat(clob-auth): ...","files":"clob-auth.ts","time":1773746092}
{"event":"task_done","task":"T004","session":"codex-1","exit":0,"commit":"eb332f6","tokens":{"input":8432,"output":1205,"cache_read":3100,"cache_write":0},"time":1773745951}
{"event":"compile_fail","hash":"abc1234","message":"feat(engine): ...","errors":"tsc failed in polygo-daemon","time":1773746100}
{"event":"eslint_fail","hash":"def5678","message":"feat(accounts): ...","time":1773746200}
```

### 9.7 Swarm 配置文件

```
~/.openclaw/workspace/swarm/
├── active-tasks.json     # 任务状态（update-task-status.sh 原子维护）
├── agent-pool.json       # Agent 注册表（spawn/cleanup/health-check 维护）
├── notify-target         # Telegram chat_id
├── project-dir           # 当前项目路径
└── hook-token            # Webhook 认证 token
```

**agent-pool.json 结构：**

```json
{
  "limits": {
    "max_codex": 4,
    "max_cc_frontend": 2,
    "min_free_memory_mb": 2048,
    "stuck_timeout_minutes": 15
  },
  "naming": {
    "codex_pattern": "codex-{1..4}",
    "cc_frontend_pattern": "cc-frontend-{1..2}",
    "fixed_sessions": ["cc-plan", "cc-review", "codex-review"]
  },
  "agents": [
    {
      "id": "codex-1",
      "type": "codex",
      "domain": "backend",
      "tmux": "codex-1",
      "status": "busy",
      "current_task": "T003",
      "spawned_at": "ISO8601",
      "last_seen": "ISO8601"
    }
  ]
}
```

### 9.8 对比：四代演进

| 维度 | v1 cron 轮询 | v2 事件驱动 | v3 Webhook + 门禁 | v4 动态 Agent 管理 |
|------|-------------|-----------|-------------------|-------------------|
| 延迟 | 最多 3 分钟 | 秒级 | 秒级 | 秒级 |
| 调度 | 需要唤醒主 session | system event（不可靠） | /hooks/agent（可靠） | 同 v3 |
| 状态更新 | 手动 | 手动 | 脚本自动（原子） | 同 v3 |
| 编译检查 | 无 | 无 | tsc 门禁 | tsc + ESLint 双门禁 |
| 忘 commit | 需要人工发现 | 需要人工发现 | dispatch.sh force-commit | 同 v3 |
| Token 消耗 | 每次轮询消耗 | 仅事件时消耗 | 仅事件时 | 同 v3，+ 任务级追踪 |
| Agent 数量 | 固定 | 固定 | 固定 | 动态按需扩容/缩容 |
| 内存保护 | 无 | 无 | 无 | check-memory.sh 守卫 |
| Session 清理 | 手动 | 手动 | 手动 | 任务完成后自动关闭 |
| 健康巡检 | 无 | 无 | 无 | health-check.sh（15min） |

---

## 10. Review 分级制度

### 10.1 三级 Review

每个任务在规划阶段标注 `review_level`，决定完成后的验证深度：

| Level | 标记 | 适用场景 | 处理流程 | Token 消耗 |
|-------|------|---------|---------|-----------|
| `full` | 🔴 | 资金安全、核心逻辑、安全关键 | 派 cross-review agent，必须 pass | 高 |
| `scan` | 🟡 | 集成代码、持久化、中等复杂 | 编排层读 git diff，快速人工判断 | 低 |
| `skip` | 🟢 | UI 页面、脚本、CLI、低风险 | 仅验证 scope，直接 done | 零 |

### 10.2 Full Review 流程

```
Agent 完成 → 编排层验证 scope
  ↓
dispatch.sh 派 cross-review agent（附 diff 内容）
  ↓
Review agent 输出：Critical / High / Low / Suggestion
  ↓
无 Critical/High → Pass → 标记 done
有 Critical/High → Fail → 返回原 agent 修改 → 最多 3 轮
  ↓
3 轮不过 → 换 agent → 最多 2 轮
  ↓
仍不过 → escalate 给人类
```

### 10.3 Scan Review 流程

```
Agent 完成 → 编排层验证 scope
  ↓
编排层执行 git diff HEAD~1 读关键函数
  ↓
无明显问题 → done
有明显问题 → 返回 agent 修改
```

### 10.4 实战数据（PolyGo 项目）

18 个任务的 review 分布：
- 🔴 full × 6（T004 T006 T008 T010 T011 T012）— 全部资金/交易相关
- 🟡 scan × 5（T001 T002 T005 T007 T014）— 集成/持久化
- 🟢 skip × 7（T003 T009 T013 T015 T016 T017 T018）— UI/脚本

**效果：** 省了约 60% 的 review token 消耗，同时关键代码仍有完整审查保障。

---

## 11. 失败与重试策略

### 11.1 重试链

```
原 agent 尝试 × 3
  ↓ 全部失败
换 agent 尝试 × 2
  ↓ 仍然失败
通知人类介入

总计：最多 5 次自动尝试
```

### 11.2 失败类型与处理

| 失败类型 | 处理方式 |
|---------|---------|
| Agent 写完但不 commit | dispatch.sh 的 force-commit 自动补提交 |
| 编译失败 | post-commit hook 自动回退（soft reset），agent 可继续修 |
| Agent 改了 scope 外的文件 | `git revert` + 重新派发更精确的 prompt |
| Agent 报错退出 | 分析错误，调整 prompt 重试 |
| Review 不通过 | 将 review 意见追加到 prompt，返回修改 |
| 需求本身不明确 | 升级给人类确认 |

### 11.3 实战案例

**T006 订单执行（PolyGo）：** codex-1 第一次实现后，cc-review 发现 nonce 生成和类型校验有问题。自动返回 codex-1 修改，产出 `fix(order-execution): improve nonce generation and type validation per review`，第二轮通过。

**T001 CLOB WS（PolyGo）：** codex-1 完成代码但没有执行 git commit。编排层检测到文件存在但未提交，手动补 commit。**教训：** prompt 中要明确强调 `git add -A && git commit && git push`。

---

## 12. 权限边界

### 12.1 编排层可自主决定

- 回答 agent 的技术问题
- 重试失败任务（调整 prompt）
- Revert 有问题的 commit
- 手动补 commit（agent 忘了提交）
- 调整任务优先级
- 选择用哪个 agent 执行任务
- 标记 skip/scan 级别任务为 done

### 12.2 必须问人类

- **需求不明确** — 设计意图模糊
- **涉及密钥** — .env、API key、私钥
- **5 次重试失败** — 当前方案无法解决
- **架构大改动** — 模块拆分、技术栈变更
- **删除重要文件或数据**

### 12.3 通知策略

```
每次派发通知：
  "🚀 T006 已派发到 codex-1"

每次完成通知：
  "🔔 T006 完成 (exit=0) — commit eb332f6"

立即通知：
  涉及密钥 / 需要设计决策 / 5 次重试失败

汇总通知：
  "✅ 全部 18 个任务完成！"

静默处理（不通知）：
  回答 agent 技术问题 / scan review 通过 / 正常重试
```

---

## 13. 任务状态持久化

### 13.1 文件位置

```
~/.openclaw/workspace/swarm/active-tasks.json   # 当前任务
~/.openclaw/workspace/swarm/notify-target        # Telegram chat_id
~/.openclaw/workspace/swarm/project-dir          # 项目路径
/tmp/agent-swarm-signals.jsonl                   # 事件信号（运行时）
```

### 13.2 数据结构

```json
{
  "project": "PolyGo",
  "repo": "github.com/ayao99315/PolyGo",
  "updated_at": "ISO8601",
  "tasks": [
    {
      "id": "T001",
      "name": "CLOB WS 行情客户端",
      "domain": "backend",
      "agent": "codex-1",
      "tmux": "codex-1",
      "status": "done",
      "review_level": "scan",
      "note": "已完成，465行代码",
      "commits": ["f28f10a"],
      "issue": null,
      "depends_on": [],
      "created_at": "ISO8601",
      "updated_at": "ISO8601",
      "attempts": 1,
      "max_attempts": 3,
      "tokens": {
        "input": 8432,
        "output": 1205,
        "cache_read": 3100,
        "cache_write": 0
      }
    }
  ]
}
```

### 13.3 状态枚举

| 状态 | 含义 |
|------|------|
| `pending` | 依赖已满足，待派发 |
| `blocked` | 等待前置任务完成 |
| `running` | Agent 正在执行 |
| `reviewing` | 交叉 review 中（仅 full 级别） |
| `done` | 完成 |
| `failed` | 失败（已达最大重试次数） |
| `escalated` | 已升级给人类处理 |

### 13.4 自动解锁规则

当任务标记 `done` 时，扫描所有 `blocked` 任务。若其 `depends_on` 列表中的任务全部为 `done`，自动翻转为 `pending`。

---

## 14. 配置文件体系

### 14.1 三层配置

```
层1: Skill（项目无关，可复用）
  ~/.openclaw/workspace/skills/agent-swarm/
  ├── SKILL.md                      # 技能说明与完整流程
  ├── scripts/
  │   ├── dispatch.sh               # 派发包装器（running + busy + tee + force-commit + 回调）
  │   ├── on-complete.sh            # 完成回调（tokens + 状态 + idle + pool 活性同步 + cleanup + webhook）
  │   ├── update-task-status.sh     # 原子更新 active-tasks.json（状态 + tokens + 解锁）
  │   ├── update-agent-status.sh    # 更新 agent-pool.json 单个 agent 状态
  │   ├── parse-tokens.sh           # 解析 agent 输出 log 的 token 用量
  │   ├── install-hooks.sh          # 安装 post-commit hook（tsc + ESLint + 自动 push）
  │   ├── check-memory.sh           # 检查可用 RAM（ok >4GB / warn 2~4GB / block <2GB）
  │   ├── health-check.sh           # 巡检所有 running agent（卡住/死亡/静默退出）
  │   ├── cleanup-agents.sh         # 任务全完成后关闭动态 session，保留固定 session
  └── references/
      ├── prompt-codex.md           # Codex prompt 模板（含质量规则 + 常见错误表）
      ├── prompt-cc-plan.md         # 规划 prompt 模板
      ├── prompt-cc-frontend.md     # 前端 prompt 模板（含防超额完成规则）
      ├── prompt-cc-review.md       # Review prompt 模板
      └── task-schema.md            # 任务 JSON schema + review_level 定义

层2: Workspace（编排层行为规则）
  ~/.openclaw/workspace/
  ├── AGENTS.md                     # 多 agent 工作流规则
  ├── HEARTBEAT.md                  # 兜底巡检（webhook 的 backup）
  └── swarm/
      ├── active-tasks.json         # 运行时任务注册表（update-task-status.sh 维护）
      ├── agent-pool.json           # Agent 注册表（spawn/cleanup/health-check 维护）
      ├── notify-target             # Telegram 通知目标 chat_id
      ├── project-dir               # 当前项目路径
      └── hook-token                # Webhook 认证 token

层3: 项目 Repo（项目特定）
  project/
  ├── CLAUDE.md                     # Agent 操作手册
  └── .git/hooks/post-commit        # 事件驱动 hook（含编译门禁 + 自动 push）

层4: OpenClaw Gateway 配置
  ~/.openclaw/openclaw.json
  hooks.enabled: true               # 启用 webhook 端点
  hooks.token: "<secret>"           # Webhook 认证
  hooks.allowRequestSessionKey: true # 允许固定 sessionKey
```

---

## 15. Prompt 模板规范

### 15.1 四条铁律

| 规则 | 错误做法 | 正确做法 |
|------|---------|---------|
| **引用实际文件** | "使用 pg 连接数据库" | "参考 `src/persistence/db.ts` 的 `getPool()` 模式" |
| **commit 命令写死** | "使用 Conventional Commits" | `git add -A && git commit -m "feat(engine): implement risk control" && git push` |
| **scope 列具体路径** | "改 providers 目录" | "创建 `src/providers/clob-auth.ts`" |
| **禁止列表要具体** | "不要改其他文件" | "不要修改: package.json, src/types/index.ts, game-runner.ts" |

### 15.2 统一结构

```markdown
## Project
[项目名] — [一句话描述]
Working directory: [绝对路径]

## Task
[ID]: [一句话描述]
⚠️ 只做这一个任务。[前端模板特有：不要顺手修改或创建其他页面]

## Scope (strict — ONLY touch these files)
- Create: [完整相对路径]
- Modify: [完整相对路径]
- 禁止修改: [列出容易被误改的关键文件]

## Reference Code (必填)
请先阅读以下文件了解项目模式：
- `[path/to/similar-module.ts]` — [展示什么模式]
- `[path/to/types.ts]` — [需要用到的类型]

## Technical Requirements
[具体技术要求]

## Do NOT
- 修改 scope 以外的任何文件
- 不要修改: [具体文件列表]
- 不要添加 npm 依赖（除非下面 Allowed Dependencies 明确列出）
- [其他禁止事项]

## Commit (直接复制执行)
git add -A && git commit -m "[预写好的 message]" && git push

## Done When
[具体完成标准]
```

### 15.3 常见错误与预防

| 错误 | 原因 | 预防 |
|------|------|------|
| Agent 用错 DB 驱动 | Prompt 描述技术栈而非引用代码 | Reference Code 指向实际 db.ts |
| Agent 改了 package.json | 自己决定加依赖 | 禁止修改列表明确包含 |
| Agent 不 commit | 忘了或被其他输出打断 | commit 命令写死 + dispatch.sh force-commit 兜底 |
| cc-frontend 超额完成 | 看到占位页面自己补了 | 加 ⚠️ "只做当前任务" |
| Commit message 不规范 | Agent 自由发挥 | 直接给出完整 git commit 命令 |
| Agent 改了共享 types | 觉得需要扩展类型 | 禁止修改列表包含 types 文件 |

---

## 16. 信任阈值模型

| 场景 | 信任度 | 行为 |
|------|--------|------|
| skip 级别任务完成 | 高 | 验证 scope 即标 done |
| scan 级别 + diff 无异常 | 高 | 标 done |
| full 级别 + review pass | 高 | 标 done |
| full 级别 + review 有 Low issues | 中 | 记录 issues，标 done |
| 任何级别 + review 有 Critical/High | 低 | 返回修改 |
| 涉及 .env / 密钥 / DB schema | 零 | 必须人类确认 |

---

## 17. 成本与资源分析

### 17.1 月度成本

| 项目 | 成本 | 说明 |
|------|------|------|
| Claude Code Max | 已有 | 含 extra usage $37.50/月 |
| Codex Pro/Business | 已有 | gpt-5.4 high |
| Mac Mini 电费 | ~¥30/月 | 24/7 运行 |
| **总增量成本** | **≈ ¥0** | |

### 17.2 实际效率（PolyGo 项目实测）

| 指标 | 数值 |
|------|------|
| 总任务数 | 18 |
| 总 commit 数 | 24（含 review 修复） |
| 总耗时 | ~2 小时（从规划到全部完成） |
| 人类介入次数 | 3 次（确认开始、讨论 review 策略、检查进度） |
| 并行度 | 最高 3 路（2 codex + 1 cc-frontend） |
| Token 消耗（Codex） | ~13 万 tokens |
| Token 消耗（Claude Code） | 周额度 13%（session 额度用完后切 extra usage） |

---

## 18. 实战经验与教训

### 18.1 ✅ 有效的做法

1. **dispatch.sh 包装器** — 自动标 running + 完成回调 + force-commit 兜底
2. **post-commit hook 自动 push** — agent 不再忘记 push
3. **review 分级** — 只对资金相关代码做 full review，省 60% token
4. **codex-2 扩展** — 后端关键路径并行，明显加速
5. **Telegram 实时通知** — 人类不用反复问"进度如何"
6. **Webhook 自动调度** — `/hooks/agent` 触发隔离 agent，全自动闭环
7. **编译门禁** — tsc 检查改动文件，失败自动回退
8. **ESLint 门禁** — web-admin 改动文件过 ESLint，--max-warnings=0，失败自动回退
9. **update-task-status.sh** — 脚本层原子更新状态，不等 AI 编排层
10. **Token 追踪** — parse-tokens.sh 解析 agent 输出，写入 tasks.tokens，里程碑预警
11. **上下文隔离** — --print/exec 每任务新进程 + --no-session-persistence，零跨任务污染
12. **最高权限** — CC bypassPermissions + Codex dangerously-bypass，无确认弹窗
13. **Swarm 收尾自动化** — on-complete.sh 同步 agent-pool 活性，cleanup-agents.sh 在全部任务完成后自动收尾
14. **健康巡检** — health-check.sh 每 heartbeat 检测卡住/死亡 agent，自动 Telegram 告警

### 18.2 ❌ 踩过的坑与修复（全历史）

所有升级按版本分阶段记录，每个问题均来自真实踩坑，不是猜测。

#### v1 → v2：从 cron 轮询到事件驱动（PolyGo 首次实战后）

| 问题 | v1 状态 | v2 修复 |
|------|---------|---------|
| 监控延迟高 | cron 每 3 分钟轮询 tmux 输出，延迟可达 3 分钟 | ✅ post-commit hook + on-complete.sh，任务完成秒级响应 |
| 无自动 push | Agent commit 后需手动 push | ✅ post-commit hook 自动执行 git push |
| 调度需要人工唤醒 | 完成后要手动告知编排层派发下一个 | ✅ on-complete.sh 自动触发下游流水线 |
| 通知不可靠 | openclaw system event 触发 heartbeat，回复 target-none | ✅ 改用 openclaw message send 直发 Telegram |
| 无任务注册表 | 任务状态只在编排层 AI 脑子里，session 重启就丢 | ✅ active-tasks.json 持久化任务状态 |
| Agent 不 commit | 代码写完但没执行 git commit（T001 实际踩坑） | ⚠️ 当时靠 prompt 强调，不可靠 |
| Prompt 技术栈描述错误 | 说"用 SQLite"但项目实际用 pg（PolyGo 真实踩坑） | ✅ 铁律：prompt 引用实际代码文件，不描述技术栈 |
| cc-frontend 超额完成 | 做了 T016 但当时没派给它（自己补了没派的任务） | ✅ 接受结果 + prompt 加 ⚠️ "只做当前任务" |

#### v2 → v2.1：Webhook + 编译门禁（稳定性加固）

| 问题 | v2 状态 | v2.1 修复 |
|------|---------|----------|
| Agent 不 commit | prompt 强调但不可靠 | ✅ dispatch.sh 在 agent 命令结束后自动 force-commit 兜底 |
| system event target-none | 用 message send 绕过，但只能通知，不能触发调度 | ✅ 改用 /hooks/agent webhook，触发隔离 agent turn，全自动闭环 |
| 调度仍需 AI 主 session 在线 | on-complete 只能通知，下一步派发需要主 session 响应 | ✅ webhook agent 用独立 session + sonnet 模型自主调度 |
| 无编译检查 | Agent commit 了有错的代码也会 push | ✅ post-commit hook tsc --noEmit，失败自动 git reset --soft 回退 |
| 状态跟踪滞后 | 需要 AI 编排层手动更新 active-tasks.json，可能漏更新 | ✅ update-task-status.sh 脚本原子更新，不依赖 AI 手动操作 |
| Agent 权限弹窗卡住 | Claude Code 遇到敏感操作弹确认，无人值守时卡死 | ✅ Claude Code --permission-mode bypassPermissions，Codex --dangerously-bypass |

#### v2.1 → v2.2：ESLint + Token 追踪 + 上下文隔离

| 问题 | v2.1 状态 | v2.2 修复 |
|------|----------|----------|
| 前端代码质量无检查 | 只有 tsc，lint 问题溜进 repo | ✅ post-commit hook 对 web-admin 改动文件跑 ESLint --max-warnings=0，失败自动回退 |
| 不知道每个任务烧了多少 token | 只有 session 级别统计，看不出哪个任务贵 | ✅ parse-tokens.sh 解析 agent 输出 log，写入 tasks[].tokens 字段（Claude Code / Codex 两种格式都支持） |
| 快烧完额度前毫无感知 | 到了 limit 才知道 | ✅ on-complete.sh 累计 input tokens 阈值预警（5万/10万/20万） |
| 跨任务上下文累积 | agent session 复用导致前一个任务的代码 / 报错污染下一个 | ✅ CC 用 --print（每次新进程），Codex 用 exec --full-auto + --no-session-persistence，零跨任务污染 |

#### v2.3 → v2.4：模型分层 + 里程碑测试 + 部署

| 问题 | v2.3 状态 | v2.4 修复 |
|------|----------|----------|
| 编排层绕过 dispatch.sh 直接 exec Codex | 无约束，偶尔发生 | ✅ SKILL.md 铁律：swarm 项目内一律走 dispatch.sh，禁止直接 exec |
| 前端模型固定用 Claude Code | 不管内部/外部页面都用 CC，费额度 | ✅ `ui_quality` 字段：internal→codex-1，external→cc-frontend |
| 没有里程碑级测试 | 验收脚本靠人手动跑 | ✅ milestone-check.sh + codex-test agent |
| 没有自动部署 | 人工 build + 部署 | ✅ codex-deploy + Nginx + Cloudflare Tunnel（polygo.doai.run）|

#### v2.2 → v2.3：动态 Agent 管理 + 健康巡检

| 问题 | v2.2 状态 | v2.3 修复 |
|------|----------|----------|
| 内存判断靠感觉 | 增加额外 agent 前没有统一判断标准 | ✅ check-memory.sh 提供统一阈值：<2GB block，2~4GB warn，>4GB ok |
| 不知道 agent 是否还活着 | 卡住的 agent 无人发现，任务悬空 | ✅ health-check.sh 每 heartbeat 检测卡住(>15min)/死亡/静默退出，自动 Telegram 告警 |
| 任务完成后旧 session 堆积 | 需要手动关闭 tmux session | ✅ cleanup-agents.sh 全部任务完成后自动关闭动态 session，保留 cc-plan/cc-review/codex-review |
| agent 命名不统一 | 随手叫 codex-a、codex-worker1 等 | ✅ 命名规则固化：codex-{1..4} + cc-frontend-{1..2}，系统约定不可改 |
| agent 状态无持久化 | 编排层 AI 靠记忆判断 agent 是否 busy | ✅ agent-pool.json 持久化 agent 状态（idle/busy/dead），脚本原子更新 |

#### v2.4 → v2.5：dispatch 链路简化 + prompt-file 修复 + swarm 汇报（2026-03-19）

| 问题 | v2.4 状态 | v2.5 修复 |
|------|----------|----------|
| webhook 链路不可靠 | `/hooks/agent` 触发隔离 agent turn，实测完成率 ~50%；隔离 session 无上下文，派发决策质量差 | ✅ 去掉 webhook，on-complete.sh 改为 `openclaw system event` 直接唤醒主 session，可靠性提升到 ~95% |
| blocked→pending 解锁需要 webhook agent 中转 | webhook agent 读 active-tasks.json 再解锁，有延迟且不可靠 | ✅ update-task-status.sh 内置同步解锁：task done 时立即扫描 blocked 任务，全部依赖满足则直接翻为 pending |
| dispatch.sh --prompt-file 引号转义地狱 | prompt 含 markdown/代码块/引号时，bash 层层转义导致 agent 收到乱码或 command not found | ✅ dispatch.sh 将 prompt 写入 tmpfile，agent 通过 stdin 管道读取，彻底绕开 shell 转义 |
| macOS tmpfile 不唯一 | `mktemp "/tmp/...XXXXXX"` 在 macOS 下不替换 XXXXXX，临时文件冲突 | ✅ 改为 `mktemp "/tmp/agent-swarm-prompt-${TASK_ID}-${SESSION}.XXXXXX.txt"` 格式，macOS/Linux 均兼容 |
| swarm 全部完成无汇总 | 每个任务单独通知，最后一批并发完成时没有全局汇报 | ✅ on-complete.sh 检测所有任务 done 时，发总汇报（项目/任务数/commit 数/token 汇总），用 sent 文件做幂等去重 |

#### v2.6：Plan 三层规范 + 文档目录结构（2026-03-20）

- 新增 Plan 三档规范（A/B/C），明确 Requirements/Design/Plan 三层分工
- cc-plan 定位收窄为"探索代码库 → 输出 docs/design/"，不负责需求和任务拆解
- 两个 repo 建立统一 docs/requirements/ docs/design/ docs/swarm/ 目录
- 新增 references/prompt-requirements.md 需求文档模板
- 新增 scripts/swarm-new-batch.sh 批次管理脚本

### 18.3 📈 未来改进方向

1. **多项目支持** — swarm 配置按项目隔离，agent-pool.json 支持多 project context

---

## 19. 参考资料

### 19.1 Elvis — OpenClaw Agent Swarm

**文章：** [OpenClaw + Codex/ClaudeCode Agent Swarm: The One-Person Dev Team](https://x.com/elvissun/status/2025920521871716562)

**我们采纳的：** OpenClaw 编排层、任务注册表、交叉 review
**我们没采纳的：** Worktree + PR 模式（我们用主干开发）

### 19.2 Peter Steinberger — Moltbot/Clawdbot

**文章：** [日均上百 commit：Moltbot 如何兼顾产品路线图和开发速度](https://x.com/wquguru/status/2016685995090153800)

**我们采纳的：** 主干开发、原子提交、Conventional Commits、4 agent 并行
**Peter 的信任阈值：** Codex 95% / Claude 80% / 其他 70%

---

> **文档版本：** v2.6
> **创建日期：** 2026-03-16
> **更新日期：** 2026-03-20（v2.6: 新增 Plan 三层规范 5.3 节 + v2.6 实战教训条目）
> **维护者：** 小明（OpenClaw Agent）
> **状态：** ✅ 实战验证 + 复盘改进完成
