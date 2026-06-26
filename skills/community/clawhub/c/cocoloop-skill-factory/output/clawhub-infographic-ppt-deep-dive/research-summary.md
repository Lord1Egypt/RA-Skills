# ClawHub 信息图与演示稿 Skill 深拆研究

## 研究范围

本轮研究聚焦 `clawhub` 中与信息图生成、视觉笔记卡片、演示稿生成、HTML slides、`pptx` 导出直接相关的 6 个 Skill：

- `article-to-infographic`
- `baoyu-infographic`
- `visual-note-card`
- `ppt-maker`
- `ai-presentation-maker`
- `text-to-ppt`

所有目标 Skill 都已经拉到本地：

- `output/clawhub-infographic-ppt-deep-dive/source-skills/`

研究方式分两层：

1. 先用 `clawhub search` 和 `clawhub inspect` 做候选筛选、文件清单确认和摘要核对。
2. 再把包体拉到本地，直接查看 `SKILL.md`、参考模板、导出脚本和 HTML/Python/JS 实现。

## 关键发现

### 1. 信息图方向已经分化出两条成熟路径

第一条是 `article-to-infographic` 和 `baoyu-infographic` 代表的“分析驱动型”。
这条路先拆信息，再选布局和风格，最后才进入生成。
重点是内容分类、结构映射、确认流程和 prompt 组装。

第二条是 `visual-note-card` 代表的“模板驱动型”。
这条路先固定版式，再把内容压进一个稳定 poster 骨架。
重点是卡片语法、固定分区、视觉密度和 HTML 到 PNG 的稳定输出。

### 2. 演示稿方向已经分化出三条成熟路径

第一条是 `ai-presentation-maker` 代表的“访谈驱动型”。
先通过 6 个阶段访谈拿到真实素材，再生成 deck、speaker notes 和多格式导出。

第二条是 `text-to-ppt` 代表的“计划先行型”。
先把输入转成 JSON 大纲，再并行生成单页 HTML，最后统一拼装。

第三条是 `ppt-maker` 代表的“语法驱动型”。
把 Markdown 当作 DSL，直接映射到 `pptxgenjs`，并从表格中自动识别图表。

### 3. HTML 产物的质量上限高于 `pptx`

本轮样本里，最精细的视觉控制都发生在 HTML 路线：

- `visual-note-card` 的固定海报模板
- `text-to-ppt` 的单页 slide shell
- `ai-presentation-maker` 的单页 HTML 和整 deck HTML

`pptx` 路线主要有两种：

- `ppt-maker` 直接生成原生 `.pptx`
- `ai-presentation-maker` 先存 Markdown，再通过 `python-pptx` 做轻量导出

从实现质量看：

- HTML 路线更适合美观、强风格、动画、导出 PDF、社交传播。
- `pptx` 路线更适合企业交付、可编辑性、兼容 PowerPoint 工作流。

### 4. 真正稳定的实现都把“内容结构”和“视觉渲染”分开了

这 6 个 Skill 虽然风格不同，但稳定做法很接近：

- 先拿源内容
- 再做结构化中间层
- 再做布局/风格/导出决策
- 最后才输出 HTML 或 `pptx`

中间层的形式不同：

- `analysis.md`
- `structured-content.md`
- JSON slide outline
- Markdown deck

但本质都是“先把信息组织清楚，再交给渲染器”。

### 5. 高质量输出都显式处理了导出和验证

不是所有 Skill 都只停在生成代码或生成 HTML：

- `visual-note-card` 自带 HTML 内部导出菜单和 Playwright PNG 截图脚本
- `article-to-infographic` 自带 Playwright 截图脚本，并在截图前强制 reveal/counter 到最终状态
- `ai-presentation-maker` 把 HTML、Gamma、`pptx`、PDF 做成分离的 export 路线
- `ppt-maker` 直接用 `pptxgenjs` 生成 `.pptx`

说明“产物交付链路”本身就是能力，不该被藏在实现细节里。

## 最值得吸收的精华

### 信息图

- `article-to-infographic`
  - 强确认流：大纲、布局、风格、插画、输出格式逐步确认
  - 强风格约束：明确禁止通用 AI 味设计
  - 强导出兜底：HTML 到 PNG 单独脚本化
- `baoyu-infographic`
  - 最好的信息分析框架
  - 最好的“layout × style”正交设计
  - 最好的结构化中间层模板
- `visual-note-card`
  - 最强固定模板
  - 最清楚的卡片级视觉语法
  - 最接近传播型图卡和知识卡片产物

### 演示稿

- `ai-presentation-maker`
  - 最好的访谈式信息采集
  - 最好的事实校验和 speaker notes 规则
  - 最完整的多导出路径
- `text-to-ppt`
  - 最好的“两阶段生成”纪律
  - 最清楚的并行 slide 生成协议
  - 最适合做 HTML slides 工厂
- `ppt-maker`
  - 最直接的 Markdown 到 `pptx` 语法映射
  - 最实用的表格转图表逻辑
  - 最适合做原生 `pptx` 快速生产

## 风险与异常

- `article-to-infographic` 在 `inspect` 中被标记为 `SUSPICIOUS`，本轮只做静态拆解，没有执行其脚本。
- `article-to-infographic/skill.json` 显示版本 `2.0.0`，但安装到本地的 `_meta.json` 仍是 `1.0.0`，存在元数据不一致。
- `ai-presentation-maker` 的设计非常完整，但包体里带了较长的营销内容，真正有价值的是中段的 interview、deck generation、export 和 template 部分。

## 结论

对 `skill-factory` 来说，这轮最重要的结论有 3 个：

1. 信息图和演示稿都应该先建“结构化中间层”，不要直接从原文跳最终产物。
2. HTML 和 `pptx` 应该被视为两条并列输出链路，各自有不同优势。
3. 后续能力沉淀不该只记录“能生成什么”，还要记录“如何收集信息、如何选结构、如何校验、如何导出”。
