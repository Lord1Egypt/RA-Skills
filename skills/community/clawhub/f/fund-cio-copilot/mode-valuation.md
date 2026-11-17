# Value Gate — 资本配置层（3A Valuation / 3B Return / 3C Exitability）

> v2.5.0 新增子 skill。定位：独立的资本配置决策层，回答**"这个价格值得投吗？"**
> 从旧 Financial 层抽离——旧架构"估值三情景 + IRR/MOIC"只有一行，导致丞士报告估值/回报论证缺失。

## 定位
Value Gate 是第五道 Hard Gate（值价），介于 Quality（值投）与 Industrial（能投）之间。**"估值合理" ≠ "回报可实现" ≠ "退出可落地"，三者独立判定，不得平均成"Value 72 分"。**

## 三个子 Gate（各自独立，结论独立保留）

### 3A Valuation — 当前价格是否合理？
- **三法估值**（给区间，不给单值）：
  1. Comparable：特种机器人 / 消防 / 工业 / 应急装备可比 PS / PE
  2. 简化 DCF / FCF：2026–2030 Revenue → Gross Margin → EBITDA → FCF
  3. Forward Exit Multiple：目标年收入 × 退出 PS
- **结论**：PASS / CONDITIONAL / WATCH / FAIL + 估值区间（low / base / high）
- **回答**："当前报价为什么在 / 不在区间内？"

### 3B Return — 风险调整后资本回报是否成立？
> **IRR 不等于回报质量。** 两个项目 Base IRR 28% vs 22%，前者若 IP 风险高/客户集中/现金流差，未必优于后者。

- **三情景回报**：Bear / Base / Bull → 投资额 → 退出价值 → 股权稀释 → MOIC / IRR
- **Risk-Adjusted Return**（必须纳入，不得只报裸 IRR）：
  - downside probability（下行概率）
  - dilution（股权稀释）
  - exit multiple（退出倍数）
  - execution probability（执行概率）
  - key risk（关键风险）
- **结论**：PASS / CONDITIONAL / WATCH / FAIL + MOIC / IRR 区间（bear/base/bull）

### 3C Exitability — 退出路径是否真实存在？
- 路径：IPO / 并购 / 下一轮 / 回购，各给**概率 + 时间窗**
- **结论**：PASS / CONDITIONAL / WATCH / FAIL
- **注意**：估值合理 + 增长强，但退出路径差 → 3A PASS / 3C FAIL，不得混成"Value 通过"

---

## 参数溯源（硬约束，P0-5）

> Risk-Adjusted Return 的所有概率参数，必须属于以下四类之一，且 **Model Estimate 不得伪装成事实**。

| 类型 | 含义 | 示例 |
|------|------|------|
| **Observed** | 历史/实际数据支持 | "同赛道 3 家被并购，均值 1.8x" |
| **Derived** | 明确公式推导 | "按 CAGR 25% 外推得 2028E 营收" |
| **Assumption** | 管理层/投资团队假设 | "管理层预计 2027E 收入 2.5 亿" |
| **Model Estimate** | 模型估算 | "模型估 execution probability 70%" |

- **Model Estimate 必须显式标注，不得写成事实**；无法溯源时写"估算，待验证"。

---

## Assumption Register（假设登记，P0-5）

> 每个关键数字必须带 `Value / Source / Type / Date / Confidence / Sensitivity`，让"企业预测"不悄悄变成"Agent 预测"再变成"Investment Case"。

登记表（每项至少一行）：
```
2027E Revenue = 2.5 亿
  Source：Management forecast / E5
  Type：Assumption
  Date：2026-08
  Confidence：Low（未独立验证）
  Sensitivity：若收入只达 80%（2 亿），MOIC 从 3.2x 降至 2.1x
```

必登项：Revenue（各年）/ Gross Margin / EBITDA Margin / Exit Multiple / 各概率参数 / Dilution / Terminal Value。

---

## Decision Sensitivity（Top3 关键假设，v2.6.2）

> 不是完整 Excel 建模，只找 **Top 3 Decision-Critical Assumptions**，回答"哪一个假设一变，这个项目就不成立"。

从 `assumption_register` 抽取 impact 最高的 Top3 输出 `decision_critical_assumptions`，四字段区分两个不同问题：

| 字段 | 回答的问题 |
|---|---|
| `impact_on_decision` | 该假设对 Recommendation 的杠杆（**敏感性 ≠ 风险**，杠杆高 ≠ 不确定）|
| `uncertainty` | 证据强弱（高 = 证据极弱）|
| `current_support` | 当前证据支撑程度（如"市场可比充分"/"仅管理层预测"）|
| `validation_priority` | 进 DD 优先级（P0/P1/P2）|

可同时出现：
> Exit Multiple：影响极高，但市场证据充分 → **高敏感、低不确定性**
> 客户转化率：影响中等，但证据极弱 → **中敏感、高不确定性**

这是两个完全不同的问题——前者是"结论对什么敏感"，后者是"哪里最不确定"。

---

## 输出：Value Gate 结论

```
【Value Gate · 资本配置层】
3A Valuation：PASS / CONDITIONAL / WATCH / FAIL
  估值区间：low X / base Y / high Z 亿
  理由：...
3B Return：PASS / CONDITIONAL / WATCH / FAIL
  三情景：Bear MOIC/IRR / Base MOIC/IRR / Bull MOIC/IRR
  Risk-Adjusted：downside p / dilution / exit multiple / execution p / key risk
3C Exitability：PASS / CONDITIONAL / WATCH / FAIL
  路径：IPO（p, 时间窗）/ 并购（p, 时间窗）/ 下一轮（p）/ 回购（p）

Assumption Register：见上（关键数字 + 溯源 + 敏感性）
参数溯源：各概率标 Observed / Derived / Assumption / Model Estimate

Value Gate 综合结论：3A / 3B / 3C 各自独立，不平均
（任一 FAIL → Value Gate FAIL，不被其余 PASS 覆盖）

Decision Sensitivity（Top3 关键假设）：
  1. Exit Multiple：影响 critical / 不确定性 low（市场可比充分）→ 高敏感低不确定
  2. 2027E Revenue：影响 high / 不确定性 high（E5 未独立验证）→ 高敏感高不确定
  3. Gross Margin：影响 medium / 不确定性 medium
  当前 Conditional 主要由 Exit Multiple 与 2027 Revenue 两项假设驱动

免责：分析建议 · 非投资决定 · 需 IC 审议
```

---

## 与五层 Soft Score 的关系（分层不回灌）
- 五层 Soft Score 的 Financial 层只评**财务质量**（收入确认/应收/毛利/现金流），**不评估值合理性**
- Value Gate 单独评估**价格与回报**，两者分两行呈现，不回灌
- Intrinsic Valuation（3A）与 Synergy Premium 分层叠加，但 **Anti-Subsidization**：Synergy 不得反向补贴不成立的 3A/3B/3C 结论
