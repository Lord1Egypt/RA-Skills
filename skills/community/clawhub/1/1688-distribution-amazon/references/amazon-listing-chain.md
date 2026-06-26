# Amazon Listing Chain Reference

## Capability Map

### AlphaShop

- 1688 offer detail query
- Amazon category mapping query
- Amazon CPV mapping query
- Image translate
- Image translate pro
- Image enlargement
- Image object extraction
- Image element detection
- Image element removal
- Image crop
- Virtual model task submit/query
- Image change model task submit/query

图片处理鉴权使用 `ALI_1688_AK` 和 CSK 签名。Amazon 主图默认先使用图片主题抠图生成白底图：

```json
{
  "imageUrl": "<1688 main image URL>",
  "transparentFlag": false,
  "bgColor": "255,255,255"
}
```

当前通用 agent 链路在 `scripts/map_category.py` 取得 Amazon `productType` 后执行 `scripts/process_images.py` 图片 pipeline，将处理结果写入独立 `image_processing.json`。`scripts/build_product.py` 会在内存中合并处理后的主图，再生成 `baseInfo.scImages`，不会覆盖原始 `query_offer.json`。

图片 pipeline 对每个处理步骤最多重试 3 次。重试只覆盖图片网关的临时失败、失败响应或未返回图片 URL 的情况；3 次后仍失败时必须停止并展示失败步骤、错误摘要和 session 目录。

类目预设 pipeline 由 `scripts/process_images.py` 维护。默认规则：

- `SCREEN_PROTECTOR`: `white_background,crop_4_3`
- `HANDBAG`: `white_background`
- `DRINKING_CUP`: `white_background`
- 其他类目：`white_background`

可以通过 `AMAZON_IMAGE_PIPELINE` 显式覆盖，例如 `white_background,crop_4_3,translate_to_en`。

## Current Standard Chain

当前标准链路以本仓库 `SKILL.md`、本 reference 和 `scripts/` 中的当前实现为准：

1. Step1 查询店小宝用户与 Amazon 店铺上下文。
2. Step2 查询并标准化 1688 商品详情。
3. Step3 以 `platform=amazon` 查询 Amazon 类目映射和 `productType`。
4. Step4 按类目预设图片 pipeline 处理主图，写入 `image_processing.json`。
5. Step5 调用 `getAttrInfoByCateIdToOut` 获取 Amazon schema，默认使用 `required-attr-mode=evaluated` 判断当前 listing 上下文实际必填字段。
6. Step6 调用 CPV 映射，必须携带 `platform=amazon`。
7. Step7 构造 `releaseProductToOut.data`，按 Amazon schema 结构化复杂字段；用户指定库存时显式写入库存。
8. Step8 默认提交 `releaseProductToOut type=localSave`，保存为店小宝本地草稿并返回 `localId`。

历史 `hard` 模式只用于诊断对比，不作为真实铺货标准。
当前 skill 主流程完成点是 `localSave` 返回 `localId`。成功后引导用户前往店小宝亚马逊商品管理页-待发布商品：`https://page.1688.com/html/isv-bridge.html?version=0.0.26&appKey=5050627&role=buyer`。

## Product Design Boundary

- Dianxiaobao now supports draft-style local save through `releaseProductToOut type=localSave`.
- The formal listing skill creates Amazon pending-product drafts in Dianxiaobao.
- Users finish later publishing from Dianxiaobao's Amazon pending-products page.

### Dianxiaobao

- `POST https://goods.dianxiaobao.net/shop/queryDxbInfoById`
- `POST https://goods.dianxiaobao.net/api-goods/aboutProduct/queryCategoryInfoToOut`
- `POST https://goods.dianxiaobao.net/api-goods/aboutProduct/getAttrInfoByCateIdToOut`
- `POST https://goods.dianxiaobao.net/api-goods/product/releaseProductToOut`

## Amazon Attribute Request

Amazon category attributes are queried with this envelope:

```json
{
  "userCode": "<encryptedCode>",
  "storeName": "<storeName>",
  "marketplaceId": "ATVPDKIKX0DER",
  "productType": "DRINKING_CUP",
  "ptName": "amazon"
}
```

