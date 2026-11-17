---
name: design-taste
description: 设计审美指南，让视觉产出显得有意图，而不是模板化的“AI slop”。用于设计、搭建、重做风格、重新设计、打磨、点评或审查 UI（网页、落地页、仪表盘、App 界面、组件），建立设计 token，挑选配色/字体/间距，给幻灯片/文档做主题，做极简风格，评审/对标线上网站 URL，评审或重制图片（照片、产品图、海报、横幅、插画、科研配图、AI 图片——构图、配色、AI 痕迹），评审游戏美术（截图、主视觉、Steam 胶囊图、图标、HUD、概念图、精灵/像素图；品类可读性），或制作海报/封面。触发词：设计界面、美化页面、界面评审、UI 审查、重新设计、改版、设计规范、配色、字体搭配、极简风格、主题、海报、网站评审、官网改版、对标、图片审美、图片评审、海报评审、配色提取、构图、科研配图、AI 图片评价、游戏美术、游戏审美、游戏 UI、二次元、像素、游戏截图评审；English keywords - UI design, redesign, design tokens, website review, image critique, game art review, RPG, MOBA. 不用于没有可见变化的后端逻辑或代码清理。
license: MIT
metadata:
  version: "1.1.0"
---

> 本文件超过一次读取的长度（约 4,000 字符）。开始之前请分段读到末尾（评审路径、约束、构建路径、报告、参考文件地图）。

# 设计审美（Design Taste）

这里的“审美”指：**一个清晰的方向、少量精选的 token、强烈的层级、没有默认感的填充物**。所有模式都先走第 0–2 步，然后走**评审路径（R3–R6）**或**构建路径（B3–B7）**，最后是**报告**。步骤编号只用于你自己跟踪，不要写进交付物。

## 第 0 步 —— 接收需求，选择模式
- **做什么：** 读需求和材料（代码、URL、图片），从下表选一个主模式（+ 叠加风格）；带模式专属步骤的完整表格见 `references/modes.md`。
- **产出：** 模式、叠加风格、路径、要加载的参考文件。
- **判定：** 只点评/打分/对标 → 评审路径；要创建或修改可见的东西 → 构建路径；Redesign = 先用评审路径做审查，再走构建路径。没有可见产出（后端、代码清理）→ 本技能不适用。

| 模式 | 路径 | 加载 |
|---|---|---|
| Audit（审查，UI/代码评审） | 评审 | `audit.md` |
| Site Review（网站评审、对标） | 评审 | `site-review.md`、`benchmarks.md`，运行 `scripts/review_site.py` |
| Image Review（图片评审：照片/海报/AI 图片） | 评审 | `image-aesthetics.md`，运行 `scripts/review_image.py <img> --type photo\|product\|poster\|social\|ui\|illustration\|figure\|ai` |
| Game Art Review（游戏美术评审） | 评审 | `game-aesthetics.md`、`game-workflows.md`，运行 `review_image.py --type game-screenshot\|key-art\|capsule\|icon\|game-ui\|concept\|sprite --genre <g>` |
| Redesign（重设计） | 评审 → 构建 | 先 `audit.md`，再 `redesign.md` |
| Create（创建页面/应用/组件） | 构建 | `direction.md`、`principles.md`、`tokens.md` |
| Theme（幻灯片/文档主题） | 构建 | `theming.md` |
| Artifact（海报/封面 PNG/PDF） | 构建 | `artifacts.md` |
| Image Restyle（图片重制/配色/科研配图） | 构建 | `image-workflows.md` |
| Minimalist（极简，叠加） | 同主模式 | `minimalist.md` |

## 第 1 步 —— 收集上下文
- **做什么：** 弄清技术栈、CSS 方案、现有 token/设计系统、品牌和约束。拿到基线数据：URL 用 `review_site.py`，图片用 `review_image.py --type … [--genre …]`（本中文版默认中文报告，英文用户传 `--lang en`）。有 OCR（`tesseract`）时，用它读取图片中的文字。
- **产出：** 简短的上下文记录 + 基线指标（或注明“无工具，仅凭目测”）。
- **完成条件：** 知道现有什么、哪些必须保留。缺材料 → 先向用户要。

## 第 2 步 —— 确定方向
- **做什么：** 构建或打分前写 3–5 行：目的与受众；**一个调性**（“简洁现代”不算调性）；**一个记忆点**；约束；密度。评审路径：以“感知到的方向”作为打分标尺。
- **产出：** 方向块（`direction.md` §5）；构建任务在第一次写文件前先给用户看。
- **完成条件：** 写明一个调性和一个记忆点；已有设计系统时方向就是“把它用好”。

## 评审路径（Audit、Site Review、Image Review、Game Art Review；Redesign 的前半段）

