---
name: a-share-global-peer
description: "Find global peer companies for A-share listed companies. Input an A-share company name or code, automatically match overseas listed companies (US, Europe, Japan, Korea) offering similar products/services, output comparison report with market share data. Triggers when user asks for overseas peer/benchmark, comparing A-share vs global leaders, or keywords like 对标, peer comparison, benchmark."
metadata:
  openclaw:
    requires:
      env:
        - name: TUSHARE_TOKEN
          required: false
          description: "Tushare API token for A-share company data (optional, fallback to Web Search)"
        - name: BRAVE_API_KEY
          required: false
          description: "Brave Search API key (optional, system default available)"
      tools:
        - web_search
        - exec
      skills:
        - ifind-finance-data
        - tushare-data
        - akshare-stock
---

# A-Share Global Peer Matching Tool

## Overview

This skill helps find overseas listed companies that can serve as benchmarks or peers for A-share (Chinese) listed companies. It matches companies based on product/service similarity and provides detailed comparison reports.

## Dependencies

### Required Tools

| Tool | Purpose | Priority |
|------|---------|----------|
| `web_search` | Search for global leaders, market share data | **Required** |
| `exec` | Run Python scripts for data fetching | Required |
| `read` | Read reference files | Optional |

### Optional Skills (Enhancement)

| Skill | Purpose | Benefit |
|-------|---------|---------|
| `ifind-finance-data` | Query A-share company products/financials | Highest accuracy |
| `tushare-data` | A-share company basic info | Structured data |
| `akshare-stock` | A-share market data | Alternative data source |

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `TUSHARE_TOKEN` | Optional | Tushare API token. If not set, falls back to Web Search for company data |
| `BRAVE_API_KEY` | Optional | Brave Search API key. System default available |

**Note**: This skill works without any API keys by using Web Search fallback. API keys enhance data quality but are not mandatory.

### Required Files (Bundled)

| File | Purpose |
|------|---------|
| `scripts/get_company_products.py` | Fetch A-share company product info |
| `references/global_leaders_reference.md` | Quick lookup table for global leaders |

---

## Workflow

### Step 1: Get A-Share Company Product Matrix

**Data Source Priority**: iFinD (if skill available) > Tushare (if token set) > Web Search (always available)

Execute:
```bash
python3 scripts/get_company_products.py --company "<company_name_or_code>" --output json
```

The script automatically:
1. Checks for `TUSHARE_TOKEN` environment variable
2. If available, queries Tushare API
3. If unavailable, returns recommended Web Search queries

Expected output:
- Main products/services (sorted by revenue %)
- Industry classification
- Revenue geography breakdown

**Fallback**: If script unavailable or no API token, use web_search with query:
- `"<公司名> 主营业务 营收构成 2024"`
- `"<公司名> products revenue breakdown"`

---

### Step 2: Search for Global Peer Companies

**Search Strategy**:
1. For each major product, search `"global leader in [product_name]"` or `"[product_name] market share"`
2. Prioritize US-listed companies (data easier to obtain), then Europe, Japan, Korea
3. Use `web_search` tool, label source as "Web Search"

**Selection Criteria**:
- MUST be publicly listed (exclude private companies)
- Prefer highest market share in same product category
- Higher product matrix overlap = higher priority

---

### Step 3: Handle Special Cases

#### Region-Specific Products

When A-share company products have strong regional/Chinese characteristics:
- Find overseas products with similar regional characteristics for analogy
- Examples:
  - Baijiu (白酒) → Whisky leader (Diageo)
  - Chinese condiments → Western condiments (McCormick)
- Mark as "类比对标 (Analogy Benchmark)" and explain logic

#### Diversified Business

When A-share company operates multiple product categories:
- First try to find single overseas company with highest product matrix overlap
- If impossible, benchmark by main product separately
- Example: Xiaomi (phone + IoT) → Apple (phone + IoT ecosystem), not separate benchmarks

---

### Step 4: Get Market Share Data

Search patterns:
```
"[company_name] [product] market share"
"[product] global market share ranking"
"[product] industry leaders 2024"
```

Label all data sources:
- `数据来源: Web Search (YYYY-MM-DD)` 
- `数据来源: iFinD API`
- `数据来源: Tushare API`

---

### Step 5: Output Comparison Report (Chinese)

**Important**: All output reports must be in **Chinese** for user readability.

Output template:

