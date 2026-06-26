---
name: feishu-cli-board
description: >-
  飞书画板全功能操作：创建画板、绘制架构图/流程图/看板（通过 create-notes API 精确控制节点位置和样式）、
  导入 Mermaid/PlantUML 图表、下载画板图片、获取/复制画板节点。
  当用户请求"画个图"、"画架构图"、"画流程图"、"画板"、"whiteboard"、"create-notes"、
  "在飞书里画图"、"画个看板"、"可视化"、"节点图"时使用。
  也适用于：用户给出一组实体和关系，期望在飞书文档中生成可视化图表的场景。
  与 Mermaid 导入的区别：Mermaid 由飞书服务端自动排版，create-notes 可精确控制坐标、颜色、连线，
  适合需要精排的架构图和看板。
argument-hint: "[whiteboard_id]"
user-invocable: true
allowed-tools: Bash, Read, Write
---

# 飞书画板操作技能

## 前置条件

- **认证**：需要有效的 App Access Token（环境变量 `FEISHU_APP_ID` + `FEISHU_APP_SECRET`，或 `~/.feishu-cli/config.yaml`）
- **权限**：应用需开通 `board:whiteboard`（画板读写）和 `docx:document`（文档中添加画板）
- **验证**：`feishu-cli auth status` 确认认证状态正常

## 两种模式

在飞书文档中创建画板并绘制可视化图表。支持两种模式：

| 模式 | 方式 | 适用场景 |
|------|------|---------|
| **精排绘图** | `board create-notes` — JSON 描述节点坐标、颜色、连线 | 架构图、看板、自定义布局 |
| **图表导入** | `board import` — Mermaid/PlantUML 代码自动渲染 | 标准流程图、时序图等 8 种图表 |

### 何时使用哪种方式

| 需求 | 推荐方式 | 说明 |
|------|---------|------|
| 精确控制节点位置、颜色、坐标 | `board create-notes`（本技能） | 完全自定义布局，适合架构图、看板 |
| 从 Mermaid/PlantUML 代码快速生成图 | `board import` 或 `doc import` | 服务端自动排版，无需手动计算坐标 |
| 在文档中内嵌简单图表 | `feishu-cli-write` / `feishu-cli-import` 的 Mermaid 支持 | Markdown 中写 Mermaid 代码块，导入时自动转画板 |

**简单判断**：如果你只需要"画个流程图"且不关心精确坐标，优先用 Mermaid；如果需要"精排"或"自定义配色布局"，用 `create-notes`。

## 精排绘图工作流（create-notes）

这是画板的核心能力，通过 JSON 精确控制每个节点的位置、大小、颜色和连线。

### 标准四步流程

```bash
# 1. 创建文档（或使用已有文档）
feishu-cli doc create --title "架构图" -o json
# → document_id

# 2. 在文档中添加画板
feishu-cli doc add-board <document_id> -o json
# → whiteboard_id

# 3. 创建节点（先形状，再连接线）
feishu-cli board create-notes <whiteboard_id> shapes.json -o json
# → node_ids（用于连接线引用）
feishu-cli board create-notes <whiteboard_id> connectors.json -o json

# 4. 截图验证
feishu-cli board image <whiteboard_id> output.png
```

**关键原则**：先创建所有形状节点获取 ID，再创建连接线引用这些 ID。

### 最小示例：2 个节点 + 1 条连线

在深入 JSON 格式细节之前，先看一个最小的完整示例——两个矩形节点通过一条箭头连接：

```bash
# shapes.json — 两个形状节点
cat > /tmp/minimal_shapes.json << 'EOF'
[
  {"type":"composite_shape","x":100,"y":100,"width":160,"height":40,
   "composite_shape":{"type":"round_rect"},
   "text":{"text":"服务 A","font_size":14,"font_weight":"regular","horizontal_align":"center","vertical_align":"mid"},
   "style":{"fill_color":"#3399ff","fill_opacity":100,"border_style":"none"},
   "z_index":10},
  {"type":"composite_shape","x":400,"y":100,"width":160,"height":40,
   "composite_shape":{"type":"round_rect"},
   "text":{"text":"服务 B","font_size":14,"font_weight":"regular","horizontal_align":"center","vertical_align":"mid"},
   "style":{"fill_color":"#509863","fill_opacity":100,"border_style":"none"},
   "z_index":10}
]
EOF
feishu-cli board create-notes $BOARD_ID /tmp/minimal_shapes.json -o json
# → 返回 node_ids: ["o1:1", "o1:2"]

# connector.json — 一条从服务 A 指向服务 B 的连线
cat > /tmp/minimal_connector.json << 'EOF'
[
  {"type":"connector","width":1,"height":1,"z_index":50,
   "connector":{"shape":"polyline",
     "start":{"arrow_style":"none","attached_object":{"id":"o1:1","position":{"x":1,"y":0.5},"snap_to":"right"}},
     "end":{"arrow_style":"triangle_arrow","attached_object":{"id":"o1:2","position":{"x":0,"y":0.5},"snap_to":"left"}}},
   "style":{"border_color":"#646a73","border_opacity":100,"border_style":"solid","border_width":"narrow"}}
]
EOF
feishu-cli board create-notes $BOARD_ID /tmp/minimal_connector.json -o json
```

