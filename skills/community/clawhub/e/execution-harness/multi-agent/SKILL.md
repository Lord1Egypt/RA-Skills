---
name: multi-agent
version: 2.0.0
category: knowledge
description: 多 agent 协调设计模式。当需要选择 coordinator/fork/swarm 模式或设计跨 agent 协作时使用。不适用于工具重试（用 tool-governance）或上下文管理（用 context-memory）。参见 execution-loop（coordinator 持续执行）。
license: MIT
triggers:
  - multi agent
  - 多 agent
  - coordinator
  - fork vs swarm
  - agent coordination
  - workspace isolation
  - file conflict
author: OpenClaw Team
---

# Multi-Agent Coordination

多 agent 系统设计模式：委托模式选型、任务协调、并发控制、质量保障。纯设计指南。

## When to Use

- 选择 Coordinator/Fork/Swarm → Three delegation modes
- 多 agent 同时编辑同一文件 → File claim and lock
- 需要隔离工作空间 → Agent workspace isolation
- 协调者需要综合 worker 结果 → Synthesis gate

## When NOT to Use

- 只有 1 个 agent → 用 `execution-loop`
- 跨阶段知识传递 → 用 `context-memory`

---

## Patterns

### 4.1 Three Delegation Modes

三种模式各有适用场景：

| 模式 | 特点 | 适用 |
|------|------|------|
| **Coordinator** | Worker 从零开始，4 阶段（Research→Synthesis→Implementation→Verification） | 多阶段复杂任务 |
| **Fork** | Child 继承 parent 完整上下文和 prompt cache（首次调用只付 cache read 价格 $0.003/1K vs 全量 $0.036/1K），单层限制 | 需要 parent context 的子任务 |
| **Swarm** | 扁平名单，file-based mailbox，不能递归 spawn | 长期独立的同质工作流 |

不确定选哪个→ Coordinator，覆盖最广。Fork 限制：child 不能再 Fork、不能 clarify、不能 memory writes。 → [详见](references/delegation-modes.md)

### 4.2 Shared Task List Protocol

共享任务板 `.coordination/tasks.json`：

```json
{
  "tasks": [
    {"id": "t1", "description": "重构 auth 模块", "status": "pending", "claimed_by": null, "result": null}
  ],
  "updated_at": "2025-03-15T10:00:00Z"
}
```

四状态：`pending → claimed → done/failed`。领取任务通过原子锁 `mkdir ".coordination/tasks.lock"`（POSIX 上 mkdir 是原子操作），10 次重试，指数退避 50-500ms，释放用 `rmdir`。

Claude Code Swarm 使用 per-agent inbox `~/.claude/teams/{team}/inboxes/{agent}.json` 替代共享 tasks.json，减少锁竞争。 → [详见](references/task-coordination.md)

### 4.3 File Claim and Lock

编辑文件前写排他锁：

```json
// .claims/src_handlers_ts.lock（路径中 / 替换为 _）
{"session_id": "abc123", "file": "src/handlers.ts", "claimed_at": 1710489600, "expires_at": 1710490200}
```

- **10 分钟 TTL**（`expires_at = now + 600`），防 crash 死锁
- PreToolUse hook 拦截 Write/Edit，读 `tool_input.file_path`，检查 lock 是否被其他 session 持有且未过期
- 过期 lock 清理：`find .claims -name "*.lock" -mmin +15 -delete`

粒度是整个文件。需更细粒度→用 workspace isolation。 → [详见](references/file-claim-lock.md)

### 4.4 Agent Workspace Isolation

每个 worker 独立 git worktree：

```bash
git worktree add .worktrees/${WORKER_ID} -b work/${WORKER_ID} HEAD
claude -p --cwd .worktrees/${WORKER_ID} "..."
```

共享 .git 仓库但独立工作目录和 index，彻底消除并发冲突。代价是 merge 阶段冲突集中爆发。三种 merge 策略：`git merge --no-ff`（保留历史）、`cherry-pick`（只取最终结果）、`git diff main...branch > patch`（最安全，人工 review）。清理：`git worktree remove` + `git branch -d`。 → [详见](references/workspace-isolation.md)

### 4.5 Synthesis Gate

Research → Implementation 之间的强制关卡。**核心原则：coordinator must synthesize, not delegate understanding**。

Gate 脚本检查 `.coordination/synthesis.md`：
1. 文件存在且非空
2. 最少 10 行
3. 必含匹配 `Conclusion`、`Action Plan|Implementation Plan`、`Evidence|Rationale` 的 section

通过后 implementation worker 启动：`claude -p --max-turns 50 "$(cat .coordination/synthesis.md)"`。

把原始 research 结果直接转发给 implementation worker 是反模式。 → [详见](references/synthesis-gate.md)

### 4.6 Review-Execution Separation

Implementation 和 review 由两个隔离 session 的 agent 分别执行，盲审消除确认偏误。

