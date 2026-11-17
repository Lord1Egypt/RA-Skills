# TYPE 4: Flowchart / Process Flow / SOP

## What to ask the user
- List of steps and decisions
- Input/output data and documents
- Conditions for branches
- Whether this is a simple linear flow or a two-column SOP (steps + notes)

## Checklist
- Sequential IDs with no gaps
- Correct shapes per node type
- Decisions have Yes/No labeled exits
- Minimum 180px horizontal spacing, 140px vertical between main flow step nodes
- Increase `pageWidth`/`pageHeight` if many nodes
- Universal box spacing applied: `spacingLeft=12;spacingRight=12;spacingTop=10;spacingBottom=10;verticalAlign=top;`
- No fan-out arrows — use chained routing for sub-item lists

---

## Shape reference
| Shape | Style keyword | Use for |
|---|---|---|
| Start / End | `ellipse` | Terminal nodes |
| Process / Action | `rounded=1` | Steps and actions |
| Decision | `rhombus` | Yes/No branches |
| Document | `shape=document` | Reports or output documents |
| Data | `shape=parallelogram` | Input or output data |

## Color palette
| Shape | fillColor | strokeColor |
|---|---|---|
| Start | `#d5e8d4` | `#82b366` |
| Process / Step | `#dae8fc` | `#6c8ebf` |
| Decision | `#fff2cc` | `#d6b656` |
| End | `#f8cecc` | `#b85450` |
| Note / Annotation | `#fff2cc` | `#d6b656` |
| Warning / HITL | `#ffe6cc` | `#d79b00` |
| WIP / Incomplete | `#f5f5f5` | `#666666` |

---

## Simple flowchart XML template

```xml
<mxGraphModel dx="1422" dy="762" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="850" pageHeight="1100" math="0" shadow="0">
  <root>
    <mxCell id="0"/>
    <mxCell id="1" parent="0"/>

    <mxCell id="10" value="Start"
      style="ellipse;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;fontSize=13;fontStyle=1;
             spacingLeft=12;spacingRight=12;spacingTop=10;spacingBottom=10;"
      vertex="1" parent="1">
      <mxGeometry x="300" y="40" width="120" height="50" as="geometry"/>
    </mxCell>

    <mxCell id="11" value="Receive Request"
      style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=12;align=left;
             spacingLeft=12;spacingRight=12;spacingTop=10;spacingBottom=10;verticalAlign=top;"
      vertex="1" parent="1">
      <mxGeometry x="275" y="140" width="200" height="50" as="geometry"/>
    </mxCell>

    <mxCell id="12" value="Is Valid?"
      style="rhombus;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;fontSize=12;
             spacingLeft=12;spacingRight=12;spacingTop=10;spacingBottom=10;"
      vertex="1" parent="1">
      <mxGeometry x="255" y="240" width="240" height="80" as="geometry"/>
    </mxCell>

    <mxCell id="13" value="Process Data"
      style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=12;align=left;
             spacingLeft=12;spacingRight=12;spacingTop=10;spacingBottom=10;verticalAlign=top;"
      vertex="1" parent="1">
      <mxGeometry x="275" y="380" width="200" height="50" as="geometry"/>
    </mxCell>

    <mxCell id="14" value="Show Error"
      style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;fontSize=12;align=left;
             spacingLeft=12;spacingRight=12;spacingTop=10;spacingBottom=10;verticalAlign=top;"
      vertex="1" parent="1">
      <mxGeometry x="560" y="255" width="150" height="50" as="geometry"/>
    </mxCell>

    <mxCell id="15" value="End"
      style="ellipse;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;fontSize=13;fontStyle=1;
             spacingLeft=12;spacingRight=12;spacingTop=10;spacingBottom=10;"
      vertex="1" parent="1">
      <mxGeometry x="305" y="490" width="120" height="50" as="geometry"/>
    </mxCell>

    <!-- Connections -->
    <mxCell id="20" value="" style="edgeStyle=orthogonalEdgeStyle;endArrow=block;endFill=1;" edge="1" parent="1" source="10" target="11"><mxGeometry relative="1" as="geometry"/></mxCell>
    <mxCell id="21" value="" style="edgeStyle=orthogonalEdgeStyle;endArrow=block;endFill=1;" edge="1" parent="1" source="11" target="12"><mxGeometry relative="1" as="geometry"/></mxCell>
    <mxCell id="22" value="Yes" style="edgeStyle=orthogonalEdgeStyle;endArrow=block;endFill=1;fontSize=11;" edge="1" parent="1" source="12" target="13"><mxGeometry relative="1" as="geometry"/></mxCell>
    <mxCell id="23" value="No" style="edgeStyle=orthogonalEdgeStyle;endArrow=block;endFill=1;fontSize=11;exitX=1;exitY=0.5;" edge="1" parent="1" source="12" target="14"><mxGeometry relative="1" as="geometry"/></mxCell>
    <mxCell id="24" value="" style="edgeStyle=orthogonalEdgeStyle;endArrow=block;endFill=1;" edge="1" parent="1" source="13" target="15"><mxGeometry relative="1" as="geometry"/></mxCell>

  </root>
</mxGraphModel>
```

---

## SOP / process documentation layout pattern

For SOPs with step descriptions, use a **two-column layout**:

```
LEFT COLUMN  (x ~50):   numbered step boxes — main vertical flow
RIGHT COLUMN (x ~680):  note/annotation boxes aligned to their step
```

