# 更新商品

`POST /api/skill/product/update`

参数结构与[创建商品](product-create.md)完全一致，仅以下字段处理规则不同：

## Create vs Update 差异对照

| 字段 | Create | Update |
|------|--------|--------|
| `product.id` | 不传 | ✅ 必填 |
| `images[].id` | 不传 | 已有图片传入，新增不传 |
| `videos[].id` | 不传 | 已有视频传入，新增不传 |
| `options[].id` | 不传 | 已有规格传入，新增不传 |
| `variants[].id` | 不传 | 已有变体传入，新增不传 |
| `tags[].id` | `""` | 已有 tag 传实际 ID |
| `payafteruse` | 放在 `product` 内 | 可放顶层 `"payafteruse": 1` |

## Update 子实体额外支持字段

| 子实体 | 额外字段（均为选填） |
|--------|---------------------|
| `images[]` | `product_id` |
| `options[]` | `id`、`product_id`、`shop_id` |
| `variants[]` | `id`、`product_id`、`shop_id`、`image_id`、`gram` |

## 调用

```
node scripts/proxy/api-call.js POST /api/skill/product/update '<JSON_BODY>'
```

## 响应

**`code` 为 `200` 表示调用成功；`code` 不为 `200` 表示调用失败。**

### 成功响应

