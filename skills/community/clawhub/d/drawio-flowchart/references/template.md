# XML Template

Complete skeleton for a medium-complexity (4-5 stage) flowchart.
Copy and adapt — replace `TODO` placeholders with real content.

```xml
<mxfile host="app.diagrams.net" agent="OpenClaw">
  <diagram id="TODO-id" name="TODO-diagram-name">
    <mxGraphModel dx="900" dy="600" grid="1" gridSize="10" guides="1"
      tooltips="1" connect="1" arrows="1" fold="1" page="1"
      pageScale="1" pageWidth="800" pageHeight="2800" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />

        <!-- ===== Title ===== -->
        <mxCell id="title" parent="1"
          style="text;html=1;align=center;verticalAlign=middle;
                 fontSize=24;fontStyle=1;fontColor=#111111;"
          value="TODO: 流程图标题" vertex="1">
          <mxGeometry x="100" y="10" width="560" height="40"
            as="geometry" />
        </mxCell>

        <!-- ===== Stage 1 Container ===== -->
        <mxCell id="g1" parent="1" connectable="0"
          style="swimlane;startSize=32;fillColor=#EBF5FF;
                 strokeColor=#2563EB;strokeWidth=2;fontSize=16;
                 fontStyle=1;fontColor=#1e40af;rounded=0;
                 collapsible=0;"
          value="① TODO: Stage Name" vertex="1">
          <mxGeometry x="20" y="60" width="720" height="180"
            as="geometry" />
        </mxCell>

        <!-- Nodes inside Stage 1 (parent=g1) -->
        <mxCell id="n1" parent="g1"
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;
                 strokeColor=#6c8ebf;fontSize=12;align=center;"
          value="&lt;b style=&quot;font-size:13px&quot;&gt;TODO: Node Title&lt;/b&gt;&lt;br&gt;&lt;br&gt;TODO: description"
          vertex="1">
          <mxGeometry x="20" y="40" width="210" height="90"
            as="geometry" />
        </mxCell>

        <mxCell id="n2" parent="g1"
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;
                 strokeColor=#6c8ebf;fontSize=12;align=center;"
          value="&lt;b style=&quot;font-size:13px&quot;&gt;TODO: Node Title&lt;/b&gt;&lt;br&gt;&lt;br&gt;TODO: description"
          vertex="1">
          <mxGeometry x="255" y="40" width="210" height="90"
            as="geometry" />
        </mxCell>

        <mxCell id="n3" parent="g1"
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;
                 strokeColor=#6c8ebf;fontSize=12;align=center;"
          value="&lt;b style=&quot;font-size:13px&quot;&gt;TODO: Node Title&lt;/b&gt;&lt;br&gt;&lt;br&gt;TODO: description"
          vertex="1">
          <mxGeometry x="490" y="40" width="210" height="90"
            as="geometry" />
        </mxCell>

        <!-- Internal arrows (parent=g1) -->
        <mxCell id="e_n1n2" parent="g1" source="n1" target="n2"
          edge="1"
          style="edgeStyle=orthogonalEdgeStyle;strokeWidth=2;
                 strokeColor=#6c8ebf;">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <mxCell id="e_n2n3" parent="g1" source="n2" target="n3"
          edge="1"
          style="edgeStyle=orthogonalEdgeStyle;strokeWidth=2;
                 strokeColor=#6c8ebf;">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- ===== Inter-stage arrow (parent=1) ===== -->
        <mxCell id="ea_1to2" parent="1" source="g1" target="g2"
          edge="1"
          style="edgeStyle=orthogonalEdgeStyle;strokeWidth=3;
                 strokeColor=#2563EB;fontColor=#2563EB;fontSize=12;
                 fontStyle=1;"
          value="TODO: transition label">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- ===== Stage 2 Container ===== -->
        <mxCell id="g2" parent="1" connectable="0"
          style="swimlane;startSize=32;fillColor=#F0FDF4;
                 strokeColor=#16a34a;strokeWidth=2;fontSize=14;
                 fontStyle=1;fontColor=#047857;rounded=0;
                 collapsible=0;"
          value="② TODO: Stage Name" vertex="1">
          <mxGeometry x="20" y="280" width="720" height="180"
            as="geometry" />
        </mxCell>

        <!-- TODO: Add nodes for Stage 2 -->

        <!-- ===== Continue pattern for stages 3-5 ===== -->

      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

## Patterns

### Sub-container (dashed, within a stage)

```xml
<mxCell id="s1box" parent="g3" connectable="0"
  style="swimlane;startSize=28;fillColor=#FEFCE8;strokeColor=#ca8a04;
         strokeWidth=1;dashed=1;fontSize=13;fontStyle=1;
         fontColor=#854d0e;rounded=0;collapsible=0;"
  value="Step 1：Sub-stage Name" vertex="1">
  <mxGeometry x="10" y="40" width="700" height="140" as="geometry" />
</mxCell>
<!-- Nodes inside: parent="s1box" -->
```

### Decision diamond

```xml
<mxCell id="d1" parent="g1"
  style="rhombus;whiteSpace=wrap;html=1;fillColor=#fff2cc;
         strokeColor=#d6b656;fontSize=12;align=center;fontStyle=1;"
  value="Decision?&lt;br&gt;&lt;span style=&quot;font-weight:normal;font-size:11px&quot;&gt;(note)&lt;/span&gt;"
  vertex="1">
  <mxGeometry x="240" y="110" width="150" height="72" as="geometry" />
</mxCell>
```

### Return/loop arrow via left margin

```xml
<mxCell id="e_loop" parent="1" source="update_node" target="g2"
  edge="1"
  style="edgeStyle=orthogonalEdgeStyle;dashed=1;strokeColor=#d97706;
         strokeWidth=2;fontColor=#d97706;fontSize=11;fontStyle=1;"
  value="Loop label">
  <mxGeometry relative="1" as="geometry">
    <Array as="points">
      <mxPoint x="5" y="SOURCE_Y" />
      <mxPoint x="5" y="TARGET_Y" />
    </Array>
  </mxGeometry>
</mxCell>
```
Replace SOURCE_Y and TARGET_Y with the vertical center of source/target.

### Parallel options with "或"

```xml
<!-- Left option -->
<mxCell id="opt_a" parent="sub_container" ... />
<!-- "或" label -->
<mxCell id="or_label" parent="sub_container"
  style="text;html=1;align=center;fontSize=16;fontStyle=1;fontColor=#999;"
  value="或" vertex="1">
  <mxGeometry x="CENTER_X" y="MID_Y" width="40" height="28"
    as="geometry" />
</mxCell>
<!-- Right option -->
<mxCell id="opt_b" parent="sub_container" ... />
```
