# Labor Market

description: CN-HK-US labor conditions and cost pressures for HK-listed corporates. Triggers on "labor market", "unemployment", "wages", "jobs", "NFP", "surveyed unemployment".

## Workflow

### Step 1: Frame
Confirm focus: China urban unemployment, HK labor market, US payrolls, or cost pressure impact on HK corporates.

### Step 2: Gather data
Run in parallel (max 2 calls):
- `get_macro_data(indicators=["US_UNEMPLOYMENT", "US_NFP", "US_WAGE_GROWTH", "CN_SURVEYED_UNEMPLOYMENT", "CN_WAGE_GROWTH"], period="1y")`
- `get_macro_data(indicators=["HK_UNEMPLOYMENT", "HK_WAGE_GROWTH", "HK_LFPR", "CN_URBAN_EMPLOYMENT"], period="1y")`

Then:
- `get_macro_data(indicators=["CN_MIGRANT_WORKER", "CN_MINIMUM_WAGE", "HK_MEDIAN_INCOME"], period="6mo")`

### Step 3: Analyze
1. **US Labor Market**
   - Unemployment rate vs NAIRU
   - NFP monthly change vs expectations
   - Wage growth (avg hourly earnings) — inflation signal

2. **China Labor Market**
   - Surveyed urban unemployment rate (official series)
   - Youth unemployment trend
   - Migrant worker employment levels
   - Wage growth in manufacturing/services

3. **HK Labor Market**
   - Unemployment rate (seasonally adjusted)
   - Underemployment rate
   - Labor force participation
   - Median income trend
   - Import labor scheme impact

4. **Cost Pressure Impact on HK Corporates**
   - Labor cost as % of revenue (by sector)
   - Minimum wage adjustment impact
   - Cross-border labor (HK employers, mainland workers)
   - FX impact on offshore labor costs

### Step 4: Present
```
| Market | Unemployment | Wage Growth | LFPR | Trend |
|--------|-------------|-------------|------|-------|
| US | ... | ... | ... | ... |
| China | ... | ... | N/A | ... |
| HK | ... | ... | ... | ... |
```

Add "Sector Impact for HK Equities" section:
```
| Sector | Labor Intensity | Cost Pressure | HK Ticker Examples |
|--------|----------------|---------------|-------------------|
| Retail | High | Rising min wage | ... |
| Tech | Medium | Talent war | ... |
| Property | Medium | Construction cost | ... |
| Logistics | High | Driver shortage | ... |
```

Add "Key Risk" callout: labor market development that could impact HK earnings.

## Important Notes
- Token: respect depth setting from style.md; summary table first, detail on request
- HK-specific: HK labor market plus China labor cost are dual drivers for HK corporates
- China youth unemployment is a key social/economic risk factor
- Note data frequency (monthly/quarterly) and latest data date
- Max 2 parallel calls per step
