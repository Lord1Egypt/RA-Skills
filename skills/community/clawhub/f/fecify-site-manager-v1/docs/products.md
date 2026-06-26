# 商品管理

## API 一览

| 操作 | 路径 | 方法 | 详细文档 |
|------|------|------|----------|
| 商品列表 | `/api/skill/product/list` | GET | [product-list.md](products/product-list.md) |
| 商品详情 | `/api/skill/product/info` | GET | [product-info.md](products/product-info.md) |
| 创建商品 | `/api/skill/product/create` | POST | [product-create.md](products/product-create.md) |
| 更新商品 | `/api/skill/product/update` | POST | [product-update.md](products/product-update.md) |

> **图片相关 API** 为跨模块公用，详见 [base-image.md](base-image.md)。
>
> **创建/更新商品涉及图片时**：必须先调用 [上传图片 API](base-image.md#2-上传图片) 获取 `path`，再将 `path` 填入 `images[].src` 和 `variants[].image`。不可凭空填写图片路径。

---

## 1. 商品列表

`GET /api/skill/product/list` — [详细文档](products/product-list.md)

**何时用**：浏览/搜索商品、获取商品 ID 用于后续操作。

查询参数（全部选填）：`pageNum` `pageSize` `title` `status` `collection_ids` `tags` `tags_type`

返回分页列表，每个商品含基本信息 + `variants` `options` `images` `collectionIds` `tagIds`。

```
node scripts/proxy/api-call.js GET /api/skill/product/list '{"pageNum":1,"pageSize":20,"title":"lamp","status":1}'
```

---

## 2. 商品详情

`GET /api/skill/product/info` — [详细文档](products/product-info.md)

**何时用**：查看单个商品完整数据、更新前获取现有数据。

参数：`id`（必填）

返回商品全集：`variants`（含 VIP 价格）`options` `images` `videos` `mergeimages` `payafteruse` `glasses_attr` 等。

```
node scripts/proxy/api-call.js GET /api/skill/product/info '{"id":4625}'
```

---

## 3. 创建商品

`POST /api/skill/product/create` — [详细文档](products/product-create.md)

**何时用**：新增商品。

必填：`product.title` `product.body_html` `product.type` `images[]` `variants[]`

多规格还需 `options[]`。新增时不传子实体 `id`。

> **图片流程**：先调用 [上传 API](base-image.md#2-上传图片) 获取 `path` → 填入 `images[].src` 和 `variants[].image`。
> **变体图片约束**：`variants[].image` 路径必须存在于 `images` 数组中，否则保存失败。

返回 `data.product_id`。

```
node scripts/proxy/api-call.js POST /api/skill/product/create '<JSON_BODY>'
```

---

## 4. 更新商品

`POST /api/skill/product/update` — [详细文档](products/product-update.md)

**何时用**：修改已有商品信息。

必填：`product.id`（其他参数结构与 Create 一致）

> **更新原则**：先通过 [详情 API](#2-商品详情) 获取完整数据 → 修改 → 提交完整数组（已有子实体带 `id`，新增不带）。

返回 `data.product_id`。

```
node scripts/proxy/api-call.js POST /api/skill/product/update '<JSON_BODY>'
```


