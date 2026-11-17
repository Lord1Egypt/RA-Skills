# Decision Object Schema（统一决策对象 · v2.5.0 状态机版）

## 定位
所有 Mode 最终输出结构化的 Decision Object（机读 JSON），作为 single source of truth。它驱动 Decision Memory、Recall、统计报表、机构学习。不是自然语言报告。

> **v2.5.0 核心升级**：从"单一 recommendation + 综合分"升级为**投资状态机**——保留每个 Gate 的独立状态（Gate-specific state），不只有 Overall；每个核心断言绑定 Evidence Object（含 Verification Status）。

## Schema 规范
```json
{
  "decision_id": "string (UUID)",
  "mode": "screening | evaluation | ic | portfolio",
  "project_id": "string",
  "project_name": "string",
  "timestamp": "ISO8601",
  "owner": "string (决策人/复核人)",

  "gate_status": {
    "mandate": "pass | conditional | watch | fail",
    "quality": "pass | conditional | watch | fail",
    "compliance": "pass | conditional | watch | fail",
    "value": {
      "valuation_3a": "pass | conditional | watch | fail",
      "return_3b": "pass | conditional | watch | fail",
      "exitability_3c": "pass | conditional | watch | fail"
    },
    "industrial": "pass | conditional | watch | fail"
  },
  "overall": "pass | conditional | watch | fail",

  "mandate_violations": ["string"],
  "market_sanity": "exist | alive | timing_ok | unknown",
  "deal_killer_flags": ["string (K1/K2/K3/K4 触发项)"],

  "evidence_objects": [
    {
      "claim": "string (核心断言)",
      "evidence": "string (证据描述)",
      "quality": "E1 | E2 | E3 | E4 | E5",
      "relevance": "direct | indirect | contextual",
      "scope": "string (证据能证明什么，不能证明什么)",
      "verification_status": "verified | partially_verified | unverified | contradicted",
      "decision_impact": "string (该证据如何影响判定)"
    }
  ],

  "thesis_ledger": [
    {
      "thesis": "string (投资命题)",
      "support": ["string (支持证据)"],
      "counter": ["string (反证证据)"],
      "status": "verified | partially_verified | unproven | not_yet_proven"
    }
  ],

  "kill_factors": [
    {
      "factor": "string (可证伪命题)",
      "trigger": "string (触发阈值)",
      "consequence": "fail | re_price | watch | downgrade"
    }
  ],

  "valuation_range": { "low": "number", "base": "number", "high": "number" },
  "return_range": { "moic_bear": "number", "moic_base": "number", "moic_bull": "number", "irr_range": "string" },
  "assumption_register": [
    { "name": "string", "value": "string", "source": "string", "type": "observed | derived | assumption | model_estimate", "date": "string", "confidence": "string", "sensitivity": "string" }
  ],

  "why_not": "string (反事实结论：不投会怎样/纯财务投资是否成立)",
  "recommendation": "YES | NO | WATCH | Invest | Wait | Track | Pass",
  "confidence": "high | medium | low",
  "confidence_block": {
    "evidence_confidence": "high | medium | low | mixed",
    "assumption_confidence": "high | medium | low | mixed",
    "model_confidence": "high | medium | low | mixed",
    "decision_confidence": "high | medium | low",
    "uncertainty_sources": ["string (决策相关的缺口)"],
    "sensitivity_note": "string (当前结论对哪些假设高度敏感)"
  },
  "decision_critical_assumptions": [
    { "assumption": "string", "impact_on_decision": "critical | high | medium", "uncertainty": "high | medium | low", "current_support": "string (证据支撑程度)", "validation_priority": "P0 | P1 | P2" }
  ],
  "evidence_conflicts": [
    { "claim": "string", "conflict_type": "口径差异 | 方向冲突", "sources": [ { "source": "string", "value": "string", "evidence_level": "E1-E5" } ], "reconciliation": "string (未调和写 待确认)", "decision_impact": "string" }
  ],
  "dd_priority": { "p0": ["string"], "p1": ["string"], "p2": ["string"] },
  "memory_tier": "A | B | C",
  "key_evidence": ["string (≤3)"],
  "key_risks": ["string (≤3)"],
  "reason": "string (决策理由摘要)",
  "next_action": "string (下一步行动)",
  "next_required_evidence": "string (解除 CONDITIONAL/WATCH 需要的证据)",
  "artifact_type": "screening_card | investment_assessment | ic_package | portfolio_review",
  "linked_decisions": ["decision_id"],
  "ic_resolution": {
    "decision": "invest | wait | track | pass",
    "agent_recommendation": "proceed_dd | invest | wait | track | pass",
    "override": true | false,
    "divergence_reason": "string (override=true 时必填)",
    "conditions": ["string"]
  },
  "outcome": "string (投后实际结果，决议后回填)",
  "disclaimer": "分析建议 · 非投资决定 · 需 IC 审议"
}
```

