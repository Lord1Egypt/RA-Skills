# Data Sources & API Reference

> Tier 1: Filing Sources (EDINET, Comtrade, OpenDART, e-Stat, KIPRIS, Lens.org) | Tier 2: Web Search | Tier 3: Financial Aggregators | Tier 4: Chemical/Trade DBs | Tier 5: Conference Exhibitors

API endpoints, company codes, and database structures are subject to change.
Test each key and endpoint before assuming data availability. If a source below
doesn't work, fall back to WebSearch and note it in the search log.

## Tier 1 — Primary Filing Sources

### EDINET (Japan) — Web Search Only

EDINET hosts Japanese company annual securities reports (有価証券報告書). The API requires a
Subscription-Key and the viewer site (GeneXus framework) cannot be scraped programmatically.

**How to access:** Use WebSearch to find filings. Search for the company name + 有価証券報告書:
- `"信越化学工業" 有価証券報告書 主要仕入先` → finds Shin-Etsu's supplier disclosures
- `"東京エレクトロン" 有価証券報告書 主要販売先` → finds TEL's major customer disclosures
- `"{company_name_jp}" EDINET site:disclosure2.edinet-fsa.go.jp` → finds filings on the viewer

**Key filing sections to search for:**
- 主要仕入先 (major suppliers)
- 主要販売先 (major customers >10% revenue)
- 事業等のリスク (business risks — often disclose supplier dependency)
- 関連当事者 (related parties)

**EDINET codes for semiconductor companies** (use as search terms):
- Shin-Etsu Chemical: E00729 (4063.T)
- SUMCO: E02336 (3436.T)
- Tokyo Electron: E01972 (8035.T)
- JSR: E00768 (was 4185.T, now private)
- TOK: E00772 (4186.T)
- Stella Chemifa: E02467 (4109.T)
- Resonac: E00770 (4004.T)

---

### UN Comtrade — Free key (500 req/day)
- **URL:** `https://comtradeapi.un.org/data/v1/get/C/A/HS`
- **Registration:** https://comtradeplus.un.org → create account → subscribe to free tier
- **Header:** `Ocp-Apim-Subscription-Key: $COMTRADE_API_KEY`

```bash
# Japan → Korea, HS 3818 (silicon wafers/doped chemicals), annual 2023
curl -s -H "Ocp-Apim-Subscription-Key: $COMTRADE_API_KEY" \
  "https://comtradeapi.un.org/data/v1/get/C/A/HS?reporterCode=392&partnerCode=410&period=2023&cmdCode=3818&flowCode=X"

# All semiconductor equipment (8486) exports from Netherlands (ASML)
curl -s -H "Ocp-Apim-Subscription-Key: $COMTRADE_API_KEY" \
  "https://comtradeapi.un.org/data/v1/get/C/A/HS?reporterCode=528&period=2023&cmdCode=8486&flowCode=X"
```

**Country codes:** Japan=392, Korea=410, USA=840, China=156, Taiwan=490 (listed as "Other Asia, nes" in UN system), Netherlands=528, Germany=276
**Key HS codes:** 3818 (wafers/doped chemicals), 3707 (photoresists), 8486 (semiconductor equipment), 2811.11 (HF), 2529.21 (fluorspar), 2804.61 (polysilicon)

---

### OpenDART (Korea) — Free key (10K req/day, needs KR phone)
- **URL:** `https://opendart.fss.or.kr/api/`
- **Registration:** https://opendart.fss.or.kr → 회원가입 → 인증키 신청
- **Key sections in filings:** 주요 거래처, 특수관계자 거래, 원재료 매입 현황, 주요 제품 현황

```bash
# Download corp code mapping (do this first, cache locally)
curl -o corpCode.zip "https://opendart.fss.or.kr/api/corpCode.xml?crtfc_key=$OPENDART_API_KEY"

# Get filing list for a company
curl -s "https://opendart.fss.or.kr/api/list.json?crtfc_key=$OPENDART_API_KEY&corp_code=XXXXXXXX&bgn_de=20230101&end_de=20231231&page_count=10"

# Get financial statements
curl -s "https://opendart.fss.or.kr/api/fnlttSinglAcntAll.json?crtfc_key=$OPENDART_API_KEY&corp_code=XXXXXXXX&bsns_year=2023&reprt_code=11011&fs_div=CFS"
```

**reprt_code:** 11011=annual, 11012=semi-annual, 11013=Q1, 11014=Q3
**Known corp codes:** Samsung Electronics=00126380 (verify others from corpCode.xml)

---

### e-Stat (Japan Trade Statistics) — Free key (100K req/day)
- **URL:** `https://api.e-stat.go.jp/rest/3.0/app/json/`
- **Registration:** https://www.e-stat.go.jp/api/ → ユーザ登録 (international users OK)

