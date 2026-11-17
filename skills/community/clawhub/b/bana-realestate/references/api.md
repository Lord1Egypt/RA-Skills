# 巴娜房地产信息 API 参考

## 基本规则

- 请求：`POST {BASE_URL}/realestate/{method}`
- 默认服务地址：`https://wxpub.aibana.art`
- Content-Type：`application/json`
- 鉴权：每个 JSON 请求体都包含 `app_id` 和 `secure_key`
- 免费：`getCities`、`getCommunityList`
- 收费：其余方法成功调用每次 `0.4 元`
- 退款：参数错误、未知方法或上游请求失败不扣费；已预扣费用自动退回
- 并发：服务端单线程处理，请求可能排队；客户端默认超时 `180 秒`，批量请求应顺序执行

免费接口仍要求有效凭证，但不检查余额，也不产生扣费流水。

## 账号与充值

- 没有 AppID 和 SecureKey：前往巴娜 Skill 技能中心 <https://wxpub.aibana.art> 注册并生成。
- 收费接口返回 `402` 余额不足：前往巴娜 Skill 技能中心 <https://wxpub.aibana.art> 充值。
- 普通用户无需配置环境变量或操作终端；没有已保存凭证时，智能体直接在对话中请求 AppID 和 SecureKey。
- 用户提供的凭证默认保存，供后续查询自动使用；用户明确要求不保存时，仅使用一次。
- 保存位置为当前用户配置目录下的 `bana-real-estate/credentials.json`，客户端会限制文件访问权限。
- 不要在后续答复中重复展示用户的 SecureKey。

## 方法与参数

| method | 必填业务参数 | 可选参数 | 说明 |
|---|---|---|---|
| `getCities` | 无 | 无 | 获取支持的全部城市 |
| `getCommunityList` | `city` | `page` | 获取城市小区列表 |
| `getCity` | `city` | 无 | 获取单个城市配置 |
| `getCommunityListByDistrict` | `city`, `district` | `page` | 按行政区获取小区 |
| `getErshoufangList` | `city` | `page` | 获取二手房列表 |
| `getErshoufangListByDistrict` | `city`, `district` | `page` | 按行政区获取二手房 |
| `getErshoufangListByBizcircle` | `city`, `bizcircle` | `page` | 按商圈获取二手房 |
| `searchErshoufang` | `city`, `keyword` | `page` | 搜索二手房 |
| `getRentalList` | `city` | 无 | 获取租房列表 |
| `searchRental` | `city`, `keyword` | `page` | 按关键词搜索租房 |
| `searchCommunity` | `city`, `keyword` | `page` | 按关键词搜索小区 |
| `getNewHouseList` | `city` | 无 | 获取新房推荐 |

参数定义：

| 参数 | 类型 | 说明 |
|---|---|---|
| `city` | string | 城市短码，如广州 `gz`、北京 `bj`、上海 `sh`、深圳 `sz` |
| `page` | integer | 正整数，默认 `1` |
| `district` | string | 安居客 URL 中的行政区拼音编码，如 `tianhe` |
| `bizcircle` | string | 安居客 URL 中的商圈拼音编码 |
| `keyword` | string | 二手房、租房或小区搜索关键词 |

## 原始请求示例

```bash
curl -X POST https://wxpub.aibana.art/realestate/getCommunityList \
  -H 'Content-Type: application/json' \
  -d '{
    "app_id": "你的AppID",
    "secure_key": "你的SecureKey",
    "city": "gz",
    "page": 1
  }'
```

小区列表响应示例：

```json
{
  "page": 1,
  "pageSize": 30,
  "totalCount": 1200,
  "totalPages": 40,
  "data": [
    {
      "communityId": "2111103317793",
      "name": "天伦花园",
      "district": "越秀",
      "bizcircle": "建设路",
      "avgPrice": 72124,
      "onsaleCount": 47,
      "deal90DayCount": 22,
      "rentalCount": 113
    }
  ]
}
```

除小区列表外的响应字段由对应上游接口决定。只解读实际返回的字段。

## HTTP 状态码

| 状态码 | 含义 | 示例 |
|---:|---|---|
| `200` | 调用成功 | 返回接口数据 |
| `400` | JSON、参数或页码不合法 | `{"error":"city is required"}` |
| `401` | AppID/SecureKey 缺失或无效 | `{"error":"Invalid app_id or secure_key"}` |
| `402` | 收费接口余额不足；前往巴娜 Skill 技能中心充值 | `{"error":"Insufficient balance"}` |
| `404` | method 不存在 | `{"error":"Unknown method: xxx"}` |
| `500` | 数据库或计费配置错误 | `{"error":"Billing error"}` |
| `502` | CDP 或安居客上游调用失败 | `{"error":"Real-estate API error: ..."}` |
