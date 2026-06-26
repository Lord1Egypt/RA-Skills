---
name: brand-prospect-researcher
description: "Find brands actively spending on influencer and creator campaigns. Scans trade press, Instagram, job boards, and news for active-spender signals, then outputs a scored, prioritized prospect list with contacts. Use when you need to find brands to pitch, identify active advertisers, build a prospect list, research which brands are hiring influencer marketers, or find companies launching creator campaigns. Triggers on: 'find brands to pitch,' 'prospect list,' 'who's spending on influencers,' 'brand prospects,' 'active advertisers,' 'campaign activity,' or any request to identify brands actively investing in creator/influencer marketing."
---

# Brand Prospect Researcher

Find and score brands actively investing in influencer/creator marketing. Built for talent managers and self-managed creators who need to know which brands are spending right now so they can pitch with confidence.

## Prerequisites

- **web_search** tool (required) — for trade press, job postings, partnership news
- **web_fetch** tool (required) — for reading full articles
- **gram CLI** (optional) — for Instagram campaign activity signals. If unavailable, skip Instagram checks and note in output.

Check gram availability:
```bash
which gram
```
If not found, proceed without Instagram data and flag it in the report.

## Workflow

### 1. Collect User Configuration

Ask the user (or use defaults):

| Parameter | Default | Description |
|-----------|---------|-------------|
| `niche` | general | Vertical to scan (fashion, beauty, food, fitness, tech, lifestyle, gaming, travel, etc.) |
| `num_prospects` | 20 | Number of brands to return |
| `categories` | all | Which signal categories to scan (trade press, jobs, Instagram, partnerships) |
| `geo_focus` | US | Geographic market focus |
| `timeframe` | 3 months | How recent signals should be |

If user provides a niche, tailor ALL searches to that vertical.

### 2. Scan Trade Press for Campaign Activity

Run web searches across major trade publications. Adapt publication list to the user's niche:

**Cross-industry:** Ad Age, Adweek, Marketing Dive, The Drum, Campaign
**Fashion/Beauty:** BoF, WWD, Glossy, Fashionista, Allure
**Food/Bev:** Food & Wine, Eater, BevNET
**Tech:** TechCrunch, The Verge, Wired
**Lifestyle/Home:** Architectural Digest, Domino, Apartment Therapy
**Gaming:** IGN, Polygon, Kotaku
**Fitness:** Well+Good, Shape, Men's Health

Search queries (run 5-8 variations):
```
"[niche] influencer campaign 2026"
"[niche] brand creator partnership"
"[niche] influencer marketing launch"
"brand ambassador [niche] campaign announcement"
"[niche] creator collaboration new"
site:adage.com OR site:glossy.co "[niche] influencer"
```

For each result, extract: brand name, campaign type, date, publication, URL.

### 3. Search for Hiring Signals

Job postings for influencer marketing roles = strong active-spender signal.

```
"influencer marketing manager" "[niche]" hiring 2026
"creator partnerships" job posting [geo_focus]
"influencer relations" "[niche]" open role
site:linkedin.com/jobs "influencer marketing" "[niche]"
```

Extract: company name, role title, posting date, URL.

### 4. Find Partnership Announcements & Product Launches

```
"[niche] brand launch 2026"
"[niche] new product launch influencer"
"[niche] brand agency change" OR "agency of record"
"[niche] rebrand 2026"
```

Brands launching products or changing agencies are actively allocating budget.

### 5. Check Instagram Campaign Activity (if gram available)

For top candidate brands from steps 2-4, check Instagram for activity signals:

```bash
gram search "[brand name]" --limit 5
gram user info [brand_handle]
```

Look for:
- Recent sponsored/partnership posts
- Tagged creator content
- Campaign hashtags
- Follower growth (indicates ad spend)

If gram is unavailable, skip and note: "Instagram verification skipped — install gram CLI for deeper signal data."

### 6. Search for Contact Information

For each high-scoring brand, search for:
```
"[brand name] influencer marketing contact"
"[brand name] PR contact email"
"[brand name] head of influencer marketing" linkedin
"[brand name] partnerships" site:linkedin.com
```

Extract: name, title, email (if public), LinkedIn URL.

### 7. Score Each Brand

Score each brand 1-100 based on signal strength:

| Signal | Points |
|--------|--------|
| Active campaign in trade press (last 3 months) | +25 |
| Hiring influencer marketing roles | +20 |
| New product/rebrand launch | +15 |
| Agency change or new agency hire | +15 |
| Instagram campaign activity confirmed | +10 |
| Multiple signals from different sources | +10 |
| Contact info found | +5 |

**Tiers:**
- 🔥 **Hot** (70-100): Multiple strong signals, actively spending now
- 🟡 **Warm** (40-69): Clear intent signals, likely receptive
- 🔵 **Cool** (20-39): Some signals, worth monitoring

### 8. Output Format

```markdown
# Brand Prospect Report: [Niche]

**Generated:** [date]
**Niche:** [niche]
**Geo Focus:** [geo]
**Sources Scanned:** [count]
**Prospects Found:** [count]

## 🔥 Hot Prospects

### 1. [Brand Name] — Score: [X]/100
**Category:** [industry]
**Signals:**
- [Signal 1 with source link]
- [Signal 2 with source link]
**Why Now:** [1-2 sentences on why this brand is actively spending]
**Contact:** [Name, Title, LinkedIn/email if found]
**Campaign Type:** [What they're likely buying: posts, stories, ambassadors, events]

---

### 2. [Brand Name] — Score: [X]/100
...

## 🟡 Warm Prospects
[Same format, briefer]

## 🔵 Watch List
[Brand names with single signals — worth monitoring]

## Methodology
- Trade press scanned: [list publications]
- Job boards checked: [list]
- Search queries run: [count]
- Instagram checked: [yes/no]
- Date range: [timeframe]
```

## Error Handling

| Issue | Action |
|-------|--------|
| gram not installed | Skip Instagram checks, note in report, still deliver results |
| No results for niche | Broaden search terms, try adjacent verticals, report limited findings |
| Rate limited on web_search | Space queries, reduce total searches, prioritize trade press |
| No contacts found | Note "Contact research needed" — don't block the report |
| Very niche vertical | Supplement with general influencer marketing news, flag lower confidence |

## Tips for Best Results

- Narrow niches (e.g., "sustainable fashion" vs "fashion") yield more targeted results
- Run quarterly to catch seasonal campaign cycles
- Cross-reference with your existing outreach to avoid duplicates
- Hot prospects should be pitched within 1-2 weeks of signal detection
