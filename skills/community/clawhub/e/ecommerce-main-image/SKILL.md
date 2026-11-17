---
name: ecommerce-main-image
description: "使用 Nano Banana 2 为不同电商渠道制作准确、可复用的商品主图，从 SKU 真值表生成白底、场景、规格与活动留白版本。Use this skill for 电商主图、商品主图、电商首图、SKU 图、白底图、淘宝天猫京东拼多多抖店小红书 Amazon TikTok Shop Shopify Listing 图片、商品卡和多平台上新；通过 AI Hive 生成。"
---

# 电商主图

本 Skill 锁定 `public_model_nano_banana_2`。它解决的是“同一 SKU 如何稳定地产出多个渠道视图”，重点放在商品身份、数量、变体、标配和渠道构图，而不是宣称一张图自动成为爆款。

## SKU 真值表

生成前写清：SKU 编号、批准照片、颜色名称、可见结构、包装数量、随附物、不得出现的道具、目标渠道、比例和文字安全区。每张成图都必须能对应到这张表，未知信息留空，不让模型猜。

## 五个上新场景

### 1. 标准白底首图

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate   --image ./sku-104-approved.png   --prompt '生成1:1电商白底首图：只展示SKU-104便携风扇一个，叶罩、底座、按键、颜色和Logo与参考图一致，三分之二视角、主体约占画面75%、自然接触阴影；不生成文字、人物、充电线、赠品、价格或新结构'   --param aspect_ratio=1:1
```

### 2. 内容渠道商品卡

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate   --image ./sku-208-approved.png   --prompt '制作4:5内容电商商品卡底图：准确保留香薰机外形、出雾口、木纹、灯带与Logo，放在真实卧室床头，顶部和下方留信息位；不生成香味、睡眠功效、价格、人物、平台Logo或未确认配件'   --param aspect_ratio=4:5
```

### 3. 标配组合图

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate   --image ./sku-311-kit.png   --prompt '生成1:1标配组合主图：只展示参考资料确认的键盘、鼠标、接收器各一个，颜色、键位、Logo、比例和数量准确，浅灰背景、整齐分层；不生成鼠标垫、电池、文字、包装、赠品或重复物件'   --param aspect_ratio=1:1
```

### 4. 两个颜色变体

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate   --image ./sku-bag-black.png ./sku-bag-cream.png   --prompt '分别生成黑色与奶油色手提包 SKU 主图。两张保持包型、缝线、五金、提手、相机角度、白背景和商品占比完全一致，每张仅一个包；不要混色、增加吊饰、文字、人物或新口袋'   --batch 2   --param aspect_ratio=1:1
```

### 5. 活动版留白适配

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate   --image ./sku-pan-approved.png   --prompt '生成两张活动主图底稿：平底锅形状、手柄、涂层、颜色和Logo不变，A版左侧留活动信息区，B版顶部留活动信息区；只改变留白位置，不生成折扣、低价、火焰、食物、文字或额外锅具'   --batch 2   --param aspect_ratio=1:1
```

## 上架验收

逐项核对 SKU、数量、结构、颜色、Logo、随附物和包装；在手机缩略图检查类别识别；再按目标平台当前主图政策检查背景、文字、边距和禁用元素。价格与促销信息建议在后台或后期排版中加入，避免生成错误。

## 网络与命令边界

可从文字起稿，也可使用商家明确提供的图片。脚本只用 Nano Banana 2 生成、查询任务与下载图片，认证请求固定前往 `https://ai-hive.iclip.cn/api`；没有聊天、视频、用户信息或余额命令。

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name ecommerce-main-image
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

平台名称只描述素材用途，不表示官方合作；批量上新前以各平台实时规则为准。
