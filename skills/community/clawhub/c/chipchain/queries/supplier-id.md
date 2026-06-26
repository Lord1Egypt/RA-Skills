# Supplier Identification Workflow

> Steps 1-7: Entity DB check → Multilingual queries (KO/JA/ZH-CN/ZH-TW) → Filing search → Industry press → Triangulation → Counterfactual → Report

**Question pattern:** "Who supplies X material to Y company?"

## Step 1: Identify the material and target company

Parse the question to extract:
- **Material:** e.g., hafnium precursors, CMP slurry, photoresist, NF3, silicon wafers
- **Target company:** e.g., SK Hynix, TSMC, Samsung, Intel
- **Geography:** Which country/countries are involved?

## Step 2: Check entity database first

Read the relevant entities file (korea.md, japan.md, taiwan.md, china.md) and search for
companies known to supply this specific material. This gives you a starting hypothesis.

## Step 3: Construct multilingual search queries

Load the relevant lexicon file and build searches:

### Korean (for Samsung/SK Hynix suppliers):
```
[회사명] [소재명] 공급업체          → "[Company] [material] supplier"
[회사명] [소재명] 납품              → "supply [material] to [Company]"
[회사명]에 [소재명] 공급하는 업체    → "company that supplies [material] to [Company]"
[소재명] [회사명]향 납품 개시        → "began supplying [material] to [Company]"
```

### Japanese (for Japanese suppliers):
```
{会社名}に{材料名}を供給           → "supplies [material] to [Company]"
{材料名}の供給元                   → "supply source of [material]"
{会社名}向け{材料名}               → "[material] for [Company]"
{材料名}の主要メーカー              → "major manufacturers of [material]"
```

### Chinese Simplified (for Chinese supply chain):
```
[公司名] 供应商                    → "[Company] supplier"
[公司名] 采购 [材料名]             → "[Company] procures [material]"
[公司名] 通过 [供应商] 验证         → "[supplier] passed [Company] qualification"
```

### Chinese Traditional (for Taiwan supply chain):
```
[公司名] 供應商                      → "[Company] supplier"
[供應商] 打入 [公司名] 供應鏈       → "[supplier] broke into [Company] supply chain"
[公司名] 採購 [材料名]              → "[Company] procures [material]"
[供應商] 通過 [公司名] 驗證         → "[supplier] passed [Company] qualification"
[供應商] 取得 [公司名] 認證         → "[supplier] obtained [Company] certification"
```

## Step 4: Search filings (highest reliability)

**For Korean companies (DART):**
- Search target company's 사업보고서 (annual report) for section: 주요 거래처 (major trading partners)
- Search supplier company's filing for: 매출 집중 (revenue concentration) — if >10% from one customer, it's disclosed
- Check 특수관계자 거래 (related party transactions) for intra-group supply

**For Japanese companies (EDINET):**
- Download annual report (有価証券報告書, docTypeCode=120)
- Search for: 主要仕入先 (major suppliers), 主要販売先 (major customers >10% of revenue)
- Check 事業等のリスク (business risks) for supplier dependency disclosures

**For Taiwan companies (MOPS):**
- Check 年報 for: 主要供應商, 前十大供應商, 關係人交易
- Note: Taiwan often anonymizes as "供應商A", "供應商B" with percentages

**For Chinese companies (cninfo):**
- IPO prospectuses (招股说明书) on STAR Market disclose 前五名供应商 BY NAME
- Annual reports: 主要供应商 section lists top-5 with amounts
- Search: cninfo.com.cn full-text search for company name + 供应商

## Step 5: Search industry press

Use WebSearch with the queries from Step 3 against:
- Korean: ET News (etnews.com), The Elec (thelec.kr/thelec.net)
- Japanese: EE Times Japan, Nikkei xTECH, Semiconductor Portal
- Chinese: JW Insights (jwinsights.com), JiWei (laoyaoba.com)
- Taiwan: DigiTimes (digitimes.com)
- Global: Semiconductor Engineering (semiengineering.com), SemiAnalysis

## Step 6: Triangulate with indirect evidence

If direct confirmation isn't found:

1. **Patent co-filing:** Search Google Patents for patents co-assigned to both companies
2. **Conference papers:** Search Google Scholar for co-authored papers between companies
3. **Revenue geography:** Supplier's annual report says "XX% of revenue from [country/region]"
4. **Supplier awards:** Search "[target company] supplier award" in target language
5. **Trade data:** Query UN Comtrade for bilateral material flows at HS code level
6. **Chemical registrations:** Search ECHA by CAS number to find registered manufacturers
7. **SEMICON exhibitor lists:** Check if supplier exhibits in the relevant product category

## Step 6b: Counterfactual check

Before assigning confidence levels, run the [Counterfactual Consistency Check](counterfactual-check.md) on every claim graded STRONG INFERENCE or higher. The most common false positive in supplier identification is confusing "makes this material" with "supplies this material to this specific fab." If the alternative explanation is equally plausible, downgrade to MODERATE INFERENCE and note the falsifier.

## Step 7: Report findings with confidence levels

Every finding MUST include:
- The specific claim
- Confidence level (CONFIRMED / STRONG INFERENCE / MODERATE INFERENCE / SPECULATIVE)
- Source(s) — specific filing, article URL, patent number, or database query
- Date of source (information freshness)
