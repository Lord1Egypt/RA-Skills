# 设计收束

## 目标

把这轮从 `clawhub` 拆出来的精华，收束成后续可并入 `skill-factory` 的稳定设计，而不是只停在“有哪些热门 Skill”。

## 设计方向

### 方向 1：信息图走“双轨”

信息图不该只做成一个泛化能力，应该分成两条轨道：

1. **分析驱动型信息图**
   - 适合文章、报告、研究总结、流程说明
   - 参考：`article-to-infographic` + `baoyu-infographic`
2. **模板驱动型知识卡片**
   - 适合知识卡片、传播图卡、单页海报
   - 参考：`visual-note-card`

原因很直接：

- 第一类任务需要先拆信息，再谈视觉组织。
- 第二类任务更适合先固定版式，再把内容压进去。

### 方向 2：演示稿走“三层”

演示稿生成建议拆成三层，而不是一个大一统 Skill：

1. **brief / interview layer**
   - 负责拿到真实素材、受众、speaker、angle、CTA
   - 参考：`ai-presentation-maker`
2. **outline layer**
   - 负责把输入压成 slide-by-slide 结构化中间层
   - 参考：`text-to-ppt`
3. **render / export layer**
   - 负责 HTML slides、Gamma、`pptx`、PDF 等不同导出
   - 参考：`ppt-maker` + `ai-presentation-maker`

这样后续不管输入来自访谈、现成文档，还是 Markdown，都可以接到同一套渲染层。

## 关键设计决策

### 1. 固定中间层

后续补能力时，必须要求信息图和演示稿都有显式中间层。

信息图建议至少有：

- `analysis.md`
- `structured-content.md`

演示稿建议至少有：

- `presentation-brief.json`
- `slide-outline.json`

### 2. 输出格式分离

不要把 HTML、PNG、`pptx`、PDF 混成一个“最终输出”。
应该把它们明确成不同导出器：

- `html_poster`
- `png_export`
- `html_slides`
- `pptx_export`
- `pdf_export`

### 3. 把事实校验写进演示稿能力

`ai-presentation-maker` 证明了：好的演示稿 Skill 不只是会排版，还要会审校。
后续 presentation 能力里建议内建：

- speculative claim check
- unverified number check
- projection caveat check
- overflow / length check

### 4. 把布局和风格分开

`baoyu-infographic` 的 layout × style 正交设计值得保留。
这意味着后续 spec 和能力目录里，信息图至少应拆出两个维度：

- `layout_family`
- `visual_style`

演示稿也建议类似处理：

- `slide_type`
- `theme`

## 推荐沉淀形态

### 原子能力层

建议后续把能力拆成下面这些原子块：

- `infographic-analysis`
- `infographic-card-template`
- `html-poster-export`
- `presentation-briefing`
- `slide-outline-generation`
- `html-slides-render`
- `pptx-render`
- `presentation-validation`

### 预设层

在现有 `document-artifacts` 和 `frontend-design` 预设里，后续可再细化：

- 信息图生成
  - 长文信息图
  - 视觉笔记卡片
- 演示稿生成
  - 商业 pitch deck
  - 研究总结 slides
  - 结构化 Markdown 转 `pptx`

### 输出层

这轮深拆之后，后续相关研究建议固定保留两类产物：

- `source-skills/`
  - 本地拉下来的 Skill 源码
- 分析文档
  - 方法拆解
  - 设计收口
  - 规格建议

## 收敛结论

后续接入 `factory` 时，最值得优先落实的不是“再搜更多 Skill”，而是先把这几条规则写稳：

1. 信息图和演示稿都必须先有中间层。
2. 信息图分分析驱动和模板驱动两轨。
3. 演示稿分 brief、outline、render 三层。
4. HTML 和 `pptx` 是两条平行输出链路。
5. 演示稿能力必须带 factual validation。
