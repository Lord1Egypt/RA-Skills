# Mode 2 — Evaluation：Quality Gate + 五层 Soft Score

> 本子 skill 由现有「产业投资顾问」专家的五层分析逻辑**打包植入**，CIO Copilot 自包含运行，不连接外部专家。
> **v2.5.0 起：五层分析降为 Soft Score（无否决权），Quality Gate 的否决权只归 Hard Killers。**

## 定位
立项分析引擎。对应「200 立项 → 40 DD」。唯一核心决策：**建议 DD？YES / NO**。
判定架构：**Quality Gate（Hard Killers 决定能不能过）→ 五层 Soft Score（决定有多好）**。

---

## Quality Gate 内部结构（Hard Killers + Soft Dimensions）

> 权限隔离递归生效：任何具有否决权的 Gate，其内部不能由一个综合 Score 决定 PASS/FAIL。

```
Quality Gate
├── Hard Killers（决定能不能过，任一触发 → Quality = FAIL / Deal Breaker）
│   ├── K1 Founder integrity（创始人诚信：诉讼/造假/圈钱）
│   ├── K2 IP / ownership（IP 权属不清 / 存在诉讼 / 职务发明争议）
│   ├── K3 Revenue authenticity（收入真实性：合同造假/关联方交易/应收堆积）
│   └── K4 Core technology non-existence（技术不存在：纯 PPT 无 MVP/客户案例）
└── Soft Dimensions（决定有多好，0–100，无否决权）
    ├── Founder capability / Market attractiveness / Product competitiveness
    └── Commercial traction / Scalability
```

**硬规则**：Hard Killer 决定过不过，Soft Dimension 决定多优秀。不得用 Soft Dimension 高分"平均掉" Hard Killer 的 FAIL。

---

## 投资类型识别（Soft Score 权重，不决定 Gate）

先判断类型，动态调整 Soft Score 权重（**仅影响"有多好"的排序，不影响 Hard Gate 结论**）：

| 类型 | Founder | Industry | Government | Financial | Industrial Cap |
|------|---------|----------|------------|-----------|---------------|
| VC | 40% | 30% | 10% | 10% | 10% |
| Growth | 25% | 25% | 10% | 30% | 10% |
| PE | 20% | 20% | 10% | 40% | 10% |
| Strategic | 20% | 25% | 25% | 20% | 10% |
| Gov Guided Fund | 10% | 25% | ≥30% | 15% | 20% |

硬规则（Gov 类型）：Government Layer ≥25%，Founder Score 不得高于 Government Fit——**此为 Soft Score 内部约束，不替代 Hard Killer 否决**。

---

## Step 0：Hard Killer 检查（决定 Quality Gate PASS / FAIL）

任一触发 → **Quality = FAIL（Deal Breaker）**，终止分析，**不得被 Soft Score 覆盖**：
- K1 创始人诚信问题（诉讼/造假/圈钱）
- K2 技术不可验证（纯 PPT，无 MVP/客户案例）
- K3 客户真实性存疑（合同造假/关联方交易）
- K4 核心技术侵权（IP 归属不清/存在诉讼）

> IP 权属等 Deal Breaker 另走独立 **Compliance Gate**（见 SKILL.md 判定层架构），未解除时 Overall 不得 PASS，与 Quality 的 FAIL 平级，均不可被评分覆盖。

---

## 五层 Soft Score（逐层打分 0–100，无否决权）

> 以下五层仅回答"有多好"，**不具备改变 Hard Gate 结论的权限**。

### Layer 1 Founder（创始人）
- Founder Score + FMF Score（行业积累 / 客户资源 / 技术理解 / 供应链理解）
- 创业者类型：科学家型 / 销售型 / 产品型 / 运营型 / 资本型

### Layer 2 Industry（行业）
- **TAM/SAM/SOM bottom-up**（禁宏观市场替代）：
  - TAM：逐场景加总——场景 1（如消防总队数 × 采购数量 × 单价）+ 场景 2（如景区数 × 渗透率 × 单价）+ 场景 3（港口/水务/校园…）
  - SAM：TAM × 可达渠道 / 采购资质约束
  - SOM：SAM × 可实现市占率（3-5 年）
  - 同时输出：各场景采购频率 / 单客户 ARPU / 产品更新周期 / CAGR
- TAM / CAGR / 生命周期
- Timing Score（政策周期 / 技术成熟度 / 资本市场 / 客户接受度）
- 动态护城河（当前 / 3年 / 5年 + 核心威胁）

