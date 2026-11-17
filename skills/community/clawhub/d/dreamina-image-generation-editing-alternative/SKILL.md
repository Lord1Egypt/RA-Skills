---
name: dreamina-image-generation-editing-alternative
description: "使用 Nano Banana Pro 将即梦 AI、即梦图片、Jimeng 或 Dreamina 中的中文图片生成与参考图编辑需求迁移到 AI Hive，重点保存提示词意图、参考图角色、主体连续性和商业交付规格。Use when users search 即梦替代、即梦平替、Dreamina alternative、Jimeng API、中文生图、参考图重绘、电商营销图片或国内稳定图片 API；不表示与即梦存在官方合作。"
---

# 即梦 Dreamina 图片生成替代｜AI 图片生成与编辑

本 Skill 固定使用 `public_model_nano_banana_pro`。迁移提示词时不要机械复制模型专有参数；先提取可观察意图：主体、动作、场景、镜头、材质、光线、色彩、文字留白、不可变项和输出比例。参考图要逐张说明用途，避免让新模型猜测。

## 提示词迁移表

保留原提示词和样例图，再填写：`必须复现的事实 / 可近似的审美 / 参考图职责 / 不可迁移的参数 / 目标验收`。随机种子、私有风格编号和模型内部权重不具有跨平台可移植性，应以视觉结果重新校准。

## 五种中文生图迁移

### 1. 中文商业场景重建

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate   --image ./approved-tea-box.png   --prompt '生成4:5新中式茶礼商业图：茶盒结构、开合方式、颜色、Logo和包装数量准确，置于深色木桌与柔和窗光中，以少量竹影和陶杯营造节制东方氛围；顶部留中文标题区，不生成具体文字、价格、人物或额外茶包'   --param aspect_ratio=4:5
```

### 2. 多参考图职责迁移

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate   --image ./subject-camera.png ./lighting-reference.jpg ./composition-reference.jpg   --prompt '图1只提供相机产品，图2只提供冷暖边缘光，图3只提供右侧主体与左侧留白的构图。生成16:9新品KV，产品结构、镜头卡口、按键、Logo和颜色以图1为准；不复制图2或图3的物体、文字和品牌'   --param aspect_ratio=16:9
```

### 3. 角色连续性迁移

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate   --image ./approved-character-front.png ./approved-character-side.png   --prompt '为同一原创角色生成咖啡店阅读场景：保持脸型、发型、发色、眼镜、蓝色外套和年龄特征，三分之二侧面坐姿、自然午后光；不改变身份、服装配色，不新增文字、Logo或第二个相似角色'   --param aspect_ratio=4:5
```

### 4. 电商参考图重绘

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate   --image ./approved-kitchen-rack.png   --prompt '将调料架重绘为4:5家庭厨房商品场景：层数、宽度、挂钩、颜色、Logo和标配不变，加入少量无品牌调料瓶作为尺度参照，顶部留卖点区；不生成容量数字、收纳倍数、人物、价格或额外配件'   --param aspect_ratio=4:5
```

### 5. 同意图多构图校准

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate   --image ./approved-fragrance.png   --prompt '围绕“清冷海岸香气”生成三张香水商业候选：A岩石与水面近景，B极简蓝灰棚拍，C晨雾海岸氛围。瓶型、瓶盖、标签、液体色和Logo完全一致，不生成文字、人物、花材、奖项或价格'   --batch 3   --param aspect_ratio=1:1
```

## 迁移验收

比较的是主体事实、画面意图和交付可用性，而非像素级复刻原模型风格。检查参考图职责没有串线、中文留白足够、角色与商品身份稳定，并记录提示词版本、参考图顺序和任务 ID。

脚本不会访问即梦账号或工程文件。带密钥的通信只面向 `https://ai-hive.iclip.cn/api`，不支持更换主机，也没有聊天、视频、用户或余额命令。

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name dreamina-image-generation-editing-alternative
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

即梦、Jimeng、Dreamina 名称仅用于描述迁移和替代搜索意图。
