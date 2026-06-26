---
name: ai-trading-consortium
description: "AI-powered hedge fund that combines multi-expert trading strategies with comprehensive information gathering. Analyzes stocks through systematic data collection, analyst reports, bull/bear debates, and a council of legendary investor personas (Buffett, Graham, Lynch, Burry, Munger, Wood, Druckenmiller, Marks). Produces executive summary slides. Trigger keywords: stock analysis, trading decision, investment analysis, market evaluation, buy/sell/hold recommendation."
---

# AI Trading Consortium

## Overview

An AI-powered hedge fund system that combines sophisticated information gathering with multi-expert trading wisdom. It coordinates a full analysis pipeline: data collection, four-analyst assessment, structured bull/bear debate, an 8-member legendary investor council, risk management, portfolio decision, and executive summary slide generation (PDF + PPTX).

**Important**: Never provide financial advice — always clarify this is for educational/research purposes only.

## Workflow

### Phase 0: Stock Identification (if needed)

If the user provides a company name, partial name, or ambiguous query instead of a ticker symbol:

1. **Search** to identify the correct stock ticker and exchange
2. Confirm the company identity (full name, ticker, exchange, sector)
3. If multiple matches exist, clarify with the user or select the most relevant

**Examples:**
- "Analyze Tesla" → Search → Confirm TSLA (Tesla Inc, NASDAQ)
- "What about the Google stock?" → Search → GOOGL or GOOG (Alphabet Inc)
- "Look at that Chinese EV company NIO" → Search → NIO (NIO Inc, NYSE)

**Output for symbol lookup:**
```json
{
  "query": "user's original query",
  "identified_stock": {
    "company_name": "Full Legal Name Inc.",
    "ticker": "TICK",
    "exchange": "NASDAQ",
    "sector": "Technology",
    "confidence": "high/medium/low"
  },
  "alternatives": [
    {"ticker": "OTHER", "reason": "Similar name..."}
  ]
}
```

### Phase 1: Information Gathering

1. **Collect comprehensive market data** from multiple sources (see Data Sources section)
2. **Run all four analyst assessments** sequentially:
   - Fundamentals Analyst → Financial health, valuation metrics
   - Technical Analyst → Price patterns, indicators
   - Sentiment Analyst → Social media, market sentiment
   - News Analyst → Breaking news, macro events

Each analyst produces a structured report (see Analyst Frameworks below).

### Phase 2: Research & Debate

3. **Construct both bull and bear cases** from the analyst reports
4. **Conduct 2-3 rounds of structured debate** (Opening Arguments → Rebuttals → Final Arguments)
5. **Synthesize debate conclusions** with a winner, scoring breakdown, and key takeaways

### Phase 3: Expert Council Review

6. **Channel each of the 8 legendary investor personas** to evaluate the opportunity
7. **Gather diverse perspectives** — each investor votes BUY/HOLD/SELL with conviction (1-10) and reasoning
8. **Weight opinions** based on relevance to the specific opportunity

### Phase 4: Risk & Execution

9. **Evaluate risk**: position sizing, stop-losses, portfolio impact, VaR
10. **Make final trading decision**: synthesize all inputs into an actionable recommendation

### Phase 5: Executive Summary Slides

11. **Create 3 PPT Summary Slides** (see Slide Specification below):
    - Slide 1: Process Overview & Data Collected
    - Slide 2: Expert Council Voting Results (hero visual with 8 investor votes)
    - Slide 3: Final Decision & Action Plan
12. **Compile slides** into PDF and PPTX deliverables

## Output Format

For each analysis, provide all of the following:

1. **Executive Summary**: Key findings and recommendation
2. **Analyst Reports**: Summary of each analyst's findings
3. **Debate Summary**: Bull vs Bear key arguments
4. **Expert Council Votes**: How each investor persona voted and why
5. **Risk Assessment**: Position size, stop-loss, risk/reward ratio
6. **Final Decision**: BUY / SELL / HOLD with conviction level (1-10)
7. **Three Summary Slides**: Visual presentation of the entire analysis

---

## Data Sources

Configure data gathering from multiple sources:

