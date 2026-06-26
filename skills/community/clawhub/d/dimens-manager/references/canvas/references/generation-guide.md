# dimens-manager 画布章节 AI 生成规范

## 1. 输出结构

AI 生成画布时，目标不是生成说明文，而是生成能被 `CanvasBoard` 渲染和继续编辑的图数据：

```json
{
  "nodes": [],
  "edges": [],
  "viewport": { "x": 0, "y": 0, "zoom": 1 },
  "version": "1.0",
  "timestamp": 1777800000000,
  "meta": { "source": "dimens-manager-canvas" }
}
```

画布表达的是可视化说明和协作，不直接代表工作流引擎已创建、发布或绑定项目。可执行工作流仍进入 `dimens-manager/references/workflow/overview.md`。

## 2. 节点生成硬规则

- 每个节点必须说明业务职责：触发、输入、处理、判断、人工处理、数据存储、文档沉淀、展示、分组或结束。
- 每个节点必须选择能表达职责的 `type`，不要把所有节点都画成 `RECTANGLE`。
- `data.label` 写业务动作或判断条件，不写“节点1 / 步骤2 / 处理”这类空泛名称。
- 节点说明放在 `data.text`、`data.markdownContent` 或整图 `meta.nodeGuide` 中；不要依赖前端一定渲染自定义字段。
- 条件节点必须使用 `DIAMOND`，并给每条分支边写 `label`，如“是 / 否 / 通过 / 驳回 / 命中 / 未命中”。
- 辅助节点如 `SECTION`、`TEXT`、`STICKY_NOTE`、`IMAGE` 不代表真实流程步骤，不能替代主流程节点。

## 3. 流程节点选型

先定义节点的业务职责，再选择节点类型。每个节点必须说明业务职责，否则 AI 只能画出看起来像流程、实际不可读的图。

| 业务职责 | 推荐节点类型 | 典型 label | 使用要求 |
| --- | --- | --- | --- |
| 触发、开始、结束、普通动作 | `RECTANGLE` | `客户提交线索`、`关闭工单` | 一个节点只写一个动作 |
| 输入、输出、上传、外部返回 | `PARALLELOGRAM` | `销售填写线索表单`、`接口返回审批结果` | 表示数据进入或输出流程 |
| 条件判断、审批、分流 | `DIAMOND` | `是否命中高风险规则` | 至少两条出边，边上写“是/否”等分支 |
| 数据库、多维表、业务对象沉淀 | `CYLINDER` | `写入客户表`、`读取库存数据` | 表示读写数据，不表示人工动作 |
| 文档、合同、报告、知识条目 | `DOCUMENT` | `生成服务报告`、`沉淀知识条目` | 表示文档产物 |
| 长说明、SOP、策略文本 | `MARKDOWN` | `审批策略说明` | 使用 `data.markdownContent` 放正文 |
| 阶段、泳道、区域分组 | `SECTION` | `售前阶段`、`交付阶段` | 只做分组背景，不作为流程步骤 |
| 备注、风险、口径补充 | `TEXT` / `STICKY_NOTE` | `风险提示` | 辅助说明，通常不接主流程边 |
| 方案树、分类树、模块拆解 | `MINDMAP` | `CRM 能力拆解` | 用 `mindMapRoot`，不用于严格时序 |
| 画布内 AI 智能体生成 | `CUSTOM_AGENT` | `根据前置内容生成报告` | 只在需要用户点击运行并生成后续节点时使用，不作为普通业务步骤 |
| 嵌入多维表视图 | `EMBEDDED_SHEET` | `客户列表视图` | 需要 `embeddedSheet.sheetId/viewId` |
| 图片、视频、SVG、信息图 | `IMAGE` / `VIDEO` / `SVG` / `INFOGRAPHIC` | `增长漏斗信息图`、`流程概览图` | 展示材料；复杂信息展示优先用 `INFOGRAPHIC` |

支持的节点类型包括：`RECTANGLE`、`CIRCLE`、`TRIANGLE`、`DIAMOND`、`PARALLELOGRAM`、`HEXAGON`、`CYLINDER`、`CLOUD`、`DOCUMENT`、`TEXT`、`STICKY_NOTE`、`GROUP`、`SECTION`、`MINDMAP`、`IMAGE`、`VIDEO`、`CUSTOM_AGENT`、`MARKDOWN`、`CLOCK`、`SVG`、`INFOGRAPHIC`、`EMBEDDED_SHEET`。不要发明前端无法识别的新类型。

