# M&A Due Diligence — AI-Augmented Assessment

Run a structured due diligence analysis on any acquisition target. Covers financial, operational, technology, legal, cultural, and AI/automation readiness dimensions.

## When to Use
- Evaluating an acquisition target
- Preparing sell-side due diligence materials
- Assessing a merger partner
- Running post-LOI deep dive
- Investor or board due diligence request

## How to Use

Tell your agent: "Run M&A due diligence on [Company Name]" or "Prepare due diligence for acquiring [target]."

The agent will walk through each dimension below and produce a scored assessment with red flags, deal-breakers, and a go/no-go recommendation.

## Due Diligence Framework

### 1. Financial Health (Weight: 30%)

**Revenue Quality Score (0-100)**
| Factor | Weight | Check |
|--------|--------|-------|
| Revenue concentration | 25% | Top client <15% of revenue = green, >30% = red |
| Recurring vs one-time | 25% | >70% recurring = green, <40% = red |
| Revenue growth trend | 20% | 3-year CAGR >15% = green, declining = red |
| Gross margin | 15% | >60% SaaS / >40% services = green |
| Cash conversion | 15% | Operating cash flow / EBITDA >80% = green |

**Financial Red Flags**
- Revenue recognized before delivery
- Related-party transactions >5% of revenue
- Working capital deteriorating quarter-over-quarter
- Customer acquisition cost (CAC) payback >18 months
- Deferred revenue declining while bookings "grow"
- Off-balance-sheet liabilities or operating leases hiding debt

**Valuation Sanity Check**
| Metric | Healthy Range | Danger Zone |
|--------|---------------|-------------|
| EV/Revenue | 3-8x (SaaS), 1-3x (services) | >15x without hypergrowth |
| EV/EBITDA | 10-20x | >30x |
| Price/FCF | 15-25x | >40x or negative FCF |
| Net debt/EBITDA | <2x | >4x |

### 2. Technology & Product (Weight: 20%)

**Tech Stack Assessment**
- Architecture: Monolith vs microservices vs serverless
- Technical debt score: deployment frequency, change failure rate, MTTR
- Security posture: SOC 2, ISO 27001, penetration test recency
- Scalability: Can 10x current load without rewrite?
- AI/Agent readiness: API-first? Automation potential?
- IP ownership: Clean IP assignments from all contributors?

**Product-Market Fit Signals**
- Net Revenue Retention >110% = strong PMF
- Logo churn <5% annually = healthy
- NPS >40 = good, >60 = excellent
- Organic growth % of total = true demand signal

### 3. Legal & Compliance (Weight: 15%)

**Legal Checklist**
- [ ] Pending or threatened litigation
- [ ] IP infringement claims or risk
- [ ] Data privacy compliance (GDPR, CCPA, HIPAA)
- [ ] Employment law compliance (contractor misclassification)
- [ ] Environmental liabilities
- [ ] Tax compliance and audit history
- [ ] Change-of-control clauses in key contracts
- [ ] Non-compete/non-solicit enforceability

**Regulatory Risk Score**
- Industry-specific regulations mapped
- Compliance cost as % of revenue
- Pending regulatory changes that could impact operations

### 4. Operational Excellence (Weight: 15%)

**Operations Scorecard**
| Area | Green | Yellow | Red |
|------|-------|--------|-----|
| Employee turnover | <15% | 15-25% | >25% |
| Key person dependency | Distributed | Some concentration | Single point of failure |
| Process documentation | Comprehensive | Partial | Tribal knowledge |
| Vendor concentration | Diversified | 2-3 critical | Single vendor lock-in |
| Customer support quality | <2hr response, >90% CSAT | 4-8hr, >80% CSAT | >24hr, <70% CSAT |

### 5. Cultural & People (Weight: 10%)

**Integration Risk Assessment**
- Leadership alignment on vision and values
- Compensation structure compatibility
- Remote/hybrid/office culture match
- Decision-making style (flat vs hierarchical)
- Glassdoor/Blind sentiment analysis
- Key employee retention risk (flight risk score)

