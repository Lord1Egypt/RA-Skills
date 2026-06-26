# Capability: link_search (链接找同款)

## 功能说明
解析用户提供的商品链接或商品 ID，自动识别平台，尝试静默获取商品主图，然后基于主图搜索同款或相似商品。与 image_search 和 text_search 共用同一 API 接口。

## 触发方式
**Skill 级触发词**: 链接找货、找同款、搜相似

**Capability 识别特征**:
- 用户输入包含完整 URL (1688/淘宝/天猫)
- 或纯商品 ID (6-12 位数字/字母组合)
- 配合文字："找同款"、"有类似的吗"、"这个的平价替代"

## 前置条件
- 已配置 AK。**Agent 判断 AK 是否已配置时，必须通过执行 `cli.py configure`（无参数）确认，禁止仅凭环境变量或对话历史判断**。AK 可能已持久化在本地配置文件中，即使当前对话未提及也可能已配置。

## CLI 调用（Agent 执行时必须使用）
```bash
python3 {baseDir}/cli.py link_search --url "商品链接" [--image "图片URL"] [--limit 10] [--sort price_asc] [--score-level high] [--purchase-amount 1] [--tags 4306497] [--ic-tags ""]
```

### 命令行参数
| 参数 | 简写 | 说明 | 默认值 |
|------|------|------|--------|
| `--url` | `-u` | 商品链接或商品 ID | 必需 |
| `--image` | `-i` | 商品图片 URL（自动获取失败时使用） | 可选 |
| `--platform` | `-p` | 目标平台 | 1688 |
| `--limit` | `-l` | 返回数量 | 10 |
| `--sort` | `-s` | 排序方式：`price_asc`(价格低→高)、`price_desc`(价格高→低)、`sold_desc`(销量高→低)、`yx_desc`(严选指数高→低) | 无（默认排序） |
| `--score-level` | - | 相关性档位：`high`(高)、`medium`(中)、`low`(低) | `high` |
| `--purchase-amount` | - | 采购件数（正整数，不支持范围） | `1` |
| `--tags` | - | TC标（品池标签），英文逗号分隔 | `4306497` |
| `--ic-tags` | - | IC标（品池标签），英文逗号分隔 | 无 |

### 使用示例
```bash
# 基本用法（自动获取主图）
python3 {baseDir}/cli.py link_search -u "https://detail.1688.com/offer/895657286458.html"

# 纯商品 ID
python3 {baseDir}/cli.py link_search -u "895657286458"

# 手动指定商品图片（当自动获取失败时）
python3 {baseDir}/cli.py link_search -u "https://detail.1688.com/offer/895657286458.html" -i "https://img.alicdn.com/xxx.jpg"

# 指定返回数量
python3 {baseDir}/cli.py link_search -u "895657286458" -l 10

# 按价格从低到高排序
python3 {baseDir}/cli.py link_search -u "895657286458" -s price_asc

# 按销量从高到低排序
python3 {baseDir}/cli.py link_search -u "895657286458" -s sold_desc

# 降低相关性要求，召回更多商品
python3 {baseDir}/cli.py link_search -u "895657286458" --score-level medium

# 指定采购件数
python3 {baseDir}/cli.py link_search -u "895657286458" --purchase-amount 100

# 指定品池标签
python3 {baseDir}/cli.py link_search -u "895657286458" --tags "4306497"

# 完整参数
python3 {baseDir}/cli.py link_search -u "895657286458" -l 5 -s price_asc --score-level high --purchase-amount 50 --tags "4306497"
```

## 输入参数
```json
{
  "url": "string (required) - 商品链接或商品 ID",
  "image_url": "string (optional) - 商品图片 URL（自动获取失败时使用）",
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

### 1. 链接解析 (LinkParser)
```python
输入示例：
- "https://detail.1688.com/offer/895657286458.html"
- "https://item.taobao.com/item.htm?id=1033765771797"
- "895657286458" (纯 ID)

