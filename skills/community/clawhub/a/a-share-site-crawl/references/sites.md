# Site Notes

## 韭研公社

### Best starting page

- `https://www.jiuyangongshe.com/plan`
- `https://www.jiuyangongshe.com/announcement`
- `https://www.jiuyangongshe.com/timeline`

### What worked in testing

- `web_fetch` could return partial readable text from the plan page
- `browser` could see real page structure, feed controls, and content entry points

### Recommended mode

- `browser-first`

### Use for

- 交易计划
- 题材逻辑
- 搜公告
- 时间轴 / 事件流
- 社区热度与讨论入口

### Main limitation

- Community content quality is uneven
- Some deeper content may depend on session state or dynamic loading

## 雪球

### Best starting page

- `https://xueqiu.com/`

### What worked in testing

- `web_fetch` returned anti-bot / obfuscated JavaScript instead of usable content
- `browser` could render the page, but the experience is strongly login-oriented
- with a logged-in Chrome relay tab, the browser could read homepage hot topics, market snapshot blocks, hot-stock lists, and real community post excerpts
- stock detail pages like `https://xueqiu.com/S/SZ300476` and `https://xueqiu.com/S/SH601872` exposed usable quote, valuation, turnover, market-cap, and related discussion modules

### Recommended mode

- default: `restricted`
- with logged-in Chrome relay: `browser-first`

### Use for

- 市场情绪
- 热帖线索
- 个股舆论跟踪
- 指数与热股快照
- 个股详情页基础行情与估值信息
- 热门个股讨论串

### Main limitation

- High anti-bot pressure
- Login gate makes unauthenticated extraction unstable
- some entry pages are front-end routed, so stable extraction often requires direct detail URLs or logged-in browser navigation

## 东方财富

### Best starting page

- `https://www.eastmoney.com/`
- `https://so.eastmoney.com/`
- `https://data.eastmoney.com/zjlx/dpzjlx.html`
- `https://data.eastmoney.com/jgdy/`

### What worked in testing

- `web_fetch` returned readable partial text
- `browser` rendered stable navigation and content blocks
- data-center style pages exposed usable A-share data entry paths including 资金、龙虎榜、融资融券、机构调研、公告大全、业绩报表、最新预告、研报 and related search/data portals

### Recommended mode

- `fetch-first`, upgrade to `browser` for better structure

### Use for

- 财经资讯
- 板块与个股新闻
- 数据中心入口
- 资金面 / 机构调研 / 公告大全 / 研报 / 财报类入口
- 门户级内容聚合

### Main limitation

- Homepage is noisy; targeted search/data/content pages are usually better than the main portal shell
- Different subdomains and data pages may require page-specific probing

## 财联社

### Best starting page

- `https://www.cls.cn/`
- `https://www.cls.cn/telegraph`
- `https://www.cls.cn/finance`
- `https://www.cls.cn/depth?id=1003`

### What worked in testing

- `web_fetch` returned useful text/event content
- `browser` rendered clear sections like 首页 / 电报 / 盯盘 / A股

### Recommended mode

- `fetch-first`, with `browser` for page truth and structure

### Use for

- 电报快讯
- 盯盘 / 盘中异动
- A股栏目深度内容
- 事件驱动
- A股主线观察

### Main limitation

- Some sections are denser and need targeted extraction rather than homepage-only fetch

## 巨潮资讯

### Best starting page

- Homepage is not the best judge
- Prefer disclosure/list/search style pages reachable from the site nav
- `https://www.cninfo.com.cn/new/commonUrl/pageOfSearch?url=disclosure/list/search`
- `https://list.cninfo.com.cn/`

### What worked in testing

- `web_fetch` on the homepage mostly returned site statements/disclaimer text
- `browser` rendered real disclosure navigation and market-board entry points

### Recommended mode

- `browser-first` on targeted disclosure/list/search pages

### Use for

- 最新公告
- 公告检索
- 披露列表页
- 个股 F10 / 公开信息入口
- 正式信息核对

### Main limitation

- Homepage is a poor extraction target
- Need to navigate to announcement/disclosure pages for useful collection

## Fallback Source Order

When one of the five target sites is restricted or unstable, prefer these public sources:

1. 财联社
2. 东方财富
3. 上交所 / 深交所
4. 证券时报 / 中证报 / 上证报
5. 同花顺财经
6. 国家统计局 / 央行 / 国务院 / 证监会

Use fallback sources to preserve factual coverage, not to imitate community sentiment sites.
