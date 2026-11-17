---
name: Monitor Content Decay & Score Refresh Opportunities Automatically
description: "Analyze content decay patterns and prioritize refresh opportunities by scoring search ranking loss, engagement drop-off, competitor movement, and outdated data. Use when the user needs content audit recommendations, SEO refresh strategy, or audience re-engagement campaigns."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {"openclaw":{"requires":{"env":["GOOGLE_ANALYTICS_API_KEY","GOOGLE_SEARCH_CONSOLE_API_KEY","SERP_API_KEY"],"bins":["python3","curl"]},"os":["macos","linux","win32"],"files":["SKILL.md"],"emoji":"📉"}}
---

## Overview

The **Content Decay & Refresh Opportunity Scorer** is a predictive intelligence module that transforms raw content performance data into actionable refresh recommendations. Rather than simply flagging outdated content, this skill analyzes decay patterns across multiple dimensions—search ranking erosion, engagement velocity, competitive positioning shifts, and factual staleness—then delivers a prioritized list with *specific* refresh actions.

### Why This Matters

Content degrades predictably. As competitors publish updated versions, search algorithms evolve, and audience interests shift, your high-performing content loses visibility and relevance. Manual audits are slow and subjective. This skill automates the discovery process, surfacing which content to refresh first and *exactly what type of refresh* (update stats, expand sections, add recent case studies, reformat for featured snippets, etc.).

### Integration Points

- **Google Analytics 4** — engagement metrics, user drop-off trends
- **Google Search Console** — ranking position tracking, impression/click decay
- **SEMrush / Ahrefs API** — competitor content analysis, backlink decay
- **WordPress REST API** — publish dates, update frequency, content structure
- **Slack** — deliver prioritized refresh lists to editorial teams
- **HubSpot / Marketo** — connect to marketing automation workflows
- **GitHub / GitLab** — version-controlled content repositories

---

## Quick Start

### Example 1: Audit a Blog Category

```
Analyze my WordPress blog posts from the "Marketing Automation" category.
I have Google Analytics and Search Console connected. 
Score content decay for:
- Ranking position changes (last 90 days)
- Click-through rate decline >15%
- Engagement time drop >20%
- Published date >18 months ago with technical content
Return top 10 refresh opportunities with specific recommendations.
```

### Example 2: Prioritize Competitor-Driven Refresh

```
My top-ranking article on "Email Marketing Best Practices" has been slipping.
Analyze:
1. My ranking for primary keyword (last 180 days)
2. Competitor articles now ranking above me
3. New topics they've covered that I haven't
4. Backlink changes for my URL
Return a refresh strategy with specific sections to expand, 
new case studies to add, and updated stats to incorporate.
```

### Example 3: Bulk Audit with Slack Delivery

```
Score all content published in my /resources directory older than 12 months.
Weight the decay model by:
- 40% search ranking loss
- 30% engagement velocity
- 20% competitor activity
- 10% data staleness (citations older than 2 years)
Identify the 15 highest-priority refresh candidates.
Send results to Slack #content-strategy with severity flags.
```

### Example 4: Fact-Based Staleness Detection

```
Audit my whitepapers and case studies for outdated claims.
Flag content that:
- References statistics older than 3 years
- Mentions deprecated product versions
- Contains regulatory info affected by 2024 law changes
- References old market research/analyst reports
Prioritize by audience impact: show which pieces affect sales/conversion most.
```

---

## Capabilities

### 1. Multi-Dimensional Decay Analysis

Scores content across four independent decay vectors:

**Search Ranking Decay**
- Tracks keyword position history (via Google Search Console API)
- Calculates position loss velocity (steep vs. gradual decline)
- Detects ranking cliff events (algorithm updates)
- Compares against competitor movement for same keywords
- Flags pages with lost featured snippet status

**Engagement Decay**
- Analyzes engagement time trends (GA4 time_on_page metric)
- Calculates drop-off rate by cohort (new visitors vs. returning)
- Detects bounce rate inflation
- Compares current engagement to page's historical peak
- Identifies which traffic segments show lowest engagement

**Competitive Positioning Shift**
- Maps which competitors now rank above you
- Analyzes their content freshness, word count, backlink authority
- Identifies gap topics they've published that you haven't
- Tracks their content update frequency
- Reveals search intent drift (user behavior changes)

**Factual & Data Staleness**
- Extracts citations and publication dates from content
- Flags statistics older than configurable threshold (default: 3 years)
- Cross-references with news/regulatory databases for invalidation
- Detects deprecated product/feature references
- Identifies market research older than refresh cycle

### 2. Prioritized Recommendation Engine

Generates specific, actionable refresh actions:

