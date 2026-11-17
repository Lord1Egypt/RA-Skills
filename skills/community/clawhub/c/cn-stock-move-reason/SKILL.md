---
name: cn-stock-move-reason
description: Use when analyzing why one A-share stock moved sharply using Codex, without Gemini, from Eastmoney quote data, announcements, Eastmoney 股吧/资讯 posts, Eastmoney Guba topic heat, Sohu index/sector context, and A-share breadth.
metadata:
  short-description: Analyze A-share move reasons from announcements, 股吧, index/sector context, and emotion cycle
---

# CN Stock Move Reason

Use this skill when the user asks why one A-share stock is rising, falling, 涨停, 跌停, 炸板, 异动, or moving unusually, and wants Codex to analyze it instead of Gemini.

The bundled script is safe for a public repository: it uses only public web pages/APIs, does not read credentials, and does not call any LLM service. Never commit personal information, API keys, account data, private RAG files, or private research materials to GitHub.

The skill accepts one stock at a time. It may also collect broad market context (indexes, sector/concept boards, and advance/decline counts) to judge whether the move is market-wide, sector-led, or stock-specific.

## Workflow


## Public And Private Versions

If both public and private versions of this skill exist, prefer the private version for local analysis when the user permits it. The private version may use local RAG indexes and user-specific study material.

When updating the skill, keep public and private versions in sync: write public-safe, generalized lessons to the public version; keep private labels, private paths, raw notes, screenshots, account data, and personal trade context only in the private version or private RAG index.

When preparing a GitHub upload or public release, use the public version only and run the repo-level release/privacy check from the repository root at `shared/references/release-and-privacy.md`. Never upload private RAG folders, `.ftindex` files, credentials, `.env`, personal data, screenshots, raw PDFs/PPTs, or private strategy labels.


1. Read `references/experience.md` before analysis, but only the `Active Playbook` and `Compression Protocol` sections unless the user explicitly asks for historical lessons. Apply those lessons when judging catalysts, sector共振, 股吧 emotion, A-share emotion-cycle position, and the stock's place in the market structure: 主线、助攻、补涨、防御、老龙反抽, or noise. When the request needs a deeper or reusable sentiment framework, also use `stock-sentiment-analysis` and its `references/sentiment-framework.md`.

   Cross-skill calls are operational. When this workflow says to use another market skill, actually load that skill's `SKILL.md` and required references if the skill is installed or available as a sibling in this repository. Do not merely mention the other skill by name in the answer.

   Required coordination: for A-share analysis, use this skill as the evidence-gathering entry point, and add supporting skills based on clues found during analysis, not only on the user's wording. 股吧 itself is an evidence source, not an automatic trigger for sentiment analysis. If 股吧/资讯/news reveals a concrete clue about main-line status, crowding, attack/defense rotation, leader/follower position, or emotion-cycle phase, load `stock-sentiment-analysis` to test that clue. If 股吧/资讯/news discusses the broad market, index pressure, policy/liquidity, FX/rates, commodities, overseas markets, or geopolitical drivers, load `macro-news-check` to verify the tape instead of accepting forum claims. If 股吧/资讯/news or the price move points to support/resistance, failed breakout, trend damage, or catalyst acceptance/rejection, load `stock-technical-analysis` to verify the chart. When the original question is directly about an index/broad tape such as 上证、深成指、创业板、科创50、A50、恒生科技/港股 spillover, load `macro-news-check` by default.

   Mandatory execution gate:
   - If the answer uses **宏观** or **快讯** to explain the stock, sector, index, liquidity, policy, FX/rates, commodities, overseas spillover, or geopolitics, load `macro-news-check`. Do not replace this layer with ad hoc web search.
   - If the answer uses **技术面** such as support/resistance, trend confirmation, failed breakout, volume-price behavior, intraday timing, or "能不能上/下", load `stock-technical-analysis`.
   - If the answer uses **情绪面** such as main-line status, crowding, emotion cycle, leader/follower, risk-on/risk-off, expectation gap, or forum psychology, load `stock-sentiment-analysis`.
   - Final answers should include a compact `融合口径` line when any supporting skill is used, e.g. `东财/公告/股吧证据 + macro-news-check tape + stock-technical-analysis 结构 + stock-sentiment-analysis 情绪周期`.

   Optional 东方财富妙想 enhancement: if the user has installed the `mx-*` A-share/financial skills in the current session or under the local skills directory, use them as a non-blocking data layer for A-share move reasons, sector mapping, valuation, financials, and current news checks. MX data supplements the existing know-how; it must not replace the normal Eastmoney/Guba/announcement collector, source hierarchy, A-share emotion-cycle framework, expectation-gap analysis, or technical/macro confirmation. If an `mx-*` skill is missing, unauthorized, over quota, or returns empty data, continue with the normal collector/web workflow and do not claim that 妙想 data was used. You may briefly suggest installing or configuring 东方财富妙想 skills only when the missing layer would materially improve the user's exact request, such as A-share sector constituents, self-selected-stock filtering, timely financial data, or official finance-data search.

   Use the 妙想 skills this way:
   - `mx-data`: current/historical quotes, market cap, PE/PB, EPS/ROE/margins, share count, main-fund flow, index/sector/board quote data, and A-share financial statement metrics for valuation.
   - `mx-search`: latest news, announcements, research reports, policies, event explainers, and time-sensitive market/sector context.
   - `mx-xuangu`: sector constituents, concept-board candidates, peer lists, condition screens, and "same theme but stronger/weaker" comparisons. For A-share questions such as `这个板块有哪些股票`, `相关股`, `概念股`, `龙头股`, `板块成分`, or `同题材还有谁`, try `mx-xuangu` first when available, then use `mx-data`/`mx-search` to rank purity, heat, and catalysts.
   - `mx-zixuan`: only when the user explicitly asks to query/add/delete/filter their 东方财富 self-selected stocks. For `自选股里哪些符合条件`, first try a direct `mx-xuangu` query constrained to self-selected stocks; if unsupported, use `mx-zixuan` to get the self-selected list and intersect it with `mx-xuangu` results. Do not use it automatically for ordinary analysis because it touches user account data.
   - `mx-moni`: only when the user explicitly asks about simulated portfolio holdings, funds, orders, simulated buy/sell, cancel orders, or posting a simulated-trading note. Do not use it for real trading or ordinary analysis.

   Eastmoney Guba topic enhancement: when the stock's sector/theme reason is unclear, or when a move may be part of a broader A-share topic rotation, check `https://gubatopic.eastmoney.com/` as an optional topic-discovery layer. Use it to identify current market hotspots, possible next-day continuations, and what topics, concepts, or boards the market is discussing, then verify with actual stock/sector moves, announcements, formal news, and the collector output. Treat Guba topic heat as sentiment/topic evidence, not confirmed fact.