### Layer 3 Government（政府，Gov 类型重点）
- 国家战略匹配 / 地方产业规划 / 补链强链价值
- 招商价值（税收 / 就业 / 产业链带动）
- 风险（补贴依赖 / 监管 / 贸易）

### Layer 4 Financial（财务）
- 营收 / 毛利率 / 现金流；融资历史
- **Unit Economics**（单台/单客户经济模型）：单台售价 / BOM Cost / 毛利率 / 安装成本 / 售后成本 / 客户获取成本（CAC）/ 回款周期 / 应收账款 / 产品寿命 / 复购更新周期
- **注**：估值 / IRR / MOIC / 退出已抽离到 Value Gate（mode-valuation.md），此处只评财务质量（收入确认/应收/毛利/现金流），不在此评估值合理性
- 投资纪律底线（>阈值 严格对赌；区间内 标准条款；<阈值 可推进）

### Layer 5 Industrial Capability（产业化能力）
- 制造能力（产能 / 良率 / OEE / CAPEX）
- 供应链能力（依赖度 / 国产替代率 / 集中度 / 周转）
- 商业化能力（订单转化 / 量产爬坡 / 交付 / 客户验证）

---

## Evidence 双维 + Claim 三层（P0-4）

> 每个核心断言（客户覆盖/市占率/毛利/订单确定性）标注证据等级，据此控制语气。

- **Quality（E1–E5）**：E1 审计/法律/官方文件；E2 合同/订单/流水/第三方数据；E3 客户/专家访谈；E4 管理层访谈；E5 BP/企业自述
- **Relevance（三档）**：Direct（直接证明命题）/ Indirect / Contextual
- **Claim 三层链路**：`Claim → Evidence → Evidence Level → Decision Impact`
- **语气规则**：E5 必须写成"企业披露 X，待验证"，不得写成"公司已 X"
- **Verification Status**：Verified / Partially Verified / Unverified / Contradicted
- **注意**：E5 + Direct ≠ 可信——企业自述合同是"存在性"直接证据，非"市占率"直接证据（靠 Scope 区分）
- **Freshness / Expiry（P2）**：每个 Evidence 带时间戳，超时效自动失效——财务数据：报告期 + 12 个月；市场/估值数据：6 个月；客户/访谈：12 个月；**过期 → Verification Status 自动降为 Unverified，需复核后方可复用**

---

## Evidence Conflict 调和（v2.6.2，正式能力）

> 把"跨源冲突交人裁决"升级为可执行链：**Evidence → Conflict → Reconciliation → Decision Impact**。不是"帮找更多资料"，而是"判断哪些资料互相打架、会不会改变结论"。

五层分析与 Evidence 标注后，新增一步「冲突识别」：

1. **登记**：同一 Claim 多源数值/方向不一致 → 登记 `evidence_conflicts[]`
2. **分类**：
   - **口径差异**（同指标不同数值，如管理层 2026E 收入 1.8 亿 vs 已验证合同覆盖 0.7 亿）→ 取保守口径 / 标注待确认
   - **方向冲突**（证据指向相反命题，如"客户覆盖达标" vs "ARPU 远低预期"）→ Thesis 降级 / 标记 misleading evidence
3. **调和**：给出 reconciliation 结论；**未调和 → 不得写成"已确认"，Base Case 不采用未验证的高值**
4. **Decision Impact**：写明对估值 / Gate / DD 优先级的实质影响

输出话术模板（替代"数据存在冲突"的模糊表述）：
> `收入预测存在重大口径差异：管理层 2026E 1.8 亿，但当前已验证合同覆盖仅 0.7 亿；建议 Base Case 暂不采用 1.8 亿，待订单确认后更新。`

---

## Confidence / Uncertainty 层（v2.6.2，推导不平均）

> 回答"Agent 到底有多确定"，把「项目不好」与「还不知道项目好不好」分开。

五层分析结束时输出 `confidence_block`（四层置信度）：

| 层 | 含义 | 来源 |
|---|---|---|
| Evidence Confidence | 证据整体强弱 | Evidence 双维（E1–E5 + Verification Status）|
| Assumption Confidence | 关键假设置信 | Assumption Register 的 confidence 字段 |
| Model Confidence | 模型/估算置信 | 概率参数的 type（Observed/Derived/Assumption/Model Estimate）|
| **Decision Confidence** | **综合（推导，不平均）** | 下述规则 |

