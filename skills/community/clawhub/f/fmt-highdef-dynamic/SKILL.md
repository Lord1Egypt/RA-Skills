---
AIGC:
    ContentProducer: Minimax Agent AI
    ContentPropagator: Minimax Agent AI
    Label: AIGC
    ProduceID: "00000000000000000000000000000000"
    PropagateID: "00000000000000000000000000000000"
    ReservedCode1: 304502200161d7bac7e93fc3190e54dd47982935dc15aff76df0ffc4bd8b24e43ddc1379022100b1d9744c641dd89c2098ddc577b867b3b3902fea0d3c59cf7a7cb13810482dc7
    ReservedCode2: 3046022100c1c586e5f387eb7854675f21a38adc84b296333092490ab53a791773ee0ec771022100ef73b8676609201e5fd9d22bcb63465601097f6ce19e6f39364a08f151f5f33e42
description: FMT肠菌移植科普高清动态图生成器（插画版+4K静态图+1080P动态视频+批量模式+风格一致）。生成配套数字手绘插画静态PNG（4K超清），并转化为高清晰度1080P动态视频。风格活泼生动，适合科普教育。触发词：生成FMT动态图 / 生成高清动态 / 插画转高清视频。
name: fmt-highdef-dynamic
version: 6.0.0
---

# FMT高清动态图生成器 v6.0

> 专为《探秘人体微宇宙 · FMT肠菌移植健康科普（插画版）.docx》文档设计
> **v6.0（2026-05-12）：新增风格参考图+批量生成+质量核查+降级策略**

---

## ⚠️ 四大核心问题修复（必读）

### 问题1：图片清晰度不足 → 4K分辨率
- 必须在 `image_synthesize` 时指定 `resolution: "4K"`，输出4096px宽超清图像
- 4K分辨率下文字边缘更锐利，AI渲染更精准

### 问题2：中文字清晰准确 → 双轨策略
- **策略A（首选）**：Prompt中正确引导，文字放在色块背景上，白字蓝底对比
- **策略B（保底）**：AI生成无文字版 → Python PIL叠加精准中文字层

### 问题3：动态视频文字消失 → 文字保留强制指令
- 每条 `gen_videos` Prompt必含文字保留模块（见第四章）

### 问题4：内容单薄 → 三层场景结构强制要求
- 前景（装饰粒子）+ 中景（多角色互动）+ 背景（场景延伸）

---

## 一、工具与输出规格

| 工具 | 用途 | 输出规格 |
|------|------|---------|
| `image_synthesize` | 静态插画PNG（首选）| **4K（4096px）**，16:9 |
| `nano-banana-pro` | 静态插画PNG（备选，中文更好）| 1K/2K/4K |
| `gen_videos`（I2V模式）| 动态视频（首选）| **1080P**，6秒，MP4 |
| `batch_image_to_video` | 动态视频（备选）| 768P，6秒，MP4 |

> ⚠️ `gen_videos` 默认选6秒1080P；10秒1080P会自动降级为768P。

---

## 二、风格一致性保障（新增·改善1）

**首次使用本技能时，必须先生成"风格参考图"，作为后续所有图片的风格锚点。**

### 步骤0：生成风格参考图（每批次只做一次）

**目的**：锁定标准角色外观、线条风格、配色体系，确保20张图风格一致

**生成命令：**
```javascript
image_synthesize({
  requests: [{
    aspect_ratio: "16:9",
    output_file: "/workspace/fmt_style_guide.png",
    prompt: "[风格参考图Prompt，见下方标准模板]",
    resolution: "4K"
  }]
})
```

