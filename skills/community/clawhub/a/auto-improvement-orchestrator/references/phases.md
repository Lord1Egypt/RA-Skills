# Phases — 路线图与里程碑

**版本**: v0.3  
**状态**: `generic-skill` P0 已从 skeleton 推进到 first runnable version，并接入 Phase 1 minimal evaluator evidence

---

## Phase 1: generic-skill first runnable version（已完成 P0）

### 目标
把 `generic-skill` lane 从“能讲设计”推进到“能真实跑 proposer → critic → executor → gate”。

### 当前已完成
- [x] `propose.py`：可读目标路径 + 简单 feedback 来源，输出 candidate artifact
- [x] `score.py`：可对 candidate 打分、排序、给 recommendation
- [x] `execute.py`：可执行低风险 Markdown 文案追加，产出 diff + backup
- [x] `gate.py`：可输出 `keep / pending_promote / revert / reject`
- [x] 持久化状态目录：`candidate_versions / rankings / executions / receipts / state`
- [x] 状态文件：`current_state.json / pending_promote.json / veto.json / last_run.json`
- [x] 输出字段对齐 control-plane-friendly 结构：`stage / status / next_step / next_owner / truth_anchor`
- [x] 已完成低风险目标 skill 的端到端演示

### 当前已知边界
- 只自动执行 `docs/reference/guardrail`
- 只支持简单 Markdown 追加
- `prompt/workflow/tests` 仍以 `hold/reject` 为主
- 已有 Phase 1 minimal evaluator evidence adapter，但还没有真正跑 benchmark / hidden tests / external regression

### Phase 1 成功标准（已达成）
- 能真实生成 candidate/ranking/execution/gate receipt
- 能写状态文件而不是只在聊天里描述状态
- 能保守地 keep 低风险文档修改
- 能把非自动 keep 的候选分流到 pending/reject

---

## Phase 2: richer judge + safer auto-promotion（下一步）

### 目标
把当前“纯规则 critic”升级成“规则 + evaluator 证据”的混合判断。

### 计划交付
- [x] Phase 1 minimal integration：把 `skill-evaluator` 的 rubric / category / boundary 证据接入 Critic 输出与混合打分
- [ ] full `skill-evaluator` adapter（真实调用 evaluator CLI / benchmark / hidden tests）
- [ ] 更细粒度 protected target policy
- [ ] docs/reference 之外的更多低风险动作
- [ ] 基础 smoke checks / benchmark hook
- [ ] pending_promote 的人工晋升接口

### 成功标准
- `hold` 和 `reject` 的区别更稳定
- low-risk 文档候选的 keep 更可信
- Critic 输出包含可被后续控制面消费的 evaluator/evidence 字段
- pending_promote 能被后续控制面继续消费，而不是停在 JSON 文件

---

## Phase 3: multi-lane orchestration 接入

### 目标
把当前 generic-skill lane artifact 接上更完整 orchestration/control-plane。

### 计划交付
- [ ] macro lane 接口统一
- [ ] browser-workflow lane 接口统一
- [ ] lane 级 run arbitration / 锁
- [ ] pending/veto 统一查看面板
- [ ] 外部审批/回调通道

### 成功标准
- 多 lane 共用统一 artifact 协议
- 控制面可基于 `truth_anchor` + `next_owner` 自动推进
- 不再依赖人工到处翻聊天记录找状态

---

## 当前结论

现在的 `generic-skill` lane 已经不是纸面设计：

> 它已经有真实候选、真实排序、真实执行、真实 gate 与真实状态文件。

但它仍然是**保守的第一版**：
- 先把推进面做实
- 再把 judge 能力做强
- 最后再扩复杂自动修改面
