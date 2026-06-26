# Data Sources — AI stock watchdog v2

Sources are listed in priority order within each category. When two sources conflict, trust regulatory/exchange filings over news, and news over social media.

---

## 1. Exchange filings & regulatory (highest trust — primary source of truth)

### Corporate announcements
- **NSE**: https://www.nseindia.com/companies-listing/corporate-filings-announcements
- **BSE**: https://www.bseindia.com/corporates/ann.html
- Search: `site:nseindia.com "{COMPANY_NAME}" announcement` or `site:bseindia.com "{COMPANY_NAME}"`

### Shareholding patterns (quarterly — critical for promoter holding/pledge tracking)
- **BSE shareholding**: https://www.bseindia.com/corporates/shpSecurities.aspx
- **NSE shareholding**: search `"{TICKER} shareholding pattern" site:nseindia.com`
- **Trendlyne shareholding**: https://trendlyne.com/equity/{TICKER}/shareholding/
- **Screener shareholding tab**: https://www.screener.in/company/{TICKER}/
- Filing schedule: within 21 days of quarter-end (Apr 21, Jul 21, Oct 21, Jan 21)

### SEBI orders & enforcement
- **SEBI orders**: https://www.sebi.gov.in/sebiweb/home/HomeAction.do?doListing=yes&sid=1&ssid=6&smid=0
- **SEBI adjudication orders**: https://www.sebi.gov.in/sebiweb/home/HomeAction.do?doListing=yes&sid=5
- **SEBI interim orders**: search `site:sebi.gov.in "{COMPANY_NAME}" interim order`
- Search: `"{COMPANY_NAME}" SEBI order` last 30 days

### Surveillance
- **NSE ASM/GSM**: https://www.nseindia.com/regulations/asm-listed-securities
- **BSE surveillance**: https://www.bseindia.com/markets/equity/EQReports/Surveillance.aspx
- **NSE T2T list**: search `site:nseindia.com trade-to-trade`
- **NSE F&O ban list**: https://www.nseindia.com/market-data/f-o-ban-list (check daily during expiry week)

### Insider trading / SAST disclosures
- **NSE SAST/PIT**: corporate filings → filter by "Insider Trading / SAST"
- **BSE insider trading**: https://www.bseindia.com/corporates/Insider_Trading_new.aspx
- Search: `"{TICKER} insider trading disclosure" site:nseindia.com` or `site:bseindia.com`

---

## 2. Fundamentals, financials & filings

### Quarterly results & ratios
- **Screener.in**: https://www.screener.in/company/{TICKER}/ — quarterly results, annual P&L, balance sheet, cash flow, ratios, shareholding, concall transcripts
- **Trendlyne**: https://trendlyne.com/equity/Snapshot/{TICKER}/ — consensus estimates, broker ratings, DVM score
- **Tijori Finance**: https://www.tijorifinance.com/company/{TICKER} — segment breakdown, subsidiary mapping
- **TIKR**: https://tikr.com/ — global-quality financial data for Indian companies

### Cash flow statement (critical for CFO/PAT divergence check)
- **Screener cash flow**: https://www.screener.in/company/{TICKER}/#cash-flow
- **Moneycontrol financials**: cash flow tab
- **Annual report**: always cross-reference audited cash flow vs quarterly estimates

### Segment-wise results (use for multi-segment / conglomerate names)
- **BSE segment results filing**: search `"{COMPANY_NAME}" segment results site:bseindia.com`
- **Annual report segment note**: Note on segment reporting in audited financials
- **Tijori segment view**: provides clean segment breakdown

### Related party transactions
- **Annual report Note**: related party disclosures (mandatory under Ind-AS 24)
- **BSE corporate governance report**: filed quarterly, includes RPT details
- Search: `"{COMPANY_NAME}" related party transactions` last 90 days

### Credit ratings
- **CRISIL**: https://www.crisil.com/
- **ICRA**: https://www.icra.in/
- **CARE Ratings**: https://www.careratings.com/
- **India Ratings (Fitch)**: https://www.indiaratings.co.in/
- **Brickwork Ratings**: https://www.brickworkratings.com/
- Search: `"{COMPANY_NAME}" credit rating` last 30 days
- Search: `"{COMPANY_NAME}" rating downgrade OR watch OR negative` last 30 days

### Auditor reports
- **Annual report auditor section**: independent auditor's report, qualifications, emphasis of matter
- Search: `"{COMPANY_NAME}" auditor qualification OR emphasis of matter OR going concern`
- **ICAI disciplinary orders**: search if auditor flagged (rare but devastating)

---

## 3. Concall transcripts & investor presentations