## Amazon Release Envelope

Amazon publishing uses the same outer envelope for no-SKU and multi-SKU products:

```json
{
  "ptName": "amazon",
  "userCode": "<encryptedCode>",
  "storeName": "<storeName>",
  "type": "localSave",
  "data": "<Amazon listing JSON string>"
}
```

Release type options:

- `localSave`: default skill path. Pair with `data`; response should contain `localId`.

The `data` JSON must contain `storeName`, `site`, `languageTag`, `categoryId`, `fullCategoryId`, `ptType`, `subject`, `productSkuType`, `upcExempt`, `brandName`, `manufacturer`, `cateInfo`, `baseInfo`, `attrInfo`, `skuInfo`, `tradeInfo`, `safetyAndCompliance`, `packInfo`, `detailInfo`, and `otherInfo`.

Key request-shape details captured in this repo:

- No-SKU products use `productSkuType=0`, `upcExempt=1`, and `skuInfo.skuSpeci={"variation_theme":""}`.
- For `productSkuType=0`, put the unique seller SKU in `baseInfo.parentSku` and leave `tradeInfo.skuAndPrice[0].skuCode` blank. Filling both parent SKU and SKU code can cause Amazon `Malformed attributes: [sku]` errors.
- Multi-SKU products use `productSkuType=1`, default `upcExempt=0`, and `skuInfo.skuSpeci` carries `variation_theme` plus variation value arrays.
- `attrInfo.catProp`, `skuInfo.skuSpeci`, `tradeInfo.skuAndPrice`, package dimensions, pricing rule, shipping model, and compliance media are JSON strings nested inside `data`.
- `tradeInfo.skuAndPrice[]` includes `conditionType`, `attrTypes`, `skuGroup`, `discountedStartTime`, and `discountedEndTime` in addition to price, inventory, image, and external product ID fields.
- Formal design rule: the final product should use `localSave` and create a Dianxiaobao pending-product draft.
- Current inventory rule: Step6 must always fill both `tradeInfo.skuAndPrice[].inventory` and `fulfillment_availability.quantity`. Default quantity is `1`.
- Inventory must keep `tradeInfo.skuAndPrice[].inventory` and `fulfillment_availability.quantity` aligned.
- `safetyAndCompliance` includes `country_of_origin`, `batteries_required`, and `supplier_declared_dg_hz_regulation`.
- `otherInfo` includes `complianceMediaShow`, `searchKeywords`, `complianceMedia`, `responsiblePartyEmail`, and `manufacturerEmail`.

Current Step6 shaping rules from the Step8 failure report:

- `item_package_dimensions` must be a nested object with `length`, `width`, and `height`; each child must contain `unit` and numeric `value`.
- `item_package_weight` must be a nested object with `unit` and numeric `value`.
- `fulfillment_availability` must contain Amazon enum field `fulfillment_channel_code`; FBM maps to `DEFAULT`.
- `list_price` must be numeric `{currency,value}`. It must not use low CPV source price when a high sale price is configured; default list price is derived from the highest SKU sale price times `AMAZON_LIST_PRICE_MULTIPLIER` (`1.25` by default).
- `stones` must be structured with `id`, `type`, `creation_method`, `treatment_method`, and `number_of_stones`.
- Inventory rule: inventory must not be blank. `build_product.py` defaults to `1`; explicit user inventory can be applied to the draft payload with `run_local_save.py --inventory-quantity <n>` or `build_product.py <session_dir> --inventory-quantity <n>`. Do not use undefined variables such as `INVENTORY=<n>`.

## Draft Completion Gate

- Default skill main-flow success is Step7 `releaseProductToOut type=localSave` returning success and a `localId`.
- User-facing final response should include `localId`, store name, marketplace, session directory, and the Dianxiaobao Amazon pending-products page URL.
- If the user asks for Amazon online publishing, state that this skill creates the Dianxiaobao pending draft and that publishing should be completed from the Dianxiaobao page.
