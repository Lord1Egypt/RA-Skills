# Capability: image_search (图片找同款)

## 功能说明
基于用户上传的商品图片，通过图像识别和特征匹配，在 1688 平台搜索同款或相似商品。支持本地图片路径和图片 URL。

## 触发方式
**Skill 级触发词**: 图片找货、找同款、搜相似

**Capability 识别特征**:
- 用户输入包含图片附件
- 或消息中包含图片 URL
- 配合文字："找同款"、"有类似的吗"、"搜这个"

## 前置条件
- 已配置 AK。**Agent 判断 AK 是否已配置时，必须通过执行 `cli.py configure`（无参数）确认，禁止仅凭环境变量或对话历史判断**。AK 可能已持久化在本地配置文件中，即使当前对话未提及也可能已配置。

## CLI 调用（Agent 执行时必须使用）
```bash
python3 {baseDir}/cli.py image_search --image "图片路径或URL" [--limit 10] [--sort price_asc] [--score-level high] [--purchase-amount 1] [--tags 4306497] [--ic-tags ""]
```

### 命令行参数
| 参数 | 简写 | 说明 | 默认值 |
|------|------|------|--------|
| `--image` | `-i` | 图片本地路径或 URL | 必需 |
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
python3 {baseDir}/cli.py image_search -i /path/to/image.jpg

# 指定返回数量
python3 {baseDir}/cli.py image_search -i /path/to/image.jpg -l 10

# 按价格从低到高排序
python3 {baseDir}/cli.py image_search -i /path/to/image.jpg -s price_asc

# 按销量从高到低排序
python3 {baseDir}/cli.py image_search -i /path/to/image.jpg -s sold_desc

# 降低相关性要求，召回更多商品
python3 {baseDir}/cli.py image_search -i /path/to/image.jpg --score-level medium

# 指定采购件数
python3 {baseDir}/cli.py image_search -i /path/to/image.jpg --purchase-amount 100

# 指定品池标签
python3 {baseDir}/cli.py image_search -i /path/to/image.jpg --tags "4306497"

