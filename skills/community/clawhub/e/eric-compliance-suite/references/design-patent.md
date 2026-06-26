# D001 外观专利检测 API 参考

## 接口信息

- **URL**: `https://saas.eric-bot.com/v1.0/eric-api/patent/design/v1/detection`
- **Method**: POST
- **Content-Type**: application/json
- **认证 Header**: `Token: <用户的API Token>`

## 注意事项

1. 图片传参仅支持 base64
2. 单次调用最多返回 TOP500 条相似专利，`top_number` 范围 1-500
3. 不传产品文本信息时无法使用模型推荐 LOC 功能，传 `[]` 或 `null` 默认全部 LOC 分类
4. 费用：`enable_radar=false` 收取 10 点/次，`enable_radar=true` 收取 15 点/次（雷达取前 20 个专利分析）

## 请求参数

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `product_title` | string | false | 产品标题 |
| `product_description` | string | false | 产品描述 |
| `regions` | array | true | 售卖国家/地区代码，支持：SE, EU, CH, IE, BR, MX, US, WO, GB, IL, JP, IN, DK, DE, AU, IT, NZ, AT, CA, BX, FI, FR, CN, KR, TH, MY |
| `img_64lis` | array | true | 商品图片 Base64 列表，目前仅支持一张 |
| `top_loc` | array | false | 一级 LOC 范围。`["13","02"]` 指定 LOC；`[]` 全部 LOC；`null` 模型预测 LOC |
| `patent_status` | array | false | 专利有效性。`1` 有效，`0` 失效，空=全部 |
| `top_number` | integer | true | 召回专利数量，最大 500 |
| `enable_tro` | boolean | true | TRO 增强 |
| `source_language` | string | false | 原语言代码（如 `zh-CN`），英文传空 |
| `query_mode` | string | true | `physical`(实物图) / `line`(线条图) / `hybrid`(混合) |
| `enable_radar` | boolean | false | 是否开启雷达风险分析，默认 false |

## 请求示例

```json
{
  "product_title": "Tennis Paddle Racket with Bag",
  "product_description": "",
  "regions": ["US", "GB", "FR", "AU", "IT", "DE", "JP"],
  "img_64lis": ["iVBORw0KGgoAAAANSUhEUgAA..."],
  "top_loc": ["01"],
  "patent_status": [1],
  "top_number": 5,
  "enable_tro": true,
  "source_language": "zh-CN",
  "query_mode": "hybrid",
  "enable_radar": true
}
```

## 响应结构

### 顶层

| Parameter | Type | Description |
|-----------|------|-------------|
| `success` | boolean | 调用是否成功 |
| `code` | integer | 状态码 |
| `message` | string | 调用信息 |
| `data` | object | 返回数据 |

### data

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | integer | 接口调用 ID |
| `list` | array | 专利列表 |
| `detail` | object | 检测详情 |

### data.list[] 专利条目

| Parameter | Type | Description |
|-----------|------|-------------|
| `global_patent_id` | string | 全球专利 ID |
| `patent_image_url` | string | 相似度最高的专利附图 URL |
| `patent_prod` | string | 专利标题（英文） |
| `patent_prod_cn` | string | 专利标题（中文） |
| `patent_loc` | string | LOC 分类，逗号分隔 |
| `is_sketch` | string | 是否线稿图 |
| `registration_office_code` | string | 专利注册受理局 |
| `grant_date` | string | 授权日 |
| `estimated_due_date` | string | 预估到期日 |
| `application_date` | string | 申请日 |
| `publication_date` | string | 公开日 |
| `patent_validity` | string | 有效性（Active/Invalid） |
| `abstracts` | string | 专利摘要 |
| `specification` | string | 专利说明书 |
| `inventors` | array | 发明人列表 |
| `applicants` | array | 申请人列表 |
| `applicant_adresses` | array | 申请人地址 |
| `publication_number` | string | 公开号 |
| `application_number` | string | 申请号 |
| `images` | array | 专利图片 URL 列表 |
| `similarity` | string | 与产品相似度（0-1） |
| `tro_holder` | boolean | 是否 TRO 权利人专利 |
| `tro_case` | boolean | 是否有 TRO 维权史 |
| `patent_family` | array | 同族专利（结构同 list[]） |
| `radar_result` | object | 雷达结果：`{same: bool, exp: string}` |
| `global_image_id` | string | 专利图片 ID |
| `loc_one` | array | LOC 一级详情：`[{code, parent_code, description}]` |
| `loc_two` | array | LOC 二级详情：`[{code, parent_code, description}]` |

### data.detail

| Parameter | Type | Description |
|-----------|------|-------------|
| `product_title` | string | 产品标题 |
| `product_keywords` | string | 产品关键词 |
| `product_prediction_loc` | array | 模型预测 LOC |
| `product_point_loc` | array | 指定 LOC |
| `keywords_filter` | array | 关键词分组：`[{global_patent_id_list, patent_image_url, keyword}]` |

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