## 4. 节点类型详解

### `RECTANGLE` 普通动作节点

- 作用：表达一个业务动作、系统处理或明确状态。
- 用法：`data.label` 使用“动词 + 对象”，如“创建客户档案”“分配服务工程师”。
- 不要：把多个动作写在同一个矩形里，如“提交、审核、归档”。

### `PARALLELOGRAM` 输入输出节点

- 作用：表达表单提交、文件上传、外部接口返回、流程输出。
- 用法：放在流程入口、数据采集点或输出交付点。
- 推荐字段：`data.label` 写输入/输出内容，`data.text` 可写来源或去向。
- 不要：把内部处理步骤画成输入输出。

### `DIAMOND` 判断节点

- 作用：表达“是否满足条件”的分支。
- 用法：`data.label` 写成问题句，如“是否需要主管审批”；每条出边都写 `label`。
- 不要：只有一条出边，或边没有“是/否/通过/驳回”等含义。

### `CYLINDER` 数据沉淀节点

- 作用：表达数据库、多维表、业务对象、日志或知识库的读写。
- 用法：写入类 label 用“写入...表”，读取类 label 用“读取...数据”。
- 不要：用它表达普通人工操作；人工操作仍用 `RECTANGLE`。

### `DOCUMENT` 与 `MARKDOWN` 文档节点

- `DOCUMENT`：表示合同、报告、工单回执、知识条目等文档产物。
- `MARKDOWN`：表示较长说明、SOP、策略规则，正文放 `data.markdownContent`。
- 不要：把主流程动作藏进长文档里，主流程仍要拆成节点。

### `SECTION` 分组节点

- 作用：表达阶段、泳道、业务域背景，如“售前阶段”“财务审批”。
- 用法：尺寸通常大于普通节点，包住一组节点，可不连边。
- 不要：把 `SECTION` 当成一个流程步骤。

### `TEXT` / `STICKY_NOTE` 说明节点

- 作用：补充风险、规则、口径和待确认事项。
- 用法：放在相关节点旁边，避免干扰主流程连线。
- 不要：把它们当作必须执行的流程环节。

### `MINDMAP` 思维导图节点

- 作用：表达非线性的分类、方案拆解、能力树。
- 用法：使用 `data.mindMapRoot`，层级控制在 2-3 层。
- 不要：用于审批流、工单流这类严格时序流程。

### `CUSTOM_AGENT` 画布内 AI 智能体节点

- 作用：画布内的 AI 智能体节点，用来读取上游节点内容，并生成新的 Markdown、思维导图或信息图节点。
- 用法：仅在用户明确需要“在画布里放一个可运行的 AI 智能体”时使用；`data.label` 写成用户给智能体的指令，`data.agentOutputType` 可用 `MARKDOWN`、`MINDMAP`、`INFOGRAPHIC`。
- 不要：不要把它当成普通“AI 分析步骤”滥用；普通业务处理、系统分类、规则判断仍优先用 `RECTANGLE` 或 `DIAMOND`。也不要把它当成后端可执行工作流节点。

### `EMBEDDED_SHEET` 嵌入表格节点

- 作用：在画布中展示项目内多维表视图。
- 用法：必须提供 `data.embeddedSheet.sheetId` 和 `data.embeddedSheet.viewId`，可附带 `sheetName/viewName`。
- 不要：没有真实表格视图时虚构 ID。

### 展示类节点

- `INFOGRAPHIC` 是复杂信息展示的强表达节点，尤其适合 PPT 页、方案页、数据解读页、流程概览页、对比分析页。
- `IMAGE`、`VIDEO`、`SVG` 用于已有素材或静态资产；如果用户给的是需要结构化表达的信息，应优先考虑 `INFOGRAPHIC`。
- `CLOCK` 适合表示计时、倒计时、SLA 提醒。
- `CLOUD` 可表示外部云服务或第三方系统，`HEXAGON` 可表示能力模块或服务组件。