### Column geometry rules
- Main step boxes: `width=550`, `x=50`, vertical spacing ≥140px between steps
- Note boxes: `x=680` (or wider), sized to content — use height formula from box-style-standards.md
- Horizontal clearance between left column right edge (50+550=600) and note box left edge (680): 80px — sufficient
- Between sub-items in a vertical list: 20px gap, chained arrows (not fan-out)
- Page width for SOP with notes column: 1600–1900px typical

### When to add a notes column
- Each step has non-trivial description text that would crowd the step box
- You need to show tools used, agent responsible, or specific instructions per step
- The diagram serves as a reference document, not just a quick overview

### SOP two-column XML skeleton

```xml
<mxGraphModel dx="1422" dy="762" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1900" pageHeight="2200" math="0" shadow="0">
  <root>
    <mxCell id="0"/>
    <mxCell id="1" parent="0"/>

    <!-- COLUMN HEADERS -->
    <mxCell id="h1" value="PROCESS STEPS"
      style="rounded=1;whiteSpace=wrap;html=1;fontSize=11;fontStyle=1;align=center;
             fillColor=#dae8fc;strokeColor=#6c8ebf;
             spacingLeft=12;spacingRight=12;spacingTop=10;spacingBottom=10;"
      vertex="1" parent="1">
      <mxGeometry x="50" y="30" width="550" height="40" as="geometry"/>
    </mxCell>

    <mxCell id="h2" value="OPERATING NOTES"
      style="rounded=1;whiteSpace=wrap;html=1;fontSize=11;fontStyle=1;align=center;
             fillColor=#fff2cc;strokeColor=#d6b656;
             spacingLeft=12;spacingRight=12;spacingTop=10;spacingBottom=10;"
      vertex="1" parent="1">
      <mxGeometry x="680" y="30" width="530" height="40" as="geometry"/>
    </mxCell>

    <!-- STEP 1 -->
    <mxCell id="s1" value="1. Step Title"
      style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=11;fontStyle=1;align=left;
             spacingLeft=12;spacingRight=12;spacingTop=10;spacingBottom=10;verticalAlign=top;"
      vertex="1" parent="1">
      <mxGeometry x="50" y="100" width="550" height="50" as="geometry"/>
    </mxCell>

    <!-- Note for Step 1 -->
    <mxCell id="s1_note" value="Description of step 1 tools, agent, and instructions."
      style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;fontSize=10;align=left;
             spacingLeft=12;spacingRight=12;spacingTop=10;spacingBottom=10;verticalAlign=top;"
      vertex="1" parent="1">
      <mxGeometry x="680" y="100" width="530" height="50" as="geometry"/>
    </mxCell>

    <!-- STEP 2 (y = step1.y + step1.height + 140 gap) -->
    <mxCell id="s2" value="2. Next Step"
      style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=11;fontStyle=1;align=left;
             spacingLeft=12;spacingRight=12;spacingTop=10;spacingBottom=10;verticalAlign=top;"
      vertex="1" parent="1">
      <mxGeometry x="50" y="290" width="550" height="50" as="geometry"/>
    </mxCell>

    <!-- Step 1 → Step 2 arrow -->
    <mxCell id="e_s1_s2" value="" style="edgeStyle=orthogonalEdgeStyle;endArrow=block;endFill=1;" edge="1" parent="1" source="s1" target="s2">
      <mxGeometry relative="1" as="geometry"/>
    </mxCell>

  </root>
</mxGraphModel>
```

### Sub-item chaining pattern (for steps with multiple sub-tasks)

```xml
<!-- Step 4 connects to first sub-item only -->
<mxCell id="e_s4_b1" value="" style="edgeStyle=orthogonalEdgeStyle;endArrow=block;endFill=1;" edge="1" parent="1" source="s4" target="b1">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>

<!-- Sub-items chain: b1 → b2 → b3 → b4 -->
<mxCell id="e_b1_b2" value="" style="edgeStyle=orthogonalEdgeStyle;endArrow=block;endFill=1;" edge="1" parent="1" source="b1" target="b2">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
<mxCell id="e_b2_b3" value="" style="edgeStyle=orthogonalEdgeStyle;endArrow=block;endFill=1;" edge="1" parent="1" source="b2" target="b3">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
<mxCell id="e_b3_b4" value="" style="edgeStyle=orthogonalEdgeStyle;endArrow=block;endFill=1;" edge="1" parent="1" source="b3" target="b4">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>

<!-- b4 → next main step (s5) -->
<mxCell id="e_b4_s5" value="" style="edgeStyle=orthogonalEdgeStyle;endArrow=block;endFill=1;" edge="1" parent="1" source="b4" target="s5">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

**Why chain instead of fan-out:** `orthogonalEdgeStyle` does not route around obstacles. Fan-out arrows from one source to multiple stacked targets will route straight through the intermediate boxes. Chaining eliminates all arrow-through-box collisions.

---

## Common errors
- Decisions drawn as processes (should be `rhombus`)
- Missing Yes/No labels on decision exits
- Fan-out arrows to sub-item lists (use chaining instead)
- Zero-gap between last sub-item and next section (cascade downstream nodes down by 20px)
- Text overflowing box bottom (add `verticalAlign=top`, increase height)
- Long-text panels too narrow (widen to 530px+)

## When to ask
- Decision condition is unclear
- Start/end is ambiguous
- Whether the diagram needs a notes column or is a simple linear flow
