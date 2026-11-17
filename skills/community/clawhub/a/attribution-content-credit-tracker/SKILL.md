---
name: Track Content Attribution & Creator Credits Automatically
description: "Monitor and track unauthorized content republication across the web. Generates cease-and-desist letters, manages canonical tags, and maintains attribution records. Use when the user needs content protection, copyright enforcement, or citation management."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {"openclaw":{"requires":{"env":["GOOGLE_CUSTOM_SEARCH_API_KEY","GOOGLE_CUSTOM_SEARCH_ENGINE_ID","COPYSCAPE_API_KEY","DMCA_TEMPLATE_VAULT","SLACK_WEBHOOK_URL"],"bins":["curl","jq"]},"os":["macos","linux","win32"],"files":["SKILL.md"],"emoji":"⚖️"}}
---

# Attribution & Content Credit Tracker

## Overview

The **Attribution & Content Credit Tracker** is an automated compliance and rights management system that protects your intellectual property by monitoring unauthorized content republication across the web. This skill continuously scans for instances where your articles, research, graphics, datasets, and original ideas are republished, quoted, or referenced without proper attribution—then takes action.

### What Makes This Valuable

Content creators, publishers, and data organizations lose millions in lost attribution and citation value annually. Google Search favoids canonical tracking, SEO credit flows to republishers instead of original authors, and serious copyright violations go undetected. This skill automates the entire lifecycle:

1. **Detection** — Scans the web for duplicated/quoted content using Google Custom Search, Copyscape API, and semantic similarity analysis
2. **Classification** — Distinguishes between legitimate citations, fair use excerpts, and serious violations
3. **Enforcement** — Generates legal notices (DMCA takedowns, cease-and-desist letters) with customizable templates
4. **Recovery** — Automatically injects `rel=canonical` tags to authoritative sources and manages public "As Seen In" galleries
5. **Reporting** — Tracks patterns, maintains audit trails, and exports compliance reports for legal/marketing teams

**Integrations:** WordPress (canonical injection), Slack (violation alerts), Google Search Console (canonical verification), DMCA.com (legal filing), HubSpot (content attribution), Zapier (workflow automation).

---

## Quick Start

Try these example prompts immediately:

### Example 1: Scan for Content Theft
```
Track unauthorized republication of my article "The Complete Guide to API Rate Limiting" 
published on www.example.com/articles/api-rate-limiting. Search across blogs, 
Medium, dev.to, LinkedIn, and news aggregators. Flag any instances with >80% 
text similarity and no attribution link.
```

### Example 2: Generate Cease-and-Desist Letter
```
Create a cease-and-desist letter for the website thievedblog.net that republished 
our research report "2024 Remote Work Trends" without permission or attribution. 
Include legal references for copyright violations and demand removal within 14 days. 
Use professional tone suitable for legal counsel review.
```

### Example 3: Build 'As Seen In' Gallery
```
Generate an automated "As Seen In" gallery page (HTML/Markdown) from all verified 
citations of our content across TechCrunch, Forbes, HackerNews, and industry publications. 
Include publication logos, article titles, publication dates, and backlink URLs. 
Exclude unverified sources and spam sites. Update weekly.
```

### Example 4: Canonical Tag Audit
```
Scan our top 50 published articles and inject rel=canonical tags pointing to 
our authoritative source URLs. Generate a WordPress bulk edit CSV file and 
report any existing canonical conflicts. Prioritize articles with high 
syndication detected.
```

### Example 5: Monthly Attribution Report
```
Produce a compliance report showing: (1) all detected unauthorized republications 
this month, (2) citation breakdown by domain/publication, (3) estimated SEO value 
lost, (4) enforcement actions taken, (5) compliance rate trends. Format as 
PowerPoint slides ready for stakeholder review.
```

---

## Capabilities

### 1. **Proactive Content Scanning**
- **Semantic Duplicate Detection** — Uses vector-based similarity (Copyscape API, Google Custom Search) to find near-exact duplicates, paraphrased content, and quote farming
- **Multi-Source Coverage** — Monitors blogs, news sites, Medium, dev.to, LinkedIn, Twitter/X, Reddit, YouTube descriptions, podcasts, and more
- **Customizable Sensitivity** — Set thresholds (70%, 85%, 95% similarity) based on content type
- **Scheduled Scans** — Run hourly, daily, or weekly automatic checks on your content inventory
- **Historical Tracking** — Maintains 12-month audit trail of first detection, republication patterns, and enforcement history

**Usage Example:**
```
Monitor my content library (50+ published articles) for unauthorized 
republication. Run scans every 7 days. Alert me only for high-confidence 
matches (>85% similarity) with external backlinks. Track trends over time.
```

### 2. **Intelligent Classification Engine**
- **Attribution Detection** — Identifies if republished content includes proper credit/backlinks
- **Fair Use Assessment** — Distinguishes legitimate excerpts (with citation) from copyright violations
- **Source Ranking** — Prioritizes violations by severity, domain authority, and potential damage
- **False Positive Filtering** — Excludes your own syndicated content, aggregator feeds, and licensed republishers