这就是 create-notes 的基本模式：**形状定义位置和样式 → 连接线通过 ID 引用形状**。下面是各字段的详细说明。

### 节点 JSON 格式

#### 形状节点（composite_shape）

最常用的节点类型，支持矩形、圆角矩形等：

```json
{
  "type": "composite_shape",
  "x": 100, "y": 100, "width": 200, "height": 50,
  "composite_shape": {"type": "round_rect"},
  "text": {
    "text": "节点文本",
    "font_size": 14,
    "font_weight": "regular",
    "horizontal_align": "center",
    "vertical_align": "mid"
  },
  "style": {
    "fill_color": "#8569cb",
    "fill_opacity": 100,
    "border_style": "none"
  },
  "z_index": 10
}
```

**注意**：多余字段会导致 `2890002 invalid arg` 错误，保持最小格式。

#### 连接线（connector）

连接两个已创建的形状节点：

```json
{
  "type": "connector",
  "width": 1, "height": 1, "z_index": 50,
  "connector": {
    "shape": "polyline",
    "start": {
      "arrow_style": "none",
      "attached_object": {
        "id": "<source_node_id>",
        "position": {"x": 1, "y": 0.5},
        "snap_to": "right"
      }
    },
    "end": {
      "arrow_style": "triangle_arrow",
      "attached_object": {
        "id": "<target_node_id>",
        "position": {"x": 0, "y": 0.5},
        "snap_to": "left"
      }
    }
  },
  "style": {
    "border_color": "#646a73",
    "border_opacity": 100,
    "border_style": "solid",
    "border_width": "narrow"
  }
}
```

#### 连接方向速查

| 方向 | start position | start snap_to | end position | end snap_to |
|------|---------------|---------------|-------------|-------------|
| → 左到右 | `{x:1, y:0.5}` | `right` | `{x:0, y:0.5}` | `left` |
| ↓ 上到下 | `{x:0.5, y:1}` | `bottom` | `{x:0.5, y:0}` | `top` |
| ← 右到左 | `{x:0, y:0.5}` | `left` | `{x:1, y:0.5}` | `right` |
| ↑ 下到上 | `{x:0.5, y:0}` | `top` | `{x:0.5, y:1}` | `bottom` |

position 是归一化坐标（0-1），表示节点边缘上的连接点位置。一个节点连多条线时，调整 position 避免重叠（如扇出：`x:0.25`、`x:0.5`、`x:0.75`）。

### 配色方案

为不同实体类型使用不同颜色，让图表一目了然：

| 用途 | 填充色 | 边框色 | 适用对象 |
|------|--------|--------|---------|
| 强调/标题 | `#8569cb` | — | 核心服务、标题栏 |
| 紫色辅助 | `#eae2fe` | `#8569cb` | API、中间层 |
| 绿色正向 | `#509863` | — | 成功、输出、完成 |
| 绿色辅助 | `#d5e8d4` | `#509863` | 处理步骤 |
| 蓝色服务 | `#3399ff` | — | 主服务、入口 |
| 蓝色辅助 | `#cce5ff` | `#3399ff` | 子服务、组件 |
| 橙色并发 | `#ffc285` | — | 并发处理、Worker |
| 橙色辅助 | `#fff0e3` | `#ffc285` | 并发子任务 |
| 红色告警 | `#ef4444` | — | 错误、降级、告警 |
| 红色辅助 | `#ffe0e0` | `#ef4444` | 容错处理 |
| 灰色输入 | `#f5f5f5` | `#616161` | 用户、外部输入 |
| 连接线 | — | `#646a73` | 普通连线 |

