---
name: amazon-serp-analysis
version: 1.0.1
description: "Analyze Amazon market tracks/niches for go/no-go investment decisions. Given a seed keyword, scrapes SERP, expands related keywords to map the full track landscape, scores competition intensity, estimates demand, and delivers a structured recommendation with entry strategy. Trigger on: 赛道分析, 赛道研究, 值不值得做, 市场分析, 竞争分析, niche analysis, track analysis, 亚马逊赛道, 切入点, 要不要做这个品, 这个类目怎么样."
---

# amazon-serp-analysis

Comprehensive Amazon niche analysis pipeline. Input: a seed keyword. Output: full track landscape map, competition scoring, demand assessment, and go/no-go recommendation with specific entry angles.

## Requirements

- `omni-scraper` skill installed and configured (required — provides SERP + PDP data)
- `amazon-listing-judge` skill installed (optional — adds listing quality depth)
- SellerSprite MCP tools (optional — adds keyword volume and search trends)
- ClickHouse MCP (optional — adds historical brand analytics data)

---

## Workflow

### Step 1 — Seed SERP Scrape

Scrape Amazon search results for the seed keyword:

```bash
curl -s -X POST "$CLAW_API_BASE/api/scrape" \
  -H "Content-Type: application/json" \
  -d '{
    "claw_key": "'"$CLAW_KEY"'",
    "url": "https://www.amazon.com/s?k=KEYWORD_URL_ENCODED",
    "mode": "scraper"
  }'
```

From the response `parsed.results`, extract for each position:
- `position`, `asin`, `title`, `price`, `rating`, `review_count`, `bought_past_month`, `sponsored`, `ac_badge`

**Stop if**: `parsed` is null and `body` is also null — report error and stop.

---

### Step 2 — Keyword Expansion (build track landscape)

Goal: identify 5–10 related search terms that form the full track.

**If SellerSprite MCP is available**, use it to expand keywords:
```
mcp__sellersprite-mcp__keyword_miner  { keyword: "<seed>", marketplace: "US" }
mcp__sellersprite-mcp__traffic_extend { keyword: "<seed>", marketplace: "US" }
```
Take the top 5–8 related keywords by search volume.

**Fallback (no SellerSprite)**: Infer related keywords from SERP titles by:
1. Extracting noun phrases and modifiers from the top 10 product titles
2. Identifying variant terms (material, size, use-case, audience)
3. Generating 5–8 plausible search terms that a buyer might use
4. Label these as "inferred" in the output

**If ClickHouse MCP is available**, check brand analytics trend data:
```sql
SELECT search_term, SUM(clicks) as total_clicks
FROM amazon.brand_analytics
WHERE search_term ILIKE '%<seed>%'
  AND date >= today() - INTERVAL 90 DAY
GROUP BY search_term
ORDER BY total_clicks DESC
LIMIT 10
```
This validates which related terms have real search volume.

---

### Step 3 — Scrape 1–2 Key Related Keywords

Pick the 2 highest-volume related keywords from Step 2 and scrape their SERPs (same curl as Step 1). This reveals:
- Whether the same products dominate multiple related SERPs (brand lock)
- Price and review patterns across the broader track

**Token budget**: If context is getting long, skip this step and note it was skipped.

---

### Step 4 — Deep-dive Top 5 Organic Products

For the top 5 non-sponsored products from the seed keyword SERP:

**If `amazon-listing-judge` is available**:
```bash
uv run <amazon-listing-judge-skill-dir>/scripts/grade.py <ASIN>
```
Record the total score and key weaknesses.

**Fallback**: Use the SERP data already collected. Estimate listing quality as:
- High (>80): has AC/BS badge + ≥4.5 stars + ≥1K reviews + bought_past_month
- Medium (55-80): has some but not all signals
- Low (<55): no badges, low reviews, no sales velocity signal

---

### Step 5 — Competition Scoring

Calculate the following metrics from collected data:

#### 5a. Review Barrier
```
avg_reviews = average review count of top 10 organic results
```
- < 200 reviews avg → **Low barrier** (🟢 +2)
- 200–1,000 → **Medium barrier** (🟡 +1)
- 1,000–3,000 → **High barrier** (🔴 0)
- > 3,000 → **Very high barrier** (🔴 -1)

#### 5b. Brand Concentration
```
count unique brands in top 10 organic results
```
- 8–10 unique brands → **Fragmented** (🟢 +2)
- 5–7 unique brands → **Moderate** (🟡 +1)
- 3–4 unique brands → **Concentrated** (🔴 0)
- 1–2 brands dominating 5+ spots → **Locked** (🔴 -1)

