# I001 发明专利检测 API 参考

## 接口信息

- **URL**: `https://saas.eric-bot.com/v1.0/eric-api/patent/utility/v1/detection`
- **Method**: POST
- **Content-Type**: application/json
- **认证 Header**: `Token: <用户的API Token>`

## 注意事项

1. 产品标题必传，最大 500 个字符；产品描述必传，最大 30000 个字符
2. 国家必传，目前只支持 US（美国）
3. 单次调用最多返回 TOP500 条相似专利，`top_number` 范围 1-500
4. 费用：限时免费（常规 10 点/次）

## 请求参数

| Parameter             | Type   | Required | Description                            |
|-----------------------|--------|----------|----------------------------------------|
| `product_title`       | string | true     | 产品标题，最大 500 字符                |
| `product_description` | string | true     | 产品描述，最大 30000 字符              |
| `regions`             | array  | true     | 售卖国家/地区代码，当前仅支持 `["US"]` |
| `top_number`          | int    | true     | 召回专利数量，最大 500                 |

## 请求示例

```json
{
  "product_title": "01918 Hefty EZ Foil Crown Oval Rack N Roaster",
  "product_description": "Product Description 01918 Hefty EZ Foil Crown Oval Rack N Roaster. Product Dimensions 145 x 663 x 1875 inches. Item Weight 255 pounds...",
  "regions": ["US"],
  "top_number": 100
}
```

## 响应结构

### 顶层

| Parameter | Type    | Description |
|-----------|---------|-------------|
| `success` | boolean | 调用是否成功 |
| `code`    | int     | 状态码      |
| `message` | string  | 调用信息    |
| `data`    | object  | 返回数据    |

### data

| Parameter | Type    | Description  |
|-----------|---------|--------------|
| `id`      | integer | 接口调用 ID  |
| `data`    | array   | 专利列表     |
| `context` | array   | 上下文信息   |

### data.data[] 专利条目

| Parameter                  | Type    | Description                            |
|----------------------------|---------|----------------------------------------|
| `global_utility_id`        | string  | 专利 ID                               |
| `patent_image_url`         | string  | 封面图（与产品最相似的一张）           |
| `title`                    | string  | 发明专利标题（英文）                   |
| `title_cn`                 | string  | 发明专利标题（中文）                   |
| `patent_abstract`          | string  | 摘要（英文）                           |
| `patent_abstract_cn`       | string  | 摘要（中文）                           |
| `similarity`               | number  | 与产品相似度（0-1，数值型）            |
| `patent_validity`          | string  | 专利有效性（Active/Invalid）           |
| `publication_number`       | string  | 公开号                                 |
| `publication_date`         | string  | 公开日 yyyy-MM-dd                      |
| `application_number`       | string  | 申请号                                 |
| `application_date`         | string  | 申请日 yyyy-MM-dd                      |
| `estimated_due_date`       | string  | 预估到期日 yyyy-MM-dd                  |
| `related_publication_date` | array   | 首次公开日 数组 yyyy-MM-dd             |
| `region`                   | string  | 受理局                                 |
| `inventors`                | array   | 发明人（含国家）数组                   |
| `applicants`               | array   | 申请人（含国家）数组                   |
| `applicant_addresses`      | array   | 权利人地址数组                         |
| `inventor_addresses`       | array   | 发明人地址数组                         |
| `priority_number`          | array   | 优先权号数组                           |
| `cpc_kind`                 | array   | CPC 分类（层级结构，见下方说明）       |
| `specification`            | string  | 说明书英文 link                        |
| `specification_cn`         | string  | 说明书中文 link                        |
| `claims`                   | string  | 权利要求英文 link                      |
| `claims_cn`                | string  | 权利要求中文 link                      |
| `images`                   | array   | 专利图片 URL 列表                      |
| `tro_holder`               | boolean | 是否 TRO 权利人专利                    |
| `tro_case`                 | boolean | 是否有 TRO 维权史                      |

### cpc_kind 结构

CPC 分类为层级数组，每一层包含：

| Parameter          | Type   | Description        |
|--------------------|--------|--------------------|
| `title_num`        | string | 大类编号（如 A）   |
| `title_cn`         | string | 大类中文名         |
| `class_num`        | string | 分类号             |
| `class_cn`         | string | 分类中文名         |
| `class_en`         | string | 分类英文名         |
| `parent_class_num` | string | 父类编号           |
| `level`            | int    | 层级               |
| `children`         | array  | 子类（结构递归同上）|

## 错误码

### 通用错误码

