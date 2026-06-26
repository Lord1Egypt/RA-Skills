# Amazon 铺货常见问题

## 默认为什么只保存本地草稿

Amazon 铺货执行 `releaseProductToOut type=localSave`。这会在店小宝侧生成 Amazon 待发布草稿，返回 `localId`。

如果用户要求直接发布，也按当前 skill 流程保存为店小宝 Amazon 待发布草稿，并引导用户前往店小宝亚马逊商品管理页-待发布商品：

```text
https://page.1688.com/html/isv-bridge.html?version=0.0.26&appKey=5050627&role=buyer
```

回复用户时必须输出完整 URL，包含 `https://`。

## 库存数量规则

草稿 payload 不允许库存为空。`build_product.py` 默认写入库存 `1`，也可以用显式参数覆盖：

```bash
bash scripts/run_python.sh scripts/run_local_save.py <offerId> --store-name "<storeName>" --marketplace-id ATVPDKIKX0DER --inventory-quantity <n>
```

分步执行时使用：

```bash
bash scripts/run_python.sh scripts/build_product.py <session_dir> --inventory-quantity <n>
```

脚本会同时写入 `tradeInfo.skuAndPrice[].inventory` 和 `fulfillment_availability.quantity`。
禁止使用 `INVENTORY=<n>`，该环境变量不会被当前脚本读取。

## 单 SKU 报 Malformed attributes: [sku]

单 SKU no-SKU 商品必须使用当前内联契约中的 no-SKU 结构：

- `productSkuType=0`
- `baseInfo.parentSku` 承载唯一 seller SKU
- `tradeInfo.skuAndPrice[0].skuCode` 置空
- 移除 `variation_theme` 和 variation 类 catProp

## CPV 映射为空

Amazon CPV 映射必须传 `platform=amazon`。若 `map_pv_attrs.py` 返回空结果，先检查 `map_amazon_attrs.json.requiredAttrs` 是否为空；如果 Amazon schema 没有解析出当前上下文必填字段，优先复查 `map_amazon_attrs.py` 的 `requiredMode` 和 `conditionContexts`。

## 图片处理失败

默认图片链路通过 `process_images.py` 执行：

- `white_background`
- 类目需要时追加 `crop_4_3`
- 类目或平台要求语言处理时可追加 `translate_to_en`

图片处理结果写入 `image_processing.json`，不会覆盖 `query_offer.json`。
每个图片处理步骤最多重试 3 次。3 次后仍失败时停止，不要伪造图片结果或跳过主图处理。
