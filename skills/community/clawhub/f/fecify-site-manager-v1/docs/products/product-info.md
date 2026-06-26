# 商品详情

`GET /api/skill/product/info`

## 请求参数

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `id` | int | ✅ 必填 | 商品 ID |

## 调用

```
node scripts/proxy/api-call.js GET /api/skill/product/info '{"id":4625}'
```

## 响应示例

```json
{
    "code": 200,
    "message": "success",
    "data": {
        "id": 4625,
        "shop_id": 15,
        "spu": "7218747113643",
        "title": "Nordic White Black Lamp Floor Lamp Wooden Standing",
        "sub_title": "",
        "body_html": "...",
        "handle": "morden-lighting-nordic-white-black-lamp-shade-floor-lamp",
        "status": 1,
        "type": 2,
        "availability": 1,
        "qty": 198,
        "price": "470.00",
        "compare_at_price": "500.00",
        "vendor": "Lighting Made",
        "sale_count": 0,
        "final_sale_count": 0,
        "virtual_sales_count": 0,
        "is_tax": 2,
        "variant_need_image": 1,
        "variant_show_image": 3,
        "variant_need_note": 1,
        "inventory_police": 1,
        "inventory_police_type": 1,
        "is_deleted": 2,
        "deleted_at": 0,
        "note": "",
        "meta_is_edit": 1,
        "meta_title": "Nordic White Black Lamp Floor Lamp Wooden Standing",
        "meta_keywords": "",
        "meta_description": "...",
        "feed_title": "",
        "feed_description": null,
        "remote_id": "7218747113643",
        "source_id": "",
        "source_url": "",
        "source_type": 0,
        "translate_type": 3,
        "template_type": "",
        "google_product_category": 0,
        "google_product_type_id": 0,
        "description_json_status": 2,
        "description_json": [],
        "params_json_status": 2,
        "params_json": [],
        "short_description_json": [],
        "created_at": "2026-02-08 10:35:42",
        "updated_at": "2026-05-05 11:10:19",
        "addition_group_id": "",
        "productattr_info": [],
        "variants": [
            {
                "id": 42432,
                "shop_id": 15,
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
                "created_at": "2026-02-08 10:35:42",
                "updated_at": "2026-05-05 11:10:20",
                "remote_id": 0,
                "source_id": "",
                "image": "/product/15/image/2026/02/08/1e0c57ae.jpg",
                "customervip": [
                    { "id": 80, "product_id": 4625, "variant_id": 42432, "customervip_id": 11, "price": "15.00", "compare_at_price": "0.00" }
                ],
                "images": [],
                "buy_min_count": 0
            }
        ],
        "options": [
            {
                "id": 5135,
                "shop_id": 15,
                "product_id": 4625,
                "name": "Lampshade Color",
                "position": 1,
                "items": ["White", "Black"],
                "created_at": "2026-02-08 10:35:42",
                "updated_at": "2026-02-08 10:35:42"
            }
        ],
        "images": [
            {
                "id": 30232,
                "product_id": 4625,
                "position": 1,
                "src": "/product/15/image/2026/02/08/90667114.jpg",
                "alt": "",
                "width": 800,
                "height": 800,
                "ratio": "1.00"
            }
        ],
        "videos": [],
        "collectionIds": [343, 327, 322, 344, 345],
        "tagIds": [
            {
                "product_id": 4625,
                "tag_id": 10,
                "tag": { "title": "red", "id": 10, "first_letter": "r" }
            }
        ],
        "mergeimages": [
            {
                "id": 151,
                "product_id": 4625,
                "position": 1,
                "src": "/product/15/image/2026/05/05/9407d10e.png",
                "width": 533,
                "height": 800,
                "ratio": "0.67",
                "alt": ""
            }
        ],
        "payafteruse": { "id": 9, "product_id": 4625, "type": 2 },
        "glasses_attr": { "id": 446, "shop_id": 15, "product_id": 4625 }
    }
}
```

## 返回字段

返回商品完整信息，包含所有关联数据。除[商品列表](product-list.md)已有字段外，info 额外返回以下字段：

