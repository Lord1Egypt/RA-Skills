# Reverse Lookup Workflow

**Question pattern:** "What does Company X actually do?" / "Company X just IPO'd — where do they fit?"

## Step 1: Identify the company

Determine: company name (in all languages), country, stock ticker, exchange.

## Step 2: Check entity databases

Read the relevant entities file. If the company is already cataloged, report what we know.

## Step 3: If not in entities, investigate

1. **Search DART/EDINET/MOPS/cninfo** for the company's own filings — read their 사업의 내용 (KR) / 事業の内容 (JP) / business description section
2. **Search industry press** for the company name in the relevant language
3. **Search patent databases** for the company as patent applicant — what IPC/CPC codes do they file in?
4. **Search SEMICON exhibitor lists** — what category did they exhibit in?
5. **Check chemical registrations** (K-REACH/ECHA) — what chemicals do they register?
6. **Check their IR/investor relations page** — product portfolio, customer list, revenue breakdown
7. **Read Korean/Japanese/Chinese broker research** via Naver Finance / Kabutan / EastMoney

## Multilingual Search Queries

### Korean (회사 조사):
```
[회사명] 사업 개요                → "[company] business overview"
[회사명] 주요 제품                → "[company] main products"
[회사명] 반도체 소재              → "[company] semiconductor materials"
[회사명] 고객사                   → "[company] customers"
[회사명] 매출 구조                → "[company] revenue structure"
[회사명] IPO 공모                 → "[company] IPO offering"
```

### Japanese (会社調査):
```
{会社名} 事業内容                 → "[company] business description"
{会社名} 主要製品                 → "[company] main products"
{会社名} 半導体材料               → "[company] semiconductor materials"
{会社名} 主要販売先               → "[company] major customers"
{会社名} 会社概要                 → "[company] company overview"
{会社名} 上場                     → "[company] listing/IPO"
```

### Chinese — Mainland (公司调研):
```
[公司名] 主营业务                 → "[company] main business"
[公司名] 产品介绍                 → "[company] product introduction"
[公司名] 半导体材料               → "[company] semiconductor materials"
[公司名] 主要客户                 → "[company] major customers"
[公司名] 招股说明书               → "[company] IPO prospectus"
[公司名] 行业地位                 → "[company] industry position"
```

### Chinese — Taiwan (公司調查):
```
[公司名] 主要業務                 → "[company] main business"
[公司名] 產品介紹                 → "[company] product introduction"
[公司名] 半導體材料               → "[company] semiconductor materials"
[公司名] 主要客戶                 → "[company] major customers"
[公司名] 月營收                   → "[company] monthly revenue"
[公司名] 供應鏈 定位              → "[company] supply chain positioning"
```

## Step 3b: Counterfactual check on positioning

Before mapping to taxonomy, run the [Counterfactual Consistency Check](counterfactual-check.md). The key question for reverse lookups: "If this company doesn't actually serve semiconductor fabs, what else could these signals mean?" A company filing CMP-related patents might sell to equipment makers, not fabs. A company exhibiting at SEMICON might be targeting display, solar, or LED customers.

## Step 4: Map to supply chain taxonomy

Place the company in the semiconductor supply chain:
- What layer? (materials → equipment → components → packaging → test)
- What sub-category? (precursors, gases, wet chemicals, photoresist, wafers, targets, CMP, ceramic parts, substrates, etc.)
- Who are their customers? (fabs, equipment OEMs, OSATs)
- Who are their competitors? (domestic and international)
- What's their approximate market position? (share, revenue, tier)
