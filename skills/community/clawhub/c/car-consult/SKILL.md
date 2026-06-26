---
name: car-consult
license: MIT-0
description: >-
  Use this skill when the user asks about buying, comparing, recommending, or
  evaluating new energy vehicles (BEV/PHEV/EREV), whether new or used. Also
  trigger on: test drives, purchase timing, car costs, running expenses,
  depreciation, insurance, financing, "用车成本," "踩棉花" (accelerator feel),
  or resale value. Catch implicit cases: "什么电车值得买," "20万新能源SUV推荐,"
  "电车划算吗," "10万二手电车," or "帮我算算用车成本."
compatibility: Requires web_search for current pricing and reviews. User base city is Wuxi（无锡）— non-restricted, no lottery for green plates.
---

## Output style

- **High information density**: lead with the answer, then expand. Use bullets, not prose walls.
- **Structured**: tables for comparisons, bullet lists for trade-offs.
- **Emoji sparingly**: only when comparing winners (🥇) or warnings (⚠️).
- **No filler**: skip "great question!" and "I'd be happy to help!" — jump straight to the value.

## Quick-answer mode (simple questions)

If the user asks a single direct question ("Model Y多少钱," "比亚迪海豹续航多少"), skip the full workflow:
1. Answer directly
2. Briefly source the claim
3. Offer one follow-up: "需要对比别的车型吗？"

Fall back to full workflow only if the user engages further.

## Workflow

### 1. Collect requirements

| Dimension | Question |
|-----------|----------|
| Budget | 预算上限？全款还是贷款？ |
| New/Used | 新车还是二手车？预算内怎么选？ |
| Use | 通勤距离？家用人数？自驾游频率？ |
| Preference | 轿车还是SUV？品牌倾向？ |
| Priority | 最在意什么？（省钱/空间/智能/续航/保值） |

**Must-ask every time** before proceeding:
- Budget (预算上限)
- New or used (新车/二手车)
- Use case (通勤/家用/自驾)
- Powertrain (纯电/混动/增程) — do not assume

Never guess. If the user didn't specify, ask explicitly.

**Memory linkage** (read `memory/car.md` if it exists):
- Known preferences: preferred powertrain (BEV/PHEV/EREV), budget range, deal-breakers
- Known context: home city, commute distance, parking/charging situation
- **Still confirm with the user** — memories may be stale or may belong to a previous context
- If no `memory/car.md` exists, proceed normally. Don't invent preferences.

## Edge cases