2. Run the collector script from the repository root:

```bash
python3 skills/cn-stock-move-reason/scripts/stock_move_sources.py 600519 --format markdown
```

Useful options:

- `--hours 24`: evidence window.
- `--posts 100`: maximum Eastmoney 股吧/资讯 rows to include. The default is 100.
- `--announcements 10`: maximum announcements to include.
- `--skip-market-context`: skip indexes, sector/concept boards, and advance/decline counts when the user wants only single-stock materials.

3. If network access fails in Codex, rerun the same command with sandbox escalation according to the normal approval policy. In this local environment, the collector may fail inside the sandbox with DNS-style errors such as `nodename nor servname provided, or not known`, `urlopen error`, or repeated empty Eastmoney/Sohu results. Treat those as sandbox/network failures, not as evidence that there is no announcement, 股吧 discussion, or market-context data. Escalate and rerun before concluding that sources are empty.

4. Analyze the script output directly. Do not call Gemini. Treat sources with this priority:

- Announcements, earnings, regulatory filings, and confirmed company materials: primary evidence.
- 妙想 `mx-data` / `mx-search` outputs, when available, can supplement or cross-check quote, financial, announcement, research, and event evidence. Use them as evidence with source attribution, but still distinguish official filings from media/research interpretation.
- Eastmoney 股吧资讯/high-read posts: secondary evidence; useful for discovering what the market is discussing.
- Eastmoney Guba topics (`https://gubatopic.eastmoney.com/`): secondary topic-discovery evidence; useful for mining possible themes and board-level reasons behind A-share moves, but must be verified against stock/sector price action and formal news.
- Sohu index and sector/concept board context plus Eastmoney intraday advance-decline counts and Sohu historical advance-decline / limit-up / limit-down data: market/sector backdrop only; use it to judge 共振 versus 独立催化.
- Ordinary 股吧 posts: emotion and speculation only. Never treat them as confirmed fact unless the same item appears in announcements/news.
- Macro tape: call `macro-news-check` only when the move may be affected by broad A-share risk appetite, policy/liquidity headlines, PBOC/CNY, commodities, US rates, Hong Kong/US China ADR moves, geopolitical risk, or sudden index/sector-wide news. Use it to judge market-wide pressure or support, not to replace announcements or stock-specific evidence.

5. Prefer this skill as the first pass for A-shares. When using `stock-sentiment-analysis`, `macro-news-check`, or `stock-technical-analysis`, first finish the stock-specific evidence read, then use the supporting skill to verify sentiment structure, broad-market pressure/support, or price confirmation. Do not replace confirmed announcements or filings with macro, sentiment, or chart evidence.

6. In multi-turn discussions about the same stock, treat user follow-ups as possible new evidence or feedback. If the user adds information, challenges the reasoning, asks for reconsideration, or the conversation reveals that the prior answer missed/misweighted something, re-evaluate the stock with the new context before defending the earlier answer.

7. If the analysis or multi-turn correction produces a durable reusable lesson, update experience after answering. First decide scope: if the lesson applies to both A-shares and Japanese stocks, update both stock-skill `references/experience.md` files and consider `stock-sentiment-analysis/references/experience.md`; if it is specific to A-shares, update only this skill. Follow the `Conversation Learning Protocol` and `Compression Protocol`: generalize the lesson, merge repeated lessons into the active summary, keep the active section short, and move only distinct older details into the archive.

