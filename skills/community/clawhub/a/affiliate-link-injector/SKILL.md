---
name: affiliate-link-injector
description: "Scan content for product mentions and auto-insert affiliate links with FTC compliance disclosures. Use when the user needs to monetize blog posts, product reviews, or guides with tracked affiliate links while maintaining legal compliance."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {
    "openclaw": {
      "requires": {
        "env": ["AFFILIATE_NETWORKS_API_KEY", "FTC_COMPLIANCE_MODE"],
        "bins": []
      },
      "os": ["macos", "linux", "win32"],
      "files": ["SKILL.md"],
      "emoji": "🔗"
    }
  }
---

## Overview

The **Affiliate Link Injector** automates the process of scanning content for product mentions and strategically inserting tracked affiliate links with FTC-compliant disclosure notices. This skill is designed for content creators, bloggers, ecommerce marketers, and agencies who need to monetize content while maintaining legal and ethical standards.

### Why This Matters

- **Revenue Automation**: Convert existing content into income streams without manual link hunting
- **FTC Compliance**: Automatically adds required disclosures (FTC Act Section 5) to protect your brand and audience
- **Link Tracking**: Integrates with Amazon Associates, ShareASale, Impact, CJ Affiliate, and custom affiliate networks
- **Content Preservation**: Maintains readability and SEO value while injecting contextual affiliate links
- **Multi-Platform Support**: Works with WordPress, Medium, Substack, Ghost, static HTML, and Markdown files

### Integrations

This skill connects with:
- **Amazon Associates** (product links, commission tracking)
- **ShareASale** (1000+ merchant networks)
- **Impact** (enterprise affiliate management)
- **CJ Affiliate** (B2B and B2C programs)
- **WordPress** (direct post/page injection via REST API)
- **Google Docs** (scan and suggest links for approval)
- **Slack** (send compliance reports and link suggestions)

---

## Quick Start

### Example 1: Scan Blog Post and Inject Amazon Links

```
Scan this blog post for product mentions and inject Amazon Associates 
affiliate links with FTC disclosures. Use my affiliate ID: 
yourname-20. Only link products that are actually available on Amazon.

[Paste your blog post content here]
```

**Expected Output**: Blog post with `[Product Name](https://amazon.com/...?tag=yourname-20)` links and a disclaimer like: *"This post contains affiliate links. We earn a commission if you click and purchase at no additional cost to you."*

---

### Example 2: Monetize Product Review with Multiple Networks

```
I have a product review comparing 5 laptop brands. Add affiliate links 
from Amazon Associates, B&H Photo, and Newegg. Insert FTC disclosure 
at the top. Format: Markdown. Only inject links where I naturally 
mention the product.

Review content:
[Paste your review]
```

**Expected Output**: Review with contextual affiliate links to each retailer, FTC disclosure banner, and a summary table showing which affiliate networks were used.

---

### Example 3: Bulk Scan WordPress Posts for Monetization Opportunities

```
Scan my WordPress blog for all product mentions across 10 recent posts. 
Generate a report showing:
1. Which products can be monetized (with affiliate network options)
2. Where to insert FTC disclosures
3. Recommended link anchor text for SEO
4. Compliance risk assessment

WordPress URL: https://myblog.com
API key: [your WordPress REST API key]
```

**Expected Output**: CSV report with post titles, product mentions, recommended affiliate networks, compliance notes, and a one-click approval button to auto-inject links.

---

### Example 4: Create FTC-Compliant Disclosure Variants

```
Generate 5 different FTC disclosure statements for my blog that are:
1. Concise (one sentence)
2. Friendly and conversational
3. Legal-safe (covers all affiliate relationships)
4. Mobile-friendly (short version for sidebars)
5. Transparent (mentions specific networks: Amazon, ShareASale)

My blog tone: [casual/professional/humorous]
```

**Expected Output**: 5 disclosure variants with guidance on placement and legal compliance notes.