**Retention Package Benchmarks**
| Role Level | Retention Period | Typical Package |
|------------|-----------------|-----------------|
| C-Suite | 12-24 months | 1-2x base + equity acceleration |
| VP/Director | 12-18 months | 0.5-1x base + equity |
| Key IC | 6-12 months | Spot bonus + equity refresh |

### 6. AI & Automation Readiness (Weight: 10%)

**Agent-Era Value Score**
- Data quality and accessibility (structured, labeled, API-accessible?)
- Process automation potential (which workflows can agents run?)
- AI talent on team (ML engineers, data scientists, prompt engineers)
- Existing AI/ML models or IP
- Competitive moat from proprietary data or models

**Post-Acquisition AI Uplift Estimate**
| Department | Automation Potential | Annual Savings |
|------------|---------------------|----------------|
| Customer Support | 40-60% ticket deflection | $120K-$400K |
| Sales Operations | 30-50% pipeline automation | $80K-$200K |
| Finance/Accounting | 50-70% reconciliation | $60K-$150K |
| HR/Recruiting | 40-60% screening | $50K-$120K |
| Legal/Compliance | 30-40% contract review | $40K-$100K |

## Scoring & Output

### Overall Deal Score (0-100)
- 80-100: Strong buy — proceed to LOI/definitive agreement
- 60-79: Conditional — address specific risks before proceeding
- 40-59: Caution — significant risk areas need resolution
- 0-39: Walk away — deal-breakers present

### Deal-Breaker Triggers (auto-fail regardless of score)
- Undisclosed material litigation
- Revenue fraud or restatement risk
- Key customer representing >40% revenue with no contract
- Unresolvable IP ownership dispute
- Regulatory action that could shut down operations
- Key founder/employee departure with no retention agreement

### Output Template

```
# M&A Due Diligence Report: [Target Company]
Date: [YYYY-MM-DD]
Prepared for: [Acquirer]

## Executive Summary
- Overall Score: [X/100]
- Recommendation: [BUY / CONDITIONAL / WALK]
- Key Strengths: [3 bullets]
- Critical Risks: [3 bullets]
- Estimated Integration Cost: $[X]
- Post-Acquisition AI Uplift: $[X]/year

## Detailed Scores
| Dimension | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Financial Health | /100 | 30% | |
| Technology & Product | /100 | 20% | |
| Legal & Compliance | /100 | 15% | |
| Operational Excellence | /100 | 15% | |
| Cultural & People | /100 | 10% | |
| AI & Automation Readiness | /100 | 10% | |
| **Overall** | | | **/100** |

## Red Flags
[Numbered list with severity and mitigation]

## Integration Roadmap
- Day 1-30: [Quick wins]
- Day 31-90: [System integration]
- Day 91-180: [Full operational merge]
- Day 181-365: [Optimization and AI deployment]

## Recommended Next Steps
[3-5 specific actions]
```

## 2026 Benchmarks

**M&A Market Context**
- Average SaaS acquisition multiple: 6-10x ARR (down from 15-20x in 2021)
- Due diligence period: 60-90 days (accelerating with AI tools)
- Integration failure rate: 70-90% of M&As fail to deliver expected value
- #1 reason for failure: Cultural mismatch and poor integration planning
- AI-ready targets command 15-25% premium over comparable non-AI companies

**What's Changed in 2026**
- AI/agent readiness is now a core valuation driver
- Data assets valued separately (proprietary training data = moat)
- Per-seat SaaS revenue declining — usage-based models preferred
- Remote-first companies easier to integrate (no office consolidation)
- Regulatory complexity increasing (EU AI Act, state privacy laws)

---

## Get the Full Industry Pack

This skill gives you the framework. For deep industry-specific due diligence benchmarks, financial models, and competitive intelligence templates:

🖤💛 **AfrexAI Context Packs** — $47 each, 10 industries covered
→ [Browse all packs](https://afrexai-cto.github.io/context-packs/)

📊 **Free AI Revenue Calculator** — find what you're leaving on the table
→ [Try it now](https://afrexai-cto.github.io/ai-revenue-calculator/)

🤖 **Agent Setup Wizard** — deploy your first AI agent in 15 minutes
→ [Start here](https://afrexai-cto.github.io/agent-setup/)

💰 **Bundle deals**: Pick 3 for $97 | All 10 for $197 | Everything for $247
