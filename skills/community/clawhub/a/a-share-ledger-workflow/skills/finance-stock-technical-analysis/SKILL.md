---
name: finance-stock-technical-analysis
version: 1.0.0
author: Hermes Assistant
license: MIT
category: finance
description: Use for stock technical work. Create indicator reports.
---

# Finance Stock Technical Analysis

## 🔴 Execution Discipline (highest priority)

**This section outranks everything else in this skill. On conflict, this section wins.**

### 1. Never-skippable items

| # | Item | What breaks if skipped |
|:-:|---|---|
| 1 | **Follow the full fallback chain**: OpenCode MCP → akshare (venv) → web_search/web_extract → placeholder | Silent single-source data with no fallback |
| 2 | 🔴 **Calculate on adjusted (前复权) prices** | Split/dividend distortion |
| 3 | **Use sufficient warm-up history** (typically from Jan 1 of current year or earlier) before taking latest values | Wrong MA/RSI/MACD from insufficient sample |
| 4 | 🔴 **Compute all indicators in code, never from memory or by hand** | Silent numeric errors |
| 5 | **Verify the trading calendar** — exclude weekends and holidays | Fabricated non-trading days in the table |
| 6 | **风险提示 must include all four**: 支撑失效 / 量能陷阱 / 基本面未评估 / 数据时效性与指标滞后性 | Report is unusable |
| 7 | **Save report to the designated folder** with `[名称]_[代码]_YYYYMMDD-YYYYMMDD_技术分析.md` | Report can't be found later |

### 2. Skill-specific red lines

- 🔴 **Never average conflicting indicator values** — resolve via price behaviour (K-line, support/resistance, volume). Some platforms multiply MACD by 2; that's a convention difference, not a real disagreement.
- 🔴 **All fetches fall back automatically**; if every automated method fails, produce the placeholder report and **clearly mark the missing data sections** — never present partial data as complete.
- 🔴 **This skill is purely technical.** It does NOT assess fundamentals, industry景气度, or policy. Any such request must be combined with other skills.
- 🔴 **Never recommend a trade from technicals alone** — output is 仅供参考, not 投资建议.
- ⚠️ **qfq caveat**: with the Tencent fqkline endpoint, the last row (today) comes back raw/unadjusted while earlier rows are qfq — don't mix the two when computing a MA.
- The three global hard rules live in `a-share-investment-workflow`《执行纪律》: ① skill_view first ② never silently skip a mandatory item ③ stop and report on missing data.

### 3. Closing self-check

- [ ] Full fallback chain attempted, data source named
- [ ] Indicators computed on 前复权 prices, in code, with proper warm-up
- [ ] Trading calendar verified (no weekends/holidays in the table)
- [ ] All four 风险提示 categories present
- [ ] Conclusions first, table-driven; saved to the designated folder
- [ ] Not presented as fundamental analysis or as a trade instruction

## When to Use
Use when the user requests technical analysis for one or more stocks (e.g., "分析某标的本周表现", "给我看看它的技术指标", "比较这些股票的走势"). The request may specify a time period (e.g.,本周, 上月, 具体日期范围) or default to the most recent completed week.

# Finance Stock Technical Analysis

Perform technical analysis on individual stocks or a list of stocks for a given time period. This skill encapsulates the workflow of fetching stock data, calculating key technical indicators, generating a structured analysis report, and resolving discrepancies between data sources or analytical approaches through a structured debate (if needed). Reports are saved in a designated folder with clear naming conventions.

## Workflow

### 1. Data Acquisition
- **Primary**: Attempt to fetch daily OHLCV (Open, High, Low, Close, Volume) data for the specified stock(s) and time period using OpenCode via MCP (if available and authorized). This leverages the OpenCode agent's ability to call financial APIs (e.g., Tencent Finance, Sina Finance) and compute technical indicators.
- **First Fallback**: If OpenCode MCP fails (e.g., connection issues, authentication errors, insufficient data) or returns incomplete data, switch to using `akshare` in a Python virtual environment. Install `akshare` if necessary (via `uv pip install akshare` in a venv) and fetch data using `stock_zh_a_hist` or similar functions.
- **Second Fallback**: If akshare fails or is unavailable, use web search (`web_search`) and web extraction (`web_extract`) to gather historical price data from financial websites (e.g., Investing.com, Sohu Finance, East Money), then parse into a structured format.
- **Tertiary Fallback**: If all automated methods fail, create a structured placeholder report based on available historical data or user-provided data points, clearly marking missing data sections.

