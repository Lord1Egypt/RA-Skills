---
name: Monitor Competitor Content & Auto-Alert with Slack Integration
description: "Analyze competitor content across YouTube, TikTok, Substack & blogs to extract engagement metrics, posting patterns, and monetization strategies. Use when the user needs competitive intelligence, content benchmarking, or reverse-engineering viral hooks for their niche."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {"openclaw":{"requires":{"env":["YOUTUBE_API_KEY","TIKTOK_API_KEY","NEWSAPI_KEY","SERPER_API_KEY"],"bins":["python3","curl"]},"os":["macos","linux","win32"],"files":["SKILL.md"],"emoji":"📊"}}
---

## Overview

**Competitor Content Intelligence Extractor** automates the extraction and analysis of competitor content performance data across multiple platforms. Instead of manually tracking 10-15 competitors weekly (5+ hours of tedious work), this skill surfaces what's actually working in your niche: hook patterns, optimal posting times, audience sentiment, engagement velocity, and monetization signals.

### Why This Matters

Content creators and digital marketers waste enormous time on manual competitor research. This skill:
- **Eliminates guesswork**: Extract real engagement metrics (likes, comments, shares, audience retention)
- **Identifies patterns**: Discover hook formulas, content length sweet spots, and posting cadences that win
- **Speeds up strategy**: Get weekly competitive briefings in minutes, not hours
- **Integrates with your workflow**: Export data to Slack, Google Sheets, Notion, or your CMS
- **Tracks monetization**: Identify sponsorship patterns, affiliate links, product mentions, and revenue signals

### Supported Platforms

- **YouTube**: Video metadata, comment sentiment, subscriber growth, watch time patterns
- **TikTok**: Viral hooks, sound usage, hashtag performance, engagement velocity
- **Substack**: Newsletter open rates, subscriber growth, content themes, reader engagement
- **Blogs**: SEO performance, backlink profiles, content clusters, social signals
- **Twitter/X**: Thread performance, reply patterns, audience growth tactics

---

## Quick Start

Copy and paste these prompts directly to get started:

### Example 1: YouTube Competitor Analysis
```
Analyze the top 5 YouTube creators in the "AI tools for marketing" niche.
Extract: video titles (hook analysis), upload frequency, average view counts,
comment sentiment, audience retention patterns, and monetization signals
(sponsorships, affiliate links). Return as a CSV with competitor name,
content themes, optimal posting day, and engagement rate.
```

### Example 2: TikTok Viral Pattern Detection
```
Find the 10 most-viewed TikToks in #ContentCreator from the last 30 days.
Extract hook patterns (first 3 seconds), sound usage, hashtag strategy,
caption length, CTA patterns, and engagement velocity (likes per hour).
Identify 3 recurring hook formulas and provide examples. Format as a
structured JSON with "hook_formula", "sound_name", "avg_engagement_rate".
```

### Example 3: Substack Newsletter Competitive Briefing
```
Track 6 Substack newsletters in the "productivity" vertical. Extract:
- Newsletter name, subscriber count, publish frequency
- Open rate patterns, average word count, content themes
- Reader engagement (reply rate), sponsor mentions, growth rate
Output as a Slack message with top 3 insights and recommendations.
```

### Example 4: Content Gap Analysis
```
Compare my blog (example.com) against 8 competitors in "financial planning".
Extract: top 10 content pieces by traffic, keyword targets, content length,
backlink count, internal linking strategy. Identify content gaps where
competitors rank but I don't. Return a prioritized roadmap.
```

### Example 5: Monetization Strategy Deep-Dive
```
Analyze how 5 creators in "productivity" monetize. Extract: product mentions,
affiliate links (Amazon, Gumroad, ConvertKit), sponsorship frequency,
pricing patterns, checkout CTAs. Identify which monetization methods appear
in top-performing content. Format as a comparison table.
```

---

## Capabilities

### 1. Engagement Metrics Extraction
Automatically collect and normalize metrics across platforms:
- **View/subscriber growth** (YouTube, TikTok, Substack, Twitter)
- **Engagement rates** (likes, comments, shares, replies)
- **Engagement velocity** (growth speed in first 24-48 hours)
- **Audience demographics** (inferred from language, topics, engagement patterns)
- **Comment sentiment analysis** (positive/negative/neutral distribution)

**Usage Example:**
```
Extract engagement metrics for [competitor_channel] over the last 90 days.
Show: average views per video, engagement rate trend, top 3 performing videos,
audience growth rate. Alert me if any metrics spike or drop by >20%.
```

### 2. Content Pattern Analysis
Identify what makes competitor content sticky:
- **Hook formulas** (opening lines, visual hooks, curiosity gaps)
- **Optimal content length** (word count for blogs, video duration, newsletter length)
- **Posting frequency & timing** (best days/times for audience engagement)
- **Content structure** (intro pattern, body, CTA format)
- **Keyword strategy** (topics, LSI keywords, search intent alignment)

