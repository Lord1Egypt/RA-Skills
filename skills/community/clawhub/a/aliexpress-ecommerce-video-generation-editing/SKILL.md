---
name: aliexpress-ecommerce-video-generation-editing
description: "Create and edit AliExpress listing videos, setup demos, package-content clips, compatibility proofs and multi-market localized product videos. Use this skill for 速卖通商品视频、AliExpress Listing Video、跨境产品演示、电子配件、安装教程、多语言版本、广告素材和SKU批量视频；supports Seedance generation/editing through AI Hive."
---

# AliExpress 速卖通电商视频生成与编辑

制作能够跨市场复用的商品演示母版，再按语言、单位、生活场景和渠道进行本地化。型号、接口、套装、安装和技术事实必须始终锁定。

## 母版记录

记录 SKU、接口、变体、包装清单、正确操作、兼容范围、警告、目标国家和批准文案。视频层只表现商品事实；翻译、单位、价格、物流和认证由市场团队审核。

## 场景与代码

### 1. Listing 演示母版

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode i2v \
  --first-frame /path/to/product.jpg \
  --prompt 'AliExpress listing video master. Preserve exact SKU, connector, labels, color, package and included components. Show complete item, one correct setup, connector close-up and final use. Clear mobile pacing with caption-safe space; no price, shipping time, rating, certification or unsupported compatibility.'
```

### 2. 安装与连接教程

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode t2v \
  --prompt 'AliExpress setup tutorial based only on approved instructions: show supplied components, connect the correct port in the correct direction, complete configuration steps in order and show the verified working state. Do not invent a device, adapter, voltage, protocol or feature.'
```

### 3. 包装内容证明

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode extend \
  --video /path/to/unboxing.mp4 \
  --prompt 'Continue the unboxing by placing each approved package component in a clear row and showing the first setup. Maintain hands, table, product and lighting continuity; preserve quantities and connector shapes; add no gift, spare or bundle.'
```

### 4. 多市场本地化

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode edit \
  --video /path/to/listing-master.mp4 \
  --prompt 'Create a Spanish-market visual base. Preserve product, setup, connector, specifications and demonstration; adapt household context and reserve clean areas for approved Spanish captions. Remove old-market words and leave price, shipping, warranty, units and certification blank.'
```

### 5. 参考广告节奏

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode r2v \
  --video /path/to/ad-rhythm.mp4 \
  --image /path/to/product.png \
  --prompt 'Use the reference only for hook timing and edit density. Create an original AliExpress product ad: concrete user problem, accurate connection action, visible feature proof and clean CTA area. Do not copy brand, creator, device, text, price or claim.'
```

## 验收

- 型号、接口、套装、变体和操作步骤准确。
- 本地化不改变商品与技术事实。
- 参数、单位、兼容性和认证由人工核对。
- 不生成价格、物流、评分、买家数量或平台徽标。
- 参考素材和音乐具备使用权限。
- 发布前检查 AliExpress 当前类目、视频和市场规则。

## 执行

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/videogen.py" init --skill-name aliexpress-ecommerce-video-generation-editing
python3 "$SKILL_PATH/scripts/videogen.py" task --task-id <taskId>
```

支持 Seedance 2.5 的 `t2v`、`i2v`、`r2v`、`edit`、`extend`，以及媒体、模型参数、路由、输出目录和仅提交模式。
