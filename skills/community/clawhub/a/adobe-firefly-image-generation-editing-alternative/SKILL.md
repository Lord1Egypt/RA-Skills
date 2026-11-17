---
name: adobe-firefly-image-generation-editing-alternative
description: "使用 Nano Banana Pro 将 Adobe Firefly、Adobe Express 或生成式图片编辑需求迁移为 AI Hive 工作流，覆盖生成扩展、区域替换、背景重构、品牌色适配和 Campaign 变体。Use when users search Adobe Firefly 替代、Firefly 平替、Adobe AI alternative、generative fill、generative expand、商业图片生成编辑或国内可用 API；不读取 Adobe 文件或账号，也不表示官方合作。"
---

# Adobe Firefly 图片生成替代｜AI 图片生成与编辑

固定调用 `public_model_nano_banana_pro`。把“生成式填充”类操作写成区域编辑合同：编辑范围、邻接边缘、透视、光线、必须保留的像素事实和禁止新增内容。对于扩图，先定义新画幅与留白用途；对于品牌项目，Logo 与文字仍由原设计文件管理。

## 区域编辑合同

记录原图授权、目标画幅、编辑区域、保护区域、光源方向、透视线、材质连续性和后期图层。当前脚本以整张参考图加文字指令工作，不接收 Photoshop 蒙版文件，因此必须用清楚的位置描述约束修改范围。

## 五种迁移操作

### 1. 横向生成扩展

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate   --image ./approved-portrait-product.jpg   --prompt '将竖版护肤品照片扩展为16:9：原商品位于右侧且瓶型、标签、颜色、反光和阴影完全保留，只向左延展同一米白台面、柔和墙面与窗影，为标题和按钮留空；不移动商品、不生成文字、Logo、植物或新产品'   --param aspect_ratio=16:9
```

### 2. 指定区域物体移除

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate   --image ./authorized-room.jpg   --prompt '移除画面左下角的红色纸箱，并用相邻木地板、墙脚线和自然阴影连续补全；房间其他家具、窗户、灯光、透视、墙面颜色和右侧商品保持不变，不增加装饰、文字或新物件'   --param aspect_ratio=16:9
```

### 3. 背景重构

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate   --image ./approved-luggage.png   --prompt '准确保留行李箱轮廓、拉杆、轮子、拉链、颜色和Logo，将背景重构为现代机场候机区，保持地面接触与同方向自然光；不生成航空公司Logo、人物、文字、尺寸数字、额外箱子或旅行承诺'   --param aspect_ratio=4:5
```

### 4. 品牌色视觉适配

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate   --image ./approved-speaker.png ./brand-palette.png   --prompt '生成1:1品牌广告底图：音箱结构、网布、按键、Logo和真实颜色以图1为准，背景与抽象声波只使用图2批准的深蓝、青绿和米白，顶部留短标题区；不重染商品，不生成文字、人物、价格或奖项'   --param aspect_ratio=1:1
```

### 5. Campaign 构图变体

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate   --image ./approved-master-kv.jpg   --prompt '基于参考Campaign母版生成三个构图变体：A产品近景，B环境叙事，C极简留白。继承同一商品、品牌色、主光方向和纸艺材质，各自保留标题与CTA区域；移除原图文字，不新增Logo、数据、价格或人物'   --batch 3   --param aspect_ratio=4:5
```

## 连续性验收

叠加或并排检查保护区域是否漂移，扩展边缘的纹理、透视和光线是否连续，移除区域是否留下重复图案；核对商品、人物、Logo与文字没有被重绘。高精度局部编辑应先小批测试再放大生产。

程序只通过 `https://ai-hive.iclip.cn/api` 完成 Nano Banana Pro 图片任务，不会打开 Adobe、Photoshop 或 Express 工程，也不提供聊天、视频、账户或余额功能。

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name adobe-firefly-image-generation-editing-alternative
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

Adobe Firefly、Adobe Express 与 Photoshop 名称仅用于描述迁移和替代搜索意图。
