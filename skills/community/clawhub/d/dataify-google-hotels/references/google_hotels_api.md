# Dataify Google Hotels API

Endpoint: `POST https://scraperapi.dataify.com/request`

Submit requests as form data using UTF-8 encoding. The `engine` field is fixed to `google_hotels`. The API token is sent in the `Authorization` header. If the token does not include `Bearer `, prefix it before the request.

Use documented defaults only. Do not use examples, placeholders, or blank values as defaults.

| Parameter | Default | Description |
|---|---|---|
| Authorization |  | 请求头中的 Dataify API token。缺失时提示用户提供 token，或前往 `https://dashboard.dataify.com/login?utm_source=skill` 注册获取。 |
| engine | google_hotels | 固定的 Google Hotels 引擎值。 |
| q |  | 搜索查询，例如城市、地标、酒店名称或目的地；普通酒店搜索必填。 |
| json | 1 | 输出格式：`1` JSON，`2` JSON+HTML，`3` HTML，`4` Light JSON。 |
| hl |  | Google Hotels 使用的语言代码，例如 `en`、`zh-cn`、`ja` 或 `fr`。 |
| gl |  | Google Hotels 使用的国家或地区代码，例如 `us`、`cn`、`jp` 或 `fr`。 |
| currency | USD | 返回价格使用的货币。 |
| check_in_date |  | 入住日期，格式为 `YYYY-MM-DD`；普通酒店搜索必填。 |
| check_out_date |  | 退房日期，格式为 `YYYY-MM-DD`；普通酒店搜索必填。 |
| adults | 2 | 成人数量。 |
| children | 0 | 儿童数量。 |
| children_ages |  | 儿童年龄，多个年龄用逗号分隔；数量必须与 `children` 匹配。 |
| sort_by |  | 排序方式。留空表示按相关性排序。可用值包括 `3` 最低价格，`8` 最高评分，`13` 评论最多。 |
| min_price |  | 最低价格筛选。 |
| max_price |  | 最高价格筛选。 |
| property_types |  | 住宿类型 ID，多个值用逗号分隔。 |
| amenities |  | 设施 ID，多个值用逗号分隔。 |
| rating |  | 评分筛选：`7` 表示 3.5+，`8` 表示 4.0+，`9` 表示 4.5+。 |
| brands |  | 酒店品牌筛选，多个值用逗号分隔。 |
| hotel_class |  | 酒店星级筛选，多个星级可用逗号分隔。 |
| free_cancellation |  | `true` 表示显示可免费取消的结果；不适用于度假租赁。 |
| special_offers |  | `true` 表示显示有特惠的结果；不适用于度假租赁。 |
| eco_certified |  | `true` 表示显示获得生态认证的结果；不适用于度假租赁。 |
| vacation_rentals | false | `true` 表示搜索度假租赁；默认搜索酒店。 |
| bedrooms |  | 最小卧室数量；适用于度假租赁。 |
| bathrooms |  | 最小浴室数量；适用于度假租赁。 |
| next_page_token |  | 用于获取下一页结果的分页 token。 |
| no_cache | false | `true` 跳过缓存；`false` 使用可用缓存。 |
| property_token |  | 用于获取酒店或住宿详情的 token。 |

Normal hotel searches should include `q`, `check_in_date`, and `check_out_date`. Detail lookups may use `property_token`; pagination lookups may use `next_page_token`.
