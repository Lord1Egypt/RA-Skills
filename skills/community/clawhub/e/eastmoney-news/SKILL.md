# eastmoney-news

东方财富秒想新闻搜索。使用此skill获取A股、财经新闻。

## When to use

- 用户询问今日A股市场走势
- 用户需要财经新闻资讯
- 用户说"看看今天有什么新闻"

## API

```bash
curl -X POST "https://mkapi2.dfcfs.com/finskillshub/api/claw/news-search" \
  -H "Content-Type: application/json" \
  -H "apikey: mkt_o2fBS-Dkbt11c7vSNnlXjESgfybI8EXzzzX2XkOQVuE" \
  -d '{"query":"<搜索关键词>","variables":0}'
```

## 常用查询

- 今日A股市场 -> "今日A股市场新闻"
- 大盘走势 -> "A股大盘走势"
- 板块轮动 -> "A股板块轮动"
- 个股新闻 -> "XXX股票新闻"

## 输出格式

解析返回的JSON，提取title、content、date、source，以可读格式呈现给用户。
