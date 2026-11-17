---
name: ai-industry-infographic
description: Generates complete ChatGPT-ready prompt packages for AI industry infographics. This skill should be used when the user needs to create data-rich information graphics about AI industry topics (LLM landscape, embodied AI, chip supply chain, computing costs, industry history, etc.), especially following large industry events. It covers the full workflow: topic design, parallel web research, data verification (web-verify-protocol), structured prompt writing, social media copy. Productized output: 生图素材包（选题+核实数据+Prompt+文案），可独立售卖或订阅. Triggers: 做信息图, 生图素材包, 生成Prompt, AI产业链图, 行业信息图, WAIC信息图, 做个选题的生图包.
agent_created: true
---

# AI Industry Infographic Generator

Generate complete, ChatGPT-ready infographic prompt packages for AI industry
topics. Each package includes verified data, structured prompts, and social
media copy.

## Workflow

### Step 1: Topic Design

Classify the infographic into one of these visual types based on data shape:

- **Multi-layer architecture** → Vertical stack diagram (e.g., industry chain layers, tech stack)
- **Time-series comparison** → Timeline + funnel chart (e.g., market consolidation, year-over-year evolution)
- **Competitive comparison** → Radar chart + bar chart (e.g., China vs US, multi-company benchmarks)
- **Cost breakdown** → Pie/donut chart + waterfall (e.g., BOM analysis, price decline curves)
- **Ecosystem map** → Radial/constellation diagram (e.g., corporate structure, investment network)
- **Scenario matrix** → 2×2 matrix + progress bars (e.g., deployment maturity by sector)

### Step 2: Parallel Web Search

Execute 3-5 simultaneous searches from different angles. Typical angles:

1. Official/authoritative data (government reports, official exhibitor lists, financial filings)
2. Industry analyst coverage (甲子光年, 36Kr, 凤凰科技, 界面新闻)
3. International comparisons (English-language sources for global benchmarks)
4. Niche/supplementary data (specific company financials, supplier lists, historical archives)
5. Recent news (past 48 hours for latest developments)

Search in both Chinese and English. Prioritize primary sources over secondary reporting.

### Step 2.5: Red Flag Pre-Screen (BEFORE verification)

**Purpose**: Before spending 3 rounds verifying data, immediately identify and
remove data patterns that have a near-100% failure rate in prior verification
runs. This saves 2-3 rounds of unnecessary cross-verification on data that will
never pass.

**Run this 8-item checklist on every search result before proceeding to Step 3**:

| # | Red Flag | Action |
|---|---------|--------|
| 1 | "XX是YY的独家供应商" | Flag 🔴. Remove "独家". If the supplier relationship is real, keep company name without "独家". |
| 2 | 进口高端产品 vs 国产低端产品价格对比（如"进口12万 vs 国产3000元"） | Flag 🔴. Delete the comparison. Different specs/tiers cannot be directly compared. |
| 3 | "全球第一""全国首家"无具体统计范围和来源 | Flag 🔴. Delete superlative unless S-grade source specifies exact scope and methodology. |
| 4 | 精确到个位数的异常高数字（118亿/17亿） | Flag 🔴. Return for source verification. If no S-grade source, delete the number. |
| 5 | BOM成本百分比未指定具体产品和测算机构 | Flag 🔴. Downgrade to 🟡 B-level and annotate: "XX方案下XX机构测算". |
| 6 | "订单排到20NN年" | Flag 🔴. Delete. Replace with qualitative milestone from company announcement. |
| 7 | 国产化率精确到个位（如73.5%） | Flag 🔴. Convert to range or qualitative description. No unified statistical authority exists. |
| 8 | "估值/收入比XX倍""市场规模仅XX亿" | Flag 🔴. Annotate source. If no S/A-grade source, delete or use qualitative language. |

**After pre-screen**: Only data that PASSES all 8 checks enters Step 3 verification.
Flagged data is either deleted, or annotated as 🔴 and excluded from any output
file. This is NOT a suggestion — it's a hard gate.

---

### Step 3: Data Verification (CRITICAL — 3-pass protocol)

Single-source reporting frequently contains inaccuracies. Every key data point
must survive a 3-pass verification before entering the output.

#### Pass 1: Source Grading

Classify each source before using its data:

