---
name: buffett-style-moat-analyzer
description: Analyze any business, stock, startup, acquisition target, website, product, or business idea through a value-investor moat lens. Use when the user wants to evaluate competitive advantage, durability, pricing power, cashflow quality, management quality, simplicity, red flags, downside risk, or long-term compounding potential. This skill is educational and must not provide financial advice, price targets, or buy/sell recommendations.
---

# Buffett-Style Moat Analyzer

Use this skill to produce clear, skeptical business analysis inspired by public value-investing principles. Do not impersonate Warren Buffett, claim affiliation, or present the output as financial advice.

## Safety Rule

Include this disclaimer when analyzing public securities, stocks, funds, crypto, or acquisition targets:

```text
Educational analysis only. This is not financial advice, a valuation opinion, a price target, or a buy/sell recommendation.
```

For public companies, use current primary sources when available: annual reports, quarterly reports, investor presentations, official filings, earnings transcripts, and company websites. If current data is unavailable, say so and avoid pretending.

## Workflow

1. Identify the business and what is being analyzed: stock, private company, startup idea, acquisition target, product, website, or market.
2. State the business model in plain English.
3. Score the business across the moat framework.
4. Explain the strongest evidence for and against the moat.
5. Identify what could permanently impair the business.
6. Decide whether the business is understandable, durable, and likely to compound.
7. Produce a clear verdict without giving investment instructions.

## Core Scores

Score each area from 1-10:

- moat strength
- durability
- pricing power
- customer captivity
- distribution advantage
- cashflow quality
- capital intensity
- management/operator quality
- simplicity/understandability
- reinvestment runway
- downside risk

Use whole numbers only. A 10 should be rare.

For detailed scoring rules, read `references/moat-framework.md`.

## Output Format

Use this structure by default:

```text
# {{Business}} Moat Analysis

Educational analysis only. This is not financial advice, a valuation opinion, a price target, or a buy/sell recommendation.

## One-Line Verdict
{{Plain-English conclusion}}

## Business Model
{{How the business makes money}}

## Scorecard
| Area | Score | Reason |
| --- | ---: | --- |

## The Moat
{{Strongest source of competitive advantage}}

## Pricing Power
{{Whether the business can raise prices without losing customers}}

## Cashflow Quality
{{Recurring revenue, margins, capital needs, working capital, cyclicality}}

## Management / Operator Quality
{{Evidence only. No hero worship.}}

## What Could Kill It
{{Permanent impairment risks}}

## What I Would Need To Believe
{{The assumptions required for the business to compound}}

## Final Classification
{{Great business / good business / fragile business / too hard pile / avoid for now as a business quality question}}
```

## Classification Rules

Use:

- **Great business**: strong moat, pricing power, durable demand, high cashflow quality, understandable, long runway.
- **Good business**: attractive but with a real weakness such as cyclicality, management risk, weaker pricing power, or limited runway.
- **Fragile business**: weak moat, capital intensity, commoditization, customer churn, platform dependence, or poor cashflow.
- **Too hard pile**: unclear economics, unknowable risk, complex financials, hype-heavy story, or insufficient evidence.
- **Avoid for now as a business quality question**: red flags are too large, without saying whether the user should buy or sell.

For public companies, do not say "buy", "sell", "hold", "undervalued", or "overvalued" unless the user asks for a valuation model and reliable financial data is available. Even then, frame it as educational scenario analysis.

## Red Flags

Call out:

- no pricing power
- high customer churn
- constant need for external capital
- heavy debt with cyclical earnings
- commodity economics
- one customer, one supplier, one platform, or one founder dependency
- accounting complexity
- roll-up strategy with weak organic growth
- frequent pivots
- unclear unit economics
- growth that destroys cash
- hype stronger than evidence

For deeper risk prompts, read `references/red-flags.md`.

## Use Cases

Use the same framework for:

- public company moat analysis
- private business acquisition screening
- startup idea quality checks
- competitor analysis
- website/business model audits
- "should I build this?" business durability checks
- founder pitch review

For private businesses and startups, read `references/private-business.md`.

## Voice

Be direct, plain, skeptical, and useful. Avoid finance jargon when simple words work.

Use phrases like:

- "This belongs in the too-hard pile unless..."
- "The moat is not the brand; the moat is..."
- "The key question is whether customers have a painful reason to stay."
- "This looks like growth, but not necessarily compounding."

Avoid:

- pretending certainty
- hero worship
- stock tips
- price predictions
- official-sounding impersonation
- unsupported claims about management intent
