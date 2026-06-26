# 政策合规检测 API 参考

## P001 纯图检测

### 接口信息

- **URL**: `https://saas.eric-bot.com/v1.0/eric-api/policy-compliance/v1/gun-parts-search`
- **Method**: POST
- **Content-Type**: application/json
- **认证 Header**: `Token: <用户的API Token>`

### 注意事项

1. 图片传参仅支持 base64
2. 可能存在找不到相似违规产品的情况，结果为空不是异常
3. 返回的结果都是违规产品，具体违反的政策需要结合 P002 接口获取
4. 每次调用收取 1 点费用（1 点/次，不区分国家）

### 请求参数

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `base64_image` | string | true | 产品图片 base64 编码 |
| `type` | array | true | 检测政策类型，当前支持 `["gun_parts"]` |

### 请求示例

```json
{
  "base64_image": "base64_image",
  "type": ["gun_parts"]
}
```

### 响应结构

#### data

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | int | 检测记录 ID |
| `list` | array | 匹配到的违规产品列表 |

#### data.list[]

| Parameter | Type | Description |
|-----------|------|-------------|
| `pd_title` | string | 匹配到的违规产品标题 |
| `pd_img_oss_url` | string | 匹配到的违规产品图片 |
| `pd_title_CHN_censored` | string | 违规产品中文标题 |
| `cosine` | float | 检测产品与违规产品相似度（0-1） |

### 响应示例

```json
{
  "success": true,
  "code": 200,
  "message": "success",
  "data": {
    "id": 707278136306794496,
    "list": [
      {
        "pd_title": "CMC TRIGGERS - AR-15 ANTI-WALK PIN SET",
        "pd_img_oss_url": "https://eric-oss-image.oss-cn-shenzhen.aliyuncs.com/gun_parts_brownell/globalassets_10000_ab_l_207000094_1.jpg",
        "pd_title_CHN_censored": "某品牌AR-15防走位销钉套装",
        "cosine": 0.5082343816757202
      }
    ]
  },
  "request_id": "20241022171046-pbQm4PPrqNhR4590"
}
```

---

## P002 纯文本检测

### 接口信息

- **URL**: `https://saas.eric-bot.com/v1.0/eric-api/policy-compliance/v1/detection`
- **Method**: POST
- **Content-Type**: application/json
- **认证 Header**: `Token: <用户的API Token>`

### 注意事项

1. 标题传参最大 300 个字符，描述传参最大 5000 个字符
2. 返回结果数量不可自定义
3. 每次调用收取 5 点费用（5 点/次），**图文同时入参检测仍为 5 点**（不分开计费）

### 请求参数

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `type` | array | false | P001 返回了 cosine>=0.4 的结果时传入对应类型 |
| `product_title` | string | true | 产品标题（最大 300 字符） |
| `product_description` | string | true | 产品描述（最大 5000 字符） |
| `product_title_suspected` | array | false | type 有值时传入 P001 中相似度最高的违规产品标题 |
| `platform_sites` | object | true | 平台与国家/地区映射，如 `{"amazon": ["us", "jp"]}` |
| `feature_detect` | object | false | 风险特征词检测配置 |

#### feature_detect 对象

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `enable` | boolean | true | 是否开启风险特征词检测 |
| `features` | array | false | 自定义特征词列表 |
| `feature_word_ids` | array | false | P007 中已保存的特征词 ID 列表 |
| `image` | string | false | 产品图片 base64（用于特征词图文联合检测） |

### 请求示例

```json
{
  "product_title": "Sony WH-XB910N EXTRA BASS Noise Cancelling Headphones",
  "product_description": "Dual Noise Cancelling for intense music...",
  "product_title_suspected": [],
  "type": [],
  "platform_sites": {"amazon": ["us", "jp", "ca"]},
  "feature_detect": {
    "enable": false
  }
}
```

### 响应结构

#### data

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | int | 检测记录 ID |
| `list` | array | 政策匹配列表 |

#### data.list[]

| Parameter | Type | Description |
|-----------|------|-------------|
| `platform` | string | 平台 |
| `site` | string | 国家/地区 |
| `prohibited` | int | 是否禁售（1=禁售, 0=非禁售） |
| `compliance` | int | 是否限售（1=限售, 0=非限售） |
| `reason` | string | 禁售/限售原因 |
| `content_url` | string | 平台政策原文 URL |
| `name_cn` | string | 政策中文标题 |
| `name` | string | 政策英文标题 |

### 响应示例