| Grade | Examples | Reliability | Rule |
|-------|----------|------------|------|
| **S** | 公司官网公告、招股书、监管文件、央媒首发（新华社/中新社）、政府白皮书 | Highest | Can be primary source |
| **A** | 证券时报/中国证券报/上海证券报/第一财经、IDC/高工等权威第三方数据 | High | Must cross-verify with at least one S or another A |
| **B** | 36Kr/虎嗅/界面/凤凰科技/甲子光年/每日经济新闻 | Medium | Must cross-verify with at least one S or A |
| **C** | 自媒体号/头条文章/公众号/小红书/微博 | Low | Never use as sole source; S or A must independently confirm |

#### Pass 2: Cross-Verification Rules

For each data point, apply these rules in order:

1. **Business metrics (出货量, 融资额, 估值, 部署台数, 价格)** → Require S + A or A + A. Never use a single B source alone.
2. **Official announcements (首发, 镇馆之宝, 战略合作)** → Require S or two independent A sources.
3. **Narrative claims ("零失误", "全球第一", "行业首次")** → Require S. If only B or C, downgrade to "据X报道" with explicit attribution.
4. **Temporal data (成立时间, 发布日期)** → Require S or A. Wikipedia/企查查 acceptable as A.

#### Pass 3: Conflict Resolution

When sources disagree on the same data point:

1. **Prefer S over A over B over C** — company's own announcement beats media paraphrasing
2. **Prefer newer over older** — later reporting often corrects earlier errors
3. **Flag the conflict** — if both sources are credible but disagree, use the higher-grade source and add a footnote: "注：另有报道称[不同数据]，本文以[来源]为准"
4. **Example from WAIC project**: 中国证券报(B) reported 智元在富临精工 "工位1→4, 负载5→14kg", but 智元官网(S) reported "作业点位2→15个". 智元官网 data used because S > B.

#### Red Flags That Trigger Re-Verification

- Any superlative claim ("全球首次", "唯一", "最大") without S-grade sourcing
- Exact round numbers (100, 1000, 10000) — often rounded or estimated
- Data attributed to "业内人士" or "据透露" without named sources
- Numbers that differ significantly between two B-grade media sources
- Statistics that would require access to non-public data (e.g., exact competitor shipment numbers)
- **"独家供应商" claims** — almost never confirmed in public filings. Downgrade to "已进入供应链" or softer language.
- **Cross-tier price comparisons** — comparing high-end imports to low-end local products is apples-to-oranges. Describe price ranges separately, don't use "vs".
- **BOM claims without product/model specification** — "执行器占BOM 30-60%" is meaningless without specifying which robot and which research institution.
- **"订单排到202N年"** — companies rarely publicly confirm multi-year forward order books. Use qualitative milestones instead ("已进入小批量生产").
- **国产化率 as exact percentage** — no unified statistical authority exists for most niche component categories. Use ranges or qualitative descriptions.

### ⛔ Step 3.5: Mandatory 3-Round Verification (STRUCTURAL GATE)

> **通用版**: 本协议已独立为 `web-verify-protocol` skill（三轮联网搜索验证协议），
> 适用于任何"AI 出数据"场景。此处保留完整版供信息图上下文使用，修改时需两边同步。

**Core principle**: A single search pass catches ~70% of errors. A second catches
~90%. Only three independent passes catch close to 100%. This is not a suggestion
or a "review checklist"—it is a structural requirement built into the workflow.

**How this gate works**: You cannot "interpret" your way around it. Below are hard
quantitative minimums. If they are not met, Step 4 is blocked.

---

#### Round 1 — Fresh search, S-grade upgrade (min 3 WebSearch calls)

Search from angles that did NOT appear in Step 2. The goal is not to review what
you already found—it is to find *better* sources.

**Hard minimums**:
- At least 3 separate WebSearch calls, each from a different angle
- At least 1 search must target S-grade sources specifically (company official
  announcements, Xinhua/CNS, government white papers, financial filings, gov.cn)
- Result: Every data point classified as S or A in Pass 1 (Step 3). Any data
  stuck at B-grade after R1 must be flagged as ⚠️ unverified.

**What R1 catches**: Media paraphrasing errors (e.g., "双足人形" vs "轮式"),
imprecise metrics, wrong company attribution, outdated pre-event data used as current.

---

#### Round 2 — Independent cross-verification (min 3 WebSearch calls)

Take R1's verified data and search for a *second independent source* that confirms
or challenges each key metric. You are looking for sources that did NOT appear in
R1 results—new outlets, new angles, new search queries.

**Hard minimums**:
- At least 3 separate WebSearch calls
- At least 1 search must target factual disputes (search for "[claim] + 核实" or
  "[claim] + correction")
- Result: Every business metric confirmed by ≥2 independent S or A sources.
  Single-source metrics must be explicitly annotated: "单源确认，待交叉验证"

