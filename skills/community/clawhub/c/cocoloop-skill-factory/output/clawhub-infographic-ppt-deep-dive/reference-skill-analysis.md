# 参考 Skill 深拆

## 样本清单

| Skill | 主方向 | 中间层 | 最终产物 | 最值得借鉴 |
| --- | --- | --- | --- | --- |
| `article-to-infographic` | 长文转单页信息图 | outline + 分步确认 | HTML, PNG | 强确认流、强风格约束、单文件 HTML |
| `baoyu-infographic` | 专业信息图生成 | `analysis.md` + `structured-content.md` + prompt | 图片 | 分析框架、布局风格正交化 |
| `visual-note-card` | 知识卡片/视觉笔记 | 固定版式内容槽位 | HTML, PNG/JPEG | 模板骨架、海报级视觉语法 |
| `ppt-maker` | Markdown 转原生 `pptx` | Markdown DSL | `pptx` | 语法映射、表格转图表 |
| `ai-presentation-maker` | 访谈式 deck 生成 | interview brief + Markdown deck + JSON metadata | Markdown, HTML, Gamma, `pptx`, PDF | 访谈流、事实校验、speaker notes、多导出 |
| `text-to-ppt` | 文本转 HTML slides | JSON slide outline | HTML slides | 两阶段生成、并行逐页渲染 |

## 1. 如何拆解信息

### `article-to-infographic`

做法是先抽标题、副标题、关键统计、关键观点、引用、比较、时间顺序、自然分类和实体，然后按内容信号归类成时间线、数据面板、对比、流程、卡片网格或 editorial。

精华在于它不让 agent 直接写版面，而是先完成一个 outline 确认表，再单独确认布局、风格、插画和输出格式。这个流程能明显降低“内容还没想清楚，视觉已经定死”的问题。

### `baoyu-infographic`

这是本轮最强的内容拆解方案。它把前处理拆成：

- `analysis.md`
  - 主题
  - 学习目标
  - 目标受众
  - 内容类型
  - 复杂度
  - 原文数据点
  - layout × style 推荐
- `structured-content.md`
  - 标题
  - Overview
  - Learning Objectives
  - 分 section 的 key concept / content / visual element / text labels
  - Data points verbatim
  - Design instructions

这里最值钱的是两个原则：

- 先按 instructional design 做分析，再做视觉
- 所有事实、统计、引语都要求 verbatim 保留

这套结构非常适合沉淀到 `infographic-generation` 原子能力里。

### `visual-note-card`

它不追求通用内容分析，而是默认“把复杂内容压缩成一个固定 poster 语法”。
核心信息拆解方式是：

- 提炼一个 2 到 6 列的 framework
- 写一个强观点 thesis
- 左侧深色区讲故事、问题、转变
- 右侧浅色区讲编号洞察
- 底部做公式化收束

它的内容拆解更像“卡片编辑器思维”，适合知识卡片、传播图卡、海报型信息图。

### `ai-presentation-maker`

它把采集流程做成 6 个访谈阶段：

1. Subject
2. Audience
3. Speaker
4. Work
5. Angle
6. Resources & CTA

精华不是提问本身，而是每一段都明确规定了要捕获什么。
这样最后的 slide、speaker notes、CTA、export 都有稳定来源。

### `text-to-ppt`

它先把任意文本转成 JSON slide outline。这个中间层非常薄，但足够支撑并行生成：

- slide number
- type
- heading
- points / chartData
- layout
- notes

这非常适合 agent 环境里的并行 slide 生产。

### `ppt-maker`

它没有显式的分析文件，而是把 Markdown 语法本身当结构层：

- `#` 封面
- `##` 分页
- `###` 页内标题
- 列表、表格、代码块、引用块分别映射不同组件

优点是简单直接。缺点是前置分析能力弱，比较依赖上游先把 Markdown 写好。

## 2. 如何组织大纲

### 信息图

有 3 种成熟套路：

1. 先大纲，再视觉确认
   - 代表：`article-to-infographic`
   - 适合开放输入和高不确定性题材
2. 先学习目标，再 section 模板
   - 代表：`baoyu-infographic`
   - 适合系统性知识整理和高密度信息图
3. 先固定海报语法，再压内容
   - 代表：`visual-note-card`
   - 适合传播型视觉卡片

### 演示稿

有 3 种成熟套路：

1. 先访谈，再按 narrative arc 组 slide
   - 代表：`ai-presentation-maker`
2. 先出 JSON 大纲，再并行做 slide
   - 代表：`text-to-ppt`
3. 先写 Markdown，再直接渲染
   - 代表：`ppt-maker`

最强做法其实是把 1 和 2 结合：

- 先拿到访谈或 brief
- 再生成结构化大纲
- 最后再进渲染

## 3. 如何写文案

### 信息图文案

#### `baoyu-infographic`

文案纪律最强：

- 不新增事实
- 不改写统计
- 标题和标签要为视觉服务
- 先定义 viewer 要学会什么

这说明信息图文案不是普通摘要，而是“为了图形组织做语言压缩”。

#### `visual-note-card`

文案风格最鲜明：

- thesis 要有态度
- framework 名称要容易记
- left panel 更偏 narrative
- right panel 更偏 numbered insights
- bottom formula 要可传播

这套方法非常适合小红书卡片、知识海报、单页传播图。

#### `article-to-infographic`