**风格参考图Prompt（固定不变，每次套用）：**
```
[4K ULTRA HIGH DEFINITION - 4096px width, 16:9]

[STYLE REFERENCE SHEET - All future images must follow this exact style]

[TITLE AREA] "FMT肠菌移植 · 风格标准" in bold white Chinese on #B5DDE5 blue banner at top

[CHARACTER REFERENCE ROW - 5 chibi characters side by side]:
Character 1: Doctor - blue medical coat, stethoscope, round glasses, kind smile, #B5DDE5 outfit
Character 2: Nurse - light cyan uniform, medical cap, rosy cheeks, waving hand, #A8D8C8 outfit
Character 3: Patient (adult) - casual clothes, slightly worried expression turning hopeful, #FDE3D1 blush
Character 4: Child patient - big head, small body, bright curious eyes, brave smile, colorful clothes
Character 5: Gut bacteria (good) - small round colorful cute characters, different shapes/colors representing diverse flora

[STYLE RULES BOX]:
- Line width: 6-8px rounded thick strokes, soft and friendly
- Eye style: Bean eyes with white highlight dot, black pupil center
- Cheek: Soft peach blush oval on both cheeks
- Body proportion: Big head (50% of body height), small body, tiny limbs
- Shadow: NONE - flat design only
- Border: None, pure shapes

[COLOR PALETTE REFERENCE]:
Primary blue: #B5DDE5 (light lake blue)
Accent cyan: #A8D8C8 (soft teal)
Warm gold: #E8C98A (soft earth yellow)
Peach blush: #FDE3D1 (warm peach)
Deep text: #4A5E6F (gray-blue for text/icons)
White: #FFFFFF (background and text on dark)
Background: #F7FBFC (very light blue-cream)

[DECORATION REFERENCE]:
- Bubbles: Semi-transparent light blue circles, sizes 15px-60px
- Particles: Tiny white dots with soft glow
- Medical icons: Shield, cross, heart - #4A5E6F color, rounded style
- No shadows, no gradients, flat only

[LINE STYLE SAMPLE]:
Draw a sample line style card showing: thick rounded lines, no sharp corners,
all elements connected smoothly, children's illustration aesthetic

[BRAND AREA] Small: hospital icon + "苏州市立医院" in small Chinese text bottom left
[VERSION] "v6.0 Style Guide" bottom right in small grey text
```

**保存路径**：`/workspace/fmt_style_guide.png`

**后续所有图片Prompt开头必须附上风格锚定指令**：
```
[FOLLOW STYLE GUIDE: /workspace/fmt_style_guide.png]
Style rules: chibi characters, thick rounded lines, flat design, pastel palette as defined.
Use the same character designs, line width, eye style, and color palette as the reference.
```

---

## 三、批量生成模式（新增·改善2）

### 批量指令格式

用户可用以下任一格式一次性提交多页需求：

**格式A：范围型**
```
批量生成第3-7页，主题分别是：肠道菌群失衡、临床表现、诊断标准、治疗方案、康复管理
```

**格式B：列表型**
```
批量生成：p1=肠菌移植概述，p2=适应证，p3=禁忌证，p4=供体筛选，p5=制备流程
```

**格式C：全文型**
```
为《FMT肠菌移植科普.docx》全文生成插画，共20页，每页独立生成
```

### 批量处理流程（自动执行）

```
Step 1: 解析需求 → 生成页面列表 [p1,p2,...pN]
Step 2: 检查是否已有风格参考图
         - 无 → 先生成风格参考图（仅1次）
         - 有 → 跳过
Step 3: 逐页生成（每页独立）：
         3a. 构建Prompt（锚定风格参考图）
         3b. image_synthesize → 4K PNG
         3c. 质量核查（见第四章）
         3d. 若通过 → gen_videos → 1080P视频
         3e. 若中文不准 → 策略B（PIL叠加）
         3f. 整理到 /workspace/fmt_pages/p[N]_主题/
Step 4: 完成后汇总报告
```

### 页面输出目录结构

```
/workspace/fmt_pages/
├── style_guide.png                    ← 风格参考图（只生成1次）
├── p01_肠菌移植概述/
│   ├── static.png                     ← 4K静态插画
│   ├── HD.mp4                         ← 1080P动态视频
│   └── metadata.json                  ← 页面元数据
├── p02_适应证/
│   └── ...
└── ...
```

**metadata.json格式**：
```json
{
  "page": 1,
  "title": "肠菌移植概述",
  "status": "completed",
  "static_generated": "2026-05-12T12:00:00",
  "video_generated": "2026-05-12T12:02:00",
  "chinese_quality": "pass",
  "notes": "中文清晰准确"
}
```