### R3 —— 测量
- **做什么：** 运行该模式的可量化检查：`audit.md` §1 的 grep 计数（不同的十六进制颜色、字号、圆角、阴影）、`review_site.py`，或 `review_image.py`（游戏另加灰度/缩略图）。绝不修改被评审的作品。
- **产出：** 用真实计数填写的指标表。
- **完成条件：** 报告模板需要的每个指标都有数字，或注明“无法测量：原因”。

### R4 —— 打分
- **做什么：** 用该模式的量表打分（`audit.md` §2、`site-review.md` §2、`image-aesthetics.md` 8 维度 + AI 清单、`game-aesthetics.md` G1–G11），按参考文件的方式合成指标分和视觉分。
- **产出：** 逐维度分数，附具体证据。
- **完成条件：** 每个维度都有分数和证据；有 P0 时按量表封顶总分。

### R5 —— 对比（仅 Site Review 和 Game Art Review）
- **做什么：** 对照 `benchmarks.md`/`benchmarks.csv` 或品类档案。**产出：** 差距表 + 2–3 条结论。**完成条件：** 每个差距都写明基准值。

### R6 —— 排优先级
- **做什么：** 列出 P0/P1/P2 问题，每条包含是什么、在哪里（file:line / 区域）、为什么、具体修法（token 值、HEX、裁切、提示词）。
- **产出：** 按优先级排列的清单。**完成条件：** 每条都有位置/原因/修法。Redesign → B3；其他 → 报告。

## 约束（B6 和评审时检查）

### 核心规则（始终生效）
- **坚持。** 大胆的极简和大胆的繁复都可以；把一切取平均的畏缩设计不行。
- **用 token，不用字面量。** 每个颜色、尺寸、圆角、阴影和时长都来自一个小的命名尺度（见 `references/tokens.md`）。
- **数量克制：** 约 1 个强调色、1–2 种字体、≤ 6–8 个字号、一个圆角族、≤ 3 级阴影、一个缓动曲线族。
- **用尺寸、字重和空间的对比建立层级** —— 而不是更多的框、边框和颜色。
- **间距落在网格上**（4/8px 基准）。相关的东西紧挨，组与组之间大方分开。
- **无障碍也是审美的一部分：** 文字对比度 ≥ 4.5:1（大字 3:1）、焦点可见、触屏点击区 ≥ 44px、尊重 `prefers-reduced-motion`。
- **真实内容。** 不要“张三 / Acme / Lorem ipsum”，不要“赋能你的工作流”式文案，不要用 emoji 当图标。
- **每种状态都存在：** 悬停、焦点、按下、禁用、加载、空、错误。

### AI slop 指纹（除非需求明确要求，否则避免）
- 白底上的紫→蓝渐变；深色上的霓虹发光；到处都是渐变文字。
- 条件反射地用 Inter/Roboto/Arial；所有东西一个字重。
- 居中 Hero + 三张一样的图标卡片 + 通用 CTA 色带。
- 卡片套卡片；每个元素都装在带投影的圆角描边盒子里。
- 无缘无故的毛玻璃；随机的装饰性色块。
- 统一的 `rounded-2xl` + `shadow-lg`；圆角不一致。
- 虚假指标（“快 10 倍”“99.9%”）和图库式用户评价。
- 处处弹跳/弹性动画；对布局属性做动画。

细节与替代方案：`references/principles.md`。

## 构建路径（Create、Redesign、Theme、Artifact、Image Restyle）

### B3 —— 预算与计划
- **做什么：** 规划好，让**完整、可用的第一版在约 40% 的步数/时间预算内完成**（页面或海报约 15 次工具调用或 8 分钟）。主文件用 1–3 次写入完成，不要几十次追加。完整版渲染出来之后才打磨。
- **产出：** 页面给出分区清单；海报给出**逐字写好的文案并统计词数**（总计 ≤ 25 个词，小字也算；中文按约 40 字计；不要编造用户没给的价格、地址、阵容、期号等细节），外加 2–4 个颜色 + 中性色。字体：两者都最多 2 个字族——等宽或标签字体也算一个。
- **完成条件：** 计划在预算之内，海报文案 ≤ 25 个词；放不下的现在就删，不要留到后面。

### B4 —— 先定 token
- **做什么：** 为颜色、字体、间距、圆角、阴影、动效定义小的命名尺度，写成 CSS 变量 / 主题配置（`tokens.md`）；Minimalist 用 `minimalist.md` 的数值。
- **产出：** token 块。**完成条件：** 约 1 个强调色、1–2 种字体、≤ 6–8 个字号、一个圆角族、≤ 3 级阴影。

