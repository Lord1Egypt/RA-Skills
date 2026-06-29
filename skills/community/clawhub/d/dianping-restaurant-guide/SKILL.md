---
name: Dianping Restaurant Guide
slug: dianping-restaurant-guide
description: Extract real restaurant insights from Dianping reviews: filter noise, detect fake reviews, build personalized dining guides.
tags: [dianping, restaurant, food, dining, review-analysis, china, recommendation]
version: 1.0.0
license: MIT-0
---

# Dianping Restaurant Guide (大众点评探店指南)

Make smarter dining decisions by cutting through Dianping's noise. Detect fake reviews, extract genuine sentiment signals, and get personalized restaurant recommendations with dish-level ordering guides.

## Core Capabilities

- **Review authenticity analysis**: Detect suspicious review patterns — timing clusters, user activity profiles, language similarity, and photo metadata
- **Sentiment distillation**: Filter out probable fake reviews, then aggregate genuine opinions across taste/environment/service/value
- **Personalized ranking**: Score restaurants against your preferences (cuisine, budget, occasion, distance)
- **Dish-level recommendations**: Not just which restaurant — which specific dishes to order, and which to avoid
- **Exploration route planner**: Optimize a multi-restaurant exploration itinerary by geography
- **Polarization decoder**: When reviews are split 50/50, analyze what each camp values and help you decide

## Workflow (8 Steps)

### Step 1: Define Dining Context
**Input**: User provides:
- **Location**: City + district/landmark (e.g., "上海静安寺", "北京三里屯")
- **Cuisine preference**: Type (川菜/日料/西餐/火锅...) or "any"
- **Budget**: Per-person range (e.g., ¥50-100, ¥200+)
- **Occasion**: Date / family / solo / group dinner / business
- **Distance radius**: Walking (1km) / short taxi (5km) / willing to travel

**Output**: Structured dining profile.
**Logic**: Fill missing fields with sensible defaults (budget = ¥50-150, radius = 3km). Ask clarifying questions for ambiguous inputs.

### Step 2: Candidate Discovery
**Input**: Dining profile.
**Action**: Search Dianping for restaurants matching criteria.
**Filters**:
- Rating 3.5–5.0 (include mid-range; some great finds are under-rated)
- Review count ≥50 (sufficient sample)
- Within radius
- Cuisine match

**Output**: Candidate list (typically 10–30 restaurants).
**Logic**: Deduplicate chain locations unless user prefers them. Track "hidden gems" (high real-review score despite moderate overall rating).

### Step 3: Review Harvesting
**Input**: Candidate restaurant list.
**Action**: Scrape recent reviews (sample ≥30 per restaurant, prioritized by recency).
**Data extracted per review**:
- Rating (overall + sub-scores)
- Text content + length
- Photos (count + metadata)
- Reviewer profile: registration date, review count, follower count, review frequency
- Timestamp

**Output**: Raw review corpus per restaurant.
**Logic**: Respect Dianping rate limits. Cache for 1 hour.

### Step 4: Fake Review Detection (The Differentiator)
**Input**: Review corpus per restaurant.
**Detection signals (multi-dimensional scoring)**:

| Signal | Red Flag Pattern | Weight |
|--------|-----------------|--------|
| Time cluster | ≥5 reviews within 30 min | High |
| Reviewer age | Account <7 days old | High |
| Review frequency | >10 reviews/day across restaurants | Medium |
| Text similarity | High cosine similarity with other reviews | High |
| Photo EXIF | Identical camera/settings across "different" users | Medium |
| Generic language | "环境不错""味道很好" without specifics | Low |
| Rating pattern | All 5-star, no detail | Low |
| Reviewer history | Only 5-star reviews, never critical | Medium |

**Output**: Each review tagged: `genuine | suspicious | likely_fake`. Restaurant scored with authenticity index (0–100).

**Logic**: Ensemble scoring with weighted signals. Flag entire restaurant as "suspicious" if >40% reviews are likely_fake. This is the key differentiator from any existing tool.

