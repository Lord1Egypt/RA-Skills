# Mode 3 — IC（投委会）

## 定位
从"分析报告"升级为"IC 秘书"。对应「40 DD → 10 投资」。唯一核心决策：**建议投资方案（Invest / Wait / Track / Pass + 建议参数）**。

## 输入
Evaluation 结果（Investment Assessment，含 Quality Gate + 五层 Soft Score）+ Value Gate 结论（调 mode-valuation.md，3A/3B/3C）+ 投资建议参数（调 recommendation.md）

## 执行内容
1. **IC Memo**：Executive Summary + Investment Highlight + Risk + Value Gate（3A/3B/3C，调 mode-valuation.md）+ Thesis Ledger + Kill Factors + Term Sheet 方向 + Conditions
2. **IC Debate 增强**：引用 Mode 2 的 Bull/Bear/Devil，补充 Why Not + 反事实 6 问（调 recommendation.md）
3. **模拟投委提问**：预测 IC 委员最可能问的 3-5 个问题 + 基于分析的回答要点
4. **会议纪要**：决策讨论要点 + 反对意见记录
5. **Action Items**：负责人 + 截止日期 + 交付物

## 模拟投委提问示例
- "这个项目超我们单项目额度多少？怎么解决？"
- "如果估值不降，我们的安全边际在哪？"
- "产业资源协同的链主客户，确定性有多高？"
- "为什么现在投，而不是 6 个月后？"（Why Not 回应）

## 交易结构合规检查（Deterministic Checkbox，P2）
> 纯规则清单，逐项 PASS/FAIL；**任一 FAIL → 交易结构不可行（Hard Compliance Gate）**，不得靠谈判软化。

- [ ] 名股实债（固定收益兜底 / 固定分红承诺）
- [ ] 兜底回购（明股实债式回购承诺，国资禁止）
- [ ] 违规借贷（投资款被挪用为借贷）
- [ ] 其他国资监管硬线（54 号文等，按基金所在地更新）

输出：✅ 全部通过 / ❌ 触发项（列出，交易结构需重设计）

## 输出：IC Package（7 块压缩版，P2）

> **输出压缩原则**：内部判定复杂，外部输出高度压缩。IC 页只留 7 块，其余进附录 / Decision Object。

```
【IC Package · 7 块压缩版】
项目：XXX
日期：YYYY-MM-DD

① Investment Decision：CONDITIONAL / INVEST / WATCH / PASS
   建议参数：金额区间 / 估值区间 / 条款方向（里程碑对赌？） / 席位（观察员 or 董事）
   Decision Confidence：High / Medium / Low（四层 Confidence Block，推导不平均）
   主要不确定性：...（决策相关缺口）
   当前结论对哪些假设高度敏感：...（Top3 关键假设，敏感性 ≠ 风险）
   Evidence Conflict：...（未调和项 + 对结论影响，如有）
② Why（3 条）：
   1. ...
   2. ...
   3. ...
③ Hard Gates：
   Mandate：PASS/CONDITIONAL/WATCH/FAIL
   Quality：PASS/CONDITIONAL/WATCH/FAIL
   Compliance：PASS/CONDITIONAL/WATCH/FAIL（IP 待核）
   Industrial：PASS/CONDITIONAL/WATCH/FAIL
④ Value Range：
   3A Valuation：low X / base Y / high Z 亿
   3B IRR Range：xx–xx% · MOIC：x–x
   3C Exitability：路径 + 概率 + 时间窗
⑤ Kill Factors（3 条，Trigger → Consequence）：
   - IP 权属：实质争议 → Deal Breaker
   - 收入真实性：无法穿透 → FAIL
   - 毛利率 < X% → Re-price
⑥ What Must Be Proven Before IC（按 DD 优先级排序，P0 不能证明则不能继续）：
   P0：1. IP 权属（实质争议 → Deal Breaker）
       2. 2027E 收入真实性（合同/流水穿透）
   P1：3. 客户集中度
       4. 采购周期
   P2：5. 海外市场 TAM
⑦ IC Questions（10–12 条，见 12 问清单）：
   Q1：...
   Q2：...

（附录 / Decision Object：Thesis Ledger / Counterfactual 6 问 / Assumption Register /
  五层 Soft Score / 模拟提问 / 免责）
Vote：建议（需 IC 表决）
Meeting Notes：决策讨论要点 + 反对意见
Action Items：
  - [ ] 负责人 / 截止日 / 交付物
```

### IC 12 问清单（预答模板，按项目裁剪）
1. 真实市场规模？（bottom-up TAM/SAM/SOM，禁宏观替代）
2. 竞争地位的分母与口径？（市占率 = 什么 ÷ 什么）
3. 客户覆盖的统计口径？（使用过 / 采购过 / 当前客户）
4. 收入集中度？（Top5 / Top10 客户占比）
5. 毛利率？净利率跃升的驱动拆解？（收入/毛利/规模/补助/结构）
6. 本轮融资用途明细？（设备/厂房/研发/人员/营销/海外/营运）
7. 估值为什么合理？（相对可比/增长/毛利/壁垒/退出倍数）
8. 未来 3 年增长来源与可验证里程碑？
9. 大厂/巨头进入的应对？
10. 落地地区除政策订单外，不可替代的价值是什么？
11. 若落地承诺无法锁定，投资结构如何设计？
12. 基金怎么退出？（路径 + 概率 + 时间窗）

## Human Decision 回填（v2.6.2，Decision Attribution）

> IC 表决后，投资经理把人工结果回填为 `ic_resolution`（结构化）：Agent 建议 vs IC 决议 + 是否 override + 分歧原因 + 条件。这是"Agent 怎么判断 → 人怎么修改 → 为什么修改 → 最终发生什么"的原始记录，是研究"人机协同决策质量"的基础。

- `override = true` 时 `divergence_reason` 必填（如"基金年度返投压力变化"）
- Outcome 回填时判定 `decision_attribution`：**必须基于预先定义的 Outcome Criterion，不得仅依最终公司表现倒推（防 hindsight bias）；无法明确归因保持 pending**
- 例：Agent 建议 Proceed DD，IC 决议 Pass——系统必须能解释"IC 为什么不同意 Agent"（override + divergence_reason），而非只记"IC Pass"

## 强制 Capture
生成 Decision Object（mode=ic），含 IC 建议方案 + 后续实际决议（决议回填后更新）。
