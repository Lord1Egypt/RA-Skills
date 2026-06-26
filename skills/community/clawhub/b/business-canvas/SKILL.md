---
name: business-canvas
description: >-
  Interactive Business Model Canvas & Value Proposition Canvas generator based on
  Strategyzer methodology. Guides users through structured business modeling with
  Jobs-Pains-Gains analysis, 9-block BMC, Test Cards, and Learning Cards.
  Use when the user asks to "fill business canvas", "商业模式画布",
  "value proposition canvas", "analyze business model", "商业建模",
  "evaluate my startup", "分析商业逻辑", "business model", "创业分析",
  or wants to think through commercialization of a product/project.
---

# Business Canvas Skill

Interactive business modeling using the Strategyzer framework. Produces up to four
structured markdown documents: Value Proposition Canvas, Business Model Canvas,
Test/Learning Cards with Progress Board, and an Executive Summary.

## When to Use

- User wants to think through how to commercialize a product
- User has a product/project but unclear business logic
- User asks about pricing, revenue model, customer segments, go-to-market
- User wants to validate a business idea before building
- User needs a structured framework for investor pitch preparation

## Output Files

All outputs go to `docs/business/` in the project root (create if missing).

1. `value-proposition-canvas.md` — Customer profile + value map + fit assessment
2. `business-model-canvas.md` — Full 9-block BMC + key risks + next steps
3. `test-cards.md` — Test Cards + Learning Cards + Progress Board (optional)
4. `canvas-summary.md` — Executive summary for investor/partner sharing (optional)

## Phase 1: Context Gathering

Before starting any canvas, understand the product:

1. Read the project README, AGENTS.md, or any product description files
2. Identify: what the product does, who it targets, what stage it's at
3. Scan for existing business docs (pricing pages, pitch decks, etc.)

Summarize your understanding to the user in 3-5 sentences. Ask them to confirm
or correct before proceeding.

## Phase 2: Value Proposition Canvas — Customer Side

Fill these three blocks by asking the user. Pre-fill what you can infer from
the codebase, then ask for confirmation and additions.

### 2A: Customer Jobs (客户任务)

Three categories of jobs:

**Functional Jobs** — What tasks are customers trying to accomplish?
- Core workflow tasks they do daily/weekly
- Specific problems they're trying to solve
- Deliverables they need to produce

**Social Jobs** — How do customers want to be perceived?
- How they want to look to their boss/peers/clients
- Professional reputation goals
- Status and credibility needs

**Emotional Jobs** — How do customers want to feel?
- Confidence, certainty, reduced anxiety
- Sense of mastery or competence
- Peace of mind about quality

Ask the user: "I've pre-filled some customer jobs based on your product.
What's missing? What did I get wrong?"

Rank jobs by importance to the customer (critical / important / nice-to-have).

### 2B: Pains (客户痛点)

For each customer job, identify pains:

**Undesired outcomes** — What bad results do customers experience?
- What goes wrong when they do the job manually?
- What mistakes do they make?
- What quality issues arise?

**Obstacles** — What prevents them from doing the job well?
- Time constraints
- Skill/knowledge gaps
- Tool limitations
- Cost barriers

**Risks** — What are they afraid of?
- Career consequences of failure
- Financial waste
- Compliance/regulatory risks

Ask: "Which of these pains is most severe? Rate each: extreme / severe / moderate."

### 2C: Gains (客户收益)

What outcomes and benefits do customers want?

**Required gains** — Without these, the solution doesn't work
**Expected gains** — Not strictly necessary but customers expect them
**Desired gains** — Beyond expectations, would love to have
**Unexpected gains** — Surprises that exceed expectations

Ask: "What would make your user say 'I can't believe this tool exists'?"

## Phase 3: Value Proposition Canvas — Product Side

### 3A: Products & Services

List all features/tools the product offers. Map each to the customer jobs it addresses.
Use the codebase to enumerate actual capabilities.

### 3B: Pain Relievers (痛点解决方案)

