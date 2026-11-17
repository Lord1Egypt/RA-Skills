---
name: ddt-amap-restaurant-network
slug: ddt-amap-restaurant-network
displayName: "高德地图地址·餐饮开关店与竞对分析"
version: 1.0.0
summary: "使用高德地图地址文本进行餐饮开关店与竞对分析。"
description: "餐饮品牌开关店、区域扩张、竞对密度与候选点机会分析。 可将高德地图中复制出的地点名称和地址文本作为地点输入；基于店店通已发布门店快照生成可核验结论。本 Skill 非高德地图官方产品，和高德地图不存在合作、授权或数据来源关系。"
tags: ["高德地图", "餐饮", "开关店", "竞对分析"]
homepage: https://gotoshop-ai.com/ddtclaw/
---

# 高德地图地址·餐饮开关店与竞对分析

## 地图地址输入说明

可把高德地图中复制出的地点名称和地址文本粘贴进问题。含地点名、城市和详细地址时，优先将其作为附近门店或候选点分析的地点输入；地址不唯一时要求补充。

本 Skill 由店店通发布，不是高德地图官方 Skill，不代表或暗示与高德地图存在合作、授权或数据来源关系。门店结论仅来自店店通当前已发布的数据快照。

用真实发布快照快速看清品牌在何处扩张、竞争对手在哪里，以及销售下一步优先跟进什么。先查品牌目录，再用聚合数据形成结论；不把网页传闻当成门店事实。

仅处理已发布的餐饮品牌。先查品牌目录，再取聚合数据，最后按用户明确需求核查少量门店；
不要用模型记忆、网页门店数或其他行业 Skill 替代接口结果。

## 准备

在 `https://gotoshop-ai.com/ddtclaw/open` 创建 API Key，仅保存到本机环境变量：

```bash
export DDT_OPEN_BASE="${DDT_OPEN_BASE:-https://gotoshop-ai.com/ddtclaw}"
test -n "$DDT_API_KEY"
```

请求统一使用 `Authorization: Bearer $DDT_API_KEY`。

## 调用流程

1. 判断问题是否属于餐饮品牌；汽车后市场、零售或五金建材问题停止并说明需要对应行业 Skill。
2. 先调用 `/v1/network/brands` 查当前发布目录，确认精确品牌名、覆盖期和 `capabilities`。
3. 优先用 `profile`、`direction`、`summary`、`trend`、`regions` 或 `compare` 获取聚合事实。
4. 只有用户明确问具体门店、地址或候选点时，才调用受限的 `events`、`stores`、`nearby`、`sales-shortlist`、`site-screen` 或 `store-compare`。
5. 检查响应状态、覆盖期和预览截断标记后再输出；任何失败或能力缺失都停止对应业务结论。

## 选择接口

| 问题 | 路径 | 参数 |
| --- | --- | --- |
| 名称不确定、有哪些品牌 | `/v1/network/brands` | `q,page,size` |
| 当前门店规模、区域与位置画像 | `/v1/network/profile` | `brand` |
| 竞对扩张/收缩方向与重点区域 | `/v1/network/direction` | `brand,start,end` |
| 开店观察、关店确认、净增与期末在营 | `/v1/network/summary` | `brand,start,end` |
| 月度开店观察、关店确认与在营趋势 | `/v1/network/trend` | `brand,start,end` |
| 省市区县增长、收缩与期末规模 | `/v1/network/regions` | `brand,start,end,level,sort,top` |
| 2–5 品牌共同窗口比较 | `/v1/network/compare` | `brands,start,end` |
| 地址/大厦/地标附近的跨品牌门店 | `/v1/network/nearby` | `q,brand,province,city,district,radius_m,size` |
| 销售攻店候选初筛 | `/v1/network/sales-shortlist` | `brand,province,city,district,months,size` |
| 1–3 个候选点选址初筛 | `/v1/network/site-screen` | `locations,city,own_brand,radius_m` |
| 明确核查少量开关店门店 | `/v1/network/events` | `brand,event,start,end,province,city,district,size` |
| 明确核查少量当前/历史门店 | `/v1/network/stores` | `brand,q,status,province,city,district,size` |
| 2–10 家已选门店对比 | `/v1/network/store-compare` | `stores=品牌甲::门店词;品牌乙::门店词` |

