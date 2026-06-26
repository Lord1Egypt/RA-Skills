# 信息图生成

## 当前定位

这个能力现在默认作为 `structured-visual-storytelling` 的 `web_infographic` 或 `showcase_graphic` adapter 使用。
共享规则优先读取：

- `../structured-visual-storytelling/index.md`
- `../structured-visual-storytelling/shared-rules.md`
- `../structured-visual-storytelling/output-adapters.md`

## 适用场景

这个能力用于生成单张或小批量的信息图、视觉卡片、知识海报、数据说明图和适合社媒传播的单页视觉产物。

它更适合承接：

- 长文压缩成单页信息图
- 研究结果或流程说明图
- 知识卡片、视觉笔记、一页纸总结
- 需要 HTML poster 或 PNG 成品的视觉交付

## 先做哪种判断

信息图能力现在默认分两条路径：

### 路径 1：分析驱动型信息图

适合：

- 文章、报告、研究内容
- 结构复杂、主题开放
- 需要先拆信息再谈版式

代表参考：

- `article-to-infographic`
- `baoyu-infographic`

### 路径 2：模板驱动型视觉卡片

适合：

- 知识卡片
- 单页 poster
- 社媒传播图卡
- 有明确固定视觉语法的单页成品

代表参考：

- `visual-note-card`

如果一开始没法判断，优先先按分析驱动型走；只有在版式语法已经很明确时，再走模板驱动型。

## 输入

- 主题
- 原始内容来源
  - 文章
  - 报告
  - 粘贴文本
  - 已整理要点
- 核心数字、引用、不能改写的文案
- 目标平台或画幅
- 风格方向
- 风格来源
  - 用户指定风格
  - 用户提供 `DESIGN.md`
  - 用户详细描述
  - 从 `ref/design-md/` 本地参考库中选起点
- 推荐在统一 spec 中继续固化 `design_md`，并在最终 Skill 中输出 `references/design.md`
- 产物要求
  - HTML
  - PNG
  - 两者都要

## 输出

- 选择哪条信息图路径
- 结构化中间层
- layout / style 或固定模板建议
- 文案保真和数字保真要求
- 输出链路与降级策略

## 最佳实践

### 1. 先做内容中间层，不直接做图

这类任务最稳定的做法都不是“原文 -> 最终图”。
至少先形成一个中间层。

进入视觉设计前，再加一条硬规则：

- 风格来源没定时，只允许做结构层和 layout 家族判断，不直接做高保真视觉稿
- 用户没有自己的品牌规范时，优先让用户从 `ref/design-md/` 里选一个起点
- 首批官方预设建议优先在 IBM、Stripe、Notion、Framer、Figma、Nothing、Apple 中选择

推荐最小中间层：

- `analysis.md`
- `structured-content.md`

建议内容：

#### `analysis.md`

- 主题
- 受众
- 内容类型
- 复杂度
- learning objectives
- verbatim data points
- 推荐 layout × style

#### `structured-content.md`

- 标题
- Overview
- Learning Objectives
- section 列表
- 每个 section 的 key concept / content / visual element / text labels
- 设计约束

### 2. layout 和 style 分开处理

`baoyu-infographic` 证明了信息图里“信息结构”和“视觉美学”不能混在一起。

建议默认拆成两个维度：

- `layout_family`
  - timeline
  - dashboard
  - comparison
  - process
  - listicle
  - magazine
- `visual_style`
  - clean-minimal
  - dark-techy
  - warm-editorial
  - bold-graphic
  - 其他风格族

先决定结构，再决定美学，稳定性会高很多。

### 3. 先确认 outline，再确认视觉

开放输入任务里，不要直接跳到视觉稿。
推荐顺序：

1. outline
2. layout
3. style source
4. style
5. 插画或图标
6. 输出格式

这条规则来自 `article-to-infographic`，很适合高不确定性任务。

### 4. 固定模板类任务要用“海报语法”

如果任务更像知识卡片或传播图卡，优先采用固定骨架，而不是做开放式版式探索。

可复用的模板语法来自 `visual-note-card`：

- top bar
- 标题区
- framework row
- 双栏正文区
- bottom highlight
- footer

这种结构特别适合：

- 知识笔记
- 学习卡片
- 单页分享图
- 观点型海报

## 如何拆解信息

### 分析驱动型

优先抽这些元素：