For each pain identified in 2B, describe how the product alleviates it.
Be specific: "Reduces column sizing calculation from 2 hours to 30 seconds"
not "Makes work faster."

### 3C: Gain Creators (收益创造方案)

For each gain identified in 2C, describe how the product creates it.

## Phase 3.5: Fit Assessment

After completing both sides of the VPC, assess the fit before moving to BMC.
This is the most valuable step — do NOT skip it.

**Fit Dimensions:**
- **Problem-Solution Fit**: Do pain relievers address the most severe pains?
- **Coverage**: Which customer jobs have NO corresponding product feature?
- **Overkill**: Which product features address NO customer job?
- **Strength**: Where is the fit strongest? (This is your wedge)

**Fit Matrix** — Map each product feature to customer jobs/pains/gains:

| Feature | Addresses Job | Relieves Pain | Creates Gain | Fit Score |
|---------|--------------|---------------|-------------|-----------|
| Feature A | Job #1 | Pain #2 | Gain #1 | Strong |
| Feature B | - | - | - | Orphan |

Output **two** fit scores with explanation using the calibration below:

1. **Optimistic Score (乐观分)**: Assuming all unvalidated hypotheses are true
2. **Realistic Score (现实分)**: Only counting validated evidence (customer quotes, usage data, payment)

In one line, state: "乐观分与现实分的差距来自 [具体原因]"

**Fit Score Calibration:**
- **9-10**: Every severe pain has a strong reliever. No orphan features. Users would
  riot if product disappeared. Evidence from real usage/payment.
- **7-8**: Most severe pains addressed. 1-2 orphan features. Strong signal from at
  least one customer segment. Some gaps identified but manageable.
- **5-6**: Partial coverage. Several pains unaddressed. Product has clear value but
  significant gaps. Needs focused iteration on specific jobs.
- **3-4**: Weak alignment. Product features don't map well to actual customer pains.
  Likely building for imagined rather than real needs. Pivot candidate.
- **1-2**: No meaningful fit. Product solves problems nobody has, or solves them in
  ways nobody wants. Stop and re-interview customers.

**Multi-segment note:** If there are multiple customer segments, create a separate
VPC for each segment. Compare fit scores across segments to identify which segment
to prioritize.

## Phase 3.7: Environment Map (环境地图)

Analyze the external environment surrounding the business model. Four quadrants:

### Market Forces (市场力量)
- Market segments and their attractiveness
- Needs and demands shifting in the market
- Revenue attractiveness (willingness to pay trends)
- Switching costs for customers

### Industry Forces (行业力量)
- Competitors: who are they, what advantages do they have?
- New entrants: who might enter this space?
- Substitute products/services: what else solves the same job?
- Suppliers and value chain actors: who has power?
- Stakeholders: regulators, investors, standards bodies

### Key Trends (关键趋势)
- Technology trends affecting the industry
- Regulatory trends (new compliance requirements, policy changes)
- Societal and cultural trends
- Socioeconomic trends (spending patterns, talent availability)

### Macroeconomic Forces (宏观经济力量)
- Global market conditions
- Capital markets (funding availability)
- Economic infrastructure
- Commodities and resources

Output as a 2x2 quadrant table. For each factor, note whether it's a
tailwind (favorable) or headwind (unfavorable) for the business.

## Phase 4: Business Model Canvas

Fill all 9 blocks. For each, provide 3-5 bullet points.

### Block 1: Customer Segments (客户细分)

Who are your most important customers? Be specific (not "enterprises" but
"biopharma companies with 10-50 person R&D teams doing process development").

Types to consider:
- Mass market / Niche market / Segmented / Diversified / Multi-sided platform

### Block 2: Value Propositions (价值主张)

Pull directly from Phase 3. Summarize the top 3 value propositions.

Which customer needs are you satisfying? Categories:
- Newness / Performance / Customization / "Getting the job done"
- Design / Brand/Status / Price / Cost reduction / Risk reduction
- Accessibility / Convenience