## 字段约束
| 字段 | 必填（各 Mode） | 说明 |
|------|----------------|------|
| decision_id / mode / project_id / timestamp | 全部 | 主键与时间 |
| gate_status / overall | Evaluation+ | **Gate-specific state（v2.5.0 核心）**，不只有 Overall |
| mandate_violations / deal_killer_flags | Screening+ | 硬约束 + Hard Killer 触发项 |
| evidence_objects | Evaluation+ | 核心断言 + 证据双维 + Verification Status |
| thesis_ledger / kill_factors | Evaluation+ / IC | 反证系统 |
| valuation_range / return_range / assumption_register | IC | Value Gate + 假设登记 |
| recommendation | 全部 | 核心决策（唯一 Owner） |
| confidence / reason / next_action | 全部 | 决策支撑 |
| next_required_evidence | Evaluation+ / IC | 解除 CONDITIONAL/WATCH 的证据（由 dd_priority 派生摘要）|
| linked_decisions | Recall 时 | 历史关联 |
| ic_resolution / outcome | IC 回填 | IC 实际决议（结构化）/ 投后结果 |
| confidence_block / decision_critical_assumptions | Evaluation+ / IC | 决策可信层（v2.6.2）：四层置信度 + Top3 关键假设 |
| evidence_conflicts | Evaluation+ / IC | 证据冲突登记与调和（v2.6.2）|
| dd_priority | Evaluation+ / IC | DD 优先级 P0/P1/P2（v2.6.2）|
| memory_tier | 全部 | 记忆分级 A/B/C（v2.6.2）|

## 设计要点
- `gate_status` 是**状态机核心**：每个 Gate 独立存状态（Gate-specific state），`overall` 由**预定义 Precedence Rules** 推导（任一 FAIL → Overall 不得 PASS），**不做跨 Gate 数学排序、不是数学平均**（Compliance WATCH ≠ Valuation WATCH）
- `evidence_objects` 支撑"可判定、可追溯"：Claim → Evidence → Level → Decision Impact，Verification Status 防止 E5 升级为"已验证事实"
- `assumption_register` 让关键数字可溯源，防止"企业预测"变"Agent 预测"变"Investment Case"
- `recommendation` 是各 Mode 的唯一核心决策，不出现第二个独立决策字段
- 所有 Artifact 内容必须能从 Decision Object 推导

## 状态机一屏视图（IC 速览，P2）

> **输出压缩原则**：内部判定复杂，外部呈现高度压缩。IC 一屏速览（由 gate_status 自动推导）：

```
Mandate PASS · Quality PASS · Compliance WATCH · Value CONDITIONAL（3A WATCH / 3B WATCH / 3C CONDITIONAL）· Industrial PASS
Overall：CONDITIONAL（可进入 DD，不构成 IC 投资承诺）
Confidence：72%（Medium）
Next Evidence：audited financial + IP legal opinion
```

- 每个 Gate 状态必须来自 `gate_status` 字段，**不得另造一个综合分**（权限隔离）
- `Overall` 后必须附一句话判断（可压缩为一句投资判断，见输出压缩原则）

---

## 四件套对象族（v2.6.0，Closed-Loop）

> 把单向 Decision Object 扩成四件套，支撑 `Decision → Monitoring → Outcome → Learning → Recall → Next Decision` 闭环。schema 见下，工作流见 `mode-portfolio.md`。

### Monitoring Object（决定之后盯什么，投资后立即生成）
```json
{
  "monitor_id": "string (UUID)",
  "decision_id": "string (关联投前 Decision Object)",
  "kill_factor_trackers": [
    { "factor": "string", "trigger": "string", "status": "active | hit | cleared", "last_check": "ISO8601" }
  ],
  "milestones": [
    { "name": "string", "target": "string", "due": "ISO8601", "status": "pending | on_track | delayed | met | missed" }
  ],
  "key_assumption_trackers": [
    { "name": "string", "forecast": "string", "status": "on_track | diverging | failed" }
  ],
  "review_cadence": "monthly | quarterly | semi_annual",
  "next_review": "ISO8601",
  "review_history": [
    { "review_date": "ISO8601", "states": { "thesis": "unchanged | weakened | strengthened", "evidence": "new | expired | contradicted | none", "assumption": "up | down | unchanged", "gate": "unchanged | degraded | improved", "kill_factor_distance": "string" } }
  ]
}
```

### Outcome Object（后来实际发生了什么，Review / 退出时回填）
```json
{
  "outcome_id": "string (UUID)",
  "decision_id": "string",
  "actual": { "revenue": "number", "customers": "number", "gross_margin": "number", "valuation": "number" },
  "variance": { "revenue_vs_forecast": "string", "arpu_vs_forecast": "string", "gm_vs_forecast": "string" },
  "attribution": ["string (偏差归因：需求/采购结构/竞争/执行/运气)"],
  "decision_outcome": "correct | partially_correct | wrong",
  "decision_attribution": "agent_right | ic_right | both_right | both_wrong | pending",
  "kill_factor_outcome": [ { "factor": "string", "hit": true | false } ],
  "recorded_at": "ISO8601"
}
```