**Decision Confidence 推导规则（不加权平均，延续权限隔离哲学）**：
- 任一 `decision_critical_assumptions` 的 `uncertainty = high` → 上限 **medium**
- 存在未调和 `evidence_conflicts`（reconciliation = 待确认）且属 decision-critical → 上限 **medium**
- **Hard Gate = WATCH/CONDITIONAL 不作机械降级**：仅当该 Gate 对应事项属于 Decision-Critical Assumption、或对当前 Recommendation 有实质性影响时才纳入 `uncertainty_sources`——Confidence 是**决策相关的不确定性**，不是所有缺口的数量统计

---

## DD Priority（v2.6.2，下一轮最值得验证什么）

> 决策"建议 DD？YES"后，进一步回答"下一轮 DD 最值得花时间验证什么"——把 What Must Be Proven 排序：

- **P0 — 不能证明则项目不能继续**（如 IP 权属、收入真实性穿透）
- **P1 — 显著改变 Value / Return**（如客户集中度、采购周期）
- **P2 — 补充信息**（如海外市场 TAM）

输出 `dd_priority`，`next_required_evidence` 为其派生摘要。

---

## 产业资源协同（Resource Synergy，Soft Score，无否决权）

在五层之外，评估"Value = Intrinsic + Resource Synergy"：
- 可导入的链主 / 龙头客户（美的 / 汇川 / 埃斯顿…）
- 可落地园区 / 区域政策
- 可对接供应链 / 科研院所 / 政府资源
- 输出 Resource Synergy Score（0-100）
- **分层叠加，不回灌**：Intrinsic Valuation 与 Synergy Premium 分两行呈现
- **Anti-Subsidization**：Synergy 不得反向补贴不成立的投资价值（Industrial × Investment 双轴独立）

---

## DD 尽调状态系统（符号标注）
✅ 已验证 / ⚠️ 部分验证 / ❗ 关键风险 / ❓ 待核实 / 🔄 进行中
四维度：财务 / 商业 / 产业 / 法务。直接转化为尽调任务清单。

## 竞品对比表（选取三锚定 · 标准模块）

**选取总原则**：不为穷举行业，而为投资 Thesis 服务——回答"凭什么把这笔钱给本项目而不是别人"。对手只选「能分流同一投资决策」或「能反证其壁垒」的标的，不拉无关玩家。

**三锚定分类（每类各选 1 个代表入表）**
1. **投资可替代者**：同一资金来源（同一基金池 / 同一 ticket 区间）里直接抢这笔钱的内部替代物。**Gov 视角强制要求**——生态内已投 / 在谈同类必须入表，论证差异化（如防爆液压 vs 应急救援电驱），避免组合同质化。
2. **技术路线替代物**：代表本项目技术路线的主流替代阵营，用以反证壁垒独特性（如电驱 vs 液压、通用 vs 细分）。
3. **场景 / 规模标杆**：同场景的成熟玩家，用以标定本项目所处阶段与规模差距，并反衬细分空白未被覆盖。

**维度锚定**：技术路线 / 专注领域 / 团队 / 量产能力 / 核心客户 / 估值。

**边界（同样重要）**
- ❌ 不跨区域拉其他政府平台做横向对比（遵守单视角评估铁律）。
- ❌ 不把不可投标杆（如海外巨头）当"竞品"——只作壁垒参照，不入投资可替代集。
- ❌ 不拉纯科研 / 未商业化团队——对比对象须同阶段或头部，保证可比性。

## IC Debate Engine
- Bull Case（看多 3 条 + 催化剂）
- Bear Case（看空 3 条 + 风险因素）
- Devil Case（极端黑天鹅 + 损失）

## 反证系统（Falsification Layer，P1）

> 共同回答"什么会杀死这笔投资"——Kill Factor 事前设防，Counterfactual 事后测试，Thesis Ledger 全程记账。

### Thesis Ledger（投资命题账本）
每个关键命题必须有支持证据 + 反证证据 + 状态：
| Thesis | 支持证据 | 反证证据 | 状态 |
|---|---|---|---|
| T1：细分市场领先 | 客户覆盖 / 认证 / 出口 | 市占率口径不明 / 竞品进入 | partially_verified |
| T2：落地放大价值 | 场景 / 产能 / 产业链 | 原基地仍在 / 本地订单未定 | unproven |
| T3：估值具吸引力 | 前瞻 PS 倍数 | 毛利率 / 可比 / 持续性未验证 | not_yet_proven |

状态：verified（证据充分无反证）/ partially_verified（部分验证）/ unproven（证据不足）/ not_yet_proven（有支持但关键反证未排除）。

