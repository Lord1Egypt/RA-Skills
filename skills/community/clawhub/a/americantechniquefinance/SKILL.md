---
name: us-tech-giant-analyst
description: This skill should be used when a user asks to analyze a US-listed technology giant such as Apple, Microsoft, Nvidia, Amazon, Alphabet, Meta, or Tesla. It produces a deep, data-rich, and visually structured investment-and-competitive analysis with charts and valuation tables, covering business model, market share, growth prospects, technology moat, financial reports, and stock price trend. Trigger when the user asks to analyze, evaluate, compare, or profile a big-tech company's fundamentals, earnings, competitive position, or stock performance.
version: 1.1.0
---

# US Tech Giant Analyst

## Overview

This skill turns a vague request like "分析一下英伟达" or "How is Apple positioned versus Microsoft?" into a deep, six-part company analysis. It gathers the latest public data through web search and renders a data-rich, visually structured report — a core summary card block, six analytical sections, a valuation comparison table, a risk matrix, and inline charts — that an investor, strategy analyst, or student can act on. The skill never fabricates numbers: every figure is traced to a fetched source and dated, and gaps are stated explicitly.

The report must go beyond listing facts. Each section delivers a judgment backed by specific numbers, and the report includes charts and comparison tables so the depth is visible, not merely asserted.

## When to Use

Activate this skill when the user:

- Names a US tech giant and asks for an analysis, evaluation, breakdown, or profile.
- Uses trigger phrases such as "分析", "评估", "护城河", "商业模式", "市场占额", "财报", "股价走势", "前景", "analyze", "evaluate", "moat", "earnings", "stock trend", "compare A vs B".
- Wants a competitor comparison across the six dimensions below.
- Asks for a plain-language explanation of why a company is winning or losing.

Do not activate for: non-US companies (unless explicitly framed as a comparison), private startups without public filings, or pure stock-trading execution (this skill informs, it does not place orders).

## Execution Logic

Follow this workflow for every request.

### Step 1 — Scope the request

Identify the target company (ticker or name) and which of the six dimensions the user wants. If the user asks broadly ("分析一下 Nvidia"), cover all six. If they ask narrowly ("Nvidia 的股价走势"), focus but still give a one-line context for the other five.

### Step 2 — Gather fresh AND deep data

Use web search and web fetch to collect, for the current year, at minimum:

Core financials (latest quarter and latest full year):

- Revenue, net income, gross margin, operating margin, free cash flow, and guidance — from the company investor-relations page, SEC 10-K / 10-Q / 8-K, or reputable outlets.
- Historical trend: the last 4-5 fiscal years of annual revenue and net income (to render a trend chart or table).

Market and competitive:

- Segment-level market share from industry reports (IDC, Canalys, StatCounter, Gartner, Omdia, TrendForce, Jon Peddie Research, Silicon Analysts). Give the exact share and note the methodology caveat (e.g., "including vs excluding custom silicon").
- Nearest competitors and their shares, laid out as a comparison table.

Valuation and capital markets:

- Forward/trailing P/E, PEG, P/S, compared against 2-4 peers in a table.
- Stock: latest close, 52-week range, year-to-date move, market cap, mean/high/low analyst targets, rating distribution.

Moat and prospects:

- Latest product / R&D / ecosystem / supply-chain moves, switching costs, patents, capacity or supply locks.
- Management commentary, secular tailwinds, and 3-5 concrete risks, each with a rough probability and impact.

Prefer primary sources (SEC filings, IR pages) over secondary. Record the source URL and the data date next to every figure. If a number cannot be found, write "未找到公开最新数据" rather than guessing.

### Step 3 — Analyze, do not just summarize

For each dimension, state a judgment supported by numbers:

- Business model: how the company makes money (revenue mix by segment with percentages), and what changed recently.
- Market share: the company's position, trajectory (gaining/losing), and the nearest competitor.
- Growth prospects: the 2-3 year thesis and the main upside/downside drivers.
- Technology moat: the durable advantage (scale, network effects, IP, integration, data, supply lock) and how defensible it is.
- Financial reports: health read from margins, cash flow, balance sheet, and how results compare with consensus.
- Stock trend: direction and key levels, framed as context — never as investment advice.

### Step 4 — Render a DEEP, VISUAL report

Produce two artifacts:

1. A markdown report (archival / citable) using the six-section template in `references/analysis-framework.md`.
2. A polished, self-contained HTML report (no external libraries or CDN) as the primary deliverable, containing:
   - A header with ticker, data date, latest price, market cap, mean analyst target, and buy-rating share.
   - A "核心摘要" (core summary) card block: 4-6 key stats plus a one-sentence verdict and 5 bullet takeaways.
   - The six sections, each expanded with sub-structure and concrete numbers.
   - At least three charts (CSS or inline SVG only): a market-share donut, a revenue-trend bar chart, a segment-mix stacked bar, and/or a 52-week range bar.
   - A valuation comparison table versus peers and a risk matrix (probability x impact).
   - A "data sources & dates" footer and a short disclaimer (analysis, not investment advice).

## Output Structure

The report must contain these six headings (in this order), prefixed by a core summary and closed by risks and sources:

0. **核心摘要 (Core Summary)** — key stats cards + one-sentence verdict + takeaways.
1. **商业模式 (Business Model)**
2. **市场占额 (Market Share)**
3. **发展前景 (Growth Prospects)**
4. **技术壁垒 (Technology Moat)**
5. **财报表现 (Financial Reports)**
6. **股价走势 (Stock Price Trend)**
7. **估值对比 (Valuation vs Peers)** — P/E, PEG, P/S table.
8. **主要风险 (Key Risks)** — risk matrix.

Close with **数据来源与日期 (Sources & Dates)**. A worked example lives in `references/analysis-framework.md`.

## Depth Requirements

Before finishing, verify the report satisfies ALL of the following:

- [ ] Core summary card block with 4+ key figures and a one-sentence verdict.
- [ ] Every section contains at least one concrete number plus one judgment (not just a summary).
- [ ] 5-year revenue / net-income trend, as a chart or table.
- [ ] Valuation table versus 3+ peers (P/E, PEG, P/S).
- [ ] Risk matrix with 4+ risks, each tagged with probability and impact.
- [ ] 3+ inline charts with no external library.
- [ ] Every figure carries a source and date; nothing fabricated.

If any item is unchecked, gather more data and re-render before delivering.

## Reliability Rules

- No fabricated figures. Every quantitative claim cites a fetched source and date.
- State the data date prominently; tech and stock data go stale fast.
- Do not give personalized investment advice; frame outputs as analysis and context.
- If the request spans multiple companies, produce one section block per company, then a comparison table.
- The HTML report must be self-contained (no CDN / external JS), so it renders offline.

## Resources

- `references/analysis-framework.md` — the deep six-section template, source checklist, chart requirements, and a fully worked Nvidia example.