### z_index 与透明度规则

| z_index | 用途 | fill_opacity |
|---------|------|-------------|
| 0-1 | 背景色带（分区底色） | ≤25% |
| 2-3 | 次级区域 | ≤60% |
| 10 | 常规形状节点 | 100% |
| 50 | 连接线 | border_opacity=100 |

背景色带 `fill_opacity` 必须 ≤60%，否则遮挡上层节点。

### 布局设计建议

绘制复杂图表时的布局规划方法：

1. **确定画布尺寸** — 宽 800px 左右，高度按行数估算（每行 ~80px 间距）
2. **按行分区** — 标题行、输入行、处理行、输出行，每行 y 坐标递增
3. **对齐网格** — 同层节点 y 坐标相同，节点间 x 间距 ≥30px
4. **背景色带** — 用低透明度矩形作为分区视觉标记（z_index=0）
5. **先画再连** — 所有形状一个批次创建，拿到 ID 后再创建连接线

### 传参方式

```bash
# 从 JSON 文件（推荐，复杂图表）
feishu-cli board create-notes <whiteboard_id> nodes.json -o json

# 内联 JSON（简单场景）
feishu-cli board create-notes <whiteboard_id> '<json_array>' --source-type content -o json
```

## Mermaid / PlantUML 图表导入

将 Mermaid 或 PlantUML 代码自动渲染为飞书画板（服务端排版）：

```bash
# 从内容导入 Mermaid
feishu-cli board import <whiteboard_id> \
  --source-type content \
  -c "graph TD; A-->B-->C" \
  --syntax mermaid

# 从文件导入 PlantUML
feishu-cli board import <whiteboard_id> diagram.puml --syntax plantuml

# 指定图表类型（通常 auto 即可）
feishu-cli board import <whiteboard_id> diagram.mmd --syntax mermaid --diagram-type 6
```

### 支持的 Mermaid 类型（8 种，全部验证通过）

| 类型 | 声明 | diagram-type |
|------|------|-------------|
| 流程图 | `flowchart TD` | 6 |
| 时序图 | `sequenceDiagram` | 2 |
| 类图 | `classDiagram` | 4 |
| 状态图 | `stateDiagram-v2` | 0 (auto) |
| ER 图 | `erDiagram` | 5 |
| 甘特图 | `gantt` | 0 (auto) |
| 饼图 | `pie` | 0 (auto) |
| 思维导图 | `mindmap` | 1 |

### Mermaid 限制

- 禁止花括号 `{text}`（被识别为菱形节点）
- 禁止 `par...and...end`（飞书不支持）
- 参与者建议 ≤8（过多会渲染失败）
- 复杂图表失败时会降级为代码块

## 其他画板命令

```bash
# 下载画板为 PNG 图片
feishu-cli board image <whiteboard_id> output.png

# 获取画板所有节点（JSON）
feishu-cli board nodes <whiteboard_id>

# 在文档中添加空画板
feishu-cli doc add-board <document_id> -o json
```

## 复制/修改画板（Redraw 模式）

画板 API 不支持修改或删除已有节点，修改需要重建：

1. `board nodes` 导出原始节点
2. 清洗数据 — 移除只读字段（`id`、`locked`、`children`、`text_color_type`、`fill_color_type`、`border_color_type`、`start_object`/`end_object`）
3. 分离形状和连接线
4. 新画板中先创建形状 → 映射旧 ID 到新 ID → 再创建连接线

详细的清洗字段列表和 Redraw 流程见 `references/node-api.md`。

## 权限要求

| 权限 | 说明 |
|------|------|
| `board:whiteboard` | 画板读写 |
| `docx:document` | 文档中添加画板 |

## 错误排障

### 错误码速查

| 错误码 | 含义 | 常见原因 |
|--------|------|---------|
| 2890001 | invalid format | JSON 格式错误 |
| 2890002 | invalid arg | 包含未公开字段（如 `sticky_note` 类型）或格式不对 |
| 2890003 | record missing | whiteboard_id 不存在 |
| 2890006 | rate limited | 超过 50 req/s |

### 排障指引

**2890002 invalid arg（最常见）**：

JSON 中包含了 API 不支持的字段。只使用以下安全字段：