```
[PRIORITY SCORE: 8.7/10]
Content: "Email Marketing ROI Guide" (12 months old)
URL: /resources/email-roi-2024
Current Ranking: Page 1, Position 7 (keyword: "email marketing ROI")
Decay Drivers:
  • Ranking slipped from Position 2 → Position 7 (lost 5 spots in 90 days)
  • Engagement time down 32% vs. 6-month average
  • HubSpot published competing article ranking Position 3 (published 2 months ago)
  • 68% of cited statistics are 4+ years old

Recommended Refresh Actions (Priority Order):
1. UPDATE STATISTICS (High Impact)
   - Replace 2020 Statista data with 2024 reports
   - Add current conversion rate benchmarks (update section: "Benchmark Your Performance")
   - Refresh ROI calculation examples with latest email platform pricing

2. EXPAND SECTION (Medium Impact)
   - Add "AI-Powered Subject Line Optimization" subsection (HubSpot has this; you don't)
   - Include new case study from recent client: Q4 2024 campaign achieving 4.2% conversion

3. REFORMAT FOR SNIPPETS (Medium Impact)
   - Create structured data FAQ schema for "How to calculate email ROI?"
   - Convert "Quick Calculation Formula" to comparison table format

4. LINK & AUTHORITY (Low Impact)
   - Add 3 new outbound links to 2024 research (improves freshness signals)
   - Audit internal links; update 6 broken references to redirects

Estimated Impact: Refresh should recover 2-3 ranking positions within 30 days.
Time to Complete: 3-4 hours. Effort Level: Moderate.
```

### 3. Batch Audit Mode

Process 50-500 pieces of content with decay scoring and automated prioritization:

- Generate CSV export with all URLs, scores, and recommended actions
- Filter by minimum decay score, publication date, traffic volume
- Group by recommended action type (statistics, expansion, reformat, etc.)
- Export as individual refresh briefs for editors
- Schedule periodic rescores (weekly/monthly) to track improvement

### 4. Custom Decay Weighting

Adjust the scoring formula to match your priorities:

```json
{
  "decay_weights": {
    "search_ranking_loss": 0.40,
    "engagement_drop": 0.30,
    "competitor_activity": 0.20,
    "data_staleness": 0.10
  },
  "ranking_loss_sensitivity": 1.2,
  "engagement_threshold_percent": 15,
  "data_age_threshold_years": 3,
  "competitor_tracking_enabled": true,
  "min_traffic_for_analysis": 50
}
```

---

## Configuration

### Required Environment Variables

```bash
# Google APIs (for ranking & engagement data)
export GOOGLE_ANALYTICS_API_KEY="your-ga4-service-account-key.json"
export GOOGLE_SEARCH_CONSOLE_API_KEY="your-gsc-api-key"

# Optional: Competitive Intelligence (SEMrush / Ahrefs)
export SEMRUSH_API_KEY="optional-semrush-api-key"
export AHREFS_API_KEY="optional-ahrefs-api-key"

# Optional: External Data Sources
export SERPAPI_KEY="for-serp-tracking"
export OPENAI_API_KEY="for-NLP-staleness-detection"

# Optional: Output Integrations
export SLACK_WEBHOOK_URL="REDACTED-SECRET"
export WORDPRESS_API_URL="https://yoursite.com"
export WORDPRESS_API_USER="your-api-user"
export WORDPRESS_API_PASSWORD="your-app-password"
```

### Setup Steps

1. **Connect Google Analytics 4**
   - Create service account in Google Cloud Console
   - Grant "Analytics Viewer" role to service account
   - Download JSON key, store as `GA4_KEY.json`
   - Set `GOOGLE_ANALYTICS_API_KEY` to file path

2. **Connect Google Search Console**
   - Authorize app in GSC settings
   - Verify site property ownership
   - Save API credentials

3. **Configure Content Sources**
   - For WordPress: Enable REST API, create application password
   - For custom CMS: Provide content export (CSV with URL, publish_date, content columns)
   - For GitHub: Provide repo path and branch

4. **Set Decay Thresholds**
   - Define what "staleness" means for your content type (3-5 years for stats, 1-2 years for product features)
   - Set minimum traffic threshold (exclude low-traffic content from scoring)
   - Choose ranking loss sensitivity (how quickly position loss triggers scoring)

5. **Initialize Baseline**
   ```bash
   content-decay-scorer init \
     --source wordpress \
     --site-url https://yourblog.com \
     --lookback-days 180
   ```

---

## Example Outputs

### Output 1: Individual Content Score Card