```markdown
## A股公司 vs 海外对标

### A股公司：[公司名] ([股票代码])
- **主营产品**: [产品1] (营收占比 XX%), [产品2] (营收占比 XX%)
- **行业**: [行业分类]
- **地域特色**: [如有则说明]

### 海外对标 1：[公司名] ([股票代码] - [交易所])
- **主营产品**: [产品1] (营收占比 XX%), [产品2] (营收占比 XX%)
- **市场地位**: [描述]
- **市场份额数据**:
  - [产品1] 全球份额: XX% (数据来源: ...)
  - [产品2] 全球份额: XX% (数据来源: ...)

### 海外对标 2：[公司名] ([股票代码] - [交易所])
- **主营产品**: ...
- **市场地位**: ...

### 产品对比

| 产品维度 | A股公司 | 海外对标1 | 海外对标2 |
|---------|---------|----------|----------|
| [维度名] | [数值] | [数值] | [数值] |
| 毛利率 | XX% | XX% | XX% |
| 营收规模 | XX亿 | XX亿 | XX亿 |

### 对标逻辑说明
- [选择这家公司对标的原因]
- [地域特色类比依据，如有]

---
*数据获取时间: YYYY-MM-DD*
```

---

## Examples

### Example 1: CATL (宁德时代)

Input: "宁德时代的海外对标公司"

Workflow:
1. Query CATL main products: EV batteries (~70% revenue)
2. Search "global leader in EV battery"
3. Results: LG Energy Solution, Panasonic, Samsung SDI
4. Get market share data
5. Output Chinese comparison report

### Example 2: Kweichow Moutai (贵州茅台)

Input: "茅台对标哪家海外公司"

Workflow:
1. Identify Moutai products: Baijiu (strong regional characteristic)
2. Search "global leader in spirits"
3. Result: Diageo (whisky leader)
4. Mark as "类比对标: 白酒 vs 威士忌"
5. Output analogy comparison report in Chinese

### Example 3: Innolight (中际旭创)

Input: "中际旭创的海外对标"

Workflow:
1. Query: Optical transceivers (95.9% revenue)
2. Search "global optical transceiver market leader"
3. Results: Coherent, Lumentum
4. **Special finding**: Innolight is already #1 globally!
5. Output competition benchmark report, note leadership position

---

## Resource Files

### scripts/

- `get_company_products.py` - Fetch A-share company product info via Tushare or recommend Web Search fallback

### references/

- `global_leaders_reference.md` - Quick lookup table for global industry leaders

Read reference file to reduce redundant searches:
```markdown
# Quick lookup example
- EV Battery → LG Energy Solution (373220.KRX), Panasonic (6752.TSE)
- Spirits → Diageo (DEO.NYSE), Brown-Forman (BF.A.NYSE)
- Optical Transceiver → Coherent (COHR.NYSE), Lumentum (LITE.NYSE)
```

---

## Data Source Labeling Rules

| Data Type | Label Format |
|-----------|--------------|
| A-share company products | `数据来源: iFinD API` or `数据来源: Tushare API` or `数据来源: Web Search` |
| Overseas company info | `数据来源: Web Search (YYYY-MM-DD)` |
| Market share | `数据来源: Web Search (YYYY-MM-DD)` + search keywords |
| Estimates/speculation | Explicitly label `推测数据，需验证` |

---

## Important Rules

1. **NEVER fabricate data** - All market share figures must come from actual search results
2. **Label uncertainty** - Clearly state when data is incomplete
3. **Max 2 peer companies** - Avoid information overload, select most representative
4. **Prioritize listed companies** - Exclude private companies (e.g., Bosch, Deloitte)
5. **Output in Chinese** - User-facing reports must be in Chinese for readability
6. **Check leadership position** - Some A-share companies may already be global leaders (e.g., Innolight, CATL)
7. **Graceful fallback** - If API tokens unavailable, use Web Search instead of failing

---

## Special Cases Handling

### Case 1: A-Share Company is Global Leader

When A-share company already ranks #1 globally:
- Change framing from "对标学习" to "竞争对标" (competition benchmark)
- Note that overseas companies are competitors, not learning targets
- Focus on competitive dynamics, technology divergence, customer overlap

Example: 中际旭创 (Innolight) surpassed Coherent to become #1 optical transceiver supplier in 2024.

### Case 2: No Direct Global Peer

When no listed overseas company produces exact same product:
- Use analogy benchmarking
- Explain analogy logic clearly
- Note limitations of analogy comparison

Example: 中国中药 → Western herbal supplements (GNC, privatized, limited options)

### Case 3: Multiple Product Categories

When company has diversified business:
- Try to find single comprehensive peer first
- If impossible, benchmark main product only
- Note "多元化经营，仅对标主营业务"

---

## Quality Checklist

Before outputting report, verify:

- [ ] All revenue percentages backed by data sources
- [ ] Market share figures labeled with source
- [ ] Overseas companies confirmed as publicly listed
- [ ] Special cases (regional products, diversified) handled properly
- [ ] Report language is Chinese
- [ ] Data timestamp included
- [ ] If A-share company is global leader, noted in report