### Block 3: Channels (渠道)

How do you reach customers? For each channel, specify stage:
1. Awareness — How do customers learn about you?
2. Evaluation — How do customers evaluate your product?
3. Purchase — How do customers buy?
4. Delivery — How do you deliver value?
5. After-sales — How do you support post-purchase?

### Block 4: Customer Relationships (客户关系)

What type of relationship does each customer segment expect?
- Personal assistance / Dedicated personal assistance
- Self-service / Automated services
- Communities / Co-creation

### Block 5: Revenue Streams (收入来源)

How does each customer segment pay? Be specific about pricing.

Models to consider:
- Asset sale / Usage fee / Subscription / Licensing
- Lending/Renting / Brokerage / Advertising

For each stream, estimate: pricing range, payment frequency, % of total revenue.

### Block 6: Key Resources (核心资源)

What key resources does the value proposition require?
- Physical / Intellectual (patents, IP, data) / Human / Financial

### Block 7: Key Activities (关键活动)

What key activities does the value proposition require?
- Production / Problem solving / Platform/Network

### Block 8: Key Partnerships (重要合作)

Who are key partners and suppliers? What key resources do they provide?

Types:
- Strategic alliances / Coopetition / Joint ventures / Buyer-supplier

For each partnership, clarify: What do they provide? What do we provide?
What's their incentive to partner?

### Block 9: Cost Structure (成本结构)

What are the most important costs inherent in the business model?

- Fixed costs / Variable costs
- Economies of scale / Economies of scope

For key costs, estimate: monthly/annual amount, % of total.

## Phase 5: Hypothesis Validation (Strategyzer Testing Methodology)

### 5A: Identify Key Assumptions

Extract the riskiest assumptions from the canvas. Three risk categories
(test in this order):

1. **Desirability risk** — Do customers actually want this?
2. **Feasibility risk** — Can we build and deliver this?
3. **Viability risk** — Can we make money doing this?

### 5B: Three-Stage Testing Funnel

Follow Strategyzer's validation roadmap:

**Stage 1: Test the Circle (Customer Profile)**
Verify that customers actually have the jobs, pains, and gains you identified.
Methods: customer interviews, Google Ads keyword campaigns, landing page tests,
search volume analysis.

**Stage 2: Test the Square (Value Map)**
Determine which products, services, and features customers want most.
Methods: Buy-A-Feature game, prototype testing, concierge MVP, Wizard of Oz tests.

**Stage 3: Test the Rectangle (Business Model)**
Validate willingness to pay and revenue model viability.
Methods: pre-sales, LOI collection, pricing A/B tests, pilot contracts.

### 5C: Test Cards

For each unvalidated assumption, generate a Test Card (Strategyzer format):

```
## Test Card: [Hypothesis Name]

**Step 1 — Hypothesis**
We believe that: [specific, falsifiable assumption]

**Step 2 — Test**
To verify that, we will: [specific experiment/action]

**Step 3 — Metric**
And measure: [what observable data to collect]

**Step 4 — Criteria**
We are right if: [specific threshold, set BEFORE running the test]

**Context:**
- Risk type: [Desirability / Feasibility / Viability]
- Cost: [time/money/resources needed]
- Timeline: [days/weeks]
- Priority: [critical / important / nice-to-have]
- Testing stage: [Circle / Square / Rectangle]
```

### 5D: Learning Cards

After running each test, generate a Learning Card:

```
## Learning Card: [Hypothesis Name]

**Step 1 — Hypothesis**
We believed that: [original hypothesis from Test Card]

**Step 2 — Observation**
We observed: [actual data collected, specific numbers]

**Step 3 — Learnings & Insights**
From that we learned: [what the data tells us, was hypothesis validated?]

**Step 4 — Decisions & Actions**
Therefore we will: [Pivot / Persevere / Stop]
Next action: [specific next step]
```

### 5E: Progress Board

Track all hypotheses in a single table:

