---
name: clawtrix-ecom-intel
description: "Surfaces the best ClawHub skills for e-commerce agents — Shopify, Stripe, order management, inventory, customer support, and ecom workflows. Use when: (1) Onboarding an agent working on an ecom store or marketplace, (2) An agent needs help with order processing, returns, inventory sync, or customer messaging, (3) Running weekly skill discovery for ecom-focused agents, (4) A Shopify/WooCommerce/custom store team is adding AI agent automation, (5) Identifying ecom skills before peak season (Black Friday, product launches). Outputs top 3 recommendations. Never more than 3."
metadata:
---

# Clawtrix Ecom Intel

Finds the best ClawHub skills for e-commerce agents. Personalized to your platform, catalog size, and operational focus — not a generic search result.

---

## Quick Reference

| Task | Action |
|------|--------|
| New ecom agent onboarding | Run full discovery for platform + operational focus |
| Order management gap | Run Step 2 with order/fulfillment queries |
| Customer support automation | Run Step 2 with support/returns queries |
| Pre-peak-season audit | Run full sequence, flag any skill gaps before high traffic |
| Weekly discovery | Run Steps 1-3, output to memory/ |

---

## Discovery Run Sequence

### Step 1 — Read Agent Mission

Read the agent's `SOUL.md`. Extract:

- **Ecom platform** (Shopify, WooCommerce, Magento, custom, marketplace)
- **Core workflows the agent automates** (e.g., "handles return requests", "manages inventory alerts", "processes wholesale orders")
- **Operational scale** (# SKUs, order volume, # of channels)
- **Integrations in use** (Stripe, Klaviyo, ShipStation, Gorgias, etc.)
- **Installed skills** (to avoid re-recommending)

### Step 2 — Search ClawHub for Ecom Skills

```bash
# Shopify integration
curl -s "https://clawhub.ai/api/v1/search?q=shopify&limit=10" \
  | jq '[.results[] | {slug, name: .displayName, installs, score}]'

# Order management and fulfillment
curl -s "https://clawhub.ai/api/v1/search?q=order+fulfillment&limit=10" \
  | jq '[.results[] | {slug, name: .displayName, installs, score}]'

# Inventory and catalog management
curl -s "https://clawhub.ai/api/v1/search?q=inventory+catalog&limit=10" \
  | jq '[.results[] | {slug, name: .displayName, installs, score}]'

# Customer support and returns
curl -s "https://clawhub.ai/api/v1/search?q=customer+support+returns&limit=10" \
  | jq '[.results[] | {slug, name: .displayName, installs, score}]'

# Payments and fraud
curl -s "https://clawhub.ai/api/v1/search?q=payments+fraud+ecommerce&limit=10" \
  | jq '[.results[] | {slug, name: .displayName, installs, score}]'
```

### Step 3 — Score Each Candidate

Apply Clawtrix scoring matrix:

| Dimension | Max | How to measure |
|-----------|-----|----------------|
| Mission relevance | 3 | 3=core ecom workflow (orders/inventory/customers), 2=adjacent, 1=tangential |
| Gap fill | 2 | Does the agent lack this today? |
| Community signal | 1 | installs > 1,000 = +1 |
| Recency | 1 | Updated in last 30 days = +1 |
| Trust | 1 | Clean publisher, no security flags |

### Step 4 — Ecom-Specific Filters

Before recommending:

- [ ] Compatible with the agent's ecom platform (Shopify skills don't always work on WooCommerce)
- [ ] Handles the agent's order volume — some skills have rate limit constraints
- [ ] No security flags — ecom agents handle payment data and customer PII (2-3x risk multiplier per `clawtrix-security-audit`)
- [ ] Not already installed

### Step 5 — Output Top 3

Never more than 3. Write to `memory/reports/ecom-intel-YYYY-MM-DD.md`:

```markdown
# Ecom Intel — YYYY-MM-DD

## Agent: [name]
## Platform: [Shopify / WooCommerce / custom]
## Focus: [orders / inventory / customer support / etc.]
## Skills audited: N candidates

## Top 3 Recommendations

**1. [author/slug]** (score: N/8)
- What: [one sentence]
- Why for this agent: [one sentence tied to SOUL.md + platform]
- Install: `clawhub install [slug]`

**2. ...**

**3. ...**

## Skipped
| Slug | Reason |
|...
```

---

## Ecom Risk Profile

Ecom agents commonly have access to:
- Stripe/Shopify Payments API keys (payment mutations)
- Customer PII: names, shipping addresses, purchase history
- Inventory systems with write access (can create/update/delete products)

Before installing any skill for an ecom agent, run `clawtrix-security-audit` first.
- Payment access: 3x risk multiplier
- Customer PII access: 2x risk multiplier
- Inventory write access: 2x risk multiplier

A skill that's MEDIUM risk for a coding agent may be HIGH risk for an ecom agent.

---

## Seasonality Note

Ecom agents should audit and update their skill stack **before** peak seasons:
- November (Black Friday / Cyber Monday)
- Q4 holiday shipping
- Major sales events (brand-specific)

A skill gap during peak season has higher operational impact than during slow periods.

---

## When to Use This for n8n Teams

Many ecom operators run n8n for order routing, CRM sync, and inventory automation:
- Ecom operators with n8n already have workflow logic that can be converted to ClawHub skills
- ClawHub skills replace fragile webhook-based zaps with more resilient agent-native automation

Run Step 2 with `n8n shopify` as a search query to find current ecom workflow conversion skills in ClawHub.

---

## Upgrade Note — Clawtrix Pro

This skill finds ecom skills on demand. **Clawtrix Pro** adds:
- Proactive alerts when high-signal ecom skills ship (especially Shopify and Stripe updates)
- Security monitoring for payment-access agents (highest blast radius tier)
- Pre-peak-season audit: "your ecom agent stack is ready for Black Friday / here's what to update"
- Multi-store fleet audits: compare skill stacks across store agents

---

## Version History

v0.1.0 — Initial release. Platform-specific discovery, order/inventory/support focus, ecom risk profile, seasonal audit note, n8n angle.
v0.1.1 — Cleaned up internal research notes from n8n section; now fully customer-facing.