### Step 5: Sentiment Extraction (Genuine Reviews Only)
**Input**: Filtered genuine reviews.
**Action**: LLM-based sentiment extraction across 4 dimensions:
- **Taste (口味)**: Dish-specific praise/criticism, freshness, authenticity
- **Environment (环境)**: Noise level, seating comfort, decor, cleanliness
- **Service (服务)**: Wait time, staff attitude, ordering convenience
- **Value (性价比)**: Portion size vs price, "worth it" sentiment

**Output**: Structured sentiment summary per restaurant.

```
=== 老王川菜 (Rating: 4.3, Authenticity: 92%) ===
👍 Taste: Mapo Tofu (must-order, 38 mentions), 回锅肉 (authentic, 25 mentions)
👎 Taste: 水煮鱼 (bland, 7 complaints)
👍 Environment: Cozy but cramped (expect wait at peak)
👎 Service: Slow during dinner rush (12 mentions)
💰 Value: ¥65/person, "great value" (22 mentions vs 3 "overpriced")
```

### Step 6: Personalized Ranking
**Input**: Sentiment summaries + user dining profile.
**Scoring formula**:
```
Score = w1 × cuisine_match + w2 × sentiment_score + w3 × value_score + w4 × occasion_fit + w5 × authenticity_bonus
```

**Output**: Ranked top 5–10 restaurants with:
1. Overall score and breakdown
2. Must-order dishes (top 3)
3. Avoid dishes (top 3)
4. Best time to go (based on wait-time mentions)
5. Occasion-fit note (e.g., "Great for date — quiet corner tables")

### Step 7: Ordering Guide Generation
**Input**: Top-ranked restaurant + dish sentiment data.
**Output**: Ready-to-use ordering card:

```
=== 老王川菜 · 2人点菜指南 ===
预算: ¥120-150

必点 (Must Order):
☑ 麻婆豆腐 ¥28 — 38人推荐，招牌菜
☑ 回锅肉 ¥42 — 25人推荐，正宗

可点 (Recommended):
○ 蒜泥白肉 ¥32 — 18人推荐

避雷 (Skip):
✕ 水煮鱼 ¥88 — 7人评价"不入味"，性价比低

💡 人均参考: ¥60-75
🕐 建议时间: 11:30前或13:30后避开高峰
```

**Logic**: Adjust portion recommendations based on party size. For group dinners, suggest "大份" or double-ordering popular dishes.

### Step 8: Optional — Exploration Route
**Input**: Multiple restaurants worth visiting + starting location.
**Output**: Geographically optimized route:
```
🍽️ 静安寺美食探店路线 (步行可达):
1. 老王川菜 (午餐, 11:30) → 步行3分钟
2. 弄堂小馄饨 (下午茶, 14:00) → 步行5分钟
3. 福1088 (晚餐, 18:00)
```

**Logic**: Group restaurants by proximity clusters. Factor in operating hours (some close between lunch and dinner).

## Sample Prompts

### Prompt 1: Quick Recommendation
**User**: "上海静安寺附近，想吃川菜，人均100左右，约会，推荐3家靠谱的"
**Expected Output**: 3 ranked restaurants with authenticity scores, must-order dishes, date-suitability notes.

### Prompt 2: Suspicious Restaurant Check
**User**: "这家网红店评分4.8但我觉得不好吃，帮我看看评价是不是刷的 —— [Dianping URL]"
**Expected Output**: Fake review detection report: what % of reviews look fake, specific suspicious patterns found, genuine review sentiment summary.

### Prompt 3: Dish-Level Deep Dive
**User**: "今晚去吃XX火锅，帮我看看哪些菜必点，哪些是雷"
**Expected Output**: Detailed ordering guide with specific dish recommendations sourced from genuine reviews.

### Prompt 4: Polarized Restaurant Decoder
**User**: "XX餐厅评分3.8，有人狂推有人狂骂，到底是什么情况？"
**Expected Output**: Analysis of both camps: "5-star reviewers love the authentic taste and value; 1-star reviewers complain about slow service and cramped space. Verdict: go for the food, not the ambiance."

