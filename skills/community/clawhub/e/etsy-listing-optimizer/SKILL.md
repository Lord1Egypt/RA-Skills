---
name: etsy-listing-optimizer
description: "Optimize Etsy titles, tags, and descriptions using keyword research and competitor analysis. Use when the user needs to improve search visibility, increase conversions, or analyze competitor listings."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {"openclaw":{"requires":{"env":["ETSY_API_KEY","GOOGLE_TRENDS_API_KEY"],"bins":["curl","jq"]},"os":["macos","linux","win32"],"files":["SKILL.md"],"emoji":"🛍️"}}
---

# Etsy Listing Optimizer

## Overview

The Etsy Listing Optimizer is a comprehensive automation skill designed to help Etsy sellers maximize product visibility and conversion rates through data-driven optimization. This skill combines keyword research, competitor analysis, and AI-powered copywriting to transform underperforming listings into high-ranking, conversion-optimized product pages.

**Why this matters:** Etsy's search algorithm heavily weights titles, tags, and descriptions. A poorly optimized listing can be invisible to thousands of potential customers. This skill analyzes top-performing competitors, identifies high-volume search keywords, and rewrites your content to match buyer intent while maintaining brand voice.

**Integrations:** Works seamlessly with Etsy API, Google Trends, SEMrush (optional), Slack notifications, and Google Sheets for batch processing.

---

## Quick Start

Try these prompts immediately to see the skill in action:

### Example 1: Optimize a Single Listing
```
Optimize my Etsy listing for a handmade ceramic mug. 
Current title: "Ceramic Mug"
Current tags: mug, ceramic, handmade
Current description: "A nice ceramic mug for coffee or tea."
Target audience: millennial home decor enthusiasts
Budget: premium positioning
```

### Example 2: Analyze Competitor Listings
```
Analyze the top 10 competitors for "vintage leather journal" on Etsy.
Show me:
- Their most common keywords in titles
- Tag strategies (frequency, specificity)
- Description length and structure
- Price positioning
Generate recommendations for my listing.
```

### Example 3: Batch Optimize Multiple Listings
```
I have 25 Etsy listings for handmade jewelry.
Optimize all titles and tags for better search visibility.
Focus on:
- Long-tail keywords (3-4 word phrases)
- Seasonal trends (current month)
- High-volume, low-competition keywords
Export results to Google Sheets.
```

### Example 4: Keyword Research & Trend Analysis
```
Research keywords for "sustainable bamboo phone case."
Show:
- Monthly search volume (Google Trends data)
- Competition level on Etsy
- Seasonal demand patterns
- Related keywords with intent classification
- Recommended tag priority (must-have vs. nice-to-have)
```

---

## Capabilities

### 1. **Keyword Research & Analysis**
- Integrates with Google Trends API to identify search volume and seasonal patterns
- Analyzes Etsy search bar autocomplete suggestions (demand signals)
- Classifies keywords by intent: transactional (buyer-ready), informational, navigational
- Provides competition scoring: how many listings use each keyword
- Recommends keyword combinations with high volume + low competition

**Usage:**
```
Find the best keywords for "eco-friendly yoga mat."
Prioritize by: search volume × (1 - competition ratio)
Show seasonal trends for the next 6 months.
```

### 2. **Competitor Listing Analysis**
- Scrapes top 20 Etsy search results for a given keyword
- Extracts and analyzes:
  - Title structure and keyword placement
  - Tag selection and frequency
  - Description length, formatting, and persuasion techniques
  - Price positioning and discount patterns
  - Review count and rating (social proof indicators)
- Identifies patterns in high-performing listings
- Highlights gaps in your current optimization

**Usage:**
```
Compare my listing against top 5 competitors for "boho wall tapestry."
Show title formulas, tag strategies, and description techniques used by winners.
```

### 3. **AI-Powered Title Generation**
- Generates 5-10 optimized title variations
- Incorporates primary keyword in first 3 words (Etsy algorithm priority)
- Includes secondary keywords naturally
- Maintains character limits (140 chars for Etsy titles)
- A/B testing recommendations (which titles to test first)
- Preserves brand voice and USP (unique selling proposition)

**Usage:**
```
Generate 8 optimized titles for my "handmade leather journal" listing.
Primary keyword: leather journal
Secondary keywords: personalized, gift, vintage
Brand voice: artisanal, premium, eco-conscious
```

