# 文旅素材 API 接口规范

> 本文档定义客户端（智能体）与服务端（数游神州 data0086.com）之间的接口契约。

## 通用约定

| 项目 | 说明 |
|------|------|
| 基址 | 由 [config.json](config.json) 的 `api_origin` 决定（当前：`https://test.data0086.com`）；可通过环境变量 `WENLV_API_ORIGIN` 覆盖 |
| 协议 | HTTPS |
| Content-Type | `application/json` |
| 字符编码 | UTF-8 |
| 鉴权 | 搜索接口：无需鉴权（`token` 头可为空）；交易接口：见下文 |

### 统一响应结构

所有接口响应遵循以下顶层结构：

```json
{
  "code": 0,
  "msg": "请求处理成功",
  "resData": { ... }
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `code` | integer | `0` 表示成功，非 `0` 为业务错误码 |
| `msg` | string | 状态描述 |
| `resData` | object | 业务数据 |

---

## 1. 素材搜索

### `POST {API_ORIGIN}/ms-base/home/getList?pageNum={pageNum}&pageSize={pageSize}`

按关键词搜索文旅素材（商品），返回分页列表。分页参数通过 **URL query** 传递，筛选条件通过 **请求体** 传递。

### 请求 URL 参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|:----:|--------|------|
| `pageNum` | integer | 否 | `1` | 页码，从 1 开始 |
| `pageSize` | integer | 否 | `18` | 每页条数；**智能体侧默认传 `5`** |

### 请求体

```json
{
  "commodityCode": null,
  "sceneType": "",
  "tradeType": "",
  "search": "雁荡山",
  "city": "330300"
}
```

| 字段 | 类型 | 必填 | 默认值 | 说明 |
|------|------|:----:|--------|------|
| `search` | string | **是** | — | 搜索关键词，支持中文自然语言 |
| `city` | string | 否 | `"330300"` | 城市行政区划代码（默认温州），缩小搜索范围 |
| `commodityCode` | string \| null | 否 | `null` | 按商品编码精确筛选；本 Skill 用此字段区分成片（传 `finished_commodity_code`）与素材（传 `null`）——见下方「两次调用」 |
| `sceneType` | string | 否 | `""` | 场景类型筛选，如 `"慢直播"`、`"创作素材"`、`"无人机航拍"`；多值逗号分隔 |
| `tradeType` | string | 否 | `""` | 交易类型筛选，如 `"cash"` |

### 两次调用：成片 + 素材

本 Skill 针对同一 `search` 关键词**依次发起两次搜索**，请求时的 `commodityCode` 分别为：

| 次序 | 请求 `commodityCode` |
|------|---------------------|
| 1 | `finished_commodity_code`（config.json，默认 `"CommodityType-7bf0aa3057bc"`） |
| 2 | `null` |

**类别判定以返回数据为准**：合并两次 `resData.datas`（按 `businessCode`/`id` 去重）后，对每条记录：

- `item.commodityCode === finished_commodity_code` → `category = "成片"`
- 否则 → `category = "素材"`

排序：成片在前、素材在后。其他请求字段（`search`、`city`、`sceneType`、`tradeType`）两次保持一致；`pageSize` 对每次调用独立。若 `finished_commodity_code` 为空字符串或未配置，则跳过第 1 次调用，所有返回记录归为 `category = "素材"`。

### 请求头

```
Content-Type: application/json
Origin: {api_origin}
Referer: {api_origin}/
token: (可为空)
```

### 响应体

```json
{
  "code": 0,
  "msg": "请求处理成功",
  "resData": {
    "total": 185,
    "datas": [
      {
        "id": 459,
        "commodityName": "雁荡山-飞拉达雾天-一镜到底-无人机航拍",
        "commodityCode": "CommodityType-e744a1044794",
        "businessCode": "Commodity-20260406211854879",
        "explain": "<table>...</table>",
        "tag": "[\"视频创作\", \"无人机航拍\"]",
        "price": 45.0,
        "sceneType": "慢直播,创作素材,无人机航拍",
        "tradeType": "cash",
        "location": "[\"330000\",\"330300\"]",
        "breviaryPic": "https://wenzhou.data0086.com:9443/res/covers/77758f136a4648888d1acd615ec24dbe.jpg",
        "fragmentUrl": "https://wenzhou.data0086.com:9443/res/hls/preview/product/77758f136a4648888d1acd615ec24dbe",
        "fragmentTime": "240.873967",
        "videoProductCode": "77758f136a4648888d1acd615ec24dbe",
        "createUser": "温州鼎诚体育发展有限公司",
        "createTime": "2026-04-06T21:18:54",
        "updateTime": "2026-04-07T01:35:30",
        "status": 2,
        "recommend": 1,
        "buyNum": 0,
        "contactName": "刘先生",
        "contactPhone": "18268777142",
        "merchantBusinessCode": "CRT-80abe67be842",
        "priceJson": "[{\"name\": \"上架短视频授权\", \"price\": 45, \"isCheck\": true, \"priceId\": 1, \"defaultCheck\": true}]",
        "sampleDealType": "waterprint",
        "sampleSpeed": 5,
        "timeRange": 1
      }
    ]
  }
}
```

### `resData` 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `total` | integer | 符合条件的素材总数 |
| `datas` | array | 素材列表，结构见下表 |

### `datas[]` 素材对象

| 字段 | 类型 | 必返回 | 说明 |
|------|------|:------:|------|
| `id` | integer | **是** | 素材唯一标识（数字 ID） |
| `commodityName` | string | **是** | 素材/商品标题 |
| `commodityCode` | string | **是** | 商品编码（如 `CommodityType-e744a1044794`），交易下单必需 |
| `businessCode` | string | **是** | 业务编码（如 `Commodity-20260406211854879`），交易下单必需，也用于详情页 URL |
| `explain` | string (HTML) | 否 | 商品详情说明（HTML 表格，包含清晰度、格式、时长等结构化信息） |
| `tag` | string (JSON array) | 否 | 标签，JSON 字符串数组，如 `'["视频创作", "无人机航拍"]'`，需 `JSON.parse` |
| `price` | number | **是** | 价格（元） |
| `sceneType` | string | 否 | 场景类型，逗号分隔，如 `"慢直播,创作素材,无人机航拍"` |
| `tradeType` | string | 否 | 交易类型，如 `"cash"` |
| `location` | string (JSON array) | 否 | 地区编码，如 `'["330000","330300"]'` |
| `breviaryPic` | string (URL) | **是** | 缩略图/封面完整 URL |
| `fragmentUrl` | string (URL) | **是** | 预览视频流地址（HLS） |
| `fragmentTime` | string | **是** | 预览视频时长（秒），如 `"240.873967"` |
| `videoProductCode` | string | 否 | 视频产品编码（可能含多个逗号分隔值） |
| `createUser` | string | 否 | 商家/上传者名称 |
| `createTime` | string (ISO 8601) | 否 | 创建时间 |
| `updateTime` | string (ISO 8601) | 否 | 更新时间 |
| `status` | integer | 是 | 状态码，`2` 表示已上架 |
| `recommend` | integer | 否 | 是否推荐，`1` = 推荐 |
| `buyNum` | integer | 否 | 已购买次数 |
| `contactName` | string | 否 | 联系人姓名 |
| `contactPhone` | string | 否 | 联系人电话 |
| `merchantBusinessCode` | string | 否 | 商家业务编码 |
| `priceJson` | string (JSON array) | 否 | 价格方案列表（JSON 字符串，包含授权类型和价格） |
| `sampleDealType` | string | 否 | 样片处理方式，如 `"waterprint"`（水印） |

---

## 2. 素材详情页（预览）

### `GET {API_ORIGIN}/#/multimodal?businessCode={businessCode}`