| # | Hypothesis | Risk Type | Stage | Status | Result |
|---|-----------|-----------|-------|--------|--------|
| 1 | ... | Desirability | Circle | Testing | - |
| 2 | ... | Viability | Rectangle | Validated | Confirmed |
| 3 | ... | Desirability | Circle | Invalidated | Pivot needed |

Status values: Backlog / Testing / Validated / Invalidated

Prioritize: test the riskiest assumptions first (desirability > feasibility > viability).
Never test more than 3 hypotheses simultaneously.

## Phase 6: Executive Summary (Optional)

If the user requests, generate a 1-page executive summary (canvas-summary.md):

```markdown
# [Product Name] — Business Canvas Summary

## One-liner
[What it does, for whom, why now — one sentence]

## Value Proposition
[Top 3 value propositions from VPC]

## Target Customer
[Primary customer segment, specific persona]

## Revenue Model
[How you make money, pricing range]

## Key Metrics
[3-5 metrics that matter most at current stage]

## Biggest Risk
[The #1 assumption that could kill this, and how to test it]

## Single Falsifying Assumption (证伪假设)
如果我对 [X] 的判断是错的，整个结论会翻转，因为 [Y]。

## Next 30-Day Action Plan
1. [Action 1]
2. [Action 2]
3. [Action 3]
```

## Phase 7: Output Generation

Generate all markdown files with proper formatting.

### value-proposition-canvas.md format:

```markdown
# Value Proposition Canvas — [Product Name]

Generated: [date]

## Customer Profile

### Customer Jobs
| # | Job | Type | Importance |
|---|-----|------|-----------|
| 1 | ... | Functional | Critical |

### Pains
| # | Pain | Severity | Related Job |
|---|------|----------|-------------|
| 1 | ... | Extreme | Job #1 |

### Gains
| # | Gain | Type | Related Job |
|---|------|------|-------------|
| 1 | ... | Required | Job #1 |

## Value Map

### Products & Services
| # | Feature | Addresses Job |
|---|---------|--------------|
| 1 | ... | Job #1, #3 |

### Pain Relievers
| # | Pain Reliever | Addresses Pain | Impact |
|---|--------------|----------------|--------|
| 1 | ... | Pain #1 | High |

### Gain Creators
| # | Gain Creator | Creates Gain | Impact |
|---|-------------|-------------|--------|
| 1 | ... | Gain #1 | High |

## Fit Assessment
- Optimistic Fit Score (乐观分): X/10
- Realistic Fit Score (现实分): Y/10
- Gap reason: 乐观与现实的差距来自 [...]
- Strongest fit: ...
- Gaps: ...
- Recommended wedge: ...

## Single Falsifying Assumption (证伪假设)
如果我对 [一个关键假设] 的判断是错的，整个商业模式会崩塌，因为 [原因]。
```

### business-model-canvas.md format:

```markdown
# Business Model Canvas — [Product Name]

Generated: [date]

## 1. Customer Segments
- ...

## 2. Value Propositions
- ...

## 3. Channels
- ...

## 4. Customer Relationships
- ...

## 5. Revenue Streams
- ...

## 6. Key Resources
- ...

## 7. Key Activities
- ...

## 8. Key Partnerships
- ...

## 9. Cost Structure
- ...

## Canvas Summary

[2-3 sentence summary of the business model]

## Key Risks & Assumptions
1. ...

## Competitive Landscape
| Competitor | What they do | Your differentiation |
|-----------|-------------|---------------------|
| ... | ... | ... |

## Unit Economics (if available)
- Customer Acquisition Cost (CAC): ...
- Customer Lifetime Value (LTV): ...
- LTV/CAC ratio: ...
- Payback period: ...
(Mark unvalidated numbers with "(unvalidated)")

## Recommended Next Steps
1. ...
```

## Phase 7.5: User Journey Map (用户旅程地图, Optional)

If requested, map the user's full journey from awareness to loyal usage:

