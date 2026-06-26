---
name: competitor-spy-tool
description: "Monitor competitor websites for pricing changes, new content, and keyword movements. Use when the user needs competitive intelligence, market tracking, or SEO monitoring across multiple domains."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {"openclaw":{"requires":{"env":["COMPETITOR_DOMAINS","SERP_API_KEY","SLACK_WEBHOOK_URL"],"bins":["curl","grep"]},"os":["macos","linux","win32"],"files":["SKILL.md"],"emoji":"🕵️"}}
---

# Competitor Spy Tool

## Overview

The Competitor Spy Tool automates continuous monitoring of competitor websites, pricing structures, content updates, and search engine rankings. This skill integrates with **SerpAPI** for SERP tracking, **web_search** for content discovery, **Slack** for real-time alerts, and **Google Sheets** for historical data logging. 

**Why it matters:** Competitive intelligence is mission-critical. Manual monitoring across 5+ competitors is time-consuming and error-prone. This tool eliminates guesswork by automating daily scans, flagging price changes within 24 hours, tracking new blog posts, and monitoring keyword position shifts—enabling you to react faster than competitors.

**Perfect for:** SaaS founders, e-commerce managers, digital agencies, content strategists, and growth teams who need to stay ahead of market movements.

---

## Quick Start

Try these prompts immediately:

```
Monitor these 3 competitors for pricing changes daily:
- competitor1.com
- competitor2.com
- competitor3.com

Alert me via Slack when prices drop by 10%+ or new products launch.
```

```
Track keyword rankings for "AI email marketing" across my competitors.
Show me which competitor owns positions 1-3 and what changed since yesterday.
```

```
Scan competitor blog feeds for new content published in the last 24 hours.
Flag posts about pricing, features, or product launches. Send summary to Slack.
```

```
Create a weekly competitive analysis report:
- Pricing changes detected
- New landing pages launched
- Top-performing keywords they're targeting
- Content gaps I can exploit
```

```
Monitor competitor email signup flows and landing page copy changes.
Screenshot key pages and store versions for comparison over time.
```

---

## Capabilities

### 1. **Pricing Monitoring**
Automatically scrapes and tracks competitor pricing pages, detects changes, and calculates percentage deltas. Stores historical pricing data in a spreadsheet for trend analysis.

**Example usage:**
```
Track pricing for:
- SaaS plans (Starter, Pro, Enterprise tiers)
- Add-on features and overage costs
- Discount codes and promotional pricing

Alert threshold: 5% change triggers notification
```

### 2. **Content Discovery & Tracking**
Monitors RSS feeds, blog indexes, and sitemap updates to detect new content within hours. Categorizes posts by topic (pricing, features, case studies, thought leadership) and extracts key metadata.

**Example usage:**
```
Monitor competitor blog feeds for:
- New blog posts (title, URL, publication date)
- Product announcements
- Case studies and testimonials
- Webinar/event announcements
```

### 3. **Keyword Position Tracking**
Uses SerpAPI to track your competitors' keyword rankings across 50+ target keywords. Shows position changes, search volume, and estimated traffic for each keyword.

**Example usage:**
```
Track these keywords across competitors:
- "AI email marketing platform"
- "email automation software"
- "marketing automation ROI"

Show daily position changes and traffic estimates
```

### 4. **Landing Page Monitoring**
Captures screenshots and stores HTML snapshots of competitor landing pages. Detects copy changes, CTA button text modifications, headline shifts, and visual redesigns.

**Example usage:**
```
Monitor landing page changes:
- Homepage headlines and value propositions
- Pricing page copy and CTA buttons
- Feature comparison tables
- Trust signals (testimonials, logos, certifications)
```

### 5. **Competitive Intelligence Reporting**
Generates weekly/monthly reports with:
- Pricing trend analysis
- Content volume and topic distribution
- Keyword ranking movements
- Market share signals
- Actionable gaps and opportunities

---

## Configuration

### Required Environment Variables

```bash
# API Keys & Webhooks
export COMPETITOR_DOMAINS="competitor1.com,competitor2.com,competitor3.com"
export SERP_API_KEY="your_serpapi_key_here"
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
export GOOGLE_SHEETS_API_KEY="your_google_api_key"
export GOOGLE_SHEET_ID="your_sheet_id"

# Optional: For advanced features
export BROWSERLESS_API_KEY="your_browserless_key"
export MAILGUN_API_KEY="for_email_alerts"
```

### Setup Instructions