### Prompt 5: Multi-City Explorer
**User**: "下周去成都出差3天，住春熙路附近，帮我规划一个探店路线，要正宗川菜和小吃"
**Expected Output**: 3-day exploration route: lunch + dinner + snack recommendations, geographically clustered, with ordering guides.

### Prompt 6: Group Dinner Planning
**User**: "8个人聚餐，北京国贸附近，预算人均150-200，要有包间，适合聊天的"
**Expected Output**: 5 restaurant options with private room availability notes, group-friendly dish combos, per-person budget breakdown.

## Real Task Examples

### Example 1: Date Night Decision
**Scenario**: User planning a third date, wants to impress without being too formal.
**Input**: "上海法租界附近，人均200-300，约会，氛围好但不要太正式，最好是西餐或日料"
**Steps**:
1. Profile: 法租界, ¥200-300, date, Western/Japanese
2. Discovery → 18 candidates, filtered to 12 after radius check
3. Review harvesting → 360+ reviews across candidates
4. Fake detection → 2 restaurants flagged (>35% suspicious), removed
5. Sentiment: focus on "romantic atmosphere" and "not too noisy"
6. Ranking: Top 5 with "date vibe" score
7. Ordering guides for top 3
**Output**: "Mr & Mrs Bund (authenticity 95%, romantic terrace), 鮨一 (94%, intimate counter seating), Osteria (91%, cozy Italian)"

### Example 2: Tourist in New City
**Scenario**: First time in Chengdu, wants authentic local food, not tourist traps.
**Input**: "刚到成都，住宽窄巷子附近，想吃地道川菜和小吃，避开网红店，人均50-100"
**Steps**:
1. Profile: 宽窄巷子, ¥50-100, solo/casual, authentic
2. Discovery → 25 candidates; immediately filter out 4.8+ perfect scores (tourism red flag)
3. Review harvesting → focus on reviews from accounts with local dining history
4. Fake detection → remove 6 restaurants with review clusters on weekends
5. Sentiment: prioritize "本地人""回头客""老店" mentions
6. "Hidden gem" bonus: moderate rating (3.8-4.3) but strong genuine sentiment
7. Route: 3-restaurant walking route from 宽窄巷子
**Output**: "陈麻婆豆腐 (老字号, 96% authentic), 小谭豆花 (local favorite, ¥30/person), 洞子口张老二凉粉 (street food gem)"

### Example 3: Business Dinner
**Scenario**: Hosting 6 clients, needs upscale private dining with guaranteed quality.
**Input**: "北京朝阳区，商务宴请6人，人均400-600，要有包间，粤菜或淮扬菜，服务要专业"
**Steps**:
1. Profile: 朝阳区, ¥400-600, business, private room, Cantonese/Huaiyang
2. Discovery → filter for "包厢""商务宴请" in tags
3. Review focus: service quality mentions, private room experience
4. Fake detection → high-end restaurants have fewer fake reviews but check for "探店博主" (paid influencer) patterns
5. Sentiment: service quality is weighted 2× for business dining
6. Dish recommendations: banquet-style combos, wine pairing suggestions
7. Booking tips: how far in advance to reserve
**Output**: "利苑酒家 (service excellence, 98% authentic), 大董烤鸭 (impressive presentation, private rooms), 淮扬府 (elegant, excellent service)"

## 🚀 First-Success Path (3 Steps)

1. **Step 1**: Say "推荐上海静安寺附近3家靠谱的川菜馆，人均100左右"
2. **Step 2**: Review the ranked list with authenticity scores and must-order dishes
3. **Step 3**: Pick a restaurant, get the ready-to-use ordering guide with specific dishes

## Boundary Conditions

| Condition | Behavior |
|-----------|----------|
| <50 total reviews for a restaurant | Flag as "insufficient data"; still show but with low-confidence warning |
| All reviews flagged as suspicious | Mark restaurant "⚠️ High fake review risk"; still show genuine sentiment if any |
| User location outside Dianping coverage | Inform; Dianping covers mainland China primarily |
| Cuisine type has <3 candidates | Expand radius or suggest adjacent cuisines |
| Budget too low for area (<¥30/person) | Suggest street food / food court alternatives |
| Restaurant chain with >10 locations | De-duplicate; show 2-3 closest locations |
| Dianping blocks scraping | Fall back to cached data; show staleness timestamp |
| Party size >12 | Suggest banquet/private dining only; filter out small-table venues |
| Occasion = "proposal" or "anniversary" | Add extra weight to environment + service; flag "special occasion" friendly venues |