| Category | Sources |
|----------|---------|
| Stock Price Data | Yahoo Finance (yfinance) — Primary for OHLCV; Alpha Vantage — Validation |
| Fundamental Data | Alpha Vantage, SEC filings (10-K, 10-Q, 8-K) |
| Technical Indicators | Yahoo Finance, Alpha Vantage |
| News Data | Alpha Vantage, Google News, financial news APIs |
| Sentiment Data | Social media APIs (Reddit, Twitter/X, StockTwits) |

### Data Gathering Output Structure

```json
{
  "ticker": "SYMBOL",
  "timestamp": "ISO datetime",
  "price_data": {
    "current_price": 0.00,
    "52_week_high": 0.00,
    "52_week_low": 0.00,
    "volume": 0,
    "avg_volume": 0
  },
  "fundamentals": {
    "market_cap": 0,
    "pe_ratio": 0.00,
    "pb_ratio": 0.00,
    "revenue_growth": 0.00,
    "earnings_growth": 0.00
  },
  "technicals": {
    "rsi_14": 0.00,
    "macd_signal": "bullish/bearish",
    "trend": "uptrend/downtrend/sideways"
  },
  "news_summary": "Recent news highlights",
  "sentiment_score": 0.00
}
```

### Data Quality Guidelines
- Validate data across multiple sources when possible
- Flag any data quality issues or missing data
- Include data freshness timestamps
- Handle API rate limits gracefully
- Cache data appropriately to avoid redundant calls

---

## Analyst Frameworks

### Fundamentals Analyst

Evaluate companies based on financial health, competitive position, and intrinsic value.

#### Financial Health Assessment

1. **Profitability**
   - Gross margin, operating margin, net margin
   - Return on Equity (ROE), Return on Assets (ROA)
   - Return on Invested Capital (ROIC)

2. **Growth Metrics**
   - Revenue growth (YoY, 3-year CAGR)
   - Earnings growth
   - Free cash flow growth

3. **Balance Sheet Strength**
   - Current ratio, quick ratio
   - Debt/equity ratio
   - Interest coverage ratio
   - Cash position

4. **Cash Flow Quality**
   - Operating cash flow vs net income
   - Free cash flow generation
   - Capital allocation efficiency

#### Valuation Methods

1. **Discounted Cash Flow (DCF)** — Project 5-10 year cash flows, apply WACC, calculate terminal value, derive intrinsic value per share
2. **Comparable Company Analysis** — Identify peer group, compare P/E, EV/EBITDA, P/S ratios, apply appropriate multiples
3. **Dividend Discount Model (DDM)** — For dividend-paying stocks; Gordon Growth Model or multi-stage DDM
4. **Asset-Based Valuation** — Book value analysis, Net Asset Value (NAV)

#### Fundamentals Report Format

```markdown
# Fundamentals Analysis Report: [TICKER]

## Financial Health Score: [1-10]

### Profitability Analysis
- [Key findings]

### Growth Assessment
- [Key findings]

### Balance Sheet Strength
- [Key findings]

### Cash Flow Quality
- [Key findings]

## Valuation Summary
| Method | Intrinsic Value | Upside/Downside |
|--------|-----------------|-----------------|
| DCF    | $XX.XX          | +/-XX%          |
| Comps  | $XX.XX          | +/-XX%          |

## Signal: [BULLISH/BEARISH/NEUTRAL]
## Confidence: [1-10]

## Key Risks
- [Risk factors]
```

---

### Technical Analyst

Analyze price patterns, volume, and technical indicators to forecast price movements and identify entry/exit points.

#### Analysis Framework

**Trend Analysis:**
- Primary trend (higher highs/lows = uptrend; lower highs/lows = downtrend; sideways/consolidation)
- Moving averages: SMA (20, 50, 200), EMA (9, 21, 50)
- Golden cross / Death cross signals
- Price relative to key MAs

**Momentum Indicators:**
- RSI (14): Overbought (>70) / Oversold (<30), divergences
- MACD: Signal line crossovers, histogram analysis, divergences
- Stochastic Oscillator: Overbought/oversold, crossovers

