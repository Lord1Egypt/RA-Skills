---
name: competitor-intelligence
description: Systematic competitor research and intelligence gathering skill. Covers how to find competitor fanpages, analyze their ad strategies, extract key insights, and build competitive advantage for Boss Store Vietnam in the cosmetics/health retail sector.
---

# 🕵️ Competitor Intelligence Playbook

> **Purpose**: Turn competitor data into actionable advantage. Always fetch live data before analyzing. Never make up competitor information.

---

## 1. How to Find Competitor Fanpages (If Not Given)

When boss says "tìm đối thủ" or "xem thị trường", execute this flow:

### Step 1: Google Search for Competitors
```
serper_search queries to run (in this order):
1. "mỹ phẩm chăm sóc sức khỏe fanpage facebook việt nam"
2. "top brand beauty skincare facebook ads vietnam 2025"
3. site:facebook.com "mỹ phẩm" quảng cáo
4. "<specific product category> facebook page việt nam"
```

### Step 2: For Each Promising URL Found
```
meta_ad_library(pageUrl: <url>) → Check if they're running ads
→ If running ads → add to competitor list
→ If not running ads → skip (they're not a real ad competitor)
```

### Step 3: Deep Analysis of Active Competitors
```
For top 3–5 competitors with active ads:
  apify_facebook_ads(url: <url>, limit: 20)
  ads_manager_scrape(url: <url>)  ← For page About info
  ads_manager_save_competitor(...)  ← Save to memory
```

---

## 2. Competitor Analysis Protocol

For EACH competitor page analyzed, extract and report:

### 2.1 Business Intelligence
```
□ Page name and verified status
□ Follower count (rough indicator of market presence)
□ Industry/category
□ Physical location if visible
□ Website URL
□ Phone / Zalo contact
□ Key products/services offered
```

### 2.2 Ad Strategy Intelligence
```
□ Total number of active ads
□ Ad formats used (Image / Video / Carousel)
□ Approximate daily spend range (from Meta Ad Library impressions data)
□ Targeting countries (from ad library)
□ Duration of longest-running ads (older = proven)

The LONGEST running ad = their most profitable ad = their "control ad"
```

### 2.3 Creative Intelligence
```
For each active ad:
  □ Hook (first line / first 3 seconds)
  □ Core offer / value proposition
  □ Social proof used (testimonials, results, reviews)
  □ CTA (Call-to-action)
  □ Landing page destination type (Messenger / Website / WhatsApp)
  □ Emotional angle (Fear / Aspiration / Belonging / Curiosity / Urgency)
```

### 2.4 Positioning Intelligence
```
□ Price positioning: Premium / Mid-market / Budget?
□ Target customer: Age/gender/lifestyle signals in ads
□ Differentiation claim: What makes them different?
□ Unique selling point: What do they claim no one else can offer?
```

---

## 3. Competitive Advantage Analysis

After gathering competitor data, answer these questions:

### 3.1 Gap Analysis
```
What are competitors NOT doing that Boss Store Vietnam COULD do?
  → Check if competitors use video (if not, video is differentiation opportunity)
  → Check if competitors use testimonials (if not, social proof is opportunity)
  → Check if competitors offer free samples / trial (if not, risk-reversal is opportunity)
```

### 3.2 Offer Analysis
```
What OFFERS are performing (long-running ads)?
  → Free shipping threshold
  → Bundle deals (mua 2 tặng 1)
  → Loyalty programs
  → Limited-time offers
  → Free gift with purchase
```

### 3.3 Angle Library
Build a list of all angles competitors are using:
```
Common Vietnamese beauty/health ad angles:
  □ "Dùng thử miễn phí"
  □ "Kết quả sau X ngày"
  □ "Được chứng nhận bởi..."
  □ "Bác sĩ khuyên dùng"
  □ "Hàng ngàn khách hàng hài lòng"
  □ "[Celebrity/KOL] sử dụng"
  □ "Giảm X% hôm nay"
  □ "Chính hãng nhập khẩu"
```

---

## 4. Competitor Monitoring Schedule

### Weekly Monitoring
- Check top 3 competitors for new ads
- Report any new ad angles or offers
- Flag if competitor increased spending (more ads = more spend)

### Monthly Deep Analysis
- Full competitor audit (all active ads analyzed)
- Year-over-year comparison if memory data exists
- Update competitive positioning recommendations

### Trigger-Based Monitoring (Do immediately when triggered)
- Boss sends new competitor URL → Full analysis protocol (Section 2)
- Own CPA spikes without clear internal reason → Check if competitor increased spend
- New product launch → Find competitive alternatives

---

## 5. Competitive Report Template

```
🕵️ BÁO CÁO CẠNH TRANH — [Date]

**Đối Thủ Đang Theo Dõi:** [N competitors in memory]

━━━━━━━━━━━━━━━━━━━━━

🏢 [Competitor Name 1]
   Trang: [URL]
   Ads đang chạy: [N]
   Angle chính: [description]
   Offer mạnh nhất: [description]
   Chạy lâu nhất: [ad description] — [X days]

🏢 [Competitor Name 2]
   ...

━━━━━━━━━━━━━━━━━━━━━

💡 INSIGHTS THỊ TRƯỜNG:
• [Trend 1 spotted across multiple competitors]
• [Trend 2]
• [Gap/opportunity Boss Store Vietnam can exploit]

🎯 ĐỀ XUẤT CHO BOSS STORE VIETNAM:
1. Test angle: "[angle from competitor that we haven't tried]"
2. Test offer: "[offer format that competitors are using successfully]"
3. Opportunity: "[gap no competitor is filling]"
```

---

## 6. Intelligence Memory Rules

### ALWAYS save to memory after analysis:
```
ads_manager_save_competitor({
  name: "<page_name>",
  angle: "<their dominant ad angle>",
  note: "<specific insight: their best performing ad description, offer used, landing page type>",
  sourceUrl: "<facebook_page_url>"
})
```

### Before any competitor analysis, CHECK MEMORY FIRST:
```
ads_manager_brief(mode: "competitors")
  → If competitor exists in memory:
    - Compare new findings to historical data
    - Note any strategy changes (new angles, new offers)
    - Check if they scaled up or down
  → If competitor NOT in memory:
    - Run full analysis protocol (Section 2)
    - Save all findings to memory
```

---

## 7. Red Flags in Competitor Ads (Things to Watch)

These competitor behaviors indicate market shifts:
- **Sudden 3x+ increase in number of active ads** → They found a winning formula or are testing heavily
- **Running same ad for 30+ days** → This is their "control" — high-performing proven ad
- **New angle never seen before** → May be testing a new market positioning
- **Pulling all ads down** → Account issue, or complete strategy pivot
- **Switching from image to video** → Responding to performance data

When any red flag spotted → Alert boss immediately and create competitive response proposal.