### `INFOGRAPHIC` 信息图节点

- 作用：把复杂信息、数据、知识、流程、对比、层级、关系压缩成强视觉表达。它比普通 `TEXT`、`MARKDOWN`、`RECTANGLE` 更适合做 PPT 里的核心展示内容。
- 用法：当用户需要展示复杂效果、方案亮点、指标趋势、业务链路、对比分析、SWOT、象限、组织结构、路线图、系统关系、数据图表时，优先使用 `INFOGRAPHIC`。
- 字段：必须在 `data.infographicSyntax` 中写 AntV Infographic DSL；不要只写 `data.label`。
- 尺寸：默认 `400 x 300`；PPT 页核心信息图建议 `720 x 420`、`800 x 460` 或按页面留白调整。
- 不要：不要把复杂信息拆成大量小 `RECTANGLE` 或长 `MARKDOWN`；如果这些内容本质上是“给用户一眼看懂”的展示信息，应使用 `INFOGRAPHIC`。

`INFOGRAPHIC` 节点的 `data.infographicSyntax` 必须遵循：

- 第一行必须是 `infographic <template-name>`。
- 使用 `data` / `theme` 块，块内使用两个空格缩进。
- 只使用一个与模板匹配的主数据字段，例如 `lists`、`sequences`、`compares`、`values`、`root`、`nodes`。
- 列表、步骤、节点、对比项等主要数据项默认补 `icon`。
- `palette` 使用裸颜色值，不加引号、不加逗号，例如 `palette #3b82f6 #8b5cf6 #f97316`。
- 用户输入中文时，`title`、`desc`、`label` 等继续用中文；用户输入英文时继续用英文，不要自动翻译。

常用模板选择：

| 信息结构 | 推荐模板 |
| --- | --- |
| 并列要点、卖点、能力清单 | `list-row-horizontal-icon-arrow`、`list-grid-badge-card`、`list-grid-ribbon-card` |
| 阶段步骤、推进路径、路线图 | `sequence-ascending-steps`、`sequence-timeline-simple`、`sequence-roadmap-vertical-simple` |
| 多角色或多系统交互 | `sequence-interaction-default-badge-card`、`sequence-interaction-default-rounded-rect-node` |
| 双方对比、方案对比、前后对比 | `compare-binary-horizontal-simple-fold`、`compare-binary-horizontal-badge-card-arrow` |
| SWOT / 象限分析 | `compare-swot`、`compare-quadrant-quarter-simple-card` |
| 层级树、组织结构、能力树 | `hierarchy-tree-curved-line-rounded-rect-node`、`hierarchy-structure` |
| 趋势、数值对比、占比 | `chart-line-plain-text`、`chart-column-simple`、`chart-pie-donut-plain-text` |
| 系统关系、依赖链路 | `relation-dagre-flow-tb-simple-circle-node`、`relation-dagre-flow-tb-badge-card` |

可渲染字段模板：

```json
{
  "id": "growth_infographic",
  "type": "INFOGRAPHIC",
  "position": { "x": 72, "y": 170 },
  "positionAbsolute": { "x": 72, "y": 170 },
  "width": 760,
  "height": 420,
  "selected": false,
  "dragging": false,
  "style": { "width": 760, "height": 420 },
  "data": {
    "label": "增长路径信息图",
    "backgroundColor": "#ffffff",
    "borderColor": "#e2e8f0",
    "borderWidth": 1,
    "textColor": "#111827",
    "fontSize": 14,
    "width": 760,
    "height": 420,
    "borderRadius": 16,
    "align": "center",
    "verticalAlign": "center",
    "infographicSyntax": "infographic list-row-horizontal-icon-arrow\ndata\n  title 产品增长要点\n  desc 聚焦获客、转化、复购三个阶段\n  lists\n    - label 获客\n      desc 多渠道投放与内容触达\n      icon rocket launch\n    - label 转化\n      desc 优化路径并减少流失\n      icon chart line\n    - label 复购\n      desc 会员权益与分层运营\n      icon repeat\ntheme\n  palette #3b82f6 #8b5cf6 #f97316"
  }
}
```

## 5. 节点字段写法

节点必须按“可渲染字段模板”生成。不要只给 `id/type/position/data.label`，否则容易出现节点不可见、尺寸丢失或拖拽异常。

