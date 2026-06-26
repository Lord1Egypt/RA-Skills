---
name: "Nearby Budget Hotels"
description: "Find nearby budget hotels. Invoke when user asks for cheap hotels near me."
---

# Nearby Budget Hotels

用途
- 提供用户当前位置附近的 Budget Hotels 列表
- 统一返回字段与查询行为，便于前端/接口复用
- 适用于“便宜酒店/性价比住宿/临时住一晚”等场景

触发条件
- 用户询问“Budget Hotels 附近 / cheap hotel near me / budget hotel near me”
- 用户提供定位/城市并希望“找/推荐/看看附近的 Budget Hotels”

输入参数
- location: 经纬度 { lat, lng }，必填
- radius_meters: 查询半径，默认 5000
- limit: 返回数量上限，默认 20，最大 50
- filters: 可选筛选（价格等级、评分、是否含早餐、keywords 等）

响应字段
- 统一参见 STANDARD_RESPONSE.md
- 本技能 category 固定为 "budget-hotels"

错误码
- INVALID_LOCATION: 经纬度不合法
- RADIUS_TOO_LARGE: 超过最大查询半径
- PROVIDER_UNAVAILABLE: 数据源不可用
- RATE_LIMITED: 触发速率限制

示例
- 输入: { location: { lat: 30.123, lng: 120.456 }, radius_meters: 5000, limit: 10, filters: { price_level: [0,1,2] } }
- 输出: 标准 POI 列表（见 STANDARD_RESPONSE.md）

隐私与速率限制
- 仅在用户授权定位后查询
- 避免保留精确坐标，必要时进行网格化模糊处理
- 建议对同一 location+category+radius 做短时缓存以降低频率
