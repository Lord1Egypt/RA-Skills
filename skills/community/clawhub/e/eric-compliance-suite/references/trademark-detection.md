# T001 文本商标检测 + T002 商标替换词 API 参考

## T001 文本商标检测

### 接口信息

- **URL**: `https://saas.eric-bot.com/v1.0/eric-api/trademark/text/v1/detection`
- **Method**: POST
- **Content-Type**: application/json
- **认证 Header**: `Token: <用户的API Token>`

### 注意事项

1. 标题传参最大 300 个字符，描述传参最大 5000 个字符
2. 每次调用收取 1 点费用（1 点/次）

### 请求参数

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `product_title` | string | true | 产品标题（最大 300 字符） |
| `product_text` | string | false | 产品的其他文本信息（最大 5000 字符） |
| `regions` | array | true | 售卖国家/地区代码，支持：US, GB, DE, JP, AU, TR, IT, ES, MX, NL, CA, FR |

### 请求示例

```json
{
  "product_title": "Ps4 Wireless Controller Bluetooth Gamepad Play Station 4 Remote",
  "product_text": "This PS4 controller is made of highly durable material with a cool appearance...",
  "regions": ["US", "JP", "DE", "GB"]
}
```

### 响应结构

#### 顶层

| Parameter | Type | Description |
|-----------|------|-------------|
| `success` | boolean | 调用是否成功 |
| `code` | integer | 状态码 |
| `message` | string | 调用信息 |
| `data` | object | 返回数据 |

#### data

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | integer | 接口调用 ID |
| `trademark_list` | array | 商标词列表 |
| `text_trademark_radar` | int | 产品风险等级：0=低风险, 1=待人工核查, 2=高风险 |
| `blackwhitelist_trademarks` | object | 黑白名单列表 |

#### data.trademark_list[]

| Parameter | Type | Description |
|-----------|------|-------------|
| `trademark` | string | 商标词 |
| `common_sense` | boolean | 是否常用词 |
| `compatibility` | boolean | 是否兼容性用法 |
| `active_holder` | boolean | 是否有活跃维权人 |
| `famous` | boolean | 是否著名商标 |
| `amazon_brand` | boolean | 是否 Amazon 热搜品牌 |
| `status` | string | 最高分商标词状态（Active/pending/end） |
| `mode_ns_codes` | array | 模型推荐的尼斯分类代码 |
| `highest_mode_score` | integer | 最高风险分数（0-5） |
| `from` | array | 原文中的出处词语 |
| `region_score` | array | 各国家/地区风险分数：`[{region, score}]` |

#### data.blackwhitelist_trademarks

| Parameter | Type | Description |
|-----------|------|-------------|
| `blacklist_trademarks` | array | 黑名单：`[{trademark, note, region}]` |
| `whitelist_trademarks` | array | 白名单：`[{trademark, note, region}]` |

### 响应示例

```json
{
  "success": true,
  "code": 200,
  "message": "success",
  "data": {
    "id": 753661385410523137,
    "trademark_list": [
      {
        "trademark": "summer heat",
        "common_sense": true,
        "compatibility": false,
        "active_holder": false,
        "famous": false,
        "amazon_brand": false,
        "status": "active",
        "mode_ns_codes": ["17", "22", "19"],
        "highest_mode_score": 0,
        "from": ["Summer Heat"],
        "region_score": [{"region": "EM", "score": 0}]
      },
      {
        "trademark": "wall",
        "common_sense": true,
        "compatibility": false,
        "active_holder": true,
        "famous": false,
        "amazon_brand": false,
        "status": "active",
        "mode_ns_codes": ["17", "22", "19"],
        "highest_mode_score": 0,
        "from": ["Wall"],
        "region_score": [{"region": "EM", "score": 0}]
      }
    ],
    "blackwhitelist_trademarks": {
      "blacklist_trademarks": [
        {"trademark": "summer heat", "note": "", "region": "EM"}
      ],
      "whitelist_trademarks": [
        {"trademark": "along", "note": "", "region": "EM"}
      ]
    },
    "text_trademark_radar": 0
  },
  "request_id": "20250227170115-G2iuGHFfNsaCdCS7"
}
```

---

## T002 商标替换词

### 接口信息

- **URL**: `https://saas.eric-bot.com/v1.0/eric-api/trademark/text/v1/safe-words-generation`
- **Method**: POST
- **Content-Type**: application/json
- **认证 Header**: `Token: <用户的API Token>`

### 注意事项

1. 标题传参最大 300 个字符，描述传参最大 5000 个字符
2. `trademark` 参数当前仅支持字符串类型单个请求
3. 每次调用收取 1 点费用（1 点/次）
4. 如果超过最大重试设定值，返回 false 后需用户自行判断是直接删除还是人为干预

### 请求参数

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `product_title` | string | true | 产品标题 |
| `product_text` | string | true | 产品描述 |
| `trademark_name` | string | true | T001 中检测出的商标词（单个） |

### 请求示例

```json
{
  "product_title": "Locsanity Daily Moisturizing Refreshing Spray for Locs",
  "product_text": "Bring Your Locs Back to Life - Our Rosewater and Peppermint Daily Spray...",
  "trademark_name": "refreshing"
}
```

### 响应结构

#### data

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | integer | 数据 ID |
| `words` | array | 推荐替换的安全词语列表 |

### 响应示例

