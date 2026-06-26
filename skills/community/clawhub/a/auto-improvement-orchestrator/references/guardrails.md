# Guardrails — generic-skill lane（first runnable version）

**版本**: v0.2  
**状态**: 第一版 guardrails 已落到可运行脚本

---

## 1. 当前 guardrail 目标

第一版不是追求“自动改一切”，而是确保：

1. 只放行**低风险**候选自动执行
2. 每次修改都能**追溯**
3. 不满足 keep 条件时能进入：
   - `pending_promote`
   - `reject`
   - `revert`
4. 已修改文件在必要时能**恢复 backup**

---

## 2. Executor 当前允许什么

### 允许自动执行
- `docs`
- `reference`
- `guardrail`

且当前仅支持：
- Markdown 文案追加（`append_markdown_section`）

### 明确不自动执行
- `prompt`
- `workflow`
- `tests`
- 任意代码/复杂逻辑变更
- 删除文件
- 对外契约调整

如果 candidate 属于不支持类别，Executor 必须返回：
- `unsupported`

而不是伪造成功。

---

## 3. Critic 推荐与 Gate 决策矩阵

### Critic recommendation

| recommendation | 含义 |
|---|---|
| `accept_for_execution` | 低风险且值得立即执行 |
| `hold` | 有价值，但当前版本不应自动 keep |
| `reject` | 收益不足或风险过高 |

### Gate decision

| 条件 | Gate 输出 |
|---|---|
| low-risk + docs/reference/guardrail + execution success/no_change | `keep` |
| critic = `hold` | `pending_promote` |
| critic = `reject` 且未改文件 | `reject` |
| critic = `reject` 且已改文件 | `revert` |
| execution failed / gate 不允许保留已改文件 | `revert` |

说明：
- `hold` 是“保留候选，等待更强 judge 或人工晋升”
- `reject` 是“当前直接否决”
- `revert` 是“工作树里已经有改动，因此先回滚”

---

## 4. Rollback 机制（当前已实现）

执行前：
- 先把目标文件 copy 到 `executions/backups/<run-id>/...`

执行后：
- execution artifact 会写入：
  - `backup_path`
  - `rollback_pointer`

Gate 若需要撤销：
- 使用 backup 恢复目标文件

当前第一版优先走 **backup restore**，而不是强绑定 git-only rollback。

---

## 5. 持久化风控状态

### `pending_promote.json`
记录需要后续人工/控制面晋升的候选：
- `run_id`
- `candidate_id`
- `category`
- `target_path`
- `recommendation`
- `receipt_path`

### `veto.json`
记录被 reject/revert 的候选：
- `run_id`
- `candidate_id`
- `decision`
- `reason`
- `receipt_path`

这两份文件就是第一版“自动编排推进能力”里的保守分流面。

---

## 6. 红线（第一版）

以下情况默认不 auto-keep：

1. `prompt` / `workflow` / `tests` / 代码类候选
2. 任何 medium/high risk 候选
3. protected target
4. 删除、重写、大段结构性改造
5. 修改对外行为/契约

---

## 7. 为什么当前默认保守

因为这一版的目标是：

> 先把状态推进、候选排序、执行记录、回滚指针都做成真实 artifact，
> 再逐步扩 executor/judge 能力。

所以当前策略是：
- **自动 keep 很窄**
- **pending/reject/revert 很明确**
- **不要用模糊“人工看看”替代状态文件**

---

## 8. 后续升级方向

下一阶段 guardrails 会补：
- frozen benchmark
- hidden tests
- richer protected target policy
- human approval receipt / review bus
- skill-evaluator adapter 证据接入
