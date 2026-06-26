# Capability: text_search (文本搜索)

## 功能说明
通过用户输入的关键词或自然语言描述，在 1688 平台搜索匹配的商品列表。与 image_search 和 link_search 共用同一 API 接口。

## 触发方式
**Skill 级触发词**: 找商品、搜商品、想要 XX、帮我找 XX

**Capability 识别特征**:
- 用户输入包含商品描述性语言
- 不包含图片附件
- 不包含完整 URL 链接

## 前置条件
- 已配置 AK。**Agent 判断 AK 是否已配置时，必须通过执行 `cli.py configure`（无参数）确认，禁止仅凭环境变量或对话历史判断**。AK 可能已持久化在本地配置文件中，即使当前对话未提及也可能已配置。

## CLI 调用（Agent 执行时必须使用）
```bash
python3 {baseDir}/cli.py text_search --query "搜索关键词" [--limit 10] [--sort price_asc] [--score-level high] [--purchase-amount 1] [--tags 4306497] [--ic-tags ""]
```

### 命令行参数
| 参数 | 简写 | 说明 | 默认值 |
|------|------|------|--------|
| `--query` | `-q` | 搜索关键词 | 必需 |
| `--platform` | `-p` | 目标平台 | 1688 |
| `--limit` | `-l` | 返回数量 | 10 |
| `--sort` | `-s` | 排序方式：`price_asc`(价格低→高)、`price_desc`(价格高→低)、`sold_desc`(销量高→低)、`yx_desc`(严选指数高→低) | 无（默认排序） |
| `--score-level` | - | 相关性档位：`high`(高)、`medium`(中)、`low`(低) | `high` |
| `--purchase-amount` | - | 采购件数（正整数，不支持范围） | `1` |
| `--tags` | - | TC标（品池标签），英文逗号分隔 | `4306497` |
| `--ic-tags` | - | IC标（品池标签），英文逗号分隔 | 无 |

### 使用示例
```bash
# 基本用法
python3 {baseDir}/cli.py text_search -q "黑色连帽卫衣"

# 指定返回数量
python3 {baseDir}/cli.py text_search -q "手机壳" -l 10

# 按价格从低到高排序
python3 {baseDir}/cli.py text_search -q "男士牛仔裤" -s price_asc

# 按销量从高到低排序
python3 {baseDir}/cli.py text_search -q "冲锋衣" -s sold_desc

# 降低相关性要求，召回更多商品
python3 {baseDir}/cli.py text_search -q "卫衣" --score-level medium

# 指定采购件数
python3 {baseDir}/cli.py text_search -q "手机壳" --purchase-amount 100

# 指定品池标签
python3 {baseDir}/cli.py text_search -q "手机壳" --tags "4306497"

# 完整参数
python3 {baseDir}/cli.py text_search -q "男士牛仔裤 修身" -p 1688 -l 5 -s price_asc --score-level high --purchase-amount 50 --tags "4306497"
```

## 输入参数
```json
{
  "query": "string (required) - 搜索关键词",
  "platform": "string (optional) - 目标平台，默认 1688",
  "limit": "int (optional) - 返回数量，默认 10",
  "sort_type": "string (optional) - 排序方式（price_asc/price_desc/sold_desc/yx_desc）",
  "score_level": "string (optional) - 相关性档位（high/medium/low），默认 high",
  "purchase_amount": "int (optional) - 采购件数，默认 1",
  "tags": "string (optional) - TC标（品池标签），英文逗号分隔，默认 4306497",
  "ic_tags": "string (optional) - IC标（品池标签），英文逗号分隔"
}
```

## 处理流程
### 1. 查询处理
直接使用用户输入的关键词作为搜索条件。

### 2. API 搜索 (_search_via_api)
**主要流程**:
1. 拼装请求并调用 `/api/find_product/1.0.0` 接口
2. 解析返回的商品数据

**API 请求格式**:
```json
{
  "query": "搜索关键词",
  "pageSize": 10,
  "purchaseAmount": 1,
  "sortType": "price_asc",
  "scoreLevel": "high",
  "tags": "4306497",
  "icTags": "标签值（可选）"
}
```

