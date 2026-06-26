# 创建商品

`POST /api/skill/product/create`

## 调用

```
node scripts/proxy/api-call.js POST /api/skill/product/create '<JSON_BODY>'
```

## 请求体顶层结构

| 顶层字段 | 类型 | 必填 | 说明 |
|----------|------|------|------|
| `product` | Object | ✅ | 产品主体数据 |
| `images` | Array | ✅ | 产品图片 |
| `variants` | Array | ✅ | 产品变体，单规格数组只有一个子项 |
| `options` | Array | 选填 | 产品规格定义，单规格为空，多规格必填 |
| `collection_ids` | int[] | 选填 | 产品所属专辑 ID 数组（多对多） |
| `tags` | Array | 选填 | 商品 tag 数组 |
| `videos` | Array | 选填 | 产品视频列表 |
| `productattr_info` | Array | 选填 | 产品属性信息 |
| `glasses` | Object | 选填 | 眼镜类商品属性 |
| `mergeimages` | Array | 选填 | 合并图片列表 |
| `addition_group_id` | string/int | 选填 | 附加分组 ID |
| `variantremark_id` | string/int | 选填 | 变体备注 ID |
| `groupbuy_id` | string/int | 选填 | 团购 ID |
| `label_ids` | Array | 选填 | 角标 ID 数组 |

## product 字段详表

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `title` | string | ✅ 必填 | 产品标题 |
| `body_html` | string | ✅ 必填 | 产品描述（HTML） |
| `type` | int | ✅ 必填 | 规格类型：`1` 单规格 / `2` 多规格 |
| `spu` | string | 选填 | 产品 SPU |
| `sub_title` | string | 选填 | 产品副标题 |
| `handle` | string | 选填 | 商品 URL handle，不填则用 title 自动生成 |
| `status` | int | 选填 | 产品状态：`1` 上架 / `2` 下架，默认上架 |
| `vendor` | string | 选填 | 产品厂家/品牌名称 |
| `virtual_sales_count` | int | 选填 | 产品虚拟销量 |
| `is_tax` | int | 选填 | 是否收税：`1` 收税 / `2` 不收税 |
| `payafteruse` | int | 选填 | 先用后付：`1` 先用后付商品 / `2` 普通商品 |
| `variant_need_image` | int | 选填 | 规格是否需要图片：`1` 需要 / `2` 不需要，默认 `1` |
| `variant_show_image` | int | 选填 | 前台商城规格显示方式：`1` 显示文字 / `2` 显示图片 / `3` 使用插件默认配置 |
| `variant_need_note` | int | 选填 | 变体是否需要备注：`1` 需要 / `2` 不需要 |
| `inventory_police` | int | 选填 | 是否跟踪库存：`1` 跟踪 / `2` 不跟踪，默认 `1` |
| `inventory_police_type` | int | 选填 | 库存策略：`1` 库存为 0 允许购买 / `2` 库存为 0 不允许购买 / `3` 库存为 0 自动下架，默认 `1` |
| `meta_is_edit` | int | 选填 | SEO 信息是否独立编辑：`1` 非独立编辑 / `2` 独立编辑 |
| `meta_title` | string | 选填 | SEO 标题 |
| `meta_keywords` | string | 选填 | SEO 关键字 |
| `meta_description` | string | 选填 | SEO 描述 |
| `feed_title` | string | 选填 | Feed 自定义 title |
| `feed_description` | string | 选填 | Feed 自定义 description |
| `translate_type` | int | 选填 | 翻译类型：`1` 强制翻译 / `2` 只翻译多语言为空部分 / `3` 不翻译 |
| `source_type` | int/string | 选填 | source 类型：`1` 代表 1688 |
| `template_type` | string | 选填 | 模版装修的 template key |
| `google_product_category` | int | 选填 | Google 商品分类 ID |
| `google_product_type_id` | string | 选填 | Google 产品类型 |
| `description_json` | Object | 选填 | JSON 描述内容（模板装修数据） |
| `description_json_status` | int | 选填 | 描述是否使用 JSON：`1` 开启 / `2` 关闭 |
| `params_json` | Array | 选填 | 参数 JSON 内容 |
| `params_json_status` | int | 选填 | 参数是否使用 JSON：`1` 开启 / `2` 关闭 |
| `short_description_json` | Array | 选填 | 简短描述，每项 `{ text: string, lang_params: { text: { "语言": "翻译" } } }` |
| `collection_ids` | int[] | 选填 | 产品所属专辑 ID 数组 |
| `label_ids` | Array | 选填 | 角标 ID 数组 |