- 标题与副标题
- 关键统计
- 关键观点
- 原文引语
- 比较维度
- 时间顺序
- 自然分类
- 关键实体

再根据内容信号决定更适合：

- 时间线
- 数据仪表盘
- 对比图
- 流程图
- 卡片网格
- editorial 混排

### 模板驱动型

优先提炼：

- 一个强观点 thesis
- 一个 2 到 6 列 framework
- 左侧 narrative
- 右侧 numbered insights
- 一条可传播的 bottom formula

## 如何组织大纲

### 推荐流程

1. 定标题和副标题
2. 定 1 到 3 个 learning objectives
3. 拆 3 到 7 个 section
4. 为每个 section 指定：
   - 内容
   - 视觉元素
   - text labels
5. 确认最终是：
   - 单条 narrative poster
   - 多 section infographic
   - 知识卡片

### 推荐数量控制

- 单张信息图建议承载 3 到 7 个核心点
- 超过这个范围时，优先拆图或改做 deck
- 长文本、复杂表格、细密标签不适合直接硬塞进一张图

## 如何写文案

### 默认规则

- 不新增事实
- 不改写统计
- 引语尽量 verbatim
- 标题和标签优先服务视觉组织
- 文案要短、准、可扫描

### 模板驱动型的额外规则

- thesis 要有态度
- framework 名称要易记
- narrative 区偏“故事与转变”
- insights 区偏“编号与结论”
- bottom formula 要可传播

## 如何排版

### 信息图 HTML

建议把 HTML poster 当正式交付链路，而不是临时预览。

推荐排版规则：

- 总布局优先 CSS Grid
- 组件级布局用 Flex
- 单页宽度明确
- 间距紧凑
- 不做松散通用卡片拼盘
- 需要 `@media print`
- 需要 `prefers-reduced-motion`

### 视觉规则

- 数字要显著
- 图表和标签必须可核对
- 重要层级用标题、对比色、编号和区块来做
- 不要用通用 AI 风格默认稿

## 如何输出美观 HTML 和 PNG

### HTML

推荐把 HTML 作为主产物，因为这条链路最适合：

- 固定高保真版式
- 浏览器内检查
- 打印 PDF
- 再导出 PNG

### PNG

推荐走单独导出器，不要把 PNG 当作生成主链路。

当前可借鉴的稳定做法：

- Playwright 打开本地 HTML
- 强制 reveal / counter 到最终状态
- 截 `.poster` 或全页

推荐单独表达为：

- `html_poster`
- `png_export`

## 推荐执行方向

### 方向 1：HTML poster 优先

适合：

- 信息密度高
- 文案和数字需要可控
- 需要后续转 PNG 或 PDF

### 方向 2：图像生成优先

适合：

- 更偏氛围和视觉冲击
- 文本量较少
- 社媒传播图

这时仍然要先固定文案和数字源，不要把长文本完全交给位图生成。

### 方向 3：改做 deck 或可编辑版式

适合：

- 文本极多
- 表格极复杂
- 后续多人协作改稿

这时应转向 `presentation-generation` 或更强的可编辑版式工具。

## 边界

- 不把长篇报告硬做成一张图
- 不把复杂交互图表当成静态信息图
- 不默认位图可以承接高精度长文本
- 不把 HTML poster 和可编辑 deck 混成一个产物类型

## 降级策略

- 信息还没整理好时，先交付 `analysis.md` 和 `structured-content.md`
- 版式没定时，先输出 outline 和 layout 建议
- 文本太多时，改做 deck
- 风格没定时，先做低保真结构图

## 与主流程的关系

这个能力最适合挂在 `frontend_design` 主域下，也可以作为 `document_artifacts` 的补充能力出现。
当任务属于更广义的视觉叙事产物时，先走 `structured-visual-storytelling`，再落到这里。

如果进入正式设计比较，建议同时回看：

- [clawhub-infographic-ppt-deep-dive/reference-skill-analysis.md](/Users/tanshow/Developer/cocoloop-skill-factory-dev/cocoloop-skill-factory/output/clawhub-infographic-ppt-deep-dive/reference-skill-analysis.md)
- [clawhub-infographic-ppt-deep-dive/design-summary.md](/Users/tanshow/Developer/cocoloop-skill-factory-dev/cocoloop-skill-factory/output/clawhub-infographic-ppt-deep-dive/design-summary.md)