### Learning Object（这次结果改变了我们什么认知，Outcome 后派生）
> **铁律**：不得写成"表现良好/不佳"，必须绑定 Thesis / Assumption / Evidence / Kill Factor。
```json
{
  "learning_id": "string (UUID)",
  "decision_id": "string",
  "outcome_id": "string",
  "what_was_right": ["string (哪个 Thesis 验证成立)"],
  "what_was_wrong": ["string (哪个 Thesis / Assumption 失败)"],
  "failed_assumptions": [ { "assumption": "string", "error": "string" } ],
  "misleading_evidence": [ { "evidence": "string", "why_misleading": "string" } ],
  "updates": ["建议（供专家治理，Agent 不自动改权重/规则）：calibrate_soft_score | adjust_comparable_weight | update_assumption_prior"],
  "created_at": "ISO8601"
}
```

### 四件套关系
- **Decision Object** →（投资）→ **Monitoring Object** →（周期复盘）→ **Outcome Object** →（派生）→ **Learning Object** → 写入 **Decision Memory** →（Recall）→ **下一次 Decision Object**
- `outcome_id` / `learning_id` 挂回 `decision_id`，保证"当时判断 → 实际结果 → 认知更新"全程可追溯
- Outcome / Learning Object 与 Decision Memory 同隐私边界：本地存储，不外发，导出需 IC 秘书人工审批

### Forecast → Actual 链路（P1，校准基线）
- Decision Object 的 `assumption_register` / `valuation_range` / `return_range` 即 **Forecast 基线**（投前承诺的可检验数字）
- Outcome Object 的 `variance` 必须逐项与 Forecast 基线对比（`revenue_vs_forecast` / `arpu_vs_forecast` / `gm_vs_forecast`），偏差必须归因（Attribution）
- **任何 Decision Object 缺失可对比的 forecast 字段 → 标记"缺校准基线"**，防止"预测不可检验"（没有基线就没有 Calibration）

---

## v2.6.2 新增字段说明（可信判断 / 人机协同 / 记忆质量）

### confidence_block（四层置信度，推导不平均）
- 回答"Agent 到底有多确定"，把「项目不好」与「还不知道项目好不好」分开。
- **Decision Confidence 推导规则（不加权平均，延续权限隔离哲学）**：
  - 任一 `decision_critical_assumptions` 的 `uncertainty = high` → `decision_confidence` 上限 **medium**；
  - 存在 `evidence_conflicts` 未调和（`reconciliation = 待确认`）且属 decision-critical → `decision_confidence` 上限 **medium**；
  - **Hard Gate = WATCH/CONDITIONAL 不作机械降级**：仅当该 Gate 对应事项属于 Decision-Critical Assumption、或对当前 Recommendation 有实质性影响时，才纳入 `uncertainty_sources` 并约束置信度。Confidence 是**决策相关的不确定性**，不是所有缺口的数量统计。

### decision_critical_assumptions（Top3，敏感性 ≠ 风险）
- 只找"哪一个假设一变，项目就不成立"的 Top3（从 `assumption_register` 抽取，不重复造数）。
- 四字段区分两个不同问题：`impact_on_decision`（对结论的杠杆，**≠ 风险**）、`uncertainty`（证据强弱）、`current_support`（证据支撑程度）、`validation_priority`（进 dd_priority 的优先级）。
- 可同时出现"Exit Multiple：影响极高但市场证据充分 → 高敏感、低不确定性"与"客户转化率：影响中等但证据极弱 → 中敏感、高不确定性"。

### evidence_conflicts（冲突 → 调和 → Decision Impact）
- **conflict_type 两分**：口径差异（同指标不同数值 → 取保守口径/标注待确认）vs 方向冲突（证据指向相反命题 → Thesis 降级/标记 misleading evidence）。
- 未调和冲突不得写成"已确认"；Base Case 不采用未经验证的高值。

### dd_priority（DD 优先级）
- `p0`（不能证明则不能继续）/ `p1`（显著改变 Value/Return）/ `p2`（补充信息）；`next_required_evidence` 为其派生摘要。

### memory_tier（记忆分级，全部 Capture、分级入 Recall）
- A Institutional Case（完整 DD/IC/Outcome，人工确认后升级）/ B Decision Memory（明确 reason + 关键证据）/ C Screening Signal（仅结构化标签，不进主要 Recall）。
- **事实完整度只触发"升级建议"，Agent 不得自主升级为 A**——升级由专家治理确认（延续 Calibration 只报告不改规则的哲学）。

### ic_resolution（结构化）与 decision_attribution（Decision Attribution）
- `ic_resolution` 记录"Agent 建议 vs IC 决议 + 是否 override + 分歧原因 + 条件"，让 IC 之后"Agent 怎么判断 → 人怎么修改 → 为什么修改"全程可追溯。
- `decision_attribution`（Outcome Object）：**必须基于预先定义的 Outcome Criterion 判定，不得仅依最终公司表现倒推（防 hindsight bias）**；无法明确归因保持 `pending`。
