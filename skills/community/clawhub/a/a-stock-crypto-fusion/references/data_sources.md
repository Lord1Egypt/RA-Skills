## Data Sources & How to Fetch (for tool authors)

This skill expects structured JSON. If you wire live data, here is a tested snapshot (2026-03-11). Do not hardcode/emit any keys. CryptoPanic needs user token; other sources are public.

### Python deps
- 推荐：`python3 -m pip install -r scripts/requirements.txt`
- 最小依赖：`akshare ccxt pandas requests`（pandas 会带 numpy）

### Out-of-the-box fetch scripts
- Crypto: `python3 scripts/fetch_crypto.py --symbol BTC/USDT`
- A-share: `python3 scripts/fetch_ashare.py --code 600519`
- Morning brief: `python3 scripts/fetch_morning.py --date 20260311`
- Optional news only: `python3 scripts/fetch_news.py --base BTC --limit 5` (needs `CRYPTOPANIC_TOKEN` or `--token`)

### Crypto (ccxt public endpoints)
- Use `ccxt.binanceusdm()`.
- Unified symbol on USDM is usually `BTC/USDT:USDT` (note the `:USDT`); the provided script accepts `BTC/USDT` and normalizes it.
- Tested (2026-03-11):
  - `fetch_ticker` keys: symbol, timestamp, datetime, high, low, bid, bidVolume, ask, askVolume, vwap, open, close, last, previousClose, change, percentage, average, baseVolume, quoteVolume, markPrice, indexPrice, info
  - `fetch_ohlcv` rows: [timestamp, open, high, low, close, volume]
  - `fetch_l2_order_book` keys: symbol, bids, asks, timestamp, datetime, nonce

Suggested crypto JSON shape (placeholders only):
```json
{
  "symbol": "BTC/USDT",
  "current_price": <number>,
  "ema20_on_5m_chart": <number>,
  "indicators_15m": {"rsi": <number>, "macd": {"histogram": <number>}, "kdj": {"k": <number>, "d": <number>, "j": <number>}},
  "indicators_1h": {"rsi": <number>, "macd": {"histogram": <number>}, "ema200": <number>},
  "market_cycle_indicators": {"15m": {"bb_width": <number>, "atr": <number>, "phase": "broad_channel|range|breakout"}, "1h": {"bb_width": <number>, "atr": <number>, "phase": "..."}},
  "order_book_analysis": {"pressure_ratio": <number>, "top_support_levels": {"<price>": <size>}, "top_resistance_levels": {"<price>": <size>}},
  "micro_structure_analysis": {"cvd_analysis": {"cvd_10m_usd": <number>, "cvd_slope_direction": "upward|downward|flat"}, "large_trade_flow": {"net_large_trade_flow_usd_10m": <number>, "dominant_side": "buy|sell|neutral"}, "absorption_analysis": {"status": "Sell Absorption (Bullish)|...", "strength": "strong|weak|none"}},
  "derivatives_data": {"funding_rate": <number>, "open_interest_usd": <number>, "open_interest_change_24h_percent": <number|string>, "long_short_ratio": <number|string>},
  "taker_volume_analysis": {"taker_buy_volume_usd_500trades": <number|string>, "taker_sell_volume_usd_500trades": <number|string>, "taker_ratio_500trades": <number|string>},
  "vpvr_analysis": {"1h": {"poc": <number>, "hvn": [<number>], "lvn": [<number>], "value_area": {"vah": <number>, "val": <number>}}, "15m": {"poc": <number>, "hvn": [<number>], "lvn": [<number>], "value_area": {"vah": <number>, "val": <number>}}}
}
```

### Crypto news (requires user token)
- Endpoint: `https://cryptopanic.com/api/developer/v2/posts/?auth_token=<TOKEN>&public=true&currencies=BTC&kind=news`
- Note: `size` param not available on Developer plan (returns api_error). Omit `size`.
- Minimal normalized item shape:
```json
[
  {"title": <string>, "published_at": <iso8601>, "source_name": <string>, "votes": {"positive": <int>, "negative": <int>, "important": <int>}}
]
```