**Volume Analysis:**
- Volume trends, On-Balance Volume (OBV), Accumulation/Distribution

**Chart Patterns:**
- Head and shoulders, double tops/bottoms
- Triangles (ascending, descending, symmetrical)
- Flags, pennants, cup and handle, wedges

**Support & Resistance:**
- Key price levels, Fibonacci retracement, pivot points, trendlines

#### Technical Report Format

```markdown
# Technical Analysis Report: [TICKER]

## Trend Summary
- Primary Trend: [UPTREND/DOWNTREND/SIDEWAYS]
- Short-term: [description]
- Medium-term: [description]

## Key Indicators
| Indicator | Value | Signal |
|-----------|-------|--------|
| RSI (14)  | XX.X  | Bullish/Bearish/Neutral |
| MACD      | XX.X  | Bullish/Bearish/Neutral |
| 50 SMA    | $XX.X | Above/Below |
| 200 SMA   | $XX.X | Above/Below |

## Support & Resistance
- Key Support: $XX.XX, $XX.XX
- Key Resistance: $XX.XX, $XX.XX

## Pattern Recognition
- [Identified patterns and implications]

## Signal: [BULLISH/BEARISH/NEUTRAL]
## Confidence: [1-10]

## Entry/Exit Levels
- Suggested Entry: $XX.XX
- Stop Loss: $XX.XX
- Target 1: $XX.XX
- Target 2: $XX.XX
```

---

### Sentiment Analyst

Analyze market sentiment from various sources to understand investor psychology and crowd behavior.

#### Sentiment Sources

**Social Media:**
- Reddit: r/wallstreetbets, r/stocks, r/investing — mention frequency and trend
- Twitter/X: Cashtag mentions ($TICKER), influential accounts, sentiment trend
- StockTwits: Bull/bear ratio, message volume

**Investor Behavior:**
- Options Flow: Put/Call ratio, unusual options activity, large block trades
- Institutional Activity: 13F filing changes, hedge fund positions, ETF flows
- Insider Activity: Insider buying/selling, Form 4 filings, cluster buying signals

**Market Indicators:**
- VIX (Fear Index) levels
- AAII Sentiment Survey
- CNN Fear & Greed Index
- Short interest ratio

#### Sentiment Scoring

Composite sentiment score from -1 to +1:

| Range | Interpretation |
|-------|---------------|
| -1.0 to -0.5 | Extremely Bearish |
| -0.5 to -0.2 | Bearish |
| -0.2 to +0.2 | Neutral |
| +0.2 to +0.5 | Bullish |
| +0.5 to +1.0 | Extremely Bullish |

#### Sentiment Report Format

```markdown
# Sentiment Analysis Report: [TICKER]

## Overall Sentiment Score: [X.XX] ([BULLISH/BEARISH/NEUTRAL])

### Social Media Sentiment
| Source | Score | Trend | Notable |
|--------|-------|-------|---------|
| Reddit | X.XX  | ↑/↓   | [notes] |
| Twitter| X.XX  | ↑/↓   | [notes] |

### Investor Behavior
- Put/Call Ratio: X.XX ([interpretation])
- Short Interest: X.X% ([interpretation])
- Insider Activity: [Net buying/selling]

### Institutional Sentiment
- Recent 13F changes: [summary]
- Notable positions: [key funds]

## Contrarian Signals
- [Any extreme readings that suggest reversal]

## Signal: [BULLISH/BEARISH/NEUTRAL]
## Confidence: [1-10]

## Key Observations
- [Notable sentiment shifts or anomalies]
```

---

### News Analyst

Monitor and analyze news, events, and macroeconomic factors impacting stock prices.

#### Coverage Areas

**Company-Specific News:**
- Earnings & Guidance: Quarterly reports, revenue/EPS surprises, forward guidance, conference call highlights
- Corporate Actions: M&A, stock splits/buybacks, dividend changes, leadership changes
- SEC Filings: 10-K, 10-Q, 8-K, proxy statements, Form 4 insider transactions
- Product/Business: Launches, contract wins/losses, partnerships, regulatory approvals

