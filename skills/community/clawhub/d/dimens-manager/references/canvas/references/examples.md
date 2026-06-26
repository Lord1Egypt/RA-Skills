# dimens-manager 画布章节案例

## 1. 一键生成审批流程画布

1. 根据用户描述生成 `approval-canvas.json`。
2. 创建画布：

```bash
dimens-cli canvas create --team-id TEAM1 --project-id PROJ1 --name 审批流程画布 --file ./approval-canvas.json
```

3. 如果后续要更新：

```bash
dimens-cli canvas info canvas_1 --team-id TEAM1 --project-id PROJ1
dimens-cli canvas save canvas_1 --team-id TEAM1 --project-id PROJ1 --base-version 1 --file ./approval-canvas.json --summary 优化审批异常分支
```

4. 如果要沉淀为组件：

```bash
dimens-cli canvas resource-save --team-id TEAM1 --name 审批节点组 --nodes '[{"id":"submit"}]' --edges '[]' --tags 审批,流程
```

## 2. 售后工单工作流画布

用户输入：

```text
帮我生成一个售后工单处理工作流画布
```

推荐输出画布 JSON：

```json
{
  "version": "1.0",
  "timestamp": 1777800000000,
  "nodes": [
    {
      "id": "ticket_submit",
      "type": "PARALLELOGRAM",
      "position": { "x": 0, "y": 0 },
      "positionAbsolute": { "x": 0, "y": 0 },
      "width": 150,
      "height": 80,
      "selected": false,
      "dragging": false,
      "style": { "width": 150, "height": 80 },
      "data": { "label": "客户提交工单表单", "backgroundColor": "#ffffff", "borderColor": "#d1d5db", "borderWidth": 1, "textColor": "#111827", "fontSize": 14, "width": 150, "height": 80, "borderRadius": 12, "align": "center", "verticalAlign": "center", "text": "职责：采集客户、问题描述、附件和期望处理时限" }
    },
    {
      "id": "ticket_classify",
      "type": "RECTANGLE",
      "position": { "x": 0, "y": 160 },
      "positionAbsolute": { "x": 0, "y": 160 },
      "width": 150,
      "height": 80,
      "selected": false,
      "dragging": false,
      "style": { "width": 150, "height": 80 },
      "data": { "label": "系统识别问题类型", "backgroundColor": "#ffffff", "borderColor": "#d1d5db", "borderWidth": 1, "textColor": "#111827", "fontSize": 14, "width": 150, "height": 80, "borderRadius": 12, "align": "center", "verticalAlign": "center", "text": "职责：根据工单内容判断问题类别、优先级和建议处理方式" }
    },
    {
      "id": "need_engineer",
      "type": "DIAMOND",
      "position": { "x": 0, "y": 320 },
      "positionAbsolute": { "x": 0, "y": 320 },
      "width": 150,
      "height": 100,
      "selected": false,
      "dragging": false,
      "style": { "width": 150, "height": 100 },
      "data": { "label": "是否需要工程师介入", "backgroundColor": "#fff7ed", "borderColor": "#f97316", "borderWidth": 1, "textColor": "#111827", "fontSize": 14, "width": 150, "height": 100, "borderRadius": 12, "align": "center", "verticalAlign": "center" }
    },
    {
      "id": "auto_reply",
      "type": "RECTANGLE",
      "position": { "x": -260, "y": 500 },
      "positionAbsolute": { "x": -260, "y": 500 },
      "width": 150,
      "height": 80,
      "selected": false,
      "dragging": false,
      "style": { "width": 150, "height": 80 },
      "data": { "label": "自动回复解决方案", "backgroundColor": "#ecfdf5", "borderColor": "#10b981", "borderWidth": 1, "textColor": "#111827", "fontSize": 14, "width": 150, "height": 80, "borderRadius": 12, "align": "center", "verticalAlign": "center" }
    },
    {
      "id": "engineer_process",
      "type": "RECTANGLE",
      "position": { "x": 260, "y": 500 },
      "positionAbsolute": { "x": 260, "y": 500 },
      "width": 150,
      "height": 80,
      "selected": false,
      "dragging": false,
      "style": { "width": 150, "height": 80 },
      "data": { "label": "工程师排查处理", "backgroundColor": "#eff6ff", "borderColor": "#3b82f6", "borderWidth": 1, "textColor": "#111827", "fontSize": 14, "width": 150, "height": 80, "borderRadius": 12, "align": "center", "verticalAlign": "center" }
    },
    {
      "id": "customer_confirm",
      "type": "DIAMOND",
      "position": { "x": 0, "y": 680 },
      "positionAbsolute": { "x": 0, "y": 680 },
      "width": 150,
      "height": 100,
      "selected": false,
      "dragging": false,
      "style": { "width": 150, "height": 100 },
      "data": { "label": "客户是否确认解决", "backgroundColor": "#fff7ed", "borderColor": "#f97316", "borderWidth": 1, "textColor": "#111827", "fontSize": 14, "width": 150, "height": 100, "borderRadius": 12, "align": "center", "verticalAlign": "center" }
    },
    {
      "id": "ticket_close",
      "type": "CYLINDER",
      "position": { "x": 0, "y": 860 },
      "positionAbsolute": { "x": 0, "y": 860 },
      "width": 150,
      "height": 80,
      "selected": false,
      "dragging": false,
      "style": { "width": 150, "height": 80 },
      "data": { "label": "写入工单状态和知识库", "backgroundColor": "#f8fafc", "borderColor": "#64748b", "borderWidth": 1, "textColor": "#111827", "fontSize": 14, "width": 150, "height": 80, "borderRadius": 12, "align": "center", "verticalAlign": "center", "text": "职责：更新工单状态、处理结果和可复用解决方案" }
    },
    {
      "id": "service_report",
      "type": "DOCUMENT",
      "position": { "x": 0, "y": 1020 },
      "positionAbsolute": { "x": 0, "y": 1020 },
      "width": 180,
      "height": 100,
      "selected": false,
      "dragging": false,
      "style": { "width": 180, "height": 100 },
      "data": { "label": "生成结案报告", "backgroundColor": "#ffffff", "borderColor": "#94a3b8", "borderWidth": 1, "textColor": "#111827", "fontSize": 14, "width": 180, "height": 100, "borderRadius": 12, "align": "center", "verticalAlign": "center", "text": "职责：输出客户可查看的结案说明和服务记录" }
    }
  ],
  "edges": [
    { "id": "edge_ticket_submit_ticket_classify", "source": "ticket_submit", "target": "ticket_classify", "sourceHandle": "source-bottom", "targetHandle": "target-top", "type": "default", "animated": false, "selected": false, "zIndex": 0, "markerEnd": { "type": "arrowclosed", "color": "#94a3b8" }, "style": { "stroke": "#94a3b8", "strokeWidth": 2 } },
    { "id": "edge_ticket_classify_need_engineer", "source": "ticket_classify", "target": "need_engineer", "sourceHandle": "source-bottom", "targetHandle": "target-top", "type": "default", "animated": false, "selected": false, "zIndex": 0, "markerEnd": { "type": "arrowclosed", "color": "#94a3b8" }, "style": { "stroke": "#94a3b8", "strokeWidth": 2 } },
    { "id": "edge_need_engineer_auto_reply", "source": "need_engineer", "target": "auto_reply", "sourceHandle": "source-left", "targetHandle": "target-top", "type": "smoothstep", "label": "否", "animated": false, "selected": false, "zIndex": 0, "markerEnd": { "type": "arrowclosed", "color": "#94a3b8" }, "style": { "stroke": "#94a3b8", "strokeWidth": 2 } },
    { "id": "edge_need_engineer_engineer_process", "source": "need_engineer", "target": "engineer_process", "sourceHandle": "source-right", "targetHandle": "target-top", "type": "smoothstep", "label": "是", "animated": false, "selected": false, "zIndex": 0, "markerEnd": { "type": "arrowclosed", "color": "#94a3b8" }, "style": { "stroke": "#94a3b8", "strokeWidth": 2 } },
    { "id": "edge_auto_reply_customer_confirm", "source": "auto_reply", "target": "customer_confirm", "sourceHandle": "source-bottom", "targetHandle": "target-left", "type": "smoothstep", "animated": false, "selected": false, "zIndex": 0, "markerEnd": { "type": "arrowclosed", "color": "#94a3b8" }, "style": { "stroke": "#94a3b8", "strokeWidth": 2 } },
    { "id": "edge_engineer_process_customer_confirm", "source": "engineer_process", "target": "customer_confirm", "sourceHandle": "source-bottom", "targetHandle": "target-right", "type": "smoothstep", "animated": false, "selected": false, "zIndex": 0, "markerEnd": { "type": "arrowclosed", "color": "#94a3b8" }, "style": { "stroke": "#94a3b8", "strokeWidth": 2 } },
    { "id": "edge_customer_confirm_ticket_close", "source": "customer_confirm", "target": "ticket_close", "sourceHandle": "source-bottom", "targetHandle": "target-top", "type": "default", "label": "确认", "animated": false, "selected": false, "zIndex": 0, "markerEnd": { "type": "arrowclosed", "color": "#94a3b8" }, "style": { "stroke": "#94a3b8", "strokeWidth": 2 } },
    { "id": "edge_ticket_close_service_report", "source": "ticket_close", "target": "service_report", "sourceHandle": "source-bottom", "targetHandle": "target-top", "type": "default", "animated": false, "selected": false, "zIndex": 0, "markerEnd": { "type": "arrowclosed", "color": "#94a3b8" }, "style": { "stroke": "#94a3b8", "strokeWidth": 2 } },
    { "id": "edge_customer_confirm_engineer_process", "source": "customer_confirm", "target": "engineer_process", "sourceHandle": "source-right", "targetHandle": "target-right", "type": "smoothstep", "label": "未解决", "animated": false, "selected": false, "zIndex": 1, "markerEnd": { "type": "arrowclosed", "color": "#ef4444" }, "style": { "stroke": "#ef4444", "strokeWidth": 2 } }
  ],
  "viewport": { "x": 0, "y": 0, "zoom": 1 },
  "meta": {
    "source": "dimens-manager-canvas",
    "scenario": "售后工单",
    "nodeGuide": {
      "ticket_submit": "输入节点：客户提交问题信息",
      "ticket_classify": "系统处理节点：识别问题类型、优先级和建议处理方式",
      "need_engineer": "判断节点：决定自动回复还是人工介入",
      "ticket_close": "数据沉淀节点：写入状态和知识库",
      "service_report": "文档节点：输出结案报告"
    }
  }
}
```