输出：
{
  "platform": "1688",
  "product_id": "895657286458",
  "canonical_url": "https://detail.1688.com/offer/895657286458.html"
}
```

**识别规则**:
- **1688**: URL 包含 `1688.com` 且路径含 `offer`，ID 格式：6-12 位纯数字
- **淘宝**: URL 包含 `taobao.com` 或 `tb.cn`，ID 格式：8-12 位字母数字
- **天猫**: URL 包含 `tmall.com`，ID 格式同淘宝

### 2. 商品主图提取 (ProductImageExtractor)
**尝试静默获取商品主图**:
1. 发起 HTTP 请求获取商品页面 HTML
2. 根据以下特征判断商品主图：
   - 图片 URL 符合阿里图片服务模式（alicdn.com）
   - 包含 `ibank` 或 `imgextra` 标识
   - 过滤掉缩略图（如 `_50x50`、`_100x100`）
3. 返回第一个符合条件的图片 URL

**如果无法获取主图**:
- 返回 `action: "need_image_url"` 信号
- 提示用户手动输入商品图片 URL
- 转到 image_search 流程完成功能

### 3. API 搜索 (_search_via_api)
**主要流程**:
1. 拼装请求并调用 `/api/find_product/1.0.0` 接口
2. 解析返回的商品数据

**API 请求格式**:
```json
{
  "imageUrl": "商品主图URL",
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

### 成功获取主图时
```json
{
  "success": true,
  "source_url": "https://detail.1688.com/offer/895657286458.html",
  "source_image": "https://img.alicdn.com/xxx.jpg",
  "similar_products": [
    {
      "product_id": "987622522091",
      "title": "同款商品标题",
      "image_url": "https://img.alicdn.com/...",
      "detail_url": "https://detail.1688.com/offer/987622522091.html",
      "similarity_score": 0.9979,
      "price": 25.0,
      "sku_id": "6052056270674",
      "sku_title": "黑色 M",
      "yx_index": 4.8,
      "quantity_begin": 1,
      "unit": "",
      "supplier": "某服饰有限公司",
      "sold_count": 30000,
      "stock_amount": 8000,
      "user_id": "",
      "member_id": "",
      "category_id": 201382421,
      "promotion_tags": [],
      "service_infos": [{"type": "发货保障", "value": "48小时发货"}],
      "selling_points": [{"type": "industryCPV", "value": "棉"}]
    }
  ],
  "search_type": "link_search",
  "total_results": 6
}
```

### 无法获取主图时
```json
{
  "success": false,
  "source_url": "https://detail.1688.com/offer/895657286458.html",
  "action": "need_image_url",
  "message": "无法自动获取商品主图，请手动输入商品图片 URL",
  "similar_products": [],
  "search_type": "link_search",
  "total_results": 0
}
```

## 代码结构
```
scripts/capabilities/link_search/
├── __init__.py      # 模块初始化
├── cmd.py           # CLI 入口
└── service.py       # 核心服务实现
    ├── LinkParser            # 链接解析器
    ├── ProductImageExtractor # 商品主图提取器
    ├── LinkSearchExecutor    # 搜索执行器
    ├── link_search()         # 主入口函数
    └── link_search_with_image()  # 使用指定图片搜索
```

## 错误处理
- **链接格式错误**: 抛出 `ValueError("无法识别的商品 ID 格式")`
- **不支持的平台**: 抛出 `ValueError("不支持的电商平台")`
- **无法获取主图**: 返回 `action: "need_image_url"` 信号
- **AK 未配置**: 提示用户运行 `cli.py configure YOUR_AK`
- **API 格式异常**: 抛出 `ServiceError("格式异常，请稍后重试")`

## 测试用例
```python
# 1688 链接
link_search(url="https://detail.1688.com/offer/895657286458.html")

# 淘宝链接
link_search(url="https://item.taobao.com/item.htm?id=1033765771797")

# 纯商品 ID
link_search(url="895657286458")

# 手动指定图片 URL
link_search_with_image(image_url="https://img.alicdn.com/xxx.jpg", limit=10)
```

## 依赖关系
- `_http.search_products`: 商品搜索公共接口
- `_auth.get_ak_from_env`: AK 认证（cmd.py 层调用）
- `_errors.ServiceError`: 错误处理
- `_output.print_output/print_error/format_products_table`: 输出格式化
- `urllib.request`: 用于获取商品页面 HTML

## 与其他能力的关系
- **共用 API**: 与 `image_search`、`text_search` 使用同一 API path (`/api/find_product/1.0.0`)
- **降级策略**: 当无法获取主图时，提示用户手动输入图片 URL，转到 `image_search` 流程

## 注意事项
1. 静默获取主图依赖于页面的 HTML 结构，可能因页面变化而失效
2. 部分商品页面可能需要登录才能访问，此时无法获取主图
3. 建议用户直接提供商品图片 URL 以获得更稳定的搜索结果
4. 返回的商品数据结构与 image_search 一致

### 平台自动提取主图支持

| 平台 | 自动提取主图 | 说明 |
|------|-------------|------|
| **1688** | ✅ 支持 | 自动从商品页面提取主图 |
| **淘宝** | ❌ 不支持 | 需要用户手动提供图片 URL |
| **天猫** | ❌ 不支持 | 需要用户手动提供图片 URL |