**Industry & Sector:**
- Competitor developments, industry trends, regulatory changes, supply chain updates

**Macroeconomic Events:**
- Economic Indicators: Fed rate decisions, inflation (CPI, PPI), employment, GDP
- Geopolitical: Trade policies, international conflicts, political developments, currency movements

#### Impact Assessment

Rate each news item:
- **Impact Level**: High / Medium / Low
- **Timeframe**: Immediate / Short-term / Long-term
- **Direction**: Positive / Negative / Neutral

#### News Report Format

```markdown
# News Analysis Report: [TICKER]

## Breaking News Summary
| Date | Headline | Impact | Direction |
|------|----------|--------|-----------|
| MM/DD | [news] | High/Med/Low | +/-/= |

## Company News
### Recent Developments
- [Key news items with analysis]

### Upcoming Events
- [Earnings date, ex-dividend, etc.]

## Industry Context
- [Relevant industry news]

## Macro Environment
- [Relevant macro factors]

## News-Driven Catalysts
### Positive Catalysts
- [List with timing]

### Negative Risks
- [List with timing]

## Signal: [BULLISH/BEARISH/NEUTRAL]
## Confidence: [1-10]

## Key Takeaways
- [Summary of most important news impacts]
```

---

## Debate Framework

Take all four analyst reports and conduct a structured investment debate.

### Round 1: Opening Arguments

**BULL CASE — Build arguments around:**
- Growth story & market opportunity
- Valuation opportunity & upside potential
- Favorable technical setup
- Positive sentiment & catalysts

**BEAR CASE — Build arguments around:**
- Valuation concerns & downside risks
- Business & competitive threats
- Financial weaknesses
- Technical warnings & sentiment risks

### Round 2: Rebuttals
- Bull addresses Bear's strongest points
- Bear addresses Bull's strongest points
- Each side must use data from analyst reports

### Round 3: Final Arguments
- Summarize strongest remaining arguments
- Acknowledge valid points from opposition
- Make final case to the jury

### Debate Rules

1. **Be Specific**: Use actual data points from analyst reports
2. **Be Fair**: Acknowledge valid opposing arguments
3. **Quantify**: Provide price targets and percentages
4. **No Fabrication**: Only use information from provided reports

### Debate Output Format

```markdown
# INVESTMENT DEBATE: [TICKER]

## ROUND 1: OPENING ARGUMENTS

### 🐂 BULL CASE
**Thesis**: [One sentence]

**Key Arguments:**
1. **[Argument 1]**
   - Evidence: [data from reports]
   - Implication: [why this matters]

2. **[Argument 2]**
   - Evidence: [data from reports]
   - Implication: [why this matters]

3. **[Argument 3]**
   - Evidence: [data from reports]
   - Implication: [why this matters]

**Upside Target**: $XX.XX (+XX%)

---

### 🐻 BEAR CASE
**Thesis**: [One sentence]

**Key Arguments:**
1. **[Argument 1]**
   - Evidence: [data from reports]
   - Implication: [why this matters]

2. **[Argument 2]**
   - Evidence: [data from reports]
   - Implication: [why this matters]

3. **[Argument 3]**
   - Evidence: [data from reports]
   - Implication: [why this matters]

**Downside Target**: $XX.XX (-XX%)

---

## ROUND 2: REBUTTALS

### 🐂 Bull Rebuts Bear
| Bear Argument | Bull Counter |
|---------------|--------------|
| [point]       | [rebuttal]   |
| [point]       | [rebuttal]   |

### 🐻 Bear Rebuts Bull
| Bull Argument | Bear Counter |
|---------------|--------------|
| [point]       | [rebuttal]   |
| [point]       | [rebuttal]   |

---

## ROUND 3: CLOSING ARGUMENTS

### 🐂 Bull's Final Statement
[2-3 sentences summarizing strongest case]

### 🐻 Bear's Final Statement
[2-3 sentences summarizing strongest case]

---

## DEBATE VERDICT

**Winner**: [BULL / BEAR]
**Margin**: [Decisive / Narrow / Too Close to Call]
**Confidence**: [1-10]

### Scoring Breakdown
| Category | Bull Score | Bear Score |
|----------|------------|------------|
| Evidence Quality | X/10 | X/10 |
| Logic & Reasoning | X/10 | X/10 |
| Risk Assessment | X/10 | X/10 |
| **Total** | XX/30 | XX/30 |

### Key Takeaways
- **Strongest Bull Point**: [summary]
- **Strongest Bear Point**: [summary]
- **Unresolved Uncertainty**: [what remains unclear]

### Recommendation to Portfolio Manager
[Summary of debate outcome and suggested weighting of bull vs bear perspectives]
```

