---
name: "Nearby Camping Sites"
description: "Find nearby camping sites. Invoke when user asks for camping near me."
---

# Nearby Camping Sites

用途
- 提供用户当前位置附近的 Camping Sites 列表
- 统一返回字段与查询行为，便于前端/接口复用
- 适用于露营地/营地/房车营地等就近查询与出行规划

触发条件
- 用户询问“Camping Sites 附近 / camping near me / nearby campsite”
- 用户提供定位/城市并希望“找/推荐/看看附近的 Camping Sites”

输入参数
- location: 经纬度 { lat, lng }，必填
- radius_meters: 查询半径，默认 8000
- limit: 返回数量上限，默认 20，最大 50
- filters: 可选筛选（open_now、min_rating、keywords 等）

响应字段
- 统一参见 STANDARD_RESPONSE.md
- 本技能 category 固定为 "camping-sites"

错误码
- INVALID_LOCATION: 经纬度不合法
- RADIUS_TOO_LARGE: 超过最大查询半径
- PROVIDER_UNAVAILABLE: 数据源不可用
- RATE_LIMITED: 触发速率限制

示例
- 输入: { location: { lat: 30.123, lng: 120.456 }, radius_meters: 8000, limit: 10 }
- 输出: 标准 POI 列表（见 STANDARD_RESPONSE.md）

隐私与速率限制
- 仅在用户授权定位后查询
- 避免保留精确坐标，必要时进行网格化模糊处理
- 建议对同一 location+category+radius 做短时缓存以降低频率