名称不确定时先调用目录，后续使用精确名称。目录的 `capabilities` 是强制门禁：`network` 才能分析网络变化，`regions` 才能按地区分析，`store_location` 才能比较完整位置画像。

## 明细与分析边界

- `/nearby`、`/stores` 与 `/events` 是受限预览，不是门店目录或导出接口。
- 默认返回 10 条，最多 20 条，只接受 `page=1`；第 2 页或更大 `size` 返回 `400`。
- `preview.truncated=true` 或 `refine_required=true` 时，增加门店名称、地址、日期、省、市或区县条件后重新查询。
- 禁止自动翻页、循环拆分地区枚举、拼接全量门店或把大量门店放进模型上下文。
- 用户索要全量清单时，改为提供 `total`、状态/事件汇总与区域聚合，并请其指定需要核查的门店或地区。
- `/store-compare` 只用于用户明确选定的 2–10 家门店。
- `/nearby` 正常返回时使用 GCJ02 坐标和精确距离，`matching.radius_filter_applied=true`；位置服务暂不可用时返回 `503`，不降级为关键词匹配，也不扣积分。
- `/direction` 日期留空时分析最近 12 个完整月，只返回聚合事实且不含门店级记录；`/sales-shortlist` 最多 20 个候选，优先级不是成交概率；`/site-screen` 每次只接受 1–3 个候选地址，空间密度不代表开店成功率。
- 默认时间窗口截止到 `complete_through`。摘要和趋势只有在用户明确指定部分月时才使用并提示；方向判断和多品牌比较始终排除部分月。

## 失败处理

- HTTP `400`：修正品牌、日期、地址唯一性或数量范围，不猜测参数。
- HTTP `401`：停止调用并提示检查 `DDT_API_KEY`；不得在回复中展示 Key。
- HTTP `429`：按响应区分限流与余额不足；限流时稍后重试，余额不足时停止，不循环重试。
- HTTP `502/503`：停止生成业务结论，保留并报告响应头 `X-Request-Id` 以便定位。
- HTTP `200` 但 `status=not_materialized`、`ok=false` 或缺少所需 `capabilities`：明确说明当前未发布或能力不足，不用相似品牌、网页数据或模型常识补齐。
- `preview.truncated=true` 或 `refine_required=true`：收窄关键词、地区或日期；禁止自动翻页或拆地区枚举。

示例：

```bash
curl --fail --silent --show-error -G \
  -H "Authorization: Bearer $DDT_API_KEY" \
  "$DDT_OPEN_BASE/v1/network/nearby" \
  --data-urlencode "q=北京航空科技大厦" \
  --data-urlencode "city=北京市" \
  --data-urlencode "radius_m=1000" \
  --data-urlencode "size=10"

curl --fail --silent --show-error -G \
  -H "Authorization: Bearer $DDT_API_KEY" \
  "$DDT_OPEN_BASE/v1/network/sales-shortlist" \
  --data-urlencode "brand=茉莉奶白" \
  --data-urlencode "city=上海市" \
  --data-urlencode "months=6" \
  --data-urlencode "size=10"

curl --fail --silent --show-error -G \
  -H "Authorization: Bearer $DDT_API_KEY" \
  "$DDT_OPEN_BASE/v1/network/stores" \
  --data-urlencode "brand=% Arabica" \
  --data-urlencode "q=浦东" \
  --data-urlencode "city=上海市" \
  --data-urlencode "size=10"
```

## 数据口径

- 开店观察日期取 `collection_time`，不等同品牌官方开业。
- 满一个自然月未更新后形成关店确认，日期取最后更新时间后一天，不等同官方闭店公告。
- 本月在营 = 上月在营 + 本月开店观察 - 本月关店确认；校验失败时停止业务结论。
- 默认查询和多品牌比较只使用共同覆盖的完整月份；显式包含部分月时必须提示。
- 关店率是观察期内的门店网络收缩指标，不代表经营失败率。
- 数据不包含可验证营收、同店增长、AUV、利润或闭店原因。

## 输出要求

按“结论 → 3–6 个关键指标 → 覆盖期与口径 → 用户明确要求的少量明细 → 未覆盖项”输出。
品牌规模、趋势、区域与位置判断优先使用聚合接口；只有用户明确问具体门店时才展示少量明细。
不要展示品牌 ID、门店内部键、版本 UUID、表名、供应商、API Key 或英文枚举。
