# Market Sizing Workflow
> Pipeline | Sizing Flow | Multilingual Queries | Step 5b: Counterfactual | Pitfalls | Output (Market Size, Share, Concentration, Growth, Gaps)

**Question pattern:** "What's the market for X?" / "How big is the CMP slurry market?" / "What's the TAM for EUV pellicles?"

## Investigation Pipeline

```
User Question: "What's the CMP slurry market breakdown?"
    │
    ▼
┌─────────────────────────────────┐
│  1. DEFINE THE SEGMENT          │  What exactly are we sizing?
│                                 │  ├── Material? Equipment? Service?
│     Scope the question          │  ├── By application? (oxide CMP vs metal CMP)
│                                 │  ├── By node? (advanced <7nm vs mature)
│                                 │  └── Geographic? (global vs China-domestic)
└──────────┬──────────────────────┘
           │
           ▼
┌─────────────────────────────────┐
│  2. TOP-DOWN: ANALYST REPORTS   │  Published market size estimates
│                                 │  ├── TrendForce (memory, foundry utilization)
│     Search for existing sizing  │  ├── Yole Group (packaging, compound semi)
│                                 │  ├── SEMI (equipment, World Fab Forecast)
│                                 │  ├── TechCET (materials — CMP, gases, wet chem)
│                                 │  ├── Omdia (broad market data, expensive)
│                                 │  └── Broker reports:
│                                 │      ├── Naver Finance → 리서치 tab (Korea)
│                                 │      ├── EastMoney → 研报中心 (China)
│                                 │      ├── Kabutan (Japan)
│                                 │      └── MoneyDJ / MOPS (Taiwan)
│                                 │
│     ⚠ ALWAYS flag source +      │  Most analyst data is paywalled.
│     date + whether you accessed │  Press summaries often quote numbers.
│     it or citing from memory    │  Search: "[material] market size 2024"
└──────────┬──────────────────────┘
           │
           ▼
┌─────────────────────────────────┐
│  3. BOTTOM-UP: COMPANY DATA     │  Sum individual company revenues
│                                 │
│     Build from public filings   │  Revenue sources by filing system:
│                                 │  ├── DART → 매출 현황, 주요 제품 현황
│                                 │  ├── EDINET → セグメント情報, 事業の内容
│                                 │  ├── MOPS → monthly 月營收 (unique — fastest)
│                                 │  ├── cninfo → 主营业务分析
│                                 │  └── 10-K → segment disclosures (US)
│                                 │
│     Cross-reference:            │  Company A segment revenue
│     Sum known players           │  + Company B segment revenue
│     vs analyst total = gap      │  + Company C segment revenue
│     Gap = unlisted/private cos  │  ─────────────────────────────
│                                 │  = Bottom-up estimate
│                                 │  Compare vs top-down → consistency check
└──────────┬──────────────────────┘
           │
           ▼
┌─────────────────────────────────┐
│  4. TRADE DATA CROSS-CHECK      │  Validate with material flows
│                                 │
│     Directional validation only │  ├── Comtrade: HS code bilateral flows
│     Trade data ≠ market size    │  │   (3818=wafers, 3707=resist, 8486=equip)
│     but exposes inconsistencies │  ├── e-Stat: Japan exports at 9-digit HS
│                                 │  └── Taiwan customs (MOPS trade data)
│                                 │
│     Example sanity check:       │  If analyst says "Japan photoresist market
│     Trade flow vs market claim  │  = $4B" but Japan HS 3707 total exports
│                                 │  = $3.3B → either market includes domestic
│                                 │  consumption or definition differs
└──────────┬──────────────────────┘
           │
           ▼
┌─────────────────────────────────┐
│  5. CONCENTRATION ANALYSIS      │  Who holds how much?
│                                 │
│     Market structure matters    │  ├── Top-1 share → monopoly risk?
│     more than total TAM         │  ├── Top-3 share → oligopoly?
│                                 │  ├── HHI index (sum of squared shares)
│                                 │  ├── Geographic concentration
│                                 │  └── Compare vs chokepoints list
│                                 │      (chemistry/precursor-chains.md)
└──────────┬──────────────────────┘
           │
           ▼
┌─────────────────────────────────┐
│  6. OUTPUT                      │
│     Grade every number          │  Market size: $X.XB ± range
│     Source everything           │  Growth: X% CAGR (source, period)
│     Flag what's estimated       │  Share breakdown by company
│     vs confirmed                │  Concentration metrics
│                                 │  Source + date for EACH figure
│                                 │  "What I Could Not Size" section
└─────────────────────────────────┘
```

## Market Sizing Flow (Material Example)

> **Note:** The figures below are illustrative methodology, not verified data.
> They show how to structure a market sizing exercise, not actual confirmed numbers.

