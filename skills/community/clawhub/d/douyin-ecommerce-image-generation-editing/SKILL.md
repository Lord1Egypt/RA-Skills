---
name: douyin-ecommerce-image-generation-editing
description: "为抖音电商、抖店和直播间生成与编辑商品卡主图、SKU图、卖点证明图、直播商品贴片及千川广告图片。Use this skill for 抖音电商图片、抖店商品图、商品卡、直播带货图片、千川测图、SKU套图、商品详情、换背景和电商广告素材；支持参考图保真与 AI Hive 自动生成。"
---

# 抖音电商图片生成与编辑

服务抖音电商的购买界面，而不是普通短视频封面：商品卡要准确识别 SKU，详情图要证明卖点，直播贴片要在小尺寸中快速辨认，千川素材要能测试明确的点击假设。

## 商品事实层

整理商品、包装、SKU、颜色、配件、真实卖点、使用步骤、批准文案和禁止表达。价格、优惠、库存、销量、平台按钮与直播机制由运营在正式系统中添加，不能生成进图片。

## 场景与代码

### 1. 抖店商品卡主图

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '抖店商品卡方形主图，严格保留参考商品结构、包装、Logo、颜色、SKU和配件；商品完整居中，在手机小尺寸中仍清晰，背景简洁，阴影真实，不添加价格、优惠券、销量、认证、平台标签或未提供文字' \
  --image /path/to/product-front.png \
  --image /path/to/package.png
```

### 2. 商品详情卖点证明图

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '生成3张抖音电商详情图：真实使用动作、关键结构近景、包装清单；保持同一商品和品牌色，每张只证明一个已提供卖点，预留短文字区，不生成参数、功效、对比结果或赠品' \
  --image /path/to/product.png \
  --batch 3
```

### 3. 直播商品贴片

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '抖音直播商品贴片底图，准确SKU占主要区域，包装与核心结构清楚，竖版紧凑构图，为运营批准的品名和权益保留两个信息区；不生成到手价、倒计时、库存、销量、优惠券或直播按钮' \
  --image /path/to/sku.png
```

### 4. 千川商品图测试

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '为同一抖店商品生成4个千川图片假设：使用痛点、操作动作、材质证明、适合人群；商品与品牌系统保持一致，每版只有一个点击理由和一个文案留白，不只改变滤镜，不生成低价、销量或夸张效果' \
  --image /path/to/product.png \
  --batch 4
```

### 5. SKU 系列统一

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '沿用批准的商品卡母版，生成米白、墨绿和深灰三个真实SKU；锁定相机、尺度、结构、包装、Logo、背景和阴影，只改变已确认颜色，每张只出现一个SKU' \
  --image /path/to/master-sku.png \
  --batch 3
```

## 电商验收

- 商品卡、详情图和直播贴片中的 SKU 完全一致。
- 包装、Logo、颜色、配件和使用动作准确。
- 小尺寸能识别商品，不依赖复杂文字。
- 价格、权益、库存、销量和平台 UI 由运营后期添加。
- 千川版本记录创意假设，不制造伪差异。
- 发布前按抖音电商和广告账户当期规则检查。

## 执行

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name douyin-ecommerce-image-generation-editing
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

固定调用 `public_model_nano_banana_pro`。支持多参考图、批量、实时参数、路由、输出目录和仅提交任务。
