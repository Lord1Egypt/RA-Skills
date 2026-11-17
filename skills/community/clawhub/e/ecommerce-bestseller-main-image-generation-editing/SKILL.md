---
name: ecommerce-bestseller-main-image-generation-editing
description: "使用 Nano Banana Pro 生成和编辑电商主图，通过搜索缩略图、商品事实、可视证据、渠道规范与单变量测试提升转化候选质量。Use this skill for 电商爆款主图生成与编辑、商品首图、淘宝天猫京东拼多多抖音电商小红书 Amazon TikTok Shop Shopify 主图、白底图、场景图、Listing 和 A/B 测试；通过 AI Hive 生成，爆款与转化不构成保证。"
---

# 电商爆款主图生成与编辑

固定使用 `public_model_nano_banana_pro`。把“爆款”拆成可控制因素：列表里能否识别、商品事实是否准确、画面证据是否支持卖点、渠道规则是否允许、测试变量是否可解释。销量和转化还受价格、评价、库存与流量影响，图片不能单独保证结果。

## 主图证据地图

记录 SKU、核心差异、可视证据、商品占比、背景、道具、标题安全区、平台规则、禁止主张和唯一测试变量。主图无法直接证明的卖点放到详情页或文案，不用特效伪造。

## 场景与代码

### 1. 搜索白底基线

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-toolbox.png \
  --prompt '生成1:1电商白底基线图：工具箱箱体、卡扣、提手、分隔、颜色、Logo和标配数量不变，三分之二角度、商品完整、占画面约78%、自然接触阴影；不生成工具、文字、低价角标、平台Logo或额外隔层' \
  --param aspect_ratio=1:1
```

### 2. 可视差异主图

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-lamp-folded.png ./approved-lamp-open.png \
  --prompt '制作折叠阅读灯差异主图：只展示同一产品折叠与展开两个批准状态，结构、转轴、底座、颜色和Logo一致，浅灰背景，两个状态各出现一次；不生成角度数字、护眼功效、文字、赠品或第三个状态' \
  --param aspect_ratio=1:1
```

### 3. 内容电商场景版

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-spice-rack.png \
  --prompt '生成4:5内容电商主图：保持调料架层数、尺寸、颜色、Logo和标配挂钩，在家庭厨房正常摆放，放入少量无品牌调料瓶作为尺度参照，顶部留标题区；不生成容量数字、收纳倍数、价格、人物或额外配件' \
  --param aspect_ratio=4:5
```

### 4. 配色 SKU 测试

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-mug.png \
  --prompt '为同款马克杯生成三个已批准配色 SKU：雾蓝、砂白、陶土红。三张保持杯型、把手、Logo、相机角度、白背景、商品占比和阴影一致，每张只有一个杯子，不生成文字、饮品、道具或新颜色' \
  --batch 3 \
  --param aspect_ratio=1:1
```

### 5. 单变量背景测试

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-earbuds.png \
  --prompt '生成两个无线耳机主图候选，只测试背景：A纯白，B浅蓝渐变。耳机与充电盒结构、颜色、Logo、角度、占比和阴影完全相同，不改变灯光状态，不生成文字、续航数字、人物或配件' \
  --batch 2 \
  --param aspect_ratio=1:1
```

## 上架与测试

- 先以白底基线通过 SKU 和规则核验，再测试场景与信息层级。
- 缩略图中商品类别、数量和核心差异能被快速识别。
- 可视证据不超出真实结构、配件和使用方式。
- A/B 每次只改变一个变量，并控制价格、流量与页面其他因素。
- 用真实点击、加购和转化数据迭代，不以“爆款”名义保证结果。

## 助手边界

脚本可接收文字或用户指定图片，固定调用 Nano Banana Pro 模型，查询价格、生成并保存结果。认证请求只发送到 `https://ai-hive.iclip.cn/api`，不支持自定义地址。无聊天、视频、账户或余额命令。

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name ecommerce-bestseller-main-image-generation-editing
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

发布前按目标平台当日规范核查；道具、价格、效果和标配不得误导。