## Error Handling

| Error Code | Scenario | Handling |
|-----------|----------|----------|
| E-SCRAPE-BLOCKED | Dianping anti-scraping triggers | Use cached data, flag staleness, retry after cooldown |
| E-INSUFFICIENT-REVIEWS | Restaurant has <30 reviews | Show with "low confidence" badge; limit recommendations |
| E-LOCATION-UNKNOWN | Location string can't be resolved | Ask user for district or landmark clarification |
| E-NO-CANDIDATES | Zero restaurants match criteria | Relax filters iteratively: expand radius → budget → cuisine |
| E-FAKE-OVERWHELM | >60% reviews detected as fake | Strong warning; recommend skipping this restaurant |
| E-PHOTO-PARSE-FAIL | Can't extract photo metadata | Degrade gracefully; skip photo-based fake detection signals |

## Security Requirements

- **Review data privacy**: Scraped reviews used for analysis only; never stored beyond session
- **No account impersonation**: All scraping is read-only, public-facing data
- **Dianping ToS compliance**: Respect robots.txt; reasonable rate limiting (1 req/sec)
- **Location privacy**: City/district level only; never store or expose precise coordinates
- **No review manipulation**: This tool reads and analyzes; it does NOT post reviews, boost ratings, or interact with Dianping in any write capacity
- **Fair use**: Analysis results are personal dining decisions; not for commercial competitive intelligence

---

## Implementation

### Project Structure

| File | Purpose |
|------|---------|
| `SKILL.md` | Full design document (this file) |
| `skill.json` | Skill metadata with script/schema references |
| `scripts/dianping-guide.py` | **Main Python CLI** — implements all workflow steps |
| `schemas/input.schema.json` | JSON Schema for dining profile and restaurant data |
| `schemas/output.schema.json` | JSON Schema for all output types (authenticity/sentiment/ranking/ordering/route) |
| `references/signals.json` | Fake review detection signal definitions, weights, and thresholds |

### CLI Usage

```bash
# Step 1: Define dining context
./scripts/dianping-guide.py profile --location "上海静安寺" --cuisine 川菜 --budget-max 100

# Step 2: Discover candidates (uses built-in sample data)
./scripts/dianping-guide.py discover --cuisine 川菜 --budget-max 100

# Step 3+4+5: Analyze a restaurant (fake detection + sentiment)
./scripts/dianping-guide.py analyze "老王川菜"

# Step 6: Personalized ranking
./scripts/dianping-guide.py rank --cuisine 川菜 --occasion date

# Step 7: Ordering guide
./scripts/dianping-guide.py order "老王川菜" --party-size 2

# Step 8: Exploration route
./scripts/dianping-guide.py route --start "静安寺"
```

### Key Algorithms

- **Fake Review Detection**: 8-signal ensemble scoring — time clusters, reviewer age, posting frequency, text similarity (cosine), photo EXIF, generic language, rating patterns, reviewer history. Each signal weighted and normalized to 0-100 authenticity index.
- **Sentiment Extraction**: Chinese keyword-based matching across 4 dimensions (taste/environment/service/value). Dish-level extraction via pattern matching near sentiment keywords.
- **Personalized Ranking**: Weighted formula `0.25×cuisine_match + 0.20×value + 0.20×occasion + 0.30×authenticity_bonus`.
- **Ordering Guide**: Separates dishes into Must-order / Recommended / Skip based on aggregated dish-level sentiment from genuine reviews.

### Dependencies

- **Python 3.8+** (stdlib only — no external packages required)
- `references/signals.json` loaded at runtime for detection thresholds

All analysis uses built-in sample restaurant data. For production use, replace `SAMPLE_RESTAURANTS` with scraped Dianping data (respecting rate limits and robots.txt).
