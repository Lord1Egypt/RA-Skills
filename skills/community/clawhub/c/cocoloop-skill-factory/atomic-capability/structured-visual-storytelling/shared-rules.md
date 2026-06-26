# 共享规则

## 1. 内容中间层

### 最小要求

所有视觉叙事产物都先整理成 `story_units`，再讨论视觉。

建议字段：

- `unit_id`
- `unit_role`
- `key_message`
- `evidence`
- `visual_intent`
- `text_priority`

### 常见 `unit_role`

- `cover`
- `hook`
- `problem`
- `method`
- `comparison`
- `result`
- `insight`
- `closing`

## 2. 文字层级规则

### 最小层级

至少区分：

- `kicker`
- `headline`
- `summary`
- `body`
- `metric`
- `annotation`

### 反模式

- 整页只有同字号的 bullet list
- 标题和正文只靠粗体区分
- 数字和结论埋在正文里
- 注释与主结论争抢视觉中心

## 3. 信息图元素规则

### 最小要求

每个内容页或内容面板都应至少规划一种非纯文本表达。

### 常见元素

- metric cards
- process flow
- comparison blocks
- timeline
- matrix
- chart
- module diagram

### 选择顺序

1. 先看信息关系是什么
2. 再选元素类型
3. 再决定视觉风格

不要反过来先决定“要做一个酷炫图”，再去塞内容。

## 4. `design_md` 规则

只要任务进入高保真视觉阶段，就补齐：

- `design_md.enabled`
- `design_md.applies_to`
- `design_md.source_mode`
- `design_md.preset_id` 或 `design_md.user_provided_ref`
- `design_md.custom_style_notes`

如果用户没有自带品牌规范，默认先从官方预设里选起点。

## 5. 输出边界

统一先判定输出属于哪类：

- 可编辑版
- 展示版
- 位图版

然后再选 adapter。

### 可编辑版

适合：

- `.pptx`
- HTML slides
- HTML poster

### 展示版

适合：

- 演示页
- 滚动 narrative 页面
- 浏览器直接播放的 deck

### 位图版

适合：

- 分享图
- 展示图
- 社媒传播图卡

## 6. 测试要求

统一检查：

- 是否退化成堆字
- 是否真的有文字层级
- 是否真的有信息图元素
- 是否和 `design_md` 一致
- 是否符合目标输出的可编辑性边界