视觉规则：

- `data.backgroundColor` 必须使用淡色或 `transparent`，禁止直接使用黑色、深灰、深蓝等深色背景。
- 流程节点默认推荐 `#ffffff`、`#f8fafc`、`#eff6ff`、`#ecfdf5`、`#fff7ed`、`#fefce8`。
- `DIAMOND` 判断节点可用 `#fff7ed` 或 `#fef3c7` 这类浅橙 / 浅黄。
- 数据沉淀节点可用 `#f8fafc` 或 `#eef2ff`。
- 文字颜色可以使用 `#111827` 这类深色，用来保证浅背景上的可读性。
- 不要把深色用作节点背景；如果需要强调，用边框色、图标、标签或信息图主题色表达。

```json
{
  "id": "lead_submit",
  "type": "PARALLELOGRAM",
  "position": { "x": 0, "y": 0 },
  "positionAbsolute": { "x": 0, "y": 0 },
  "width": 150,
  "height": 80,
  "selected": false,
  "dragging": false,
  "style": { "width": 150, "height": 80 },
  "data": {
    "label": "销售填写线索表单",
    "backgroundColor": "#ffffff",
    "borderColor": "#d1d5db",
    "borderWidth": 1,
    "textColor": "#111827",
    "fontSize": 14,
    "width": 150,
    "height": 80,
    "borderRadius": 12,
    "align": "center",
    "verticalAlign": "center",
    "text": "职责：采集客户来源、联系人、需求摘要"
  }
}
```

关键字段：

- `id`：稳定英文短名，后续边通过它连接。
- `type`：用来表达节点语义，不只是视觉形状。
- `position`：React Flow 相对坐标；无父节点时和 `positionAbsolute` 保持一致。
- `positionAbsolute`：绝对坐标；生成时必须填，避免画布恢复或检索时坐标缺失。
- `style.width/style.height`、顶层 `width/height`、`data.width/data.height`：三处保持一致。普通节点标准尺寸 `150x80`。
- `data.label`：用户第一眼看到的业务动作。
- `data.backgroundColor`：节点背景色，只允许淡色或 `transparent`。
- `data.align` / `data.verticalAlign`：普通流程节点默认 `center/center`。
- `data.borderRadius`：普通节点默认 `12`，开始/结束或强调节点可用 `16`。
- `data.text` / `data.markdownContent`：放节点说明、规则、SOP。
- `selected` / `dragging`：保存型 JSON 默认都填 `false`。

标准尺寸：

| 节点类型 | 推荐尺寸 |
| --- | --- |
| 普通流程节点 | `150 x 80` |
| 判断节点 `DIAMOND` | `150 x 100` |
| 文档节点 `DOCUMENT` | `180 x 100` |
| `MARKDOWN` | `400 x 300` 或更大 |
| `INFOGRAPHIC` | 默认 `400 x 300`，PPT 核心展示建议 `720 x 420` 或更大 |
| `SECTION` | 按包裹范围设置，通常不小于 `800 x 400` |
| PPT 页面分区 `SECTION` | 固定 16:9，推荐 `1280 x 720` |
| `EMBEDDED_SHEET` | `720 x 420` |

## 6. 连线设计

边必须按“可渲染字段模板”生成。不要只给 `id/source/target/type/label`。

```json
{
  "id": "edge_start_check",
  "source": "start",
  "target": "check",
  "sourceHandle": "source-bottom",
  "targetHandle": "target-top",
  "type": "default",
  "animated": false,
  "selected": false,
  "zIndex": 0,
  "markerEnd": { "type": "arrowclosed", "color": "#94a3b8" },
  "style": { "stroke": "#94a3b8", "strokeWidth": 2 }
}
```

规则：

- 主流程边不要交叉，默认从 `source-bottom` 连到 `target-top`。
- 横向回退或人工兜底路径可用 `source-right -> target-right` 或 `source-left -> target-left`，并调整布局避免重叠。
- 普通直线边用 `type: "default"`；分支、回退、跨层级连接可用 `type: "smoothstep"`。
- 条件分支边必须在 `label` 上标注“是 / 否 / 通过 / 驳回”。
- 所有边必须带 `markerEnd: { "type": "arrowclosed" }` 和 `style.stroke/style.strokeWidth`。
- 保存型 JSON 默认 `animated: false`、`selected: false`、`zIndex: 0`；只有需要强调运行中或高亮时才改。
- 连线方向必须与业务时序一致。
- 不要把多个业务动作挤进一条边，动作应该放在节点里。