---

## Capabilities

### 1. **Intelligent Product Detection**
- Scans content for product names, brands, and model numbers
- Uses NLP to distinguish between casual mentions and recommendation contexts
- Identifies products already linked (avoids duplicate linking)
- Recognizes variations: "MacBook Pro" = "MacBook Pro 16-inch M2"

### 2. **Affiliate Network Matching**
- Automatically matches products to available affiliate programs
- Prioritizes highest-commission networks
- Falls back to general retailers (Amazon) for unmatched products
- Supports custom affiliate URLs and UTM parameters
- Integrates with:
  - Amazon Associates (commission: 1-10%)
  - ShareASale (1000+ merchants)
  - Impact (enterprise tracking)
  - CJ Affiliate (B2B focus)
  - Custom affiliate networks (paste your own links)

### 3. **FTC Compliance Automation**
- Generates legally-reviewed disclosure statements
- Places disclosures prominently (top of post, before first link)
- Adds visual indicators: badges, icons, or inline notices
- Tracks which links have disclosures (audit trail)
- Generates compliance reports for legal review
- Supports multiple disclosure standards:
  - FTC Endorsement Guides (US)
  - AANA Code of Ethics (Australia)
  - ASA Guidelines (UK)
  - DGPR considerations (EU)

### 4. **Content-Aware Link Injection**
- Analyzes context to place links naturally (not spammy)
- Limits links per 1000 words (default: 3-5 links)
- Avoids linking competitor products negatively
- Preserves original anchor text or suggests better SEO variants
- Respects nofollow requirements for sponsored content

### 5. **Multi-Format Support**
- **Markdown**: Direct link injection with metadata
- **HTML**: Wraps links with data attributes for tracking
- **WordPress**: Injects via REST API with post scheduling
- **Google Docs**: Suggests links in comments for approval workflow
- **Substack**: Formats links for newsletter compatibility
- **Plain Text**: Generates separate link mapping file

### 6. **Reporting & Analytics**
- Generates monetization opportunity reports
- Shows estimated revenue per post
- Tracks link click-through rates (requires analytics integration)
- Compliance audit logs
- Competitor link analysis

---

## Configuration

### Required Environment Variables

```bash
# Affiliate Network Credentials
export AFFILIATE_NETWORKS_API_KEY="your_api_key_here"
export AMAZON_ASSOCIATES_ID="yourname-20"
export SHARESALE_MERCHANT_ID="your_merchant_id"

# FTC Compliance Settings
export FTC_COMPLIANCE_MODE="strict"  # strict, moderate, minimal
export DISCLOSURE_PLACEMENT="top"    # top, sidebar, inline, footer
export DISCLOSURE_LANGUAGE="en-US"   # en-US, en-GB, en-AU, de-DE, etc.

# Content Analysis
export LINK_DENSITY_MAX="5"          # Max links per 1000 words
export MIN_PRODUCT_RELEVANCE="0.75"  # 0-1 scale (1 = perfect match)
export AUTO_INJECT="false"           # true = inject, false = suggest only
```

### Setup Instructions

1. **Get API Keys**:
   - Amazon Associates: https://affiliate-program.amazon.com/
   - ShareASale: https://www.shareasale.com/
   - Impact: https://impact.com/
   - CJ Affiliate: https://www.cjaffiliates.com/

2. **Set Environment Variables**:
   ```bash
   export AFFILIATE_NETWORKS_API_KEY="your_key"
   export FTC_COMPLIANCE_MODE="strict"
   ```

3. **Connect Your Platform**:
   - **WordPress**: Generate REST API token at Settings → Users
   - **Google Docs**: Share document and authenticate with your Google account
   - **Slack**: Install bot and authorize channel access

4. **Test with Sample Content**:
   ```
   Run: affiliate-link-injector --test --mode=suggest
   Input: "I recommend the iPhone 14 Pro and iPad Air"
   Output: Suggested links with compliance check
   ```

