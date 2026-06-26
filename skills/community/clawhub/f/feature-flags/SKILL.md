---
name: feature-flags
description: Deep feature flag workflow—taxonomy, targeting, lifecycle, safety and kill switches, cleanup, and governance. Use when shipping gradually, experimenting, or decoupling deploy from release.
---

# Feature Flags

Flags decouple **deploy** from **release**—and become **debt** if never removed. **Taxonomy**, **ownership**, and **retirement** matter as much as targeting.

## When to Offer This Workflow

**Trigger conditions:**

- Gradual rollouts, kill switches, or experiments behind flags
- Flag sprawl and unknown defaults
- Client vs server evaluation and hydration flicker

**Initial offer:**

Use **six stages**: (1) taxonomy, (2) targeting rules, (3) evaluation & consistency, (4) safety & ops, (5) lifecycle & cleanup, (6) governance). Confirm provider (LaunchDarkly, Unleash, ConfigCat, homegrown).

---

## Stage 1: Taxonomy

**Goal:** Separate short-lived **release** flags, long-lived **config** flags, and **experiment** flags tied to analytics.

**Exit condition:** Naming convention and expected TTL per type.

---

## Stage 2: Targeting Rules

**Goal:** Percentage rollouts, segments (tenant, plan, region), deterministic bucketing (stable user key).

---

## Stage 3: Evaluation & Consistency

**Goal:** Server-side authoritative for security and billing; client flags for UX only; avoid UI flicker on hydration (SSR/CSR agreement).

---

## Stage 4: Safety & Ops

**Goal:** Kill-switch runbook; audit trail for changes; safe defaults when provider unavailable (often “off”).

---

## Stage 5: Lifecycle & Cleanup

**Goal:** Tickets to remove flags after full rollout; periodic audits; metric for stale flags.

---

## Stage 6: Governance

**Goal:** Approvals for broadening exposure; promotion across environments; break-glass access for incidents.

---

## Final Review Checklist

- [ ] Flag types and naming documented
- [ ] Targeting and bucketing deterministic
- [ ] Server vs client boundaries clear
- [ ] Kill switches and defaults documented
- [ ] Cleanup process and ownership

## Tips for Effective Guidance

- Never put security-only gates solely in client-side flags.
- Pair with **ab-testing** when experiment analysis is primary.

## Handling Deviations

- Align with **release-management** for communication cadence.