## 7. 布局规则

推荐左到右布局：

- 起点：`x=0`
- 普通节点标准尺寸：`width=150`、`height=80`
- 普通步骤间隔：`x += 260`
- 分支节点上下间隔：`y += 160`
- 异常或退回路径放在主流程下方

推荐自上而下布局：

- 起点：`y=0`
- 普通节点标准尺寸：`width=150`、`height=80`
- 普通步骤间隔：`y += 160`
- 分支节点左右间隔：`x += 260`

## 8. PPT / 演示稿画布规则

当用户说“创建 PPT”“生成演示稿”“做一套汇报幻灯片”“把方案做成 PPT 画布”时，必须按 PPT 画布结构生成，而不是把内容散落在无限画布上。

硬规则：

- PPT 画布必须是 `16:9` 比例。
- 最外层必须是 `SECTION` 分区；一页 PPT 对应一个 `SECTION`。
- 每个 PPT 页面分区推荐尺寸固定为 `1280 x 720`，也可等比放大或缩小，但 `width / height` 必须等于 `16 / 9`。
- 所有标题、正文、图表、流程、图片、备注等内容节点都必须在对应页面 `SECTION` 内实现。
- PPT 页面里只要涉及复杂信息展示、指标趋势、方案对比、流程概览、路径拆解、SWOT、象限或系统关系，优先使用 `INFOGRAPHIC` 节点承载，而不是堆叠大量 `TEXT` / `RECTANGLE`。
- 页面内容节点必须写 `parentNode: "<slide_section_id>"`，`position` 使用相对该页分区的坐标，`positionAbsolute` 使用画布绝对坐标。
- 页面分区节点要排在 `nodes` 数组前面，保证作为底层容器渲染。
- 页面之间建议纵向排列，默认 `y += 820`，也就是 `720` 页面高度加 `100` 页间距。
- PPT 页面之间通常不需要连边；如果要表达跨页导航，可以用轻量 `TEXT` 节点标注，不要用主流程边把所有页串起来。
- 不要把 `SECTION` 当成幻灯片中的普通内容块；PPT 场景下它就是页面画布。
- 不要让内容节点超出页面分区边界；标题、正文、图表都必须留在 `SECTION` 的 `0 <= x <= 1280`、`0 <= y <= 720` 范围内，并预留页边距。

PPT 页面分区模板：

```json
{
  "id": "slide_01",
  "type": "SECTION",
  "position": { "x": 0, "y": 0 },
  "positionAbsolute": { "x": 0, "y": 0 },
  "width": 1280,
  "height": 720,
  "selected": false,
  "dragging": false,
  "style": { "width": 1280, "height": 720 },
  "data": {
    "label": "第 1 页：方案总览",
    "backgroundColor": "#ffffff",
    "borderColor": "#e5e7eb",
    "borderWidth": 1,
    "textColor": "#111827",
    "fontSize": 16,
    "width": 1280,
    "height": 720,
    "borderRadius": 0,
    "align": "left",
    "verticalAlign": "top",
    "text": "PPT 页面分区，16:9"
  }
}
```

页面内内容节点模板：

```json
{
  "id": "slide_01_title",
  "type": "TEXT",
  "parentNode": "slide_01",
  "position": { "x": 72, "y": 56 },
  "positionAbsolute": { "x": 72, "y": 56 },
  "width": 520,
  "height": 64,
  "selected": false,
  "dragging": false,
  "style": { "width": 520, "height": 64 },
  "data": {
    "label": "客户增长方案",
    "backgroundColor": "transparent",
    "borderColor": "transparent",
    "borderWidth": 0,
    "textColor": "#111827",
    "fontSize": 36,
    "width": 520,
    "height": 64,
    "borderRadius": 0,
    "align": "left",
    "verticalAlign": "center",
    "text": "客户增长方案"
  }
}
```

多页布局示例：

