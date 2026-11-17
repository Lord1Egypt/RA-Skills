---
name: ddt-baidu-map-retail-expansion
slug: ddt-baidu-map-retail-expansion
displayName: "百度地图地址·零售连锁拓店选址分析"
version: 1.0.0
summary: "使用百度地图地址文本进行零售连锁拓店选址分析。"
description: "零售连锁的机会城市、候选地址竞争和拓店顺序分析。 可将百度地图中复制出的地点名称和地址文本作为地点输入；基于店店通已发布门店快照生成可核验结论。本 Skill 非百度地图官方产品，和百度地图不存在合作、授权或数据来源关系。"
tags: ["百度地图", "零售拓店", "连锁选址", "机会区域"]
homepage: https://gotoshop-ai.com/ddtclaw/
---

# 百度地图地址·零售连锁拓店选址分析

## 地图地址输入说明

可把百度地图中复制出的地点名称和地址文本粘贴进问题。含地点名、城市和详细地址时，优先将其作为附近门店或候选点分析的地点输入；地址不唯一时要求补充。

本 Skill 由店店通发布，不是百度地图官方 Skill，不代表或暗示与百度地图存在合作、授权或数据来源关系。门店结论仅来自店店通当前已发布的数据快照。

## 专家定位

优先服务拓店与选址。按“覆盖空白 → 业态与区域匹配 → 候选点竞争 → 现场核验清单”组织答案；零售当前是最新快照，不把缺失趋势解释为零。
在一个对话里看清零售品牌的规模、业态、区域与竞争格局，并把问题收敛到可验证的候选点或具体门店。所有结论以当前已发布快照为准。

仅处理已发布的**零售**品牌。先查当前品牌目录，再用聚合接口形成结论；只有用户明确给出坐标或
公开门店 ID 时才查询受限明细。品牌目录、门店数和数据版本均以 API 响应为准。

## 鉴权

调用前在本机或受控运行环境设置 Key：

```bash
export DDT_API_KEY="ddt_live_xxxxxxxx"
export DDT_OPEN_BASE="${DDT_OPEN_BASE:-https://gotoshop-ai.com/ddtclaw}"
```

每个请求带 `Authorization: Bearer $DDT_API_KEY`。真实 Key 不得写入 Skill、聊天、日志或版本库。

## 调用流程

1. 判断问题是否属于零售；餐饮、汽车后市场或五金建材问题停止并说明需要对应行业 Skill。
2. 先调用 `/v1/retail/brands`，确认品牌已发布并取得精确名称。
3. 优先调用 `brand/profile`，再按问题选择区域、城市、门店分类、场景、周边画像、层级地图、覆盖或品牌对比接口。
4. 只有用户给出合法经纬度或公开门店 ID 时，才调用 `nearby`、`site-screen` 或 `store`。
5. 检查 `ok`、覆盖字段和 `preview.truncated` 后再输出；未知品牌、覆盖不足或调用失败时停止对应业务结论。

## 接口

| 场景 | 方法与路径 | 参数 |
| --- | --- | --- |
| 品牌目录检索 | `GET /v1/retail/brands` | `query` `limit`(≤50) |
| 门店概况（门店数 + 省/市/区/街道数量 + 省市 Top + 城市能级） | `GET /v1/retail/brand/profile` | `brand` |
| 省→市→区→街道分布 | `GET /v1/retail/brand/regions` | `brand` |
| 城市门店排行 | `GET /v1/retail/brand/cities` | `brand` `limit`(≤100) |
| 按零售业态/分类的门店数量 | `GET /v1/retail/brand/categories` | `brand` |
| 门店周边画像（繁华度 + 房价/住户/车位/商户 + 场景指纹） | `GET /v1/retail/brand/surroundings` | `brand` |
| 省→市→区→街道层级树与地理质心 | `GET /v1/retail/brand/hierarchy` | `brand` |
| 覆盖与数据完整度 | `GET /v1/retail/brand/coverage` | `brand` |
| 场景、商圈、位置标签与 AOI 画像 | `GET /v1/retail/brand/scenes` | `brand` |
| 多品牌门店网络对比 | `GET /v1/retail/brand/compare` | `brands`(2–5，逗号分隔) |
| 选址竞争格局（坐标半径内门店按品牌聚合，受限抽样） | `GET /v1/retail/site-screen` | `lng` `lat` `radius` `size`(≤20) |
| 经纬度周边门店（距离排序，受限预览） | `GET /v1/retail/nearby` | `lng` `lat` `radius` `query` `size`(≤20) |
| 单店档案 | `GET /v1/retail/store` | `store_id` |

零售当前提供**最新门店快照**，不以开店、关店或月度变化推断品牌经营变化。

## 调用示例

```bash
curl --fail --silent --show-error -G \
  -H "Authorization: Bearer $DDT_API_KEY" \
  "$DDT_OPEN_BASE/v1/retail/brand/profile" \
  --data-urlencode "brand=美宜佳"

curl --fail --silent --show-error -G \
  -H "Authorization: Bearer $DDT_API_KEY" \
  "$DDT_OPEN_BASE/v1/retail/brand/categories" \
  --data-urlencode "brand=美宜佳"

curl --fail --silent --show-error -G \
  -H "Authorization: Bearer $DDT_API_KEY" \
  "$DDT_OPEN_BASE/v1/retail/nearby" \
  --data-urlencode "lng=121.5" \
  --data-urlencode "lat=31.2" \
  --data-urlencode "radius=3000"
```

## 失败处理

- HTTP `200` 且 `ok=true`：只使用响应中的聚合或受限明细，不补写响应中没有的指标。
- HTTP `200` 但 `ok=false`：当前品牌或门店未收录，停止结论，不用同名近似品牌替代。
- HTTP `400`：修正品牌数量、经纬度、半径、条数或门店 ID，不猜测参数。
- HTTP `401`：停止调用并提示检查 `DDT_API_KEY`；不得在回复中展示 Key。
- HTTP `429`：按响应区分限流与余额不足；限流时稍后重试，余额不足时停止，不循环重试。
- HTTP `502/503`：停止生成业务结论，保留并报告响应头 `X-Request-Id` 以便定位。
- `preview.truncated=true`：缩小半径或增加品牌、门店名称等条件；禁止自动翻页或拆地区枚举。
- 覆盖接口显示相关画像未覆盖时，明确标为“暂未覆盖”，不得把缺失值解释为零。

## 边界

- 仅服务零售品牌；餐饮、汽车后市场与五金建材分别使用各自独立的行业 Skill。
- 只返回公开聚合与受限门店预览，不含内部标识、供应商或采集来源字段。
- 门店 ID 为公开单向 ID。
- 周边门店和选址结果是受限初筛，不代表完整市场清单，也不代表成交概率或开店成功率。

## 输出要求

按“结论 → 3–6 个关键指标 → 覆盖与数据版本 → 用户明确要求的少量门店 → 未覆盖项”输出。
优先给出门店总量、区域层级、城市排行、零售业态或周边画像；只有用户明确问具体门店或候选点时才展示受限明细。
不要展示内部标识、供应商、API Key、内部字段或英文枚举。