### 3. **Legal Enforcement Automation**
- **DMCA Notice Generation** — Creates legally-compliant takedown notices using certified templates
- **Cease-and-Desist Letters** — Professional legal documents (customizable per jurisdiction: US, EU, UK)
- **Demand Letters** — Formal requests for attribution correction or content removal
- **Legal Template Vault** — Access 40+ pre-vetted templates for copyright, trademark, and IP violations
- **E-signature Integration** — Auto-route generated letters through DocuSign or HelloSign for signing

**Sample Output (Cease-and-Desist):**
```
TO: [violator domain owner]
RE: Unauthorized Republication of Copyrighted Content

This letter serves as formal notice that your website [domain] has 
republished copyrighted material authored by [your company] without 
authorization or attribution.

INFRINGING CONTENT:
- Original: [URL] (Published: [date])
- Reproduction: [infringing URL] (Published: [date])
- Similarity: 94%
- Current Status: Live (no attribution/backlink)

DEMAND: Remove content within 14 calendar days or face legal action 
including DMCA filing, damages claim, and attorney fees.

[Legal signature block, jurisdiction, remedies]
```

### 4. **Canonical Tag Management**
- **Automatic Injection** — Add `<link rel="canonical" href="your-authoritative-url">` to source documents via WordPress API, direct server access, or generated CSV
- **Conflict Resolution** — Detect and fix canonical conflicts (multiple sources claiming authority)
- **Verification Dashboard** — Confirm canonical tags are live and Google Search Console recognizes them
- **Syndication Coordination** — Manage canonical tags for legitimate content syndication (Medium, Dev.to, etc.)
- **SEO Credit Recovery** — Monitor Google Search Console to verify SEO credit flows to authoritative source

### 5. **As Seen In Gallery & Badge System**
- **Auto-Generated Gallery Page** — Creates beautiful HTML/Markdown showcasing all verified citations
- **Logo Integration** — Automatically pulls publication logos and favicons
- **Responsive Design** — Mobile-friendly gallery with filtering (by date, publication, content type)
- **Embeddable Widget** — JavaScript snippet for your website footer/sidebar (auto-updates weekly)
- **Social Proof Link Builder** — Formats citations for LinkedIn, Twitter, and marketing materials

**Sample Gallery Entry:**
```
📰 "API Rate Limiting Strategies" mentioned in TechCrunch
Publication: TechCrunch | Date: March 15, 2024 | Domain Authority: 92
Citation: "According to a comprehensive guide on rate limiting..."
[View Article] [Claim Credit] [Share]
```

### 6. **Violation Analytics & Reporting**
- **Monthly Compliance Reports** — PPT/PDF with violation trends, enforcement results, and attribution gaps
- **Revenue Attribution** — Estimate lost SEO value, traffic, and lead value from unattributed republications
- **Enforcement Metrics** — Track cease-and-desist response rates, content removal rates, and remediation timelines
- **Competitive Benchmark** — Compare your citation patterns vs. competitors
- **Auditor-Ready Exports** — Generate compliance documentation for legal teams, tax, and IP audits

---

## Configuration

### Required Environment Variables
```bash
# Google Custom Search API
export GOOGLE_CUSTOM_SEARCH_API_KEY="AIzaSy..."
export GOOGLE_CUSTOM_SEARCH_ENGINE_ID="cx:your-engine-id"

# Copyscape Plagiarism Detection API
export COPYSCAPE_API_KEY="your-copyscape-token"
export COPYSCAPE_USER_ID="username"

# Legal Template Access
export DMCA_TEMPLATE_VAULT="https://your-vault.example.com/dmca-templates"
export LEGAL_TEMPLATE_KEY="your-auth-token"

# Notifications
export SLACK_WEBHOOK_URL="REDACTED-SECRET"

# Optional: E-signature services
export DOCUSIGN_API_KEY="your-docusign-key"
export DOCUSIGN_ACCOUNT_ID="account-id"

# Optional: WordPress integration
export WORDPRESS_SITE_URL="https://yourblog.com"
export WORDPRESS_API_TOKEN="your-wp-token"
```

### Setup Instructions

1. **Register APIs:**
   - Google Custom Search: https://programmablesearchengine.google.com/
   - Copyscape: https://www.copyscape.com/api/
   - DMCA.com: Register for legal filing access

2. **Configure Content Library:**
   ```bash
   # Create inventory of your published content
   skill configure --add-content-urls="urls.csv" \
     --source="WordPress|Medium|Manual" \
     --categories="blog,research,guides"
   ```

3. **Set Scan Frequency:**
   ```bash
   skill configure --scan-schedule="weekly" \
     --similarity-threshold=85 \
     --alert-channels="slack,email"
   ```

4. **Initialize Canonical Management:**
   ```bash
   skill configure --enable-canonical-auto-inject \
     --wordpress-api-key="your-token" \
     --verify-with-gsc
   ```

---

## Example Outputs