- `composite_shape` 节点：`type`, `x`, `y`, `width`, `height`, `composite_shape`, `text`, `style`, `z_index`
- `connector` 节点：`type`, `width`, `height`, `z_index`, `connector`, `style`
- `text` 对象：`text`, `font_size`, `font_weight`, `horizontal_align`, `vertical_align`
- `style` 对象：`fill_color`, `fill_opacity`, `border_style`, `border_color`, `border_width`, `border_opacity`

排查步骤：逐步删减 JSON 字段，定位导致错误的多余字段。常见陷阱包括 `id`、`locked`、`children`、`text_color_type` 等只读字段。

**画板创建失败**：

- 检查应用是否已开通 `board:whiteboard` 权限
- 确认 `whiteboard_id` 来自 `doc add-board` 的返回值，而非 `document_id`
- 运行 `feishu-cli auth status` 确认 Token 有效

**Mermaid 导入降级为代码块**：

- 飞书服务端解析失败时会自动降级，属于预期行为
- 使用 `--verbose` 查看具体的服务端错误信息
- 常见原因：花括号 `{text}`、`par...and...end` 语法、参与者过多（>8）
- 解决方案：简化图表语法，或拆分为多个小图表

## 完整示例：绘制简单架构图

```bash
# 1. 创建文档和画板
DOC_ID=$(feishu-cli doc create --title "架构图" -o json | python3 -c "import sys,json;print(json.load(sys.stdin)['document_id'])")
BOARD_ID=$(feishu-cli doc add-board $DOC_ID -o json | python3 -c "import sys,json;print(json.load(sys.stdin)['whiteboard_id'])")

# 2. 创建形状节点
cat > /tmp/shapes.json << 'EOF'
[
  {"type":"composite_shape","x":50,"y":50,"width":150,"height":40,
   "composite_shape":{"type":"round_rect"},
   "text":{"text":"客户端","font_size":14,"font_weight":"regular","horizontal_align":"center","vertical_align":"mid"},
   "style":{"fill_color":"#f5f5f5","fill_opacity":100,"border_style":"solid","border_color":"#616161","border_width":"narrow"},
   "z_index":10},
  {"type":"composite_shape","x":300,"y":50,"width":150,"height":40,
   "composite_shape":{"type":"round_rect"},
   "text":{"text":"API 网关","font_size":14,"font_weight":"bold","horizontal_align":"center","vertical_align":"mid"},
   "style":{"fill_color":"#3399ff","fill_opacity":100,"border_style":"none"},
   "z_index":10},
  {"type":"composite_shape","x":550,"y":50,"width":150,"height":40,
   "composite_shape":{"type":"round_rect"},
   "text":{"text":"数据库","font_size":14,"font_weight":"regular","horizontal_align":"center","vertical_align":"mid"},
   "style":{"fill_color":"#509863","fill_opacity":100,"border_style":"none"},
   "z_index":10}
]
EOF
feishu-cli board create-notes $BOARD_ID /tmp/shapes.json -o json
# → 返回 node_ids: ["o1:1", "o1:2", "o1:3"]

# 3. 创建连接线（引用上面返回的 ID）
cat > /tmp/connectors.json << 'EOF'
[
  {"type":"connector","width":1,"height":1,"z_index":50,
   "connector":{"shape":"polyline",
     "start":{"arrow_style":"none","attached_object":{"id":"o1:1","position":{"x":1,"y":0.5},"snap_to":"right"}},
     "end":{"arrow_style":"triangle_arrow","attached_object":{"id":"o1:2","position":{"x":0,"y":0.5},"snap_to":"left"}}},
   "style":{"border_color":"#646a73","border_opacity":100,"border_style":"solid","border_width":"narrow"}},
  {"type":"connector","width":1,"height":1,"z_index":50,
   "connector":{"shape":"polyline",
     "start":{"arrow_style":"none","attached_object":{"id":"o1:2","position":{"x":1,"y":0.5},"snap_to":"right"}},
     "end":{"arrow_style":"triangle_arrow","attached_object":{"id":"o1:3","position":{"x":0,"y":0.5},"snap_to":"left"}}},
   "style":{"border_color":"#646a73","border_opacity":100,"border_style":"solid","border_width":"narrow"}}
]
EOF
feishu-cli board create-notes $BOARD_ID /tmp/connectors.json -o json

# 4. 截图验证
feishu-cli board image $BOARD_ID /tmp/architecture.png
```

## 详细 API 参考

节点类型完整字段、connector 高级参数、Redraw 清洗字段等详细信息见 `references/node-api.md`。