```
╔════════════════════════════════════════════════════════════════╗
║ DECAY SCORE: 8.2/10 — HIGH PRIORITY REFRESH CANDIDATE         ║
╚════════════════════════════════════════════════════════════════╝

Title: "Complete Guide to Marketing Attribution Models"
URL: /blog/attribution-models-2024
Primary Keyword: "marketing attribution models"

DECAY BREAKDOWN:
┌─ Search Ranking Loss (40% weight): 8.5/10
│  └─ Lost 6 positions in 120 days (Page 1 → Page 2)
│  └─ Competitor gained authority with fresher piece
│  └─ Your content: Published 14 months ago
│  └─ Competitor's content: Published 3 months ago
├─ Engagement Decline (30% weight): 7.8/10
│  └─ Avg. time on page: 4:12 (vs. 6:45 six months ago)
│  └─ Bounce rate: 42% (↑ 8% from baseline)
│  └─ Return visitor rate: 23% (↓ 12% from baseline)
├─ Competitive Positioning (20% weight): 8.9/10
│  └─ 3 new high-authority competitors now rank above you
│  └─ HubSpot's piece: 5,000+ words, 12 case studies (vs. your 3,200 words, 2 cases)
│  └─ Forrester report published Q4 2024 (new market data you lack)
└─ Data Staleness (10% weight): 7.2/10
   └─ 5 statistics dated 2021-2022 (should be 2023-2024)
   └─ Market size estimate: $12.5B (outdated; current $18.3B)
   └─ Platform references: HubSpot, Marketo (Salesforce acquisition changed positioning)

RECOMMENDED REFRESH ACTIONS (Prioritized):
─────────────────────────────────────────
1. ⭐ UPDATE STATISTICS [High Impact, 1.5 hrs]
   • Replace Gartner 2022 data with 2024 Magic Quadrant
   • Add Forrester Wave analysis from Q4 2024
   • Update market size: $12.5B → $18.3B (per latest IDC report)
   • Add 2024 adoption rates by attribution model

2. ⭐ EXPAND CONTENT [High Impact, 2 hrs]
   • Add section: "AI-Powered Attribution (New in 2024)"
   • Add 2 new case studies (yours + 1 industry leader example)
   • Create comparison table: Multi-touch vs. First-party vs. AI models
   • Add "Challenges in 3rd-Party Cookie Deprecation" section

3. 📊 REFORMAT FOR SEARCH [Medium Impact, 1 hr]
   • Add FAQ schema markup ("What is marketing attribution?", "Which model is best?")
   • Create visual comparison table → structured data
   • Add featured snippet optimization for "types of attribution models"

4. 🔗 AUTHORITY & FRESHNESS [Low Impact, 30 min]
   • Add 4 new outbound links to 2024 resources (Forrester, HubSpot, Gartner)
   • Update internal link anchor text from "old" to "attribution models 2024"
   • Add schema for "lastReviewed" date (freshness signal)

PREDICTED IMPACT:
─────────────────
• Ranking recovery: 2-3 positions within 30 days
• Engagement improvement: +15-20% time-on-page within 60 days
• Traffic increase: +25-35% within 90 days (based on historical refresh data)

ESTIMATED EFFORT: 5 hours total | Skill Level: Moderate | ROI: Very High
TARGET COMPLETION: Within 2 weeks
```

### Output 2: Batch Audit CSV

```csv
rank,url,title,decay_score,primary_keyword,ranking_position,days_since_publish,engagement_trend,competitor_threat,data_staleness,primary_action,secondary_actions,effort_hours,priority
1,/blog/email-marketing-roi,Email Marketing ROI Guide,8.7,email marketing roi,7,365,↓32%,high,4.2y,UPDATE_STATS,"EXPAND, SNIPPET",3.5,critical
2,/blog/seo-checklist-2024,SEO Checklist 2024,8.4,seo checklist,6,180,↓18%,high,2.8y,EXPAND_CONTENT,"STATS, SNIPPETS",4,critical
3,/resources/buyer-journey,Modern Buyer Journey,7.9,buyer journey,9,420,↓24%,medium,3.1y,UPDATE_STATS,"EXPAND, REFORMAT",3,high
4,/blog/crm-implementation,CRM Implementation Guide,7.3,crm setup,12,210,↓8%,medium,2.0y,EXPAND_CONTENT,"STATS, LINKS",2.5,high
5,/guides/content-marketing,Content Marketing 101,6.8,content marketing strategy,15,180,↓5%,low,1.5y,MINOR_REFRESH,"STATS",1.5,medium
```

### Output 3: Slack Summary Report

```
📉 CONTENT DECAY AUDIT COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Audited: 47 pieces of content
Critical Priority (refresh within 2 weeks): 6 pieces
High Priority (refresh within 4 weeks): 12 pieces
Medium Priority (refresh within 8 weeks): 18 pieces
Total Estimated Effort: 52 hours
Predicted Traffic Recovery: +31% within 90 days

🔴 CRITICAL REFRESH NEEDED:
1. Email Marketing ROI Guide (Decay: 8.7) — HubSpot's new guide stealing traffic
2. SEO Checklist 2024 (Decay: 8.4) — Algorithm updates made content outdated
3. Modern Buyer Journey (Decay: 7.9) — Statistics from 2021 need refresh

✅ CLICK BELOW TO VIEW FULL REPORT & RECOMMENDATIONS:
[View Full Audit] [Assign to Editor] [Export as CSV]
```

---