### Kill Factors（What kills the thesis）
> 可证伪命题 + 触发条件，**必须带 Action（Trigger → Decision Consequence），不是风险描述**。

| Kill Factor | 当前状态 | Trigger | 后果 |
|---|---|---|---|
| IP 权属 | 待核 | 存在实质争议 | FAIL（Deal Breaker）|
| 收入真实性 | 待核 | 无法穿透验证 | FAIL |
| 毛利率 | 观察 | < X% | Re-price（重新估值）|
| 落地锁定 | 谈判中 | 无法锁定 | WATCH |
| 订单转化 | 待验证 | < X% | Thesis downgrade |

### 与 Counterfactual 的关系
- Kill Factor：事前设防（"什么事件发生后应不投"）
- Counterfactual（反事实 6 问，调 recommendation.md）：事后测试（"关键前提不成立还投吗"）
- 两者 + Thesis Ledger 构成 Falsification Layer，位于 Value 与 Industrial 之间

## Industrial × Investment 二维矩阵（P2）

> 双轴独立判定，禁止招商价值反向补贴投资价值（Anti-Subsidization Rule）。输出当前项目落点 + 对应动作。

| | Investment 高 | Investment 低 |
|---|---|---|
| **Industrial 高** | 产业投资优先 | 招商优先 · 投资谨慎 |
| **Industrial 低** | 财务投资评估 | NO-GO |

- Industrial 轴：产业协同 / 落地 / 返投 / 场景 / 产业链价值
- Investment 轴：Value Gate（3A/3B/3C）+ 五层 Soft Score + 反证系统综合
- **右上格铁律（产业高 × 投资低）**：可招商、可产业合作，但**不得为招商降低投资标准**
- 输出：当前项目落在哪一格 + 对应决策动作

## 投资备忘录（最终输出）
Quality Gate 结果 + Hard Killer 检查 + Soft Score 五层 + **Thesis Ledger + Kill Factors + 二维矩阵落点** + 核心逻辑 Top3 + 核心风险 Top3 + 缺失信息 Top3 + 投资条件 Top3 + 投后赋能 + 下一步行动。

---

## 输出：Investment Assessment（Gate 结果优先）

```
【Investment Assessment】
投资类型：XXX（Soft Score 权重已调整，仅影响排序）

Quality Gate：✅ PASS / ⚠️ CONDITIONAL / ❌ FAIL
Hard Killer 检查：
  K1 创始人诚信：✅ / ❌
  K2 IP 权属：✅ / ❌（→ Compliance Gate 另判）
  K3 收入真实性：✅ / ❌
  K4 技术存在性：✅ / ❌

五层 Soft Score（无否决权，仅供排序/定价）：
  Founder XX / Industry XX / Gov XX / Financial XX / Industrial Cap XX
Resource Synergy：XX（可导入：XXX / 落地：XXX）

Evidence（双维标注）：
  断言1：...（E5 · Indirect · Unverified → 企业披露，待验证）
  断言2：...（E2 · Direct · Verified）

Thesis Ledger（反证记账）：
  T1 细分领先：...（partially_verified）
  T2 落地放大：...（unproven）
Kill Factors（Trigger → Consequence）：
  KF1 IP 权属：实质争议 → FAIL（Deal Breaker）
  KF2 收入真实性：无法穿透 → FAIL
  KF3 毛利率 < X% → Re-price

Industrial × Investment 落点：产业投资优先 / 招商优先·投资谨慎 / 财务投资评估 / NO-GO

核心证据：...
核心风险：...
缺失信息：...

决策：建议 DD？YES / NO
理由：...

Confidence：High / Medium / Low（详：Confidence Block 四层）
主要不确定性：...（决策相关缺口，非缺口数量统计）
Top3 关键假设敏感性：...（impact_on_decision × uncertainty，敏感性 ≠ 风险）
Evidence Conflict：...（未调和项 + 对结论影响）
DD 优先级：P0（不能证明则不能继续）/ P1（显著改变 Value/Return）/ P2（补充信息）
免责：分析建议 · 非投资决定 · 需 IC 审议
```

> **权限隔离**：Quality Gate 结果（尤其 FAIL）不被 Soft Score 覆盖；五层评分再高也不得把 FAIL 改写为 PASS。

## 强制 Capture
生成 Decision Object（mode=evaluation），含 Quality Gate 结果 + 五层 Soft Score + Evidence（带 Verification Status）。
