# 结构化视觉叙事产物

## 适用场景

这个能力用于批量生产各类“视觉叙事型” Skill，而不只是一种具体产物。

它适合承接：

- `.pptx`、HTML slides、答辩稿、汇报 deck
- 网页信息图、可滚动 narrative 页面、单页 poster
- 展示图、说明页、知识海报、报告型页面
- 后续还可能扩展到海报、长图、报告页等同类产物

这些产物的共同点不是格式，而是：

- 都要先有结构化内容层
- 都要先确定 `design_md`
- 都要控制文字层级
- 都要显式加入信息图元素
- 都要区分展示版、可编辑版和位图版输出

## 这层负责什么

这一层不直接替代 `presentation-generation` 或 `infographic-generation`。
它负责先定义共享主线，再把具体落地交给不同 adapter。

默认主线：

1. 先把原始内容压成 `story_units`
2. 再确认 `design_md`
3. 再检查文字层级
4. 再规划信息图元素
5. 再选择输出 adapter
6. 最后才进入具体渲染

如果跳过上面任一步，后续很容易退化成“把一堆字塞进 PPT”或“把长文硬排成信息图”。

## 通用输入

- 主题
- 原始材料
- 目标受众
- 叙事目标
- 输出载体
- 风格来源
- 是否需要可编辑性交付

## 通用输出

- 结构化叙事单元
- 设计约束
- 文字层级规则
- 信息图元素要求
- adapter 选择结果
- 验收与降级策略

## 强制门槛

### 1. 先结构化，再做视觉

无论目标产物是什么，都不允许“原文 -> 最终视觉稿”直接跳转。
至少要先形成一个内容中间层。

建议最小中间层：

- `story-units.md`
- `adapter-plan.md`

### 2. 必须有 `design_md`

只要任务进入正式视觉输出，就要继续补：

- `design_md.enabled`
- `design_md.source_mode`
- `design_md.preset_id` 或 `design_md.user_provided_ref`

没有 `design_md` 时，可以继续做结构方案，但不能直接进入高保真视觉输出。

### 3. 文字层级必须显式设计

不允许所有文字都在同一层级。
至少要区分：

- kicker 或章节标签
- 主标题
- 一句话结论或摘要
- 正文说明
- 数字或短句强调
- 注释或边界说明

### 4. 信息图元素不是点缀，而是主内容的一部分

不能把图表、流程、对比卡当作“有空再加”的视觉装饰。
对于视觉叙事产物，信息图元素本身就是内容表达方式。

默认至少规划：

- metric cards
- process flow
- comparison blocks
- timeline
- matrix
- chart
- module diagram

### 5. 输出必须走 adapter，而不是一层包打天下

同一套共享主线可以落到不同输出：

- `ppt`
- `web_infographic`
- `showcase_graphic`
- 后续还可扩到 `poster`、`report_page`

这一步决定：

- 版式语法
- 可编辑性边界
- 交付格式
- 测试方式

## 推荐读取顺序

1. [shared-rules.md](./shared-rules.md)
2. [output-adapters.md](./output-adapters.md)
3. 再进入具体 adapter：
   - `../presentation-generation/index.md`
   - `../infographic-generation/index.md`

## 与现有能力的关系

- `presentation-generation`
  现在作为 `ppt` adapter 理解
- `infographic-generation`
  现在作为 `web_infographic` 和 `showcase_graphic` adapter 理解

后续新增视觉叙事类能力时，也优先挂在这条主线下，不再各自重新发明完整流程。
