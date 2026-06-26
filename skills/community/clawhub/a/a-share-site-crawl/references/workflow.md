# Five-Site Workflow

## Goal

Turn the five target websites into a repeatable A-share collection workflow.

## Recommended Order

### 1. Official / factual layer

Start with:
- 巨潮资讯
- 上交所 / 深交所
- 东方财富数据类入口

Use this layer for:
- 公告
- 披露
- 财报/预告
- 龙虎榜/融资融券/机构调研等正式或准正式数据入口

### 2. Fast event layer

Use:
- 财联社
- 东方财富资讯/搜索页

Use this layer for:
- 快讯
- 收评/午报/盘中异动
- 事件催化

### 3. Community / topic layer

Use:
- 韭研公社
- 雪球（logged-in relay preferred）

Use this layer for:
- 题材传播
- 个股热度
- 社区逻辑
- 市场情绪

### 4. Stock detail layer

Use:
- 雪球个股详情页

Use this layer for:
- 个股价格快照
- 成交额/换手/估值/关注度
- 关联讨论入口

## Per-Site Best Known Paths

### 韭研公社
- `/plan`
- `/announcement`
- `/timeline`

### 雪球
- homepage hot stream (logged-in)
- `/today`
- `/S/SHxxxxxx` / `/S/SZxxxxxx`

### 东方财富
- `data.eastmoney.com/zjlx/dpzjlx.html`
- `data.eastmoney.com/jgdy/`
- `so.eastmoney.com/`
- `data.eastmoney.com/stockcomment/`
- data-center nav pages for 公告大全 / 研报 / 财报 / 融资融券 / 龙虎榜

### 财联社
- `/telegraph`
- `/finance`
- `/depth?id=1003`

### 巨潮资讯
- disclosure/list/search pages
- `list.cninfo.com.cn`

## Reliability Notes

- 雪球 is strongest with logged-in browser relay
- 巨潮资讯 should be judged from disclosure/search/list pages, not homepage text
- 东方财富 is more useful through data-center/navigation-specific pages than the front portal shell
- 韭研公社 and 雪球 are valuable for topic discovery, but should not be treated as sole truth sources
