---
name: amazon-ads-manager
version: 1.1.0
description: "Manage Amazon Advertising campaigns via the official Advertising API. Read live campaign/keyword/search-term performance, calculate ACOS/ROAS/CTR, identify wasted spend, adjust bids, pause keywords, add negatives. Trigger on: 广告优化, 广告分析, ACOS, 竞价, 投放, 关键词出价, 广告报告, 浪费花费, campaign analysis, ads optimization, keyword bid, sponsored products, 广告表现, 哪些词在烧钱, adjust bid, pause campaign."
---

# amazon-ads-manager

Amazon Advertising API wrapper for live campaign management — read performance reports, update bids, pause keywords, add negatives.

## Setup (one-time)

Create a `.env` file in the skill root directory (same level as this SKILL.md):

```
AMAZON_ADS_CLIENT_ID=amzn1.application-oa2-client.xxx
AMAZON_ADS_CLIENT_SECRET=xxx
AMAZON_ADS_REFRESH_TOKEN=Atzr|xxx
AMAZON_ADS_PROFILE_ID=          # find via `ads.py profiles`
AMAZON_ADS_REGION=NA            # NA | EU | FE
```

**How to get credentials:**
1. [Amazon Ads Developer Console](https://advertising.amazon.com/API/docs/en-us/onboarding/overview) → create app → get client_id + client_secret
2. OAuth flow → get refresh_token (login with your Seller Central account)
3. Run `ads.py profiles` to find your `AMAZON_ADS_PROFILE_ID` (one per marketplace)

> **If credentials are not yet configured:** ask the skill owner (the person who installed this skill) to provide the Amazon Ads API credentials and save them to the `.env` file listed above. Without these, all commands will fail with a clear error message listing exactly which variables are missing.

---

## Commands

### List profiles (find your PROFILE_ID)
```bash
uv run <skill-dir>/scripts/ads.py profiles
```
Returns all linked ad accounts with profileId, marketplace, currency.
Set `AMAZON_ADS_PROFILE_ID` to the correct profileId for subsequent calls.

---

### View campaigns
```bash
# Active campaigns
uv run ... campaigns

# All (including paused)
uv run ... campaigns --state all
```
Returns: campaignId, name, state, budget, bidding strategy.

---

### View ad groups
```bash
uv run ... adgroups <campaign_id>
```

### View keywords
```bash
uv run ... keywords <adgroup_id>
```
Returns: keywordId, keywordText, matchType, state, bid.

---

### Performance reports (async, ~30–90 sec)

```bash
# Campaign-level ACOS/ROAS summary (last 30 days)
uv run ... report campaigns --days 30

# Keyword-level performance
uv run ... report keywords --days 30

# Search terms (harvesting + negation)
uv run ... report searchterms --days 30

# Scope to one campaign
uv run ... report keywords --days 30 --campaign-id 12345678
```

Output fields (enriched): impressions, clicks, cost, attributedSales7d, attributedUnitsOrdered7d, **acos_pct**, **roas**, **ctr_pct**, **cpc**

Sorted by spend descending.

---

### Update keyword bid
```bash
uv run ... set-bid <keyword_id> <new_bid>
# e.g.
uv run ... set-bid 987654321 0.85
```

### Pause / enable / archive keyword
```bash
uv run ... set-state <keyword_id> paused
uv run ... set-state <keyword_id> enabled
```

### Add campaign-level negative keyword
```bash
# Negative exact (default)
uv run ... add-negative <campaign_id> "bad search term"

# Negative phrase
uv run ... add-negative <campaign_id> "irrelevant" --match phrase
```

---

## Optimization Workflow

### Step 1 — Get overview
```bash
uv run ... report campaigns --days 30
```
Flag campaigns with acos_pct > 50% for drill-down.

### Step 2 — Drill into problem campaigns
```bash
uv run ... report keywords --days 30 --campaign-id <id>
```

Classify each keyword:

| Condition | Action |
|-----------|--------|
| spend > $5, sales = 0, clicks ≥ 10 | 🔴 **Pause** — pure waste |
| acos_pct > target × 1.5, clicks ≥ 20 | 🟠 **Reduce bid** by 20–30% |
| acos_pct > 0, acos_pct < target, impressions < 500 | 🟡 **Raise bid** by 20% |
| ctr_pct > 0.5%, orders/clicks < 5% | 🟡 **Listing problem** — don't touch bid |
| impressions = 0 | Check match type / bid floor |

**Target ACOS benchmarks**: SP Manual 25–35% · SP Auto 35–45% · SB 40–55%

### Step 3 — Harvest search terms
```bash
uv run ... report searchterms --days 30
```

From auto campaigns:
- `acos_pct < target AND clicks ≥ 5 AND sales > 0` → add to manual exact at 80% of current auto bid
- `spend > $3 AND sales = 0 AND clicks ≥ 8` → add as negative exact

### Step 4 — Execute changes
For each action identified, run the appropriate command (`set-bid`, `set-state`, `add-negative`).
Present a summary of what was changed and the expected impact.

---

## Output Format

After analysis, present:

```
## 广告优化报告

### 账户概览 (最近 N 天)
| 总花费 | 总销售额 | ACOS | ROAS | 点击数 | 平均 CPC |
|--------|---------|------|------|--------|---------|

### 🔴 高优先级 — 建议暂停 (X 个词，节省 $X/月)
| Campaign | Ad Group | Keyword | 花费 | 点击 | 销售 | 操作 |

### 🟠 降价建议 (X 个词)
| Keyword | 当前 bid | 建议 bid | 当前 ACOS | 目标 ACOS |

### 🟢 收割词 — 建议加入 Manual (X 个词)
| 搜索词 | Auto 花费 | ACOS | 建议 bid |

### 执行摘要
已执行 / 等待确认 X 项操作
```

Always ask for confirmation before executing bid changes or pauses unless the user explicitly said "直接执行" or "just do it".