---

## 四、质量核查清单（新增·改善3）

**每张图生成后、发送给用户前，必须执行以下核查：**

### 核查A：图片清晰度
- [ ] 图片尺寸 ≥ 4096px 宽（4K）
- [ ] 无明显模糊区域
- [ ] 线条边缘锐利，无锯齿

### 核查B：中文文字（策略A使用时）
- [ ] 标题文字清晰可读，无乱码
- [ ] 文字与背景对比度高（白字蓝底 / 深字白底）
- [ ] 字号足够大（标题≥72px，正文≥48px）
- [ ] 无文字错误或缺字

### 核查C：三层构图
- [ ] 前景层：存在装饰粒子/气泡（5-8个）
- [ ] 中景层：存在多角色互动（≥2人）+ 核心场景
- [ ] 背景层：存在场景延伸，非空白

### 核查D：风格一致性
- [ ] 与风格参考图（fmt_style_guide.png）风格一致
- [ ] 角色外观符合参考图规范
- [ ] 配色在标准色板范围内

### 核查E：动态视频（生成后）
- [ ] 视频时长6秒
- [ ] 分辨率1080P
- [ ] 文字/图标/编号全程可见，未消失
- [ ] 动效柔和，无剧烈抖动

**核查结果处理：**
- 全部通过 → 发送给用户
- 任一项失败 → 记录失败项 → 重新生成或切换策略B → 重新核查

---

## 五、降级策略（新增·改善4）

### 降级路径总览

```
image_synthesize 失败 → nano-banana-pro 备选
gen_videos 失败 → batch_image_to_video 降级768P
中文不准 → 策略B：PIL叠加字层
风格漂移 → 重新锚定风格参考图
```

### 详细降级规则

**降级1：静态图生成失败**
```
触发条件：image_synthesize 返回错误或图片质量极差（无法识别内容）
降级动作：切换到 nano-banana-pro
  uv run ~/.codex/skills/nano-banana-pro/scripts/generate_image.py \
    --prompt "[原Prompt精简版，不含resolution参数]" \
    --filename "/workspace/fmt_page_[N]_[主题].png" \
    --resolution 4K
修复后：继续原流程
```

**降级2：动态视频生成失败**
```
触发条件：gen_videos 返回错误或输出文件损坏
降级动作：切换 batch_image_to_video
  batch_image_to_video({
    count: 1,
    image_file_list: ["/workspace/fmt_page_[N]_[主题].png"],
    output_file_list: ["/workspace/fmt_page_[N]_[主题]_HD.mp4"],
    prompt_list: ["[动态Prompt精简版，不含分辨率指令]"],
    duration_list: [6],
    resolution_list: ["768P"]
  })
修复后：告知用户视频为768P备选版本
```

**降级3：中文不准（PIL叠加字层）**
```
触发条件：image_synthesize 生成的中文出现错误/乱码/模糊
修复动作：
  Step A: 生成无文字版本（在原Prompt后追加 "NO TEXT, NO CHINESE CHARACTERS"）
  Step B: 使用Python PIL叠加中文字层
    python3 -c "
    from PIL import Image, ImageDraw, ImageFont
    img = Image.open('/workspace/fmt_page_[N]_[主题].png').convert('RGBA')
    w, h = img.size
    scale = w / 4096  # 4K基准
    # 标题栏
    bar = Image.new('RGBA', (w, int(h*0.10)), (181,205,214,245))
    img.paste(bar, (0,0), bar)
    draw = ImageDraw.Draw(img)
    try:
        font_title = ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', int(64*scale))
        font_sub = ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', int(36*scale))
    except:
        font_title = ImageFont.load_default()
        font_sub = ImageFont.load_default()
    draw.text((w//2, int(h*0.05)), '[标题文字]', fill=(255,255,255,255), font=font_title, anchor='mm')
    draw.text((w//2, int(h*0.08)), '[副标题文字]', fill=(200,220,240,255), font=font_sub, anchor='mm')
    img.convert('RGB').save('/workspace/fmt_page_[N]_[主题]_cn.png')
    "
  Step C: 用 _cn.png 作为基础重新调用 gen_videos
```

