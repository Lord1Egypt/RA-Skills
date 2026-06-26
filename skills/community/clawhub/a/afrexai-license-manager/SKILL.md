# Software License Manager

Audit, track, and optimize your organization's software licenses. Finds waste, flags compliance risks, and builds a renewal calendar.

## What It Does

1. **License Inventory Audit** — Catalog every SaaS subscription, perpetual license, and open-source dependency across the org
2. **Waste Detection** — Flag unused seats, duplicate tools, and zombie subscriptions burning cash
3. **Compliance Risk Scanner** — Identify expired licenses, exceeded seat counts, and audit-risky gaps
4. **Renewal Calendar** — Build a 12-month renewal timeline with 60/30/15-day alerts
5. **Negotiation Prep** — Generate vendor scorecards with usage data, alternatives, and leverage points
6. **Cost Optimization Report** — Recommend downgrades, consolidations, and tier changes with projected savings

## How to Use

Tell the agent what you need:
- "Audit our software licenses" → full inventory + waste report
- "Find unused SaaS subscriptions" → waste detection with savings estimate
- "Build a license renewal calendar" → 12-month timeline with alerts
- "We're renewing Salesforce — prep negotiation" → vendor scorecard + leverage analysis
- "Check our open-source license compliance" → dependency scan for GPL/AGPL risks

## Audit Framework

### License Categories
| Category | Examples | Risk Level |
|----------|----------|------------|
| SaaS Subscriptions | Salesforce, HubSpot, Slack, Zoom | Medium — auto-renews silently |
| Perpetual Licenses | Microsoft Office, Adobe CS6 | Low — but may lack support |
| Usage-Based | AWS, Twilio, Stripe | High — unpredictable costs |
| Open Source | GPL, MIT, Apache, AGPL | Compliance risk if commercial |
| Enterprise Agreements | Microsoft EA, Oracle ULA | High — complex true-ups |

### Waste Indicators
- **Ghost seats**: Licensed users who haven't logged in 60+ days
- **Duplicate tools**: Multiple tools serving same function (e.g., Zoom + Teams + Meet)
- **Tier bloat**: Enterprise tier when Standard covers actual usage
- **Orphan licenses**: Departed employees still consuming seats
- **Shelf software**: Purchased but never deployed

### Compliance Red Flags
- Seat count exceeds license agreement
- Using software past license expiration
- GPL/AGPL code in proprietary products without disclosure
- Non-commercial licenses used commercially
- Unlicensed copies on employee machines

## Renewal Calendar Template

```
| Vendor | Product | Annual Cost | Renewal Date | Alert Date | Action |
|--------|---------|-------------|-------------- |------------|--------|
| [Name] | [Product] | $XX,XXX | YYYY-MM-DD | 60 days prior | Review/Negotiate/Cancel |
```

## Negotiation Prep Scorecard

For each renewal:
1. **Current spend** — annual + per-seat breakdown
2. **Actual usage** — DAU/MAU, feature adoption rate
3. **Alternatives** — 2-3 competitors with pricing
4. **Leverage points** — multi-year discount, volume pricing, competitor quotes
5. **Walk-away price** — your BATNA if vendor won't budge
6. **Timing** — best: 90 days before renewal, negotiate with fiscal year pressure

## Cost Optimization Playbook

### Quick Wins (Week 1)
- Remove departed employee seats → typical savings: 8-15% of SaaS spend
- Cancel unused trials and forgotten subscriptions
- Downgrade over-provisioned tiers

### Medium Term (Month 1-3)
- Consolidate duplicate tools (pick one, migrate)
- Renegotiate top 5 vendors by spend
- Implement approval workflow for new subscriptions

### Strategic (Quarter 1-2)
- Enterprise agreement consolidation
- Annual vs monthly billing optimization (typically 15-20% discount)
- Build internal tool alternatives for simple SaaS

## Industry Benchmarks

- Average company wastes **25-30%** of SaaS spend on unused or underused licenses
- Companies with 100+ employees average **130+ SaaS tools** (most don't know exact count)
- License audit typically recovers **$1,000-$3,000 per employee per year**
- Open-source compliance violation fines: **$100K-$5M+** depending on jurisdiction

## Output Formats

- **Executive Summary** — 1-page waste + risk + savings overview
- **Detailed Audit Report** — full inventory with status, usage, recommendations
- **Renewal Calendar** — spreadsheet-ready timeline
- **Vendor Scorecard** — per-vendor negotiation brief
- **Compliance Report** — risk register with remediation steps

---

## Go Deeper

This skill handles the audit and optimization framework. For full industry-specific automation contexts:

🔗 **[AfrexAI Context Packs](https://afrexai-cto.github.io/context-packs/)** — $47 per industry. SaaS, Fintech, Healthcare, Legal, and 7 more verticals with complete agent configurations.

🔗 **[AI Revenue Calculator](https://afrexai-cto.github.io/ai-revenue-calculator/)** — Find out how much your org is losing to manual processes.

🔗 **[Agent Setup Wizard](https://afrexai-cto.github.io/agent-setup/)** — Configure your AI agent stack in minutes.