## images[] 字段详表

> 新增时不传 `id`，系统自动生成。

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `src` | string | ✅ 必填 | 产品图片路径（需先通过 [上传图片 API](../base-images/image-upload.md) 获取） |
| `position` | int | ✅ 必填 | 排序位置，从 `1` 开始依次递增，`1` 为主图 |
| `alt` | string | 选填 | 图片 alt 文本 |
| `width` | int | 选填 | 图片宽度（像素） |
| `height` | int | 选填 | 图片高度（像素） |
| `ratio` | string | 选填 | 宽高比 |
| `key` | float | 选填 | 前端唯一标识 key |

## variants[] 字段详表

> 单规格产品数组只有一个子项。新增时不传 `id`。

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `price` | float | ✅ 必填 | 售卖价格 |
| `qty` | int | ✅ 必填 | 变体库存，默认 `0` |
| `weight` | string | ✅ 必填 | 变体重量 |
| `weight_unit` | string | ✅ 必填 | 重量单位：`g` / `kg` / `lb` / `oz` |
| `option1` | string | 选填 | 规格值 1，其值必须存在于 `options` 中 `position=1` 那行的 `items` 数组中 |
| `option2` | string | 选填 | 规格值 2，其值必须存在于 `options` 中 `position=2` 那行的 `items` 数组中 |
| `option3` | string | 选填 | 规格值 3，其值必须存在于 `options` 中 `position=3` 那行的 `items` 数组中 |
| `compare_at_price` | float | 选填 | 划线价格 |
| `cost_price` | float | 选填 | 成本价格 |
| `wholesale_price` | Array | 选填 | 批发价格，每项 `{ qty: int, price: float }` |
| `sku` | string | 选填 | 产品 SKU（根据配置项决定必填唯一/选填唯一/选填非唯一） |
| `barcode` | string | 选填 | 条形码 |
| `image` | string | 选填 | 变体图片路径。**该图片必须存在于 `images` 数组中，否则保存失败** |
| `note` | string | 选填 | 变体备注 |
| `buy_min_count` | int | 选填 | 最小起购数量 |
| `customervip` | Array | 选填 | VIP 会员价格，每项 `{ customervip_id: int, price: float }` |
| `images` | Array | 选填 | 变体图片列表 |

## options[] 字段详表

> 单规格产品为空数组，多规格产品必填。新增时不传 `id`。

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `name` | string | ✅ 必填 | 规格名称（如 "Color"、"Size"） |
| `position` | int | ✅ 必填 | 规格排序，只能为 `1`/`2`/`3`，每个 option 的 position 不可重复 |
| `items` | string[] | ✅ 必填 | 规格子项数组（如 `["White", "Black"]`） |

## 其他字段

### videos[]

> 新增时不传 `id`。

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `src` | string | ✅ 必填 | 视频 URL 路径 |
| `alt` | string | 选填 | 视频 alt 文本 |
| `position` | int | ✅ 必填 | 排序位置 |
| `key` | float | 选填 | 前端唯一标识 key |

### tags[]

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `id` | string | 选填 | Tag ID，新增时传空字符串 `""` |
| `title` | string | 选填 | Tag 标题 |

### productattr_info[]

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `attr_id` | int | ✅ 必填 | 属性 ID |
| `item_ids` | int[] | ✅ 必填 | 属性值 ID 数组 |
| `id` | string | 选填 | 记录 ID，新增时传空字符串 |

