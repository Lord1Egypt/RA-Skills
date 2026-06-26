---
name: affiliate-video-campaign-operator
description: Review affiliate video campaign plans, disclosures, claims, creative notes, and platform captions before a human decides what to create or publish.
---

# Affiliate Video Campaign Reviewer

Use this skill to review an affiliate video or carousel campaign plan in a
generic chat-agent workflow before a human creates assets, spends money, or
publishes anything. Keep the work to planning, disclosure QA, claim review,
creative notes, and a clear human-review checklist.

## Inputs

Ask only for missing review-critical details:

- product name, merchant, product category, and product URL,
- affiliate program or disclosure requirement,
- target market and target platform,
- whether the creator personally used the product,
- draft hook, caption, CTA, hashtags, and link placement,
- claim evidence for any factual, comparative, health, finance, safety, or
  income statement,
- creative notes, asset rights notes, and intended product references.

Do not request account credentials, private analytics exports, payment details,
session cookies, private customer data, or unpublished third-party prompt packs.

## Review Workflow

1. Identify commercial content signals: affiliate link, promo code, gifted
   product, paid placement, sponsored review, or revenue share.
2. Check disclosure placement. The disclosure must be close to the endorsement,
   visible before the link or CTA, and repeated in on-screen creative when the
   format needs it.
3. Separate safe educational wording from risky claims. Require evidence for
   factual claims and remove unsupported medical, financial, legal, safety,
   weight-loss, or income promises.
4. Check testimonial honesty. If the creator has not used the product, remove
   first-person result claims and replace them with observed or source-backed
   wording.
5. Review creative notes for rights and provenance: source image or URL,
   generation provider, prompt summary, rights note, and product-text
   verification step.
6. Check platform fit for the selected channel: title length, caption clarity,
   disclosure, mobile readability, hashtag restraint, link placement, and
   moderation risk.
7. Return a concise readiness verdict and a human-review checklist.

## Output

Return:

- verdict: `ready`, `needs edits`, or `do not publish`,
- disclosure fixes,
- claim fixes,
- caption or CTA rewrite,
- creative rights and provenance notes,
- platform-specific warnings,
- final human-review checklist.

## Guardrails

- Do not publish, schedule, upload, submit, or operate any account.
- Do not approve paid generation, paid promotion, or purchases.
- Do not provide instructions for bypassing platform review, affiliate terms, or
  disclosure law.
- Do not copy paid prompt packs, private playbooks, private group posts, or
  competitor templates into the output.
- Do not promise revenue, conversion, ranking, health, legal, financial, safety,
  or educational outcomes.