- **Screener "Documents" tab**: https://www.screener.in/company/{TICKER}/#documents (often fastest)
- **Company investor relations page**: usually at `{company-domain}/investors` or `{company-domain}/investor-relations`
- **Trendlyne concall page**: https://trendlyne.com/equity/{TICKER}/concall-transcripts/
- **NDTV Profit concall coverage**: for major companies, journalists cover key quotes
- Search: `"{COMPANY_NAME}" concall transcript Q{N} FY{YY}` or `"{COMPANY_NAME}" analyst meet`

---

## 4. News (use multiple, cross-check before flagging)

### Tier-1 financial news
- **Moneycontrol**: https://www.moneycontrol.com/india/stockpricequote/{slug}
- **Economic Times Markets**: https://economictimes.indiatimes.com/markets
- **Business Standard**: https://www.business-standard.com/markets
- **Mint**: https://www.livemint.com/market
- **Reuters India**: https://www.reuters.com/world/india/
- **NDTV Profit (BQ Prime)**: https://www.ndtvprofit.com/

### Investigative / deep-dive (flag Sev-1 governance triggers from these)
- **The Ken**: https://the-ken.com/
- **Newslaundry Business**: for investigative pieces
- **SEBI Chai (Twitter/X)**: tracks SEBI orders and unusual filings

### Search patterns for news
- `"{COMPANY_NAME}" news` last 1 day (daily scan)
- `"{COMPANY_NAME}" SEBI OR "show cause" OR order` last 7 days
- `"{COMPANY_NAME}" ED OR CBI OR "income tax" OR raid OR investigation` last 30 days
- `"{COMPANY_NAME}" downgrade OR "target price cut"` last 7 days
- `"{COMPANY_NAME}" promoter pledge OR "shares pledged" OR encumbrance` last 30 days
- `"{COMPANY_NAME}" auditor resignation OR "auditor change"` last 90 days
- `"{COMPANY_NAME}" fraud OR whistleblower OR "forensic audit"` last 90 days

---

## 5. Institutional flows

### FII/FPI data
- **NSDL FPI data**: https://www.fpi.nsdl.co.in/ (sector-wise monthly flows)
- **Trendlyne FII/DII data**: daily net buy/sell
- **Moneycontrol FII/DII**: https://www.moneycontrol.com/stocks/marketstats/fii_dii_activity/

### Mutual fund holdings (monthly)
- **ValueResearch**: https://www.valueresearchonline.com/ — fund-wise holdings
- **Trendlyne MF holdings**: https://trendlyne.com/equity/{TICKER}/mutual-fund-holdings/
- **AMFI**: https://www.amfiindia.com/ — industry-level AUM data
- **MorningStar India**: portfolio-level holdings data

### Block / bulk deals
- **NSE bulk/block deals**: https://www.nseindia.com/market-data/large-deals
- **BSE bulk deals**: https://www.bseindia.com/markets/equity/EQReports/bulk_deals.aspx
- Decode who traded: cross-reference entity name with promoter group, PE/VC funds, FIIs

---

## 6. Pre-market & global cues

- **GIFT Nifty / SGX Nifty**: ET Markets pre-market page, Moneycontrol pre-market
- **US close**: Dow, Nasdaq, S&P 500 — any major source
- **Asian markets**: Nikkei 225, Hang Seng, Shanghai Composite
- **Brent crude**: Investing.com (direct impact on OMCs, airlines, paints)
- **USD/INR**: RBI reference rate, Investing.com (impact on IT, pharma exporters)
- **US 10Y yield**: sharp moves impact FII flows into emerging markets
- **VIX (India VIX)**: https://www.nseindia.com/market-data/india-vix — elevated >20 = risk-off

---

## 7. India market calendar (check at start of each week)

### Regular events
- **RBI MPC**: 6 meetings/year (Feb, Apr, Jun, Aug, Oct, Dec) — 3-day meeting, decision on last day
- **Union Budget**: typically Feb 1
- **Economic Survey**: day before Budget
- **GST Council meetings**: roughly quarterly
- **SEBI board meetings**: quarterly

### Result season windows (heaviest scan load)
- **Q3 (Oct-Dec) results**: mid-Jan to mid-Feb
- **Q4 (Jan-Mar) results**: mid-Apr to end-May (busiest — annual + quarterly)
- **Q1 (Apr-Jun) results**: mid-Jul to mid-Aug
- **Q2 (Jul-Sep) results**: mid-Oct to mid-Nov

### F&O expiry (elevated volatility)
- **Monthly expiry**: last Thursday of each month
- **Weekly Bank Nifty/Nifty expiry**: every Thursday
- **Quarterly expiry**: end-March, end-June, end-Sep, end-Dec (rollover week = extra volatile)

### Result date tracking
- **BSE result calendar**: https://www.bseindia.com/corporates/results_calendar.html
- **Trendlyne results calendar**: https://trendlyne.com/calendar/quarterly-results/
- **Moneycontrol results calendar**: check company page for board meeting date