**Usage Example:**
```
Analyze content structure patterns for [competitor]. Extract: opening hooks
(first 10 words), content length distribution, CTA patterns, keyword targets.
Provide 5 hook templates I can adapt for my content.
```

### 3. Monetization Strategy Mapping
Surface how competitors convert audiences into revenue:
- **Product mentions** (frequency, placement, context)
- **Affiliate links** (networks, products promoted, link placement)
- **Sponsorship patterns** (sponsor types, frequency, disclosure style)
- **Upsells** (lead magnets, email sequences, paid products)
- **Revenue signals** (estimated earning potential based on engagement)

**Usage Example:**
```
Show all monetization touchpoints in [competitor's] top 10 videos.
List products mentioned, affiliate links, sponsorship deals, and pricing CTAs.
Estimate annual revenue based on engagement rates. Format as a pipeline.
```

### 4. Audience & Community Intelligence
Understand audience behavior and preferences:
- **Comment themes** (frequently asked questions, objections, praise)
- **Audience questions** (content gaps your competitor hasn't addressed)
- **Community sentiment** (satisfaction, complaints, feature requests)
- **Engagement patterns** (when/how audience interacts, reply rate)
- **Audience growth drivers** (which content types attract subscribers)

**Usage Example:**
```
Extract the top 50 comments from [competitor's] 5 most-viewed videos.
Identify: recurring questions, objections, compliments. Summarize audience
pain points and desires. Provide 5 content ideas based on unmet needs.
```

### 5. Posting Schedule & Frequency Optimization
Discover the cadence that drives visibility:
- **Posting calendar** (days/times content is published)
- **Frequency analysis** (optimal posting rate for the niche)
- **Seasonal patterns** (content spikes around events/seasons)
- **Platform-specific timing** (when YouTube, TikTok, Substack audiences are most active)
- **Gap identification** (days/hours when no content is published)

**Usage Example:**
```
Map [competitor's] publishing schedule for the last 180 days. Show: posting
frequency, day-of-week pattern, time-of-day pattern, any seasonal changes.
Recommend optimal posting schedule for maximum reach in this niche.
```

### 6. SEO & Backlink Competitive Analysis
Track search visibility and link authority:
- **Keyword rankings** (which keywords competitors rank for)
- **Organic traffic estimates** (from ranking keywords)
- **Backlink profile** (top referring domains, anchor text patterns)
- **Content gap analysis** (keywords competitors rank for, you don't)
- **Link opportunities** (sites linking to competitors)

**Usage Example:**
```
Analyze [competitor.com]'s SEO profile. Extract: top 20 ranking keywords,
estimated organic traffic, backlink sources, anchor text patterns. Identify
20 keywords I should target but competitors currently dominate. Export as CSV.
```

---

## Configuration

### Required Environment Variables

Set these in your environment before using the skill:

```bash
# YouTube Data API v3 (for video metrics, comments)
export YOUTUBE_API_KEY="your_youtube_api_key_here"

# TikTok Research API (for video performance, sounds, hashtags)
export TIKTOK_API_KEY="your_tiktok_api_key_here"

# NewsAPI (for blog tracking, article discovery)
export NEWSAPI_KEY="your_newsapi_key_here"

# Serper API (for SEO, backlink, keyword data)
export SERPER_API_KEY="your_serper_api_key_here"

# Optional: Slack integration for automated briefings
export SLACK_WEBHOOK_URL="REDACTED-SECRET"

# Optional: Google Sheets API for exporting reports
export GOOGLE_SHEETS_API_KEY="your_google_sheets_api_key"
```

### Setup Instructions

1. **Get YouTube API Key**:
   - Go to [Google Cloud Console](https://console.cloud.google.com)
   - Create a new project
   - Enable "YouTube Data API v3"
   - Create OAuth 2.0 credentials (service account)
   - Copy API key to `YOUTUBE_API_KEY`

2. **Get TikTok Research API Access**:
   - Apply for TikTok Research API at [TikTok Developers](https://developers.tiktok.com)
   - Request approval (24-48 hours)
   - Add API key to `TIKTOK_API_KEY`

3. **Get NewsAPI Key**:
   - Sign up at [NewsAPI.org](https://newsapi.org)
   - Copy API key to `NEWSAPI_KEY`

4. **Get Serper API Key**:
   - Sign up at [Serper.dev](https://serper.dev)
   - Copy API key to `SERPER_API_KEY`

5. **Enable Slack Integration** (Optional):
   - Create a Slack incoming webhook: [Slack Apps](https://api.slack.com/apps)
   - Copy webhook URL to `SLACK_WEBHOOK_URL`

### Configuration Options

```yaml
# competitor-config.yaml
analysis:
  platforms:
    - youtube
    - tiktok
    - substack
    - blogs
    - twitter
  
  lookback_period: 90  # days
  competitor_count: 10  # number of competitors to analyze
  
  metrics:
    extract_engagement: true
    extract_patterns: true
    extract_monetization: true
    extract_audience_sentiment: true
    extract_seo_data: true
  
  export:
    format: csv  # csv, json, google_sheets, slack
    destination: ./reports/
    schedule: weekly  # one-time, daily, weekly, monthly
```

---

## Example Outputs

### Output 1: YouTube Competitive Analysis CSV
```
Competitor,Channel,Subscribers,Avg Views,Eng Rate,Top Hook,Upload Freq,Monetization
"Creator A","AI Daily",145K,8.2K,5.2%,"3 ways to...","2x weekly","Sponsorships + Affiliate"
"Creator B","Tech Weekly",89K,4.1K,3.8%,"You missed...","Weekly","AdSense + Products"
"Creator C","AI Explained",52K,12.5K,7.1%,"Here's what...","3x weekly","Patreon + Sponsorships"
```

### Output 2: TikTok Hook Formula JSON
```json
{
  "analysis_date": "2024-01-15",
  "platform": "tiktok",
  "niche": "content-creation",
  "hook_formulas": [
    {
      "formula_id": 1,
      "pattern": "Contrarian statement + pattern interrupt",
      "examples": [
        "Everyone's doing it wrong...",
        "Stop wasting time on..."
      ],
      "avg_engagement_rate": 8.3,
      "viral_rate": 34,
      "sound_usage": ["trending_audio_xyz"],
      "hashtags": ["#ContentCreator", "#CreatorTips"]
    },
    {
      "formula_id": 2,
      "pattern": "Question + reveal",
      "examples": [
        "Guess how much I made?",
        "Can you spot the difference?"
      ],
      "avg_engagement_rate": 6.9,
      "viral_rate": 28,
      "sound_usage": ["viral_sound_abc"]
    }
  ],
  "best_posting_times": ["2pm-4pm EST", "7pm-9pm EST"],
  "content_length_optimal": "45-60 seconds"
}
```

### Output 3: Substack Briefing Slack Message
```
📊 **Weekly Newsletter Competitive Briefing**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🏆 **Top Performer**: The Productivity Pod (8.2K subscribers, +340/week)
  • Open rate: 47% (↑5% vs last week)
  • Content theme: AI productivity hacks
  • Publish day: Tuesday, 9am EST
  • Avg word count: 1,240

💡 **Emerging Insight**: Newsletter sponsorships spiked 40% among top 5
  • New sponsor types: AI tools, productivity apps
  • Avg sponsorship placement: 2x per issue
  • Estimated CPM: $50-75

⚠️ **Opportunity Gap**: No one covers "productivity budgeting"
  • Your competitors: 0 articles
  • Reader mentions: 23 in comments
  • Suggested post: "The $0 Productivity Stack for Bootstrappers"

📈 **This Week's Recommendation**: Publish Tuesday 9am with productivity angle
```

### Output 4: SEO Gap Analysis Table
```
Keyword,Monthly Volume,Difficulty,Competitor1,Competitor2,Me,Opportunity
"AI tools for writing",8500,42,#1,#3,#12,HIGH
"best ChatGPT prompts",12000,68,#2,#4,#18,MEDIUM
"productivity hacks 2024",4200,35,#1,#2,#8,HIGH
"how to use Claude API",2100,28,#3,#5,NR,VERY HIGH
"content calendar templates",3800,31,#2,#6,#14,HIGH
```

---

## Tips & Best Practices

### 1. Narrow Your Competitor Set
**Don't** analyze 50 competitors. **Do** pick 5-8 direct competitors and 2-3 aspirational ones.
- Direct competitors: Similar audience, format, niche
- Aspirational: Larger audience, advanced monetization strategies
- Analyze with 90-day rolling window for trend detection

### 2. Focus on Patterns, Not Individual Videos
One viral video is noise. 10 videos with the same hook formula is a signal.
- Extract top 20-30 performing pieces per competitor
- Identify 3-5 recurring patterns
- Test those patterns in your own content

### 3. Combine Multiple Data Signals
Don't rely solely on views. Combine:
- Engagement rate (comments, shares relative to views)
- Audience retention (for YouTube)
- Comment sentiment (loyalty signals)
- Monetization indicators (sponsorships, upsells)

### 4. Track Changes Over Time
Set up weekly scans of your competitor set:
- Did their posting frequency change?
- Did audience engagement shift?
- New monetization method appearing?
- New content theme emerging?

**Best Practice**: Create a Slack channel that receives automated briefings every Monday morning.

### 5. Extract Actionable Hooks
When you find a winning hook pattern, don't copy it—adapt it:
- **Original**: "5 productivity hacks nobody talks about"
- **Your version**: "5 productivity hacks for [your_audience]" or "5 productivity hacks in [your_niche]"

### 6. Map Monetization Progression
Understand the creator's revenue funnel:
1. **Phase 1**: AdSense/platform revenue only
2. **Phase 2**: Add sponsorships + affiliate links
3. **Phase 3**: Launch own products/community
4. **Phase 4**: Multiple revenue streams (courses, coaching, software)

Use this to predict your own monetization timeline.

### 7. Segment by Content Performance