```json
{
  "success": true,
  "code": 200,
  "message": "success",
  "data": {
    "id": 707262153340968960,
    "words": ["invigorating"]
  },
  "request_id": "20241022160716-mexpOgDw556ud3wf"
}
```

---

## 错误码

### 通用错误码

| code | 常量名 | 说明 |
|--------|--------------------------------------|--------------------------------------|
| 0 | SYSTEM_ERROR | 系统异常 |
| 500 | SERVER_ERROR | 服务器错误 |
| 100007 | PARAM_INVALID | 参数错误（缺少必填字段或格式不正确） |
| 30007 | INVALID_ACCESS_TOKEN | Token 无效或已过期 |

### 积分相关

| code | 常量名 | 说明 |
|---------|------------------------|------------------------|
| 4000011 | CONSUME_EMPTY_ERROR | 扣点 API 返回为空 |
| 4000012 | PRE_DEDUCT_POINT_ERROR | 预扣点失败（余额不足） |
| 4000013 | DEDUCT_POINT_ERROR | 扣点失败 |
| 4000014 | ROLLBACK_POINT_ERROR | 回滚积分失败 |

### 文本商标检测相关

| code | 常量名 | 说明 |
|---------|--------------------------------------|--------------------------------------|
| 4003001 | T_DSC_NC_CODE_EMPTY_ERROR | 商标分类接口返回为空 |
| 4003002 | T_DSC_NC_CODE_ERROR | 商标分类接口异常 |
| 4003003 | ES_QUERY_WORD_EMPTY_ERROR | ES 查询词返回为空 |
| 4003004 | ES_QUERY_WORD_ERROR | ES 查询词接口异常 |
| 4003005 | BRAND_DETAILS_ERROR | 品牌详情接口异常 |
| 4003006 | TRADEMARK_CLASSIFICATION_ERROR | 商标分类异常 |
| 4003011 | TRADEMARK_CLASSIFICATION_EMPTY_ERROR | 商标分类返回为空 |

### 替换词相关

| code | 常量名 | 说明 |
|---------|--------------------------|--------------------------------------|
| 4003007 | SAFE_WORD_ERROR | 安全词接口异常 |
| 4003008 | SAFE_WORD_SAVE_ERROR | 安全词保存异常 |
| 4003009 | SAFE_WORD_INAPPROPRIATE_ERROR | 安全词不适用 |
| 4003010 | NO_SAFE_WORD | 无可用安全替换词 |

### 超时

| code | 常量名 | 说明 |
|---------|-----------------|--------------------------------------|
| 5000504 | GATEWAY_TIMEOUT | 请求超时（检测时间较长时可能触发） |

### 错误响应示例

```json
{
  "success": false,
  "code": 100007,
  "message": "参数错误",
  "data": null
}
```

## 代码示例

### T001 Shell

```bash
# 检查 Token 环境变量
if [ -z "${ERIC_API_TOKEN}" ]; then
  echo "错误：请先设置 ERIC_API_TOKEN 环境变量" >&2
  exit 1
fi

curl -s -X POST "https://saas.eric-bot.com/v1.0/eric-api/trademark/text/v1/detection" \
  -H "Content-Type: application/json" \
  -H "Token: ${ERIC_API_TOKEN}" \
  -d '{
    "product_title": "Ps4 Wireless Controller Bluetooth Gamepad",
    "product_text": "This PS4 controller is made of highly durable material...",
    "regions": ["US", "JP", "DE", "GB"]
  }'
```

### T001 Python

```python
import requests, os, sys

if "ERIC_API_TOKEN" not in os.environ:
    print("错误：请先设置 ERIC_API_TOKEN 环境变量", file=sys.stderr)
    sys.exit(1)

resp = requests.post(
    "https://saas.eric-bot.com/v1.0/eric-api/trademark/text/v1/detection",
    headers={"Content-Type": "application/json", "Token": os.environ["ERIC_API_TOKEN"]},
    json={
        "product_title": "Ps4 Wireless Controller Bluetooth Gamepad",
        "product_text": "This PS4 controller is made of highly durable material...",
        "regions": ["US", "JP", "DE", "GB"],
    },
)
data = resp.json()
```

### T002 Shell

```bash
# 检查 Token 环境变量
if [ -z "${ERIC_API_TOKEN}" ]; then
  echo "错误：请先设置 ERIC_API_TOKEN 环境变量" >&2
  exit 1
fi

curl -s -X POST "https://saas.eric-bot.com/v1.0/eric-api/trademark/text/v1/safe-words-generation" \
  -H "Content-Type: application/json" \
  -H "Token: ${ERIC_API_TOKEN}" \
  -d '{
    "product_title": "产品标题",
    "product_text": "产品描述...",
    "trademark_name": "refreshing"
  }'
```

### T002 Python

```python
import requests, os, sys

if "ERIC_API_TOKEN" not in os.environ:
    print("错误：请先设置 ERIC_API_TOKEN 环境变量", file=sys.stderr)
    sys.exit(1)

resp = requests.post(
    "https://saas.eric-bot.com/v1.0/eric-api/trademark/text/v1/safe-words-generation",
    headers={"Content-Type": "application/json", "Token": os.environ["ERIC_API_TOKEN"]},
    json={
        "product_title": "产品标题",
        "product_text": "产品描述...",
        "trademark_name": "refreshing",
    },
)
safe_words = resp.json()
```