### 2. Technical Indicator Calculation
For each stock, calculate the following indicators using sufficient historical data (typically starting from January 1 of the current year or earlier) to ensure proper warm-up:
- Moving Averages: MA5, MA10, MA20 (simple moving averages)
- Relative Strength Index: RSI14 (Wilder's smoothing)
- MACD: DIF (EMA12 - EMA26), DEA (EMA9 of DIF), Histogram (DIF - DEA)
- Bollinger Bands: Upper = MA20 + 2 * standard deviation, Lower = MA20 - 2 * standard deviation (population standard deviation over the lookback period)
Ensure all calculations are performed on adjusted (前复权) prices to account for splits and dividends.

### 3. Report Generation
For each stock, produce a markdown report with the following sections:
- **数据来源**: Note the primary source used (e.g., Tencent Finance via OpenCode MCP, akshare, web extraction).
- **原始日线OHLCV**: Table showing Date, Open, High, Low, Close, Change %, Volume (in 万手 or shares).
- **技术指标**: Table showing Date, MA5, MA10, MA20, RSI14, DIF, DEA, MACD Hist, Bollinger Upper, Bollinger Lower (values as of each close).
- **周汇总** (if applicable): Week Open, Week Close, Weekly Change %, Week High, Week Low, Range, Week Volume, Avg Daily Volume, Up Days, Volume Path (daily volume sequence).
- **分析**:
  - 价格行为：描述趋势（如盘整、突破、反转）、测试的支撑/压力位、缺口、K线形态。
  - 成交量：解读量能趋势（如上涨放量、下跌缩量、量价关系、异常放量）。
  - 动能：评估RSI（超买/超卖）、MACD（金叉/死叉、柱状图变化）。
  - 关键位置：列出即时阻力位、即时支撑位、均线关系、心理整数位。
- **底线综述**：给出明确的偏见（看多/看空/中性）、关键观察点、风险/回报设置。
- **风险提示**：必须包括：
  - 支撑失效风险：若跌破关键支撑，下方支撑强度及潜在目标位。
  - 量能陷阱：持续放量下跌将确认趋势转弱，反弹可能是陷阱。
  - 基本面未评估：本报告仅限技术面，未考察公司业绩、行业景气度或政策影响。
  - 数据时效性：分析基于截至某日期的收盘数据，盘中异动及次日开盘可能迅速改变技术面貌。
  - 指标滞后性：MACD、MA等趋势指标本质滞后，在转折点可能发出错误信号。
- **操作建议**（可选）：根据分析给出的具体策略（如激进/保守进场点、止损位、目标位、仓位建议）。
- **数据来源与免责声明**：注明数据来源时间点、计算方法，并声明分析仅供参考，不构成投资建议。

### 4. Discrepancy Resolution (if applicable)
When multiple data sources or analytical methods yield conflicting results (e.g., different indicator values from OpenCode vs. akshare, or divergent trend interpretations):
- 暂停并列出具体分歧点（如MACD符号、RSI数值、趋势判断）。
- 模拟结构化辩论：双方各自陈述理由，基于价格行为（K线形态、支撑压力位、量价关系）寻求共识。
- 达成共识：明确哪些指标值得信赖，哪些因数据深度或计算惯例差异而失效，并以价格行为为主要依据。
- 输出带有‘风险提示’的决策书：包含共识结论、操作建议和必读的风险提示。

### 5. Report Storage
Save each report in the designated folder (default: `$STOCK_DATA_DIR/reports/`) with a filename in the format:
`[股票名称]_[代码]_YYYYMMDD-YYYYMMDD_技术分析.md`
For weekly reports, use the Monday-Friday date range of the week (e.g., `20260820-20260826`). Ensure the folder exists; create it if necessary.

## Configuration
- **Python Environment**: Use a virtual environment (e.g., `/tmp/venv` or under `~/hermeswebui/`) for akshare to avoid system-wide package conflicts.
- **OpenCode MCP**: Ensure the MCP opencode tool is configured and authorized (requires valid ModelScope token). If not available, the workflow will automatically fall back to akshare or web extraction.
- **Fallback Order**: OpenCode MCP → akshare → web extraction → manual input (if user provides data).

## Notes
- Prioritize price behavior over indicator values when discrepancies arise due to calculation conventions (e.g., some platforms multiply MACD by 2).
- Always verify the trading calendar: exclude weekends and holidays from analysis.
- For indices or ETFs, adjust data fetching methods accordingly (e.g., use指数 codes in akshare).
- This skill does not perform fundamental analysis; it is purely technical. If fundamental factors are requested, combine with other skills (e.g., research, finance-news-briefing).
- The user prefers concise, table-driven reports with conclusions first. Avoid lengthy explanations; let the tables and bullet points convey the analysis, followed by a clear bottom line.

## Example
User prompt: "分析某标的本周的表现，然后把数据发给你、由你（Hermes）来独立完成技术分析。对比双方结果，若有分歧，强制OpenCode就分歧点与你进行3轮限时辩论，最终输出带有‘风险提示’的决议书。"
Skill execution:
1. Use OpenCode MCP to fetch 示例标的 (600000) data for Aug 20-26, 2026 and compute indicators.
2. Independently fetch data via akshare and compute indicators.
3. Compare results, note discrepancies in MACD sign and RSI interpretation.
4. Simulate a 3-round debate focusing on price action, volume, and key levels.
5. Produce a consensus report with risk warnings and decision summary.
6. Save as `$STOCK_DATA_DIR/reports/<标的>_<代码>_<起止日期>_技术分析.md`.

## References
- See `references/technical_indicator_formulas.md` for detailed calculation formulas.
- See `templates/report_template.md` for a starter report structure.