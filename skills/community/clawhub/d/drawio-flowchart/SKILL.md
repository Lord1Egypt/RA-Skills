---
name: drawio-flowchart
description: Generate draw.io (.drawio) flowchart XML files. Use when the user asks for a flowchart, process diagram, workflow diagram, or any visual diagram in draw.io / diagrams.net format. Produces well-structured, visually clean .drawio files with proper alignment, hierarchy, and readable text. NOT for: Mermaid diagrams, ASCII art, or image-based diagrams.
---

# draw.io Flowchart Generator

Generate production-ready `.drawio` XML files that render cleanly in app.diagrams.net.

## Quick Start

1. Understand the user's process/workflow
2. Plan the hierarchy: stages → sub-stages → nodes
3. Generate the XML following the mandatory rules below
4. Save the `.drawio` file and tell the user how to open it (see [Output Delivery](#output-delivery))

## Mandatory Rules

These are non-negotiable. Every flowchart MUST follow all of them.

### Canvas Sizing (Critical)

**diagrams.net auto-scales to fit the canvas.** A canvas too large = tiny text on screen.

| Content complexity | pageWidth | pageHeight |
|---|---|---|
| Simple (≤3 stages, few nodes) | 600 | 1200 |
| Medium (4-5 stages) | 800 | 2800 |
| Complex (6+ stages, nested) | 800 | 3800 |

- **Never exceed pageWidth=800.** Wider canvases get scaled down, making text unreadable.
- Set `dx` and `dy` to match or slightly exceed page dimensions.

### Container Structure

Use `swimlane` containers for every stage/group — never bare `mxgraph.basic.rect`:

```xml
<mxCell id="g1" parent="1" connectable="0"
  style="swimlane;startSize=32;fillColor=#EBF5FF;strokeColor=#2563EB;
         strokeWidth=2;fontSize=16;fontStyle=1;fontColor=#1e40af;
         rounded=0;collapsible=0;"
  value="① Stage Name" vertex="1">
  <mxGeometry x="20" y="60" width="720" height="200" as="geometry" />
</mxCell>
```

Key properties:
- `startSize=32` — header height for title
- `rounded=0` — sharp corners (never rounded containers)
- `collapsible=0` — prevent collapse UI
- `connectable="0"` — on the cell tag, not in style

### Text Hierarchy

Three tiers of text size — no exceptions:

| Level | fontSize | fontStyle | Example |
|---|---|---|---|
| Stage title (swimlane) | 14-16 | 1 (bold) | ① Skill 上传 |
| Node title (inside box) | 13 with `<b>` tag | bold via HTML | **格式验证 ✅** |
| Node body text | 12 | normal | SKILL.md & YAML 合法 |

Use inline HTML for mixed sizes within a single cell:
```xml
value="&lt;b style=&quot;font-size:13px&quot;&gt;Title&lt;/b&gt;&lt;br&gt;&lt;br&gt;Body text line 1&lt;br&gt;Body text line 2"
```

### Alignment

- **All text: `align=center`** — no exceptions for node content
- **Stage titles** use swimlane's built-in left-aligned bold header (this is fine)
- **Nodes within a container**: distribute evenly across the container width
  - 2 nodes: left half + right half
  - 3 nodes: thirds

### Arrows

**Arrows must be clean and orthogonal. No diagonal lines, no crossing, no spaghetti.**

#### Between stages (main flow)
```xml
<mxCell id="ea_1to2" parent="1" source="g1" target="g2" edge="1"
  style="edgeStyle=orthogonalEdgeStyle;strokeWidth=3;strokeColor=#2563EB;
         fontColor=#2563EB;fontSize=12;fontStyle=1;"
  value="Label text">
```
- strokeWidth=3, blue (#2563EB), bold label

#### Within a container (internal flow)
```xml
<mxCell id="e30" parent="g2" source="30" target="31" edge="1"
  style="edgeStyle=orthogonalEdgeStyle;strokeWidth=2;strokeColor=#82b366;">
```
- strokeWidth=2, color matches container theme

#### Fan-out pattern (one source → multiple targets)
Use explicit entry points to prevent crossing:
```xml
<!-- Left target: entryX=0.25 -->
style="...entryX=0.25;entryY=0;exitX=0.5;exitY=1;"
<!-- Center target: entryX=0.5 -->
style="...entryX=0.5;entryY=0;exitX=0.5;exitY=1;"
<!-- Right target: entryX=0.75 -->
style="...entryX=0.75;entryY=0;exitX=0.5;exitY=1;"
```

#### Return/loop arrows
Use dashed lines routed via explicit waypoints on the left margin:
```xml
style="edgeStyle=orthogonalEdgeStyle;dashed=1;strokeColor=#d97706;strokeWidth=2;"
```
With `<Array as="points">` routing along x=5 to avoid crossing content.

### Color Palette

Use this consistent 5-stage palette. If fewer stages, use a subset:

| Stage | fillColor | strokeColor | fontColor |
|---|---|---|---|
| 1 (intro/input) | #EBF5FF | #2563EB | #1e40af |
| 2 (validation) | #F0FDF4 | #16a34a | #047857 |
| 3 (evaluation) | #FAF5FF | #7c3aed | #6d28d9 |
| 4 (approval) | #F0FDF4 | #059669 | #047857 |
| 5 (management) | #FFF7ED | #ea580c | #c2410c |

Sub-containers (dashed): use lighter fills (#FEFCE8, #FFF7ED, #FEF2F2) with `dashed=1`.

Node fills: always `#FFFFFF` with border color matching the parent stage.

Special nodes:
- Warning/fail: fillColor=#f8cecc, strokeColor=#b85450
- Pending/future: fillColor=#fff2cc, strokeColor=#d6b656
- Decision (rhombus): fillColor=#fff2cc, strokeColor=#d6b656

### Spacing Rules

- Container left margin: x=20, right margin: leave 20px
- Container width: `pageWidth - 40` (e.g., 720 for 800-wide canvas)
- Vertical gap between stages: 30-40px (including arrow space)
- Nodes inside container: 10-20px padding from container edges
- Vertical gap between node bottom and container bottom: ≥15px

### "或" (Or) Pattern

When two parallel options exist (e.g., manual vs automatic):
```xml
<mxCell id="s1or" parent="s1box"
  style="text;html=1;align=center;fontSize=16;fontStyle=1;fontColor=#999;"
  value="或" vertex="1">
```
Place centered between the two option boxes, vertically aligned to their midpoint.

### Status/Note Bars

For status flow annotations or notes at the bottom of a container:
```xml
style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#999;
       fontSize=11;align=center;fontStyle=2;"
```
Height: 22-28px, italic, gray — visually subordinate to main content.

## XML Structure Template

See [references/template.md](references/template.md) for the complete XML skeleton.

## Output Delivery

**交付本地 `.drawio` 文件**，告诉用户打开方式。

### 步骤

1. 生成完整的 `.drawio` XML，**必须包含 `<mxfile>` 外层包裹**：

```xml
<mxfile host="app.diagrams.net" type="device">
  <diagram id="xxx" name="图表名称">
    <mxGraphModel ...>
      <root>
        ...
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

2. 将文件保存到 workspace 或用户指定路径，文件名以 `.drawio` 结尾
3. 告诉用户文件路径和打开方式：

**打开方式（告知用户，选其一即可）：**
- **方式一**：浏览器打开 https://app.diagrams.net → 点「Open Existing Diagram」→ 选择本地文件
- **方式二**：直接将 `.drawio` 文件拖拽到已打开的 app.diagrams.net 页面中
- **方式三**：如果安装了 diagrams.net 桌面版（或 VS Code draw.io 插件），直接双击文件打开

## Validation Checklist

Before writing the file, verify:

- [ ] `pageWidth` ≤ 800
- [ ] All containers use `swimlane` style with `rounded=0;collapsible=0`
- [ ] All node text has `align=center`
- [ ] Stage titles use fontSize 14-16 with fontStyle=1
- [ ] Node titles use `<b>` tags at fontSize 13
- [ ] Inter-stage arrows: strokeWidth=3, strokeColor=#2563EB
- [ ] Intra-container arrows: strokeWidth=2, matching container color
- [ ] Fan-out arrows use explicit entryX/exitX anchors
- [ ] No XML comments (`<!-- -->`) in the output — they cause load errors
- [ ] All `edge` cells have `edge="1"` attribute and valid source/target
- [ ] Container cells have `connectable="0"` on the tag (not in style)
- [ ] Nodes inside a container have `parent="containerId"`
- [ ] No overlapping geometry — manually check x/y/width/height
- [ ] Return arrows route via left margin with explicit waypoints
