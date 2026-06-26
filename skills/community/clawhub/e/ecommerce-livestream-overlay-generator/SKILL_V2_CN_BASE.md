---
name: 生成电商带货直播间全套贴片
description: >
  直播间装修贴片全自动生成。
  根据品牌、商品和活动信息，或直接根据商品图片，自动生成完整直播间视觉套装：
  背景图、标题横卡、人物、促销竖卡、桌面商品贴、权益下贴。
  支持绿幕抠图、自动合成预览、打包交付。
---

# 直播间装修贴片生成 Skill

## 一、前置条件

### 依赖
- Python 3 + Pillow + opencv-python-headless + numpy
- 火山方舟 API Key

### 安装依赖
```bash
pip3 install Pillow==12.2.0 opencv-python-headless==4.13.0 numpy==2.3.2
```

## 二、需求确认（正式生成前必须执行）

> ⚠️ 收到用户生成请求后，不要立即开始生成图片。先确认以下信息，确保一次性出图到位。

### 2.1 必须确认的信息

| 信息 | 说明 | 必填 |
|------|------|------|
| 品牌 | 如 戴森、茅台、三只松鼠等 | ✅ |
| 主推商品 | 具体品名和型号 | ✅ |
| 促销活动 | 满减、买赠、积分兑换等具体内容 | ✅ |
| 风格偏好 | 如有特殊要求（颜色、氛围、调性） | ❌ |

### 2.2 确认流程

1. **用户已提供完整信息** → 列出理解的需求摘要，请用户确认后直接开始
2. **用户信息不完整** → 只追问缺失的必要信息，其他自动推导
3. **用户只发了商品图片没文字** → 识别图中商品，推测品牌和品类，列出理解的需求摘要请用户确认
4. **用户说"按案例来"/"照着做"** → 直接用下方案例的需求生成

### 2.3 需求确认示例回复

```
我确认一下需求：

📋 **品牌**：戴森
📋 **主推商品**：戴森Supersonic HD16吹风机 + Airwrap多功能美发棒
📋 **促销活动**：满3000减300
📋 **买赠**：买吹风机送两支造型风嘴
📋 **包装**：直播间限定礼盒包装
📋 **风格**：科技奢华风（根据戴森品牌推导）

文案我这样设计：
- 主标题：「Dyson·沙龙级造型」
- 副标题：「限定礼盒·奢宠体验」
- 促销竖卡：「满3000立减300 / 买吹风机送造型风嘴 / 直播间限定礼盒」
- 权益：「两年质保无忧 / 顺丰包邮到家 / 专属礼盒包装」

确认OK的话我就开始生成了，有想调整的随时说 👇
```

### 2.4 需求描述案例（首次触发时主动展示）

> 收到用户的生成请求后，主动展示以下案例，让用户可以照着描述或直接要求按案例生成。

**示例需求描述**：
> 做一套戴森吹风机直播间贴片，主品是戴森Supersonic HD16吹风机和Airwrap多功能美发棒，买吹风机送两支造型风嘴，满3000减300，直播间限定礼盒包装

**首次回复模板**：
```
你可以直接告诉我你的品牌和促销信息，比如：

> 做一套戴森吹风机直播间贴片，主品是戴森Supersonic HD16吹风机和Airwrap多功能美发棒，买吹风机送两支造型风嘴，满3000减300，直播间限定礼盒包装

也可以直接说「按戴森案例来」，我就直接用这个需求生成。

你的需求是什么？
```

**最低限度只需提供**：品牌 + 主推商品 + 促销活动（三个核心信息）
**文案、风格色调、人物造型、权益**均由 AI 自动推导生成，用户可选择性修改。

## 三、文案自动生成规则

### 3.1 主标题
- 必须含品牌名并具有氛围感
- **禁用**"官方""旗舰"等字样
- 不能直接写商品名，要有宣传感和下单欲望

### 3.2 副标题
- 核心利益点（福利/功效/场景）或正在进行的活动
- 简洁有力

### 3.3 促销竖卡
- 根据促销活动拆分为 2-3 层
- 每层包含：金额/权益 + 使用条件