**降级4：风格漂移**
```
触发条件：多张图风格不一致（角色外观、线条粗细、配色偏差）
修复动作：
  重新调用 image_synthesize，在Prompt开头强制附上：
  "[MUST FOLLOW STYLE GUIDE: /workspace/fmt_style_guide.png]"
  "Exact same line width, eye style, body proportion, color palette"
```

---

## 六、中文字解决策略（核心）

### 策略A：AI直出中文（首选）

**关键技巧：**
1. 用英文括号包裹中文：`"肠菌移植" in bold white Chinese`
2. 强化指令："render Chinese text accurately, crisp and clear"
3. 指定字体风格："Chinese text in clean sans-serif font, thick strokes"
4. 文字放在色块背景上，白字蓝底，对比度最高
5. 字号占图高3-5%（4K图上约120-200px）

**配色对比强化中文清晰度：**
| 背景色 | 文字色 | 效果 |
|--------|--------|------|
| #B5DDE5（浅湖蓝）| #FFFFFF（白色）| ✅ 最清晰 |
| #4A5E6F（深灰蓝）| #FFFFFF（白色）| ✅ 清晰 |
| #E8C98A（金色）| #4A5E6F（深色）| ✅ 清晰 |
| #FFFFFF（白色）| #4A5E6F（深色）| ⚠️ 可用 |
| 透明/渐变 | 任意颜色 | ❌ 模糊，禁止 |

---

## 七、静态插画生成规范（4K超清）

### 构图层次要求

```
[前景层 - FOREGROUND] 5-8个元素
- 彩色气泡（半透明浅蓝色，多种尺寸）
- 光点粒子（白色微光点）
- 小装饰图标（医疗符号、爱心、星标）

[中景层 - MIDDLE GROUND] 核心内容层
- 主要角色（3-5个Q版卡通人物互动）
- 核心场景主体（器官/设备/流程道具）
- 信息色块（带中文标题的色块卡片）
- 编号圆圈①②③标注流程步骤

[背景层 - BACKGROUND]
- 场景延伸（肠道内壁纹理/医院走廊/自然环境）
- 渐变色调（从浅到深，暗示景深）
```

### 视觉风格规范

| 属性 | 要求 |
|------|------|
| 风格 | 数字手绘插画（Digital Hand-drawn Illustration） |
| 人物 | Q版大头，豆豆眼（深色+白色高光），淡淡腮红，粗圆润线条 |
| 线条 | 柔和圆润，6-8px粗，无锐角，无阴影 |
| 色彩 | 低饱和马卡龙色系，纯扁平无阴影 |
| 背景 | 极浅纯色（#F7FBFC），充足留白 |
| 画布 | 16:9，4K（4096px宽），横版 |

### 配色方案

| 颜色 | 色值 | 用途 |
|------|------|------|
| 浅湖蓝 | #8ECCD6 / #B5DDE5 | 主色调/标题栏 |
| 浅土黄 | #D4A96A / #E8C98A | 强调、点缀 |
| 沙色 | #F2E4C9 / #F5E8D3 | 背景辅助 |
| 淡青 | #A8D8C8 / #B8E4D4 | 辅助色调 |
| 雾蓝 | #D6EAF0 / #E8F4FA | 装饰、留白 |
| 深灰蓝 | #4A5E6F | 中文字、图标底色 |
| 白色 | #FFFFFF | 背景/白字底色 |

---

## 八、动态视频生成规范（1080P+文字保留）

### 动效Prompt结构