### A股 (akshare public)
- 单股实时要素（更稳）：`stock_individual_info_em(symbol="600519")`
- 单股盘口（买卖五档）：`stock_bid_ask_em(symbol="600519")`
- 全市场实时行情: `stock_zh_a_spot_em()` 或拆分 `stock_sh_a_spot_em/stock_sz_a_spot_em/stock_bj_a_spot_em`（偶发远端断开，可重试）。
- 指数行情备源: `stock_zh_index_spot_em(symbol="沪深重要指数")`, 备 `stock_zh_index_spot_sina()`（偶发远端断开，可重试）。
- 个股资金流: `stock_individual_fund_flow`
- 个股新闻: `stock_news_em(symbol="600519")`
- 研报: `stock_research_report_em(symbol="600519")`
- 财务摘要: `stock_financial_abstract(symbol="600519")`
- 筹码分布: `stock_circulate_stockholder`（或版本可用的筹码接口）
- 机构龙虎榜: `stock_lhb_jgzz_sina`（备 `stock_lhb_jgmmtj_em`）
- 行业/主力资金流: `stock_fund_flow_industry(symbol="即时")`，备 `stock_sector_fund_flow_rank(indicator="今日", sector_type="行业资金流")`
- 涨停池: `stock_zt_pool_previous_em(date=YYYYMMDD)`，备 `stock_zt_pool_em()`
- 财经早餐/快讯: `stock_info_cjzc_em()`，备 `stock_info_global_em/ths/futu/sina`
- 历史日线: `stock_zh_a_hist(..., period="daily", adjust="qfq")`
Verified columns (2026-03-11):
- `stock_fund_flow_industry`: 序号, 行业, 行业指数, 行业-涨跌幅, 流入资金, 流出资金, 净额, 公司家数, 领涨股, 领涨股-涨跌幅, 当前价
- `stock_zt_pool_previous_em`: 序号, 代码, 名称, 涨跌幅, 最新价, 涨停价, 成交额, 流通市值, 总市值, 换手率, 涨速, 振幅, 昨日封板时间, 昨日连板数, 涨停统计, 所属行业
- `stock_zt_pool_em`: 序号, 代码, 名称, 涨跌幅, 最新价, 成交额, 流通市值, 总市值, 换手率, 封板资金, 首次封板时间, 最后封板时间, 炸板次数, 涨停统计, 连板数, 所属行业
- `stock_lhb_jgzz_sina`: 股票代码, 股票名称, 累积买入额, 买入次数, 累积卖出额, 卖出次数, 净额
- `stock_lhb_jgmmtj_em`: 序号, 代码, 名称, 收盘价, 涨跌幅, 买方机构数, 卖方机构数, 机构买入总额, 机构卖出总额, 机构买入净额, 市场总成交额, 机构净买额占总成交额比, 换手率, 流通市值, 上榜原因, 上榜日期
- `stock_info_cjzc_em`: 标题, 摘要, 发布时间, 链接
- `stock_info_global_em`: 标题, 摘要, 发布时间, 链接
- `stock_info_global_ths`: 标题, 内容, 发布时间, 链接
- `stock_info_global_futu`: 标题, 内容, 发布时间, 链接
- `stock_info_global_sina`: 时间, 内容
Suggested A股 analysis JSON shape:
```json
{
  "stock_name": <string>,
  "stock_code": <string>,
  "quote_data": {"最新价": <number>, "市盈率-动态": <number>, "市净率": <number>, "换手率": <number>, "成交量": <number>},
  "technical_indicators": {"rsi_14": <number>, "bollinger_bands": {"status": <string>}, "kdj": {"k": <number>, "d": <number>, "j": <number>}, "macd": {"dif": <number>, "dea": <number>, "macd_hist": <number>}, "volume_ratio": <number|string>},
  "fundamental_data": {"company_profile": {"main_operation_business": <string>, "org_cn_introduction": <string>}, "business_composition": [{"主营构成": <string>, "主营收入": <number>, "主营利润": <number>, "毛利率": <number>}], "gross_profit_margin": <number|string>},
  "fund_flow_data": [{"日期": <string>, "主力净流入": <number>}],
  "chip_distribution_data": {"获利比例": <number>, "平均成本": <number>, "90集中度": <number>},
  "stakeholder_data": {"institutional_holdings": [<string>], "institutional_participation": [<string>]},
  "market_sentiment_data": {"hot_keywords": [<string>], "user_attention": <number>, "participation_desire": <number>},
  "news_and_reports_data": {"latest_news": [<string>], "research_reports": [<string>]},
  "order_book_data": {"buy_1": <number|string>, "sell_1": <number|string>}
}
```

### Morning briefing data (akshare combo)
- 指数：`stock_zh_index_spot_sina` (备 `stock_zh_index_spot_em`)
- 行业资金：`stock_fund_flow_industry` (备 `stock_sector_fund_flow_rank`)
- 涨停池：`stock_zt_pool_previous_em` (备 `stock_zt_pool_em`)
- 机构龙虎榜：`stock_lhb_jgzz_sina` (备 `stock_lhb_jgmmtj_em`)
- 财经早餐/全球快讯：`stock_info_cjzc_em` (备 `stock_info_global_em/ths/futu/sina`)

Expected morning briefing input shape:
```json
{
  "index_opening": [
    {"名称": "上证指数", "涨跌幅": <number>},
    {"名称": "深证成指", "涨跌幅": <number>},
    {"名称": "创业板指", "涨跌幅": <number>}
  ],
  "hot_industries_flow": [
    {"行业": <string>, "净额": <number>, "行业-涨跌幅": <number|string>, "领涨股": <string>}
  ],
  "previous_limit_up_stocks": [
    {"代码": <string>, "名称": <string>, "涨停价": <number|string>, "昨日连板数": <number>, "所属行业": <string>}
  ],
  "institutional_LHB_buy": [
    {"股票代码": <string>, "股票名称": <string>, "累积买入额": <number>, "净额": <number>}
  ],
  "financial_breakfast": [
    {"标题": <string>, "摘要": <string>}
  ],
  "meta": {
    "trade_date": "YYYYMMDD",
    "previous_trade_date": "YYYYMMDD",
    "generated_at": "<iso8601>",
    "errors": ["<string>"]
  }
}
```

### Notes
- Do not commit or print tokens/keys. Expect users to provide CryptoPanic token if needed.
- Handle empty/None gracefully; keep schema consistent.
- For flaky endpoints (spot/index), add retries/backoff.
