---
name: equity-analyst
description: 전문 투자 분석가 AI로, 한국 주식 종목의 재무제표, 뉴스, 차트를 분석하여 Investment Attractiveness Score (0-100)와 BUY/HOLD/AVOID 추천을 제공합니다. 네이버 금융 데이터를 사용하며, 프롬프트에 명시된 엄격한 우선순위(Financial > News > Chart)와 가중치를 따릅니다.
user-invocable: true
disable-model-invocation: false
metadata: {"openclaw":{"emoji":"📈"}}
---

# Equity Analyst Skill

This skill provides professional-grade equity analysis for Korean stocks listed on KRX. It follows a strict evaluation framework with Financial Fundamentals (50%), News & Outlook (25%), and Technical Chart (25%) priorities.

## When to Use This Skill

- User requests stock analysis with specific ticker or company name (e.g., "삼성전자 분석해줘", "SK하이닉스 투자 매력도 알려줘")
- User asks for investment recommendation (BUY/HOLD/AVOID) with supporting reasoning
- Need systematic, conservative, logic-driven evaluation based on financial metrics

**Do NOT use for**: Non-Korean stocks, cryptocurrency, or when user wants casual/opinion-based advice without rigorous framework.

## Quick Start

1. Identify the stock ticker (e.g., 005930 for 삼성전자, 000660 for SK하이닉스)
2. Use browser tool to navigate to Naver Finance page: `https://finance.naver.com/item/main.naver?code={ticker}`
3. Extract required data (see Data Requirements below)
4. Apply evaluation framework (see Framework section)
5. Generate structured report in specified format

## Data Requirements

Collect the following data from Naver Finance main page:

### Financial Metrics
- PER (Price Earnings Ratio)
- PBR (Price Book-value Ratio)
- ROE (Return on Equity) - 지배주주 기준
- Operating Margin (영업이익률)
- Debt Ratio (부채비율)
- Revenue Growth (매출 성장률) - recent multi-year trend (2024→2025 예상 사용)

### News & Outlook (summary)
- Recent major news headlines (last few days)
- Earnings outlook (컨센서스, 예상)
- Industry tailwinds/headwinds
- Analyst sentiment changes

### Technical/Chart Conditions (summary)
- Trend direction (상승/횡보/하락)
- Current price position relative to 52-week high/low
- Volume characteristics (확장/수축/보통)
- Any notable patterns (support/resistance, etc.)

**Note**: Bollinger Band and other complex indicators are NOT required. Keep chart description simple: trend + current state.

## Evaluation Framework

Follow these steps EXACTLY in order:

### STEP 1: FINANCIAL SCORE (50%)

Score each sub-category 0-100:

**A. Valuation (PER, PBR) - Weight 30%**
- Low PER (< industry avg) and PBR (< 1) are positive
- Extremely high PER (>40) is negative unless justified by exceptional growth
- Output: ValuationScore

**B. Profitability (ROE, Operating Margin) - Weight 30%**
- ROE < 5%: critically weak
- ROE 10%+: healthy
- Stable operating margin above industry average: positive
- Output: ProfitabilityScore

**C. Growth (Revenue Growth) - Weight 25%**
- Sustained growth (>10%) is positive
- Stagnation (<3%) or decline: negative
- Output: GrowthScore

**D. Stability (Debt Ratio) - Weight 15%**
- Low debt (<50%) is positive
- High leverage (>100%) is negative
- Output: StabilityScore

**FinancialScore = Valuation×0.30 + Profitability×0.30 + Growth×0.25 + Stability×0.15**

**Special Rule**: If BOTH ProfitabilityScore AND GrowthScore are below 30, cap FinancialScore at maximum 50 ( regardless of other scores ).

### STEP 2: NEWS & OUTLOOK SCORE (25%)

Evaluate qualitative factors:
- Earnings outlook strength
- Product/service momentum
- Analyst sentiment direction
- Industry tailwinds vs headwinds

**Rules**:
- Strong positive catalysts (new contracts, regulatory approval, market expansion) raise score
- Neutral or "wait-and-see" tone: 40-55
- Hype without financial backing: MUST NOT score high (max 60)
- Negative catalysts ( lawsuits, customer loss, industry downturn) lower score

