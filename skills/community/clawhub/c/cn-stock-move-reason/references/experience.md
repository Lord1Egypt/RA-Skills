# CN Stock Analysis Experience

Purpose: keep reusable lessons for A-share analysis without forcing the model to read a growing archive every time.

## Active Playbook

Read this section before using the CN stock skill. Keep it compact and current.

### Current Core Rules

- Separate confirmed catalysts from market imagination. Announcements, orders, earnings, regulatory approvals, and company filings outrank 股吧 narratives.
- For every sharp move, explicitly compare `prior market expectation` versus `actual news`: what the market was pricing, what actually landed, whether it is above expectation, merely landed/in line, or below expectation. Apply this to numeric news such as orders, earnings, guidance, policy size, and buybacks, and to qualitative news such as wording strength, timing, certainty, regulatory tone, management confidence, and whether the announcement solves the market's real concern.
- Judge the move in context: market breadth, sector rank, concept strength, and whether the stock is leading, following, or diverging from its sector.
- For direct A-share questions such as `怎么看`, `该不该卖`, `能不能拿`, `要不要加`, or `是不是弱了`, always give a `个股-板块-大盘` assessment before the final view: individual price/volume and relative strength; sector/concept trend, leader/follower status, and回流/退潮; broad-market index, breadth, and emotion-cycle state. Explicitly state whether weakness is systematic, sector-led, or stock-specific.
- When an A-share answer uses macro/flash-news, technical, or sentiment reasoning, call the corresponding sibling skill instead of folding that layer into this skill ad hoc: `macro-news-check` for 宏观/快讯, `stock-technical-analysis` for 技术面, and `stock-sentiment-analysis` for 情绪面/期待差. State the fusion layers in the final answer when they materially affect the conclusion.
- When a sell/hold decision involves valuation, separate `fundamental fair value`, `theme/emotion premium or discount`, and `technical invalidation`. Do not let a fair or cheap valuation override a broken short-term structure, and do not let a short-term break automatically imply fundamental overvaluation.
- Treat 股吧 and Eastmoney Guba topic heat as expectation-gap, topic-discovery, and emotion data, not as fact. High-read posts and hot topics can reveal what the market is pricing or which board/theme investors are attaching to the stock, but ordinary posts and topic heat are only sentiment until confirmed by price action, announcements, or formal news.
- For high-theme stocks, classify whether the stock is an `情绪票`, `趋势票`, or hybrid. Do not use the same risk rules for all three.
- In `高潮期` and `高位分歧/分化期`, do not assume good industry logic protects the stock from short-term drawdown. Watch turnover, long upper shadows, failed boards, and back-row weakening.
- A weak stock during a strong sector day is an important negative signal unless there is a clear one-off reason such as a small insider reduction, financing issue, or other announcement overhang.

### A股情绪结构框架

- 先定市场状态，再定股票位置：当前是进攻、防御、轮动、退潮，股票属于主线、助攻、补涨、防御、老龙反抽，还是杂质噪音。
- 主线不是单日涨幅最大，而是资金高频回流、连续性强、扩散充分、板块内大多数成分有赚钱效应；只有少数高标强而后排不跟，更多是高端情绪局。
- 用资金回流频率判断强弱：隔一两天反复回流的方向强于隔五六天才回流的方向。慢回流方向可以等，但节奏要匹配，不要提前太多导致心态被主线干扰。
- 主线第一次健康分歧可能是`倒车接人`，但倒车接人是关键节点，不是每天都有。错过后要么等下一次分歧/新主线，要么承认自己进入快进快出的追强模式。
- 高潮或弱转强之后，下一步要预案`强上强`和`强转分歧`两种路径。新开仓避免在高潮日盲目追高；已在车上则看赚钱效应是否继续扩散。
- 机构盘和游资盘分开处理：机构盘常见趋势反复回流、板块大面积赚钱；游资盘是PK强弱、强转弱就跑，若不会PK容易接到弱化资金的卖盘。
- 进攻阶段做进攻，防御阶段做防御。进攻主线未衰竭时提前买防御，容易等不动；主线高位释放资金后，再观察助攻、防御、老龙谁先承接。
- 主线走弱后的承接含义不同：助攻方向抢到资金，可能说明指数仍强；防御方向抢到资金，可能说明市场进入调整；老龙反抽常是出货/扰动信号，不宜当作新主线。
- 不要提前和下一条假想主线绑定。候选方向在启动前地位平等，谁在关键节点率先走出连续性和扩散，再跟随谁。
- 强指数/强量能会提高纠错力，掩盖弱板块的问题；一旦市场从普涨转为结构行情，更要回到主线、扩散、回流、赚钱效应这些脉络。
- 对补涨保持阶段感：指数强时补涨很多，可能可做但不要误认成新主线；同频跟涨主线的票，风险也常与主线龙头同频释放。
- 情绪分析不等于追高。可以用情绪结构找主线和分歧低吸点，风格上仍以稳定套利、低买高卖为主。

### Reasonable Valuation Framework

Use this section when the user asks whether a stock is cheap/expensive, asks for fair value, target range, upside/downside, or valuation after earnings.

