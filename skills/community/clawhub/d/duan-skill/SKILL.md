---
name: duan-slides
description: AI演示文稿全流程制作：内容结构化→设计选型→AI插画/HTML构建→PPTX导出。17种实战验证的视觉风格（漫画/极简/数据叙事/国风），可编辑HTML与全AI视觉两条路径自由选择。当用户提到"做PPT"、"制作幻灯片"、"演示文稿"、"Keynote"、"slides"、"课件"、"汇报材料"、"路演"时使用。
---

# AI Presentation Workflow

> **设计哲学：Context, not control。** 理解目标和风格感觉，自主做出设计决策。参考文件是灵感库，不是逐字执行的清单。

---

## Skill 路径

脚本安装路径因用户不同而不同。执行脚本前，先用 Glob 工具搜索 `**/duan-slides/scripts/generate_image.py`，取所在目录作为 `SKILL_SCRIPTS_DIR`。

---

## 启动：三个决策

每次任务开始，确认以下三项。

### 协作模式

| 模式 | 适合 | 检查点 |
|------|------|-------|
| **Full Auto** | 信任AI交付，只需最终PPTX | 确认主题即可 |
| **Guided**（默认） | 把控方向，不管细节 | 大纲 / 风格选定 / 组装前 |
| **Collaborative** | 逐张审阅，全程掌控 | 每张slide |

### 制作路径

| | **Path A：可编辑HTML**（默认） | **Path B：全AI视觉** |
|---|---|---|
| 做法 | HTML slides + 选择性AI插画 → PPTX | 每张slide全AI生成图片 → PPTX |
| 优势 | 文字可在PPT中继续编辑，中文渲染完美 | 视觉震撼，风格高度统一 |
| 适合 | 商务汇报、需要反复修改的场景 | 艺术感强、发布演讲、快速草稿 |
| 注意 | — | 中文偶有错误，文字不可后期编辑 |

### 个人形象融入

检查 `assets/character/` 目录：
- 有 `*-sheet.png` → 直接使用
- 有 `original.*` 无设定图 → 自动生成设定图
- 为空 → 询问用户是否需要

**生成角色设定图：**
```bash
export $(grep GEMINI_API_KEY ~/.claude/.env) && \
uv run [SKILL_SCRIPTS_DIR]/generate_image.py \
  --input-image "assets/character/original.jpg" \
  --prompt "Character design sheet in [STYLE] style. Keep facial features faithfully. Show 3 expressions: neutral explaining, surprised/eureka, thinking. White background, no text." \
  --filename "assets/character/[style-name]-sheet.png" \
  --resolution 2K
```

同一风格只生成一次，后续复用。

---

## Step 1: 内容梳理

将原始材料转为逐张slide大纲。每张定义：
- **标题**：断言句，不是主题词 — 「Q3销售增长23%，新用户是主要驱动力」✓，「Q3销售」✗
- **要点**：最多3-4条
- **视觉类型**：插画 / 图表 / 流程图 / 引言
- Path A：是否需要AI插画？Yes/No + 一行场景描述
- Path B：完整视觉场景描述（布局+内容+情绪）

slide内容全部中文，仅保留必要英文（人名、品牌、技术术语）。

**Checkpoint（Guided/Collaborative）：** 表格展示大纲，用户确认后进入Step 2。

---

## Step 2: 风格选择

**核心洞察：插画/漫画类风格AI生成效果远优于「专业极简」。** 漫画风格有明确视觉语言，AI可充分发挥；暗色底+大留白缺乏视觉元素，生成结果「空」且「平」。

**按主题推荐3个风格：**

| 主题类型 | 第一推荐 | 第二推荐 | 第三推荐 |
|---------|---------|---------|---------|
| 品牌/产品 | Snoopy漫画 | Neo-Pop | 浮世绘/敦煌 |
| 教育/培训 | Neo-Brutalism | 学習漫画 | Snoopy漫画 |
| 技术分享 | xkcd白板 | Neo-Brutalism | Ligne Claire |
| 数据报告 | **NYT Magazine** ★ | Pentagram编辑 | Ligne Claire |
| 年轻受众 | Neo-Pop | 像素画 | 孔版印刷 |
| 国风/东方 | 敦煌壁画 | 浮世绘 | Takram思辨 |
| 正式商务 | **NYT Magazine** ★ | Pentagram编辑 | Build极简 |
| 路演/发布 | 苏联构成主义 | **NYT Magazine** ★ | Neo-Pop |
| 行业分析 | Pentagram编辑 | **NYT Magazine** ★ | Fathom数据 |
| 培训课件 | Takram思辨 | 温暖叙事 | 学習漫画 |
| 内部分享 | Neo-Brutalism | The Oatmeal | xkcd白板 |