| 阶段 | 用户行为 | 用户感受 | 触点 | 痛点/机会 |
|------|----------|----------|------|-----------|
| 发现 | 如何第一次听说产品 | 好奇/怀疑 | ... | ... |
| 了解 | 如何了解产品功能 | 期待/困惑 | ... | ... |
| 首次使用 | 第一次上手体验 | 兴奋/受挫 | ... | ... |
| 持续使用 | 日常使用模式 | 满意/无感 | ... | ... |
| 推荐 | 是否会推荐给同事 | 自豪/犹豫 | ... | ... |

For each stage, identify:
- **Moments of truth**: Where the user decides to continue or leave
- **Drop-off risks**: Where users are most likely to abandon
- **Delight opportunities**: Where you can exceed expectations

This complements the VPC by showing the temporal dimension of the customer experience.

## Phase 8: Iteration Guidance

After the first canvas is complete, guide the user on when to re-run:

- **Re-run VPC** when: new customer interviews reveal different jobs/pains/gains,
  product scope changes significantly, or a Test Card invalidates a key assumption
- **Re-run BMC** when: revenue model changes, new partnership opportunity emerges,
  cost structure changes significantly, or entering a new customer segment
- **Never treat the canvas as final** — it's a living document that evolves with evidence

When re-running, load the previous canvas files and highlight what changed.

### Version Comparison (版本对比)

When generating an updated canvas, automatically append a changelog section:

```markdown
## 变更记录

| 日期 | 变更模块 | 变更内容 | 触发原因 |
|------|----------|----------|----------|
| 2026-XX-XX | 客户细分 | 新增 CRO 细分 | 用户访谈发现新需求 |
| 2026-XX-XX | 价值主张 | 移除功能 X | Test Card #3 否决 |
```

This creates an audit trail of how the business model evolved with evidence.

## Interaction Style

- Ask ONE block at a time, not all at once
- Pre-fill what you can infer from the codebase, then ask for confirmation
- Use the "pre-fill → confirm → refine" loop for each block
- If the user can't answer a question, mark it as "(unvalidated — needs user research)"
  and add a corresponding Test Card
- Push for specificity: "SMBs in biotech" is not a customer segment;
  "Process development scientists at CRO companies with 20-100 employees" is

## Competitive Analysis Framework (竞争分析框架)

When filling BMC Block 2 (Value Propositions) and the Competitive Landscape section,
use a simplified Porter's Five Forces + positioning analysis:

### Five Forces Quick Check

| 力量 | 评估 (高/中/低) | 说明 |
|------|-----------------|------|
| 现有竞争者威胁 | ? | 谁在做类似的事？ |
| 新进入者威胁 | ? | 进入门槛高不高？ |
| 替代品威胁 | ? | 用户还能用什么方式解决？ |
| 买方议价能力 | ? | 客户有没有别的选择？ |
| 供方议价能力 | ? | 关键供应商（如 LLM API）能不能掐住你？ |

### Positioning Map

Place competitors on a 2D grid using the two most important differentiation dimensions
for this market (e.g. price vs depth, generality vs specialization). Mark where the
product sits and where the white space is.

## Integration with office-hours Skill

If the user has already run Garry Tan's office-hours skill (from gstack), pull insights:

- **Q1 (Demand Reality)** answers → feed into Customer Jobs and Pains
- **Q2 (Status Quo)** answers → feed into Competitive Landscape
- **Q3 (Desperate Specificity)** answers → feed into Customer Segments
- **Q4 (Narrowest Wedge)** answers → feed into Recommended Wedge in Fit Assessment
- **Q5 (Observation)** answers → feed into User Journey Map
- **Q6 (Future-Fit)** answers → feed into Environment Map / Key Trends

If office-hours has NOT been run yet, suggest running it first:
"建议先用 office-hours skill 回答 6 个强迫问题，再来填画布。顺序：先诊断，再建模。"

## Anti-patterns

- Do NOT generate a canvas without reading the actual codebase first
- Do NOT fill in vague descriptions like "various customers" or "multiple channels"
- Every entry must be specific enough to be actionable
- Do NOT skip the fit assessment — it's the most valuable part
- Do NOT assume the user knows business terminology — explain jargon in Chinese
  if the user communicates in Chinese