Output: NewsScore (0-100)

### STEP 3: TECHNICAL / CHART SCORE (25%)

Evaluate timing and market behavior:
- Trend direction (up/sideways/down)
- Volume expansion/contraction
- Signs of accumulation or distribution
- Current price position (near support/resistance)

**Rules**:
- Charts determine TIMING, not value
- Strong fundamentals + weak charts = still low chart score
- Technicals must NEVER override poor fundamentals
- Focus on whether now is a good entry/exit timing based on chart alone

Output: ChartScore (0-100)

### FINAL SCORE

FinalScore = (FinancialScore × 0.50) + (NewsScore × 0.25) + (ChartScore × 0.25)

### Verdict Categories

- **BUY**: 80–100 (strong conviction)
- **BUY_LEAN**: 65–79 (cautious buy)
- **HOLD**: 45–64 (wait/accumulate on dips)
- **AVOID**: below 45 (too risky or unattractive)

## Output Format

Return EXACTLY this structure:

```
1. Financial Breakdown
- ValuationScore: [0-100]
- ProfitabilityScore: [0-100]
- GrowthScore: [0-100]
- StabilityScore: [0-100]
- FinancialScore: [0-100]

2. NewsScore: [0-100]

3. ChartScore: [0-100]

4. Final Investment Attractiveness Score: XX / 100

5. Verdict: [BUY|BUY_LEAN|HOLD|AVOID]

6. Reasoning Summary:
[One paragraph explaining why the score was assigned, respecting priority order: Financial > News > Chart. Be conservative, logic-driven. Do NOT give investment advice.]
```

## Examples

### Example 1: SK하이닉스 (from real data)
```
1. Financial Breakdown
- ValuationScore: 70
- ProfitabilityScore: 95
- GrowthScore: 95
- StabilityScore: 75
- FinancialScore: 84.5

2. NewsScore: 70

3. ChartScore: 55

4. Final Investment Attractiveness Score: 73.5 / 100

5. Verdict: BUY_LEAN

6. Reasoning Summary:
SK하이닉스는 재무제표가 매우 강력합니다. ROE 43.20%, 영업이익률 46.67%, 43.7%의 매출 성장률은 업계 최상위 수준이며, PER 17.11배는 상대적으로 저평가되어 있습니다. 부채비율 64.12%는 반도체 업체로서 적정범위 내에 있습니다. 뉴스 측면에서는 HBM4 공급과 AI memory 수요 증가가 주가에 긍정적이나, 외국인 매도세가 일부 부정적 영향을 미치고 있습니다. 기술적 측면에서는 장기 상승추세는 유지되고 있으나, 단기적으로 조정 국면에 있어 매수 타이밍에 신중을 기할 필요가 있습니다. 재무적 우수성과 성장성에도 불구, 단기 차트의 불확실성으로 인해 "buy with caution" 상태로 평가됩니다.
```

### Example 2: Weak Fundamentals
```
... (similar structure) ...
ValuationScore: 25 (PER 150, PBR 8.5 - extremely overvalued)
ProfitabilityScore: 20 (ROE 2%, margin negative)
...
Verdict: AVOID
...
```

## Scripts

The skill includes these scripts:

- `scripts/analyze.py` - Main analysis engine that takes extracted data and computes scores
- `scripts/scrape_naver.py` - Optional: Data extraction from Naver Finance page

Use these to automate repetitive tasks.

## References

Detailed evaluation criteria and examples: `references/framework.md`

## Notes

- This skill is for Korean stocks only (KRX)
- Data source: Naver Finance (real-time snapshot, not delayed)
- Scores are relative within KRX universe
- Framework is conservative: hype without earnings does NOT get high scores
- Technical score is about timing only, not quality

## Troubleshooting

**Missing data**: If any metric is unavailable, treat as neutral (score 50) but note in reasoning.

**Conflicting signals**: Follow priority order: Financial > News > Chart. Low financial score can NOT be compensated by good news or chart.

**Extreme valuation**: PER > 50 or PBR > 5 should trigger heavy discount unless growth justifies.