- Implementation agent：`claude -p --max-turns 60`
- Review agent：`claude -p --max-turns 20`，只接收 `git diff main` 和任务描述，**不知道 implementation agent 的推理过程**
- Review 输出：`.coordination/review-result.json` 含 `{approved: bool, issues: [...], suggestions: [...]}`
- `approved == false` → issues 喂给一个**新** implementation session（不是原来那个），避免锚定

→ [详见](references/review-execution-separation.md)

### E4.x Extended Patterns

Cache-safe forking、完整 context 隔离、file-based mailbox（per-agent inbox JSON + lockfile）、permission delegation、结构化消息协议。 → [详见](references/extended-patterns.md)

## Workflow

选模式用决策树，选完后按对应路径执行。

```
需要多 agent？
├── Worker 需要 parent 已加载的 context？
│   └── 是 → Fork
│         · child 继承完整上下文 + prompt cache，首次调用只付 cache read 价格
│         · 单层限制：child 不能再 Fork
│         · 任务和 parent context 无关时别用 Fork，浪费 context 装无关内容
│
├── Workers 之间需要分阶段协调？
│   └── 是 → Coordinator（4 阶段）
│         1. Research — 多 worker 并行探索
│         2. Synthesis — coordinator 独占，综合所有结果产出 synthesis.md
│            （不可委派，不可跳过——直接转发原始结果会让下游无所适从）
│         3. Implementation — 按文件集分配，同文件串行防 merge conflict
│         4. Verification — 独立 review agent 盲审，不看 implementation 推理
│
└── 各自独立、同质任务？
    └── 是 → Swarm
          · 扁平名单：teammate 不能 spawn 新 teammate
          · 通过 file-based mailbox 通信（per-agent inbox JSON + lockfile）
          · 用 .coordination/tasks.json 共享任务状态
```

所有模式通用：每个 worker 分配独立 worktree（Pattern 4.4），编辑文件前写 claim lock（Pattern 4.3）。

<example>
场景: 15 个文件的跨模块重构（统一错误处理）— Coordinator 模式
Phase 1 — 研究: 3 个 worker 各自 worktree（`git worktree add .worktrees/r1 -b work/r1 HEAD`），并行扫描输出影响分析
Phase 2 — 综合: coordinator 独自消化 3 份报告，写 `.coordination/synthesis.md`（迁移方案 + 文件优先级 + 依赖顺序），gate 脚本验证含 Conclusion + Action Plan + Evidence
Phase 3 — 实现: 2 个 worker 按 synthesis 认领文件，编辑前写 `.claims/src_auth_ts.lock`（TTL 10min），防止并发编辑同一文件
Phase 4 — 审查: 1 个 review worker 只拿到 `git diff main` + 任务描述做盲审，输出 `.coordination/review-result.json`
结果: 15 文件迁移完成，0 冲突，审查一次通过
</example>

<example>
场景: 10 个 API endpoint 的测试补全 — Swarm 模式
任务同质（每个 endpoint 独立写测试），无需跨阶段协调。
`.coordination/tasks.json` 列出 10 个 pending 任务。5 个 worker 各自领取：`mkdir .coordination/tasks.lock`（原子），读 tasks.json 找 pending 项，改为 claimed，`rmdir .coordination/tasks.lock`。
每个 worker 在独立 worktree 工作，写完测试后标记 done。Coordinator 最后 merge 所有 worktree。
</example>

<anti-example>
错误: coordinator 收到 3 份 research 报告后直接说 "Based on your findings, fix it" 转发给 implementation worker
后果: 3 份报告有矛盾结论（Result 类型 vs exception），implementation worker 自己做了不一致的选择
违反: Pattern 4.5 — coordinator 跳过 synthesis，把判断责任下推给 worker
</anti-example>

<anti-example>
错误: 用 Fork 模式做需要递归委托的任务
parent Fork 出 child-A，child-A 想再 Fork child-B — 失败，Fork 只支持单层。
需要递归委托或多阶段协调 → 用 Coordinator。Fork 只适合 child 需要 parent context 的单层子任务。
</anti-example>

## Output

| 产物 | 路径 | 说明 |
|------|------|------|
| 任务清单 | `.coordination/tasks.json` | 所有 worker 的任务分配、状态、认领记录 |
| 综合文档 | `.coordination/synthesis.md` | coordinator 综合 worker 结果的结构化决策文档 |
| 文件锁 | `.claims/*.lock` | 每个 worker 编辑文件前写入的排他锁，防止并发冲突 |

## Related

- `execution-loop` — Ralph 持续执行循环，用于 coordinator 的长时间持续执行
- `context-memory` — handoff 文档，用于跨阶段（研究→综合→实现）的知识传递
- `tool-governance` — component-scoped hooks，用于给不同 worker 配置不同的工具权限