### 3.4 权益文案
- 通常 3 个：赠品相关 + 正品保障 + 物流/售后
- ⚠️ 避免使用"正品""保障"等触发审核的词，替换为"品质""保证"

## 四、组件清单与尺寸

> ⚠️ 尺寸已根据 `doubao-seedream-4-5-251128` 的最低像素限制调整

| # | 组件 | 尺寸 | 绿幕 | 说明 |
|---|------|------|------|------|
| 1 | 背景图 | **1440×2560** | ❌ | C4D 场景 |
| 2 | 标题横卡 | **3328×1109** | ✅ | 异形贴纸 |
| 3 | 人物 | **1440×2560** | ✅ | 素颜+幼态脸+精致造型（不用手持商品） |
| 4 | 促销竖卡 | **1920×1920** | ✅ | 正方形异形贴纸 |
| 5 | 桌面商品贴 | **3328×1109** | ✅ | 40+单品密集排列 |
| 6 | 权益下贴 | **3328×1109** | ❌ | 铺满底部 |

## 五、Prompt 写法标准

### 核心原则
- 所有组件使用统一风格前缀确保色调一致
- 必须包含反向约束条件
- 背景图使用"纯色均匀绿色背景"（不是#00FF00）

### 5.1 背景图 Prompt
**约束**：无文字、无人物、无产品。

**模板**：
```
这是一幅融合[风格描述]的C4D商业空间场景。空间以[主色调]为主色调，搭配[辅助色]作为辅助色，点缀以[点缀色]的细节元素，整体被[中性色]所平衡。空间结构呈现出[结构描述]，营造出[氛围]的氛围。灯光设计[灯光描述]，突显出空间的质感与层次。材质上运用了[材质]，展现出[风格]的魅力。布局上，模块化的抽象展示元素散落其中，如[元素1]、[元素2]和[元素3]，共同营造出一种[整体感受]的空间体验。
```

### 5.2 标题横卡 Prompt
**模板**：
```
纯色均匀绿色背景#00FF00。画面正中是一个[颜色]渐变的异形横条卡片，卡片有[边框质感]，四边是不规则的艺术形状。卡片内部左侧[文字区域底色]，大字「[主标题]」用[字体描述]，下方「[副标题]」用[字体描述]。卡片右侧是[产品插画描述]。整个卡片颜色浓郁厚重，绝对没有白色底色区域，不要任何绿色青色蓝绿色。卡片是一个完整的实体贴纸，边界清晰。
```

### 5.3 人物 Prompt

> ⚠️ 核心规则（v2 更新）：
> 1. **人物模型用 `doubao-seedream-5-0-260128`**（其他组件仍用 `doubao-seedream-4-5-251128`）
> 2. **完全不化妆的素颜**（不是"清透裸妆"）
> 3. **不手持商品**，双手自然下垂微曲（v2 取消了手持商品）
> 4. **网红幼态脸短中庭**，眼部轮廓深邃有水润感，唇部有果冻感水润饱满
> 5. **服装必须提前设计好**，prompt 中完整描述上衣+下装（不含鞋子）+ 配饰
> 6. **发色尽量黑色**，发质柔顺有光泽，发型精致可加配饰，符合品牌调性
> 7. 背景用"纯色均匀绿色"（不是#00FF00）

**模板**：
```
纯色均匀绿色背景，颜色绝对均匀纯净无渐变无纹理无阴影无光斑无杂色。竖版人像，人物站立面对镜头，取景从头顶到大腿中段，人物位于画面中央且占据画面大部分面积，头顶距画面顶部很近。25岁年轻漂亮女主播，完全不化妆的素颜，冷白皮白皙通透肌肤，网红幼态脸短中庭，{眼型描述}，眼部轮廓深邃有水润感，{眼周描述}，唇部{唇型描述}有果冻感水润{唇色描述}，{气质描述}。完全不化妆素颜出镜，面部没有任何妆容，没有任何眼影眼线睫毛膏腮红口红粉底，完全素净的面容。身穿{上衣描述}，下身穿{下装描述}，{配饰描述}。{发型发色描述}，{发型配饰描述}。正面柔和均匀灯光。人物自然站立，双手自然下垂微曲，姿态放松优雅。
```

