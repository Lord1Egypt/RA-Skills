---
name: seo-audit-pro
description: Crawl any website and get a 0-100 SEO score with 50+ checks across Technical, On-Page, Schema, Social, and Compliance categories. Identifies quick wins, competitor gaps, and generates AI-written SEO articles. Industry-specific compliance checks for mortgage, real estate, medical, and legal.
version: 1.0.1
author: drivenautoplex1
price: 0
tags:
  - seo
  - marketing
  - real-estate
  - mortgage
  - crypto
  - saas
  - healthcare
  - legal
  - e-commerce
  - coaching
  - content
  - analytics
  - compliance
  - competitor-analysis
metadata:
  openclaw:
    requires:
      env:
        - ANTHROPIC_API_KEY
      anyBins:
        - python3
    primaryEnv: ANTHROPIC_API_KEY
    emoji: "🔍"
    homepage: https://github.com/drivenautoplex1/openclaw-skills
    install:
      - kind: uv
        package: requests
        bins: []
      - kind: uv
        package: beautifulsoup4
        bins: []
      - kind: uv
        package: anthropic
        bins: []
---

# SEO Audit Skill

Run a full SEO audit on any website in seconds. Get a 0-100 score, 50+ individual checks, industry compliance flags, and a prioritized fix list — no agency required.

## Free vs Premium

**Free tier (no API key needed):**
- `--demo` — full audit output on a built-in static sample, zero network calls, see exactly what the output looks like
- `--compliance-only <url>` — fast HTTP fetch + forbidden word/MLO compliance scan, no AI analysis
- `--version` — print version

**Premium tier (ANTHROPIC_API_KEY):**
- Full 50+ check crawl + AI analysis (Claude Haiku, ~$0.003/audit)
- `--competitor` — side-by-side gap analysis against a competitor URL
- `--generate-article` — AI-written 800-word SEO article with H1/H2/FAQ schema, ~$0.003/article
- `--format=json` — pipe results into agent workflows or dashboards
- Industry-specific scoring modes: `--industry=mortgage`, `--industry=medical`, `--industry=legal`

The free compliance scan catches NMLS violations, missing disclosures, and forbidden words before they cost you — worth installing on that alone.

## What this skill does

Crawls a URL and runs 50+ checks across 5 categories. Returns a weighted 0-100 score, per-check PASS/FAIL/WARN results, and a ranked fix list ordered by score impact.

### Check categories

| Category | Checks | Industry weight |
|---|---|---|
| Technical | HTTPS, robots.txt, sitemap, page speed signals, canonical, mobile | All |
| On-Page | Title (length, keyword), meta description, H1/H2 hierarchy, image alt, word count | All |
| Schema | LocalBusiness, FAQ, BreadcrumbList, Review markup | Real estate, medical, legal |
| Social | OG tags, Twitter card, description, image | All |
| Compliance | NMLS number, phone, address, disclosures, CTA count | Mortgage, medical, legal |

**Scoring:** Weight-based (not binary pass/fail count). Critical checks (NMLS, HTTPS, H1) weight 3×. Minor checks weight 1×. Score = pass_weight / total_weight × 100.

## Input contract

Tell me:
1. **URL to audit** — the page you want scored
2. **Target keyword** (optional) — for on-page keyword density check
3. **Industry** (optional): mortgage / real-estate / crypto / saas / healthcare / legal / general
4. **Competitor URL** (optional) — for gap analysis

Example prompts:
- "Audit https://example.com for 'mortgage broker [city]'"
- "Audit https://example.com --competitor https://rocket.com"
- "Check https://example.com compliance only"
- "Generate an article for 'first time home buyer [city]'"

## Output contract