```json
{
  "success": true,
  "code": 200,
  "message": "success",
  "data": {
    "id": 707588166881103872,
    "list": [
      {
        "platform": "Amazon",
        "prohibited": 1,
        "compliance": 0,
        "reason": "这是一个盐基杀虫器，根据武器和仿真武器政策，属于禁售商品。",
        "site": "CA",
        "content_url": "https://sellercentral.amazon.ca/help/hub/reference/external/G200164950",
        "name_cn": "武器和仿製武器",
        "name": "Weapons and imitation weapons"
      },
      {
        "platform": "Amazon",
        "prohibited": 0,
        "compliance": 1,
        "reason": "受到美国EPA法规监管，需要提供有效的EPA注册号。",
        "site": "US",
        "content_url": "https://sellercentral.amazon.com/help/hub/reference/external/G202115120",
        "name_cn": "害虫防治商品和农药",
        "name": "Pest control products and pesticides"
      }
    ]
  },
  "request_id": "20241023134219-bdMiR8L8DDaouZHA"
}
```

---

## P004 风险特征词联想

### 接口信息

- **URL**: `https://saas.eric-bot.com/v1.0/eric-api/policy-compliance/feature/v1/suggestion`
- **Method**: POST
- **Content-Type**: application/json
- **认证 Header**: `Token: <用户的API Token>`

### 注意事项

1. 获取到词后需通过 P005 保存到系统
2. 【Beta 版】每天限定特征词调用次数 50 次

### 请求参数

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `word` | string | true | 需要联想的模糊词 |

### 响应结构

#### data

| Parameter | Type | Description |
|-----------|------|-------------|
| `word_arr` | array | 联想出的清晰特征词列表（不包含输入词本身） |
| `status` | integer | -2=含糊无关, -1=已够清晰, 0=模糊匹配出多个清晰词 |
| `suggestion_num` | integer | 联想词总数 |

### 响应示例

```json
{
  "success": true,
  "code": 200,
  "message": "",
  "data": {
    "word_arr": [
      "用于攻击或防御的黑色开刃刀具",
      "黑色开刃匕首",
      "黑色开刃战术刀",
      "黑色开刃求生刀"
    ],
    "status": 0,
    "suggestion_num": 24
  },
  "request_id": "20241212110705-lQVMxPjt8TnDlR7n"
}
```

---

## P005 风险特征词保存

### 接口信息

- **URL**: `https://saas.eric-bot.com/v1.0/eric-api/policy-compliance/feature/v1/save`
- **Method**: POST
- **Content-Type**: application/json
- **认证 Header**: `Token: <用户的API Token>`

### 请求参数

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `word` | string | true | 要保存的特征词 |

### 响应示例

```json
{
  "success": true,
  "code": 200,
  "message": "",
  "data": {"id": 429},
  "request_id": "20250113175421-g6DefjpYUyfIPY0b"
}
```

---

## P006 风险特征词删除

### 接口信息

- **URL**: `https://saas.eric-bot.com/v1.0/eric-api/policy-compliance/feature/v1/delete`
- **Method**: POST
- **Content-Type**: application/json
- **认证 Header**: `Token: <用户的API Token>`

### 请求参数

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | integer | true | 特征词 ID 编号 |

### 响应示例

```json
{
  "success": true,
  "code": 200,
  "message": "",
  "data": {"id": 429},
  "request_id": "20241212154238-gikzorU0KKA1Auvh"
}
```

---

## P007 风险特征词列表

### 接口信息

- **URL**: `https://saas.eric-bot.com/v1.0/eric-api/policy-compliance/feature/v1/list`
- **Method**: POST
- **Content-Type**: application/json
- **认证 Header**: `Token: <用户的API Token>`

### 注意事项

保存后需等拉取状态成功（`pull_status=1`）后，风险词才能在检测中使用。

### 请求参数

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `per_page` | integer | true | 每页条数 |
| `page` | integer | true | 页码 |

### 响应结构

#### data

| Parameter | Type | Description |
|-----------|------|-------------|
| `current_page` | int | 当前页码 |
| `data` | array | 特征词列表（按创建时间倒序） |
| `from` | int | 起始序号 |
| `per_page` | int | 每页条数 |
| `to` | int | 结束序号 |
| `total` | int | 总数 |

#### data.data[]

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | int | 特征词 ID |
| `pull_status` | integer | 0=未拉取, 1=拉取成功, 2=拉取失败 |
| `words` | string | 特征风险词 |
| `create_time` | string | 创建时间 |

### 响应示例