### Output 1: Violation Detection Report
```json
{
  "scan_date": "2024-01-15",
  "content_scanned": 47,
  "violations_found": 12,
  "critical": 3,
  "violations": [
    {
      "original_url": "example.com/article/api-rate-limiting",
      "original_published": "2023-10-20",
      "reproduced_url": "copycat-blog.com/posts/rate-limiting-guide",
      "reproduced_date": "2023-11-02",
      "similarity": "94%",
      "has_attribution": false,
      "has_backlink": false,
      "domain_authority": 24,
      "estimated_traffic_loss": "~340 monthly visits",
      "severity": "HIGH",
      "recommended_action": "DMCA_NOTICE",
      "legal_template_id": "dmca-copyright-2024"
    }
  ]
}
```

### Output 2: Generated Cease-and-Desist (Plain Text)
```
[COMPANY LETTERHEAD]

January 15, 2024

VIA EMAIL & REGISTERED MAIL

To Whom It May Concern:
Re: Cease and Desist Notice – Unauthorized Republication of Copyrighted Material

This firm represents [Your Company], owner of copyrighted content published 
at example.com. We have discovered that your website (copycat-blog.com) 
has republished our protected work without authorization, attribution, or license.

INFRINGING WORK:
Title: "The Complete Guide to API Rate Limiting"
Original URL: example.com/article/api-rate-limiting
Original Publication Date: October 20, 2023
Copyright Registration: [if applicable]

INFRINGING REPRODUCTION:
Unauthorized URL: copycat-blog.com/posts/rate-limiting-guide
Publication Date: November 2, 2023
Similarity Match: 94% (verified via Copyscape)
Current Status: LIVE with zero attribution or backlink

LEGAL BASIS:
This reproduction violates the Copyright Act (17 U.S.C. § 102 et seq.) 
and constitutes copyright infringement, tortious interference, and 
unjust enrichment.

DEMAND:
You must immediately:
1. REMOVE the infringing content from your website and all platforms
2. REMOVE all cached and archived versions
3. CEASE all future republication of our copyrighted material
4. PROVIDE written confirmation of compliance within 14 calendar days

FAILURE TO COMPLY will result in:
- DMCA takedown notice filing
- Legal action for damages (actual + statutory damages up to $150,000/work)
- Attorney fees and court costs
- Injunctive relief to prevent future infringement

Sincerely,
[Your Legal Counsel]
[Firm Name & Contact]
```

### Output 3: As Seen In Gallery (HTML)
```html
<section class="as-seen-in-gallery">
  <h2>Featured In</h2>
  <div class="publications-grid">
    <article class="publication-card">
      <img src="techcrunch-logo.png" alt="TechCrunch">
      <h3>TechCrunch</h3>
      <p class="citation">Mentioned in: "2024 API Trends Report"</p>
      <p class="date">March 10, 2024</p>
      <a href="https://techcrunch.com/..." class="read-link">Read Article →</a>
    </article>
    <article class="publication-card">
      <img src="forbes-logo.png" alt="Forbes">
      <h3>Forbes</h3>
      <p class="citation">Featured in: "The Future of Cloud Architecture"</p>
      <p class="date">February 28, 2024</p>
      <a href="https://forbes.com/..." class="read-link">Read Article →</a>
    </article>
  </div>
</section>
```

### Output 4: Monthly Compliance Report (PDF Summary)
```
ATTRIBUTION & COMPLIANCE REPORT
Period: January 1–31, 2024

📊 EXECUTIVE SUMMARY
• Content Scanned: 47 articles
• Violations Detected: 12 (↑ 3 from December)
• High-Priority Cases: 3
• Enforcement Actions: 2 cease-and-desist letters sent
• Removal Success Rate: 67% (2 of 3 responded)

⚠️ CRITICAL VIOLATIONS
1. copycat-blog.com — 94% match, no attribution, 340 monthly visits lost
   Action: DMCA notice sent Jan 8 | Status: Awaiting response
2. content-farm.net — 91% match, paraphrased, high DA domain
   Action: Cease-and-desist sent Jan 12 | Status: Content removed Jan 14 ✓
3. syndication-blog.io — 88% match, legitimate but missing backlink
   Action: Attribution request sent Jan 15 | Status: Pending

📈 METRICS
• Estimated Traffic Loss: 1,247 monthly visits (~$12K opportunity cost)
• Canonical Tags Verified: 45/47 live and working
• SEO Credit Recovery: 89% attributed to authoritative source
• Citation Accuracy: 94% (up from 91% last month)

📋 ACTIONS TAKEN
✓ Injected canonical tags on 2 new articles
✓ Updated "As Seen In" gallery (42 verified publications)
✓ Filed 1 DMCA notice with DMCA.com
✓ Sent 2 cease-and-desist letters
✓ Verified 15 legitimate syndication partnerships

NEXT MONTH PRIORITIES
1. Follow up on 1 pending cease-and-desist response
2. Expand monitoring to podcast transcripts and YouTube
3. Implement automated attribution monitoring via API integration
```

---

## Tips & Best Practices

### 1. **Prioritize High-Impact Violations**
- Focus enforcement efforts on high-DA domains and high-traffic violations
- Don't waste resources on small spam sites