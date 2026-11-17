---
name: dual-ai-stock-analysis
description: Use for dual-AI (Hermes+OpenCode) stock analysis and debate.
version: 1.0.0
author: Hermes Agent
license: MIT
category: finance
tags: [stock, dual-ai, opencode, debate, finance]
---

# Dual-AI Stock Analysis + Debate

> ⚪ 可选技能：需要 OpenCode 或 Pi 协作（双 AI 独立分析＋辩论）。
> 没有也不卡死 —— 用单模型复核替代（见本技能"诚实标注"条），流程照常走。

Do a stock analysis where Hermes and OpenCode work independently, then debate their
disagreements over a fixed number of rounds, ending in concrete operating advice.
This is the class of task: "你和 opencode 分别分析 XX 这只股票，辩论三轮，给操作建议。"

## 🔴 Execution Discipline (highest priority)

**This section outranks everything else in this skill. On conflict, this section wins.**

### 1. Never-skippable items

| # | Item | What breaks if skipped |
|:-:|---|---|
| 1 | 🔴 Run `date "+%Y-%m-%d %A"` FIRST, before any data search. Use THAT as today. | Stale date → data that isn't today's → user corrects you |
| 2 | 🔴 Hermes pulls data independently → OpenCode pulls independently → **cross-check cell-by-cell BEFORE writing any analysis** | One unverified dataset poisons the whole report |
| 3 | 🔴 **The comparison MUST appear in the user-facing output.** Silent comparison is insufficient | User wants to trust the process, not just the conclusion |
| 4 | 🔴 **Per-point verification**: every day needs close + change% + main-force flow from **≥2 independent sources**. Mark single-source cells with a footnote. | User has corrected individual bad figures (right change%, wrong flow) |
| 5 | **Debate capped at 3 rounds**, one disagreement point each. Do not force consensus. | Fake debate is worse than honest disagreement |
| 6 | **Conclusions first, table-driven, no verbose prose** | Violates standing report style |
| 7 | 🔴 **Every report ends with operating advice + risk warnings** + 「仅供参考，不构成投资建议」 | Analysis without actionable next step is incomplete |

### 2. Skill-specific red lines

- 🔴 **Never average conflicting prices** — pick the dated authoritative source.
- 🔴 **Never present single-AI output as "dual-AI"**: if OpenCode times out twice, label it honestly (e.g. "Hermes单AI分析（OpenCode超时）") and state the independent search was unavailable. Do NOT block on the subagent.
- 🔴 **Numerical disputes (MA/RSI/MACD/stop) are arbitrated by the host independently** — recompute from the pre-fetched 10–15 day fqkline. Claims like "MA20 needs more data" are usually evasion; the window can be back-derived.
- 🔴 **Never retry the same failing search query twice** — switch phrasing or source site.
- 🔴 **Weekly analysis needs all 5 trading-day rows + a weekly aggregate row.** Search per-day by keyword (`<code>` `<月>月<日>日` 主力资金); never the whole week in one query. A day you can't find → mark "data unavailable", do **not** omit the row.
- 🔴 **Gate-style stock tasks deliver two documents per ticker**: ① 走势裁决报告 (both sides' verbatim excerpts, 裁决表 = 争议项×两方取值×裁定+理由, 分歧与不确定性, 数据源) ② 交易计划 (评级, 统一技术位表, 金字塔式分批表, 盯盘表 = 触发→判断→动作, 催化剂日历, 风险提示). Delete the .md source after PDF conversion.
- 🔴 **Multi-ticker batch = sequential pipeline** (one ticker fully through debate→verdict→documents before the next); only pre-verification may be batched.
- The three global hard rules live in `a-share-investment-workflow`《执行纪律》: ① skill_view first ② never silently skip a mandatory item ③ stop and report on missing data.

### 3. Closing self-check

- [ ] `date` run and its value used as today; "this week"/"next week" ranges computed from it and stated in the header
- [ ] Both sides pulled data independently; cross-check section **shown to user**
- [ ] Single-source cells footnoted
- [ ] Debate reflects genuine disagreement (or honestly says there was none)
- [ ] Verdict + entry range + stop-loss + target + risk list all present
- [ ] Honest label if only one AI's data was obtained

## Hard rules (apply to every instance)

1. **Confirm today's date FIRST, before any data search.**
   Run `date "+%Y-%m-%d %A"` in terminal and use THAT as "today". Do not trust the
   conversation start date, compacted session context, or old filenames — a stale
   date makes the data "not today's" and the user will correct it. Re-run `date`
   at the start of each fresh analysis request.
   *Why: the user corrected a wrong-date data search twice in one session.*

   **When the user says "this week" or "next week", compute the range from TODAY**,
   not from a previously discussed date. Example: if today is Sunday 09-13, "this
   week" = Mon 09-07 to Fri 09-11. Always state the computed range explicitly in
   the report header so the user can verify it matches their intent.

2. **Independent data first, then cross-check, then analyze — in that order.**
   - Hermes searches/verifies the stock's data (close, change %, volume, main
     net flow, turnover) via web_search/web_extract on its own.
   - OpenCode searches independently via a delegate_task subagent.
   - Compare the two datasets cell-by-cell and flag every discrepancy BEFORE
     writing any analysis. Do NOT merge data silently and do NOT start the debate
     on a single unverified dataset.
   *Why: the user explicitly wants to see the data compared so wrong figures are
   caught early instead of poisoning the whole report.*

   **The comparison MUST appear in the user-facing output** — a short
   "数据交叉验证" section listing any discrepancies found (or "两方数据一致" if none).
   Silent comparison without showing the user is insufficient; the user wants to
   trust the process, not just the conclusion.

   **Per-point verification is mandatory**: for each day in the range, verify
   close price AND change % AND main-force net flow from at least two independent
   web sources (e.g. 证券之星 + 新浪财经 or Investing.com). The user has corrected
   individual data points that a single source got wrong (e.g. correct change %
   but wrong main-force flow). A data table with a single source per cell is
   insufficient — mark cells whose figures come from only one source with a
   footnote, and prioritize sources with explicit dates in the URL/title
   (证券之星 daily fund-flow articles are the most reliable per-day source).
   Never present a number the user can cross-check against a public quote as
   "verified" when it came from one snippet.

