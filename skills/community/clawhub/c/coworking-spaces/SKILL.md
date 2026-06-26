---
name: "附近共享办公"
description: "Find nearby coworking spaces. Invoke when user asks for shared offices near me."
---

# Nearby Coworking Spaces

用途
- 提供用户当前位置附近的 Coworking Spaces 共享办公列表
- 统一返回字段与查询行为，便于前端/接口复用

触发条件
- 用户询问“共享办公 附近 / coworking spaces near me / shared offices”

输入参数
- location: 经纬度 { lat, lng }，必填
- radius_meters: 查询半径，默认 3000
- limit: 返回数量上限，默认 20，最大 50
- filters: 可选筛选（是否按日租、会议室、咖啡、评分等）

响应字段
- 统一参见 [STANDARD_RESPONSE.md](file:///Users/mac_lkm/workspace/trae/100fj/.trae/skills/STANDARD_RESPONSE.md)
- 本技能 category 固定为 "coworking-spaces"

错误码
- INVALID_LOCATION: 经纬度不合法
- RADIUS_TOO_LARGE: 超过最大查询半径
- PROVIDER_UNAVAILABLE: 数据源不可用
- RATE_LIMITED: 触发速率限制

示例
- 输入: { location: { lat: 30.123, lng: 120.456 }, radius_meters: 2500, limit: 10 }
- 输出: 标准 POI 列表（见 STANDARD_RESPONSE.md）

隐私与速率限制
- 仅在用户授权定位后查询
- 避免保留精确坐标，必要时进行网格化模糊处理