用户说「想要XX风格」「不确定」「有例子吗」→ 查 `references/design-movements.md` 转换美学语言。

**展示风格：** 主动用 Read 工具显示 `assets/style-samples/style-NN-name.png` 样例图（不只是文字描述）。图片编号：01-snoopy, 02-manga, 03-ligne-claire, 04-neo-pop, 05-xkcd, 06-constructivism, 07-dunhuang, 08-ukiyo-e, 09-warm-narrative, 10-oatmeal, 11~17=第三梯队。

每个风格完整参数（色值/排版/构图/prompt规范）→ `references/proven-styles-gallery.md`

**Checkpoint（Guided/Collaborative）：** 展示3个风格 + 样例图，用户选定后进入Step 3。

---

## Step 3: 构建

### Path A：HTML + 选择性插画

每张slide生成独立HTML文件（720pt × 405pt）。**生成前必须遵守 4 条 html2pptx 硬性约束**（见 `references/prompt-templates.md` 第2节），否则导出会报错：
- DIV 里的文字必须用 `<p>` 或 `<h1>`-`<h6>` 包裹，不能裸文字
- 不支持 CSS 渐变，只能纯色（`linear-gradient` 会报错）
- `<p>`/`<h*>` 不能有背景/边框，这些放在外层 `<div>`
- `<div>` 不能用 `background-image`，改用 `<img>` 标签

**AI插画生成：**
```bash
export $(grep GEMINI_API_KEY ~/.claude/.env) && \
uv run [SKILL_SCRIPTS_DIR]/generate_image.py \
  [--input-image "assets/style-samples/style-NN-name.png"] \
  --prompt "[scene description in [STYLE] style]" \
  --filename "slide-NN-illustration.png" \
  --resolution 2K
```

垫图机制：`--input-image` 传入风格样例图或角色设定图，强制AI生成与参照图风格一致的插画。

### Path B：全AI视觉

每张slide生成完整图片（含所有文字和布局）：
```bash
export $(grep GEMINI_API_KEY ~/.claude/.env) && \
uv run [SKILL_SCRIPTS_DIR]/generate_image.py \
  --input-image "assets/style-samples/style-NN-name.png" \
  --prompt "[完整视觉描述：布局+内容+风格+情绪]" \
  --filename "slide-NN-name.png" \
  --resolution 2K
```

**短prompt比长prompt效果更好。** 描述mood和内容，不要约束颜色比例、构图位置、字号数字。详细提示词模板 → `references/prompt-templates.md`

---

## Step 4: 组装 PPTX

**Path A（html2pptx）：**
```bash
node [SKILL_SCRIPTS_DIR]/html2pptx.js \
  slide-01.html slide-02.html ... \
  -o output.pptx
```

**Path B（create_slides.py）：**
```bash
uv run [SKILL_SCRIPTS_DIR]/create_slides.py \
  slide-01.png slide-02.png ... \
  --layout fullscreen \
  -o output.pptx
```

---

## Step 5: 收尾

- Path A：可用 Playwright 截图预览关键slides
- Path B：直接用 Read 工具显示生成的PNG

**Checkpoint（所有模式）：** 展示预览，交付PPTX，汇报：完成X张，风格Y，文件路径Z。

Keynote/PowerPoint中可添加动画和Speaker Notes；Path A文字可继续编辑，Path B如有文字错误需重新生成该张图片。

---

## Assets 目录

```
assets/
├── style-samples/     # 17种风格样例图（视觉参照 + 垫图两用）
│   └── style-NN-name.png
└── character/         # 用户个人形象
    ├── original.jpg   # 用户提供的照片
    └── [style]-sheet.png  # 各风格的角色设定图（首次使用时生成）
```

---

## 参考文件

| 需要 | 文件 |
|------|------|
| 17种风格完整参数（色值/排版/构图/prompt规范） | `references/proven-styles-gallery.md` |
| HTML规范 + Path A/B提示词模板 | `references/prompt-templates.md` |
| 设计运动 → 风格映射（美学词汇转换） | `references/design-movements.md` |
| 设计原则与视觉规范 | `references/design-principles.md` |
| Snoopy风格专项深度指南 | `references/proven-styles-snoopy.md` |