3. **Debate is capped (default 3 rounds).** Each round targets one specific point
   of disagreement (e.g. main-force outflow = washout vs distribution; valuation;
   entry level). At the end of each round, state which facts are independently
   verified, which views remain disputed, and whether the disagreement could change
   the decision; do not force consensus. The debate is driven by real data gathered
   in step 2, not invented positions.

4. **Conclusions first, table-driven, no verbose prose.** Lead each section with
   the rating/verdict, put numbers in tables, follow with a short "what to do next".
   *This is the user's standing report style — see memory.*

5. **Every report ends with explicit operating advice + risk warnings**: rating
   (buy/hold/avoid), entry range, stop-loss, target, and a risk list. Never
   deliver analysis without the actionable next step.

6. **门禁式股票任务按两份文档交付**（每只标的各一份对）：① 走势裁决报告
   （双方原文摘录、裁决表=争议项×两方取值×主持人裁定+理由、分歧与不确定性、
   数据源）；② 交易计划（总评级、统一技术位表、金字塔式分批表、盯盘表=
   触发→判断→动作、催化剂日历、风险提示）。用户要 PDF 时转完删 MD 源文件。
   文件存 `$STOCK_DATA_DIR/`（文件名含标的名+代码+日期）。
   多只标的批量时：顺序流水线（一只走完三轮+裁决+落文档再开下一只），
   但预核验（代码/全称+K线锚点）可批量一次做完。

## Workflow

1. `date` → fix today, and "this week" / "next week" ranges from it.
2. Hermes independent data pull (web_search/web_extract; 证券之星, 新浪财经,
   Investing.com, 东方财富 are reliable sources for A-share 688xxx quotes).
3. OpenCode independent data pull (delegate_task subagent, isolated context —
   pass the codes and date range explicitly). Let it run in the background;
   do NOT poll. Reconcile when its result returns.
4. Cross-check the two datasets; list discrepancies; resolve before analysis.
5. Write each side's analysis (technical + fundamental + market sentiment),
   save to files (e.g. `/opt/data/<stock>_hermes.md`, `/opt/data/<stock>_opencode.md`).
6. Run the capped debate on the disagreeing points; save the debate log.
7. Produce the final report: verdict table, operating advice, risk warnings,
   data-source note with timestamps, and the disclaimer "仅供参考，不构成投资建议".

## Pitfalls

- **数值类分歧（MA/RSI/MACD/止损位谁算对）由主持人独立重算裁决，不让辩手互辩收场**：用预抓的 10-15 日 fqkline 自行重算各方主张值——以某日为终点的 N 日窗口收盘价和是固定的，宣称的 MA 值可被算术直接证伪（"MA20 缺数据无法计算"常是对方回避，窗口可回推）。判定哪方正确后，把核验值写进下一轮任务卡"双方已核实/认可的事实（直接用）"区块让双方锁定，不再纠缠；确实无法复核的数值取"保守表述+标注存疑"，不硬判。
- **辩手 API 限流/超时的重试模式（本批验证 3 次）**：pi 撞 429（免费额度）时，重试改用"离线快速版"——把已核实事实+已收敛值写进 instruction、注明"不要联网、快速出稿"，比原样重发完整任务成功率高得多；opencode 上游超时（`Upstream request timed out`）时，重试同时精简 instruction（上轮要点压成列表）——长指令是超时主因，原样重发大概率再超。各按失败纪律只重试 1 次，仍失败才标缺席。
- **delegate_task to OpenCode often times out (420s) on the first call.** Retry
  once; if it times out again, proceed with Hermes-only data and **state explicitly
  in the report that the OpenCode independent search was unavailable** — do NOT
  present the analysis as "dual-AI" when only one side searched. Label the report
  honestly (e.g. "Hermes单AI分析（OpenCode超时）"). Do NOT block the whole
  analysis on a subagent that will not return.
