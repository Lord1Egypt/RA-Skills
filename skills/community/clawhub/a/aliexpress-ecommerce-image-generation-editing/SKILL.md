---
name: aliexpress-ecommerce-image-generation-editing
description: "Create and edit AliExpress product listing images, variant galleries, compatibility graphics, package-content images and multi-country localization bases. Use this skill for 速卖通商品图、AliExpress主图、跨境Listing、电子配件、规格图、多语言详情页、SKU批量图、包装清单和多市场广告素材；supports reference-guided AI Hive generation."
---

# AliExpress 速卖通电商图片生成与编辑

为跨国家、跨语言商品目录建立可复用图片系统。商品、接口、规格和套装内容属于统一事实层；语言、单位、使用场景与活动信息属于市场层，二者不能混用。

## Listing 事实表

记录商品型号、变体、接口、材料、尺寸、包装清单、兼容范围、目标国家、单位制、批准文案和禁售/限制信息。复杂参数、认证与翻译文字由运营后期排版并复核。

## 场景与代码

### 1. AliExpress 主图

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt 'AliExpress listing primary image for the supplied SKU. Preserve exact product shape, connector, labels, color, package and included parts. Show the complete item large on a clean background with realistic shadow and crop tolerance. No price, discount, shipping promise, rating, certification or unprovided text.' \
  --image /path/to/product-front.png \
  --image /path/to/product-back.png
```

### 2. 接口与兼容性底图

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt 'AliExpress compatibility graphic base: accurate product plus two close-ups of the actual connector and control area, with clean callout spaces for merchant-approved device list and specifications. Do not create a port, protocol, voltage, certification or compatibility claim.' \
  --image /path/to/connectors.jpg
```

### 3. 套装与包装清单

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt 'Top-down AliExpress package-content image showing exactly the supplied main unit, cable, adapter and manual, each once and with correct connector shape. Use clear spacing and neutral background; do not add a gift, spare part, bundle name or shipping badge.' \
  --image /path/to/package-reference.jpg
```

### 4. 多市场详情页底图

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt 'Create three localized lifestyle bases for the same AliExpress SKU: Spain, Brazil and South Korea. Preserve product and use method; adapt household context and caption-safe layout only. Leave language, units, warranty, plug compatibility and offer areas blank for approved localization.' \
  --image /path/to/product.png \
  --batch 3
```

### 5. SKU 变体统一

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt 'Generate catalog images for merchant-confirmed black, silver and blue variants. Lock geometry, connector, camera angle, scale, background, label and package; change only the true color. One SKU per image, no mixed bundle.' \
  --image /path/to/master-sku.png \
  --batch 3
```

## 跨境验收

- 型号、接口、标签、变体和包装清单准确。
- 语言、单位、插头、兼容性与认证按市场审核。
- 本地化版本只改场景与版式，不改商品事实。
- 不生成价格、运输时效、评分、买家数量或平台徽标。
- 文件名包含 SKU、国家、语言、用途和版本。
- 上架前检查 AliExpress 当前类目和目标市场规则。

## 执行

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name aliexpress-ecommerce-image-generation-editing
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

固定调用 `public_model_nano_banana_pro`。支持多参考图、批量、实时参数、路由、输出目录和仅提交模式；批量前核对实时费用。