## 3. PPT 演示稿画布

用户输入：

```text
帮我创建一个客户增长方案 PPT 画布
```

生成要求：

- 每一页 PPT 必须是一个 `SECTION` 分区。
- 每个 `SECTION` 固定 16:9，推荐 `1280 x 720`。
- 页面内容节点必须通过 `parentNode` 挂到对应 `SECTION` 下。
- 复杂方案、路径、趋势、对比等核心内容优先使用 `INFOGRAPHIC` 信息图节点。
- 内容节点的 `position` 是页内相对坐标，`positionAbsolute` 是画布绝对坐标。
- 页面分区节点放在 `nodes` 数组前面，页面内容节点跟在对应分区后面。

推荐输出画布 JSON 结构：

```json
{
  "version": "1.0",
  "timestamp": 1777800000000,
  "nodes": [
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
      "data": { "label": "第 1 页：方案总览", "backgroundColor": "#ffffff", "borderColor": "#e5e7eb", "borderWidth": 1, "textColor": "#111827", "fontSize": 16, "width": 1280, "height": 720, "borderRadius": 0, "align": "left", "verticalAlign": "top", "text": "PPT 页面分区，16:9" }
    },
    {
      "id": "slide_02",
      "type": "SECTION",
      "position": { "x": 0, "y": 820 },
      "positionAbsolute": { "x": 0, "y": 820 },
      "width": 1280,
      "height": 720,
      "selected": false,
      "dragging": false,
      "style": { "width": 1280, "height": 720 },
      "data": { "label": "第 2 页：执行路径", "backgroundColor": "#ffffff", "borderColor": "#e5e7eb", "borderWidth": 1, "textColor": "#111827", "fontSize": 16, "width": 1280, "height": 720, "borderRadius": 0, "align": "left", "verticalAlign": "top", "text": "PPT 页面分区，16:9" }
    },
    {
      "id": "slide_01_title",
      "type": "TEXT",
      "parentNode": "slide_01",
      "position": { "x": 72, "y": 56 },
      "positionAbsolute": { "x": 72, "y": 56 },
      "width": 620,
      "height": 72,
      "selected": false,
      "dragging": false,
      "style": { "width": 620, "height": 72 },
      "data": { "label": "客户增长方案", "backgroundColor": "transparent", "borderColor": "transparent", "borderWidth": 0, "textColor": "#111827", "fontSize": 40, "width": 620, "height": 72, "borderRadius": 0, "align": "left", "verticalAlign": "center", "text": "客户增长方案" }
    },
    {
      "id": "slide_01_growth_infographic",
      "type": "INFOGRAPHIC",
      "parentNode": "slide_01",
      "position": { "x": 72, "y": 170 },
      "positionAbsolute": { "x": 72, "y": 170 },
      "width": 760,
      "height": 420,
      "selected": false,
      "dragging": false,
      "style": { "width": 760, "height": 420 },
      "data": { "label": "客户增长路径信息图", "backgroundColor": "#ffffff", "borderColor": "#cbd5e1", "borderWidth": 1, "textColor": "#111827", "fontSize": 14, "width": 760, "height": 420, "borderRadius": 16, "align": "center", "verticalAlign": "center", "infographicSyntax": "infographic list-row-horizontal-icon-arrow\ndata\n  title 客户增长路径\n  desc 聚焦获客、转化、复购三个阶段\n  lists\n    - label 获客\n      desc 统一线索来源并提升触达效率\n      icon rocket launch\n    - label 转化\n      desc 优化销售跟进路径并减少流失\n      icon chart line\n    - label 复购\n      desc 用会员权益和分层运营提升复购\n      icon repeat\ntheme\n  palette #3b82f6 #8b5cf6 #f97316" }
    },
    {
      "id": "slide_02_title",
      "type": "TEXT",
      "parentNode": "slide_02",
      "position": { "x": 72, "y": 56 },
      "positionAbsolute": { "x": 72, "y": 876 },
      "width": 620,
      "height": 72,
      "selected": false,
      "dragging": false,
      "style": { "width": 620, "height": 72 },
      "data": { "label": "执行路径", "backgroundColor": "transparent", "borderColor": "transparent", "borderWidth": 0, "textColor": "#111827", "fontSize": 40, "width": 620, "height": 72, "borderRadius": 0, "align": "left", "verticalAlign": "center", "text": "执行路径" }
    }
  ],
  "edges": [],
  "viewport": { "x": 0, "y": 0, "zoom": 0.8 },
  "meta": {
    "source": "dimens-manager-canvas",
    "scenario": "ppt-canvas",
    "slideRule": "16:9; one SECTION per slide; all content nodes must use parentNode",
    "infographicRule": "use INFOGRAPHIC for complex PPT content; data.infographicSyntax must be AntV Infographic DSL"
  }
}
```