**面孔差异化（必须每次指定以下维度）**：

| 维度 | 说明 | 示例 |
|------|------|------|
| 脸型 | 网红幼态脸短中庭（固定） | 心形脸/鹅蛋脸/瓜子脸/方圆脸 |
| 眼型 | 圆眼/丹凤眼/杏眼/桃花眼 | 需描述"微微下垂显无辜感"或"细长微微上挑"等 |
| 眼部水润感 | 固定要求 | "眼部轮廓深邃有水润感，眼周皮肤细腻透亮" |
| 唇部果冻感 | 固定要求 | "饱满嘟嘟唇有果冻感水润透亮" / "薄唇自然淡粉色有果冻感" |
| 气质 | 甜美亲和/清冷高级/知性优雅/元气活泼/自信从容 | 每个品牌不同 |
| 服装 | 必须提前设计，上衣+下装+配饰 | 不含鞋子 |
| 发型 | 必须提前设计，黑色为主+配饰 | 柔顺有光泽，精致有设计感 |

**人物造型设计示例（v2 版）**：

兰蔻菁纯：
```
网红幼态脸短中庭，眼型圆眼微微下垂显无辜感，眼部轮廓深邃有水润感，眼周皮肤细腻透亮，唇部饱满嘟嘟唇有果冻感水润透亮，五官精致甜美亲和。身穿白色细针织短款开衫，内搭米白色蕾丝吊带，下身穿高腰浅粉色百褶缎面半裙，胸前戴一条玫瑰金细锁骨链，左手腕戴一只玫瑰金细手镯，右手戴一枚简约珍珠戒指。黑色长直发柔顺有光泽披落至锁骨下方，头顶偏右侧夹一个珍珠小发夹，几缕碎发自然垂落在脸颊两侧修饰脸型。
```

赫莲娜黑绷带：
```
网红幼态脸短中庭，丹凤眼细长微微上挑，眼部轮廓深邃有水润感，眼尾自带清冷高级感，唇部薄唇自然淡粉色有果冻感水润，五官偏清冷高级感。身穿黑色高领修身真丝衬衫，袖口挽至手肘处露出纤细手腕，下身穿黑色高腰阔腿西装裤，左侧耳垂戴一颗两克拉钻石耳钉，右手腕戴一条极细银色手链。黑色长直发柔顺有光泽中分后自然垂落至背部中央，右侧太阳穴旁别一枚黑色极细发簪造型简约利落。
```

海蓝之谜：
```
网红幼态脸短中庭，杏眼明亮圆大，眼部轮廓深邃有水润感，眼神温柔灵动有灵气，唇部标准唇有果冻感自然粉润水润饱满，五官柔和清透。身穿珍珠白色丝缎面宽松衬衫，领口微微解开一颗扣子露出精致锁骨，袖口蓬松泡泡袖设计，下身穿香槟色高腰缎面阔腿长裤，颈间戴一条极细香槟金项链配一颗小珍珠吊坠，左手腕戴一只白玉细手镯。黑色长卷发柔顺有光泽自然大波浪卷披落至肩胛骨，头顶编一个松散的精致法式麻花辫从左侧垂落，发间点缀几颗极小的珍珠发扣。
```

### 5.4 促销竖卡 Prompt
> ⚠️ 尺寸从 896×1344 改为 **1920×1920**（正方形）

**模板**：
```
纯色均匀绿色背景#00FF00。画面正中是一个紧凑的竖向异形标签贴纸，整体为[深色系]实心底色，没有任何白色区域、没有任何浅色区域、没有任何渐变到白色的部分，不要任何绿色青色蓝绿色。贴纸形状为圆角矩形加顶部弧形装饰。顶部有[装饰元素]。大字「[大标题]」用[字体描述]；下方分三层：「[内容1]」「[内容2]」「[内容3]」。整个贴纸颜色浓郁深实，边界清晰锐利，是一个实心异形贴纸。贴纸占据画面约40%面积，紧凑不松散。
```

### 5.5 桌面商品贴 Prompt（⚠️ 与原始 skill 完全不同）

