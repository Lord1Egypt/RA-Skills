# 可定制化AI 演示文稿（PPT）生成器

**Custom AI PPTX Generator — Design-driven, editable PowerPoint creation from your content**

### 简介

Custom AI PPTX Generator 是一个面向实际工作场景的 AI 演示文稿生成 Skill。

它不是简单地把文字转换成 PPT，也不是从固定模板库中套用页面，而是首先理解用户提供的内容、受众和表达目标，再根据内容特征设计合适的视觉表达方式，最终生成可编辑的 PowerPoint（PPTX）文件。

核心理念：

> **Content determines Design.**
> **内容决定设计，而不是模板决定内容。**

### 适用场景

适合需要频繁制作 PPT，但不希望每次从零开始设计的用户，例如：

* HR / People & Culture
* 管理咨询顾问
* 培训师 / L&D
* 项目经理
* 销售与市场人员
* 企业管理者
* 教师与学生
* 创业者
* 需要制作汇报、培训、方案或项目介绍的职场人士

### 支持的输入

可以从多种材料开始，包括：

* 文字 / Prompt
* Word / DOCX
* PDF
* PowerPoint / PPTX
* Email / EML
* 图片
* 表格 / Excel
* 用户提供的图片、Logo、图标及其他素材

### 核心工作流程

1. **Content Analysis**
   分析原始材料，提取核心信息、逻辑关系和数据。
2. **Presentation Structure**
   将内容转化为适合演示的页面结构和叙事逻辑。
3. **ASCII Storyboard**
   用结构化 ASCII storyboard 明确每一页的内容、层级和布局逻辑，作为后续制作的内容契约。
4. **Visual Prototype**
   根据内容和 storyboard 建立视觉方向及页面样例，在正式生成 PPT 前进行视觉确认。
5. **Native PPTX Generation**
   生成真正的 PowerPoint 文件，而不是图片拼成的"假 PPT"。
6. **Quality Assurance**
   对生成结果进行结构、内容和 PowerPoint 可打开性检查，并在必要时进行视觉验证。

### 核心特点

**1. Content-driven design**

不同主题不应该长得一样。

Skill 会根据内容类型、受众和表达目的选择不同的视觉表达方式，例如信息卡片、流程、时间线、对比、数据叙事、场景化视觉、概念图等。

**2. Editable native PPTX**

最终输出为原生 PPTX，文字、形状、图表及其他元素尽可能保持 PowerPoint 可编辑，而不是只生成一张图片。

**3. Human-in-the-loop**

重要的设计决策不会被 AI 静默决定。

用户可以在结构和视觉方向阶段进行确认，再进入正式 PPT 制作。

**4. Content integrity**

用户提供的原始内容和确认后的 storyboard 是内容事实来源。

如果使用外部图像生成工具，必须避免因为 AI 重绘而改变原始文字、数字或事实信息。

**5. Visual variety**

Skill 不以固定模板库作为核心。

它复用的是设计原则、视觉规律和制作能力，而不是反复复用相同的页面长相。

### 与普通 AI PPT 工具的区别

普通 AI PPT 工具通常采用：

> Content → Template → Slides

而 Custom AI PPTX Generator 更强调：

> **Content → Meaning → Visual Concept → Design → Editable PPTX**

因此，同一个 Skill 可以针对不同主题产生完全不同的视觉结果。

### 品牌理念

**千题千境**

> 同样是 PPT，不应该因为使用了同一个工具，就拥有同一张脸。
>
> **Every topic, a different design.**

---

## 安装 / Install

1. 将 `custom-ai-pptx-generator/` 文件夹复制到技能目录：
   - WorkBuddy: `~/.workbuddy/skills/custom-ai-pptx-generator/`
   - CodeBuddy: `~/.codebuddy/skills/custom-ai-pptx-generator/`
2. 重启应用 / 重新加载技能。当用户要求制作 PPT 且希望交付原生可编辑 PowerPoint 时自动触发。

## 环境要求 / Requirements

| 组件 | 用途 |
|---|---|
| Python 3.10+ 及 `python-pptx` | 原生 PPTX 重建 |
| Windows 桌面版 PowerPoint | COM 导出 PNG 做视觉自检 |
| 出图工具（内置 image_gen 或混元生图 API，可选） | 视觉样图；不可用时自动切换「提示词交付」兜底路径 |

## 许可 / License

MIT