跳转到数游神州前端的**商品详情页**（SPA hash 路由），页面内部处理视频播放与商品信息展示。用户在搜索结果中点击「预览」或「详情」时打开此地址。

| 参数 | 位置 | 类型 | 说明 |
|------|------|------|------|
| `businessCode` | query | string | 商品业务编码（来自搜索结果的 `businessCode` 字段） |

**示例**：
```
https://test.data0086.com/#/multimodal?businessCode=Commodity-20260406211854879
```

---

## 3. 交易下单

### `POST {TRADE_API_BASE}/orders`

批量购买素材，创建交易订单。

> **当前阶段（`trade_api_base` 为空）**：不调用此真实接口，改为 **mock 交易响应**（`video_url` = 搜索结果的 `fragmentUrl`），然后**下载视频到本地**。详见 SKILL.md「购买后输出」。智能体收到购买指令时**必须执行 mock + 下载**，不得拒绝。

### 鉴权

| 方式 | 说明 |
|------|------|
| Header | `Authorization: Bearer {token}`（具体方案由服务方约定） |

### 请求体

```json
{
  "items": [
    {
      "id": 459,
      "commodityCode": "CommodityType-e744a1044794",
      "businessCode": "Commodity-20260406211854879",
      "commodityName": "雁荡山-飞拉达雾天-一镜到底-无人机航拍"
    }
  ]
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|:----:|------|
| `items` | array | **是** | 购买素材列表，至少 1 条 |
| `items[].id` | integer | **是** | 素材 ID（来自搜索接口的 `id`） |
| `items[].commodityCode` | string | **是** | 商品编码（来自搜索接口的 `commodityCode`） |
| `items[].businessCode` | string | **是** | 业务编码（来自搜索接口的 `businessCode`） |
| `items[].commodityName` | string | 否 | 素材标题（便于核对，非必填） |

### 错误码

| code | 说明 |
|------|------|
| `0` | 成功 |
| `4001` | 参数错误（缺少必填字段 / 格式不正确） |
| `4003` | 鉴权失败 |
| `4004` | 素材不存在 |
| `4009` | 重复下单（同一素材已购买） |
| `5000` | 服务端内部错误 |

---

## 附：字段映射参考

客户端从搜索接口原始字段到展示字段的映射关系：

| 展示字段 | 来源 | 说明 |
|----------|------|------|
| `title` | `commodityName` | 素材标题 |
| `cover_url` | `breviaryPic` | 封面完整 URL（已是绝对地址） |
| `video_url` | `fragmentUrl` | 预览视频流（HLS） |
| `stream_type` | 由 `fragmentUrl` 判定 | 含 `/hls/` → `HLS`；以 `.mp4` 结尾 → `MP4` |
| `preview_url` | `{API_ORIGIN}/#/multimodal?businessCode={businessCode}` | 商品详情页地址 |
| `duration_seconds` | `fragmentTime` | 预览时长（秒） |
| `price` | `price` | 价格（元） |
| `scene_type` | `sceneType` | 场景类型（逗号分隔） |
| `tags` | `tag`（JSON.parse） | 标签列表 |
| `merchant` | `createUser` | 商家名称 |
