# Mode 5 — Portfolio（投后管理 · Lifecycle Closure）

> v2.6.0 新增。定位：补上投资生命周期闭环——**Decision → Monitoring → Outcome → Learning → Recall → Next Decision**。
> 对应「投资后 → 退出 / 复盘」。唯一核心决策：**监测结论 / 建议动作——建议重新评估 / 建议维持当前判断 / 建议提交 IC 复核 / 记录 Outcome**（Agent 只给建议，不"决定继续持有"）。

## 定位
投前 Decision Object 回答"当时为什么这么决定"；Portfolio Mode 负责"决定之后盯什么、后来实际发生了什么、改变了我们什么认知"。**没有 Outcome 就没有 Calibration，没有 Calibration，Score 永远只是主观意见。**

> **边界（v2.6.0 收窄）**：Monitoring 只服务于**决策复核**（提醒投资经理重新评估 Thesis），**不是企业管理**——Agent 提醒"毛利率连续两季度低于 Base Case → 建议重新评估 Thesis"，而**不要求企业整改、不自动管理 Portfolio、不自动执行退出**。

## 异常驱动首页（Exception-driven UX，v2.6.0）

> 用户不是每天打开 Agent"重新分析所有项目"，而是问"**有什么事情值得我现在关注？**"。首页围绕"需要我决策什么"呈现状态表，而非全面投后报告。

```
需要我决策什么？
| 状态 | 项目 | 事件 | Agent 判断 | 建议 |
|------|------|------|-----------|------|
| 🔴 | 项目 A | IP 权属出现新证据 | Hard Gate 状态变化 | 重新 DD |
| 🟠 | 项目 B | 2027E 收入下修 18% | Return 接近下限 | 重新测算 |
| 🟡 | 项目 C | Kill Factor 接近触发 | Thesis 风险上升 | 关注 |
| 🟢 | 项目 D | 无重大变化 | Thesis 稳定 | 无需处理 |
```

- 触发源：Kill Factor Trigger 命中 / Milestone 到期 / Forecast 偏离阈值 / 外部事件
- 每行可下钻到 Portfolio Review Card（四问 + Outcome + Learning）

## 输入
- 历史 Decision Object（mode=ic / evaluation，含 `gate_status` / `kill_factors` / `thesis_ledger` / `assumption_register` / `valuation_range` / `return_range`）
- 项目进展数据（里程碑打卡 / 财务更新 / 返投落地 / 外部事件）

## 执行内容

### 1. Monitoring Plan（建立监测计划，投资后立即执行）
从投前 Decision Object 自动派生四类监测项（**只服务决策复核，不管理企业**）：
- **Kill Factors**：Trigger 逐一登记为自动跟进项（**命中 → 触发重评**）
- **KPI / Milestones**：对赌节点（收入 / 客户 / 产能 / 返投），打卡 + 到期
- **Review Cadence**：按项目风险设定节奏（高风险月度 / 常规季度 / 稳定半年）
- **Key Assumptions**：Assumption Register 中关键数字（如 2027E Revenue）成为验证对象

### 2. Periodic Review（周期复盘：Since Last Review + 四问）

#### Since Last Review（v2.6.2，变化量优先）
> 固定输出"上次以来发生了什么变化"，CIO 不用重读全项目，只看增量。支撑：Monitoring Object `review_history[]` 存每次 states 快照，本次与上次 diff。

```
Since Last Review（上次以来）：
  Thesis：unchanged / weakened / strengthened
  Evidence：new / expired / contradicted（列出）
  Assumption：up / down / unchanged（列出关键项）
  Gate：unchanged / degraded / improved
  Kill Factor：距 Trigger 的距离（如"毛利率 46%，距 Re-price 阈值 40% 尚 6pp"）
  Recommendation：unchanged / reconsider
```

每次 Review 必须回答（四问）：
1. **Triggered？**——Kill Factor Trigger / Milestone 是否命中
2. **Thesis still valid？**——当初投资命题（Thesis Ledger）是否仍成立
3. **Value assumptions changed？**——估值 / 回报关键假设是否变化（Forecast vs Actual）
4. **Risk / Compliance changed？**——风险与合规状态是否变化

任一关键项变化 → 输出"触发重评"建议，**自动发起 Evaluation 重跑**（先 Recall 历史，再重新判定，对比原 Decision Object 的 `gate_status` 变化）。