| code   | 常量名               | 说明                                 |
|--------|-----------------------|--------------------------------------|
| 0      | SYSTEM_ERROR          | 系统异常                             |
| 500    | SERVER_ERROR          | 服务器错误                           |
| 100007 | PARAM_INVALID         | 参数错误（缺少必填字段或格式不正确） |
| 30007  | INVALID_ACCESS_TOKEN  | Token 无效或已过期                   |

### 积分相关

| code    | 常量名                 | 说明                   |
|---------|------------------------|------------------------|
| 4000011 | CONSUME_EMPTY_ERROR    | 扣点 API 返回为空      |
| 4000012 | PRE_DEDUCT_POINT_ERROR | 预扣点失败（余额不足） |
| 4000013 | DEDUCT_POINT_ERROR     | 扣点失败               |
| 4000014 | ROLLBACK_POINT_ERROR   | 回滚积分失败           |

### 发明专利检测相关

| code    | 常量名                    | 说明               |
|---------|---------------------------|--------------------|
| 4006001 | INVENTION_RETRIEVAL_ERROR | 发明专利检测失败   |

### 超时

| code    | 常量名          | 说明                                 |
|---------|-----------------|--------------------------------------|
| 5000504 | GATEWAY_TIMEOUT | 请求超时（检测时间较长时可能触发）   |

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
    "id": 765224336382545920,
    "data": [
      {
        "related_publication_date": null,
        "application_number": "US-60597196-A",
        "inventors": ["CRNJANSKI MIHAILO(US)"],
        "applicants": null,
        "priority_number": [],
        "applicant_addresses": [],
        "title": "Roasting rack",
        "patent_abstract_cn": null,
        "inventor_addresses": [],
        "publication_date": "1996-11-12",
        "publication_number": "US-5572924-A",
        "patent_validity": "Invalid",
        "cpc_kind": [
          {
            "title_num": "A",
            "title_cn": "人类生活必需",
            "class_num": "A47J",
            "class_cn": "厨房用具",
            "class_en": "KITCHEN EQUIPMENT; COFFEE MILLS; SPICE MILLS; APPARATUS FOR MAKING BEVERAGES",
            "parent_class_num": "A47",
            "level": 3,
            "children": [
              {
                "title_num": "A",
                "title_cn": "人类生活必需",
                "class_num": "A47J37/00",
                "class_cn": "烘;烤;煎;炸",
                "class_en": "Baking; Roasting; Grilling; Frying",
                "parent_class_num": "A47J",
                "level": 4,
                "children": [
                  {
                    "title_num": "A",
                    "title_cn": "人类生活必需",
                    "class_num": "A47J37/0694",
                    "class_cn": "..{烤架}",
                    "class_en": ". . {Broiling racks}",
                    "parent_class_num": "A47J37/00",
                    "level": 5
                  }
                ]
              }
            ]
          }
        ],
        "patent_abstract": "An improved roasting rack having an infinitely adjustable width...",
        "title_cn": null,
        "application_date": "1996-02-20",
        "global_utility_id": "1627062806069186574",
        "similarity": 0.7280737161636353,
        "tro_holder": false,
        "tro_case": false,
        "region": "US",
        "images": [],
        "patent_image_url": "",
        "specification": "https://eric-cdn.eric-bot.com/google-patent/google_patent_publication_description_localized/US/US-5572924-A_en.html",
        "specification_cn": "",
        "estimated_due_date": "2016-02-20",
        "claims": "https://eric-cdn.eric-bot.com/google-patent/google_patent_publication_claims_localized/US/US-5572924-A_en.html",
        "claims_cn": ""
      }
    ],
    "context": [],
    "request_id": "20250331144814-p2EfgIpCQFBglcDs"
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

curl -s -X POST "https://saas.eric-bot.com/v1.0/eric-api/patent/utility/v1/detection" \
  -H "Content-Type: application/json" \
  -H "Token: ${ERIC_API_TOKEN}" \
  -d '{
    "product_title": "产品标题",
    "product_description": "产品描述...",
    "regions": ["US"],
    "top_number": 50
  }'
```

### Python

```python
import requests, os, sys

if "ERIC_API_TOKEN" not in os.environ:
    print("错误：请先设置 ERIC_API_TOKEN 环境变量", file=sys.stderr)
    sys.exit(1)

resp = requests.post(
    "https://saas.eric-bot.com/v1.0/eric-api/patent/utility/v1/detection",
    headers={"Content-Type": "application/json", "Token": os.environ["ERIC_API_TOKEN"]},
    json={
        "product_title": "产品标题",
        "product_description": "产品描述...",
        "regions": ["US"],
        "top_number": 50,
    },
)
data = resp.json()
```
