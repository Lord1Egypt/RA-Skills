---
name: Customer Persona Copy Map
version: 1.1.0
tags: [customer-persona, copywriting, tone-of-voice, marketing-messaging]
---
# Customer Persona Copy Map

## Purpose

This skill turns audience research and customer signals into a practical copy matrix that maps different personas to their specific pain points, motivations, objections, preferred benefits, and CTA language. Instead of one-size-fits-all copy, it helps teams segment messaging across product pages, ad creative, email flows, and landing pages — all while clearly labeling what's evidence-based vs. assumed.

## Triggers

- "Map copy to different customer personas"
- "Create persona-based messaging for my product"
- "Build a copy matrix for audience segments"
- "Segment my product messaging by buyer type"
- "Write persona-specific ad copy"
- "Create messaging for different customer types"

## Workflow

1. **Audience signal collection** — Gather known customer segments, demographic/behavioral signals, purchase data patterns (if available), review themes by customer type, support ticket themes, and any existing persona research.
2. **Evidence vs. assumption separation** — For each persona, clearly separate: what data supports this segment (reviews, sales data, survey results) vs. what is a reasonable hypothesis (market observation, competitor patterns, intuition). Assumptions must be labeled.
3. **Persona card creation** — For each distinct persona, create a card with: name/descriptor, primary need/job-to-be-done, dominant purchase barrier, emotional driver, trust requirement, and preferred channel.
4. **Pain-benefit-message matrix** — Create a cross-reference matrix: persona → top pain points → product benefits that address them → message framing → CTA language → best channel.
5. **Copy snippet drafting** — Write persona-specific copy snippets: above-the-fold headline, key benefit statement, objection pre-handler, and CTA. Each snippet should feel natural for that persona.
6. **Channel recommendation** — For each persona-message pair, recommend the best channel(s) and format (e.g., "gift-buyer persona → Instagram Story with gift-guide angle").
7. **Validation plan** — For every low- or medium-evidence persona, recommend one lightweight validation test before major ad spend.

## Prompt Templates

### 1. Persona Copy Matrix Builder (`persona_matrix`)

**Purpose:** Build a complete persona-to-copy matrix from audience data.

**Input:**
- `${product_name}` — Product name
- `${product_category}` — Product category
- `${personas}` — List of customer persona descriptions (2–5 personas)
- `${product_benefits}` — Key product benefits
- `${channels}` — Available marketing channels
- `${evidence_sources}` — (Optional) data sources supporting persona definitions

**Output:** Complete matrix with persona cards, pain/benefit/message map, copy snippets, and channel recommendations.

### 2. Persona Expander (`persona_expand`)

**Purpose:** Expand a thin persona description into a full messaging profile.

**Input:**
- `${persona_name}` — Persona name or descriptor
- `${known_traits}` — What's known about this persona
- `${product_context}` — What this product does for them

**Output:** Expanded persona card with messaging angles, objections, and copy snippet drafts.

### 3. Message Adapter (`message_adapt`)

**Purpose:** Adapt one core message to multiple persona framings.

**Input:**
- `${core_message}` — The central product message
- `${personas}` — List of personas with key motivations
- `${channels}` — Target channels for adaptation

**Output:** Persona-specific message adaptations with rationale for changes.

### 4. Assumption Auditor (`assumption_audit`)

**Purpose:** Audit a persona set for untested assumptions that could lead to wasted spend.

**Input:**
- `${persona_set}` — Complete persona definitions with messaging
- `${evidence_available}` — What data actually supports each persona

**Output:** Each persona scored by evidence strength (High/Medium/Low), with assumptions highlighted and test recommendations for low-evidence personas.

## Output Format

```
## Persona Copy Map: [Product Name]
**Category:** [Category] | **Personas:** [N personas]

### Persona Cards

**Persona 1: [Name/Descriptor]**
- **Primary Need:** [Job-to-be-done]
- **Dominant Barrier:** [What keeps them from buying]
- **Emotional Driver:** [What feeling motivates them]
- **Trust Requirement:** [What proof they need]
- **Preferred Channel:** [Where they're most reachable]
- **Evidence Strength:** [High/Medium/Low] — [what data supports this]

**Persona 2: [...]**
...

### Pain-Benefit-Message Matrix

| Persona | Top Pain | Product Benefit | Message Frame | CTA Language | Best Channel |
|---|---|---|---|---|---|
| Persona 1 | [Pain] | [Benefit] | [How to frame] | "[CTA]" | [Channel] |
| Persona 2 | [Pain] | [Benefit] | [How to frame] | "[CTA]" | [Channel] |
| ... | ... | ... | ... | ... | ... |

### Copy Snippets

**For [Persona 1]:**
- 🎯 Headline: "[Above-the-fold headline]"
- 💡 Benefit: "[Key benefit statement]"
- 🛡️ Objection handler: "[Pre-handle common objection]"
- 🚀 CTA: "[Call to action]"

**For [Persona 2]:**
...

### Channel Recommendations
- **[Channel]:** Best for personas [X, Y] — format: [suggestion]
- **[Channel]:** Best for persona [Z] — format: [suggestion]

### Assumption Audit
- ✅ Persona 1: [Evidence strength] — supported by [sources]
- ⚠️ Persona 2: Medium evidence — [assumptions] need validation via [test idea]
- ❓ Persona 3: Low evidence — consider deprioritizing until [validation method]

### Validation Plan
- **Persona / claim:** [what needs validation]
- **Test:** [survey, landing-page A/B, interview, review mining, small ad test]
- **Success signal:** [CTR, conversion, qualitative pattern, objection frequency]
- **Stop condition:** [when to drop or rewrite the persona/message]
```