- Revenue numbers should be ranges, not precise guesses — mark unvalidated
  numbers with "(unvalidated)"
- Do NOT generate Test Cards for assumptions that are already validated
  (e.g. "customers exist" when there's a signed contract)
- Do NOT ask all questions at once — the user will disengage
- Do NOT output the final canvas until all blocks have been discussed with the user

## References

This skill implements the methodology from:
- Alexander Osterwalder & Yves Pigneur, "Business Model Generation" (2010)
- Alexander Osterwalder et al., "Value Proposition Design" (2014)
- David Bland & Alexander Osterwalder, "Testing Business Ideas" (2019)
- Strategyzer.com official canvas templates and testing framework

## Glossary (中英术语对照表)

| 英文 | 中文 | 简要说明 |
|------|------|----------|
| Business Model Canvas (BMC) | 商业模式画布 | 用 9 个模块描述一个商业模式的工具 |
| Value Proposition Canvas (VPC) | 价值主张画布 | 把客户需求和产品价值对应起来的工具 |
| Customer Jobs | 客户任务 | 客户要完成的事情（功能/社会/情绪三类） |
| Pains | 客户痛点 | 客户完成任务时遇到的困难 |
| Gains | 客户收益 | 客户完成任务后想要的好处 |
| Pain Relievers | 痛点解决方案 | 产品如何减轻客户痛点 |
| Gain Creators | 收益创造方案 | 产品如何创造客户收益 |
| Problem-Solution Fit | 问题-方案匹配 | 你的方案真的解决了客户最痛的问题吗 |
| Product-Market Fit (PMF) | 产品-市场匹配 | 产品在市场上被验证有人愿意持续付费使用 |
| Customer Segments | 客户细分 | 你最重要的客户群体是谁 |
| Revenue Streams | 收入来源 | 客户怎么付钱给你 |
| Key Resources | 核心资源 | 实现价值主张需要的关键资源 |
| Key Activities | 关键活动 | 实现价值主张需要做的关键事情 |
| Key Partnerships | 重要合作 | 关键的合作伙伴和供应商 |
| Cost Structure | 成本结构 | 运营这个商业模式的主要成本 |
| Channels | 渠道 | 你怎么触达客户、交付价值 |
| Customer Relationships | 客户关系 | 你跟客户之间是什么类型的关系 |
| Test Card | 验证卡片 | 用来测试一个假设的结构化工具 |
| Learning Card | 学习卡片 | 测试后记录学到了什么的工具 |
| Progress Board | 进度追踪表 | 跟踪所有假设验证状态的表格 |
| Wedge | 切入点 | 最小可行的市场入口 |
| CAC | 客户获取成本 | 获得一个新客户要花多少钱 |
| LTV | 客户终身价值 | 一个客户一辈子给你贡献多少收入 |
| TAM | 总可触达市场 | 你的产品理论上能覆盖的最大市场 |
| SAM | 可服务市场 | 你当前能力能覆盖的市场范围 |
| SOM | 可获取市场 | 你现实中能拿到的市场份额 |
| Desirability | 需求性 | 客户是否真的想要这个 |
| Feasibility | 可行性 | 你是否真的能做出来 |
| Viability | 商业可行性 | 你是否真的能靠这个赚钱 |
| MVP | 最小可行产品 | 能验证核心假设的最简版本 |
| Pivot | 转向/调整方向 | 假设被否定后改变策略 |
| Porter's Five Forces | 波特五力 | 分析行业竞争格局的经典框架 |
| Environment Map | 环境地图 | 分析外部环境的四象限工具 |

## Language

Match the user's language. If the user writes in Chinese, output the canvas in Chinese
with English terms in parentheses where helpful (e.g. "客户细分 (Customer Segments)").
When a glossary term appears for the first time in output, briefly explain it in
parentheses if the user communicates in Chinese.