# 完整参数
python3 {baseDir}/cli.py image_search -i /path/to/image.jpg -p 1688 -l 5 -s price_asc --score-level high --purchase-amount 50 --tags "4306497"
```

## 输入参数
```json
{
  "image_path": "string (required) - 本地图片路径或 URL",
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
### 1. 图片预处理 (ImagePreprocessor)
```python
步骤：
1. 判断输入类型（本地路径 / URL）
2. 本地图片：检查文件存在性和大小
3. 返回处理后的图片信息
```

### 2. API 搜索 (_search_via_api)
**主要流程**:
1. 将图片通过 base64 编码转换成字符串
2. 拼装请求并调用 `/api/find_product/1.0.0` 接口
3. 解析返回的商品数据

**API 请求格式**:
```json
{
  "imgBase64": "base64编码的图片字符串",
  "imageUrl": "图片URL（可选）",
  "pageSize": 10,
  "purchaseAmount": 1,
  "sortType": "price_asc",
  "scoreLevel": "high",
  "tags": "4306497",
  "icTags": "标签值（可选）"
}
```
> `sortType` 和 `scoreLevel` 为可选字段，不传则使用默认值。

**API 响应格式**:
```json
{
  "data": {
    "data": [
      {
        "itemId": 987622522091,
        "title": "商品标题",
        "imageUrl": "商品主图URL",
        "detailUrl": "商品详情页URL",
        "score": 0.99786893,
        "currentPrice": 12.8,
        "skuId": 6052056270674,
        "skuTitle": "五彩公鸡",
        "yxIndex": 4.5,
        "quantityBegin": 1,
        "unit": "",
        "company": "义乌某工艺品有限公司",
        "soldOut": 20000,
        "storeAmount": 5000,
        "userId": "",
        "memberId": "",
        "cateId": 201382421,
        "industryName": "消费品",
        "source": "1688",
        "recallSource": "same_product_recall",
        "promotionTags": [],
        "serviceInfos": [{"type": "赊账服务", "value": "先采后付"}],
        "sellingPoints": [{"type": "industryCPV", "value": "亚克力"}],
        "offerTags": "180739;3056835;...",
        "offerICTagInfo": {},
        "class": "com.alibaba.china.shared.tagspider.client.Model.aifindproduct.AiFindProductItem"
      }
    ],
    "count": 3
  }
}
```

### 3. 错误处理（无浏览器降级）
**本能力不存在浏览器降级方案。** 当 API 不可用或 AK 未配置时，直接返回错误信息，由 Agent 引导用户解决（配置 AK、检查路径等），禁止尝试通过浏览器访问 1688 网站。

## 输出格式
```json
{
  "success": true,
  "source_image": "/path/to/uploaded.jpg",
  "similar_products": [
    {
      "product_id": "987622522091",
      "title": "跨境创意五彩公鸡动物摆件2D平面亚克力家居办公桌面装饰摆件",
      "image_url": "https://img.alicdn.com/...",
      "detail_url": "https://detail.1688.com/offer/987622522091.html",
      "similarity_score": 0.9979,
      "price": 12.8,
      "sku_id": "6052056270674",
      "sku_title": "五彩公鸡",
      "yx_index": 4.5,
      "quantity_begin": 1,
      "unit": "",
      "supplier": "义乌某工艺品有限公司",
      "sold_count": 20000,
      "stock_amount": 5000,
      "user_id": "",
      "member_id": "",
      "category_id": 201382421,
      "promotion_tags": [],
      "service_infos": [{"type": "赊账服务", "value": "先采后付"}],
      "selling_points": [{"type": "industryCPV", "value": "亚克力"}]
    }
  ],
  "search_type": "image_similarity",
  "total_results": 3
}
```

## 代码结构
```
scripts/capabilities/image_search/
├── __init__.py      # 模块初始化
├── cmd.py           # CLI 入口
└── service.py       # 核心服务实现
    ├── ImagePreprocessor    # 图片预处理器
    ├── ImageSearchExecutor  # 搜索执行器
    └── image_search()       # 主入口函数
```

## 错误处理
- **图片路径无效**: 抛出 `ServiceError("图片路径无效")`
- **图片不存在**: 抛出 `FileNotFoundError`
- **图片太大**: 抛出 `ValueError`（超过 5MB）
- **API 格式异常**: 抛出 `ServiceError("格式异常，请稍后重试")`
- **AK 未配置**: 提示用户运行 `cli.py configure YOUR_AK`

## 测试用例
```python
# 本地图片路径
image_search(image_path="/workspace/product.jpg")

# 图片 URL
image_search(image_path="https://example.com/product.png")

# 指定返回数量
image_search(image_path="xxx.jpg", limit=10)

# 指定采购件数
image_search(image_path="xxx.jpg", purchase_amount=100)

# 指定排序和相关性
image_search(image_path="xxx.jpg", sort_type="price_asc", score_level="medium")
```

## 依赖关系
- `_http.search_products`: 商品搜索公共接口
- `_auth.get_ak_from_env`: AK 认证（cmd.py 层调用）
- `_errors.ServiceError`: 错误处理
- `_output.print_output/print_error/format_products_table`: 输出格式化

## 注意事项
1. 图片上传需考虑隐私和安全，临时文件会自动清理
2. API 调用需要有效的 AK 配置
3. **不存在浏览器降级方案**，AK 缺失或 API 失败时只能返回错误提示，不得尝试浏览器搜索
4. Windows 环境下临时文件可能受沙箱限制，代码已内置 fallback 到工作目录
5. **本地图片必须使用绝对路径**（如 `/home/user/image.png` 或 `C:\Users\user\image.png`），禁止使用相对路径（如 `./image.png`），否则在不同操作系统下可能因工作目录不一致导致找不到文件
6. **图片预处理限制**：本地图片最大支持 5MB；超过 800×800 像素的图片会自动等比缩放；非 JPEG 格式会自动转换为 JPEG（透明通道处理为白色底）