> ⚠️ 关键区别：
> 1. **白色哑光大理石展示桌面**（不是纯绿底+白平面）
> 2. **分层聚核+左右镜像+前后递进**布局逻辑
> 3. **商品总数至少40个以上单品**（不是"丰富一些"）
> 4. 中层核心区分左中右三块，中心区视觉焦点

**模板**：
```
背景为纯色均匀绿色背景。画面正下方是一张正面平放的白色高级展示桌面（白色哑光大理石质感），桌面完全水平不倾斜，桌面宽阔占满画面底部40%高度。桌面上产品按分层聚核加左右镜像加前后递进逻辑摆放，商品总数至少40个以上单品，密集排列覆盖绝大部分桌面面积：【中层核心展示区分左中右三块】中心区视觉焦点：放置{产品布局描述}【整体布局要求】所有产品竖立放置正面朝向观众。高度差控制形成阶梯状层次。左右区与中心区之间各留适当空白间距保证呼吸感。桌面产品密集饱满，商品总数至少40个以上单品。除了商品和白色哑光金属陈列架外不要出现任何其他内容，绝对不要出现人的手、手指、手臂、人体任何部位，不要出现人和手。光线均匀自然。这是一个纯静物产品陈列照片，没有任何人参与。
```

> ⚠️ prod_layout 里**不能出现"最前方留手持位"**——手持商品是人物图的事，桌面商品贴是纯产品陈列

### 5.7 用户商品图（可选）

当用户提供真实商品照片时：

**a) 去背景**：根据商品图的背景类型选择策略

| 商品背景 | 去背景方法 |
|---------|-----------|
| 白色/浅色纯色背景 | HSV 阈值去除白色区域 |
| 深色纯色背景 | HSV 阈值去除对应深色 |
| 复杂场景背景 | GrabCut 或 Rembg |

```python
import cv2
import numpy as np

def remove_white_bg(img_path, output_path):
    """去除白色/浅色背景"""
    img = cv2.imread(img_path)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask_w = cv2.inRange(hsv, np.array([0, 0, 200]), np.array([180, 30, 255]))
    mask_g = cv2.inRange(hsv, np.array([0, 0, 160]), np.array([180, 50, 240]))
    mask = cv2.bitwise_or(mask_w, mask_g)
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, k, iterations=5)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, k, iterations=3)
    mask = cv2.GaussianBlur(mask, (5, 5), 0)
    mask = (mask > 200).astype(np.uint8) * 255
    b, g, r = cv2.split(img)
    cv2.imwrite(output_path, cv2.merge([b, g, r, 255 - mask]))
```

**b) 桌面商品贴 Prompt 调整**：中心区留白，供用户商品图叠加

```
在原有的桌面商品贴 prompt 中，将中心区描述改为：
"中心区域留出足够的空白空间用于放置主推商品（大约占中心30%面积保持干净），
周边按分层聚核加左右镜像加前后递进逻辑摆放配套产品"
```

**c) 合成时叠加**：用户商品图缩放后放在产品区域中心偏上

```python
# 用户商品图：缩放到画面宽度25%，放在产品区域中心
up_target_w = int(cw * 0.25)
ups = up_target_w / user_product.width
up_resized = user_product.resize((int(user_product.width * ups), int(user_product.height * ups)), Image.LANCZOS)
upx = (cw - up_resized.width) // 2
upy = pdy + int(pdr.height * 0.05)  # 略高于产品区域顶部

# 在 paste 顺序中，用户商品图在桌面商品贴之后、标题横卡之前
canvas.paste(pdr, (0, pdy), pdr)
canvas.paste(up_resized, (upx, upy), up_resized)  # ← 用户商品图
canvas.paste(tr, (tx, ty), tr)
```

**d) 新增交付物**：

| 文件名 | 说明 |
|--------|------|
| 用户商品图.png | 去背景后的用户商品图，已定位到画布坐标 |

### 5.6 权益下贴 Prompt
**模板**：
```
左右对称构图，平视视角。核心元素呈现在上半部分：三个简单权益图标，下方对应文字「[权益1] / [权益2] / [权益3]」。背景[背景描述]。风格：平面，光影简约。色彩：[主色]，简洁大方。
```