### B5 —— 做出完整版
- **做什么：** 在用户的技术栈中按全局层 → 每个计划的分区/元素 → 状态的顺序构建，只用 token；第一遍就包含 `prefers-reduced-motion` 和闭合标签。视觉作品：现在就渲染 PNG/PDF。
- **产出：** 完整文件 / 渲染出的作品。
- **完成条件：** 全部范围都存在且能渲染（HTML 以 `</html>` 结尾、PDF 能打开）。然后进入 B6——在此之前不打磨。

### B6 —— 硬性检查
- **做什么：** 逐条对照“约束”，再测量：十六进制颜色/字号/圆角数量；不同字族数（≤ 2，含等宽字体）；对比度；约 375/1280px 截图。**海报/视觉作品：** 列出画布上的每段文字并统计词数（加字距或转曲的文字也算；`pdftotext` 读不到转曲文字，所以从你的源文件统计）——除非需求本身提供了更多文案，否则必须 ≤ 25；超了就**删行，而不是缩小字号**；统计渲染图中的主色（量化后占像素 ≥ 2%）——必须 ≤ 4 个加中性色；字体已嵌入或转曲；没有被裁切的内容。运行现有测试/构建；Redesign 和 Image Restyle 重新运行第 1 步的脚本，对比前后数据。
- **产出：** 带数字的检查结果。
- **判定：** 任何一项不通过 → 回 B5 修正后再查；全部通过 → B7。

### B7 —— 打磨（仅在还有预算时）
- **做什么：** 细化间距、字体和细节；改动后重新跑 B6。**产出：** 改进后的文件。**完成条件：** 预算用完或看不出普通感；绝不能比上一个通过检查的版本更差。

## 最后一步 —— 报告
- **做什么：** 用用户的语言写（本中文版脚本默认生成中文报告骨架，替换每个 TODO）。构建：用 2–4 行说明方向和取舍、产出了什么（文件路径）、B6 的数字。评审：用该模式的模板（`audit.md` §3、`site-review.md` §4、`image-aesthetics.md` §7、`game-workflows.md` §2），开头先直接回答用户的问题。
- **产出：** 交付消息（以及报告文件/截图）。
- **完成条件：** 每个结论都有 R3/R4 或 B6 的数字或观察作支撑；没验证过的不说成已检查。

## 参考文件地图

- `references/modes.md` —— 完整模式表，含每个参考文件驱动的模式专属步骤。
- `references/direction.md` —— 方向提问、风格目录、按风格选字体/配色。
- `references/principles.md` —— 色彩、字体、间距、圆角、阴影、动效、布局规则 + 反模式。
- `references/tokens.md` —— 三层 token 体系（原始 → 语义 → 组件）及示例。
- `references/audit.md` —— P0/P1/P2 清单、可量化检查、报告格式。
- `references/redesign.md` —— 现有项目的安全升级流程。
- `references/minimalist.md` —— 暖色单色编辑风格规格。
- `references/theming.md` —— 幻灯片/文档/报告主题；主题配方。
- `references/artifacts.md` —— 海报与静态视觉作品（哲学 → 画布）。
- `references/site-review.md` —— URL 评审流程：抓取 → 指标 → 45/55 评分 → P0/P1/P2 报告。
- `references/benchmarks.md` —— 顶级公司官网拆解、行业打法、指标目标、常见错误。
- `scripts/review_site.py` —— Playwright 抓取 + 指标分 + 报告骨架；`scripts/benchmarks.csv` —— 147 个已评分站点。
- `references/image-aesthetics.md` —— 图片量表：8 个维度 × 类型权重、P0/P1/P2、AI 痕迹清单、指标区间。
- `references/image-workflows.md` —— 解析 → 配色 → 版式 → 增强流程；纸刊/拼贴/产品/配色/封面配方；Nature 风格配图清单；反 slop 提示词模板。
- `scripts/review_image.py` —— Pillow+numpy 图片指标（配色、和谐、影调、锐度、噪点、色彩丰富度、三分/重心、留白）→ metrics.json、palette.png、thirds-overlay.png、report.md。
- `references/game-aesthetics.md` —— 游戏量表：11 个维度（可读性、明度、玩法清晰度、HUD、特效…）× 资产权重、21 个品类档案、9 个资产量表、AI 检查、指标区间。
- `references/game-workflows.md` —— 灰度/剪影/缩略图/2 秒测试、按品类解读指标、P0/P1/P2 报告、修改配方、反 slop 游戏美术提示词。
- `scripts/review_image.py --type <游戏类型> --genre <g>` —— 增加明度分档、图底、形状清晰度、HUD 覆盖、色数、商店缩略图可读性 → grayscale.png、thumbnail.png。
- `references/sources.md` —— 上游技能、URL 与许可。
