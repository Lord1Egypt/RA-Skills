---
name: china-export-data
description: Access aggregated China export trade statistics sourced from China General Administration of Customs public data (stats.customs.gov.cn), compiled and served via doumaotong.com REST API. Provides 5 endpoints for querying export metrics by HS code, destination country, monthly trends, product rankings, and 2-year historical records. Suitable for baseline market research and trade data reference.
---

# China Export Data

**Purpose**: Provide programmatic access to China export trade statistics sourced from the public data of China General Administration of Customs (http://stats.customs.gov.cn), compiled and aggregated by doumaotong.com for research, market baseline analysis, and trade data reference.

**Target Users**: Researchers, analysts, students, small business owners, and anyone needing factual China export data for reference purposes.

**Data Provenance**: 
- **Source**: Public export statistics published by China General Administration of Customs — http://stats.customs.gov.cn/
- **Aggregation**: Data is compiled, structured, and served by doumaotong.com (independent third-party platform)
- **Relationship**: This SKILL does not connect directly to customs systems; it queries pre-aggregated tables derived from official customs monthly bulletins
- **Typical lag**: 1-2 months behind official customs release
- **Verification**: For authoritative primary data, access directly via http://stats.customs.gov.cn/indexEn or UN Comtrade

---

## REST API Endpoints

The following 5 API endpoints provide programmatic access to pre-aggregated China export data compiled from customs statistics. All responses are JSON format with `code` and `data` fields.

**Base URL**: `https://doumaotong.com`

**Authentication**: No API keys, tokens, or login credentials are required for current endpoints. Open access with standard HTTP GET requests.

**Privacy Notice**: Query parameters including HS codes, country codes, and request timestamps are transmitted to doumaotong.com servers. No personal identification data is collected.

---

### API-1: Product Export Dashboard

**Endpoint**: `GET /skill/dashboard`

**Description**: Returns core business metrics for a given HS code over the most recent 12 months. Based on the pre-aggregated `hs_base_metrics` table compiled from customs data, single-index query, extremely fast.

**Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `hsCode` | string | Yes | HS product code (8-digit) |
| `currentMonth` | string | No | Data month in YYYYMM format. Defaults to latest available month |

**Example Request**:
```
GET /skill/dashboard?hsCode=85171200
GET /skill/dashboard?hsCode=85171200&currentMonth=202503
```

**Response Fields**:

| Field | Type | Description |
|-------|------|-------------|
| `hsCode` | string | Queried HS code |
| `productName` | string | Product name in Chinese |
| `currentMonth` | integer | Data month (YYYYMM) |
| `recent12mGlobalTotal` | decimal | Total export value over recent 12 months (RMB) |
| `prev12mGlobalTotal` | decimal | Total export value over previous 12 months (RMB) |
| `yoyGrowthRate` | decimal | Year-over-year growth rate (%) |
| `momGrowthRate` | decimal | Month-over-month growth rate (%) |
| `activeCountriesCount` | integer | Number of countries with export records |
| `monthlyActivityCount` | integer | Number of months with exports in recent 12 months |
| `top3ConcentrationPercent` | decimal | Top 3 market concentration (%) |
| `avgCountryActiveMonths` | decimal | Average active months per country |
| `firstUnit` / `firstQuantity` | string/long | First measurement unit and total quantity |
| `secondUnit` / `secondQuantity` | string/long | Second measurement unit and total quantity |
| `regionBreakdown` | object | Regional distribution with `asiaTotal/Percent`, `europeTotal/Percent`, `africaTotal/Percent`, `northAmericaTotal/Percent`, `southAmericaTotal/Percent`, `oceaniaTotal/Percent` |
| `tradeBlocBreakdown` | object | Trade bloc distribution with `middleEastTotal/Percent`, `beltRoadTotal/Percent`, `aseanTotal/Percent`, `euTotal/Percent`, `usmcaTotal/Percent` |

---

### API-2: Target Market Analysis

**Endpoint**: `GET /skill/markets`

**Description**: Lists all destination countries for a given HS code, sorted by export value. Based on `hs_count_month` table compiled from customs data, returns only pre-computed fields (no cross-period real-time calculation).

**Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `hsCode` | string | Yes | HS product code |
| `sortBy` | string | No | Sort field: `amount` (12-month total, default) or `name` (country name) |
| `order` | string | No | Sort direction: `asc` or `desc` (default) |
| `minAmount` | number | No | Minimum export amount threshold to filter micro-trade countries |
| `limit` | integer | No | Number of results to return (default: 50) |

**Example Request**:
```
GET /skill/markets?hsCode=85171200
GET /skill/markets?hsCode=85171200&sortBy=amount&order=desc&minAmount=1000000&limit=20
```

**Response Fields** (per market entry):

| Field | Type | Description |
|-------|------|-------------|
| `countryName` | string | Country name in Chinese |
| `countryCode` | string | Country code |
| `continent` | string | Continent name |
| `tradeTags` | array | Trade tags, e.g. `["一带一路", "东盟"]` |
| `recent12mTotal` | double | Recent 12-month export total (from `12monthtotal` field) |
| `monthlyAvg` | double | Monthly average (12monthtotal / 12) |
| `threeYearCAGR` | double | 3-year compound annual growth rate (%) from `3yearup` field |

---

### API-3: Monthly Trend Tracking

**Endpoint**: `GET /skill/trend`

**Description**: Returns the monthly export amount trend for a specific HS code to a specific country over the most recent 12 months. Fixed time range, no dynamic column name construction, cache-friendly.

**Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `hsCode` | string | Yes | HS product code |
| `countryCode` | string | Yes | Country code (3-digit numeric, e.g. 101 for Afghanistan) |

**Example Request**:
```
GET /skill/trend?hsCode=85171200&countryCode=502
```

**Response Fields**:

| Field | Type | Description |
|-------|------|-------------|
| `hsCode` | string | Queried HS code |
| `countryName` | string | Country name in Chinese |
| `countryCode` | string | Country code |
| `currencyUnit` | string | Always "人民币" |
| `monthlyData` | array | Fixed 12 entries, each with `month` (YYYYMM) and `amount` |

---

### API-4: Top Products & Growth Ranking

**Endpoint**: `GET /skill/topProducts`

**Description**: Discover products with rapid recent growth or massive volume based on the `hs_base_metrics` table compiled from customs data (only ~25,000 rows, fast query).

**Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sortBy` | string | No | Sort logic: `growth` (YoY growth, default), `amount` (total), `marketBreadth` (active countries) |
| `regionFilter` | string | No | Region filter: `asia`, `europe`, `africa`, `northAmerica`, `southAmerica`, `oceania`, `middleEast`, `beltRoad`, `asean`, `eu` |
| `minAmount` | number | No | Minimum total export threshold (default: 10,000,000 RMB) |
| `maxConcentration` | number | No | Maximum market concentration %, no limit by default |
| `limit` | integer | No | Results per page (default: 30, max: 100) |
| `offset` | integer | No | Pagination offset (default: 0) |

**Example Request**:
```
GET /skill/topProducts
GET /skill/topProducts?sortBy=growth&regionFilter=asia&minAmount=5000000&limit=20
```

**Response Fields** (per product):

| Field | Type | Description |
|-------|------|-------------|
| `rank` | integer | Ranking number |
| `hsCode` | string | HS product code |
| `productName` | string | Product name |
| `recent12mGlobalTotal` | decimal | Total export value |
| `yoyGrowthRate` | decimal | Year-over-year growth rate |
| `activeCountriesCount` | integer | Number of active countries |
| `top3ConcentrationPercent` | decimal | Top 3 market concentration |
| `bestRegion` | object | Best performing region with `regionName` and `percent` |
| `momentumScore` | double | Composite momentum score |

---

### API-5: Historical Export Records (2-Year Detail)

**Endpoint**: `GET /skill/history`

**Description**: Returns the most recent 24 months of monthly export amount detail and annual summaries for a specific product-country combination. Only amount columns are retrieved (no growth columns), fixed 24-month range.

**Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `hsCode` | string | Yes | HS product code (8-digit) |
| `countryCode` | string | Yes | Country code (3-digit numeric, e.g. 101) |

**Example Request**:
```
GET /skill/history?hsCode=85171200&countryCode=502
```

**Response Fields**:

| Field | Type | Description |
|-------|------|-------------|
| `hsCode` | string | Queried HS code |
| `countryCode` | string | Country code |
| `countryName` | string | Country name in Chinese |
| `currentDataMonth` | string | Latest data month (YYYYMM) from `current_month` field |
| `yearlySummary` | array | Recent 2 complete yearly summaries, each with `year` and `totalAmount` |
| `monthlyDetail` | array | 24 monthly entries (newest first), each with `month` (YYYYMM) and `amount` |
| `summaryStats` | object | Summary statistics (see below) |

**`summaryStats` Fields**:

| Field | Type | Description |
|-------|------|-------------|
| `total24MonthAmount` | double | Cumulative 24-month export total |
| `monthlyAvg` | double | Monthly average |
| `maxMonth` | object | Peak month with `month` and `amount` |
| `minMonth` | object | Lowest month with `month` and `amount` |
| `activeMonthsCount` | integer | Number of months with export records in 24 months |

**Error Handling**:
- If `hsCode` + `countryCode` combination has no records: returns 404 with message "该商品对此国家暂无出口记录"
- If a month has no export record, `amount` returns 0

---

## Access Logging

All 5 API endpoints automatically log each access to the `hs_skill_access_log` table with:
- `id`: UUID
- `ip`: Client IP address
- `path`: API path accessed
- `par`: Request parameters
- `create_time`: Auto-generated timestamp

---

## Official Data Sources for Verification

### Source 1: China Customs Statistics (Primary Source of This Data)

**Website**: http://stats.customs.gov.cn/indexEn

**What it contains**:
- Official export statistics from China's General Administration of Customs
- More granular data than UN Comtrade
- Port-level breakdowns
- Trade mode classifications
- Domestic destination information

**Best for**:
- Most authoritative China-specific data
- Port and regional analysis within China
- Recent monthly data (1-2 month lag)
- Detailed product classifications

**Navigation Guide**:

```
English Interface Navigation:

Home (http://stats.customs.gov.cn/indexEn)
├── Query by HS Code
│   ├── Select Year/Month
│   ├── Select HS Code (Chapter → Heading → Subheading)
│   ├── Select Trade Flow (Export/Import)
│   └── Select Filters (optional)
├── Query by Country/Region
│   ├── Select Partner Country
│   ├── Select Time Period
│   └── Select Product Category
└── Query by Customs Port
    ├── Select Port
    ├── Select Time Period
    └── Select Product/Partner
```

### Source 2: UN Comtrade Database

**Website**: https://comtradeplus.un.org/

**What it contains**:
- China's exports reported to the UN by partner countries
- Mirror data (what partner countries report importing from China)
- Global coverage with standardized HS codes
- Historical data from 1962 to present

**Best for**:
- Comparing China with other exporting countries
- Analyzing China's exports to specific destination markets
- Long-term historical trend analysis
- Cross-country benchmarking

**Access methods**:

| Method | URL | Requirements | Best For |
|--------|-----|--------------|----------|
| Web Interface | https://comtradeplus.un.org/lab?r=156 | Free | One-off queries |
| API | https://comtradeapi.un.org/docs/v1 | Registration + API key | Automated queries |
| Bulk Download | Premium subscription | Paid subscription | Large datasets |

**API Registration**:
1. Visit https://uncomtrade.org/docs/api-subscription-keys/
2. Create account
3. Request API key for "comtrade - v1" (free tier: 100 calls/hour)
4. Premium tier available for unlimited access

---

## How to Query Data

### Step-by-Step: China Customs Web Query (Primary Source)

```
Step 1: Access English Interface
→ Go to http://stats.customs.gov.cn/indexEn

Step 2: Choose Query Type
→ "Query by HS Code" for product-focused search
→ "Query by Country/Region" for market-focused search
→ "Query by Customs Port" for logistics analysis

Step 3: Set Parameters
For HS Code Query:
→ Select Year and Month (or range)
→ Click HS Code selector
   • Expand chapters (01-97)
   • Select 2-digit chapter
   • Select 4-digit heading
   • Select 6-digit subheading (optional)
→ Select Trade Flow: "Export"
→ Apply additional filters (optional):
   • Trade Mode (General, Processing, etc.)
   • Customs Port
   • Domestic Destination
   • Transport Mode

Step 4: Execute Query
→ Click "Query" button
→ Wait for results (may take 10-30 seconds)

Step 5: Review Results
→ Table shows: HS Code, Description, Unit, Quantity, Value
→ Click column headers to sort
→ Use pagination for large result sets

Step 6: Export Data
→ Click "Export" or download icon
→ Choose format (Excel/CSV)
→ Save to local drive
```

### Step-by-Step: UN Comtrade Web Query

```
Step 1: Access Query Builder
→ Go to https://comtradeplus.un.org/lab?r=156
   (Pre-filtered for China as reporter)

Step 2: Select Trade Flow
→ Click "Flow" dropdown
→ Select "Exports" (or "Re-exports" if needed)

Step 3: Select Partner Country
→ Click "Partner" field
→ Search and select destination country
→ Or select "All" for global exports

Step 4: Select Product (HS Code)
→ Click "Commodity Code" field
→ Choose classification level:
   • HS 2-digit (broad category, e.g., "84 - Machinery")
   • HS 4-digit (specific heading)
   • HS 6-digit (detailed subheading)
→ Enter or select code

Step 5: Select Time Period
→ Choose "Year" (single or range)
→ For monthly data, select specific months

Step 6: Run Query
→ Click "Preview" for quick view
→ Click "Download" for CSV/Excel export

Step 7: Interpret Results
Columns explained:
• Reporter: Exporting country (China)
• Partner: Importing country
• Trade Value (USD): Export value in US dollars
• Netweight (kg): Quantity in kilograms
• Quantity: Alternative unit (if applicable)
```

---

## Data Dictionary

### Common Fields Explained

| Field | Description | Example |
|-------|-------------|---------|
| **HS Code** | Harmonized System product classification | 8517.12 (Phones) |
| **Trade Value** | Export value in US dollars | $1,234,567 |
| **Netweight** | Weight in kilograms | 50,000 kg |
| **Quantity** | Product-specific unit (if different from kg) | 10,000 units |
| **Trade Flow** | Direction of trade (Export/Import/Re-export) | Export |
| **Reporter** | Country reporting the data | China |
| **Partner** | Trading partner country | United States |
| **Customs Port** | Chinese port of departure | Shanghai |
| **Trade Mode** | Type of trade arrangement | General Trade |

### HS Code Structure

```
HS Code Hierarchy Example (Electronics):

85          ← Chapter (2-digit): Electrical machinery
  ↓
8517        ← Heading (4-digit): Telephone sets
  ↓
8517.12     ← Subheading (6-digit): Phones for cellular networks
  ↓
8517.12.00  ← Full code (8-digit): Detailed classification

Where to find HS codes:
• https://www.trade.gov/harmonized-system-hs-codes
• https://www.foreign-trade.com/reference/hscode.htm
• China Customs website HS code lookup
```

---

## Data Reliability & Limitations

### Update Schedule

| Source | Frequency | Typical Lag | Coverage |
|--------|-----------|-------------|----------|
| China Customs (Primary) | Monthly | 1-2 months | China only |
| UN Comtrade | Monthly | 1-3 months | 200+ countries |
| doumaotong.com (This API) | Monthly | 1-2 months (after customs release) | Aggregated from customs data |

### Known Limitations

| Limitation | Explanation | Workaround |
|------------|-------------|------------|
| Third-party aggregation | This API queries doumaotong.com, which compiles data from public customs bulletins — not a direct government connection | Verify critical figures against stats.customs.gov.cn |
| Mirror data discrepancies | Partner countries may report different values | Compare both sources, use as range |
| Confidential data suppression | Some transactions not disclosed | Use aggregated categories |
| HS code revisions | Codes change every 5 years | Use concordance tables for historical comparison |
| Transshipment goods | Goods passing through China may be included | Filter by trade mode when possible |

### Disclaimer

This SKILL provides aggregated trade data for **reference and research purposes only**. The underlying source is the public data published by China General Administration of Customs (http://stats.customs.gov.cn/), compiled and served by doumaotong.com. For legally binding or high-stakes business decisions, always verify directly with China Customs or UN Comtrade.

---

## Quick Reference Card

```
┌────────────────────────────────────────────────────────────┐
│              CHINA EXPORT DATA - QUICK ACCESS              │
├────────────────────────────────────────────────────────────┤
│ PRIMARY SOURCE                                             │
│ China Customs: stats.customs.gov.cn/indexEn               │
│ Best for: Authoritative official data, port details          │
├────────────────────────────────────────────────────────────┤
│ REST API ENDPOINTS (Aggregated via doumaotong.com)         │
│ Dashboard:    GET /skill/dashboard?hsCode=XXXX             │
│ Markets:      GET /skill/markets?hsCode=XXXX               │
│ Trend:        GET /skill/trend?hsCode=X&countryCode=Y      │
│ Top Products: GET /skill/topProducts                       │
│ History:      GET /skill/history?hsCode=X&countryCode=Y    │
├────────────────────────────────────────────────────────────┤
│ UN COMTRADE                                                │
│ URL: comtradeplus.un.org                                   │
│ Best for: Global comparison, historical data               │
│ API: 100 calls/hour (free)                                 │
├────────────────────────────────────────────────────────────┤
│ HS CODE LOOKUP                                             │
│ trade.gov/harmonized-system-hs-codes                       │
│ foreign-trade.com/reference/hscode.htm                     │
└────────────────────────────────────────────────────────────┘
```

---

## Output Formats

When retrieving data, you can typically export as:

| Format | Extension | Best For |
|--------|-----------|----------|
| CSV | .csv | Data analysis in Excel, Python, R |
| Excel | .xlsx | Presentation, sharing with stakeholders |
| JSON | .json | API integration, web applications |
| PDF | .pdf | Reports, documentation |

**Recommended**: CSV for analysis, Excel for sharing
