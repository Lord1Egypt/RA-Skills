---
name: amazon-listing-image-generation-editing
description: "使用 Nano Banana Pro 规划和生成 Amazon Listing 图片栈，包括主图、功能证据、尺寸、生活方式、使用步骤与包装清单，并保持 ASIN/SKU 事实一致。Use this skill for Amazon Listing 图片生成与编辑、亚马逊主图、Amazon A+、产品图片栈、白底图、infographic、lifestyle image、尺寸图、包装清单和跨境电商素材；通过 AI Hive 生成，提交前复核 Amazon 当前政策。"
---

# Amazon Listing 图片生成与编辑

底层模型锁定为 `public_model_nano_banana_pro`。工作起点不是“做一张好看主图”，而是给整套 Listing 分工：第一张负责准确识别商品，后续画面依次解释功能、尺度、使用情境和箱内物。任何画面说法都必须能回到 ASIN/SKU 资料。

## ASIN 视觉档案

为每个变体保留一页档案：ASIN/SKU、销售站点、主图约束、图位任务、标配清单、尺寸出处、获批表述、后期文字区，以及最后一次政策复核日期。站点要求可能变化，真正上传时仍以 Seller Central 页面为准。

## 五个图位的运行示例

### 1. 白底主图候选

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-pet-carrier.png \
  --prompt '生成 Amazon 白底主图候选：只展示参考宠物航空箱与确认随附的肩带，箱体、网窗、拉链、颜色、Logo和数量不变，商品完整居中、纯白背景、轻阴影；不生成宠物、文字、尺寸线、徽章、场景或非标配物品' \
  --param aspect_ratio=1:1
```

### 2. 功能证据辅助图

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-tool-bag.png \
  --prompt '生成工具包辅助图：保持包型、口袋、拉链、颜色和Logo，打开显示实际内部分区，周围留三个功能标签区域；只使用确认可见结构，不生成文字、容量数字、工具赠品、防水测试或额外口袋' \
  --param aspect_ratio=1:1
```

### 3. 尺寸信息底图

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-lamp.png \
  --prompt '生成台灯尺寸辅助图底图：产品结构、转轴、底座、颜色和Logo不变，正侧视角清楚，预留高度、底座直径和灯臂长度的尺寸线与单位区域；不生成具体数字、文字、功能图标或改变比例' \
  --param aspect_ratio=1:1
```

### 4. 生活方式场景

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-picnic-cooler.png \
  --prompt '生成保冷包生活方式辅助图：保持包体、肩带、拉链、颜色、Logo和真实容量，在公园桌面正常使用，旁边只放少量无品牌饮料作为尺度参照；不生成保冷时长、温度数字、家庭身份、文字、额外商品或平台Logo' \
  --param aspect_ratio=1:1
```

### 5. 包装清单

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-massage-gun-kit.png \
  --prompt '生成按摩枪包装清单图：只展示确认包含的主机、四个按摩头、充电线和收纳盒，各一次、比例真实、白到浅灰背景，右侧留清单文字区；不生成医疗功效、说明文字、额外按摩头、适配器或认证' \
  --param aspect_ratio=1:1
```

## 上线门槛

- 分开审查首图、辅图与 A+，不可拿同一套标准笼统放行。
- 实物轮廓、颜色、商标、随箱物与变体档案逐项对上。
- 所有尺度、性能、比较内容都有可定位的内部来源。
- 各图位回答不同问题，连续浏览时不存在无意义重复。
- 归档政策复核日、成图版本、生成任务号和批准人。

## 接口权限

可以从文字起稿，也可以接收卖家明确提供的参考图片；返回结果来自 Nano Banana Pro。带认证信息的网络访问仅面向 `https://ai-hive.iclip.cn/api`，调用方无法改成别的主机。程序没有聊天、视频、账户查询或余额功能。

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name amazon-listing-image-generation-editing
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

Amazon 名称仅描述使用平台，不表示官方合作；政策以当前 Seller Central 为准。