**API 响应格式**:
```json
{
  "data": [
    {
      "itemId": 984731164094,
      "title": "按摩垫按摩靠垫电动热敷按摩仪长导轨家用按摩仪揉捨腰部按摩器",
      "imageUrl": "https://img.alicdn.com/imgextra/O1CN018RgEjT1KiHAGIt18W_!!2212920081197-0-cib.jpg",
      "detailUrl": "https://detail.1688.com/offer/984731164094.html",
      "score": "0.97332934",
      "currentPrice": 45.5,
      "skuId": 6052056270674,
      "skuTitle": "黑色 XL",
      "yxIndex": 4.9,
      "quantityBegin": 2,
      "unit": "件",
      "company": "广州某服饰有限公司",
      "soldOut": 50000,
      "storeAmount": 12000,
      "userId": "",
      "memberId": "",
      "cateId": 122698013,
      "industryName": "消费品",
      "source": "1688",
      "recallSource": "same_product_recall",
      "promotionTags": ["满99减5"],
      "serviceInfos": [{"type": "发货保障", "value": "48小时发货"}],
      "sellingPoints": [{"type": "industryCPV", "value": "加绒"}],
      "offerTags": "180739;3056835;...",
      "offerICTagInfo": {},
      "class": "com.alibaba.china.shared.tagspider.client.Model.aifindproduct.AiFindProductItem"
    }
  ],
  "__msgCode__": "OK",
  "__success__": true,
  "count": 1,
  "intent": {
    "intentType": "IMAGE_SEARCH",
    "imageUrl": "https://img.alicdn.com/imgextra/O1CN01Mx7Qyb24jADQmO25X_!!2217083847426-0-cib.jpg",
    "findSame": true,
    "class": "com.alibaba.china.shared.tagspider.client.Model.aifindproduct.AiFindProductIntent"
  }
}
```

## 输出格式
```json
{
  "success": true,
  "query": "黑色连帽卫衣",
  "similar_products": [
    {
      "product_id": "987622522091",
      "title": "2024新款黑色连帽卫衣男宽松加绒加厚秋冬季外套",
      "image_url": "https://img.alicdn.com/...",
      "detail_url": "https://detail.1688.com/offer/987622522091.html",
      "similarity_score": 0.95,
      "price": 45.5,
      "sku_id": "6052056270674",
      "sku_title": "黑色 XL",
      "yx_index": 4.9,
      "quantity_begin": 2,
      "unit": "件",
      "supplier": "广州某服饰有限公司",
      "sold_count": 50000,
      "stock_amount": 12000,
      "user_id": "",
      "member_id": "",
      "category_id": 201382421,
      "promotion_tags": ["满99减5"],
      "service_infos": [{"type": "发货保障", "value": "48小时发货"}],
      "selling_points": [{"type": "industryCPV", "value": "加绒"}]
    }
  ],
  "search_type": "text_search",
  "total_results": 6
}
```

## 代码结构
```
scripts/capabilities/text_search/
├── __init__.py      # 模块初始化
├── cmd.py           # CLI 入口
└── service.py       # 核心服务实现
    ├── TextSearchExecutor   # 搜索执行器
    └── text_search()        # 主入口函数
```

## 错误处理
- **AK 未配置**: 提示用户运行 `cli.py configure YOUR_AK`
- **API 格式异常**: 抛出 `ServiceError("格式异常，请稍后重试")`
- **无搜索结果**: 返回空数组

## 测试用例
```python
# 基础搜索
text_search(query="黑色连帽卫衣")

# 多关键词搜索
text_search(query="黑色连帽卫衣 宽松 加绒")

# 限定数量
text_search(query="手机壳", limit=10)
```

## 依赖关系
- `_http.search_products`: 商品搜索公共接口
- `_auth.get_ak_from_env`: AK 认证（cmd.py 层调用）
- `_errors.ServiceError`: 错误处理
- `_output.print_output/print_error/format_products_table`: 输出格式化

## 与其他能力的关系
- **共用 API**: 与 `image_search`、`link_search` 使用同一 API path (`/api/find_product/1.0.0`)
- **区别**: text_search 通过 `query` 参数传递搜索词，而非图片

# 注意事项
1. 搜索关键词应尽量准确，避免过于宽泛
2. 返回的商品数据结构与 image_search 一致
3. **--query 必须完整保留用户意图**：禁止丢弃用户提及的排序要求（如"按销量倒排"）、价格筛选（如"100元以下"）、品牌限定等信息，这些要素必须一并携带到 query 参数中

### --query 构造示例

| 用户输入 | ✅ 正确的 --query | ❌ 错误的 --query |
|---------|------------------|------------------|
| 帮我找一件深绿色的始祖鸟同款冲锋衣，按销量倒排 | "深绿色 始祖鸟同款 冲锋衣 销量排序" | "深绿色冲锋衣 始祖鸟同款"|
| 找价格100元以下的男士牛仔裤 | "男士牛仔裤 价格100元以下" | "男士牛仔裤" |