### glasses

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `button_type` | int | 选填 | 按钮类型 |
| `distance_min` | string | 选填 | 最小距离 |
| `distance_max` | string | 选填 | 最大距离 |
| `sex` | Object | 选填 | `{ value: string, language: { "cn": "性别" } }` |
| `lens_type` | Object | 选填 | `{ value: string, language: { "cn": "类型" } }` |
| `material` | Object | 选填 | `{ value: string, language: { "cn": "材料" } }` |

### mergeimages[]

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `src` | string | ✅ 必填 | 图片路径 |
| `position` | int | ✅ 必填 | 图片位置排序 |
| `alt` | string | 选填 | 图片 alt 文字 |
| `width` | int | 选填 | 图片宽度（像素） |
| `height` | int | 选填 | 图片高度（像素） |
| `ratio` | string | 选填 | 宽高比 |

## 响应

**`code` 为 `200` 表示调用成功；`code` 不为 `200` 表示调用失败。**

### 成功响应

```json
{ "code": 200, "message": "success", "data": { "product_id": 4693 } }
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `code` | Number | 状态码，`200` 表示成功 |
| `message` | String | 执行结果的文字描述 |
| `data.product_id` | int | 创建成功后返回的新产品 ID |

### 错误响应

```json
{ "code": 100701001, "message": "product save fail | Inventory Police cannot be blank." }
```

### 错误码

| 错误码 | 说明 |
|--------|------|
| `200` | 成功 |
| `100701003` | 商品 id 为空 |
| `100701001` | 商品保存报错（含字段校验失败、缺必填字段等） |
| 其他 | 商品保存报错 |

> 如响应体不是 JSON 而是 HTML（如 `<title>yii\base\ErrorException</title>`），说明服务端 PHP 异常，需查服务端日志。

## 创建示例（多规格完整请求体）

```json
{
    "product": {
        "spu": "3232323",
        "title": "Morden Lighting Nordic Fabric Shade Black White Floor Lamp",
        "sub_title": "...subtitle",
        "body_html": "<p>Template HTML...</p>",
        "status": 1,
        "is_tax": 1,
        "payafteruse": 1,
        "virtual_sales_count": 33,
        "type": 2,
        "vendor": "Lighting Made",
        "variant_need_image": 1,
        "variant_show_image": 3,
        "inventory_police": 1,
        "inventory_police_type": 1,
        "meta_is_edit": 2,
        "meta_title": "Morden Lighting Nordic Fabric Shade Black White Floor Lamp",
        "meta_keywords": "Morden Lighting",
        "meta_description": "Introducing the Morden Lighting...",
        "feed_description": "google feed description",
        "feed_title": "google feed title",
        "handle": "morden-lighting-nordic-fabric-shade-black-white-floor-lamp",
        "translate_type": 3,
        "google_product_category": 111,
        "google_product_type_id": "light",
        "description_json": {},
        "description_json_status": 1,
        "params_json": [],
        "params_json_status": 2,
        "template_type": "product",
        "variant_need_note": 1,
        "short_description_json": [
            { "text": "Morden Lighting Nordic...", "lang_params": { "text": { "cn": "摩登照明北欧布艺灯罩黑白落地灯" } } },
            { "text": "Nordic Fabric Shade...", "lang_params": { "text": { "cn": "北欧风格黑白布艺灯罩落地灯" } } }
        ]
    },
    "productattr_info": [],
    "images": [
        { "src": "/product/15/image/2026/04/28/3fb5620f.jpg", "position": 1, "alt": "", "width": 600, "height": 600, "ratio": "1.00" },
        { "src": "/product/15/image/2026/04/28/f6d04b41.jpg", "position": 2, "alt": "", "width": 600, "height": 600, "ratio": "1.00" },
        { "src": "/product/15/image/2026/04/28/858278fe.jpg", "position": 3, "alt": "", "width": 600, "height": 600, "ratio": "1.00" }
    ],
    "videos": [
        { "src": "https://cloud.video.taobao.com/play/...mp4", "position": 1, "alt": "" }
    ],
    "addition_group_id": 73,
    "variantremark_id": 9,
    "groupbuy_id": 12,
    "collection_ids": [342, 343],
    "label_ids": [],
    "options": [
        { "name": "Color", "position": 1, "items": ["grey", "white"] },
        { "name": "Size", "position": 2, "items": ["L", "M"] }
    ],
    "variants": [
        {
            "price": "59.99", "compare_at_price": "69.99", "cost_price": "29.99",
            "sku": "3232323-grey-L", "barcode": "1111",
            "image": "/product/15/image/2026/04/28/3fb5620f.jpg",
            "qty": 8999, "option1": "grey", "option2": "L", "option3": "",
            "weight": "11", "weight_unit": "kg", "note": "grey l", "buy_min_count": 1,
            "wholesale_price": [{"qty":2,"price":"45.88"},{"qty":5,"price":"41.88"}],
            "customervip": [{"customervip_id":11,"price":44},{"customervip_id":10,"price":45}]
        },
        {
            "price": "59.99", "compare_at_price": "69.99", "cost_price": "29.99",
            "sku": "3232323-grey-M", "barcode": "2222",
            "image": "/product/15/image/2026/04/28/3fb5620f.jpg",
            "qty": 8999, "option1": "grey", "option2": "M", "option3": "",
            "weight": "11", "weight_unit": "kg", "note": "grey m", "buy_min_count": 1,
            "wholesale_price": [{"qty":2,"price":"45.88"},{"qty":5,"price":"41.88"}],
            "customervip": [{"customervip_id":11,"price":44},{"customervip_id":10,"price":45}]
        },
        {
            "price": "59.99", "compare_at_price": "69.99", "cost_price": "29.99",
            "sku": "3232323-white-L", "barcode": "3333",
            "image": "/product/15/image/2026/04/28/858278fe.jpg",
            "qty": 8999, "option1": "white", "option2": "L", "option3": "",
            "weight": "11", "weight_unit": "kg", "note": "white l", "buy_min_count": 1,
            "wholesale_price": [{"qty":2,"price":"45.88"},{"qty":5,"price":"41.88"}],
            "customervip": [{"customervip_id":11,"price":44},{"customervip_id":10,"price":45}]
        },
        {
            "price": "59.99", "compare_at_price": "69.99", "cost_price": "29.99",
            "sku": "3232323-white-M", "barcode": "4444",
            "image": "/product/15/image/2026/04/28/858278fe.jpg",
            "qty": 8999, "option1": "white", "option2": "M", "option3": "",
            "weight": "11", "weight_unit": "kg", "note": "white m", "buy_min_count": 1,
            "wholesale_price": [{"qty":2,"price":"45.88"},{"qty":5,"price":"41.88"}],
            "customervip": [{"customervip_id":11,"price":44},{"customervip_id":10,"price":45}]
        }
    ],
    "glasses": {
        "button_type": 1, "distance_min": "11", "distance_max": "99",
        "sex": { "value": "sex", "language": {"cn":"性别"} },
        "lens_type": { "value": "style", "language": {"cn":"类型"} },
        "material": { "value": "type", "language": {"cn":"材料"} }
    },
    "mergeimages": [],
    "tags": [
        { "title": "white", "id": "" },
        { "title": "black", "id": "" }
    ]
}
```

## 注意事项

1. `body_html` 为商品详情页的 HTML 模板装修内容，与 `description_json` 对应
2. 变体的 `image` 字段必须已存在于 `images` 数组中，否则无法保存
3. `images[].position` 必须从 `1` 开始连续递增，`position=1` 的图片为主图
4. `options[].position` 只能为 `1`、`2`、`3`，且每个 option 的 position 不可重复
5. `variants` 中的 `option1/2/3` 值必须与对应 `position` 的 `options[].items` 中的值匹配
6. `wholesale_price` 为变体的批发价格数组，每个元素包含 `qty`（起批数量）和 `price`（批发单价）
7. `weight_unit` 支持 `g`、`kg`、`lb`、`oz` 四种单位
8. `description_json` 为模板装修数据（Object），非数组；`description_json_status` 为 `1` 时才生效
9. `short_description_json` 每项包含 `text`（默认文本）和 `lang_params.text.{语言}`（多语言翻译）
10. 新增时所有实体的 `id` 字段均不需要传（或传空），系统会自动生成