```
Global CMP Slurry Market (~$2.5B est.)
    │
    ├── By application
    │   ├── Oxide CMP (colloidal silica) ── ~40%
    │   ├── Metal CMP (Cu, W, barrier) ──── ~35%
    │   ├── STI CMP (ceria) ──────────────── ~15%
    │   └── Other (poly, ILD) ────────────── ~10%
    │
    ├── By supplier (approx. share, UNVERIFIED)
    │   ├── Entegris/CMC Materials (US) ──── #1
    │   ├── Fujimi (5384.T, Japan) ────────── #2-3
    │   ├── AGC (5201.T, Japan) ───────────── #2-3
    │   ├── DuPont (US) ──────────────────── Top 5
    │   ├── Anji Micro (688019.SS, China) ── Growing
    │   └── KC Tech (281820.KQ, Korea) ───── Regional
    │
    ├── By geography (demand)
    │   ├── Taiwan (TSMC) ───── ~30%
    │   ├── Korea (Samsung/SK) ── ~25%
    │   ├── China ──────────────── ~20% (growing fast)
    │   ├── Japan ──────────────── ~10%
    │   └── US/EU ─────────────── ~15%
    │
    └── Upstream chokepoint
        └── Colloidal silica → Fuso Chemical (4368.T) [VERIFY]
        └── Ceria → China rare earth processing [VERIFY]
```

## Multilingual Search Queries

### Korean (시장 규모):
```
[소재명] 시장 규모              → "[material] market size"
[소재명] 시장 점유율            → "[material] market share"
반도체 [소재명] 시장 전망       → "semiconductor [material] market outlook"
[소재명] 세계 시장              → "[material] global market"
```

### Japanese (市場規模):
```
{材料名} 市場規模               → "[material] market size"
{材料名} シェア                 → "[material] share"
半導体材料 市場 予測            → "semiconductor materials market forecast"
{材料名} 世界市場               → "[material] global market"
```

### Chinese — Mainland (市场规模):
```
[材料名] 市场规模               → "[material] market size"
[材料名] 市场份额               → "[material] market share"
[材料名] 国产化率               → "[material] localization rate"
[材料名] 行业研究报告           → "[material] industry research report"
```

### Chinese — Taiwan (市場規模):
```
[材料名] 市場規模               → "[material] market size"
[材料名] 市佔率                 → "[material] market share" (Taiwan phrasing)
半導體 [材料名] 市場 展望       → "semiconductor [material] market outlook"
[材料名] 全球市場               → "[material] global market"
```

## Step 5b: Counterfactual check on sizing

When top-down (analyst reports) and bottom-up (summing company revenues) estimates diverge by >20%, run the [Counterfactual Consistency Check](counterfactual-check.md). Don't average the numbers. Surface the contradiction: which source uses what market definition? Does the analyst include adjacent segments? Are private companies creating a blind spot in the bottom-up sum? A documented disagreement is more useful than a false consensus.

## Common Pitfalls

1. **"Market" definition varies wildly.** CMP slurry market — does that include pads? Conditioners? Diamond discs? Always clarify scope.
2. **Currency matters.** A "$2B market" in a 2020 report at ¥110/$ is different from 2024 at ¥150/$. Japanese company revenues in yen can look like growth when it's just depreciation.
3. **Analyst reports age fast.** A 2022 market sizing doesn't account for the 2023-2024 AI/HBM demand surge. Always note the report date.
4. **China double-counts.** Chinese broker reports sometimes count domestic + import as "China market" and sometimes only domestic production. Clarify which.
5. **Private companies are black holes.** Morita Chemical (HF), SEMES (equipment), Tanaka Precious Metals — no public revenue data. Their share is estimated by subtraction.
6. **MOPS monthly revenue is gold.** Taiwan is the only market where you get company revenue within 10 days of month-end. Use it for real-time market tracking.

## Output Format

```markdown
# [Material/Equipment] Market Assessment

## Market Size
- Global: $X.XB (YYYY) [SOURCE, accessed/not accessed]
- CAGR: X% (YYYY-YYYY) [SOURCE]
- ⚠ Confidence: [CONFIRMED from accessed report / APPROXIMATE from press summary / ESTIMATED bottom-up]

## Market Share Breakdown
| Company | Approx. Share | Revenue (segment) | Source | Confidence |
|---|---|---|---|---|

## Concentration
- Top-1: X% | Top-3: X% | HHI: XXXX
- Geographic: [X% from Country A]
- Chokepoint: [tier-2 dependency if any]

## Growth Drivers
- [driver 1]
- [driver 2]

## What I Could Not Size
- [gaps, unavailable data, private company blind spots]
```