## 六、生图 API

| 项目 | 内容 |
|------|------|
| 地址 | `https://ark.cn-beijing.volces.com/api/v3/images/generations` |
| 方式 | POST |
| Content-Type | application/json |
| **通用模型** | **`doubao-seedream-4-5-251128`** |
| **人物模型** | **`doubao-seedream-5-0-260128`**（仅人物组件用此模型） |

### 请求参数
```json
{
  "model": "doubao-seedream-4-5-251128",
  "stream": false,
  "watermark": false,
  "sequential_image_generation": "disabled",
  "prompt": "<中文prompt>",
  "size": "<宽>x<高>"
}
```

### 请求示例
```bash
curl -s "https://ark.cn-beijing.volces.com/api/v3/images/generations" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <API_KEY>" \
  -d '{
    "model": "doubao-seedream-4-5-251128",
    "stream": false,
    "watermark": false,
    "sequential_image_generation": "disabled",
    "prompt": "prompt内容",
    "size": "1440x2560"
  }'
```

## 七、绿幕抠图

对组件 2（标题横卡）、3（人物）、4（促销竖卡）、5（桌面商品贴）执行绿幕去除。

```python
import cv2
import numpy as np

def remove_green(img_path, output_path):
    img = cv2.imread(img_path)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask1 = cv2.inRange(hsv, np.array([35, 80, 80]), np.array([85, 255, 255]))
    mask2 = cv2.inRange(hsv, np.array([30, 40, 120]), np.array([90, 255, 255]))
    mask = cv2.bitwise_or(mask1, mask2)
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, k, iterations=3)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, k, iterations=2)
    mask = cv2.GaussianBlur(mask, (3, 3), 0)
    mask = (mask > 127).astype(np.uint8) * 255
    b, g, r = cv2.split(img)
    rgba = cv2.merge([b, g, r, 255 - mask])
    cv2.imwrite(output_path, rgba)
```

## 八、合成预览

> ⚠️ 布局参数与原始 skill 完全不同

### 布局参数

```python
layout = {
    "title":   {"scale": 0.95, "pos": "center-top", "y_pct": 0.07},
    "person":  {"scale": 0.70, "pos": "left", "x_pct": 0.15, "y_pct": 0.14},
    "promo":   {"scale": 0.40, "pos": "right", "x_pct": 0.55, "y_pct": 0.22},
    "product": {"zoom": 1.2,  "pos": "bottom-full", "above": "benefit"},
    "benefit": {"scale": 1.0,  "pos": "bottom-full"},
}
```

### 合成代码

```python
from PIL import Image

def compose_preview(bg_path, person_nobg, title_nobg, promo_nobg, product_nobg, benefit_path, output_path):
    bg = Image.open(bg_path).convert("RGBA")
    cw, ch = bg.size

    def fit(img, w_ratio, center=True):
        w = int(cw * w_ratio)
        s = w / img.width
        r = img.resize((w, int(img.height * s)), Image.LANCZOS)
        x = (cw - w) // 2 if center else cw - w
        return r, x

    def fit_full(img):
        s = cw / img.width
        return img.resize((cw, int(img.height * s)), Image.LANCZOS)

    def zoom_crop(img, zoom):
        w = int(cw * zoom)
        s = w / img.width
        h = int(img.height * s)
        r = img.resize((w, h), Image.LANCZOS)
        cx = (w - cw) // 2
        return r.crop((cx, 0, cx + cw, h))

    title = Image.open(title_nobg).convert("RGBA")
    person = Image.open(person_nobg).convert("RGBA")
    promo = Image.open(promo_nobg).convert("RGBA")
    product = Image.open(product_nobg).convert("RGBA")
    benefit = Image.open(benefit_path).convert("RGBA")

    tr, tx = fit(title, 0.95); ty = int(ch * 0.07)
    prr, prx = fit(promo, 0.40, center=False); prx = int(cw * 0.55); pry = int(ch * 0.22)
    per, perx = fit(person, 0.70); perx = int(cw * 0.15); pery = int(ch * 0.14)
    pdr = zoom_crop(product, 1.2); pdy = ch - fit_full(benefit).height - pdr.height
    bfr = fit_full(benefit); bfy = ch - bfr.height

    # 图层顺序：背景 → 促销竖卡 → 人物 → 桌面商品贴 → 标题横卡 → 权益下贴
    # 若需标题在人物下层，将 tr 的 paste 调到 per 之前即可
    # 示例（标题在人物下方）：canvas.paste(prr,...); canvas.paste(tr,...); canvas.paste(per,...)
    canvas = bg.copy()
    canvas.paste(prr, (prx, pry), prr)
    canvas.paste(per, (perx, pery), per)
    canvas.paste(pdr, (0, pdy), pdr)
    canvas.paste(tr, (tx, ty), tr)
    canvas.paste(bfr, (0, bfy), bfr)

    canvas.convert("RGB").save(output_path, "JPEG", quality=95)
```