### 外观专利检测相关

| code | 常量名 | 说明 |
|---------|----------------------------------------|--------------------------|
| 4001001 | DESIGN_PATEN_REVER_EMPTY_ERROR | 检测接口返回为空 |
| 4001002 | DESIGN_PATEN_REVER_ERROR | 接口数据返回为空 |
| 4001003 | DESIGN_PATEN_MULTIPLE_RESULT | 接口数据为空 |
| 4001004 | DESIGN_DPAS_SOFA_EMPTY_ERROR | SOFA 接口数据为空 |
| 4001005 | DESIGN_CONFIDENCE_INTERVAL_EMPTY_ERROR | 置信区间返回为空 |
| 4001006 | DESIGN_CONFIDENCE_INTERVAL_ERROR | 置信区间数据为空 |
| 4001007 | DESIGN_BATCH_DPSA_ERROR | 外观批量雷达接口检测失败 |

### 翻译相关

| code | 常量名 | 说明 |
|---------|------------------------|----------------------|
| 4001008 | TRANSLATE_EMPTY_ERROR | 翻译接口返回为空 |
| 4001009 | TRANSLATE_ERROR | 翻译接口异常 |

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

## 响应示例

```json
{
  "success": true,
  "code": 200,
  "message": "success",
  "data": {
    "id": 768528235190620200,
    "list": [
      {
        "global_patent_id": "1661532815902113979",
        "patent_image_url": "https://patent-oss-image.eric-bot.com/DESIGN_PATENT_IMG/US/1661532815902113979/1.png",
        "patent_prod": "Media device",
        "registration_office_code": "US",
        "grant_date": "2007-04-24",
        "patent_validity": "Invalid",
        "applicants": ["Apple Computer, Inc."],
        "publication_number": "USD541299S1",
        "patent_prod_cn": "媒体设备",
        "images": [
          "https://patent-oss-image.suntekcorps.com/DESIGN_PATENT_IMG/US/1661532815902113979/1.png"
        ],
        "similarity": "0.98",
        "tro_holder": false,
        "tro_case": false,
        "patent_family": [],
        "radar_result": null,
        "loc_one": [{"code": "14", "parent_code": "", "description": "记录、电信或数据处理设备"}],
        "loc_two": [{"code": "14-03", "parent_code": "14", "description": "电信设备、无线遥控设备和无线电放大器"}]
      }
    ],
    "detail": {
      "product_title": "example product",
      "product_keywords": "product keywords",
      "product_prediction_loc": ["10", "14", "13"],
      "product_point_loc": ["10", "14", "13"],
      "keywords_filter": [
        {
          "global_patent_id_list": ["1661538226571051743"],
          "patent_image_url": "https://patent-oss-image.eric-bot.com/...",
          "keyword": "关键词"
        }
      ]
    }
  }
}
```

## 代码示例

### Shell

```bash
# 检查 Token 环境变量
if [ -z "${ERIC_API_TOKEN}" ]; then
  echo "错误：请先设置 ERIC_API_TOKEN 环境变量" >&2
  exit 1
fi

# base64 编码（跨平台兼容）
if [[ "$OSTYPE" == "darwin"* ]]; then
  IMG_B64=$(base64 -i /path/to/image.png | tr -d '\n')
else
  IMG_B64=$(base64 -w 0 /path/to/image.png)
fi

curl -s -X POST "https://saas.eric-bot.com/v1.0/eric-api/patent/design/v1/detection" \
  -H "Content-Type: application/json" \
  -H "Token: ${ERIC_API_TOKEN}" \
  -d "$(cat <<EOF
{
  "product_title": "产品标题",
  "regions": ["US", "GB"],
  "img_64lis": ["${IMG_B64}"],
  "top_number": 50,
  "enable_tro": true,
  "query_mode": "hybrid",
  "enable_radar": false
}
EOF
)"
```

### Python

```python
import base64, requests, os, sys

if "ERIC_API_TOKEN" not in os.environ:
    print("错误：请先设置 ERIC_API_TOKEN 环境变量", file=sys.stderr)
    sys.exit(1)

with open("/path/to/image.png", "rb") as f:
    img_b64 = base64.b64encode(f.read()).decode()

resp = requests.post(
    "https://saas.eric-bot.com/v1.0/eric-api/patent/design/v1/detection",
    headers={"Content-Type": "application/json", "Token": os.environ["ERIC_API_TOKEN"]},
    json={
        "regions": ["US", "GB"],
        "img_64lis": [img_b64],
        "top_number": 50,
        "enable_tro": True,
        "query_mode": "hybrid",
        "enable_radar": False,
    },
)
data = resp.json()
```
