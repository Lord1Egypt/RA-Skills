# Architecture — generic-skill lane（first runnable version）

**版本**: v0.2  
**状态**: `generic-skill` lane 已可运行；其他 lane 仍以规划为主

---

## 1. 总览

当前实现采用五角色顺序推进（与 SKILL.md 一致）：

```text
Generator -> Discriminator -> Evaluator -> Executor -> Gate
```

但重点不只是脚本能跑，而是**每一步都会落本地 artifact**，形成可被后续 control plane 消费的状态推进链。

---

## 2. 目录真值

`generic-skill` lane 的 artifact 根目录：

```text
$OPENCLAW_ROOT/shared-context/intel/auto-improvement/generic-skill/
├── candidate_versions/   # proposer 输出
├── rankings/             # critic 输出
├── executions/           # executor 输出 + backups/
├── receipts/             # gate receipt
└── state/
    ├── current_state.json
    ├── pending_promote.json
    ├── veto.json
    └── last_run.json
```

这套目录就是当前版本的**本地 control-plane-friendly 状态面**。

---

## 3. 各角色当前实现边界

### 3.1 Proposer

输入：
- `--target`
- 可选 `--source`（支持 memory / learnings / `.feedback` 的简单文本读取）

行为：
- 分析目标 skill/file 的 Markdown 结构
- 读取输入来源中的关键词/信号
- 生成 candidate 列表

当前能提出的 candidate 类型：
- `docs`
- `reference`
- `guardrail`
- `prompt`
- `workflow`
- `tests`

说明：
- `docs/reference/guardrail` 默认视为低风险优先候选
- `prompt/workflow/tests` 当前只进入候选池，不等于会自动执行

### 3.2 Critic

当前不是 LLM judge，而是**规则 + 启发式评分器**：
- 分类加权（docs/reference/guardrail 更高）
- 风险惩罚（low / medium / high）
- protected target 惩罚
- executor 是否支持 的惩罚/加分

输出：
- `score`
- `risk_penalty`
- `recommendation`
- `blockers`
- `judge_notes`

recommendation 当前三档：
- `accept_for_execution`
- `hold`
- `reject`

### 3.3 Executor

当前只支持非常保守的执行面：
- 低风险 Markdown 文案追加
- action 主要是 `append_markdown_section`

支持类别：
- `docs`
- `reference`
- `guardrail`

不支持：
- `prompt`
- `workflow`
- `tests`
- 任意复杂逻辑修改

执行结果会产出：
- `status`
- `modified`
- `diff`
- `diff_summary`
- `backup_path`
- `rollback_pointer`

### 3.4 Gate

Gate 读取 critic + executor 输出后做最终决策：
- `keep`
- `pending_promote`
- `revert`
- `reject`

当前保守策略：
- 只有 `docs/reference/guardrail` + `low risk` + 执行成功，才允许 `keep`
- `hold` 候选进入 `pending_promote`
- `reject` 候选直接进入 `reject` / `revert`
- 如果有已修改文件但不允许保留，优先恢复 backup

---

## 4. 状态模型

### 4.1 stage 字段

当前产物统一使用以下 stage：
- `proposed`
- `ranked`
- `executed`
- `gated`

状态文件内部的流程 stage：
- `proposed`
- `ranked`
- `executed`
- `gated_keep`
- `gated_pending`
- `gated_revert`
- `gated_reject`

### 4.2 control-plane-friendly 字段

所有关键 artifact / state 文件都尽量包含：
- `stage`
- `status`
- `next_step`
- `next_owner`
- `truth_anchor`
- `run_id`

这几个字段是为了后续接 orchestration/control-plane，而不是只服务人类阅读。

---

## 5. 状态文件职责

### `current_state.json`
当前真值锚点，描述：
- 当前 run
- 当前 stage/status
- 下一步应该由谁接手
- 当前 truth anchor 在哪里

### `last_run.json`
最新一次处理结果摘要，便于快速读取当前 lane 最近落点。

### `pending_promote.json`
存放 `hold -> pending_promote` 的候选，给后续人审或控制面晋升使用。

### `veto.json`
存放被 `reject/revert` 的候选和原因，形成 veto 记忆面。

---

## 6. 为什么说它已接入“自动编排推进思路”

当前版本还没有真正改 canonical orchestration repo，但已经对齐了关键编排约束：

1. **阶段推进真实存在**
   - proposer / critic / executor / gate 各自产生 artifact

2. **状态推进真实存在**
   - `current_state.json` / `last_run.json` 每步都更新

3. **待晋升/否决真实存在**
   - `pending_promote.json` / `veto.json` 不是纸面字段，而是可写状态文件

4. **真值锚点可追踪**
   - 每个阶段都能从 `truth_anchor` 找回对应 artifact

5. **后续控制面可读**
   - machine-readable JSON 优先，不把状态藏在聊天文本里

---

## 7. 当前仍未实现

- 冻结 benchmark / hidden tests
- richer adapter 协议
- 多 lane 共用调度器
- 并发锁 / run arbitration
- skill-evaluator 真正 judge 化接入
- 审批总线 / Discord review hook

换句话说，当前版本是：

> **generic-skill lane 已经能跑，而且产物结构已经对齐 control-plane；但“更智能的 judge”和“更完整的编排控制面”还没接上。**