### Review Scheduler + Track 触发自动化（P2）
- **Review Scheduler**：按 Monitoring Object 的 `review_cadence` 自动安排 `next_review`；用户显式建立定时自动化（复用 Radar 基建）后可自动发起 Periodic Review
- **Track 重评触发**：recommendation.md 的 Track 建议必须附**结构化触发条件**（指标 + 阈值 + 检查频率），纳入 Monitoring Plan 自动跟进，避免"无限期观察"
- **权限**：自动 Review 仅在用户显式建立调度后执行（延续 Radar 的限自主执行模式，不产出投资决定）

### 3. Outcome 回填（Forecast → Actual → Variance → Attribution）
- **Actual**：实际结果（收入 / 客户 / 毛利 / 估值 / 里程碑）
- **Variance vs Forecast**：与投前 Base Case 的偏差
- **Attribution**：偏差归因（市场需求 / 采购结构 / 竞争 / 执行 / 运气）
- **Decision Outcome**：当初决策（Invest / Wait / Pass）事后对错
- **Kill Factor Outcome**：哪些 Kill Factor 命中 / 未命中（验证 Kill Factor 是否有预测力）

### 4. Learning Record（学习记录，绑定 Thesis / Assumption / Evidence / Kill Factor）
> **铁律**：不得写成"本项目表现良好 / 不佳"，必须绑定当初的命题与假设。

- **What was right**：哪个 Thesis 验证成立
- **What was wrong**：哪个 Thesis / Assumption 失败
- **Which assumption failed**：哪个 Assumption Register 数字偏差最大
- **Which evidence was misleading**：哪个 Evidence 产生虚假信号（如"客户覆盖数达标但 ARPU 远低于预测"→ 该 Evidence 只能证明覆盖，不能证明收入质量）
- **更新指令**：Calibrate（Comparable Recall 权重 / Assumption Prior / Soft Score 校准）

---

## 输出：Portfolio Review Card

```
【Portfolio Review Card】
项目：XXX ｜ 关联 Decision：decision_id
Review：第 X 次 ｜ 周期：YYYY-MM-DD

Monitoring Plan：
  Kill Factor 跟进：
    - IP 权属：active / hit（→ 触发重评）
    - 收入真实性：active / cleared
  Milestones：
    - 2026E 收入 1 亿：on_track / delayed / missed
    - 返投落地：on_track / delayed
  Review Cadence：quarterly ｜ Next：YYYY-MM

四问复盘：
  1. Triggered？：未命中 / 命中（列出）
  2. Thesis still valid？：T1 成立 / T2 需下调
  3. Assumptions changed？：ARPU 假设偏离（Forecast 10 万 → Actual 6 万）
  4. Risk / Compliance changed？：无变化 / IP 法律意见已出具

Outcome（Forecast → Actual → Variance → Attribution）：
  Actual：营收 1.2 亿 / 客户 30 家 / 毛利率 32%
  Variance：营收 +20% / ARPU -40% / 毛利率 -5pp
  Attribution：客户数超预期，但采购结构判断错误（低 ARPU 小单占比高）
  Decision Outcome：partially_correct
  Kill Factor Outcome：收入真实性未命中（核实无造假），毛利率触发 Re-price

Learning Record：
  What was right：消防客户拓展速度命题成立
  What was wrong：单客户收入质量假设失败
  Failed assumption：ARPU（Assumption Register #3）
  Misleading evidence：E5 客户覆盖数 → 不能推导收入质量
  更新：Assumption Prior 调整 / Soft Score 校准（Financial 层下调 ARPU 权重）

建议（监测结论 / 建议动作）：建议重新评估 / 建议维持当前判断 / 建议提交 IC 复核 / 记录 Outcome
免责：分析建议 · 非投资决定 · 需 IC 审议
```

---

## 强制 Capture（四件套）
- **Monitoring Object**：投资后立即生成（Kill Factor / Milestone / Cadence / Key Assumptions）
- **Outcome Object**：每次 Review / 退出时生成（Actual / Variance / Attribution / Decision Outcome / Kill Factor Outcome）
- **Learning Object**：Outcome 回填后派生（What was right / wrong / failed assumption / misleading evidence / 更新指令）

schema 见 `decision-object.md`（四件套对象族）。

> **隐私边界**：Outcome / Learning Object 属机构学习数据，本地存储，不外发（与 Decision Memory 同规则）；导出需 IC 秘书人工审批。