---

## Multi-Expert Investment Council

Channel 8 legendary investors, each with distinct investment philosophies.

### Council Members

#### 1. Warren Buffett (Value/Quality)
**Philosophy**: "Buy wonderful companies at fair prices"
- Look for durable competitive advantages (moats)
- Management integrity and capital allocation
- Understandable business model
- Long-term holding period (forever)
- Circle of competence

#### 2. Benjamin Graham (Deep Value)
**Philosophy**: "Margin of safety is paramount"
- Net-net stocks (trading below net current assets)
- Low P/E, low P/B ratios
- Strong balance sheets
- Quantitative screening
- Diversification across cheap stocks

#### 3. Peter Lynch (Growth at Reasonable Price)
**Philosophy**: "Invest in what you know"
- Ten-baggers in everyday businesses
- PEG ratio < 1
- Understand the story behind the stock
- Categorize: slow growers, stalwarts, fast growers, cyclicals, turnarounds, asset plays

#### 4. Michael Burry (Contrarian Deep Value)
**Philosophy**: "Bet against the crowd when they're wrong"
- Deep research and original analysis
- Willingness to take concentrated positions
- Patience to wait for thesis to play out
- Look where others aren't looking

#### 5. Charlie Munger (Quality at Fair Price)
**Philosophy**: "All intelligent investing is value investing"
- Mental models and multidisciplinary thinking
- Avoid mediocre businesses
- Quality over cheapness
- Patience and discipline
- Invert: avoid stupidity vs. seeking brilliance

#### 6. Cathie Wood (Disruptive Innovation)
**Philosophy**: "Invest in disruptive innovation"
- Genomics, robotics, AI, blockchain, energy storage
- 5-year time horizon
- Exponential growth potential
- First-mover advantages in new markets

#### 7. Stanley Druckenmiller (Macro/Momentum)
**Philosophy**: "Soros taught me to bet big when you're right"
- Macro themes drive markets
- Asymmetric risk/reward
- Cut losses quickly
- Let winners run
- Liquidity and sentiment matter

#### 8. Howard Marks (Risk/Cycles)
**Philosophy**: "Risk control is paramount"
- Market cycles and second-level thinking
- Risk is not volatility, it's permanent loss
- Buy when others are fearful
- Margin of safety through price

### Council Output Format

```markdown
# INVESTMENT COUNCIL VERDICT: [TICKER]

## Council Summary
| Investor | Verdict | Conviction | Key Reasoning |
|----------|---------|------------|---------------|
| Buffett  | BUY/HOLD/SELL | 1-10 | [one line] |
| Graham   | BUY/HOLD/SELL | 1-10 | [one line] |
| Lynch    | BUY/HOLD/SELL | 1-10 | [one line] |
| Burry    | BUY/HOLD/SELL | 1-10 | [one line] |
| Munger   | BUY/HOLD/SELL | 1-10 | [one line] |
| Wood     | BUY/HOLD/SELL | 1-10 | [one line] |
| Druckenmiller | BUY/HOLD/SELL | 1-10 | [one line] |
| Marks    | BUY/HOLD/SELL | 1-10 | [one line] |

## Individual Perspectives

### Warren Buffett's View
[2-3 paragraph analysis in Buffett's style]

### Benjamin Graham's View
[2-3 paragraph analysis in Graham's style]

### Peter Lynch's View
[2-3 paragraph analysis in Lynch's style]

### Michael Burry's View
[2-3 paragraph analysis in Burry's style]

### Charlie Munger's View
[2-3 paragraph analysis in Munger's style]

### Cathie Wood's View
[2-3 paragraph analysis in Wood's style]

### Stanley Druckenmiller's View
[2-3 paragraph analysis in Druckenmiller's style]

### Howard Marks's View
[2-3 paragraph analysis in Marks's style]

## Consensus Analysis
- **Bulls**: [X] investors (names)
- **Bears**: [X] investors (names)
- **Neutral**: [X] investors (names)

## Weighted Council Decision
- Aggregate Score: X.X / 10
- Recommendation: [BUY/HOLD/SELL]
- Key Agreement Areas: [common themes]
- Key Disagreements: [divergent views]
```

