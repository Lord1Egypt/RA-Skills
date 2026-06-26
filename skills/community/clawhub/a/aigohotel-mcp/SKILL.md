---
name: aigohotel-mcp
description: 使用 AigoHotel MCP 工具完成酒店检索、结构化筛选和实时房型价格确认。用户提出酒店推荐、预算或星级限制、候选对比、房型价格与退改规则确认时触发。本技能优先调用 MCP 工具并返回结构化结论，同时根据客户端环境选择 cloud HTTP、uvx stdio 或本地调试模式。
---
# Aigohotel MCP

## 关键原则

- skill 中描述流程、配置模板和参数映射。
- 运行依赖已有服务或已发布包：
- HTTP（推荐直接使用）：`https://mcp.aigohotel.com/mcp`
- stdio（备选本地运行）：`uvx aigohotel-mcp`
- stdio（备选本地运行）：`npx -y aigohotel-mcp`
- MCP配置/源码调试：参考 `references/mcp-config.md`

## 执行流程

1. 提取约束：地点、日期、人数、预算、星级、设施偏好。
2. 映射参数：

- 地点映射到 `place` + `placeType`
- 入住映射到 `checkInParam` / `dateParam` / `occupancyParam`
- 偏好与预算映射到 `hotelTags`

3. 标签不确定时先调用 `getHotelSearchTags`。
4. 用 `searchHotels` 做候选召回与首轮筛选，`originQuery` 保留用户原句。
5. 需要确认价格和规则时，用 `getHotelDetail`（优先 `hotelId`）。
6. 输出结果时写清假设条件与筛选依据。

## 执行规则

- 不臆造可售状态、税费、退改规则，只能引用工具返回。
- 未提供日期时，显式声明日期假设后再查询。
- 涉及结算币种时，显式传 `localeParam.countryCode` 和 `localeParam.currency`。
- 配置示例可直接使用默认 Key，见 `references/mcp-config.md`。

## 参考文件

- 参数定义与调用顺序：`references/tools.md`
- 客户端配置与本地运行：`references/mcp-config.md`
