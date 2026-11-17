---
name: etsy-ecommerce-image-generation-editing
description: "Create and edit Etsy listing images for handmade, vintage and personalized products, including scale, material, maker-process, customization and gift-packaging visuals. Use this skill for Etsy商品图、手作产品、个性化定制、刻字预览、复古商品、制作过程、礼物包装、尺寸参考和创作者店铺视觉；supports AI Hive reference generation."
---

# Etsy 电商图片生成与编辑

帮助买家理解物品本身、手作过程、尺寸、材料和可定制范围，同时保留卖家的真实创作痕迹。不要把批量工业品伪装成手工，也不要修掉复古物品的重要磨损或生成不存在的刻字成品。

## 真实性底稿

收集成品多角度图、材料、尺寸、制作步骤、可选文字/颜色、复古物品状况、包装方式、创作者空间和知识产权边界。个性化内容必须来自买家输入并在生产前确认。

## 场景与代码

### 1. Handmade listing hero

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt 'Etsy handmade listing hero using the exact reference item. Preserve shape, material, maker marks, color and natural handmade variation. Show the complete object on a warm simple surface with realistic scale and texture. Do not add a brand, bestseller badge, review, personalization or perfect factory symmetry.' \
  --image /path/to/handmade-item.jpg
```

### 2. 尺寸与使用比例

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt 'Create an Etsy scale image showing the reference item naturally held in one hand and placed beside an ordinary desk object. Keep item dimensions visually consistent and reserve blank measurement callouts for seller-approved numbers. Do not generate measurements or change size between views.' \
  --image /path/to/item.png
```

### 3. 个性化预览底图

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt 'Personalization preview base for the reference pendant: preserve metal, shape and engraving area; show three clean layout positions with blank text placeholders. Do not invent a customer name, final engraving, trademarked phrase or production guarantee.' \
  --image /path/to/pendant.jpg
```

### 4. 制作过程套图

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt 'Create four process images from the seller-provided workshop references: material preparation, shaping, finishing and final inspection. Keep the real maker space, hands, tools and item consistent; do not add machinery, staff, certificates or steps that were not provided.' \
  --image /path/to/workshop-1.jpg \
  --image /path/to/workshop-2.jpg \
  --batch 4
```

### 5. 礼物包装与到货内容

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt 'Etsy gift-packaging image showing exactly the supplied item, box, tissue, care card and ribbon, each once. Warm gifting mood, clear package contents, no free gift, shipping promise, handwritten customer message or holiday trademark.' \
  --image /path/to/packaging.jpg
```

## 上架验收

- 商品、材料、手作差异和复古磨损如实保留。
- 尺寸、材料与个性化范围来自卖家资料。
- 制作过程只使用真实工作室、工具和步骤。
- 不生成客户姓名、买家评价、评分、销量或“手工”证明。
- 检查图案、文字、角色和品牌的知识产权权限。
- 按 Etsy 当前 Handmade、Vintage、Personalized 与广告规则复核。

## 执行

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name etsy-ecommerce-image-generation-editing
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

固定使用 Nano Banana Pro 图片入口，支持参考图、批量、实时参数、路由与任务查询。个性化订单先确认预览再生产。
