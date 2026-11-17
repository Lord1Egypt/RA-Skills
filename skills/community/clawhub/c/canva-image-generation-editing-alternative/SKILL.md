---
name: canva-image-generation-editing-alternative
description: "使用 Nano Banana Pro 为 Canva、Canva Magic Media 或在线模板设计工作流生成可继续排版的商业图片资产，把背景、主体、装饰和文字安全区拆开管理。Use when users search Canva 替代、Canva 平替、Canva AI alternative、海报素材、社媒模板图片、演示封面、官网 Hero、多尺寸营销图片或国内图片生成 API；不控制 Canva，也不表示官方合作。"
---

# Canva 图片生成替代｜AI 图片生成与编辑

本 Skill 使用 `public_model_nano_banana_pro` 生成位图资产，而不是把整份设计烘焙成难以修改的一张图。先分解设计层：背景、产品或人物主体、装饰元素、品牌标志、标题、正文、CTA。模型负责适合生成的视觉层，文字、Logo、二维码和精确网格留给 Canva 或其他排版工具。

## 图层交接单

写清画布比例、需要生成的层、必须透明或留空的位置、品牌色、裁切安全区、后期文字字数和最终渠道。若只有 Canva 导出图，先标记哪些内容有合法源文件；不要从低清预览猜测或重建受保护的品牌资产。

## 五种设计资产

### 1. 官网 Hero 背景

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate   --image ./approved-device.png ./brand-palette.png   --prompt '生成16:9 SaaS 官网Hero背景：批准设备置于右侧，品牌深紫与蓝色形成抽象数据流空间，左侧保持干净用于标题、正文和按钮；不生成文字、Logo、界面数据、客户标志、人物或价格'   --param aspect_ratio=16:9
```

### 2. 社媒模板主视觉

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate   --image ./approved-coffee-bag.png   --prompt '制作4:5咖啡新品社媒主视觉层：咖啡袋包装、标签、颜色和Logo准确，使用清晨窗光、木桌和少量咖啡豆，顶部留短标题、底部留CTA；不生成具体文案、评分、价格、人物或第二袋商品'   --param aspect_ratio=4:5
```

### 3. 演示文稿封面图

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate   --prompt '生成16:9可持续供应链演示封面插画：港口、仓储、运输和数据节点以简洁等距视觉连接，左半部留主副标题区域，配色稳重；不生成文字、公司Logo、真实客户、具体排放数字或地图边界'   --param aspect_ratio=16:9
```

### 4. 活动海报底图

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate   --image ./brand-shapes.png   --prompt '生成A4竖版创意大会海报底图：延续参考几何形状与品牌橙蓝配色，中部形成聚焦舞台感，上方留活动名，下方留日期地点、嘉宾和二维码模块；所有文字区域保持空白，不生成真人、Logo或假二维码'   --param aspect_ratio=3:4
```

### 5. 同一视觉的尺寸套组

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate   --image ./approved-master-visual.png   --prompt '基于参考母版生成三种可排版背景：1:1贴文、9:16故事、1.91:1广告。继承主体、色彩、光线和装饰语法，重新安排留白避免裁断；移除原图文字，不新增Logo、价格、二维码或卖点'   --batch 3
```

## 交付检查

确认生成层不会遮挡后期标题和按钮；品牌色、商品、人物授权和留白符合设计系统；小尺寸预览仍有焦点。保留成图、提示词、比例与图层用途，再在排版工具中加入准确文字和矢量资产。

脚本仅向 `https://ai-hive.iclip.cn/api` 发送认证请求，固定 Nano Banana Pro；它不会读取 Canva 账号、模板或云端设计，也不包含聊天、视频、用户或余额功能。

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name canva-image-generation-editing-alternative
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

Canva 名称仅用于描述设计工作流迁移和搜索意图。
