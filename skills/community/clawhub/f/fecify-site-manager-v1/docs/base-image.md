# 图片管理（基础）

图片上传和列表是商品、专辑、博客等多个模块的共享基础能力。

## API 一览

| 操作 | 路径 | 方法 | 详细文档 |
|------|------|------|----------|
| 图片列表 | `/api/skill/base-image/get-image-list` | GET | [image-list.md](base-images/image-list.md) |
| 上传图片 | `/api/skill/base-image/upload` | POST | [image-upload.md](base-images/image-upload.md) |

---

## 1. 图片列表

`GET /api/skill/base-image/get-image-list` — [详细文档](base-images/image-list.md)

**何时用**：查找已上传的图片、获取图片 `path` 用于商品/专辑等业务。

查询参数：`pageNum` `pageSize` `group_type` `begin_at` `end_at`（全部选填）

`group_type` 枚举：`product` / `category` / `blog_article` / `editor` / `common`

返回分页列表，每项含 `id` `name` `path` `group_type` `width` `height` `ratio`。同时返回系统配置 `upload_img_max_size` 和 `upload_img_allow_types`。

```
node scripts/proxy/api-call.js GET /api/skill/base-image/get-image-list '{"pageNum":1,"pageSize":10,"group_type":"product"}'
```

---

## 2. 上传图片

`POST /api/skill/base-image/upload` — [详细文档](base-images/image-upload.md)

**何时用**：商品创建/更新前先上传图片获取 `path`；专辑、博客等模块需要上传图片时。

必填：`image_base64encode`（纯 base64，**不带** `data:image/png;base64,` 前缀）、`image_name`（含扩展名如 `test.jpg`）

选填：`group_type`（默认 `product`）

支持的格式：`jpg` `gif` `png` `webp` `avif`

返回的 `data.path` 为核心字段，供后续业务 API 使用。服务端会重命名文件（`data.name` 可能与传参不同）。

```
node scripts/proxy/api-call.js POST /api/skill/base-image/upload '{"image_base64encode":"iVBORw0KGgo...","image_name":"product.jpg"}'
```

---

## 3. 典型工作流

以商品创建为例：

```
# ① 上传图片
node scripts/proxy/api-call.js POST /api/skill/base-image/upload '{"image_base64encode":"...","image_name":"product.jpg"}'
# → data.path = "/product/15/image/2026/05/05/abc123.jpg"

# ② 用 path 创建商品
node scripts/proxy/api-call.js POST /api/skill/product/create '{
  "product": {"title":"新品","body_html":"<p>描述</p>","type":1},
  "images": [{"src":"/product/15/image/2026/05/05/abc123.jpg","position":1}],
  "variants": [{"price":"99.00","qty":100,"weight":"1","weight_unit":"kg"}]
}'
```

---

## 4. 重要约束

1. `image_base64encode` 只传纯 base64 字符串，不要带 data URI 前缀
2. `image_name` 必须包含正确的文件扩展名
3. `group_type` 必须从枚举值中选择
4. 上传成功后服务端会重命名，返回的 `name` 可能与传入不同
5. `begin_at` / `end_at` 配合使用可按创建时间区间过滤
