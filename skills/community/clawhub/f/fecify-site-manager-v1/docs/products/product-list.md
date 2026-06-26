# 商品列表

`GET /api/skill/product/list`

## 请求参数（Query String）

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `pageNum` | int | 选填 | 页码，不填默认第 1 页 |
| `pageSize` | int | 选填 | 每页数据个数，不填使用系统默认值 |
| `title` | string | 选填 | 按商品标题模糊搜索（LIKE） |
| `status` | int | 选填 | `1` 上架 / `2` 下架 |
| `collection_ids` | string | 选填 | 专辑 ID 过滤，逗号分隔（如 `"343,32"`）。**或**关系：只要商品属于其中任意一个专辑就会被搜出 |
| `tags` | string | 选填 | Tag 过滤，逗号分隔（如 `"red,black"`） |
| `tags_type` | string | 选填 | Tag 搜索逻辑关系。`or`（默认，或关系）/ `and`（并关系） |

## 调用

```
node scripts/proxy/api-call.js GET /api/skill/product/list '{"pageNum":1,"pageSize":20,"title":"lamp","status":1,"collection_ids":"343,32","tags":"red,black","tags_type":"and"}'
```

> `api-call.js` 自动将 JSON body 转为 query string。

## 响应示例

```json
{
    "code": 200,
    "message": "success",
    "data": {
        "list": [
            {
                "id": 4625,
                "handle": "morden-lighting-nordic-white-black-lamp-shade-floor-lamp",
                "spu": "7218747113643",
                "title": "Nordic White Black Lamp Floor Lamp Wooden Standing",
                "sub_title": "",
                "body_html": "<p>...</p>",
                "meta_title": "Nordic White Black Lamp Floor Lamp Wooden Standing",
                "meta_keywords": "",
                "meta_description": "...",
                "status": 1,
                "availability": 1,
                "type": 2,
                "vendor": "Lighting Made",
                "qty": 198,
                "created_at": "2026-02-08 10:35:42",
                "updated_at": "2026-05-05 11:10:19",
                "inventory_police": 1,
                "inventory_police_type": 1,
                "variant_need_image": 1,
                "variant_need_note": 1,
                "variants": [
                    {
                        "id": 42432,
                        "product_id": 4625,
                        "title": "White",
                        "price": "470.00",
                        "compare_at_price": "500.00",
                        "cost_price": "0.00",
                        "wholesale_price": [
                            { "qty": 2, "price": "38.99" },
                            { "qty": 5, "price": "18.99" }
                        ],
                        "sku": "LM4540066",
                        "gram": 2267,
                        "position": 0,
                        "barcode": "",
                        "image_id": 30233,
                        "qty": 98,
                        "option1": "White",
                        "option2": "",
                        "option3": "",
                        "weight": "5.00",
                        "weight_unit": "lb",
                        "sale_count": 0,
                        "note": "",
                        "remote_id": 0,
                        "source_id": "",
                        "image": "https://cdn12.fecmall.com/product/15/image/2026/02/08/1e0c57ae.jpg"
                    }
                ],
                "options": [
                    {
                        "id": 5135,
                        "product_id": 4625,
                        "name": "Lampshade Color",
                        "position": 1,
                        "items": ["White", "Black"]
                    }
                ],
                "images": [
                    {
                        "id": 30232,
                        "product_id": 4625,
                        "position": 1,
                        "src": "https://cdn12.fecmall.com/product/15/image/2026/02/08/90667114.jpg",
                        "alt": "",
                        "width": 800,
                        "height": 800,
                        "ratio": "1.00"
                    }
                ],
                "collectionIds": [343, 327, 322, 344, 345],
                "tagIds": [
                    {
                        "product_id": 4625,
                        "tag_id": 10,
                        "tag": { "title": "red", "id": 10, "first_letter": "r" }
                    }
                ]
            }
        ],
        "total": 1,
        "pageSize": 20,
        "totalPage": 1
    }
}
```

## 返回字段

### data 顶层

| 字段 | 类型 | 说明 |
|------|------|------|
| `total` | int | 列表总数 |
| `pageSize` | int | 每页个数 |
| `totalPage` | int | 总页数 |
| `list` | Array | 商品列表 |