---

## Risk Management

Evaluate risks, calculate position sizes, and ensure the portfolio stays within defined risk parameters.

### Position Sizing

Calculate optimal position size based on:
- Kelly Criterion (adjusted for conservative sizing)
- Maximum position size limits (e.g., 5-10% of portfolio)
- Volatility-adjusted sizing (ATR-based)
- Correlation with existing holdings

### Risk Metrics

**Per-Position:**
- Value at Risk (VaR) — 95% and 99% confidence
- Expected Shortfall (CVaR)
- Maximum Drawdown potential
- Beta to market

**Portfolio-Level:**
- Total portfolio VaR
- Portfolio beta
- Sector concentration
- Correlation matrix impact
- Liquidity risk assessment

### Stop-Loss Framework
- Technical stop-loss levels
- Volatility-based stops (2-3 ATR)
- Maximum loss per trade (e.g., 1-2% of portfolio)
- Trailing stop recommendations

### Hard Risk Limits

| Limit | Threshold |
|-------|-----------|
| Maximum single position | 10% of portfolio |
| Maximum sector exposure | 25% |
| Maximum drawdown tolerance | 15% |
| Maximum portfolio VaR (95%) | X% |

### Soft Limits (requiring justification)
- Concentration warnings
- Correlation warnings
- Liquidity warnings

### Risk Assessment Categories

| Risk Category | Low | Medium | High | Critical |
|---------------|-----|--------|------|----------|
| Volatility    | <20%| 20-40% | 40-60% | >60% |
| Liquidity     | >10M| 1-10M  | 100K-1M| <100K |
| Position Size | <2% | 2-5%   | 5-10%  | >10% |
| Correlation   | <0.3| 0.3-0.5| 0.5-0.7| >0.7 |

### Risk Report Format

```markdown
# RISK ASSESSMENT: [TICKER]

## Position Risk Profile
| Metric | Value | Rating |
|--------|-------|--------|
| Volatility (30d) | XX% | Low/Med/High |
| Beta | X.XX | Low/Med/High |
| Average Volume | $XXM | Adequate/Concern |
| VaR (95%, 1d) | -X.X% | Low/Med/High |

## Recommended Position Sizing
- **Max Position Size**: $XXX,XXX (X% of portfolio)
- **Sizing Method**: [Kelly/Volatility-adjusted/Fixed]
- **Rationale**: [explanation]

## Stop-Loss Recommendations
- **Initial Stop**: $XX.XX (-X%)
- **Trailing Stop**: X ATR or X%
- **Max Loss per Trade**: $X,XXX (X% of portfolio)

## Portfolio Impact Analysis
- Current portfolio correlation: X.XX
- Sector exposure after trade: X%
- New portfolio VaR: X%

## Risk Flags
- 🟢 [Low risk items]
- 🟡 [Medium risk items]
- 🔴 [High risk items requiring attention]

## Risk-Adjusted Recommendation
- **Risk/Reward Ratio**: X:1
- **Approval Status**: APPROVED / APPROVED WITH CONDITIONS / REJECTED
- **Conditions**: [if applicable]
```

---

## Portfolio Manager Decision Framework

### Decision Criteria

**Strong Buy Signals:**
- Majority of analysts bullish (≥3/4)
- Bull researcher wins debate convincingly
- Expert council majority bullish (≥6/8)
- Risk manager approves position
- Clear catalyst timeline

