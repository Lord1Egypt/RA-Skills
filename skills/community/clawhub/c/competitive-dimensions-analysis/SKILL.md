---
name: competitive-dimensions-analysis
description: Conduct comprehensive competitor research through feature comparison matrices, product positioning analysis, differentiation strategy, and competitive impact assessment.
---

# Competitive Dimensions Analysis

Conduct comprehensive competitor research through feature comparison matrices, product positioning analysis, differentiation strategy, and competitive impact assessment.

## Use Cases

- Researching competitors
- Comparing capabilities across multiple products/services
- Assessing competitive positioning
- Preparing competitive strategy briefs
- Analyzing market landscape
- Developing differentiation strategies
- SWOT analysis

## Core Workflow

### Step 1: Clarify Analysis Objectives and Scope

Before beginning analysis, confirm with the user:

1. **Analysis Objective** — Understanding competitors for: capturing market share? Identifying differentiation opportunities? Evaluating product roadmap? Or investment/partnership decisions?
2. **Competitor Scope** — Which competitors does the user already have in mind? Which ones need to be added?
3. **Comparison Dimensions** — Features, pricing, user experience, technical architecture, market positioning, target audience, growth strategy?

> If the user does not specify comparison dimensions, prioritize covering: core features, pricing model, user experience, and differentiation points.

### Step 2: Information Gathering

Use multi-source search strategies to gather competitor information:

```markdown
Search Dimensions:
- Product features and capabilities (official websites, help docs, product demos)
- Pricing strategy (pricing pages, public reports)
- User reviews and feedback (App Store, marketplaces, social media)
- Company background and funding (Crunchbase, public reports)
- Tech stack and architecture (developer docs, tech blogs)
- Market performance and growth (public data, third-party reports)
```

### Step 3: Build Feature Comparison Matrix

Use `references/feature-matrix-template.md` as a template to output a structured comparison matrix:

```
| Dimension          | Our Product | Competitor A | Competitor B | Competitor C |
|--------------------|-------------|--------------|--------------|--------------|
| Core Features      |             |              |              |              |
| Pricing            |             |              |              |              |
| Target Users       |             |              |              |              |
| Differentiation    |             |              |              |              |
| User Experience    |             |              |              |              |
| Integration Ecosystem |          |              |              |              |
| Customer Support   |             |              |              |              |
```

Mark each feature with: ✅ Fully supported / ⚠️ Partially supported / ❌ Not supported / 📌 Key differentiator

### Step 4: Positioning Analysis

Analyze each competitor's positioning strategy across the following dimensions:

1. **Target Users** — Which user segments are they targeting? What is their user persona?
2. **Value Proposition** — What is their core value proposition? What pain points do they solve?
3. **Brand Tone** — Brand positioning, tone, and market messaging
4. **Pricing Strategy** — Subscription / Freemium / One-time purchase / Usage-based?
5. **Market Strategy** — Primary acquisition channels, content marketing, community operations?

### Step 5: Strategic Impact Assessment

After completing the matrix and positioning analysis, provide strategic recommendations:

1. **SWOT Analysis** — Analyze strengths and weaknesses for each competitor and for our own product
2. **Differentiation Opportunities** — White space or weak points in our product offering
3. **Competitive Threat Level** — Low / Medium / High, with justification
4. **Strategic Recommendations** — Specific, actionable suggestions (feature roadmap reference, pricing adjustments, user acquisition strategies, etc.)

## Reference Resources

- **Comparison Matrix Template** → `references/feature-matrix-template.md`
- **Positioning Analysis Framework** → `references/positioning-framework.md`
- **Strategic Assessment Framework** → `references/strategic-impact-framework.md`

## Output Format

Final output should include:

1. 📊 **Feature Comparison Matrix** (table format)
2. 🎯 **Competitor Positioning Map** (textual positioning comparison)
3. ⚔️ **SWOT Analysis** (each competitor + our own product)
4. 💡 **Differentiation Opportunities and Strategic Recommendations**