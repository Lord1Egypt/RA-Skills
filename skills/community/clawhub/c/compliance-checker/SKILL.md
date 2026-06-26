---
name: compliance-checker
description: Audit ecommerce listings, ad copy, and creator content against TikTok Shop policies to catch violations before they trigger penalties. Use when reviewing new listings, vetting creator videos and captions, responding to policy warnings, or building pre-publish compliance workflows.
---

# Compliance Checker

TikTok Shop enforces strict policies on product listings, promotional claims, and creator content. Violations can lead to listing removal, account suspension, or permanent bans — often without warning. This skill helps ecommerce operators proactively audit their listings, ad copy, and creator deliverables against known TikTok Shop policy requirements, catching problems before the platform does.

## Quick Reference

| Decision | Strong | Acceptable | Weak |
|---|---|---|---|
| Claim substantiation | Every objective claim mapped to evidence on file (lab test, certification, spec sheet) | Claims softened to subjective/experience language where evidence is thin | "Everyone in this niche says it" |
| Health/beauty language | Cosmetic-effect wording ("appearance of", "feels firmer") | Sensory and experience claims | Treatment/cure/prevention claims ("removes scars", "cures acne", "burns fat") |
| Before/after content | Not used, or platform-permitted formats with timeline and disclosure | Lifestyle results framing without explicit B/A comparison | Side-by-side body-transformation B/A images |
| Discount framing | Real prior price history backs every strikethrough and "X% off" | Time-limited offers with accurate end behavior | Fake urgency, perpetual countdowns, inflated reference prices |
| Creator brief | Written do/don't claim list per product, script pre-check, disclosure requirement | Caption and claim review before posting | "Creators know what to say" |
| Category/certification | Restricted-category check + required docs uploaded before listing | Category checked against current platform list | Listing first, checking after the violation notice |
| Violation response | Root-cause fix + targeted appeal with evidence + account-wide sweep for the same pattern | Appeal with corrected listing | Relist the same content with synonyms |

## Solves