---

## Example Outputs

### Output 1: Injected Blog Post (Markdown)

```markdown
# Best Budget Laptops in 2024

*Disclosure: This post contains affiliate links. We earn a commission 
if you click and purchase at no additional cost to you.*

## Budget Champion: ASUS VivoBook 15

The [ASUS VivoBook 15](https://amazon.com/s?k=ASUS+VivoBook+15&tag=yourname-20) 
offers excellent value at under $500. With a Ryzen 5 processor and 
16GB RAM, it handles everyday tasks effortlessly.

**Affiliate Networks Used**: Amazon Associates
**Commission Rate**: 4%
**Estimated Revenue Per Sale**: $20
```

### Output 2: Monetization Opportunity Report

```
AFFILIATE LINK INJECTOR REPORT
Generated: 2024-01-15

Post: "Top 10 Photography Gadgets"
Current Links: 2
Monetization Opportunities: 8 new products
Estimated Revenue Potential: $450-$800/month

Products Found:
✓ Canon EOS R6 → Amazon (10%), B&H Photo (8%)
✓ Nikon Z9 → Amazon (10%), Adorama (7%)
✓ Sony A7IV → Amazon (10%), Newegg (6%)
✓ DJI Air 3S → Amazon (5%), Best Buy (4%)
✓ Peak Design Backpack → Amazon (8%), REI (6%)

FTC Compliance Status: APPROVED
Disclosure Placement: Top of post
Risk Assessment: LOW (all links contextualized)
```

### Output 3: Compliance Audit Log

```
COMPLIANCE AUDIT TRAIL

Post ID: 42
Post Title: "Best Wireless Earbuds 2024"
Scan Date: 2024-01-15 10:30 UTC

Links Injected: 5
├─ AirPods Pro → Amazon (FTC disclosed: YES)
├─ Sony WF-1000XM5 → Amazon (FTC disclosed: YES)
├─ Jabra Elite 85t → ShareASale (FTC disclosed: YES)
├─ Bose QuietComfort → Amazon (FTC disclosed: YES)
└─ Anker Soundcore → Amazon (FTC disclosed: YES)

Disclosure Statement: Present
Disclosure Visibility: High (top of post)
Regulatory Compliance: ✓ FTC (US), ✓ ASA (UK), ✓ AANA (AU)
Risk Level: LOW
Recommended Review: None
```

---

## Tips & Best Practices

### 1. **Maximize Revenue Without Compromising Readers**
- Link only products you genuinely recommend (credibility = click-through)
- Use "Use when the user needs..." language in product descriptions
- Limit to 3-5 links per 1000 words (optimal for engagement)
- Test different disclosure placements (top vs. inline)

### 2. **Optimize for Search Engines**
- Use natural anchor text: "the [ASUS VivoBook 15](link)" not "click here"
- Keep affiliate URLs clean (remove tracking parameters that hurt SEO)
- Add product schema markup for rich snippets
- Interlink related posts to boost domain authority