- **MCP tool calls must be validated with tool_describe before use** when using
  the OpenCode MCP backend.
- **Price figures drift across sources** (e.g. a 600000 quote of ~17 vs 21).
  This is exactly why step 4's cross-check exists — never average conflicting
  prices, pick the dated authoritative source.
- Do not present a "debate" where both sides say the same thing as a fight; the
  rounds must reflect genuine disagreement, or say so honestly.
- **web_search backends rotate** (Exa / Firecrawl / keyless MCP), and individual
  calls fail intermittently with 403 or shape errors. Do NOT retry the same
  failing query more than once — switch to a different phrasing or a different
  source site (证券之星 daily articles, 搜狐财经, Investing.com historical data
  pages) rather than hammering one backend. Batch independent queries into a
  single turn to reduce total calls.
- **Weekly analysis must include per-day rows for all 5 trading days** (Mon–Fri),
  plus a weekly aggregate row (week change %, weekly high/low, weekly main-force
  net flow total). A report that only has 2–3 days of data is incomplete and
  the user will notice. If a day's data cannot be found after a genuine search
  attempt, mark that row "data unavailable" rather than omitting the row.
  - **Search by date keyword per day**: for each trading day, search
    "`<stock code>` `<month>月<day>日` 主力资金" to find the 证券之星 daily
    article. Do NOT search for the whole week in one query — per-day queries
    return more precise results.
  - **The 证券之星 weekly review (周评) article** (search "`<stock code>` 周评
    本周") gives the week aggregate AND the week high/low dates in one call.
    Use it as the anchor, then fill per-day details from individual daily articles.
- **The user's correction pattern is "the X number is wrong, not today's"** —
  when the user flags a specific figure, re-verify ONLY that figure immediately
  (one targeted search), acknowledge the error, and update the report section
  that contains it. Do not restart the whole analysis from scratch.

## Data-source reliability ranking (A-share 688xxx daily quotes)
Useful when web_search backends fail and you must pick where to look:
0. **Tencent Finance real-time API** (`https://qt.gtimg.cn/q=sh{code}` or `sz{code}`)
   — no auth, no rate limit, returns real-time price / volume / turnover / P/E /
   market cap / timestamp in one call. Split the response on `~` to parse fields.
   Use this FIRST for any "today's quote" check — web_search is NOT reliable
   for live A-share prices (cached pages show stale dates).
   For historical bars use akshare:
   `uv pip install akshare` in a venv, then
   `ak.stock_zh_a_hist(symbol='600000', period='daily', start_date='20260810', end_date='20260916', adjust='qfq')`.
   **Faster no-auth alternative for a 10–15 day anchor (preferred for pre-verification):**
   `https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param=sz{code},day,,,{count},qfq`
   returns an array of `[date, open, close, high, low, volume(手)]` rows plus a
   `qt` realtime block in ONE call — no venv, no akshare install. Use this to pull
   the K-line anchor for a task card or cross-check. Two caveats: (a) the dead
   controller `web.ifzq.gtimg.cn/app/kline/kline?param=...` 404s with
   "Can't load controller:KlineController" — use the `appstock/app/fqkline/get`
   path instead; (b) the last row (today) comes back raw/unadjusted, earlier rows
   are qfq — don't mix the two when computing a MA.
   East Money fund-flow API (`stock_individual_fund_flow`) is often unstable
   (RemoteDisconnected) — retry at most 2–3 times, then mark unavailable
   rather than blocking the report on it.
1. **证券之星 daily fund-flow articles** (`stock.stockstar.com/RBYYYYMMDD*.shtml`)
   — one article per stock per day, contains close, change %, turnover %, volume,
   main/hot-money/retail net flow, and a 5-day flow table. Most reliable per-day
   source; search by "`<code>` `<date>` 主力资金".
2. **搜狐财经 股市必读** (`sohu.com`) — close + change % + volume, with the
   closing date in the title; good for a second source on price figures.
3. **新浪财经 实时行情页** (`finance.sina.com.cn/realstock/...`) — timestamped
   quotes, useful for confirming intraday vs closing values.
4. **Investing.com / Google Finance historical pages** — close + change, but
   often a day behind or showing a stale cached quote; use as a tie-breaker,
   not a primary source.
5. **东方财富周评** (`stock.stockstar.com` weekly review, e.g. "周评：本周涨
   12.83%") — gives the weekly aggregate in one shot; verify it matches your
   per-day sum before trusting it.

## Related skills
- `finance-stock-technical-analysis` (user-owned): indicator formulas + report
  template — reuse its formula reference and table layout, but note it cannot be
  patched by the curator; keep class-level date/dual-data rules here.
- `opencode-evidence-report` (user-owned): evidence requirements for reporting
  OpenCode task outcomes.
- `hermes-opencode-workflow` (user-owned): OpenCode MCP fallback mechanics.