1. **Get API Keys:**
   - SerpAPI: Sign up at [serpapi.com](https://serpapi.com), create API key
   - Slack: Create webhook at api.slack.com/apps
   - Google Sheets: Enable API in Google Cloud Console

2. **Add Competitor Domains:**
   ```bash
   # Create config file
   cat > competitor_config.json << EOF
   {
     "competitors": [
       {
         "name": "Competitor A",
         "domain": "competitor-a.com",
         "pricing_page": "/pricing",
         "blog_feed": "/blog/feed.xml",
         "keywords": ["email marketing", "automation"]
       },
       {
         "name": "Competitor B",
         "domain": "competitor-b.com",
         "pricing_page": "/plans",
         "blog_feed": "/feed.xml",
         "keywords": ["email campaigns", "marketing"]
       }
     ],
     "check_frequency": "daily",
     "alert_threshold": 5
   }
   EOF
   ```

3. **Initialize Google Sheet:**
   - Create sheet with columns: Date, Competitor, Metric, Old Value, New Value, Change %
   - Share with service account email

4. **Test Connection:**
   ```bash
   curl -X POST $SLACK_WEBHOOK_URL \
     -H 'Content-Type: application/json' \
     -d '{"text":"Competitor Spy Tool initialized ✅"}'
   ```

---

## Example Outputs

### Slack Alert (Price Change Detected)
```
🚨 PRICE CHANGE DETECTED
Competitor: TechRival Inc.
Change: Pro Plan $99 → $79 (-20%)
Detected: 2024-01-15 09:34 AM
Action: Review competitive positioning
```

### Content Discovery Report
```
📰 NEW COMPETITOR CONTENT (Last 24h)
Competitor A:
  ✓ "5 Email Marketing Trends for 2024" (Blog)
  ✓ "Case Study: 40% Open Rate Improvement" (Case Study)
  
Competitor B:
  ✓ "Product Launch: AI Subject Line Generator" (Announcement)
  ✓ "Pricing Update: Enterprise Tier Added" (Update)

Total posts: 4 | New features: 1 | Pricing changes: 1
```

### Keyword Ranking Report
```
📊 KEYWORD RANKINGS (vs. 24h ago)
Keyword: "email marketing automation"
  Competitor A: Position 3 (↑ 1) | Est. Traffic: 1.2K/mo
  Competitor B: Position 5 (↓ 2) | Est. Traffic: 890/mo
  You: Position 2 (→) | Est. Traffic: 1.8K/mo

Opportunity: Competitor A gaining momentum. Consider content refresh.
```

### Weekly Intelligence Summary
```
📈 WEEKLY COMPETITIVE INTELLIGENCE
Period: Jan 8-14, 2024

PRICING MOVEMENTS:
  • 2 competitors raised prices (avg +8%)
  • 1 competitor introduced annual discount
  • Enterprise tier pricing now $599-999 (range: 500-1200)

CONTENT VELOCITY:
  • Avg posts/competitor: 6.3/week
  • Top topics: AI features (35%), case studies (25%)
  • Your gap: Limited thought leadership content

KEYWORD SHIFTS:
  • 15 keywords tracked
  • Avg position change: -0.2 (slight improvement)
  • New keyword targets emerging: "generative AI marketing"

RECOMMENDED ACTIONS:
  1. Publish 2-3 thought leadership posts on AI
  2. Consider enterprise pricing adjustment
  3. Target "generative AI marketing" keyword cluster
```

---

## Tips & Best Practices

### 1. **Set Smart Alert Thresholds**
- Price changes: 5-10% (lower for commodities, higher for SaaS)
- Content: Alert on product announcements, not every blog post
- Keywords: Flag position changes >3 spots, not minor fluctuations

### 2. **Organize by Competitive Tier**
Monitor direct competitors (same market, price) separately from adjacent players. Direct competitors warrant daily checks; adjacent players, weekly.

```json
{
  "tier_1_direct": ["competitor1.com", "competitor2.com"],
  "tier_2_adjacent": ["adjacent1.com", "adjacent2.com"],
  "tier_3_emerging": ["startup1.com"]
}
```

### 3. **Create Keyword Clusters**
Group keywords by intent (pricing, features, use cases) to spot trends faster.

```
Pricing Intent: "cost", "pricing", "plans", "enterprise pricing"
Feature Intent: "AI", "automation", "integrations"
Use Case Intent: "B2B email", "ecommerce marketing"
```

### 4. **Establish Baseline Data**
Run initial scans for 2 weeks to establish normal patterns before setting alerts. This prevents false positives from minor page updates.

### 5. **Cross-Reference with Your Metrics**
Correlate competitor pricing changes with your conversion rates, churn, and customer feedback. Price wars often signal market saturation.

### 6. **Automate Report Distribution**
Schedule weekly reports to Slack #competitive-intel channel. Include executive summary + detailed metrics for strategy team.

---

## Safety & Guardrails

### What This Skill Will NOT Do

- **Scrape protected content:** This tool respects `robots.txt` and Terms of Service. It will not bypass authentication, paywalls, or CAPTCHA challenges.
- **Access private data:** No scraping of customer data, internal documents, or confidential information.
- **Violate GDPR/CCPA:** No personal data collection. Monitoring is limited to public-facing pages only.
- **Impersonate users:** All requests include proper User-Agent headers and identify as a monitoring bot.
- **Exceed rate limits:** Built-in throttling respects server load (max 10 requests/minute per domain).

### Ethical Boundaries

This tool monitors **public, published content only:**
- ✅ Public pricing pages
- ✅ Published blog posts and RSS feeds
- ✅ Public search engine rankings
- ✅ Landing page copy and screenshots
- ❌ Customer databases or user accounts
- ❌ Confidential internal documents
- ❌ Password-protected areas

### Legal Compliance

- Ensure your use complies with local laws and competitor ToS
- Document your monitoring for audit trails
- Do not share competitor data publicly without attribution
- Use intelligence for strategic decisions, not misleading marketing claims

---

## Troubleshooting

### "API Rate Limit Exceeded"
**Problem:** SerpAPI or competitor servers are rate-limiting requests.
**Solution:** 
- Reduce check frequency from daily to every 2 days
- Increase delay between requests: `delay: 5000ms` in config
- Upgrade SerpAPI plan for higher limits

### "Slack Webhook URL Invalid"
**Problem:** Webhook URL is expired or incorrectly formatted.
**Solution:**
```bash
# Test webhook
curl -X POST $SLACK_WEBHOOK_URL \
  -H 'Content-Type: application/json' \
  -d '{"text":"Test message"}'

# If 404, regenerate webhook at api.slack.com/apps
```

### "No Price Changes Detected (False Negative)"
**Problem:** Competitor uses dynamic pricing, JavaScript rendering, or session-based prices.
**Solution:**
- Enable Browserless rendering: `use_browserless: true`
- Add CSS selectors for price elements: `price_selector: ".plan-price"`
- Manually verify on competitor site; may be A/B testing

### "Google Sheets Not Updating"
**Problem:** Service account lacks write permissions.
**Solution:**
```bash
# Share sheet with service account email
# Grant Editor role (not Viewer)
# Test write permission
curl -X POST https://sheets.googleapis.com/v4/spreadsheets/$GOOGLE_SHEET_ID/values/Sheet1!A1:append \
  -H "Authorization: Bearer $GOOGLE_SHEETS_API_KEY" \
  -d '{"values":[["Test","Data"]]}'
```

### "Competitor Domain Returns 403/429"
**Problem:** Server is blocking automated requests.
**Solution:**
- Add rotating User-Agent headers
- Use residential proxy service (Bright Data, Smartproxy)
- Increase delay between requests
- Contact competitor's support if monitoring is legitimate

### FAQ

**Q: How often should I check competitors?**
A: Daily for direct competitors, weekly for adjacent players, monthly for emerging threats.

**Q: Can I monitor 50+ competitors?**
A: Yes, but scale API costs. Consider tiering: top 5 daily, next 15 weekly, others monthly.

**Q: What if a competitor blocks my IP?**
A: Use a proxy rotation service or contact them directly—legitimate competitive monitoring is defensible.

**Q: How do I export data for analysis?**
A: All data syncs to Google Sheets. Export as CSV/Excel for further analysis in Tableau, Looker, or custom dashboards.

**Q: Is this legal?**
A: Yes, monitoring public content is legal. Ensure you're not violating ToS, accessing protected areas, or using data deceptively.

---

## Integration Examples

### Slack Workflow
```
Daily at 9 AM → Run competitor scans → Slack alert if changes detected → Weekly summary to #strategy
```

### Google Sheets Historical Tracking
```
Append daily scan results → 12-month pricing history → Trend analysis charts
```

### WordPress Blog Integration
```
Detect competitor blog posts → Auto-create draft response posts → Publish counter-content
```

### Zapier Automation
```
Competitor price drop → Create Asana task → Notify sales team → Log to CRM
```

---

## Support & Updates

For issues, feature requests, or contributions: [GitHub Issues](https://github.com/ncreighton/empire-skills/issues)

**Version History:**
- 1.0.0 (Current): Initial release with pricing, content, and keyword monitoring

---

**Tags:** competitive-intelligence, web-scraping, market-research, pricing-monitoring, seo-tracking, automation, saas, ecommerce