- First classify the stock: 情绪票, 趋势票, 周期股, 成长股, 资产/资源股, 平台型公司, or mixed. Do not value all stocks with the same PE.
- Build at least three anchors: `earnings anchor` such as forward EPS/PE, `quality anchor` such as margin/ROE/cash flow/order durability, and `market anchor` such as comparable A-share/HK/US/Japan multiples and current theme premium.
- Treat equity valuation as `price = EPS x PE` when using earnings multiples. A Davis double play needs both EPS upgrades and PE expansion, usually because earnings visibility, growth duration, industry cycle, main-line status, or shareholder return improved. A Davis double kill means EPS cuts and PE compression arrive together; downside can be much larger than the profit downgrade alone.
- In each scenario, state both the EPS assumption and the deserved PE assumption. Explain whether the market is paying for near-term EPS, future EPS upgrades, multiple expansion, emotion premium, or a combination.
- Before calling a low PE stock cheap, reconcile operating profit, recurring/core profit, net income, and EPS. If net income is lifted by asset sales, investment/security gains, tax effects, impairment reversals, or subsidy/accounting noise, value the stock on normalized operating/core profit and show the gap versus headline PE.
- For low PB or low PE small caps, test for a value trap separately from business improvement. Strong earnings can still deserve a low multiple when liquidity is thin, payout is very low, governance is passive, capital allocation is weak, or management gives no buyback/dividend/capital-efficiency signal.
- For limit-up, sharp-move, and post-announcement valuation in A-shares, map the catalyst into `confirmed earnings/order`, `capital policy`, `theme premium`, or `forum/social speculation`; use a lower deserved PE for speculation-only moves and require explicit execution milestones before moving from base to bull scenarios.
- For A-shares, explicitly separate fundamental value from emotion-cycle premium. In 高潮期/高位分歧, the stock can trade above reasonable value; in退潮, even good fundamentals may trade below it.
- Adjust EPS and valuation for buybacks, placements, convertible bonds, equity incentives, large impairment, one-off gains, and major capital expenditure.
- Separate operating quality from accounting noise. For hardware/materials leaders, revenue mix, gross margin, backlog/orders, capacity release, and customer validation can matter more than one-quarter net profit; for cyclical stocks, price/FX sensitivity should lower the multiple.
- Use scenario valuation instead of a single point: conservative, base, and bull. State the key assumptions that move the stock from one scenario to another.
- After setting the fair range, compare current price to the range and explain whether the market is pricing current fundamentals, future upgrades, sector theme, or pure emotion.
- For `该不该卖` or `能不能拿` follow-ups, translate valuation into timeframe-specific action meaning: whether current price has enough margin of safety for a medium-term holder, and whether it protects a short-term or leveraged position.
- Valuation output should end with a "what must happen to justify upside" test and a "what invalidates the valuation" test.


- For reusable sentiment lessons that apply across markets, update `stock-sentiment-analysis/references/experience.md` as the shared layer, then keep only market-specific details here.

## Compression Protocol

Keep this file readable by compressing before it becomes too large.

- Always read only `Active Playbook` first.
- If a new lesson repeats an existing rule, merge it into the existing bullet instead of appending.
- Keep `Active Playbook` under about 120 lines. When it grows beyond that, rewrite it into fewer higher-signal bullets before adding new material.
- Move detailed older examples into `Archive` only if they still teach a distinct rule. Otherwise delete the detail after preserving the rule.
- Never paste long raw source output here. Store only distilled lessons, dates, tickers, and the rule learned.
- Do not store personal positions, watchlists, unpublished research notes, credentials, cookies, private URLs, or any content that should not be committed to a public repository.

## Conversation Learning Protocol

Use this protocol after multi-turn discussion about the same stock.

- Auto-update experience only when the follow-up reveals a reusable lesson, such as a missed catalyst type, wrong source priority, poor sector共振 framing, bad emotion-cycle judgment, overconfidence, or a recurring output weakness.
- Decide scope before writing: if the lesson applies to both A-shares and Japanese stocks, update both stock-skill `references/experience.md` files; if it relies on A-share-specific sources, rules, or market structure, update only this file.
- Do not update for one-off ticker facts, ordinary user preferences, speculative claims without support, or information that is only useful for the current stock.
- Convert the correction into a general rule before writing it. Prefer one concise bullet in `Active Playbook`; use `Archive` only for distinct dated examples that still teach the rule. The ticker may appear only as a compact example in `Archive`, never as the center of the active rule.
- If the lesson came from a user challenge, capture the analytical failure mode, not the user's private wording. Example: write "When a stock is weak on a strong sector day, explicitly test for stock-specific overhang", not a transcript of the exchange.

## Archive

- 2026-05-11 从一份A股板块讨论转写稿中提炼了情绪结构规则；具体板块和个股观点已删除，只保留可复用的方法。
- 2026-05-15 Added a generalized expectation-gap rule: compare prior expectation with actual numeric and qualitative news before explaining a sharp move, and treat forum/news heat as evidence of what was priced rather than proof of fact.
- 2026-05-19 Added mandatory fusion rule: macro/flash-news, technical, and sentiment layers must route to their sibling skills when used.
