---
name: drawio-generator
description: 将自然语言或文档（docx/pdf/txt）转换为 draw.io 可编辑 XML 图表（.drawio 文件）。当用户说"画个流程图"、"生成图表"、"画架构图/时序图/网络拓扑图"、"帮我画xxx流程"、"生成draw.io"等时自动触发。使用流程：接收描述→生成JSON→用户确认→调用gen.py生成.drawio→告知用户用draw.io打开。
---

# drawio-generator

## 如何使用（标准流程）

**Step 1**：接收用户的流程描述（文字或文件上传）

**Step 2**：根据描述生成结构化 JSON（nodes + edges），将 JSON 展示给用户确认

**Step 3**：用户确认后，调用生成脚本：
```bash
python3 skills/drawio-generator/scripts/gen.py "图表标题" '{"title":"...","nodes":[...],"edges":[...]}' [类型]
```

**Step 4**：交付 `.drawio` 文件到输出目录，并告知用户：
> 用 draw.io 打开此文件（网页版 https://app.diagrams.net 或桌面版 App），如需微调请手动调整节点位置后保存。

> ⚠️ 生成结果非完美，可能存在线条重叠或间距不理想，需要在 draw.io 中手动微调。

**输出目录**：
- 默认：`/Users/owen/Desktop/drawio-generator/`
- 可通过环境变量 `DRAWIO_OUTPUT_DIR` 或命令行 `--output-dir` 自定义

---

## JSON 结构

```json
{
  "title": "流程名称",
  "type": "flowchart",
  "nodes": [
    {"id": "0", "type": "start", "label": "开始"},
    {"id": "1", "type": "process", "label": "处理步骤"},
    {"id": "2", "type": "decision", "label": "判断条件？"},
    {"id": "3", "type": "end", "label": "结束"}
  ],
  "edges": [
    {"source": "0", "target": "1"},
    {"source": "1", "target": "2"},
    {"source": "2", "target": "3", "label": "是"},
    {"source": "2", "target": "1", "label": "否"}
  ]
}
```

### 节点 type 值

| type | 形状 |
|------|------|
| `start` | 椭圆 |
| `end` | 椭圆 |
| `process` | 圆角矩形 |
| `decision` | 菱形 |
| `document` | 文档形状 |
| `data` | 平行四边形 |

### edges.label 值

| label | 含义 |
|-------|------|
| `是` / `Y` | 条件为真 |
| `否` / `N` | 条件为假 |
| 空 | 普通顺序流 |

### 支持的图表类型

`flowchart` | `sequence` | `network` | `architecture` | `hierarchy` | `function` | `deployment`

---

## 文件说明

| 文件 | 说明 |
|------|------|
| `scripts/gen.py` | **标准生成脚本**（必须使用，禁止直接调用 generator.py） |
| `scripts/generator.py` | 底层 XML 生成器（gen.py 内部调用） |
| `scripts/parser.py` | 输入解析（txt 直接读取，docx/pdf 需额外安装库） |
| `references/drawio-xml-spec.md` | draw.io XML 格式规范 |

**依赖说明**：
- 解析 .docx 需要：`pip install python-docx`
- 解析 .pdf 需要：`pip install pdfplumber`

## 布局参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `CANVAS_WIDTH` | 850 | 画布宽度 |
| `_LAYER_GAP_Y` | 120 | 层间垂直间距 |
| `MAIN_X` | 425 | 主轴 X 坐标 |