### list[] — 基本信息

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | int | 产品 ID |
| `spu` | string | SPU 编码 |
| `title` | string | 产品标题 |
| `sub_title` | string | 副标题 |
| `body_html` | string | 描述（HTML） |
| `handle` | string | 商品 URL handle |
| `meta_title` | string | SEO 标题 |
| `meta_keywords` | string | SEO 关键字 |
| `meta_description` | string | SEO 描述 |

### list[] — 状态/配置

| 字段 | 类型 | 说明 |
|------|------|------|
| `status` | int | `1` 上架 / `2` 下架，默认上架 |
| `type` | int | `1` 单规格 / `2` 多规格 |
| `availability` | int | `1` 可售 / `2` 不可用 |
| `qty` | int | 总库存 |
| `vendor` | string | 厂家/品牌名称 |
| `virtual_sales_count` | int | 虚拟销量 |
| `variant_need_image` | int | 规格是否需要图片：`1` 需要 / `2` 不需要，默认 `1` |
| `variant_need_note` | int | 变体是否需要备注：`1` 需要 / `2` 不需要 |
| `inventory_police` | int | 是否跟踪库存：`1` 跟踪 / `2` 不跟踪，默认 `1` |
| `inventory_police_type` | int | 库存策略：`1` 为 0 允许购买 / `2` 为 0 不允许购买 / `3` 为 0 自动下架，默认 `1` |
| `created_at` | string | 创建时间 |
| `updated_at` | string | 更新时间 |

### list[].variants[] — 变体/规格

> 单规格产品该数组只有一个子项。

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | int | 变体 ID |
| `product_id` | int | 产品 ID |
| `title` | string | 规格名称 |
| `price` | float | 售卖价格 |
| `compare_at_price` | float | 划线价格 |
| `cost_price` | float | 成本价格 |
| `wholesale_price` | Array | 批发价数组，每项 `{ qty: int, price: string }`，`qty` 为起批数量，`price` 为批发单价 |
| `sku` | string | 产品 SKU |
| `gram` | int | 重量（克） |
| `weight` | float | 重量 |
| `weight_unit` | string | `g` / `kg` / `lb` / `oz` |
| `barcode` | string | 条形码 |
| `qty` | int | 变体库存 |
| `image_id` | int | 图片 ID |
| `image` | string | 变体图片路径 |
| `option1/2/3` | string | 规格值 |
| `position` | int | 排序位置 |
| `note` | string | 变体备注 |
| `sale_count` | int | 销量 |
| `remote_id` | int | 远程 ID，用于与三方系统（如 ERP）同步商品数据 |
| `source_id` | string | 来源 ID |

### list[].options[] — 规格定义

> 单规格产品为空，多规格产品不为空。

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | int | Option ID |
| `product_id` | int | 产品 ID |
| `name` | string | 规格名称（如 "Color"、"Size"） |
| `position` | int | 规格排序 |
| `items` | string[] | 规格子项（如 `["White","Black"]`） |

### list[].images[] — 产品图片

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | int | 图片 ID |
| `product_id` | int | 产品 ID |
| `src` | string | 图片 URL 路径 |
| `alt` | string | alt 文本 |
| `position` | int | 排序，从 `1` 递增，`1` 为主图 |
| `width` | int | 宽度（像素） |
| `height` | int | 高度（像素） |
| `ratio` | string | 宽高比 |

### list[].collectionIds

| 字段 | 类型 | 说明 |
|------|------|------|
| `collectionIds` | int[] | 所属专辑 ID 数组（多对多） |

### list[].tagIds[]

| 字段 | 类型 | 说明 |
|------|------|------|
| `product_id` | int | 产品 ID |
| `tag_id` | int | Tag ID |
| `tag.id` | int | Tag 的 ID |
| `tag.title` | string | Tag 标题 |
| `tag.first_letter` | string | Tag 首字母 |

## 注意事项

1. `pageNum`、`pageSize`、`title`、`status`、`collection_ids`、`tags`、`tags_type` 均为选填参数
2. `collection_ids` 多个值时是**或**关系，会搜索出存在于这些专辑中的全部商品
3. `tags` 配合 `tags_type` 使用：`tags_type=or`（默认）为或关系，`tags_type=and` 为并关系
4. `wholesale_price` 为变体的批发价格数组，每个元素包含 `qty`（起批数量）和 `price`（批发单价）
5. `weight_unit` 支持 `g`、`kg`、`lb`、`oz` 四种单位
6. `remote_id` 用于与三方系统（如 ERP）同步商品数据时，记录三方系统的商品 ID
