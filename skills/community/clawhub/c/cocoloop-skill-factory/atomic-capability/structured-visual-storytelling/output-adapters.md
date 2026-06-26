# 输出适配器

## 目标

共享主线只负责把内容和视觉约束收口清楚。
真正落地到哪种产物，要通过 adapter 决定。

## 当前 adapter

### 1. `ppt`

默认落到：

- `presentation-generation`

适合：

- 汇报型 `.pptx`
- HTML slides
- 答辩稿
- 培训 deck

重点：

- cover / content / closing 分页明确
- 可编辑性优先
- 需要 speaker notes 时单独处理

### 2. `web_infographic`

默认落到：

- `infographic-generation`

适合：

- HTML poster
- 滚动 narrative infographic
- 知识可视化页面

重点：

- 结构先于风格
- 内容块要可扫描
- 适合继续导出 PNG / PDF

### 3. `showcase_graphic`

默认也可落到：

- `infographic-generation`

适合：

- 单页展示图
- 传播图卡
- 模块化功能说明图

重点：

- 单页强主张
- 信息密度可控
- 位图导出优先

## 后续预留 adapter

- `poster`
- `report_page`
- `interactive_story`

## 选择规则

1. 先看输出是否必须可编辑
2. 再看是否需要浏览器内播放或滚动
3. 再看文字量和信息密度
4. 最后才决定单页还是多页

## 适配器输出建议

每个 adapter 都继续明确：

- 输出格式
- 渲染语法
- 文字层级实现方式
- 信息图元素最低配额
- 降级路径