```json
{
  "success": true,
  "code": 200,
  "message": "",
  "data": {
    "current_page": 1,
    "data": [
      {
        "id": 5,
        "pull_status": 0,
        "words": "黑色厨房用刀具（包括砍骨刀和切片刀）",
        "create_time": "2024-12-12 15:14:30"
      },
      {
        "id": 4,
        "pull_status": 0,
        "words": "色战术刀具",
        "create_time": "2024-12-12 15:11:09"
      }
    ],
    "from": 1,
    "per_page": 15,
    "to": 3,
    "total": 3
  },
  "request_id": "20241212154448-mUVSEoRpjPhXqssB"
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

### 图片上传相关

| code | 常量名 | 说明 |
|---------|----------------------|--------------------------|
| 4000020 | OSS_UPLOAD_ERROR | 图片上传 OSS 异常 |
| 4000021 | OSS_UPLOAD_URL_ERROR | 图片 URL 上传 OSS 异常 |

### 政策合规检测相关

| code | 常量名 | 说明 |
|---------|----------------------------------------------|--------------------------------------|
| 4004001 | POLICY_IS_COVERNED_EMPTY_ERROR | 政策覆盖检测返回为空 |
| 4004002 | POLICY_IS_COVERNED_ERROR | 政策覆盖检测异常 |
| 4004003 | POLICY_VALIDATA_SALE_STATUS_EMPTY_ERROR | 销售状态验证返回为空 |
| 4004004 | POLICY_VALIDATA_SALE_STATUS_ERROR | 销售状态验证异常 |
| 4004005 | SUSPECTED_POLICY_VALIDATA_SALE_STATUS_EMPTY_ERROR | 疑似违规销售状态验证返回为空 |
| 4004006 | SUSPECTED_POLICY_VALIDATA_SALE_STATUS_ERROR | 疑似违规销售状态验证异常 |
| 4004007 | SEARCH_GUN_PARTS_EMPTY_ERROR | 枪械配件检测返回为空 |
| 4004008 | SEARCH_GUN_PARTS_ERROR | 枪械配件检测异常 |
| 4004009 | GET_BY_CROPPED_UID_EMPTY_ERROR | 裁剪 UID 查询返回为空 |
| 4004010 | GET_BY_CROPPED_UID | 裁剪 UID 查询异常 |
| 4004011 | BI_RADAR_V1_API_EMPTY_ERROR | BI 雷达 API 返回为空 |
| 4004012 | BI_RADAR_V1_API_ERROR | BI 雷达 API 异常 |
| 4004020 | DELETE_FEATURE_NO_EXIST_FAIL | 删除特征词不存在 |
| 4004021 | DELETE_FEATURE_WORD_FAIL | 删除特征词失败 |

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

### P001 Shell

```bash
# 检查 Token 环境变量
if [ -z "${ERIC_API_TOKEN}" ]; then
  echo "错误：请先设置 ERIC_API_TOKEN 环境变量" >&2
  exit 1
fi

if [[ "$OSTYPE" == "darwin"* ]]; then
  IMG_B64=$(base64 -i /path/to/image.png | tr -d '\n')
else
  IMG_B64=$(base64 -w 0 /path/to/image.png)
fi

curl -s -X POST "https://saas.eric-bot.com/v1.0/eric-api/policy-compliance/v1/gun-parts-search" \
  -H "Content-Type: application/json" \
  -H "Token: ${ERIC_API_TOKEN}" \
  -d "{\"base64_image\": \"${IMG_B64}\", \"type\": [\"gun_parts\"]}"
```

### P001 Python

```python
import base64, requests, os, sys

if "ERIC_API_TOKEN" not in os.environ:
    print("错误：请先设置 ERIC_API_TOKEN 环境变量", file=sys.stderr)
    sys.exit(1)

with open("/path/to/image.png", "rb") as f:
    img_b64 = base64.b64encode(f.read()).decode()

resp = requests.post(
    "https://saas.eric-bot.com/v1.0/eric-api/policy-compliance/v1/gun-parts-search",
    headers={"Content-Type": "application/json", "Token": os.environ["ERIC_API_TOKEN"]},
    json={"base64_image": img_b64, "type": ["gun_parts"]},
)
data = resp.json()
```

### P002 Shell

```bash
# 检查 Token 环境变量
if [ -z "${ERIC_API_TOKEN}" ]; then
  echo "错误：请先设置 ERIC_API_TOKEN 环境变量" >&2
  exit 1
fi

curl -s -X POST "https://saas.eric-bot.com/v1.0/eric-api/policy-compliance/v1/detection" \
  -H "Content-Type: application/json" \
  -H "Token: ${ERIC_API_TOKEN}" \
  -d '{
    "product_title": "产品标题",
    "product_description": "产品描述...",
    "type": [],
    "product_title_suspected": [],
    "platform_sites": {"amazon": ["us", "jp"]},
    "feature_detect": {"enable": false}
  }'
```

### P002 Python

```python
import requests, os, sys

if "ERIC_API_TOKEN" not in os.environ:
    print("错误：请先设置 ERIC_API_TOKEN 环境变量", file=sys.stderr)
    sys.exit(1)

resp = requests.post(
    "https://saas.eric-bot.com/v1.0/eric-api/policy-compliance/v1/detection",
    headers={"Content-Type": "application/json", "Token": os.environ["ERIC_API_TOKEN"]},
    json={
        "product_title": "产品标题",
        "product_description": "产品描述...",
        "type": [],
        "product_title_suspected": [],
        "platform_sites": {"amazon": ["us", "jp"]},
        "feature_detect": {"enable": False},
    },
)
data = resp.json()
```
