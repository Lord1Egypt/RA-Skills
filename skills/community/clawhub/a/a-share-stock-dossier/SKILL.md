---
name: a-share-stock-dossier
description: Analyze A-share stocks and portfolios with analyst-grade, evidence-first reports. Use when the user asks for 个股分析、持仓复盘、逻辑是否还在、行业龙头、盘前/盘后策略、情绪+技术综合判断, especially when they want deep web verification and full process transparency (检索过程摘要 + 证据逐条分析) via web_search/web_fetch/browser plus Eastmoney/Tencent quote data.
---

# A-Share Stock Dossier

## Overview
Produce professional analyst-style stock reports that are **process-transparent, evidence-bound, and directly executable**.
Always split conclusions into two layers:
- 产业逻辑（fundamental/industry logic）
- 交易逻辑（price/flow/sentiment logic）

Default output mode is **long-form process report** unless user explicitly asks for a short summary.

## Workflow

### Step 1) Fix scope and objective
- Extract stock list, cost, position size, horizon (日内 / 次日 / 5-10日), and risk preference.
- Confirm output mode:
  - 单票深挖
  - 组合分层（A/B/C）
  - 盘前执行单
- If screenshot is provided, parse first; ask only missing fields.

### Step 2) Pull structured baseline before any narrative
Run:

```bash
python skills/a-share-stock-dossier/scripts/a_share_snapshot.py \
  --codes 603618,002149,002506,002475,002729,601116,601096 \
  --with-indices --with-kline --kline-days 60 --pretty
```

Lock objective facts first:
- Price/pct/range/volume/turnover
- 5d/10d/20d return
- MA5/MA10/MA20/MA60 context
- Index mood and breadth proxy

Field reference:
- `references/eastmoney-fields.md`

### Step 3) Run deep-search loop (before and during writing)
Use:
- `references/source-checklist.md`
- `references/search-depth-protocol.md`

Mandatory minimum evidence per stock:
1. Structured quote/kline data
2. One official source (CNINFO/exchange/company IR)
3. One mainstream finance source
4. One sector/leader verification source

Tool order:
- `web_search` discover
- `web_fetch` extract正文
- `browser` for JS-heavy/anti-bot/paginated/incomplete extraction

### Step 4) Maintain retrieval log (hard requirement)
During analysis, build a step log `S1..Sn`.
Each step must include:
- 检索目标（why this search）
- 查询/页面（query/url）
- 摘要（1-3条关键事实）
- 来源等级（官方/主流媒体/社区）
- 对判断影响（supports/weakens/conflicts）

If a conclusion appears without supporting steps, do not keep it in final recommendations.

### Step 5) Write stock analysis in fixed order
For each stock, output strictly in this order:
1. 公司业务与收入/应用场景定位
2. 当前市场叙事与叙事阶段（启动/强化/分歧/退潮）
3. 行业龙头与板块阶段（强度/轮动/分化）
4. 技术面（趋势、关键位、失效位）
5. 舆情与事件（利多/利空/争议）
6. 双逻辑判断
   - 产业逻辑：在 / 弱化 / 失效
   - 交易逻辑：在 / 弱化 / 失效
7. 明日三情景（强/中/弱）触发条件 -> 动作
8. 证据绑定（E1/E2/E3/E4）+ 置信度

Use template:
- `references/report-template.md`

### Step 6) Continuous-search triggers during writing
Pause and re-search immediately if:
- only one source supports a key claim
- key event is stale (>7 days) and no update is checked
- price/volume behavior conflicts with narrative
- wording becomes uncertain（可能/大概/据说）
- sector leader list mismatches same-day board behavior

### Step 7) Conflict resolution and stop rule
- Unify basis first (timestamp, adj/non-adj, intraday/close)
- Priority: official > exchange data > mainstream media > community
- If unresolved, keep explicit uncertainty notes

Stop searching only when:
1. each core conclusion has >=2 sources and >=1 official/preferred source
2. recent two re-search rounds add no high-value facts
3. conflicts are either resolved or explicitly marked

### Step 8) Portfolio decision + self-correction
After all stocks:
- Rank A/B/C:
  - A: 产业逻辑与交易逻辑同向
  - B: 产业逻辑在、交易逻辑弱
  - C: 交易逻辑受损
- Give one-line portfolio action (cut/hold/wait + why)
- Add self-correction:
  - 2-3 weak points in this round
  - how to recalibrate thresholds next round

## Output requirements (must follow)
Default to detailed analyst-report style with this top-level structure:
1. 检索过程纪要（S1..Sn）
2. 市场底色（结构化数据）
3. 逐股深度分析（证据逐条绑定）
4. 组合分层与执行重点
5. 本轮不确定性与下轮修正计划

Never output only short conclusions unless user asks explicitly.
