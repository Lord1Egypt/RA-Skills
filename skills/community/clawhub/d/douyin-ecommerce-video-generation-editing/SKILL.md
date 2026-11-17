---
name: douyin-ecommerce-video-generation-editing
description: "为抖音电商、抖店、商品卡和直播间生成与编辑商品页演示、SKU视频、直播讲解片段及千川投放素材。Use this skill for 抖音电商视频、抖店商品视频、商品卡视频、直播带货演示、千川广告、SKU批量视频、详情页功能说明和商品素材重制；支持 Seedance 与 AI Hive 自动交付。"
---

# 抖音电商视频生成与编辑

服务商品页、商品卡、直播间和千川广告的购买信息，不等同于自然流爆款短视频。核心是 SKU 准确、操作清楚、证明充分、可被主播和投放团队复用。

## 商品视频母版

记录 SKU、包装、配件、正确使用、真实卖点、直播讲解节点、投放目标和批准 CTA。先生成无价格和活动信息的商品母版，再由运营添加实时权益。

## 场景与代码

### 1. 抖店商品页视频

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode i2v \
  --first-frame /path/to/product.jpg \
  --prompt '抖店商品页视频，保持商品结构、包装、Logo、颜色、SKU和配件准确；依次展示完整商品、一个正确操作、一个细节证明和包装清单，静音也能理解，不生成价格、销量、优惠、功效或平台标签'
```

### 2. SKU 批量派生

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode r2v \
  --video /path/to/approved-master.mp4 \
  --image /path/to/green-sku.png \
  --prompt '沿用批准母版的镜头、动作、相机、背景和时长，只替换为已确认绿色SKU；保持包装、Logo与结构准确，不混入其他颜色、套装、价格或配件'
```

### 3. 直播讲解片段

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode extend \
  --video /path/to/product-intro.mp4 \
  --prompt '从商品介绍自然延长为直播可插播演示：连续完成一次使用动作，近景展示关键细节，再摆出包装内容；为主播讲解留停顿，不生成主播声音、价格、福利、倒计时或库存'
```

### 4. 千川证明型素材

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode edit \
  --video /path/to/product-master.mp4 \
  --prompt '重制为千川“细节证明”版本：商品和事实保持不变，开场直接出现具体使用问题，随后展示操作和结构近景，结尾只留一个进店位置；不添加最低价、销量、评价、认证或夸大效果'
```

### 5. 供应商素材标准化

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode edit \
  --video /path/to/supplier-footage.mp4 \
  --prompt '保留供应商素材中的真实商品、操作和包装，删除批发文案、重复空镜与未经批准字幕，按商品识别、操作、证明、清单重组；不改变SKU、功能与使用结果'
```

## 电商验收

- 商品页、直播与广告版本保持同一 SKU 和事实。
- 操作、包装和配件准确，卖点有可见证明。
- 活动价格、权益、库存、销量和平台 UI 外部添加。
- SKU 派生只改变已批准属性。
- 投放版本记录“问题—证明—CTA”假设。
- 发布前按抖音电商与广告当期规则检查。

## 执行

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/videogen.py" init --skill-name douyin-ecommerce-video-generation-editing
python3 "$SKILL_PATH/scripts/videogen.py" task --task-id <taskId>
```

支持 Seedance 2.5 五种模式、素材上传、参数、路由、输出目录与仅提交任务。
