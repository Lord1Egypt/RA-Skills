---
name: affiliate-ugc-test-planner
description: Plan compliant affiliate UGC test campaigns from a product or niche into disclosure-safe hooks, short-form video briefs, carousel briefs, platform routing, cost assumptions, test metrics, and kill criteria. Use when the user wants to test affiliate products with AI-generated UGC, Pinterest pins, TikTok/Reels/Shorts, Claude/Higgsfield-style workflows, or similar content-generation systems without making unsupported income, health, or testimonial claims.
metadata: {"openclaw":{"homepage":"https://www.youtube.com/watch?v=EYZKlJmFUXw","requires":{"anyBins":["python3","python"]}}}
---

# Affiliate UGC Test Planner

Use this skill to turn an affiliate product idea into a small, compliant content test. It plans the campaign; it does not promise commissions, post content, or generate media directly.

## Workflow

1. Validate the product.
   - Identify product, audience, affiliate network, commission range, allowed traffic sources, and disclosure requirements.
   - Reject or flag products that require medical, financial, legal, or unverifiable personal-result claims.
   - Ask for real product evidence if claims are weak: landing page, product page, user reviews, usage notes, or creator-owned footage.

2. Choose the test path.
   - Pick one primary platform: Pinterest, TikTok, Instagram Reels, YouTube Shorts, Lemon8, or owned landing page.
   - State whether direct affiliate links are allowed, uncertain, or should route through an owned bridge page.
   - Separate organic tests from paid tests.

3. Build the hook matrix.
   - 5 hooks: problem, routine, comparison, objection, curiosity.
   - Each hook must avoid fake personal experience unless the user actually used the product.
   - For AI-generated people, do not present them as real customers.

4. Build content briefs.
   - 2 short video briefs.
   - 1 carousel brief.
   - Each brief includes scene idea, product evidence, caption angle, disclosure line, CTA, and failure risk.

5. Plan generation and cost control.
   - Define the minimum viable creative set before scaling.
   - Estimate generation count, not revenue.
   - Include a stop rule for tools that burn credits or require paid plans.

6. Define measurement.
   - Track posts, impressions, saves, clicks, outbound CTR, affiliate network clicks, conversion events if available, and policy/account issues.
   - Give day-3 and day-7 kill criteria.

## Output Format

Start directly with the deliverable. Do not add a persona, greeting, or process preamble.

Return:

- `offer fit`: product, audience, traffic source, and risk level.
- `compliance flags`: disclosures, claim risks, platform risks, and evidence gaps.
- `hook matrix`: 5 hooks in a table.
- `video briefs`: 2 concise UGC-style briefs.
- `carousel brief`: 4-slide structure.
- `platform plan`: posting path and link/disclosure handling.
- `cost risk`: low, medium, or high with reason.
- `test metrics`: day-3 and day-7 metrics.
- `kill criteria`: when to stop or rework.

## Guardrails

- Do not copy prompts, private workflows, landing-page claims, or creator-provided files from a source video.
- Do not claim guaranteed views, income, commissions, sales, ranking, or virality.
- Do not promise income, commissions, virality, ranking, or sales.
- Do not fabricate testimonials, personal product experience, before/after results, medical outcomes, or financial outcomes.
- Do not advise hiding affiliate disclosures.
- Do not tell users to bypass platform policies, moderation, account limits, or affiliate-network rules.
- For health, wellness, finance, legal, or regulated products, use cautious copy and require evidence review.
- For AI-generated actors, disclose or phrase as demonstration/content, not a real customer review.

## Reference

If source validation is needed, read `references/source-evidence.md`. It summarizes the public video/comment evidence behind this skill and the limits of the conversion.