**Standard audit output:**
```
SEO Audit — https://example.com
Score: 74/100  |  Industry: Mortgage  |  Keyword: "mortgage broker [city]"

TECHNICAL (8/10)
  ✓ HTTPS enforced
  ✓ robots.txt found
  ✓ sitemap.xml found
  ⚠ No canonical tag — add <link rel="canonical"> to prevent duplicate content
  ✗ Missing mobile viewport meta

ON-PAGE (6/10)
  ✓ Title: 52 chars, keyword present
  ✗ Meta description: 210 chars (too long, truncates at 160)
  ✓ H1 present: "[City] Mortgage Broker — Get Pre-Approved Today"
  ⚠ Only 380 words — thin content, target 800+
  ✗ 4 images missing alt text

SCHEMA (3/10)
  ✗ No LocalBusiness schema — quick win, adds map pack eligibility
  ✗ No FAQ schema — competitors using this get 2× SERP real estate
  ✗ No Review schema

SOCIAL (9/10)
  ✓ OG title, description, image all present
  ✓ Twitter card configured

COMPLIANCE (10/10)  [Mortgage]
  ✓ NMLS number visible
  ✓ Phone number present
  ✓ Physical address in footer
  ✓ No forbidden words detected

TOP 3 QUICK WINS (ranked by score impact):
  1. Add LocalBusiness + FAQ schema  (+8 pts estimated)
  2. Expand content to 800+ words    (+6 pts estimated)
  3. Fix meta description length     (+4 pts estimated)
```

**Competitor gap analysis** (with `--competitor`):
```
GAP ANALYSIS — Your Site vs competitor.com

Your site WINS: NMLS compliance, OG tags, sitemap
Competitor WINS: FAQ schema, 2,400-word content, 3 review schema blocks

Top gaps to close:
  1. FAQ schema — competitor has 8 FAQ pairs, you have 0
  2. Content depth — competitor 2,400 words vs your 380
  3. Review schema — competitor shows star rating in SERP, you don't
```

**Article generation** (with `--generate-article`):
```
[800-word article with H1/H2 structure, FAQ section, target keyword density 1-2%]
Ready to paste into CMS. Estimated read time: 4 min.
```

## How the skill works

Uses `seo_audit_skill.py` (in this directory). Makes HTTP requests with BeautifulSoup for crawling, Claude Haiku for AI analysis.

```bash
# Full audit
python3 seo_audit_skill.py --url https://example.com --keyword "mortgage broker [city]"

# Demo mode (no network, no API — see the output format)
python3 seo_audit_skill.py --demo

# Compliance scan only (free, HTTP fetch only)
python3 seo_audit_skill.py --compliance-only --url https://example.com --industry=mortgage

# Competitor gap analysis
python3 seo_audit_skill.py --url https://yoursite.com --competitor https://competitor.com

# Generate SEO article (premium)
python3 seo_audit_skill.py --generate-article "first time home buyer [city]" --output article.md

# JSON output (for pipelines)
python3 seo_audit_skill.py --url https://example.com --format=json | jq '.score'

# Industry-specific compliance
python3 seo_audit_skill.py --url https://medicalsite.com --industry=healthcare

# Version
python3 seo_audit_skill.py --version
```

## Industry compliance modes

| Industry | Extra checks |
|---|---|
| mortgage | NMLS number, rate disclosure, APR presence, "pre-approval" forbidden |
| real-estate | License number, fair housing logo, MLS disclaimer |
| healthcare | HIPAA disclaimer, no diagnosis claims, credential display |
| legal | Bar number, jurisdiction disclosure, no outcome guarantees |
| general | Standard checks only |

## Why weight-based scoring

A missing NMLS number is not equal to a missing favicon. Weight-based scoring reflects real SEO impact:
- Critical (weight 3): HTTPS, NMLS/license number, H1, sitemap
- Moderate (weight 2): Meta description, canonical, mobile viewport, schema
- Minor (weight 1): OG tags, alt text on individual images, word count

A site with perfect compliance + schema but missing HTTPS scores lower than a site with HTTPS + good on-page but weak social.

## Competitor intelligence note

Large mortgage sites (Rocket, LoanDepot, NerdWallet) use Cloudflare WAFs and will 403 bot requests. The audit reports the 403 as a FAIL on HTTPS-accessible content — which is honest. For auditing your own site, no issue. For competitor research on large players, use `--format=json` to capture what passes before the block.

Real finding: NerdWallet scores ~70/100 on this audit — they fail schema markup entirely and have a 22-char title. Their SEO advantage is domain authority (backlinks), not on-page quality. This gap is closeable for smaller operators who nail technical + schema.

## Integration with agent infrastructure

```bash
# Via Telegram
@openclaw seo-audit "Audit https://example.com for '[city] mortgage'"
@openclaw seo-audit "Compare https://mysite.com vs https://competitor.com"

# Via Claude Code
openclaw run seo-audit "Audit https://example.com"

# In agent pipelines (JSON mode)
python3 seo_audit_skill.py --url https://example.com --format=json | jq '.score, .quick_wins'
```
