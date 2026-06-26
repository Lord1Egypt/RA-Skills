# 文旅素材搜索 API 参考

## 基址来源（可配置）

1. **环境变量** `WENLV_API_ORIGIN`：仅站点根（如 `https://test.data0086.com`）。若设置，优先使用。
2. 否则使用与本 Skill 同目录的 [config.json](../config.json) 中的 `api_origin`。
3. **`search_url`** = `api_origin`（去尾 `/`）+ `search_path`（默认 `/ms-base/home/getList`）+ `?pageNum={pageNum}&pageSize={pageSize}`。

搜索：`POST {search_url}`，`Content-Type: application/json`，**无需鉴权**（`token` 头可为空）。

## 详情页（用户点击「预览」）

商品详情页地址（数游神州前端 SPA hash 路由）：

```text
{api_origin}/#/multimodal?businessCode={businessCode}
```

默认 `detail_path` 为 **`/#/multimodal`**，即 `{api_origin}/#/multimodal?businessCode={businessCode}`。

**与 `fragmentUrl` 的区别**：`fragmentUrl` 是 **媒体流**（常为 HLS 预览地址），在 Markdown 里作为主链接易导致 **下载 m3u8** 或无法播放；**表格/卡片中的可点击「预览」** 必须使用上式的 **详情页** URL，**不要**使用 `fragmentUrl`。`fragmentUrl` 仍保留在结构化结果中供交易与调试。

## 请求 URL 参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `pageNum` | integer | 否 | 页码，默认 1 |
| `pageSize` | integer | 否 | 每页条数，默认 18；**智能体侧默认传 `5`** |

## 请求体

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `search` | string | 是 | 搜索关键词，支持中文 |
| `city` | string | 否 | 城市行政区划代码，默认 `"330300"`（温州） |
| `commodityCode` | string \| null | 否 | 按商品编码精确筛选。Skill 用此字段分两次调用：成片传 `finished_commodity_code`（见 config.json），素材传 `null` |
| `sceneType` | string | 否 | 场景类型筛选，逗号分隔 |
| `tradeType` | string | 否 | 交易类型筛选，如 `"cash"` |

## 响应顶层

```json
{
  "code": 0,
  "msg": "请求处理成功",
  "resData": {
    "total": 185,
    "datas": []
  }
}
```

## `resData.datas[]` 单条素材（原始）

典型字段（实际以接口为准）：

| 字段 | 说明 |
|------|------|
| `id` | 素材数字 ID |
| `commodityName` | 商品标题 |
| `commodityCode` | 商品编码（交易下单必需） |
| `businessCode` | 业务编码（交易下单必需，详情页 URL 参数） |
| `explain` | 商品说明（HTML 表格，含清晰度、格式等） |
| `tag` | 标签（JSON 字符串数组，需 `JSON.parse`） |
| `price` | 价格（元） |
| `sceneType` | 场景类型，逗号分隔 |
| `tradeType` | 交易类型 |
| `location` | 地区编码（JSON 字符串数组） |
| `breviaryPic` | 封面缩略图（完整 URL） |
| `fragmentUrl` | 预览视频流（HLS 地址） |
| `fragmentTime` | 预览视频时长（秒，字符串） |
| `videoProductCode` | 视频产品编码 |
| `status` | 状态码，`2` = 已上架 |
| `createUser` | 商家名称 |
| `createTime` / `updateTime` | 时间 |
| `contactName` / `contactPhone` | 联系人 |
| `merchantBusinessCode` | 商家业务编码 |
| `priceJson` | 价格方案（JSON 字符串数组） |
| `sampleDealType` | 样片处理方式，如 `"waterprint"` |

### 重点字段

| 字段 | 说明 |
|------|------|
| `fragmentUrl` | **预览流**（HLS），**P0** |
| `breviaryPic` | 封面完整 URL，**P0** |
| `commodityCode` | 商品编码，**P0**（交易必需） |
| `businessCode` | 业务编码，**P0**（交易必需 + 详情页 URL） |
| `fragmentTime` | 时长（秒，字符串） |
| `price` | 价格（元） |

## `fragmentUrl` 类型判定

| 类型 | 条件 | 播放 |
|------|------|------|
| HLS | URL 含 `/hls/` | 需 HLS 播放器 |
| MP4 | URL 以 `.mp4` 结尾 | 浏览器 `<video>` 可直接播 |

## 封面 `cover_url`

新接口的 `breviaryPic` 已是**完整绝对 URL**（如 `https://wenzhou.data0086.com:9443/res/covers/xxx.jpg`），无需像旧接口那样拼接 `api_origin` + 相对路径。

嵌入前仍须校验 URL 主机属于 `trusted_media_origins`（`wenzhou.data0086.com:9443` 已在 config 中声明）。

## 调用示例

```bash
ORIGIN="${WENLV_API_ORIGIN:-https://test.data0086.com}"
curl "${ORIGIN}/ms-base/home/getList?pageNum=1&pageSize=5" \
  -H 'Content-Type: application/json' \
  -H "Origin: ${ORIGIN}" \
  -H "Referer: ${ORIGIN}/" \
  -H 'token;' \
  --data-raw '{"commodityCode":null,"sceneType":"","tradeType":"","search":"雁荡山","city":"330300"}'
```