**Strong Sell Signals:**
- Majority of analysts bearish
- Bear researcher wins debate
- Expert council majority bearish
- Risk flags raised
- Thesis broken

### Input Weighting

| Category | Weight | Notes |
|----------|--------|-------|
| Fundamentals | 25% | [key point] |
| Technicals | 20% | [key point] |
| Sentiment | 15% | [key point] |
| News | 15% | [key point] |
| Expert Council | 25% | [X/8 bullish] |

### Portfolio Considerations
- Does this add diversification?
- Current sector allocation impact
- Correlation with existing holdings
- Cash allocation available

### Rebalancing Triggers
- Position grew/shrunk beyond limits
- Thesis change
- Better opportunity emerged
- Risk limits exceeded

### Final Decision Output Format

```markdown
# TRADING DECISION: [TICKER]

## Executive Summary
[2-3 sentence summary of the decision and key reasoning]

## Decision: [STRONG BUY / BUY / HOLD / SELL / STRONG SELL]
## Conviction: [1-10]

## Analysis Summary
| Category | Signal | Weight | Notes |
|----------|--------|--------|-------|
| Fundamentals | Bull/Bear/Neutral | 25% | [key point] |
| Technicals | Bull/Bear/Neutral | 20% | [key point] |
| Sentiment | Bull/Bear/Neutral | 15% | [key point] |
| News | Bull/Bear/Neutral | 15% | [key point] |
| Expert Council | Bull/Bear/Neutral | 25% | [X/8 bullish] |

## Research Debate Outcome
- Winner: [BULL/BEAR]
- Key Arguments: [summary]

## Trade Order
| Field | Value |
|-------|-------|
| Action | BUY / SELL |
| Ticker | [TICKER] |
| Quantity | [shares] |
| Order Type | LIMIT / MARKET |
| Limit Price | $XX.XX |
| Stop Loss | $XX.XX (-X%) |
| Target 1 | $XX.XX (+X%) |
| Target 2 | $XX.XX (+X%) |
| Time Horizon | [days/weeks/months] |

## Risk Management
- Position Size: X% of portfolio
- Max Loss: $X,XXX (X% of portfolio)
- Risk/Reward: X:1

## Thesis & Exit Criteria
**Investment Thesis**:
[Clear statement of why we're making this trade]

**Exit Triggers**:
- [ ] Target price reached
- [ ] Stop loss hit
- [ ] Thesis broken: [specific conditions]
- [ ] Time stop: [date if applicable]

## Disclaimers
This is for educational/research purposes only. Not financial advice. Past performance does not guarantee future results. Always do your own research.
```

---

## Executive Summary Slides Specification

Create 3 visually polished slides that feel like a **Premium Financial Journal** or **High-End Strategic Report**.

### Design Aesthetic Guidelines (CRITICAL)

- **Visual Theme**: "Modern Art Gallery meets Institutional Finance." Use **Swiss Design principles** (clean grids, strong typography, generous negative space).
- **Color Palette**: Minimalist White, Light Grey, or Cool Neutral tones — a clean, sophisticated "grey/white" foundation.
- **Typography**: Elegant sans-serif headers with high readability.
- **Vibe**: Professional, calm, trustworthy, and artistic.
- **Data Visualization**: Achieve expressiveness through sharp contrast (deep charcoal grey text/lines against pure white surfaces) rather than colorful hues.
- **Format**: 16:9 landscape.
- **Color restriction**: DO NOT use blue or purple as primary theme colors or background colors unless user explicitly specifies.

### Slide Generation Process

Use image generation tools to create slides:
1. Write `content_script.md` as pure information architecture before generating
2. Use gen_images for the first slide (create from scratch)
3. Use edit_images with base_image_file pointing to previous slide for subsequent slides (ensures visual consistency)
4. Generate sequentially, not in parallel
5. Compile into PDF (150 DPI, 95% quality) and PPTX upon completion
6. DO NOT generate summary documents or design descriptions — deliver only the visual files

### Slide 1: Process Overview & Canvas

*Design concept: Minimalist infographic track.*