它对文案的要求更多落在“不要 AI 套版味”和“设计必须有明确气质”。
这类 Skill 的文案策略偏保守，强在流程，不强在内容表达本身。

### 演示稿文案

#### `ai-presentation-maker`

文案最成熟的点有 4 个：

- 先选 angle，再写 deck
- slide 上只放事实，不放幻想
- 每页都带 speaker notes
- 显式规定 “What NOT to say”

它还做了 factual validation：

- speculative
- unverified number
- projection
- superlative

这一套特别适合商业汇报和对外演讲。

#### `text-to-ppt`

文案策略更偏工程化：

- 每页一个明确 layout
- 数据必须变成 chartData
- 列表必须符合短句规则
- notes 只做 slide 提示

#### `ppt-maker`

文案几乎全部托管给 Markdown 输入本身。
优点是清晰。缺点是很难自动生成高质量 narrative。

## 4. 如何排版

### 单页信息图 HTML

#### `visual-note-card`

这是本轮最值得复用的固定模板。
它的版式骨架很清楚：

- 顶部信息条
- 左标题 / 右 thesis
- framework row
- 深色故事面板 + 浅色洞察面板
- bottom highlight bar
- footer

优点：

- 模板稳定
- 视觉识别强
- 单页密度高
- 适合 HTML 到 PNG 的高保真导出

#### `article-to-infographic`

更像“版式原则库”而不是固定模板：

- timeline
- statistics dashboard
- comparison
- process flow
- listicle / card grid
- magazine / editorial

它强调：

- CSS Grid 做总布局
- 紧凑间距
- 不允许通用卡片堆叠感
- 需要 print media query

#### `baoyu-infographic`

它的排版方法是“layout × style”正交：

- `layout` 决定结构
- `style` 决定美学

这比简单的“theme”更适合信息图，因为信息结构本身就是版面的一部分。

### HTML slides

#### `text-to-ppt`

它给了一套很清楚的 slide DSL：

- centered
- bullets
- split
- grid
- timeline
- cards
- fullchart
- quote

再用固定 design system 约束：

- 16:9
- 无滚动
- 数字必须可视化
- 编号列表必须做 badge
- Font Awesome 图标
- Chart.js 模板

#### `ai-presentation-maker`

它把 HTML slides 分成两层：

- combined deck
- per-slide files

再配 11 种 slide type 和 4 套 theme。
这种做法对 factory 很有价值，因为它把“内容型 slide” 和 “舞台型 slide” 明确分开了。

### 原生 `pptx`

#### `ppt-maker`

它用 `pptxgenjs` 做得很实：

- cover / content / ending 三类页
- 主题色和图表色分离
- 列表、代码块、引用块、表格都有对应 renderer
- 图表页自动走“图表 + 辅助内容”双栏布局

这不是特别惊艳的版式系统，但非常实用。

#### `ai-presentation-maker`

它的 `pptx` 更像轻量导出：

- 从 Markdown 解析 slide
- 用 `python-pptx` 的基础 layout
- speaker notes 写入 notes slide

优点是通用。
缺点是视觉上明显弱于 HTML 路线。

## 5. 如何输出美观 HTML 和 `pptx`

### 美观 HTML 的共性

从这几套实现里，HTML 质量高的共同点是：

- 有稳定中间层，不是现编现排
- 主题、版式、组件有明确边界
- 把导出状态也算进模板
- 为 print / PNG / notes / keyboard navigation 单独设计

可直接吸收的做法：

- `visual-note-card`
  - 固定 poster 宽度和 section 语法
  - 浮动导出按钮
  - HTML 内建 PNG/JPEG 导出
- `text-to-ppt`
  - shell 模板 + slide div 拼装
  - JSON 大纲驱动逐页生成
- `ai-presentation-maker`
  - combined deck 和 per-slide 双模式
  - theme gallery + slide type gallery
  - notes 面板和打印链路

### 稳定 `pptx` 的共性

原生 `pptx` 质量更依赖 renderer：

- `ppt-maker` 适合从结构化 Markdown 快速出一个可编辑 deck
- `ai-presentation-maker` 适合把已有 Markdown deck 转成一个保守的 `pptx`

对 factory 最实用的结论是：

- 如果目标是“高颜值演示”，优先 HTML。
- 如果目标是“交付给 PowerPoint 用户继续改”，优先原生 `pptx`。
- 如果两个都要，最好先做 HTML 或 Markdown deck，再加单独导出器。

## 6. 最终可沉淀的方法库

### 信息图方法库

1. 先做内容分析
2. 产出结构化中间层
3. 分开选择 layout 和 style
4. 先确认 outline，再确认视觉
5. HTML 和 PNG 分开处理

### 演示稿方法库

1. 先拿 brief 或 interview
2. 产出 slide outline
3. 做 slide type 选择
4. 内容页和视觉页分开
5. HTML、Gamma、`pptx`、PDF 分开导出
6. 导出前做 factual validation 和 overflow 检查

## 7. 对 factory 的直接启发

后续如果要把这轮精华沉淀回 `factory`，最值得做的不是新增一个“会做 PPT/信息图”的笼统能力，而是补成几个稳定模块：

- 信息图分析模板
- 视觉卡片固定模板
- 演示稿访谈模板
- slide outline 协议
- HTML slide shell
- `pptx` adapter
- factual validation 规则
- HTML 到 PNG / PDF 的导出链路