1. Listings removed (or shadow-suppressed) for prohibited claims the seller did not know were prohibited.
2. Creator videos that earn commissions and violations simultaneously — health claims, fake discounts, missing disclosure — counted against the seller's account.
3. Policy warnings arriving with vague reasons and a ticking appeal window, with no idea what actually triggered them.
4. Account health scores degrading from an accumulation of small violations, putting the shop one strike from suspension.
5. Restricted categories (supplements, topicals, kids' products, electricals) listed without the required certifications.
6. Promotional pricing patterns (inflated strikethrough prices, fake countdowns) that violate deceptive-pricing rules.
7. No pre-publish review process — every listing and video is a compliance gamble.

## Workflow

### Step 1 — Scope the audit
Identify what is being audited: a new listing (title, images, description, price display), a creator deliverable (video, caption, live script), an ad, an account-wide sweep after a warning, or a violation notice response. Collect the product category, target market, and any certifications/evidence the seller holds. The audit standard differs by category — supplements and topicals get the strictest pass.

### Step 2 — Check category eligibility and documentation
Verify the product is allowed at all (prohibited list), restricted-with-requirements (certifications, brand authorization, category approval), or open. Confirm required documents exist BEFORE content review: lab tests, safety certifications (e.g., for electricals or kids' products), brand authorization letters for branded goods, ingredient disclosures. A perfectly worded listing for an unapproved restricted product is still a violation.

### Step 3 — Audit claims line by line
Extract every claim from title, bullets, description, images (including text baked into images), and video scripts. Classify each: objective/measurable (needs evidence), health/treatment (mostly prohibited — see `references/claims-and-categories.md`), superlative ("best", "#1" — needs substantiation or removal), comparative (naming competitors — high risk), guarantee/absolute ("100%", "permanent", "instant"). For each flagged claim, propose compliant replacement language that preserves selling power — auditing without rewrites is half the job.

### Step 4 — Audit pricing and promotion mechanics
Check: strikethrough/reference prices reflect a genuine recent selling price; discount percentages compute correctly; "limited time" claims have real end conditions; free-gift and bundle terms are accurate; shipping-fee representations match checkout reality. Deceptive pricing is one of the most algorithmically-detected violation classes.

### Step 5 — Audit creator/affiliate content
For each creator deliverable: claims check (same standard as listings — creators saying it counts against the shop), disclosure check (paid partnership/affiliate disclosure per platform and local ad law), prohibited formats (before/after transformations, medical settings, fear-based hooks like side-effect horror stories), and music/IP (commercial-use audio only). Produce a per-creator do/don't sheet from `references/creator-content-rules.md` so the next video starts compliant.

### Step 6 — Risk-grade and prioritize
Grade every finding: **Critical** (likely removal/suspension: prohibited claims, banned category, fake pricing) — fix before publishing; **High** (probable violation on review: unsubstantiated objective claims, missing disclosure) — fix within 24h; **Medium** (gray zone, enforcement varies: aggressive superlatives, borderline imagery) — fix in next revision; **Low** (best practice: hedging language, evidence filing). Never bury a Critical under a wall of Lows.

### Step 7 — Deliver report and prevention workflow
Output the audit using `references/output-template.md`: findings table with locations, risk grades, and ready-to-paste compliant rewrites; documentation gaps; and — for warning responses — the appeal draft with evidence list plus an account-wide sweep recommendation for the same violation pattern. Run `assets/compliance-audit-checklist.md` before delivering. Recommend a pre-publish gate: no listing or creator video goes live without passing the checklist.

## Worked Example 1 — Pre-launch audit of a supplement listing

**Input:** "Audit this listing before we publish. Product: collagen gummies. Title: 'Anti-Aging Collagen Gummies — Erases Wrinkles in 14 Days, Clinically Proven #1 Collagen'. Description includes: 'reverses skin aging', 'doctor recommended', 'cures brittle nails', before/after customer photos, '70% OFF today only!' (regular price set 3x higher than it has ever sold). We have a certificate of analysis for the ingredients but no clinical study."

**Process:** Category check: dietary supplement = restricted category — verify the shop has category approval and required documentation (COA helps; check market-specific requirements) — gate item. Claims audit: "Erases wrinkles in 14 days" = treatment claim + unsubstantiated timeline → Critical; "Clinically proven" with no study on file → Critical; "reverses skin aging" / "cures brittle nails" = disease/treatment claims → Critical; "doctor recommended" without substantiation → High; "#1 Collagen" unsubstantiated superlative → High; before/after photos in a supplement context → Critical (prohibited format); "70% OFF" against a never-sold reference price → Critical (deceptive pricing). Rewrites: "Collagen Gummies with Vitamin C — Supports Skin Elasticity & Healthy Nails" (structure/function-style support language, market-dependent — flag for local regs); replace B/A photos with texture/lifestyle imagery; reset reference price to genuine recent selling price and re-compute the discount.

**Output:** Findings table (7 findings: 5 Critical, 2 High) with line-level locations and paste-ready rewrites, documentation gap list (category approval status, substantiation file), and a hold-launch recommendation until Criticals are fixed. Notes that supplement claim rules vary by market and the compliant wording given targets the platform's general standard, with a local-regulation check advised.

## Worked Example 2 — Responding to a violation notice

**Input:** "We got 'Listing removed: Exaggerated or misleading claims' on our LED face mask (sold 1,400 units, our #2 product). The listing says 'clinically proven to eliminate acne and wrinkles', '10x collagen production', 'dermatologist approved', 'results guaranteed or money back'. Appeal window: 5 days. We have one small-sample study from the LED panel supplier and a dermatologist influencer who posted about it."

**Process:** Root cause: "eliminate acne and wrinkles" is a treatment/cure claim — primary trigger; "10x collagen production" is a specific measurable claim the supplier study (different device configuration, n=23) cannot substantiate; "dermatologist approved" based on one paid influencer ≠ approval; "results guaranteed" creates a guarantee claim. Strategy: do not appeal-as-is (appeals restating removed claims fail and burn credibility). Fix first: rewrite to red-light-therapy experience claims ("helps improve the appearance of skin texture and tone with regular use"), remove the 10x figure or cite the exact supplier study parameters if platform evidence upload allows, replace "dermatologist approved" with the influencer's genuine quote properly disclosed as sponsored, convert guarantee language into the actual return policy terms. Then appeal: acknowledge the specific violation, show the corrected listing, attach the COA/supplier docs as supporting evidence. Account sweep: the same claim pattern exists in 3 other listings and 12 creator videos — fix before the platform finds the pattern (repeat violations escalate penalties).

**Output:** Appeal draft (violation acknowledgment + corrected listing + evidence list), fully rewritten listing copy, account-wide sweep table of the same claim pattern with priorities, and a 5-day action timeline working back from the appeal deadline.

## Common Mistakes

1. **Auditing only the description.** Violations live in titles, image text overlays, video captions, pinned comments, and live-stream speech — the platform reviews all of them.
2. **Treating creator content as the creator's problem.** Affiliate and sponsored content claims attach to the seller's shop; one rogue creator video can strike the account.
3. **Synonym-swapping banned claims.** "Cures acne" → "banishes breakouts forever" is the same violation; classifiers detect claim semantics, not keywords. Change the claim type, not the wording.
4. **Appealing without fixing.** An appeal that defends the original claim almost always fails and marks the account as non-cooperative. Fix, then appeal with the fix.
5. **Inflated reference prices.** Setting a "regular price" the product never sold at to make discounts look bigger is among the most reliably detected violations.
6. **Ignoring image text.** OCR catches "FDA approved" baked into a product render even when the description is clean.
7. **One audit, then drift.** Listings get edited, creators improvise, promos change — compliance decays. Re-audit on every edit and brief every new creator.
8. **Fixing one listing and leaving the pattern.** Platforms escalate for repeat patterns; if one listing had the violation, your other listings probably do too. Sweep account-wide.
9. **Confusing platform rules with the law.** Passing TikTok Shop policy does not satisfy FTC/ASA/local ad law (and vice versa); high-risk categories need both checks.

## Resources

- `references/output-template.md` — audit report and appeal-response formats
- `references/claims-and-categories.md` — prohibited claim types by category, compliant rewrite patterns, restricted categories
- `references/creator-content-rules.md` — creator/affiliate content rules, disclosure, prohibited formats, brief template
- `assets/compliance-audit-checklist.md` — pre-delivery quality checklist