### 3. **FTC Compliance Best Practices**
- Use "Disclosure" not "Disclaimer" (clearer for readers)
- Place disclosure BEFORE the first affiliate link
- Use clear language: "We earn a commission" not "We may earn a commission"
- Document your affiliate relationships in a separate page
- Review FTC updates quarterly (https://www.ftc.gov/endorsements)

### 4. **A/B Test Link Placement**
- Compare performance: top disclosure vs. inline notices
- Track which products generate highest CTR
- Test different link colors/styles (if using custom CSS)
- Monitor bounce rates to ensure links don't distract

### 5. **Maintain Reader Trust**
- Disclose ALL affiliate relationships (not just some)
- Link competitors fairly if you mention them
- Update links quarterly (broken links hurt credibility)
- Be transparent about commission rates (optional but builds trust)

### 6. **Integrate with Analytics**
- Use UTM parameters: `?utm_source=blog&utm_medium=affiliate&utm_campaign=post-title`
- Track conversions in Google Analytics or your affiliate dashboard
- Measure ROI per post to identify high-performing content
- Adjust link strategy based on performance data

---

## Safety & Guardrails

### What This Skill Will NOT Do

❌ **Will NOT inject links without compliance review**
- Requires explicit approval or "suggest only" mode by default
- Generates compliance reports for legal review before publishing

❌ **Will NOT link to competitors in negative contexts**
- Detects comparative language and avoids unfair linking
- Example: "Unlike the [Product X](link), our choice..." → Skips link

❌ **Will NOT exceed ethical link density**
- Hard limit: 5 links per 1000 words (configurable)
- Flags content as "over-monetized" if density exceeds threshold
- Prevents spammy affiliate content that harms reader experience

❌ **Will NOT link to prohibited categories**
- Respects your custom blocklist (weapons, adult content, etc.)
- Automatically filters based on FTC guidelines
- Prevents linking to competitors' affiliate programs

❌ **Will NOT work without explicit user content**
- Requires you to provide content (won't scrape web)
- Respects copyright and intellectual property
- Requires API authentication for WordPress/platform integrations

❌ **Will NOT guarantee affiliate program approval**
- Some networks (Amazon Associates) have strict policies
- Your account must be approved independently
- Skill generates compliant links but doesn't bypass network restrictions

### Limitations

- **Network Coverage**: ~500 affiliate networks supported; niche products may not have affiliate options
- **Language Support**: Optimized for English; other languages have reduced accuracy
- **Real-Time Updates**: Affiliate commission rates updated monthly (not real-time)
- **Link Verification**: Does not verify if products are currently in stock or available
- **Revenue Guarantees**: Estimated earnings are approximations based on average conversion rates

---

## Troubleshooting

### Issue 1: "No Affiliate Links Found for Product X"

**Cause**: Product not in supported affiliate networks

**Solutions**:
1. Check if the product has an affiliate program directly (contact brand)
2. Use a fallback network (Amazon Associates for most products)
3. Add a custom affiliate link manually
4. Adjust `MIN_PRODUCT_RELEVANCE` setting lower (0.5-0.7)

```bash
affiliate-link-injector --product="Obscure Product" --fallback=amazon
```

---

### Issue 2: "FTC Disclosure Not Appearing in Output"

**Cause**: Disclosure placement setting or content format incompatibility

**Solutions**:
1. Verify `DISCLOSURE_PLACEMENT` is set correctly:
   ```bash
   export DISCLOSURE_PLACEMENT="top"  # or "inline", "footer", "sidebar"
   ```

2. Check content format supports disclosure (HTML/Markdown required):
   ```
   affiliate-link-injector --format=markdown --disclosure=top
   ```

3. For WordPress, ensure theme supports custom HTML blocks

---

### Issue 3: "Links Injected But Analytics Not Tracking"

**Cause**: UTM parameters missing or affiliate network not configured

**Solutions**:
1. Verify affiliate network API key is active:
   ```bash
   affiliate-link-injector --test-api
   ```

2. Enable UTM parameter generation:
   ```bash
   export UTM_ENABLED="true"
   export UTM_SOURCE="blog"
   export UTM_MEDIUM="affiliate"
   ```

3. Check your affiliate dashboard for conversion tracking setup

---

### Issue 4: "Too Many Links Injected (Over-Monetized)"

**Cause**: Link density exceeds recommended threshold

**Solutions**:
1. Reduce `LINK_DENSITY_MAX`:
   ```bash
   export LINK_DENSITY_MAX="3"  # Changed from 5 to 3
   ```

2. Use "suggest only" mode to review before injecting:
   ```
   affiliate-link-injector --mode=suggest --review=true
   ```

3. Manually remove lower-priority links

---

### Issue 5: "WordPress Integration Not Working