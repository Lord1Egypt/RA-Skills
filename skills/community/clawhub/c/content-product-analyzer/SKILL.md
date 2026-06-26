---
name: content-product-analyzer
description: produce a commercial teardown of a post, creator profile, product page, landing page, or app page from urls, screenshots, or pasted text. use to infer audience, positioning, growth mechanics, monetization signals, credibility, sentiment, and opportunities to borrow or avoid. supports multi-link bundles and competitor comparison; separate observed facts from supported inferences and unknowns; use mixed-mode web verification when public urls are provided or freshness matters and cite sources.
---

# Content Product Analyzer

Turn raw content or product inputs into a structured commercial teardown. Focus on business value, audience, positioning, growth mechanics, credibility, sentiment, and opportunities to borrow or avoid.

## Inputs supported
- Single object: one post / creator profile / product page / landing page / app page
- Bundle: multiple URLs / screenshots / text snippets for one product or campaign
- Competitor set: multiple products/pages to compare side-by-side

## Evidence modes (must choose explicitly)
1) **User-provided only**
   - Use only what the user pasted or what is visible in screenshots.
   - Do not claim external facts.

2) **Mixed mode**
   - Allowed when: the user provides public URLs OR the user asks for “latest/pricing/reviews/current ranking” OR recency clearly matters.
   - Verify and enrich with public sources.
   - Prefer: official site → original platform page → pricing/docs → reputable review sources.
   - Cite factual claims from public sources.

## Non-negotiable rules
- Start from evidence, not vibes.
- Distinguish clearly between:
  - **Observed facts** (directly visible/quoted)
  - **Supported inferences** (reasonable, evidence-linked)
  - **Unknowns** (explicitly list)
- Prefer commercial and strategic analysis over technical implementation detail.
- For screenshots: only claim what is visible or directly implied.
- Do not overstate follower psychology, revenue, conversion rates, or traction when not evidenced.
- When input is sparse: state low confidence and keep recommendations lightweight.

## Workflow
1) Identify object type(s): post / creator profile / product page / landing page / app page / bundle.
2) Pick evidence mode: user-only vs mixed-mode.
3) Extract observable facts first.
4) Infer audience, positioning, growth/virality mechanics, monetization, sentiment.
5) Separate confirmed facts vs inferences vs unknowns.
6) Produce BOTH outputs (in order):
   - Structured summary
   - Detailed teardown
7) End with concrete advice tailored to:
   - **creator** (content packaging, hooks, formats, audience resonance)
   - **indie builder** (positioning, MVP, pricing, distribution, differentiation)

## Analysis lenses (pick what’s relevant; don’t force all)
### For creators / posts / social profiles
Assess:
- Content topic and promise
- Hook structure & attention mechanics
- Tone/persona & stylistic signatures
- Engagement structure (replies/saves/reposts/CTAs)
- Likely audience and motivations
- Credibility signals & weak signals
- Commercial intent (sponsorship, lead-gen, affiliate, community funnel, product funnel)
- What is repeatable vs personality-dependent

### For products / landing pages / app pages
Assess:
- Core problem and target user
- Positioning & category framing
- Value proposition clarity
- Feature packaging vs differentiation
- Pricing/monetization signals
- Social proof, trust, risk
- Marketability (share/buy/ignore triggers)
- Objections & opportunity space for an indie builder

## Required output format

### 1) Structured summary (compact)
Use these fields when applicable:

- **对象类型**
- **一句话定位**
- **目标用户**
- **用户想要的结果**
- **内容/产品风格特征**
- **增长或传播机制**
- **商业模式/变现线索**
- **可信度信号**
- **风险或不足**
- **可借鉴点**
- **建议动作**
- **结论置信度**: 高 / 中 / 低

### 2) Detailed teardown (long-form)
Use this default structure (adapt as needed):

# 分析标题

## 核心信息提炼
Only the highest-signal facts.

## 结构化拆解
Topic/audience/style/mechanics/commercial logic.

## 用户与市场判断
Who it is for, what desire/pain it maps to, market signal.

## 商业价值与增长判断
Monetization clues, retention/funnel logic, why it may or may not work.

## 风险、槽点与反证
What’s missing, inflated, weak, or misleading.

## 可复用方法
What a creator/indie builder can actually borrow.

## 建议
Tailor advice:
- **For creators**: topic ideas, hook patterns, audience angles, content directions.
- **For indie builders**: positioning, MVP, monetization, differentiation, GTM.

## 一句话结论
Sharp final judgment.

## Competitor comparison add-on (when user provides 2+ competitors)
If the user asks “竞品对比 / compare / vs”, append this section after the teardown:

### 竞品对比矩阵
Create a markdown table comparing:
- Positioning sentence
- Target user / job-to-be-done
- Key differentiators
- Pricing / plan structure signals
- Trust & proof
- Distribution channel guesses
- Likely wedge (why users start)
- Likely lock-in (why users stay)
- Risks / gaps

### 对比结论与切入策略
- What is easiest to copy vs defensible
- Underserved segment(s)
- Recommended wedge for the user
- 3–7 action items (sequenced)

## Quality bar
A good answer should:
- Read like a sharp operator, not a generic summarizer
- Contain explicit judgment, not just description
- Surface upside AND failure modes
- Produce at least 3 concrete suggestions when enough evidence exists
- Be honest about uncertainty