```json
{ "code": 200, "message": "success", "data": { "product_id": 4646 } }
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `code` | Number | 状态码，`200` 表示成功 |
| `message` | String | 执行结果的文字描述 |
| `data.product_id` | int | 更新后的产品 ID |

### 错误响应

```json
{ "code": 100701001, "message": "product save fail | ..." }
```

### 错误码

| 错误码 | 说明 |
|--------|------|
| `200` | 成功 |
| `100701003` | 商品 id 为空 |
| `100701001` | 商品保存报错（含字段校验失败、缺必填字段等） |
| 其他 | 商品保存报错 |

> 如响应体不是 JSON 而是 HTML（如 `<title>yii\\base\\ErrorException</title>`），说明服务端 PHP 异常，需查服务端日志。

## 更新关键原则

> 先通过 [商品详情 API](product-info.md) 获取完整数据 → 修改需要的字段 → 提交完整的 `images`/`variants`/`options` 数组（保留已有 `id`、移除不需要的、新增不带 `id` 的）。

## 更新示例

```json
{
    "product": {
        "id": 4646,
        "source_type": "",
        "spu": "7218746753195",
        "title": "先用后付，测试：Morden Lighting Nordic Fabric Shade Black White Floor Lamp",
        "sub_title": "",
        "body_html": "<p>...</p>",
        "status": 1,
        "is_tax": 1,
        "virtual_sales_count": 54,
        "type": 2,
        "vendor": "Lighting Made",
        "variant_need_note": 1,
        "variant_need_image": 1,
        "variant_show_image": 3,
        "inventory_police": 1,
        "inventory_police_type": 1,
        "meta_is_edit": 2,
        "meta_title": "Morden Lighting Nordic Fabric Shade Black White Floor Lamp",
        "meta_keywords": "Morden Lighting Nordic",
        "meta_description": "Introducing the Morden Lighting Nordic Fabric Shade...",
        "feed_description": null,
        "feed_title": "",
        "handle": "morden-lighting-big-nordic-fabric-shade-black-or-white-floor-lamp-em7v0pso",
        "translate_type": 3,
        "google_product_category": 111,
        "google_product_type_id": "light",
        "description_json": {},
        "description_json_status": 1,
        "params_json": [],
        "params_json_status": 2,
        "short_description_json": [
            {
                "text": "Morden Lighting Nordic Fabric Shade Black White Floor Lamp",
                "lang_params": { "text": { "cn": "摩登照明北欧布艺灯罩黑白落地灯" } }
            },
            {
                "text": "Nordic Fabric Shade Black White Floor Lamp",
                "lang_params": { "text": { "cn": "北欧风格黑白布艺灯罩落地灯" } }
            },
            {
                "text": "This sleek and stylish floor lamp is perfect for any modern home",
                "lang_params": { "text": { "cn": "这款时尚且造型优美的落地灯非常适合任何现代风格的家居" } }
            }
        ],
        "label_ids": [],
        "collection_ids": [],
        "template_type": ""
    },
    "productattr_info": [
        {"id": "", "attr_id": 31, "item_ids": [63, 56]},
        {"id": "", "attr_id": 29, "item_ids": [52, 53]},
        {"id": "", "attr_id": 35, "item_ids": [60]},
        {"id": "", "attr_id": 33, "item_ids": [61]},
        {"id": "", "attr_id": 32, "item_ids": [57]},
        {"id": "", "attr_id": 28, "item_ids": [62]}
    ],
    "images": [
        { "id": 30335, "product_id": 4646, "position": 1, "src": "/product/15/image/2026/02/08/90526227.jpg", "alt": "", "width": 800, "height": 800, "ratio": "1.00" },
        { "id": 30336, "product_id": 4646, "position": 2, "src": "/product/15/image/2026/02/08/a8a35a02.jpg", "alt": "", "width": 750, "height": 845, "ratio": "0.89" },
        { "id": 30337, "product_id": 4646, "position": 3, "src": "/product/15/image/2026/02/08/66a079e0.jpg", "alt": "", "width": 750, "height": 453, "ratio": "1.66" },
        { "id": 30338, "product_id": 4646, "position": 4, "src": "/product/15/image/2026/02/08/ca8fd9c9.jpg", "alt": "", "width": 750, "height": 564, "ratio": "1.33" }
    ],
    "videos": [
        { "id": 868, "product_id": 4646, "position": 1, "src": "https://cloud.video.taobao.com/play/...mp4", "alt": "" }
    ],
    "addition_group_id": 73,
    "variantremark_id": "",
    "groupbuy_id": "",
    "collection_ids": [349, 345],
    "label_ids": [],
    "options": [
        { "id": 5153, "shop_id": 15, "product_id": 4646, "name": "Color", "position": 1, "items": ["White", "Black"] },
        { "id": 5189, "shop_id": 15, "product_id": 4646, "name": "Size", "position": 2, "items": ["L", "M"] }
    ],
    "variants": [
        {
            "id": 44774, "shop_id": 15, "product_id": 4646, "title": "White / L",
            "price": "68.99", "compare_at_price": "89.99", "cost_price": "38.99",
            "wholesale_price": [{"qty":2,"price":"58.99"},{"qty":5,"price":"53.99"}],
            "sku": "7218746753195-White-L-1010799", "barcode": "",
            "image_id": 30335, "qty": 999,
            "option1": "White", "option2": "L", "option3": "",
            "weight": "2", "weight_unit": "kg", "note": "",
            "image": "/product/15/image/2026/02/08/90526227.jpg",
            "customervip": [{"customervip_id":11,"price":54},{"customervip_id":10,"price":55}],
            "images": [], "buy_min_count": 1
        },
        {
            "id": 44775, "shop_id": 15, "product_id": 4646, "title": "White / M",
            "price": "68.99", "compare_at_price": "89.99", "cost_price": "38.99",
            "wholesale_price": [{"qty":2,"price":"58.99"},{"qty":5,"price":"53.99"}],
            "sku": "7218746753195-White-M-1010800", "barcode": "",
            "image_id": 30335, "qty": 999,
            "option1": "White", "option2": "M", "option3": "",
            "weight": "2", "weight_unit": "kg", "note": "",
            "image": "/product/15/image/2026/02/08/90526227.jpg",
            "customervip": [{"customervip_id":11,"price":54},{"customervip_id":10,"price":55}],
            "images": [], "buy_min_count": 1
        },
        {
            "id": 44776, "shop_id": 15, "product_id": 4646, "title": "Black / L",
            "price": "68.99", "compare_at_price": "89.99", "cost_price": "38.99",
            "wholesale_price": [{"qty":2,"price":"58.99"},{"qty":5,"price":"53.99"}],
            "sku": "7218746753195-Black-L-1010801", "barcode": "",
            "image_id": 30336, "qty": 999,
            "option1": "Black", "option2": "L", "option3": "",
            "weight": "2", "weight_unit": "kg", "note": "",
            "image": "/product/15/image/2026/02/08/a8a35a02.jpg",
            "customervip": [{"customervip_id":11,"price":54},{"customervip_id":10,"price":55}],
            "images": [], "buy_min_count": 1
        },
        {
            "id": 44777, "shop_id": 15, "product_id": 4646, "title": "Black / M",
            "price": "68.99", "compare_at_price": "89.99", "cost_price": "38.99",
            "wholesale_price": [{"qty":2,"price":"58.99"},{"qty":5,"price":"53.99"}],
            "sku": "7218746753195-Black-M-1010802", "barcode": "",
            "image_id": 30336, "qty": 999,
            "option1": "Black", "option2": "M", "option3": "",
            "weight": "2", "weight_unit": "kg", "note": "",
            "image": "/product/15/image/2026/02/08/a8a35a02.jpg",
            "customervip": [{"customervip_id":11,"price":54},{"customervip_id":10,"price":55}],
            "images": [], "buy_min_count": 1
        }
    ],
    "glasses": {
        "button_type": 1, "distance_min": "1.00", "distance_max": "22.00",
        "sex": { "value": "sex", "language": {"cn":"性别"} },
        "lens_type": { "value": "style", "language": {"cn":"风格"} },
        "material": { "value": "type", "language": {"cn":"材质"} }
    },
    "mergeimages": [],
    "tags": [
        {"id": 25, "title": "white"},
        {"id": 79, "title": "black"}
    ],
    "payafteruse": 1
}
```

## 注意事项

1. `product.id` 在更新时必须传入，否则可能被当作新增处理
2. 变体的 `image` 字段必须已存在于 `images` 数组中，否则无法保存
3. `images[].position` 必须从 `1` 开始连续递增，`position=1` 的图片为主图
4. `options[].position` 只能为 `1`、`2`、`3`，且每个 option 的 position 不可重复
5. `variants` 中的 `option1/2/3` 值必须与对应 `position` 的 `options[].items` 中的值匹配
6. `wholesale_price` 为变体的批发价格数组，每个元素包含 `qty`（起批数量）和 `price`（批发单价）
7. `weight_unit` 支持 `g`、`kg`、`lb`、`oz` 四种单位
8. 更新已有数据时传入 `id`（图片 ID、变体 ID、Option ID 等），新增数据时不传 `id`
9. `description_json` 为模板装修数据（Object），非数组；`description_json_status` 为 `1` 时才生效
10. `short_description_json` 每项包含 `text`（默认文本）和 `lang_params.text.{语言}`（多语言翻译）