| 页码 | SECTION id | position / positionAbsolute | width x height |
| --- | --- | --- | --- |
| 第 1 页 | `slide_01` | `{ "x": 0, "y": 0 }` | `1280 x 720` |
| 第 2 页 | `slide_02` | `{ "x": 0, "y": 820 }` | `1280 x 720` |
| 第 3 页 | `slide_03` | `{ "x": 0, "y": 1640 }` | `1280 x 720` |

PPT 画布生成后自检：

- 是否每一页都有一个 `type: "SECTION"` 的页面分区。
- 是否每个页面分区都是 `16:9`，推荐 `1280 x 720`。
- 是否所有非页面内容节点都有 `parentNode` 指向某个 `SECTION`。
- 是否复杂展示内容优先使用了 `INFOGRAPHIC`，并在 `data.infographicSyntax` 中写入合法 AntV Infographic 语法。
- 是否所有内容节点的相对 `position` 落在所属页面分区内。
- 是否所有页面分区和内容节点仍满足可渲染字段模板。

## 9. 常见业务流程模板

审批流程：

1. `PARALLELOGRAM` 提交申请。
2. `RECTANGLE` 系统校验字段和权限。
3. `DIAMOND` 是否需要主管审批。
4. `RECTANGLE` 主管审批。
5. `DIAMOND` 是否通过。
6. `CYLINDER` 写入审批结果。
7. `DOCUMENT` 生成审批记录或回执。

工单流程：

1. `PARALLELOGRAM` 客户提交工单。
2. `RECTANGLE` 系统识别问题类型。
3. `DIAMOND` 是否可自动回复。
4. `RECTANGLE` 工程师处理。
5. `CYLINDER` 更新工单状态。
6. `DOCUMENT` 沉淀知识条目。

数据处理流程：

1. `PARALLELOGRAM` 导入或接收数据。
2. `RECTANGLE` 清洗和标准化。
3. `DIAMOND` 是否存在异常。
4. `RECTANGLE` 人工修正异常。
5. `CYLINDER` 写入多维表。
6. `EMBEDDED_SHEET` 展示结果视图。

## 10. 业务工作流生成清单

生成前确认：

1. 触发条件是什么。
2. 参与角色有哪些。
3. 核心业务对象是什么。
4. 正常路径有哪些步骤。
5. 判断条件有哪些。
6. 异常路径如何处理。
7. 最终沉淀到哪里：表格、文档、报表、消息或外部系统。

生成后自检：

- 每个节点只做一件事。
- 每个节点都有清晰业务职责和合适 `type`。
- 所有节点都有稳定 `id`。
- 所有节点都有 `style.width/height`、顶层 `width/height`、`positionAbsolute`、`data.width/height`、`data.align/verticalAlign`。
- 所有节点的 `data.backgroundColor` 都是淡色或 `transparent`，不能是黑色或深色。
- 所有边的 `source/target` 都能找到节点。
- 所有边都有 `sourceHandle/targetHandle`、`markerEnd`、`style.stroke/style.strokeWidth`。
- 至少有一个起点和一个终点。
- 条件分支有清晰 label。
- 保存前能通过 `canvas save` 的 `nodes/edges` 校验。
- 如果用户要 PPT / 演示稿，必须额外确认一页一个 `SECTION`、页面比例 `16:9`、所有内容节点都在页面分区内。
- 如果用户要展示复杂信息，必须优先考虑 `INFOGRAPHIC`，并检查 `data.infographicSyntax` 是否以 `infographic <template-name>` 开头。

## 11. 生成后校验

生成完成后必须先通过本地结构校验，再保存到项目画布：

```bash
dimens-cli canvas validate --file ./workflow-canvas.json
```

校验失败时，按错误提示修正 `nodes/edges`，不要继续执行 `canvas create/save`。

校验重点见：

```text
dimens-manager/references/canvas/references/validation-checklist.md
```

## 12. 保存要求

- 新建画布可以在 `canvas create --file` 中直接带初始图。
- 修改已有画布必须先执行 `canvas info`，再执行 `canvas save`。
- 保存后必须执行 `canvas info` 和 `canvas versions` 回查版本。
- 输出文件建议命名为 `*-canvas.json`，方便后续版本追踪。