---

## 8. Sector-specific sources

### Banks / NBFCs
- **RBI**: weekly statistical supplement, financial stability report, master circulars
- **RBI PCA list**: https://www.rbi.org.in/ — search "prompt corrective action"
- **NPA data**: quarterly RBI financial stability report, individual bank disclosures
- Key metrics to search: NIM, CASA ratio, GNPA/NNPA, slippage ratio, credit cost, CD ratio

### Auto
- **SIAM monthly data**: https://www.siam.in/statistics.aspx (wholesale dispatches)
- **FADA monthly data**: https://www.fada.in/ (retail registrations — more reliable than SIAM)
- **VAHAN dashboard**: https://vahan.parivahan.gov.in/vahan4dashboard/ (registration data)

### IT Services
- **NASSCOM**: https://nasscom.in/ — industry reports
- **Peer concalls**: TCS/Infosys/HCL Tech guide for the sector — their commentary is sector read
- Key metrics: deal TCV, headcount, attrition, utilization, constant currency growth

### Pharma
- **USFDA**: https://www.fda.gov/ — search for Form 483, Warning Letters, Import Alert
- **DCGI / CDSCO**: https://cdsco.gov.in/ — Indian drug regulator
- **ANDA approvals**: https://www.accessdata.fda.gov/scripts/cder/daf/
- Key metrics: US revenue %, ANDA pipeline, R&D as % of sales, API vs formulations mix

### Cement
- **Company monthly dispatches**: most large players disclose monthly volumes
- **ICRA cement reports**: quarterly
- Key metrics: realization per tonne, cost per tonne, capacity utilization, clinker ratio

### Oil & Gas (refining, petchem, E&P)
- **Singapore GRM**: proxy for India refining margins — search `Singapore GRM` weekly
- **Brent-Dubai spread**: impacts Indian refiner margins vs global benchmarks
- **Petchem spreads**: polymer/polyester delta — search `{product} spread Asia`
- **Ministry of Petroleum**: https://www.ppac.gov.in/ — petroleum planning & analysis cell
- **Gas pricing**: APM gas price notification (revised semi-annually by govt)

### Telecom (relevant for Reliance Jio)
- **TRAI data**: https://www.trai.gov.in/ — subscriber data, ARPU, monthly reports
- **COAI**: https://coai.com/ — industry body data
- Key metrics: subscriber adds, ARPU, data usage per subscriber, tower sharing revenue

### Retail (relevant for Reliance Retail)
- **RAI (Retailers Association of India)**: sentiment surveys
- Key metrics: revenue per sqft, same-store sales growth, store count, footfall
- Compare with: DMart (DMART), Trent (TRENT), V-Mart, Shoppers Stop

### Real Estate
- **ANAROCK / Knight Frank / JLL**: quarterly reports on absorption, launches, pricing
- **RERA portals**: state-wise project registrations

### Power & Energy
- **CEA daily reports**: https://cea.nic.in/ — generation, PLF data
- **IEX (Indian Energy Exchange)**: spot power prices
- **MNRE**: https://mnre.gov.in/ — renewable energy capacity additions

---

## 9. Macro indicators (scan weekly, not daily)

- **RBI press releases & MPC minutes**: https://www.rbi.org.in/
- **Budget documents**: https://www.indiabudget.gov.in/
- **MOSPI GDP data**: https://mospi.gov.in/
- **CMIE**: economic indicators (unemployment, consumer sentiment, capex data)
- **PMI Manufacturing & Services**: released first week of each month
- **GST collection data**: released monthly by Finance Ministry (proxy for economic activity)
- **Auto sales data**: released by 1st-2nd of each month (early economic indicator)
- **Core sector output (IIP)**: 8 core industries data — released monthly

---

## 10. Search query templates (copy-paste ready)

### Daily scan per stock
```
"{COMPANY_NAME}" news today
"{TICKER}" NSE announcement
"{COMPANY_NAME}" SEBI
"{COMPANY_NAME}" results OR earnings
"{COMPANY_NAME}" promoter pledge OR holding
"{COMPANY_NAME}" block deal OR bulk deal
```

### Weekly deep scan per stock
```
"{COMPANY_NAME}" credit rating
"{COMPANY_NAME}" auditor
"{COMPANY_NAME}" forensic OR fraud OR whistleblower
"{COMPANY_NAME}" ED OR CBI OR "income tax" raid
"{COMPANY_NAME}" shareholding pattern
"{COMPANY_NAME}" related party transaction
```

### Sector scan
```
"{SECTOR}" India outlook 2026
RBI policy impact {SECTOR}
"{SECTOR}" India regulatory change
```
