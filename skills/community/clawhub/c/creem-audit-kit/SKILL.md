---
name: creem-audit-kit
description: Create a Creem (Merchant of Record) audit-ready compliance pack for a SaaS/digital product website. Use when preparing for Creem review or getting unblocked after rejection: generate Privacy Policy, Terms, Refund Policy, Content Policy, and Contact/Support pages; produce a Creem-focused preflight checklist; and list where to surface required legal/support/auto-renew/price info across footer, pricing, checkout, and account pages.
---

# Creem Audit Kit

Generate an audit-ready **policy page pack + preflight checklist** for Creem review.

This skill is **not** about integrating Creem APIs; it focuses on the content and site-surface requirements that commonly block MoR onboarding/review.

## Workflow (recommended)

### Step 0 — Collect inputs (keep it minimal)
Fill the variables in `references/inputs.md` (or answer them in chat) and choose a refund model.

### Step 1 — Produce the preflight checklist
Use `references/creem-preflight-checklist.md` and tailor it to the site stack (Next.js, Webflow, etc.).
Output should be a checkbox list the team can execute.

### Step 2 — Generate the 5 required pages
Start from the templates in `assets/legal-pages/`:
- `privacy-policy.md`
- `terms-of-service.md`
- `refund-policy.md`
- `content-policy.md`
- `contact-support.md`

Rules:
- Keep statements consistent across pages (company name, domain, support email, refund window, auto-renew).
- Avoid ambiguous promises (e.g., “refund anytime”). Be explicit about eligibility, timelines, and how to request.
- If a field is unknown, insert **[TODO]** rather than hallucinating.

### Step 3 — Surface requirements on key site pages
Use `references/site-surface-requirements.md` to produce a punchlist for:
- Footer (always-visible links)
- Pricing page
- Checkout entry points / paywall
- Account / billing portal

### Step 4 — Final consistency pass
Run the consistency checks in `references/consistency-checks.md`:
- one-source-of-truth contact info
- one-source-of-truth refund policy
- no conflicting “trial / refund / cancel” language

## Output format (what to deliver)

1) `Preflight Checklist (Creem)`
2) `Legal Pages Pack` (5 markdown pages)
3) `Site Surface Punchlist` (where to add links/labels)
4) `Open questions / TODOs` (if any)

## Resource map

- Inputs: `references/inputs.md`
- Checklist: `references/creem-preflight-checklist.md`
- Site surfaces: `references/site-surface-requirements.md`
- Consistency: `references/consistency-checks.md`
- Templates: `assets/legal-pages/*.md`