### 4. **Tag Optimization**
- Recommends 13 optimal tags (Etsy's maximum)
- Prioritizes tags by search volume and competition
- Balances specificity with reach (mix of broad + niche tags)
- Identifies "long-tail tags" (3-4 word phrases) for less saturated positioning
- Flags tags with high volume but extreme competition (avoid)
- Suggests seasonal tags for timely relevance

**Usage:**
```
Optimize tags for "personalized wooden gift box."
Current tags: box, wooden, gift, personalized
Target audience: wedding planners, corporate gifting
Season: Q4 (holiday season)
```

### 5. **Description Optimization**
- Analyzes current description for:
  - Keyword density (natural, not spammy)
  - Readability (sentence length, paragraph breaks)
  - Persuasion elements (benefits vs. features)
  - Call-to-action clarity
  - Mobile responsiveness (Etsy mobile users = 70%+ traffic)
- Rewrites descriptions to improve:
  - Scannability (bullet points, bold highlights)
  - Emotional triggers (aspirational language)
  - Objection handling (size, care, shipping info)
  - SEO optimization (keyword placement)
- Maintains authentic voice while improving conversion

**Usage:**
```
Rewrite my product description for better conversions.
Current description: "This is a nice coffee mug. It's made of ceramic. You can use it for hot drinks."
Pain points to address: durability concerns, dishwasher safety, size questions
Tone: warm, approachable, trustworthy
```

### 6. **Batch Processing & Export**
- Process 10-100+ listings in one operation
- Export results to:
  - Google Sheets (for review before publishing)
  - CSV (for bulk upload tools)
  - Slack (notifications of key changes)
- Tracks changes made (before/after comparison)
- Prioritizes listings by impact (biggest improvement potential first)

**Usage:**
```
Optimize all 50 of my Etsy listings.
Export to Google Sheets with columns: 
[Product Name | Old Title | New Title | Old Tags | New Tags | Improvement Score]
Send Slack notification when complete.
```

---

## Configuration

### Required Environment Variables

```bash
# Etsy API credentials (get from https://www.etsy.com/developers)
ETSY_API_KEY=your_etsy_api_key
ETSY_API_SECRET=your_etsy_api_secret
ETSY_SHOP_ID=your_shop_id

# Google Trends API (for keyword volume data)
GOOGLE_TRENDS_API_KEY=your_google_api_key

# Optional: SEMrush integration (for advanced competition analysis)
SEMRUSH_API_KEY=your_semrush_key

# Optional: Slack notifications
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
```

### Setup Instructions

1. **Register for Etsy API Access:**
   - Go to https://www.etsy.com/developers
   - Create an application
   - Generate API keys and store in environment variables

2. **Enable Google Trends API:**
   - Create a Google Cloud project
   - Enable Trends API
   - Generate service account credentials

3. **Configure Skill Parameters:**
   ```yaml
   optimization_mode: "aggressive" # conservative | balanced | aggressive
   keyword_volume_threshold: 100    # minimum monthly searches
   competition_threshold: 5000      # max listings using keyword
   export_format: "google_sheets"   # csv | json | google_sheets
   auto_publish: false              # don't auto-publish; review first
   ```

---

## Example Outputs

### Sample 1: Single Listing Optimization Report

```
📊 ETSY LISTING OPTIMIZATION REPORT
Product: Handmade Ceramic Mug

CURRENT STATE:
  Title: "Ceramic Mug"
  Tags: mug, ceramic, handmade, coffee, tea, gift, blue
  Description: 85 words (too short)
  Current Etsy Rank: #247 for "ceramic mug"

KEYWORD ANALYSIS:
  Primary: "ceramic mug" (2,400 searches/month, 8,200 listings)
  Secondary: "handmade ceramic mug" (890 searches/month, 1,200 listings) ⭐
  Opportunity: "personalized ceramic mug" (1,100 searches/month, 3,400 listings) ⭐⭐

OPTIMIZED TITLE (Recommended):
  "Handmade Ceramic Mug | Personalized Coffee Cup | Artisan Gift"
  (138 characters, includes 3 primary keywords in first 6 words)

OPTIMIZED TAGS (Priority Order):
  1. handmade ceramic mug (890 searches, 1,200 competitors)
  2. personalized coffee mug (1,100 searches, 3,400 competitors)
  3. ceramic coffee cup (450 searches, 2,100 competitors)
  4. artisan mug (280 searches, 890 competitors)
  5. gift for coffee lover (320 searches, 1,200 competitors)
  6. blue ceramic mug (180 searches, 450 competitors)
  7. handmade pottery (1,200 searches, 5,600 competitors)
  8. home decor mug (290 searches, 3,100 competitors)
  9. unique coffee gift (210 searches, 800 competitors)
  10. ceramic drinkware (150 searches, 400 competitors)
  11. artisan pottery mug (95 searches, 280 competitors)
  12. personalized gift (5,600 searches, 45,000 competitors - broad reach)
  13. coffee lover gift (410 searches, 1,900 competitors)

REWRITTEN DESCRIPTION (285 words, optimized for mobile):
  Handcrafted ceramic mug perfect for coffee, tea, or your favorite beverage. 
  Each piece is individually thrown and glazed by hand, making it truly unique.
  
  ✨ FEATURES:
  • Dishwasher safe (top rack recommended)
  • Microwave safe
  • Food-safe glaze
  • Holds 12 oz (standard coffee mug size)
  • Available in 5 colors
  
  🎁 PERFECT FOR:
  • Daily morning coffee ritual
  • Corporate gifts
  • Housewarming presents
  • Coffee lover gifts
  • Home decor accent
  
  📝 CUSTOMIZATION:
  Add a personalized name or message (up to 15 characters) for $5 extra.
  
  🌱 ECO-FRIENDLY:
  Made from sustainable clay. No harmful chemicals or synthetic glazes.
  
  ⚠️ CARE INSTRUCTIONS:
  Hand wash recommended for longevity. Avoid sudden temperature changes.
  
  Each mug is handmade to order and ships within 5-7 business days.

PROJECTED IMPACT:
  ✅ Estimated rank improvement: #247 → #18 for "ceramic mug"
  ✅ Estimated visibility increase: +340% in search impressions
  ✅ Expected CTR improvement: +28% (better title/description match)
  ✅ Conversion impact: +15-22% (assuming similar traffic quality)
```

### Sample 2: Competitor Analysis

```
🔍 COMPETITOR ANALYSIS: "Vintage Leather Journal"

TOP 5 LISTINGS ANALYZED:

Rank #1 - "Vintage Leather Journal | Personalized Diary | Refillable Notebook"
  Strengths:
    • Title includes 3 primary keywords in first 8 words
    • 4.8★ rating (287 reviews) - strong social proof
    • Price: $34.99 (premium positioning)
    • Description: 420 words (comprehensive, benefit-focused)
  
  Tags Used:
    leather journal, vintage journal, personalized journal, diary, notebook,
    refillable journal, leather diary, gift for writer, journaling, handmade,
    personalized gift, writing journal, leather notebook

Rank #2 - "Handmade Leather Journal Vintage Style Personalized"
  Strengths:
    • Simpler title (easier to remember)
    • 4.7★ rating (156 reviews)
    • Price: $29.99 (value positioning)
    • Description: 280 words (scannable, bullet-point heavy)

PATTERN ANALYSIS:
  ✅ All top 5 use "personalized" in title (high-intent keyword)
  ✅ Average title length: 7-9 words
  ✅ All include "handmade" or "vintage" for authenticity
  ✅ Descriptions average 300-450 words
  ✅ Price range: $24.99-$44.99 (your price: $32.99 = competitive ✓)
  ⚠️ Tag strategy: Mix of specific (leather journal) + broad (gift, personalized)

RECOMMENDATIONS FOR YOUR LISTING:
  1. Add "personalized" to title (all top 5 use it)
  2. Expand description to 350+ words (you're at 180)
  3. Add "gift for writer" tag (used by 4 of top 5)
  4. Consider seasonal angle ("perfect graduation gift" for Q4)
```

---

## Tips & Best Practices

### 1. **Keyword Research Strategy**
- **Do:** Focus on "long-tail" keywords (3-4 words) that have 100-1,000 monthly searches
  - Why? Less competition, higher buyer intent, better conversion rates
- **Don't:** Target massive keywords like "gift" (45M+ searches) — you'll never rank
- **Pro tip:** Use Google Trends to identify seasonal keywords 6 weeks in advance
  ```
  Example: "Personalized wedding favors" peaks in Feb-March (wedding season planning)
  Optimize listings 6 weeks early to capture rising demand.
  ```

### 2. **Title Optimization**
- **Formula that works:** [Primary Keyword] | [Benefit/USP] | [Secondary Keyword]
  - Example: "Handmade Leather Journal | Personalized Diary | Perfect Gift"
- **Position keywords strategically:** Etsy algorithm weights words in first 3-5 positions heavily
- **A/B test:** Generate 3 title variations and monitor which gets more clicks
- **Avoid:** Keyword stuffing (looks spammy, hurts conversions)
  - ❌ Bad: "leather journal journal diary journal notebook journal gift"
  - ✅ Good: "Handmade Leather Journal | Personalized Diary | Gift"

### 3. **Tag Strategy**
- **Mix specificity:** 5-6 specific tags + 3-4 broad tags + 3-4 long-tail tags
  - Specific: "ceramic handmade mug" (lower volume, higher intent)
  - Broad: "gift", "home decor" (high volume, lower intent)
  - Long-tail: "personalized ceramic mug for coffee lovers" (ultra-specific)
- **Avoid gaps:** If you have 13 tag slots, use all 13 (Etsy rewards tag usage)
- **Update seasonally:** Swap 2-3 tags quarterly to capture seasonal demand

### 4. **Description Best Practices**
- **Lead with benefits, not features:**
  - ❌ Bad: "Made from ceramic. 12 oz capacity. Microwave safe."
  - ✅ Good: "Start your morning ritual with this artisan ceramic mug. Durable enough for daily use, beautiful enough to display."
- **Use formatting:** Bullet points, bold text, line breaks improve mobile readability
- **Address objections:** Include care instructions, size details, shipping timeline
- **Include call-to-action:** "Add to cart," "Perfect gift," "Limited stock"
- **Target length:** 250-400 words (comprehensive but scannable)

### 5. **