```english
[FOLLOW STYLE GUIDE: /workspace/fmt_style_guide.png]
The chibi cartoon medical illustration comes gently to life with rich layered motion.

[LAYER 1 - BACKGROUND ANIMATION]:
- Background texture gently breathes with soft color waves, subtle parallax drift
- Organic gut-wall pattern slowly shifts, very subtle

[LAYER 2 - MIDDLE GROUND ANIMATION]:
- [核心角色] gently bob up and down, arms wave slowly, smile widens gradually
- [主要场景] twinkle with warm glow, pulse gently, never disappear
- [流程步骤] ①②③ numbered circles pulse in gentle sequence
- [中文字区域] stable with soft breathing glow, text always visible

[LAYER 3 - FOREGROUND ANIMATION]:
- Bubbles float upward slowly with slight wobble
- Light particles twinkle and sparkle gently
- Small medical icons pulse with warm glow

[CRITICAL - TEXT STABILITY]:
- Every text element, Chinese label, number badge remains FIXED in position
- NO text fades, disappears, or becomes blurry at any point
- Text may have gentle shimmer/glow but must always remain legible
- Chinese characters stay crisp and stable throughout entire animation
- All ①②③ circles stay clearly visible with steady light pulse

[ANIMATION QUALITY]:
- High definition 1080P, ultra crisp and clear
- Gentle looping animation, dreamy and warm, never frantic
- Dreamy atmosphere, educational and friendly tone
Duration: 6 seconds. All characters and text in place throughout.
```

---

## 九、中文优化Prompt片段库

### 标题型
```
[TOP BANNER] Full-width #B5DDE5 light blue banner at top:
"肠菌移植" in large bold white Chinese, very large font, crisp and clear
"重建肠道健康" in smaller white Chinese below
Chinese font: bold rounded sans-serif, thick strokes, white-on-blue high contrast
```

### 步骤标注型
```
[STEP INDICATORS] Three numbered circles:
Circle 1: "① 评估" white text on #4A5E6F dark blue circle
Circle 2: "② 供体" white text on #B5DDE5 light blue circle
Circle 3: "③ 移植" white text on #E8C98A gold circle
All: bold font, crisp Chinese, high contrast, evenly spaced
```

### 对话气泡型
```
[SPEECH BUBBLE] White rounded rectangle, soft #B5DDE5 border:
"医生：您好，我来为您详细说明。"
in #4A5E6F dark blue Chinese text, 48px on 4K image, clean rounded font
```

### 信息卡片型
```
[INFO CARDS] Three cards with colored top strips:
Card top strip: #B5DDE5, body: white
Title "适用人群" in #4A5E6F, large number "3" bold, small Chinese description
All Chinese: bold, high contrast, minimum 48px
```

---

## 十、构图模板（4K版）

### 模板A：中央主体+三层场景
```
[前景] 光点粒子 + 气泡漂浮（5-8个）
[中景] 大型核心主体（器官/设备）+ 2-3个卡通人物围绕
       顶部大标题：「肠菌移植」（白字蓝底，≥72px）
[背景] 渐变肠道纹理/医院场景延伸
[底部] 医院图标（无中文）
```

### 模板B：流程叙事型（三步骤）
```
[顶部] 标题栏：「肠菌移植流程」（白字蓝底色块）
[左侧] 步骤①：角色+①②③圆形标注
[中间] 步骤②：核心互动场景（多角色）
[右侧] 步骤③：结果展示（图标+色块）
[背景] 肠道壁纹理连续延伸
[前景] 气泡/粒子装饰层
```

### 模板C：多角色互动型
```
[顶部] 标题：「肠菌移植」（白字蓝底大字）
[中央] 3-5人卡通人物互动
[四周] 设备/图标/流程框辅助
[背景] 丰富场景（肠道壁+装饰）
[前景] 气泡+光效
[底部] 医院图标
```

---

## 十一、输出规范

| 类型 | 路径 | 规格 |
|------|------|------|
| 风格参考图 | `/workspace/fmt_style_guide.png` | 16:9，4K |
| 批量输出根目录 | `/workspace/fmt_pages/` | 子目录结构 |
| 静态插画 | `fmt_pages/p[NN]_[主题]/static.png` | 16:9，4K，PNG |
| 高清动态视频 | `fmt_pages/p[NN]_[主题]/HD.mp4` | 16:9，1080P，6秒，MP4 |
| 页面元数据 | `fmt_pages/p[NN]_[主题]/metadata.json` | JSON |

---

*更新于：2026-05-12 v6.0 — 新增：风格参考图锚定+批量生成+质量核查+降级策略*