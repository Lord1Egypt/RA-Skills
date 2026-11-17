# V4 Template 通用化合同

## 范围

本合同只适用于 Template 路线。麦肯锡模板、MGI 报告以及其他真实样本只用于回归，
不得成为生产代码中的组件 ID、颜色、页码、形状名称或版式分支。

支持目标是结构正常、可由 PPTX 对象模型读取的模板。加密/损坏文件、ActiveX、OLE、
宏对象、不可拆解 SmartArt、整页栅格模板和缺失外部资产必须明确报告限制或拒绝，不能
伪装成可复用原生组件。

## 每模板动态证据

每次上传模板都重新提取：

- 页面尺寸、对象类型、几何和密度；
- 主题色语义角色、常用填充、字体和字号层级；
- reviewed 组件的语义、拓扑、字段、数量和数据容量；
- 组件内容边界、装饰边界、背景对象和背景面积；
- 可用响应式方式、原生宽高比、支持宽高比和最低内容密度；
- 封面、章节页和尾页是否存在真正可独立成页的 recipe。

`engine.template_component_adaptation` 从当前 Atlas 的 reviewed 对象角色和标准化几何生成
`adaptation_contract`。默认策略保守：大于内容边界的页面级/行级背景在复用时剥离；
组件级容器跟随内容重排；只支持等比缩放的组件不能声称适配一个必须铺满的异形区域。
reviewer 可以覆盖推断，但必须提供理由，且覆盖仍绑定当前模板对象。

## 页面适配

组件选择同时检查：

- 目标区域宽高比是否位于组件支持范围；
- 计划是否要求铺满，组件是否具备相应重排能力；
- 每个元素的可见标签是否达到最低内容量；
- 定量组件是否具有足够数字标注；
- 主组件要求的解释、含义或其他 companion 是否存在；
- 背景是语义容器还是源页面遗留底板。

适配失败时应换用其他 feasible 组件或由模型按当前模板语法绘制新原生组件，不得机械
拉伸、缩小字体或保留无意义背景。

## 真实渲染节奏

`engine.template_visual_fingerprint` 从真实渲染 PNG 计算几何占用指纹，颜色不参与布局
身份，左右镜像视为同一视觉骨架。因此仅把 chart-left 改名为 chart-right，或更换 recipe
名称，不能伪造布局多样性。

普通主叙事中：

- 同一真实视觉骨架不得连续出现三页；
- 单一骨架原则上不得超过正文页的 25%；
- 明确的对比系列只有在声明统一比较锚点和统一尺度时才可共用网格；
- 主叙事中的同一系列最多五页，更多内容应合并为小多图或进入附录。

## 跨模板验收

通用能力至少以以下矩阵验证：

1. 明亮咨询风 16:9；
2. 深色科技风 16:9；
3. 极简商务风 4:3；
4. 图表密集模板；
5. 图片主导模板；
6. 中文政企汇报模板；
7. 开发期间未绑定任何品牌名称的保留模板。

矩阵使用同一 Atlas、适配、编排和 QA 代码。测试必须证明：不同尺寸、背景、主色和对象
组合不会触发品牌特判；Template 新模块也不得被 Bespoke 或 Standard 导入。

## Fail-close 代码

- `TEMPLATE_COMPONENT_TARGET_ASPECT_UNSUPPORTED`
- `TEMPLATE_COMPONENT_CONTENT_DENSITY_LOW`
- `TEMPLATE_COMPONENT_LABEL_DENSITY_LOW`
- `TEMPLATE_COMPONENT_NUMERIC_ANNOTATION_LOW`
- `TEMPLATE_COMPONENT_COMPANION_REQUIRED`
- `TEMPLATE_RENDERED_LAYOUT_CONSECUTIVE_LIMIT`
- `TEMPLATE_RENDERED_LAYOUT_OVERUSED`
- `TEMPLATE_COMPARISON_SERIES_ANCHOR_REQUIRED`
- `TEMPLATE_SERIES_MAIN_NARRATIVE_TOO_LONG`
- `TEMPLATE_SERIES_HERO_REPETITION`

这些门禁只属于 Template 路线。