#### 5c. Demand Signals
Count how many of the top 10 organic results have "bought in past month" badge:
- 6–10 products → **Hot track** (🟢 +2)
- 3–5 products → **Active** (🟡 +1)
- 0–2 products → **Low demand or seasonal** (🔴 0)

#### 5d. Listing Quality Gap
Average listing quality score of top 5 organic products:
- Average score < 60 → **Big quality gap** (🟢 +2, easy to outcompete)
- 60–75 → **Some gap** (🟡 +1)
- > 75 → **Well-optimized** (🔴 0)

#### 5e. Price Range Health
```
min_price = lowest price among top 10
max_price = highest price among top 10
range_ratio = max_price / min_price
```
- ratio > 3 → **Wide range, room to position** (🟢 +1)
- ratio 1.5–3 → **Moderate** (🟡 0)
- ratio < 1.5 → **Commodity, price war risk** (🔴 -1)

#### Competition Score Total (max 9)
```
competition_score = sum of all sub-scores above
```
- 7–9 → 🟢 **Low competition — favorable**
- 4–6 → 🟡 **Moderate — conditional entry**
- 0–3 → 🔴 **High competition — difficult**

---

### Step 6 — Track Demand Score

Estimate overall demand level:

**If SellerSprite available**: use `traffic_keyword_stat` for monthly search volume.

**From SERP signals**:
- Count products with "bought in past month" → quantify total estimated monthly units
- Estimate: if avg = "1K+" per product × 10 products = ~10K monthly units in track
- Note: this is a rough lower bound estimate

Seasonal flags:
- If keyword contains holiday/event terms, flag as seasonal
- If ClickHouse shows <3 months of search history, flag as trend/fad

---

### Step 7 — Synthesis & Recommendation

#### Entry Assessment Matrix

| Factor | Your Score | Implication |
|--------|-----------|-------------|
| Competition score | X/9 | |
| Demand level | High/Med/Low | |
| Price positioning room | Yes/No | |
| Listing quality gap | Yes/No | |

#### Verdict

🟢 **GO** — competition_score ≥ 7 AND demand ≥ Medium
🟡 **CONDITIONAL** — competition_score 4–6 OR strong demand with one differentiator
🔴 **NO-GO** — competition_score ≤ 3 OR demand Low with high barrier

#### Entry Angle Candidates (pick the best fit)

1. **Price disruption**: If top products cluster at $20+, enter at $12–15 with comparable quality
2. **Listing quality gap**: If top listings score < 65, win on listing optimization alone
3. **Underserved variant**: If SERP titles share one attribute, find the missing variant buyers search for
4. **Bundle/differentiation**: If all products are standalone, add accessories or improved feature
5. **Niche long-tail**: If main keyword is crowded, target the highest-volume related term with lower competition

---

## Output Format

Present the full analysis in this structure:

```
## 🔍 赛道分析：{seed_keyword}

### 赛道全貌
- **关键词组**: [seed] + [related1], [related2], ... (数据来源: SellerSprite/推断)
- **价格带**: $X–$Y，主力区间 $A–$B
- **市场容量估算**: 约 X 万月销量（基于月销标信号）

### 📊 SERP 竞品概览（前10有机结果）
| 排名 | ASIN | 标题(简) | 价格 | 评分 | 评论数 | 月销 | 徽章 |
|------|------|---------|------|------|--------|------|------|
...

### ⚔️ 竞争强度评分：X/9 — 🟢/🟡/🔴
| 维度 | 得分 | 说明 |
|------|------|------|
| 评论壁垒 | | 平均 X 条 |
| 品牌集中度 | | X 个独立品牌 |
| 需求热度 | | X/10 产品有月销标 |
| Listing 质量差距 | | 头部均分 X/100 |
| 价格带健康度 | | 区间比 X |

### 🔥 赛道热度
- 需求水平: High/Med/Low
- 季节性: 是/否
- 趋势信号: ...

### 🎯 结论

**裁定**: 🟢 GO / 🟡 有条件进入 / 🔴 NO-GO

**最佳切入点**: ...

**建议策略**:
1. ...
2. ...

**风险提示**: ...
```

---

## Data Source Labels

Always label where each data point comes from:
- `[omni-scraper]` — from SERP/PDP scrape
- `[SellerSprite]` — from SellerSprite MCP
- `[ClickHouse]` — from brand analytics DB
- `[inferred]` — LLM reasoning from available data

If a tool was unavailable, explicitly state: "SellerSprite not available — keyword volume data omitted."