## A-share Emotion Cycle

Classify the short-term emotion backdrop qualitatively into one of seven stages from the single-stock materials, price action, 股吧 discussion, market indexes, sector/concept boards, today's breadth, and recent Sohu zdt history:

1. `冰点期`: many limit-downs or large losers, high failed-board/亏钱效应, shrinking participation. Observe who resists the selloff.
2. `修复/潜伏期`: panic eases, limit-downs decrease, front-row names begin to rebound, but most traders are still skeptical. Small trial positions only.
3. `启动期`: new theme appears, first/second boards increase, capital starts focusing. Prefer front-row names in the core theme.
4. `加速期`: leaders continue limit-up, followers spread, sector赚钱效应 is strong. Hold strength, avoid random laggards.
5. `高潮期`: everyone discusses the theme, limit-up wave or one-word boards, retail emotion is hot. Take profits progressively; do not chase heavily.
6. `高位分歧/分化期`: after高潮, leaders may炸板/断板/long upper shadow while back-row names weaken, but the whole market has not fully collapsed yet. Treat it as the transition from emotion top to退潮.
7. `退潮期`: leaders break down, 天地板/核按钮 rise,亏钱效应 spreads. Reduce exposure or wait.

Useful loop: `冰点 -> 修复/潜伏 -> 启动 -> 加速 -> 高潮 -> 高位分歧/分化 -> 退潮 -> 再冰点`.

`分歧` is not always bearish. A healthy divergence during 启动/加速 can be a换手 test or main-line pullback before renewed agreement; a high-level divergence after高潮 is usually a risk signal. The favorable windows are usually late 修复 to early 启动, and healthy main-line divergence before 加速. The most dangerous windows are late 高潮, 高位分歧/分化, and early 退潮.

## Reading News And Emotion

- Separate `confirmed catalyst` from `market imagination`. A confirmed order, policy, earnings beat, regulatory approval, or buyback is stronger than a forum narrative.
- For each meaningful catalyst, do an expectation-gap check: `市场原来预期什么` -> `实际消息落地什么` -> `超预期 / 符合预期或只是落地 / 不及预期`. This applies to numeric news such as orders, earnings, guidance, policy size, and buybacks, and to qualitative news such as wording strength, timing, certainty, regulatory tone, management confidence, and whether the news solves the market's real concern.
- Use the emotion-structure checklist from `references/experience.md`: classify market phase, main-line versus defensive bucket, capital return frequency, breadth/赚钱效应, first healthy divergence versus high-level divergence, institution-style trend versus 游资PK, and whether a rebound is new leadership or old-leader exit liquidity.
- Decide whether the stock is an `情绪票` or a `趋势票`:
  - 情绪票: topic-driven, high volatility, limit-up relay, fast climax/retreat.
  - 趋势票: supported by industry cycle, earnings, policy, or institutional logic; slower but more durable.
- Watch for emotional-top clues: high attention, continuous large candles, high turnover, failed breakout, long upper shadow, break-board/炸板, or broad follower exhaustion.
- Watch for trend-risk clues: good news priced in, valuation stretch, volume-price divergence, loss of key moving averages, or gradual weakening after a crowded story.

## Output Style

Reply in Chinese unless the user asks otherwise. The answer can be detailed because this is a single-stock local script workflow. Use this order:

1. `最有力理由`: most likely catalyst, with source names and timing.
2. `补助理由`: secondary drivers such as theme, sector rotation, liquidity, valuation, or positioning.
3. `共振判断`: whether the stock is moving with the market, its sector/concept, or mostly on stock-specific news.
4. `情绪面/周期位置`: qualitative 股吧 emotion plus the seven-stage A-share emotion cycle.
5. `确定度`: high / medium / low, with one sentence explaining why.
6. `注意点`: what remains unconfirmed or what could invalidate the read.

If evidence is weak, say so plainly and use wording like `思惑`, `低信息量`, `未确认`, or `确认待ち`. Do not invent catalysts absent from the collected evidence.

## Valuation Requests

When the user asks for `合理估值`, `目标价`, `估值`, `贵不贵`, `空间`, `fair value`, or similar:

- Still collect current quote/news/公告/股吧/market-context materials first, then add financial guidance, EPS/share-count, capital policy, and peer/sector context when available.
- Use the `Reasonable Valuation Framework` from `references/experience.md`.
- Provide scenario ranges rather than one exact target: conservative / base / bull.
- State the anchors used, such as forward EPS/PE, operating profit, ROE/PB, EV/EBITDA, orders/backlog, buyback/convertible bond dilution, and peer multiples.
- When using EPS/PE, explicitly decompose price into `EPS x PE`: judge whether the setup is a Davis double play (`EPS upgrades + PE expansion` from better growth/certainty/theme premium) or Davis double kill (`EPS downgrades + PE contraction` from weaker guidance/cycle reversal/expectation miss). Do not call a stock cheap from PE alone if EPS or the deserved multiple is falling.
- Explicitly separate fundamental fair value from A-share emotion-cycle premium/discount.
- Explicitly say what the current price already prices in, what must happen to justify upside, and what would invalidate the valuation.
