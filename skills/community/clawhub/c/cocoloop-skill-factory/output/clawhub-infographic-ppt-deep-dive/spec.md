# 本轮规格

## 范围

本规格只约束“如何从参考 Skill 中提炼信息图与演示稿生成能力”。
当前不直接改写主 Skill 流程，也不直接新增构建脚本。

## 规格要求

### 1. 参考 Skill 必须本地化

凡是进入设计决策的参考 Skill，都必须本地拉取到：

- `output/clawhub-infographic-ppt-deep-dive/source-skills/`

分析不得只基于搜索摘要或市场页标题。

### 2. 信息图能力必须区分两条路径

后续任何信息图相关能力设计，都要先判断属于哪一类：

- `analysis_driven_infographic`
- `template_driven_visual_card`

如果需求同时包含两类，应在设计阶段明确主路径和次路径。

### 3. 演示稿能力必须显式声明输入层和导出层

后续任何演示稿相关能力设计，都要至少写清：

- 输入层
  - `interview`
  - `markdown`
  - `raw_text`
  - `document`
- 中间层
  - `presentation_brief`
  - `slide_outline`
  - `deck_markdown`
- 导出层
  - `html_slides`
  - `pptx`
  - `pdf`
  - `gamma_markdown`

### 4. 中间层必须可落盘

后续如果正式做 capability 或 preset 收口，至少要能保留：

#### 信息图

- `analysis.md`
- `structured-content.md`

#### 演示稿

- `presentation-brief.json`
- `slide-outline.json`
- `deck.md`

### 5. 视觉结构和审校规则都算能力的一部分

后续沉淀能力时，不允许只写“如何生成”。
至少还要补齐：

- 如何收集信息
- 如何组织大纲
- 如何选择 layout / style / slide type / theme
- 如何导出
- 如何做 factual validation 或 overflow check

### 6. 输出能力要单独表达

后续能力目录建议单独表达这些导出器，而不是藏在主能力说明里：

- `html_to_png`
- `html_to_pdf`
- `deck_markdown_to_html`
- `deck_markdown_to_pptx`

## 当前 open gaps

- 还没有把这轮结论正式写回原子能力索引。
- 还没有把 infographic / presentation 的中间层 schema 变成正式协议。
- 还没有把演示稿的 factual validation 规则接进主流程。