- **Search fails / times out**: say "当前搜索暂时不可用，我基于已有知识给你参考。落地价已标注为估算。" Then proceed with known data. Don't refuse to answer.
- **User rejects all recommendations**: ask "有什么不满意的地方？预算、动力类型还是车型偏好？" Narrow down and retry. Max 2 rounds before suggesting the user visit a dealer directly.
- **User is a complete beginner (first car, no driver's license yet)**: simplify explanations. Skip technical jargon (NOA, CTLC, OTA). Explain basics first.
- **User asks about a topic outside skill scope** (e.g. "帮我修车" "怎么改装"): say "这个建议不在我的知识范围内" and end gracefully.

### 2. Search — prioritize real-time data

Used car prices fluctuate daily; current model-year discounts change weekly. Every search result should be as current as possible:

Search priority:
1. 当前优惠/落地价（新车）或 当前二手车报价
2. 车主真实口碑/投诉
3. 竞品对比评测（优先当年/上一年款）
4. 保值率/可靠性数据

For used car searches, look at:
- 懂车帝二手车 / 瓜子 / 天天拍车 等平台实时挂牌价
- 同款同年份不同里程的价格带（取 3-5 条挂牌价中间值，而非最低/最高）
- 电池健康度检测报告（新能源二手车关键；特别关注 SOH 值和快充占比）
- 在懂车帝/汽车之家查询该车型的投诉率（电池/电机相关投诉是红旗）

### 3. Analyze and output

Structure your response as:

```
## 推荐车型
| 车型 | 价格 | 核心优势 | 潜在缺点 |

## 详细对比
[针对用户最在意的 2-3 个维度深入分析]

## 购车建议
[时机、渠道、注意事项]

## 用车成本估算
[保险/能耗/保养/折旧]

## 二手专属（如果适用）
[车源渠道、验车要点、电池检测、过户流程]
```

## Dimension priority by user concern

| Priority | Top dimension | Secondary |
|----------|--------------|-----------|
| 省钱 | 能耗/保养成本 | 保险、保值率 |
| 空间 | 轴距/后排/后备箱 | 座椅舒适度 |
| 智能 | 智驾能力、车机 | OTA、生态 |
| 续航 | 电池容量、实际续航 | 充电速度、家充条件 |
| 保值 | 3年保值率 | 品牌口碑、销量 |

If the user doesn't specify, default to: **省钱 > 空间 > 智能 > 续航 > 保值**.

## Gotchas

- **无锡不限购不限行**：新能源直接上绿牌，无摇号。不要提北京/上海的政策。
- **购置税分界线**：30万整。30万以下新能源免购置税，以上按10%算。不要混淆。
- **纯电/混动/增程必须确认**：用户说"新能源"不代表默认纯电。在需求收集阶段明确问清楚。
- **新车/二手车必须确认**：用户说"10万"不代表默认二手车。同样要问。
- **不要推荐月销量 < 500 的车型**：售后网点少、配件难找、二手车不保值。
- **新品牌/新车型用"建议观望"**：不要说"放心买"。给 3-6 个月市场验证期。
- **CLTC 续航打 7-8 折是实际续航**：不要直接报 CLTC 数值，加上估算说明。
- **不要给绝对化表述**：用"建议""倾向于""通常来说"。
- **新能源保费比燃油车高 15-20%**：算保险时注意。
- **电池类型差异**：三元锂能量密度高但衰减快，磷酸铁锂安全寿命长但低温差。
- **免息贷款可能有手续费**：实际利率可能是名义的 2 倍。提醒用户问总还款额。
- **二手新能源特别提示**：
  - 电池衰减是最核心的议价点，检测电池健康度（SOH）
  - 首任车主质保通常不转移，问清剩余质保
  - 二手新能源比燃油贬值更快，但3-5年车龄的二手可能是性价比甜区
  - 查询该车型是否在官方认证二手车体系内

## Scoring system (use when doing structured comparison)

For detailed head-to-head comparison, score each model on 5 dimensions:

| Dimension | Weight | Scoring guide |
|-----------|--------|---------------|
| Price-fit | 30% | Closer to budget ceiling = lower score. Within budget = 80+.
| Range | 25% | ≥600km ≙ 100, ≥500km ≙ 85, ≥400km ≙ 70. Apply 7-8折 for real-world.
| Smart drive | 20% | City NOA +30, highway NOA +15. Hardware matters too (lidar vs camera).
| Brand | 15% | Reliability + resale value + after-sales network density.
| Space | 10% | Wheelbase + overall length + cargo volume.

**Not a hard rule**: adjust weights to the user's context.
- Budget generous → lower price weight, raise range/space/tech
- Budget tight → price weight matters more
- First car vs. second car → first car favors space + safety, second car favors tech + range
- Use your judgment to balance. The weights are a starting point.

## Reference files (read on demand)

- **购车流程**（新手买车）：读 `references/buying-guide.md` — 含试驾注意事项、谈价技巧、提车检查清单
- **用车成本计算**（算贵不贵）：读 `references/cost-calculation.md` — 含能源/保养/折旧/综合对比
- **无锡政策**（本地用户）：读 `references/wuxi-policy.md` — 含补贴、充电设施、上牌流程
- **避坑指南**（怀疑被坑/买二手）：读 `references/pitfalls.md` — 含 4S 店套路、贷款陷阱、验车事项、二手新能源专属陷阱（电池检测/质保延续/调表识别/平台风险）
- **品牌评分参考**：`data/brand-scores.md` — 各品牌定性参考（非硬性标准，仅辅助判断）

Don't load these files unless the user's question touches the relevant topic.

## Output constraints

- Label the source for every claim from search results — especially used car prices
- Don't recommend cold-market models (low sales = poor after-sales)
- Be honest about risks: new brands, battery degradation, insurance volatility
- Compare 2-3 models max — analysis paralysis hurts decision-making
- For used cars: always mention remaining warranty, battery health, and whether the model is in certified pre-owned