```bash
# Search for trade statistics tables
curl -s "https://api.e-stat.go.jp/rest/3.0/app/json/getStatsList?appId=$ESTAT_API_KEY&searchWord=貿易統計&lang=J"

# Get metadata for a table (MUST do this first to learn category codes)
curl -s "https://api.e-stat.go.jp/rest/3.0/app/json/getMetaInfo?appId=$ESTAT_API_KEY&statsDataId=TABLE_ID"

# Get actual trade data (category codes from metadata)
curl -s "https://api.e-stat.go.jp/rest/3.0/app/json/getStatsData?appId=$ESTAT_API_KEY&statsDataId=TABLE_ID&cdCat01=3818&limit=100"
```

**Gotcha:** You MUST call getMetaInfo first to learn which cdCat parameter maps to HS codes vs countries. Japan uses 9-digit HS codes.

---

### KIPRIS Plus (Korea Patents) — Free key (1K req/day)
- **URL:** `http://plus.kipris.or.kr/openapi/rest/`
- **Registration:** https://plus.kipris.or.kr → 오픈API 이용신청

```bash
# Search by applicant
curl -s "http://plus.kipris.or.kr/openapi/rest/patUtiModInfoSearchSevice/applicantNameSearchInfo?applicant=삼성전자&numOfRows=10&pageNo=1&ServiceKey=$KIPRIS_API_KEY"

# Search by keyword in semiconductor classification
curl -s "http://plus.kipris.or.kr/openapi/rest/patUtiModInfoSearchSevice/ipcSearchInfo?ipc=H01L&numOfRows=10&pageNo=1&ServiceKey=$KIPRIS_API_KEY"
```

**Gotcha:** Response is XML by default. Note the typo "Sevice" in the actual API path.

---

### Lens.org (Patents + Scholarly Articles) — Free academic key (50 req/day)
- **URL:** `https://api.lens.org/patent/search`
- **Registration:** https://www.lens.org → request API access

```bash
curl -s -X POST "https://api.lens.org/patent/search" \
  -H "Authorization: Bearer $LENS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query":{"bool":{"must":[{"match":{"applicant.name":"Samsung Electronics"}},{"match":{"classification_cpc.symbol":"H01L21"}}]}},"size":10}'
```

---

## Tier 2 — Web Search Sources (use WebSearch tool)

| Source | URL | Language | Access | Best for |
|--------|-----|----------|--------|----------|
| **The Elec** | thelec.net | English | Free | Samsung/SK Hynix supply chain scoops |
| **ET News** | etnews.com | Korean | Free | Korean semiconductor industry daily |
| **DigiTimes** | digitimes.com | EN/CN | Partial paywall | Taiwan/TSMC supply chain intel |
| **JW Insights** | jwinsights.com | English | Mostly free | Chinese semiconductor industry (English) |
| **SemiAnalysis** | semianalysis.com | English | Paywall | Deep technical analysis |
| **Semiconductor Engineering** | semiengineering.com | English | Free | Technical process/design coverage |
| **Nikkei Asia** | asia.nikkei.com | English | Partial paywall | Japan semiconductor revival (Rapidus, JASM) |
| **EE Times Japan** | eetimes.itmedia.co.jp | Japanese | Free | Japanese semiconductor coverage |
| **Maeil Business** | mk.co.kr | Korean | Free | Korean business/semiconductor |
| **JiWei / 集微网** | laoyaoba.com | Chinese | Free | China semiconductor industry (Chinese) |

## Tier 3 — Financial Research Aggregators (free)

| Platform | URL | Country | What it aggregates |
|----------|-----|---------|-------------------|
| **Naver Finance** | finance.naver.com | Korea | All Korean broker reports (free) |
| **EastMoney** | eastmoney.com | China | All Chinese broker reports (free PDFs) |
| **Kabutan** | kabutan.jp | Japan | Japanese stock data + news |
| **Goodinfo** | goodinfo.tw | Taiwan | TWSE stock financials |
| **TWSE MOPS** | mops.twse.com.tw | Taiwan | Monthly revenue + annual reports |

## Tier 4 — Chemical/Trade Databases

| Database | URL | What it reveals | Access |
|----------|-----|----------------|--------|
| **ECHA** | echa.europa.eu | EU chemical registrants by CAS number | Free web search |
| **PubChem** | pubchem.ncbi.nlm.nih.gov | Chemical properties + safety data | Free API |
| **K-REACH** | kreach.me | Korea chemical importers/manufacturers | Free (Korean) |
| **EPA CDR** | epa.gov/chemical-data-reporting | US manufacturing sites for chemicals | Free |
| **ImportGenius** | importgenius.com | Bill of lading / shipment records | Paid |
| **Panjiva** | panjiva.com | Global trade shipment data | Paid (S&P Global) |
| **TradeMap** | trademap.org | ITC trade flow analysis | Free basic |

## Tier 5 — Conference Exhibitor Databases

SEMICON events publish free searchable exhibitor directories:
- SEMICON Japan: semiconjapan.org
- SEMICON Korea: semiconkorea.org
- SEMICON Taiwan: semicontaiwan.org
- SEMICON China: semiconchina.org
- SEMICON West: semiconwest.org

**How to use:** Exhibitor categories (e.g., "CMP materials", "photoresist", "specialty gases") reveal which companies operate in which supply chain segment. Historical exhibitor data available via web archives.
