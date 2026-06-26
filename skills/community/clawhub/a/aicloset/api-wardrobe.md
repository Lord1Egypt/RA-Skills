# 衣橱与单品管理 API

## POST /skill/wardrobe/list

查询用户衣橱列表，支持分页。

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| page | int | 否 | 页码，默认 1 |
| page_size | int | 否 | 每页数量，默认 10 |

### 请求示例

```bash
curl -X POST https://aicloset-dev.wxbjq.top/skill/wardrobe/list \
  -H "x-api-key: $AICLOSET_API_KEY" \
  -d "page=1&page_size=10"
```

### 响应示例

```json
{
  "code": 0,
  "msg": "ok",
  "data": {
    "list": [
      {
        "id": 1,
        "name": "我的衣橱",
        "cover_image": "https://...",
        "total": 5
      }
    ],
    "total": 10,
    "page": 1
  }
}
```

---

## POST /skill/wardrobe/create

创建新衣橱。衣橱名称在同一用户下不可重复。

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| name | string | 是 | 衣橱名称（用户内唯一） |
| cover_image | string | 否 | 封面图 URL |
| remark | string | 否 | 备注 |

### 请求示例

```bash
curl -X POST https://aicloset-dev.wxbjq.top/skill/wardrobe/create \
  -H "x-api-key: $AICLOSET_API_KEY" \
  -d "name=春季衣橱"
```

### 响应示例

```json
{
  "code": 0,
  "msg": "ok",
  "data": {
    "id": 1,
    "name": "春季衣橱",
    "cover_image": "https://..."
  }
}
```

### 错误响应

名称重复时返回：

```json
{"code": 43600, "msg": "衣橱名不可以重复", "data": null}
```

---

## POST /skill/product/add

录入单品。上传服饰图片后，系统异步执行 AI 识别（分类、抠图等）。

支持两种方式提供图片（二选一）：
- **文件上传**：通过 `multipart/form-data` 上传 `image` 字段（推荐）
- **URL**：通过 `image_url` 参数传入已有图片 URL

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| image | file | 二选一 | 单品图片文件（png/jpg/jpeg，≤20MB） |
| image_url | string | 二选一 | 单品图片 URL |
| wardrobe_id | int64 | 否 | 关联衣橱 ID |

### 请求示例（文件上传）

```bash
curl -X POST https://aicloset-dev.wxbjq.top/skill/product/add \
  -H "x-api-key: $AICLOSET_API_KEY" \
  -F "image=@shirt.jpg" \
  -F "wardrobe_id=1"
```

### 请求示例（URL）

```bash
curl -X POST https://aicloset-dev.wxbjq.top/skill/product/add \
  -H "x-api-key: $AICLOSET_API_KEY" \
  -d "image_url=https://example.com/shirt.jpg&wardrobe_id=1"
```

### 响应示例

```json
{
  "code": 0,
  "msg": "ok",
  "data": {
    "user_product_id": 100,
    "status": "processing"
  }
}
```

> `status: "processing"` 表示 AI 识别正在异步进行中。

---

## POST /skill/product/edit

编辑单品信息。

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| product_id | int64 | 是 | 单品 ID |
| name | string | 是 | 单品名称 |

### 请求示例

```bash
curl -X POST https://aicloset-dev.wxbjq.top/skill/product/edit \
  -H "x-api-key: $AICLOSET_API_KEY" \
  -d "product_id=100&name=白色T恤"
```

### 响应示例

```json
{
  "code": 0,
  "msg": "ok",
  "data": {
    "product_id": 100,
    "updated": {
      "name": "白色T恤"
    }
  }
}
```
