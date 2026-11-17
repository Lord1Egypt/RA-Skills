---
name: ddt-amap-auto-network
slug: ddt-amap-auto-network
displayName: "高德地图地址·汽车后市场门店网络分析"
version: 1.0.0
summary: "使用高德地图地址文本进行汽车后市场门店网络分析。"
description: "汽服、轮胎和润滑油品牌的门店网络、区域覆盖与位置画像分析。 可将高德地图中复制出的地点名称和地址文本作为地点输入；基于店店通已发布门店快照生成可核验结论。本 Skill 非高德地图官方产品，和高德地图不存在合作、授权或数据来源关系。"
tags: ["高德地图", "汽车后市场", "汽服", "门店网络"]
homepage: https://gotoshop-ai.com/ddtclaw/
---

# 高德地图地址·汽车后市场门店网络分析

## 地图地址输入说明

可把高德地图中复制出的地点名称和地址文本粘贴进问题。含地点名、城市和详细地址时，优先将其作为附近门店或候选点分析的地点输入；地址不唯一时要求补充。

本 Skill 由店店通发布，不是高德地图官方 Skill，不代表或暗示与高德地图存在合作、授权或数据来源关系。门店结论仅来自店店通当前已发布的数据快照。

把品牌网络、单店位置画像与销售机会放进同一条分析链路：从全国覆盖到区域下钻，再到具体门店或候选点。所有门店结构化结论以已发布数据为准。

仅处理连锁**汽车后市场**品牌。先查当前品牌目录，再用聚合接口形成结论，最后按用户明确
需求查询坐标周边门店或单店档案；品牌目录、覆盖与数据版本均以 API 响应为准。

## 鉴权

调用前在本机或受控运行环境设置 Key（去开放平台申请）：

```bash
export DDT_API_KEY="ddt_live_xxxxxxxx"
export DDT_OPEN_BASE="${DDT_OPEN_BASE:-https://gotoshop-ai.com/ddtclaw}"
```

每个请求带 `Authorization: Bearer $DDT_API_KEY`。真实 Key 不得写入 Skill、聊天、日志或版本库。

## 调用流程

1. 判断问题是否属于汽车后市场；餐饮、零售或五金建材问题停止并说明需要对应行业 Skill。
2. 先调用 `/v1/auto-service/brands`，确认品牌已发布并取得精确名称。
3. 优先调用 `brand/profile`；再按问题选择区域、城市、服务类型、场景、周边画像、层级地图、覆盖或品牌对比接口。
4. 只有用户给出合法经纬度或公开门店 ID 时，才调用 `nearby`、`site-screen` 或 `store`。
5. 检查 `ok`、覆盖字段和 `preview.truncated` 后再输出；未知品牌、覆盖不足或调用失败时停止对应业务结论。

## 接口

| 场景 | 方法与路径 | 参数 |
| --- | --- | --- |
| 品牌目录检索 | `GET /v1/auto-service/brands` | `query` `limit`(≤50) |
| 门店概况（门店数 + 省/市/区/街道数量 + 省市 Top + 城市能级） | `GET /v1/auto-service/brand/profile` | `brand` |
| 省→市→区→街道全量分布 | `GET /v1/auto-service/brand/regions` | `brand` |
| 城市门店排行 | `GET /v1/auto-service/brand/cities` | `brand` `limit`(≤100) |
| 按服务类型分类门店数量（洗车/保养/维修/美容…） | `GET /v1/auto-service/brand/categories` | `brand` |
| 门店周边画像（繁华度 + 房价/住户/车位/商户 + 场景指纹） | `GET /v1/auto-service/brand/surroundings` | `brand` |
| 省→市→区→街道层级树 + 各级门店数与地理质心 | `GET /v1/auto-service/brand/hierarchy` | `brand` |
| 覆盖与数据完整度（总数/可映射/有画像/各级覆盖/城市能级） | `GET /v1/auto-service/brand/coverage` | `brand` |
| 按业态门店画像（场景指纹 + 商圈 + 位置标签 + AOI） | `GET /v1/auto-service/brand/scenes` | `brand` |
| 多品牌门店网络对比 | `GET /v1/auto-service/brand/compare` | `brands`(2–5，逗号分隔) |
| 选址竞争格局（坐标半径内门店按品牌聚合，受限抽样） | `GET /v1/auto-service/site-screen` | `lng` `lat` `radius` `size`(≤20) |
| 经纬度周边门店（距离排序，受限预览） | `GET /v1/auto-service/nearby` | `lng` `lat` `radius` `query` `size`(≤20) |
| 单店档案 | `GET /v1/auto-service/store` | `store_id` |

## 调用示例

```bash
curl --fail --silent --show-error -G \
  -H "Authorization: Bearer $DDT_API_KEY" \
  "$DDT_OPEN_BASE/v1/auto-service/brand/profile" \
  --data-urlencode "brand=中鑫之宝"

curl --fail --silent --show-error -G \
  -H "Authorization: Bearer $DDT_API_KEY" \
  "$DDT_OPEN_BASE/v1/auto-service/brand/regions" \
  --data-urlencode "brand=中鑫之宝"

curl --fail --silent --show-error -G \
  -H "Authorization: Bearer $DDT_API_KEY" \
  "$DDT_OPEN_BASE/v1/auto-service/nearby" \
  --data-urlencode "lng=120.6" \
  --data-urlencode "lat=31.3" \
  --data-urlencode "radius=3000"
```

## 失败处理

- HTTP `200` 且 `ok=true`：使用返回的聚合或受限明细；不得补写响应中没有的指标。
- HTTP `200` 但 `ok=false`：当前品牌或门店未收录，停止结论，不用同名近似品牌替代。
- HTTP `400`：修正品牌数量、经纬度、半径、条数或门店 ID，不猜测参数。
- HTTP `401`：停止调用并提示检查 `DDT_API_KEY`；不得在回复中展示 Key。
- HTTP `429`：按响应区分限流与余额不足；限流时稍后重试，余额不足时停止，不循环重试。
- HTTP `502/503`：停止生成业务结论，保留并报告响应头 `X-Request-Id` 以便定位。
- `preview.truncated=true`：缩小半径或增加品牌、门店名称等条件；禁止自动翻页或拆地区枚举。
- 覆盖接口显示相关画像未覆盖时，明确标为“暂未覆盖”，不得把缺失值解释为零。

## 边界

- 仅服务汽车后市场品牌；餐饮、零售与五金建材分别使用各自独立的行业 Skill。
- 只返回公开聚合与门店点位，不含存储 ID、数据供应商或高德来源字段。
- 门店 ID 为公开单向 ID。
- 周边门店和选址结果是受限初筛，不代表完整市场清单，也不代表成交概率或开店成功率。

## 输出要求

按“结论 → 3–6 个关键指标 → 覆盖与数据版本 → 用户明确要求的少量门店 → 未覆盖项”输出。
优先给出门店总量、区域层级、城市排行、服务类型或周边画像中的相关指标；只有用户明确问
具体门店或候选点时才展示受限明细。不要展示存储 ID、供应商、API Key、内部字段或英文枚举。
