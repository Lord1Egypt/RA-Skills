# AigoHotel MCP 工具参考

MCP 连接配置与本地运行请看 `references/mcp-config.md`。

## 工具列表

- `searchHotels`：酒店候选召回与初筛。
- `getHotelDetail`：单酒店房型级价格、可售状态、规则确认。
- `getHotelSearchTags`：获取可用标签元数据，用于构造 `hotelTags`。

## 推荐调用顺序

1. 需要标签映射时，先调用 `getHotelSearchTags`。
2. 调用 `searchHotels` 做候选筛选。
3. 对候选结果中最可能选中的酒店调用 `getHotelDetail` 做确认。

## searchHotels

必填参数：

- `originQuery`：用户原始需求句子。
- `place`：可地理解析的位置文本。
- `placeType`：以下固定值之一。

`placeType` 可选值：

- `城市`
- `机场`
- `景点`
- `火车站`
- `地铁站`
- `酒店`
- `区/县`
- `详细地址`

高影响可选参数：

- `checkInParam.checkInDate`（`YYYY-MM-DD`）
- `checkInParam.stayNights`（默认 `1`）
- `checkInParam.adultCount`（默认 `2`）
- `countryCode`（ISO 二位国家码，如 `CN`、`US`、`JP`）
- `filterOptions.starRatings`（如 `[4.5, 5.0]`）
- `filterOptions.distanceInMeter`
- `hotelTags.requiredTags`、`preferredTags`、`excludedTags`
- `hotelTags.preferredBrands`
- `hotelTags.maxPricePerNight`
- `hotelTags.minRoomSize`
- `size`（不超过 `20`，默认 `5`）

## getHotelDetail

酒店标识参数：

- 优先使用 `searchHotels` 返回的 `hotelId`。
- `hotelId` 缺失时再使用 `name`。

可选细化参数：

- `dateParam.checkInDate` / `dateParam.checkOutDate`
- `occupancyParam.adultCount` / `childCount` / `childAgeDetails` / `roomCount`
- `localeParam.countryCode` / `localeParam.currency`

## getHotelSearchTags

- 无参数。
- 将返回标签作为 `hotelTags` 的标准值，减少标签不匹配。

## 常见语义映射

- “靠近迪士尼” -> `place` 用景点名称，`placeType` 用 `景点`
- “靠近机场” -> `place` 用机场名称，`placeType` 用 `机场`
- “只看五星” -> `filterOptions.starRatings: [4.5, 5.0]`
- “每晚 800 以内” -> `hotelTags.maxPricePerNight: 800`
- “必须有亲子房” -> `hotelTags.requiredTags` 加对应标签

## 输出约束

- 用户未给日期时，必须明确写出日期假设。
- 接口不支持的筛选项，必须标记为不确定而不是硬判定。
- 未调用 `getHotelDetail` 前，不下结论说某房型一定可售或可退。
