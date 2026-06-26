---
name: mall-market-overview
description: 生成 mall.yy.com / gamemarket.yy.com 游戏账号行情与挂牌数据报告。用于查看市场行情、最近交易行情、挂牌行情、价格分布和账号交易数据。触发词：游戏账号行情、账号行情、账号价格行情、最近交易行情、游戏交易行情、账号交易数据、挂牌数据、账号挂牌数据、价格数据、行情报告、挂牌数据分析、账号价格分析、账号市场分析、mall.yy.com 行情、mall.yy.com 数据。例如“我想看看王者荣耀账号最近的交易行情”应使用此 skill。
---

# 游戏账号行情与挂牌数据

Use this skill when the user asks for mall.yy.com game account 行情, recent trading 行情, account listing data, 挂牌数据, 价格数据, 账号交易数据, 行情报告, or account price analysis. Keep 大盘 as a weak match, but prioritize 行情 and 数据 wording.

## 路由边界

Use this skill for market-level 行情 and listing-data intent, such as 最近交易行情、账号交易行情、游戏账号行情、挂牌行情、挂牌数据、价格分布、市场数据、行情报告、账号市场分析.

Example requests that should use this skill:

- 我想看看王者荣耀账号最近的交易行情
- 查一下王者荣耀账号挂牌数据
- 看看和平精英账号价格分布
- 给我一份游戏账号行情报告

Do not use this skill when the user wants to evaluate one specific account, such as 我的号值多少钱、帮我估价、账号估值、游戏号估价. Use `game-valuation` for those requests.

## Bundled scripts

Use the bundled scripts in this skill directory:

- `scripts/fetch_mall_trade_data.py`: fetches public mall.yy.com listing samples as JSON.
- `scripts/generate_market_overview.py`: converts fetched JSON into a Markdown行情 report.

The scripts do not use cookies, login tokens, or user-provided browser session headers.

## Defaults

- Default page size: 20
- Default pages per sort: 2
- Sort profile: all
- Sort perspectives:
  - `baseline`: 综合排序
  - `recent`: 最新发布
  - `high_price`: 价格最高

If the user says 快速看下, use `--pages-per-sort 1`.
If the user says 深度分析, use `--pages-per-sort 5`.
If the user names games, pass each game with repeated `--game` arguments.

## Workflow

1. Decide target games and depth from the user's request.
2. Run `scripts/fetch_mall_trade_data.py` and save JSON to `/tmp/mall-market-overview-YYYYmmdd-HHMMSS.json`.
3. Run `scripts/generate_market_overview.py` on that JSON.
4. Return the Markdown report directly.
5. Mention that the report is based on listing samples and does not represent 成交价.

## Commands

Default all-game 行情 report, from the skill directory:

```bash
python3 scripts/fetch_mall_trade_data.py --page-size 20 --pages-per-sort 2 --sort-profile all > /tmp/mall-market-overview.json
python3 scripts/generate_market_overview.py /tmp/mall-market-overview.json
```

Single-game quick report:

```bash
python3 scripts/fetch_mall_trade_data.py --game 王者荣耀 --page-size 20 --pages-per-sort 1 --sort-profile all > /tmp/mall-market-overview.json
python3 scripts/generate_market_overview.py /tmp/mall-market-overview.json
```

## Output rules

- Return the generated Markdown report directly.
- Do not paste raw JSON unless the user explicitly asks.
- Do not persist cookies, login headers, or browser tokens.
- Include detail links in sample rows when `goodsId` is present.
- State the JSON path only when useful for traceability or when the user asks for raw data.