**What R2 catches**: Single-source errors propagated when media quote each other,
outdated numbers republished as current, regional data misattributed as national.

---

#### Round 3 — Narrative claim audit (min 2 WebSearch calls)

This round ONLY targets storytelling numbers: percentage improvements, "X-fold"
claims, before/after comparisons, superlatives, any number that feels "too neat."

**Hard minimums**:
- At least 2 separate WebSearch calls
- Each call must target a *specific* narrative number from your data tables
  (not a general topic search)
- Result: Every narrative claim must have an S or A source. Claims from B/C
  sources are either replaced with S-grade alternatives or explicitly attributed
  ("据XX白皮书") and marked ⚠️.

**What R3 catches**: B-grade white papers and analyst reports using imprecise
storytelling numbers contradicted by S-grade company/government data.

---

#### ⛔ BLOCKING GATE — Print this before ANY output file

**You MUST print the following report in your conversation response BEFORE the
first Bash call that writes a file. This is the user's only way to verify rounds
were completed without asking "did you run three rounds?"**

```
══════════ 三轮核实报告 ══════════
R1 S级升级: {N}次搜索, {M}个数据点从B升到S/A, {K}个仍为⚠️单源
R2 交叉验证: {N}次搜索, {M}个指标≥2源确认, {K}处修正
R3 叙事审查: {N}次搜索, {M}个叙事数字审查, {K}个替换/降级
结论: ✅ 通过 / ❌ 需补充{R1/R2/R3}
═══════════════════════════════
```

If any round has fewer than the minimum calls, or if R3 found unresolved
narrative claims, the gate is **NOT passed**. Fix the gaps and re-verify.

**After the gate**: Proceed to Step 4 and write output files. The files you
deliver are the final verified version—not a draft awaiting the user to
ask for verification rounds.

---

### Step 3.6: Data Confidence Levels for Infographic Output

After the 3-round verification gate, every data point must receive a **confidence
level** that determines whether it can appear on an infographic, and with what
annotation. This is separate from source grading (S/A/B/C for the origin) — it
represents a final quality gate before visual output.

#### 🟢 A-Level — Can appear on infographic without annotation

**Condition**: S-grade source (company filings/government docs) OR A-grade source
with ≥2 independent confirmations.

**Examples**:
- SK海力士Q2毛利率83%（财报原文）
- 2026年人形机器人整机产量有望突破10万台（工信部）
- SEMI半导体材料国产化率15-20%（官方报告）

#### 🟡 B-Level — Can appear on infographic WITH source annotation

**Condition**: B-grade source with ≥2 independent confirmations, OR A-grade from
a single source. Must NOT contain superlative claims ("独家/第一/唯一/最大") without
S-grade confirmation.

**Annotation format**: "据中国信通院2026Q1，多源引述" / "摩根士丹利2026研报测算" / "行业估计"

**Examples**:
- 行星滚柱丝杠国产化率约40-50%（据信通院Q1，多源引述）
- Optimus整机BOM 1.2-1.5万美元（摩根士丹利2026研报测算）

#### 🔴 C-Level — CANNOT appear on infographic

**Condition**: Single B-grade source, OR contains unverifiable superlatives, OR
the number is abnormally high/low without official confirmation, OR different
sources for the same metric diverge by >30%.

**Treatment**: Either re-verify with stronger sources, or delete entirely. If the
insight is true but the number can't be verified, use qualitative language instead.

**Examples of what gets deleted**:
- "绿的谐波市占60%+、订单排到2027年" → 未找到公告原文，删除后将"订单排到2027年"改为"已进入小批量生产"
- "进口丝杠8-12万/套 vs 国产3000元" → 量程/精度不同不可比价，删除价格对比
- "拓普Optimus独家供应商" → "独家"无官方来源，改为"布局并推进机器人电驱执行器产业化"

#### ⚠️ 产品线差异化标准

Different output channels have different confidence thresholds:

| 产品线 | 🟢 A级 | 🟡 B级 | 🔴 C级 |
|--------|:--:|:--:|:--:|
| **商业图解（信息图/付费图）** | 必须 | 允许，标注来源 | 严格禁止 |
| **公众号文章（ECS pipeline）** | 必须 | 允许，可弱标注 | 禁止；但可用定性描述替代 |
| **公众号素材（data pack for rewriting）** | 必须 | 允许 | 禁止出现在素材文件中 |

商业图解的信息图要求最严格——数字直接印在图上，不可撤回。公众号文章经deepseek改写后有缓冲层。

