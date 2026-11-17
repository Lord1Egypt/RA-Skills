---
name: etsy-ecommerce-video-generation-editing
description: "Create and edit Etsy listing videos for handmade, vintage and personalized products, including maker process, scale, customization, packaging and use demonstrations. Use this skill for Etsy商品视频、手作过程、个性化定制、刻字预览、复古商品状态、创作者故事、礼物包装和Listing演示；supports Seedance modes through AI Hive."
---

# Etsy 电商视频生成与编辑

用短视频证明物品真实存在、如何制作、大小如何、如何定制和会收到什么。保留手工痕迹与复古状况，不把工业品包装成手作，也不伪造创作者、工作室或制作过程。

## 卖家底稿

准备成品、尺寸、材料、真实制作步骤、工作室、工具、个性化范围、复古瑕疵、包装内容和版权说明。买家姓名与定制文字只有在订单确认后才能进入生产素材。

## 场景与代码

### 1. Handmade listing video

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode i2v \
  --first-frame /path/to/handmade-item.jpg \
  --prompt 'Etsy handmade listing video preserving exact item, material, color, maker marks and natural variation. Slowly show full object, texture, underside and item held for scale, then return to the complete piece. Warm simple setting; no rating, bestseller badge, customer name or factory-perfect symmetry.'
```

### 2. 真实制作过程

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode edit \
  --video /path/to/maker-process.mp4 \
  --prompt 'Edit the real maker footage into material preparation, shaping, finishing and inspection. Preserve creator hands, tools, workshop and actual sequence; remove dead time but do not add machinery, staff, certificates or unperformed steps.'
```

### 3. 个性化流程说明

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode t2v \
  --prompt 'Etsy personalization explainer: show blank item, indicate approved text area, present three layout choices with placeholder shapes, then show seller review before production. Do not generate a real customer name, copyrighted phrase, final engraving or delivery guarantee.'
```

### 4. 复古商品状态记录

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode i2v \
  --first-frame /path/to/vintage-item.jpg \
  --prompt 'Etsy vintage condition video: preserve exact patina, scratches, discoloration, maker mark and missing parts; show front, back, edges and scale under neutral light. Do not restore, hide damage, replace a part or imply authentication.'
```

### 5. 礼物包装与到货内容

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode extend \
  --video /path/to/item-video.mp4 \
  --prompt 'Continue into the real packaging process: place item in supplied box, add tissue, care card and ribbon, then show final parcel contents. Maintain item and hands; do not add a gift, handwritten customer message, shipping date or holiday trademark.'
```

## 真实性验收

- 商品、材料、尺寸感、手作差异和复古磨损如实呈现。
- 制作过程来自真实创作者、工具和步骤。
- 个性化文字在买家确认前只使用占位符。
- 不生成评分、销量、认证、版权角色或“手工”证明。
- 音乐、图案、文字和参考素材具备使用权。
- 发布前检查 Etsy 当前 Handmade、Vintage 和 Personalized 规则。

## 执行

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/videogen.py" init --skill-name etsy-ecommerce-video-generation-editing
python3 "$SKILL_PATH/scripts/videogen.py" task --task-id <taskId>
```

使用 Seedance 2.5 的生成、参考、编辑与延长能力。传入素材、实时参数、路由与输出目录；超时后继续查询原任务。