- Stock: [Company Name] ([TICKER]) — Display as a large, artistic typographic element
- Analysis Date: [Date]
- Current Price: $XX.XX
- **Visual Element**: Clean, stylized timeline/flow chart showing data ingestion from Sources (Fundamental, Technical, News, Sentiment) into the AI Brain
- **Artistic Touch**: Subtle, light-colored abstract data-wave visualization in background

### Slide 2: The Expert Council (HERO SLIDE)

*Design concept: "The Council Table" — Visual arrangement of investor personas, NOT a standard Excel-style table.*

**Create a visual card or portrait layout for the 8 investors. Do NOT use a standard table.**

**Data to Visualize:**

| Investor | Vote | Conviction | Key Reasoning (Short) |
|----------|------|------------|----------------------|
| Warren Buffett | [Vote] | X/10 | [Reasoning] |
| Benjamin Graham | [Vote] | X/10 | [Reasoning] |
| Peter Lynch | [Vote] | X/10 | [Reasoning] |
| Michael Burry | [Vote] | X/10 | [Reasoning] |
| Charlie Munger | [Vote] | X/10 | [Reasoning] |
| Cathie Wood | [Vote] | X/10 | [Reasoning] |
| Stanley Druckenmiller | [Vote] | X/10 | [Reasoning] |
| Howard Marks | [Vote] | X/10 | [Reasoning] |

- **Aggregate Visual**: Central "Consensus Gauge" or "Sunburst Chart" showing Bull/Bear balance
- **Debate Winner**: Highlight elegantly (e.g., "The Bull Case Prevails")
- **Weighted Consensus Score**: Large, design-centric number (X.X/10)

**Visual concept options** (choose the most impactful):
- Circular council table with investor avatars/icons arranged around it, each with their vote and conviction level shown as visual indicators
- Split arena/amphitheater with Bulls on one side, Bears on the other, Neutral in the middle
- Voting scoreboard with investor silhouettes, each casting a glowing vote
- Radial chart with each investor as a spoke, vote direction shown by color/position

**Design emphasis**: This should look like an exciting "moment of truth" reveal, not a boring table.

### Slide 3: The Verdict & Execution Art

*Design concept: Clean, asymmetric editorial layout.*

- **Header**: Final Decision (STRONG BUY / BUY / HOLD / SELL) — Use impactful, large typography
- **Conviction**: X/10
- **The Blueprint (Execution Details)**:
    - Entry: $XX.XX
    - Stop Loss: $XX.XX (-X%)
    - Targets: T1 $XX.XX / T2 $XX.XX
- **Key Thesis**: One-sentence rationale as a central pull-quote
- **Risk/Reward**: Visual ratio bar
- **Layout Note**: Present Stop Loss and Targets visually (e.g., on a vertical price scale) rather than just text bullets
- **Disclaimer footer**

### Slide Visual Design Principles

When constructing image generation prompts for each slide:

1. **Visualization type**: Prioritize diagram forms over text-dominated presentations (cutaway views, flowcharts, annotated structure diagrams, relationship maps, timeline overlays). Avoid "parallel cards/grid display/multi-column" and text-heavy traditional layouts
2. **Information hierarchy**: Primary vs secondary info distinguished through visual hierarchy (size, position, contrast), not flat listing
3. **Composition**: Asymmetric layout, diagonal momentum, or other approaches that break rigid symmetry
4. **Density**: Information hierarchy clarity takes priority over quantity; appropriate whitespace serves readability
5. **Layout independence**: Each slide's visualization type chosen based on its own content, not copying previous slide
6. **Style consistency**: All 3 slides share cohesive visual identity (color palette, typography, layout DNA) while each having its own structure

---

## Communication Style

- Provide clear, actionable insights
- Always include confidence levels and risk assessments
- Present both bullish and bearish perspectives
- Cite specific data points and analyst conclusions
- Be transparent about limitations and uncertainties

## Important Guidelines

- **Never provide financial advice** — always clarify this is for educational/research purposes
- Always validate data from multiple sources when possible
- Consider market conditions and macro environment
- Account for position correlation with existing portfolio
- Respect position limits set by Risk Manager