#### Pattern Library: Common C-Level Red Flags

The following patterns consistently fail verification and should trigger immediate
re-verification before appearing in any output:

| Pattern | Why it fails | Correct handling |
|---------|-------------|-----------------|
| "XX公司是YY的独家供应商" | "独家"几乎从不出现在公开公告中 | 改为"供应商"或"已进入供应链" |
| 进口高端 vs 国产低端价格对比 | 规格/量程/精度不同，不可跨等级比价 | 分别描述价格区间，不写"vs" |
| "全球第一""全国首家"无范围限定 | 下线量≠交付量≠销量，统计范围不明 | 标注具体口径或删除"第一" |
| 精确到个位数的订单/收入数字（118亿/17亿） | 异常高数字通常来自单一B级源 | 退回核实公告原文，找不到就删 |
| BOM成本外推到所有产品 | Tesla Optimus的BOM≠宇树G1≠所有人形机器人 | 必须标注具体产品和测算机构 |
| "订单排到202N年" | 极少有公司公开确认远期订单 | 改为"已进入XX阶段"等定性描述 |
| 国产化率精确到个位（如73.5%） | 这类数据通常不存在统一统计口径 | 用区间（40-50%）或定性（"仍较低"） |
| "估值/收入比XX倍""市场规模XX亿" | 通常来自单一券商或媒体估算 | 标注"据XX测算"，或改为"据行业观察" |

#### Correction Propagation Rule

When a data point is revised (downgraded or deleted) in one output, all other
deliverables in the same project sharing that data must also be updated.
This applies to:
- 图解资料包 → 同步修正对应的公众号素材文件
- 公众号素材 → 同步修正ECS inbox中已上传的素材（需重新scp）
- 交叉矩阵 → 如果数据出现在矩阵中，同步修正

### Step 4: Structured Output

Write the output in this exact four-section format:

```
# 生图 NXX：{Chinese Title}

## 一、选题定位
- Title (one line)
- Hook (one sentence summarizing the key insight)

## 二、核心数据
- Structured tables with verified figures
- Comparison tables, timelines, or hierarchical breakdowns
- Annotate data sources inline

## 三、ChatGPT 生图 Prompt
- English prompt with clear layout instructions
- Specify chart types, color palette, data points to include
- Add: "No realistic faces or product photos. Dark tech background (#1a1a2e)."

## 四、发帖文案
- 120-200 characters
- One sentence per paragraph (一句一段)
- No markdown bold, no hashtags in body, no parallelism patterns
- Conversational, first-person tone with personal observations
- Close with a judgment, not a scenic ending

## 数据来源
- List all sources with dates
```

### Step 5: Title + Copy Variations

Generate 5 title options for 小红书, ranked from data-shock to insight-driven:

1. Data shock (big number, surprising stat)
2. Practical utility (search-friendly,收藏-oriented)
3. Scarcity/unique angle (previously unpublished)
4. Identity hook (where do YOU fit?)
5. Knowledge summary (authoritative conclusion)

Generate 1 copy body following the tone rules above.

## Design Rules

- Every data point must be attributable to a specific source
- Never fabricate exhibitor names — cross-verify against official lists
- When official lists are available (e.g., venue brand lists), use them as ground truth
- Mark unverified claims explicitly with "需核实" or "待确认"
- Store search data even for rejected angles — they become reference for future topics

## Step 6: Post-Generation Correction Protocol

When the user or subsequent fact-checking discovers errors in a generated package:

1. **Re-verify** the disputed data point using the 3-pass protocol (Step 3)
2. **Correct in-place** — edit the source file directly, do not create a new file
3. **Propagate corrections** — if the same data appears in other packages (e.g., a company's shipment number used in N04, N08, N09), fix all occurrences
4. **Add a correction note** at the bottom of the file: `🔄 YYYY-MM-DD 修正：[具体修正内容]。来源：[S/A/B级来源]`
5. **Update the开工文档** if the data also appears in the master reference document

Example: 灵心巧手出货量从"月千台"修正为"月超4000台" → corrected in N12, propagated to any future N0X that cites this number.

## Advanced Protocols

### A. Topic Prioritization

Before generating a topic, classify its lifecycle:

| Lifecycle | Examples | Rule |
|-----------|---------|------|
| **Event-driven** (strong deadline) | WAIC闭幕数据、展会热点 | Must publish within 48h of event; skip if missed |
| **Evergreen** (no deadline) | 产业链图谱、技术栈拆解、商业模式分析 | Can publish anytime; deprioritize during event crunch |
| **Hybrid** (event hook + evergreen body) | "WAIC上看到的具身智能落地信号" | Event hook has 48h window; body is evergreen. Publish within window. |

Assign P0/P1/P2 based on lifecycle + data readiness:
- **P0**: Evergreen with all S/A-grade data verified OR event-driven within window
- **P1**: Evergreen with some B-grade data pending verification
- **P2**: Event-driven but window passed → demote or skip

### B. Data Reuse Across Topics

When multiple topics share the same data (common in a series about one event):

1. **Establish a single source of truth** — put shared data in the开工文档 appendix, not duplicated in each topic file
2. **Cross-reference by topic ID** — in each topic file, cite "数据详见开工文档附录 N04" rather than re-copying
3. **When data is updated** — update in the appendix first, then check all referencing topics
4. **Mark shared data as such**: "📎 共享数据 — 与N04/N08共用，修改时需同步"

### C. 小红书 Copy Tone Standards

After extensive iteration, the following rules produce natural, human-sounding copy:

**Must do**:
- Start with a personal observation or specific anecdote
- Use conversational connectors like "说实话", "有意思的是", "但真正让我意外的是"
- Include at least one concrete scene or moment (a number you noticed, a booth you walked past)
- End with a judgment, insight, or open question — not a summary

**Must NOT do**:
- No structural parallelism ("一方面...另一方面", "首先...其次...最后")
- No hashtags in body text
- No "在这个时代" "随着AI的发展" style of grand opening
- No exclamation marks as emphasis tools
- No explicit call-to-action ("关注我", "收藏这张图") — let the content earn the save

**Title formula**:
1. Data shock: "{Surprising number or stat}" — e.g., "三年降了300倍"
2. Utility: "{What problem this solves}" — e.g., "整理了两天 把中国AI产业链画成了这张图"
3. Scarcity: "{Previously unpublished angle}" — e.g., "还没人做过"
4. Identity: "{Where YOU fit}" — e.g., "如果你也在AI行业"
5. Knowledge: "{Authoritative conclusion}" — e.g., "从芯片到机器人 五层 缺一层都跑不起来"

### D. Prompt Template Library

For each visual type, use this prompt skeleton:

**2×2 Matrix**:
```
Create a [title]. LAYOUT: 2×2 matrix. X-axis: [dim1]. Y-axis: [dim2].
Four quadrants: [TL/TR/BL/BR descriptions with data]. Below matrix: [summary stats].
DESIGN: Dark tech background (#1a1a2e). [Color scheme]. No realistic faces/photos.
```

**Comparison Table**:
```
Create a [title]. LAYOUT: Clean comparison table. Columns: [list]. Rows: [list].
Use color gradient: [scheme]. Below: [additional context].
DESIGN: Dark tech background (#1a1a2e). [Specific layout notes]. No realistic faces/photos.
```

**Timeline + Funnel**:
```
Create a [title]. LAYOUT: Horizontal timeline [years] above, funnel chart below.
Timeline annotations: [key events per year]. Funnel stages: [stages with numbers].
DESIGN: Dark tech background (#1a1a2e). Gradient from [color1] to [color2]. No realistic faces/photos.
```

**Multi-Layer Architecture**:
```
Create a [title]. LAYOUT: Vertical stack of [N] layers. Each layer shows: [name, key players, stat].
Right sidebar: [cross-layer trends]. Bottom: [summary].
DESIGN: Dark tech background (#1a1a2e). Color gradient bottom-to-top. No realistic faces/photos.
```

### E. Collaboration with exhibitor-list-generator

When both skills are used in the same project:

1. **Company data in info graphics** — pull from the verified `.xlsx`, never from memory or B-grade media
2. **Sector classification** — use the same tag system from exhibitor-list-generator for consistency
3. **When adding a company to an infographic** — verify it exists in the verified list first
4. **If the infographic needs a company not in the list** — flag it for exhibitor-list-generator to verify and add

### F. Obsolescence Rules

After a major event concludes:

1. **Pre-event data** (会前预测、展商预告) → Mark as "会前数据，以实际为准" or discard
2. **Event-day data** (首日直击、排队情况) → Retain as historical record, mark date prominently
3. **Post-event analysis** (闭幕数据、行业总结) → This is the canonical reference going forward
4. **When the same metric appears in pre-event and post-event sources** → Use post-event data (e.g., 实际参展数 > 预告参展数)
5. **After 30 days** → Review all topic packages for stale data; update or annotate as needed