### 后处理：人物提亮

合成前对人物图层单独提亮，避免合成后人物偏暗：

```python
from PIL import ImageEnhance

# 在合成前对人物图层提亮17%
person_bright = ImageEnhance.Brightness(person).enhance(1.17)
# 后续合成使用 person_bright 代替 person
```

> ⚠️ 只提亮人物图层（17%），不动其他图层。最终交付的人物.png 也使用提亮后的版本。

## 九、打包交付

### 交付文件（固定7个）

| 文件名 | 格式 | 说明 |
|--------|------|------|
| 背景.png | PNG 1440×2560 | 全铺 |
| 标题横卡.png | PNG 1440×2560 透明 | 内容在预览位置 |
| 人物.png | PNG 1440×2560 透明 | 已提亮处理（不标注"提亮"） |
| 促销竖卡.png | PNG 1440×2560 透明 | 内容在预览位置 |
| 桌面商品贴.png | PNG 1440×2560 透明 | 内容在预览位置 |
| 权益下贴.png | PNG 1440×2560 透明 | 内容在预览位置 |
| 预览.jpg | JPG 1440×2560 | 合成预览效果 |

若提供了用户商品图，该商品图会合成到桌面商品贴的中心区域，不单独输出。

### 交付方式（二选一，自动判断）

**方式一：对话内直接发送（当通道支持文件发送时）**
1. 先发送预览图（`预览.jpg`）到对话
2. 再发送压缩包（命名为「{品牌名}直播间_全套贴图.zip」，内含上述7个文件）

```bash
cd output/
zip -j "../{品牌名}直播间_全套贴图.zip" 背景.png 标题横卡.png 人物.png 促销竖卡.png 桌面商品贴.png 权益下贴.png 预览.jpg
```

**方式二：桌面文件夹（当通道不支持文件发送时）**
1. 在用户桌面创建文件夹，命名为「{品牌名}直播间贴片」
2. 文件夹内只放上述7个文件，不包含中间文件、不包含压缩包
3. 用 `open` 命令直接打开预览图，让用户看到效果
4. 用 `open` 命令直接打开文件夹，让用户浏览文件

> ⚠️ 注意：webchat（Control UI）当前不支持文件发送，走方式二。飞书、微信等走方式一。

## 十、完整工作流

```
1. 收集需求（品牌、促销活动、可选：用户商品图）
2. 分析品牌风格 → 确定色调
3. 为人物设计造型（幼态脸+水润眼+果冻唇+服装+发型发色+配饰）
4. 自动生成缺失文案
5. 编写 6 个组件的 prompt（人物用 v2 模板，不用手持商品）
   - 若有用户商品图：桌面商品贴 prompt 中心区留白
6. 通用组件调用 doubao-seedream-4-5-251128，人物组件调用 doubao-seedream-5-0-260128
7. 对组件 2/3/4/5 执行绿幕抠图
8. 对人物图层提亮17%（ImageEnhance.Brightness 1.17）
9. [可选] 对用户商品图执行去背景（白底/浅色背景用HSV阈值）
10. 合成预览图（使用提亮后的人物图层，用户商品图叠加在桌面产品区中央）
11. 打包交付
```