## Safety Rules

- **ALWAYS** clearly label assumptions vs. evidence — unvalidated personas can waste budget and alienate real customers
- **NEVER** stereotype based on protected characteristics (age, gender, race, religion, disability, sexual orientation) when the data doesn't support it
- **NEVER** create personas for sensitive categories (health conditions, financial distress, personal crises) without extreme care and explicit disclosure of limitations
- **ALWAYS** avoid manipulative messaging that exploits persona vulnerabilities (e.g., insecurity-based marketing to teens, fear-based messaging to elderly)
- **NEVER** present assumed personas as "proven by AI" — clearly state the evidence basis for every segment
- **ALWAYS** prefer behavioral or job-to-be-done segmentation over protected traits when possible
- **ALWAYS** include a validation test for personas built mostly from assumptions

## Examples

### Example 1: Skincare Serum (3 Personas)

**Input:** Product="Vitamin C Brightening Serum", Personas="(1) Skincare Beginner — wants results without complexity, (2) Ingredient Nerd — researches every component, (3) Gift Buyer — buying for someone else, wants safe choice"

**Output:** Matrix showing: Beginner → pain="too many choices, don't know what works" → message="One serum, proven ingredients, simple routine" → CTA="Start your 2-step routine" → channel=Instagram/TikTok. Ingredient Nerd → pain="skeptical of marketing claims" → message="15% L-AA + E + ferulic, airless pump, dermatologist-tested — here's the data" → CTA="See the full ingredient breakdown" → channel=blog/email. Gift Buyer → pain="will they like it? will it work for their skin?" → message="Universally loved, fragrance-free, suitable for most skin types, beautiful packaging" → CTA="Gift the glow" → channel=Facebook/Instagram.

### Example 2: Kitchen Gadget (2 Personas)

**Input:** Product="Air Fryer Liners", Personas="(1) Convenience Cook — wants faster cleanup, (2) Eco-Conscious Cook — wants to reduce waste (aluminum foil/paper)"

**Output:** Matrix: Convenience → pain="air fryer cleanup is annoying" → message="Cook, eat, toss the liner — no scrubbing" → CTA="Make cleanup optional" → channel=TikTok. Eco-Conscious → pain="using disposable foil/paper feels wasteful" → message="Reusable silicone liners replace hundreds of foil sheets" → CTA="Cook cleaner, waste less" → channel=Instagram/blog. Assumption audit flags that "Eco-Conscious" is partially assumed — recommended survey validation.


## Usage Scenarios

### Scenario 1

**User Input:** "Create a copy map for 3 personas: 'Budget Parent', 'Tech Enthusiast', and 'Eco Minimalist' for our reusable water bottle."

**Expected Output:** A 3-column copy matrix: headline variants, benefit statements, objection-handling lines, and CTA language tailored to each persona's core motivation.

### Scenario 2

**User Input:** "Review our current landing page copy. Are we over-indexing on 'Tech Enthusiast' and alienating 'Budget Parent'?"

**Expected Output:** Sentiment and vocabulary analysis. Highlights 7 phrases that resonate with tech audience but may confuse or put off budget-conscious buyers. Suggests inclusive alternatives.

### Scenario 3

**User Input:** "Generate A/B test copy variants for Facebook ads targeting 'Eco Minimalist' vs. 'Budget Parent'."

**Expected Output:** Four ad-copy pairs (2 per persona) with distinct emotional hooks, value propositions, and CTAs, formatted for Facebook's character limits.


### Scenario 4: 淘宝店写文案没人看
**User input:** "我在淘宝开了个店卖女装，详情页写了一大堆产品描述但转化率不到1%。感觉我的客户根本不知道我想说什么。怎么办？"
**Expected output:** 淘宝详情页文案体系——第一步：定义核心客户（年龄/职业/收入/风格/痛点/她为什么来淘宝买而不是线下去买）；第二步：针对她最关心的3个问题写文案（显瘦/不廉价/面料舒服还是设计独特/怎么搭配/要不要干洗——从评价和问大家里找高频词）；第三步：详情页结构（头图短视频→痛点共鸣句→产品尺寸实测图→面料细节放大→搭配推荐→买家秀集锦→退换政策）；第四步：A/B测试（用生意参谋对比不同标题/主图的点击率，找到点击率最高的组合）。关键工具：生意参谋+直通车流量解析+评价分析。

## Related Skills

- [listing-bullet-booster](../listing-bullet-booster/) — For persona-specific bullet variants
- [campaign-angle-spark](../campaign-angle-spark/) — For campaign angles targeting specific personas
- [faq-objection-crusher](../faq-objection-crusher/) — For persona-specific objection handling
