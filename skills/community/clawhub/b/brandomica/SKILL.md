---
name: brandomica
description: Check brand name safety across domains, social handles, trademarks, app stores, and SaaS channels. Get availability scores, safety assessments, and filing readiness decisions.
version: 1.0.5
homepage: https://www.brandomica.com/mcp-server
metadata:
  openclaw:
    requires:
      bins:
        - npx
    emoji: "🔍"
    homepage: https://www.brandomica.com
    install:
      - kind: node
        package: brandomica-mcp-server
---

# Brandomica Lab — Brand Name Verification

You have access to the Brandomica MCP server for brand name safety checks. Use these tools to help users verify brand names before launching.

## Available Tools

- **brandomica_check_all** — Full brand check (domains, social, trademarks, app stores, SaaS + availability score + safety assessment). Use `mode: "quick"` for fast local-only checks, or `mode: "full"` for comprehensive results.
- **brandomica_assess_safety** — Quick safety risk decision (0-100 score, risk level, 6-signal breakdown). Start here for a fast go/no-go.
- **brandomica_filing_readiness** — Filing readiness summary (verdict, risk, top conflicts, confidence). Use after safety assessment shows medium/high risk.
- **brandomica_compare_brands** — Compare 2-5 brand name candidates side by side with recommendation.
- **brandomica_batch_check** — Check 2-50 names at once, sorted by score.
- **brandomica_brand_report** — Generate a timestamped evidence document (JSON).
- **brandomica_check_domains** — Domain availability + pricing for 6 TLDs.
- **brandomica_check_social** — Social handle availability (GitHub, Twitter, TikTok, LinkedIn, Instagram).
- **brandomica_check_trademarks** — USPTO + EUIPO trademark search.
- **brandomica_check_google** — Google Search presence (competitor overlap detection).
- **brandomica_check_appstores** — iOS App Store + Google Play search.
- **brandomica_check_saas** — Package registries (npm, PyPI, crates.io, etc.) + SaaS channels.

## Recommended Workflow

1. Start with `brandomica_assess_safety` for a quick risk decision
2. If medium/high risk, run `brandomica_filing_readiness` for filing details
3. Use `brandomica_check_all` for full evidence across all channels
4. Compare candidates with `brandomica_compare_brands`

## Brand Name Format

Brand names must be lowercase alphanumeric (hyphens allowed). The tools will reject invalid characters.

## Automation Ideas

- **Brainstorm + validate loop**: Generate name ideas, then batch-check them all with `brandomica_batch_check`
- **Domain shopping**: Use `brandomica_check_domains` to find available domains with pricing
- **Trademark clearance**: Run `brandomica_filing_readiness` before any trademark filing
- **Competitive analysis**: Use `brandomica_check_google` to see who else uses a similar name