### data 顶层扩展字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `shop_id` | int | 店铺 ID |
| `price` | string | 产品价格，多变体时取最低变体价格 |
| `compare_at_price` | string | 产品划线价，和 `price` 取自同一变体 |
| `sale_count` | int | 实际销售个数 |
| `final_sale_count` | int | 最终销售个数 = `virtual_sales_count + sale_count` |
| `is_tax` | int | 是否收税：`1` 收税 / `2` 不收税 |
| `variant_show_image` | int | 前台规格显示方式：`1` 显示文字 / `2` 显示图片 / `3` 使用插件默认配置 |
| `is_deleted` | int | 软删除标记：`1` 已删除 / `2` 未删除 |
| `deleted_at` | int | 软删除日期时间（时间戳），`0` 表示未删除 |
| `note` | string | 商品备注 |
| `meta_is_edit` | int | SEO 信息是否独立编辑：`1` 非独立编辑 / `2` 独立编辑 |
| `feed_title` | string | Feed 标题 |
| `feed_description` | string/null | Feed 描述 |
| `remote_id` | string | 远程 ID，用于与三方系统同步商品数据 |
| `source_id` | string | 来源 ID |
| `source_url` | string | 来源 URL |
| `source_type` | int | source 类型：`1` 代表 1688 |
| `translate_type` | int | 翻译类型：`1` 强制翻译 / `2` 只翻译多语言为空部分 / `3` 不翻译 |
| `template_type` | string | 模版装修的 template key |
| `google_product_category` | int | Google 商品分类 ID |
| `google_product_type_id` | int | Google 商品类型 ID |
| `description_json_status` | int | 描述是否使用 JSON 字段：`1` 开启 / `2` 关闭 |
| `description_json` | Array | 描述 JSON 数据 |
| `params_json_status` | int | 参数是否使用 JSON：`1` 开启 / `2` 关闭 |
| `params_json` | Array | 参数 JSON 数据 |
| `short_description_json` | Array | 商品简短描述（JSON 格式数组，支持多语言） |
| `addition_group_id` | string | 附加分组 ID |
| `productattr_info` | Array | 产品属性信息 |

### data.variants[] 扩展字段

> 比列表接口的 variants 多以下字段：

| 字段 | 类型 | 说明 |
|------|------|------|
| `shop_id` | int | 店铺 ID |
| `cost_price` | float | 成本价格 |
| `wholesale_price` | Array | 批发价格，每项 `{ qty: int, price: string }` |
| `customervip` | Array | VIP 会员价格，每项 `{ id, product_id, variant_id, customervip_id, price, compare_at_price }`。只在站点启用了 VIP 会员功能时返回有效数据 |
| `images` | Array | 变体图片列表 |
| `buy_min_count` | int | 最小起购数量 |
| `created_at` | string | 创建时间 |
| `updated_at` | string | 更新时间 |

### data.options[] 扩展字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `shop_id` | int | 店铺 ID |
| `created_at` | string | 创建时间 |
| `updated_at` | string | 更新时间 |

### data 额外关联

| 字段 | 类型 | 说明 |
|------|------|------|
| `videos` | Array | 产品视频列表 |
| `mergeimages` | Array | 合并图片列表，每项 `{ id, product_id, position, src, alt, width, height, ratio }` |
| `payafteruse` | Object | 先用后付：`{ id, product_id, type }`，`type=1` 先用后付商品 / `type=2` 普通商品 |
| `glasses_attr` | Object | 眼镜类商品专有属性（普通商品返回空数据）。包含 `id` `shop_id` `product_id` `size_lens` `size_inside` `size_length` `button_type` `distance_min` `distance_max` `sex` `lens_type` `material` `created_at` `updated_at` |

## 注意事项

1. `id` 为必填参数，不传或传无效 ID 将返回错误
2. 该接口返回商品的完整信息，包含变体、规格、图片、专辑、标签、VIP 价格等所有关联数据
3. `variants[].customervip` 仅在站点启用了 VIP 会员功能时返回有效数据
4. `wholesale_price` 为变体的批发价格数组，每个元素包含 `qty`（起批数量）和 `price`（批发单价）
5. `weight_unit` 支持 `g`、`kg`、`lb`、`oz` 四种单位
6. `remote_id` 用于与三方系统（如 ERP）同步商品数据时，记录三方系统的商品 ID
7. `glasses_attr` 为眼镜类商品的专有属性，普通商品返回空数据
