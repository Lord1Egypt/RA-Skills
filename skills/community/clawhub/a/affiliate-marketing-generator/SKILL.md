# Affiliate Marketing Content Generator

**Version:** 1.0.0  
**Author:** max_0x1  
**Category:** Marketing / Affiliate Marketing  
**License:** MIT-0  
**Tags:** affiliate marketing, product review, comparison post, email sequence, content monetization

---

## Overview

Generates a complete affiliate marketing content system for any product or niche. Turns your affiliate links into high-converting reviews, comparison posts, email sequences, and social content — without writing from scratch.

Four prompts cover the highest-converting affiliate content formats:
1. **Product Review Post** — SEO-optimized long-form affiliate review (1,200-1,800 words)
2. **Comparison Post (vs Alternatives)** — "X vs Y vs Z" format with feature matrix and use-case routing
3. **Email Affiliate Sequence** — 5-email warm-list promotion sequence with disclosure language
4. **Social + YouTube Pre-Roll Script** — Short-form content across Instagram, TikTok, YouTube, Twitter/X

---

## Prompts

### 1. `affiliate-review`
**Purpose:** Generate a full SEO-optimized affiliate product review post.

**Input variables:**
- `[PRODUCT_NAME]` — Name of the affiliate product
- `[PRODUCT_CATEGORY]` — Type of product (e.g., "email marketing tool", "standing desk", "online course platform")
- `[TARGET_AUDIENCE]` — Who you're writing for (e.g., "freelance writers", "home office workers", "online coaches")
- `[KEY_FEATURES]` — 3-5 main features or differentiators to highlight
- `[AFFILIATE_DISCLOSURE]` — Your disclosure language (e.g., "This post contains affiliate links. I earn a commission at no cost to you.")
- `[PRICE_POINT]` — Pricing tier (e.g., "$15/month", "$299 one-time")
- `[ALTERNATIVES]` — 2 competing products to compare against

**Output:** 1,200-1,800 word review post with hook, product overview, pros/cons table, comparison section, FAQ (5 questions), and affiliate CTA with disclosure.

---

### 2. `comparison-post`
**Purpose:** Generate a "Product A vs Product B vs Product C" comparison post — the highest-converting affiliate format.

**Input variables:**
- `[PRODUCT_A]` — Primary affiliate product (the one you earn most from)
- `[PRODUCT_B]` — Second option
- `[PRODUCT_C]` — Third option (budget or enterprise alternative)
- `[CATEGORY]` — Product category (e.g., "project management software")
- `[TARGET_AUDIENCE]` — Reader profile
- `[USE_CASES]` — 3 distinct buyer scenarios (e.g., "solo freelancer", "5-person agency", "enterprise team")
- `[AFFILIATE_LINKS_AVAILABLE]` — Which products have affiliate programs

**Output:** 1,500-2,000 word comparison post with feature matrix table, use-case routing guide ("If you need X, get Y"), price-per-value analysis, and affiliate CTAs for each option with disclosure.

---

### 3. `email-affiliate-sequence`
**Purpose:** Generate a 5-email sequence to promote an affiliate product to a warm email list.

**Input variables:**
- `[PRODUCT_NAME]` — Affiliate product to promote
- `[LIST_NICHE]` — Your audience's primary interest (e.g., "productivity for remote workers")
- `[YOUR_NAME]` — Sender name
- `[PRODUCT_BENEFIT]` — Single biggest benefit (e.g., "cuts meeting time by 40%")
- `[PRICE_AND_OFFER]` — Pricing + any bonus or deadline (e.g., "$49/month, 20% discount through Friday")
- `[YOUR_BONUS]` — Bonus you're offering for buying through your link (e.g., "free 30-min onboarding call")
- `[AFFILIATE_DISCLOSURE]` — Your disclosure language

**Output:** 5 emails — Day 1 (teaser), Day 2 (story-based proof), Day 4 (objection handler), Day 6 (urgency + bonus stack), Day 7 (final deadline). Each email includes subject line, preview text, body copy, and affiliate CTA with disclosure baked in.

---

### 4. `social-affiliate-scripts`
**Purpose:** Generate short-form affiliate promotional content for social media and YouTube.

**Input variables:**
- `[PRODUCT_NAME]` — Affiliate product
- `[TARGET_PLATFORM]` — Primary platform (or "all" for full kit)
- `[HOOK_ANGLE]` — Main hook (e.g., "I tried this for 30 days", "The tool that replaced 3 apps for me")
- `[TARGET_AUDIENCE]` — Who will see this content
- `[KEY_PROOF_POINT]` — One specific result or feature to lead with
- `[AFFILIATE_DISCLOSURE]` — Platform-appropriate disclosure (e.g., "#ad" for Instagram)

**Output:** Instagram Reel script (60 sec, hook + demo + CTA), TikTok script (30 sec, pattern interrupt + proof + CTA), YouTube 30-second pre-roll ad script (skip-proof hook in first 5 sec), Twitter/X thread (5 tweets, native feel). Each includes platform-appropriate disclosure.

---

## Example Usage

See `examples/convertkit-review.md` for a complete worked example:
- Affiliate review of ConvertKit targeting freelance writers
- 3-way comparison: ConvertKit vs Mailchimp vs Beehiiv
- 5-email launch sequence
- Full social kit (Reel + TikTok + pre-roll + X thread)

---

## Tips for Best Results

1. **Be specific about your audience** — "freelance writers who blog about personal finance" outperforms "writers"
2. **Use real proof points** — actual conversion rates, specific feature names, real pricing tiers
3. **Lead with problems, not products** — the best affiliate content solves a reader's problem and mentions the product as the solution
4. **Always include disclosure** — FTC requires it; it also builds trust
5. **Stack the comparison** — put your highest-earning affiliate as Product A in the comparison post
