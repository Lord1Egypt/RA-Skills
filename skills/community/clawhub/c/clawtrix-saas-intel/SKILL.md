---
name: clawtrix-saas-intel
description: "Surfaces the best ClawHub skills for SaaS-focused agents — auth, billing, onboarding, customer lifecycle, and SaaS product patterns. Use when: (1) Onboarding an agent that works on a SaaS product (billing, subscriptions, user management), (2) An agent needs help with Stripe integration, auth flows, or onboarding automation, (3) Running a weekly skill discovery for product-builder agents, (4) A SaaS team is instrumenting agents across their stack and needs a starting skill set, (5) The n8n integration angle is relevant (convert existing workflows to agent skills). Outputs top 3 recommendations. Never more than 3."
metadata:
---

# Clawtrix SaaS Intel

Finds the best ClawHub skills for SaaS product agents. Personalized to your product's domain, stack, and stage — not a generic search result.

---

## Quick Reference

| Task | Action |
|------|--------|
| New SaaS agent onboarding | Run full discovery for the product's core domain |
| Billing/payments gap | Run Step 2 with Stripe/billing queries |
| Onboarding flow automation | Run Step 2 with onboarding queries |
| n8n workflow → skill conversion | Run Step 2 with n8n-specific queries |
| Weekly discovery | Run Steps 1-3, output to memory/ |

---

## Discovery Run Sequence

### Step 1 — Read Agent Mission

Read the agent's `SOUL.md`. Extract:

- **SaaS product domain** (e.g., "project management SaaS", "billing infrastructure", "customer success platform")
- **Core user actions the agent automates** (e.g., "handles subscription upgrades", "automates onboarding emails")
- **Current tech stack** (Stripe, Auth0, Intercom, HubSpot, etc.)
- **Installed skills** (to avoid re-recommending)
- **Business model** (B2B/B2C, pricing tiers, trial flows)

### Step 2 — Search ClawHub for SaaS Patterns

```bash
# Billing and subscription management
curl -s "https://clawhub.ai/api/v1/search?q=stripe+billing&limit=10" \
  | jq '[.results[] | {slug, name: .displayName, installs, score}]'

# Auth and identity
curl -s "https://clawhub.ai/api/v1/search?q=auth+identity+saas&limit=10" \
  | jq '[.results[] | {slug, name: .displayName, installs, score}]'

# Customer onboarding
curl -s "https://clawhub.ai/api/v1/search?q=onboarding+activation&limit=10" \
  | jq '[.results[] | {slug, name: .displayName, installs, score}]'

# n8n workflow conversion (high-signal March 2026)
curl -s "https://clawhub.ai/api/v1/search?q=n8n+workflow&limit=10" \
  | jq '[.results[] | {slug, name: .displayName, installs, score}]'

# Product analytics + retention
curl -s "https://clawhub.ai/api/v1/search?q=product+analytics+retention&limit=10" \
  | jq '[.results[] | {slug, name: .displayName, installs, score}]'
```

### Step 3 — Score Each Candidate

Apply Clawtrix scoring matrix:

| Dimension | Max | How to measure |
|-----------|-----|----------------|
| Mission relevance | 3 | 3=core SaaS workflow, 2=adjacent, 1=tangential |
| Gap fill | 2 | Does the agent lack this today? |
| Community signal | 1 | installs > 1,000 = +1 |
| Recency | 1 | Updated in last 30 days = +1 |
| Trust | 1 | Clean publisher, no security flags |

### Step 4 — SaaS-Specific Filters

Before recommending, verify:

- [ ] Compatible with the product's payment provider (Stripe vs. Paddle vs. custom)
- [ ] Works at the right business model (B2B vs. B2C billing patterns differ significantly)
- [ ] No security flags — billing agents have HIGH blast radius (3x risk multiplier per `clawtrix-security-audit`)
- [ ] Not already installed

### Step 5 — Output Top 3

Never more than 3. Write to `memory/reports/saas-intel-YYYY-MM-DD.md`:

```markdown
# SaaS Intel — YYYY-MM-DD

## Agent: [name]
## Product domain: [SaaS type]
## Skills audited: N candidates

## Top 3 Recommendations

**1. [author/slug]** (score: N/8)
- What: [one sentence]
- Why for this product: [one sentence tied to SOUL.md + business model]
- Install: `clawhub install [slug]`

**2. ...**

**3. ...**

## Skipped
| Slug | Reason |
|...
```

---

## SaaS-Specific Risk Note

SaaS agents operate in sensitive environments: payment processing, user management, and customer data. This means the blast radius of a compromised skill is significantly higher than for a read-only agent.

Before installing any skill for a SaaS agent, run `clawtrix-security-audit` first. The risk multiplier for payment/billing access is 3x — a MEDIUM-flagged skill becomes HIGH risk.

---

## When to Use This for n8n Teams

SaaS teams running n8n for automation (Zapier replacement, internal workflows) are a strong fit:
- They already think in workflow automation terms
- Adding ClawHub skills to their OpenClaw agents extends their n8n investment
- Natural onboarding path: existing n8n workflow → SKILL.md → deploy to OpenClaw agent

Run Step 2 with `n8n workflow` as a search query to find current conversion tools in ClawHub.

---

## Upgrade Note — Clawtrix Pro

This skill finds SaaS skills on demand. **Clawtrix Pro** adds:
- Proactive alerts when a high-signal SaaS skill ships (especially Stripe, Auth0, billing patterns)
- Security monitoring specific to billing-access agents (highest blast radius tier)
- Fleet-level audit: "all 5 of your SaaS agents have clean stacks except agent #3"
- Monthly SaaS skills landscape report

---

## Version History

v0.1.0 — Initial release. SaaS domain discovery, billing/auth/onboarding focus, n8n integration angle, 3x risk flag for billing-access agents.
v0.1.1 — Cleaned up internal research notes from n8n section; now fully customer-facing.
