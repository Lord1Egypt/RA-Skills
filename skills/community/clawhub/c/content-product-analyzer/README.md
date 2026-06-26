# content-product-analyzer

A reusable Skill that turns raw content/product inputs into a structured commercial teardown:
audience, positioning, growth mechanics, monetization signals, credibility, sentiment,
and actionable “borrow vs avoid” recommendations.

## What it’s good at
- Product page / landing page teardowns
- Creator profile / post analysis (hooks, CTAs, engagement mechanics)
- Multi-link bundles (home + pricing + docs + reviews)
- Competitor comparison with a side-by-side matrix and a recommended wedge

## Inputs
- URLs (public)
- Screenshots (visible evidence only)
- Pasted text (copy, feature lists, pricing, reviews)

## Evidence modes
- **User-provided only**: no external lookup; only analyze what’s provided.
- **Mixed mode**: when public URLs are provided or freshness matters; verify and cite sources.

## Output
1) Structured summary (fields in Chinese)
2) Detailed teardown (long-form)
+ Optional competitor comparison add-on (when 2+ competitors)

## Safety / trust statement
- This skill is **instruction-only** (no executable scripts).
- It should **never** request secrets (API keys, cookies, tokens, wallets).
- Mixed-mode research (if used) should only access public URLs and cite sources.

## Quick start prompts
See `examples/`.

## License
MIT (see LICENSE)
