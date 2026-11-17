# TYPE 5: Architecture / System Diagram

## What to ask the user
- Components/services and their responsibilities
- Connection protocols or types
- System boundaries (external vs internal)

## Checklist
- Sequential IDs with no gaps
- Consistent iconography across the diagram
- Connections labeled with protocol/type
- Minimum spacing: 220px horizontal, 180px vertical
- Increase `pageWidth`/`pageHeight` if many components

## Layout rules
- Frontend on the left, data stores on the right
- Core services aligned horizontally in the center
- Use larger grid: `gridSize=20`
- Recommended spacing: 220px between columns, 180px between rows
- For 6+ components: double the page width

## Common errors
- Connections without protocol labels
- Mixing shape styles inconsistently

## When to ask
- Protocol not specified
- System boundaries unclear

## Color palette
| Component type | fillColor | strokeColor |
|---|---|---|
| Frontend / UI | `#dae8fc` | `#6c8ebf` |
| API / Gateway | `#fff2cc` | `#d6b656` |
| Microservice | `#d5e8d4` | `#82b366` |
| Database | `#f5f5f5` | `#666666` |
| Message queue | `#e1d5e7` | `#9673a6` |
| External system | `#f8cecc` | `#b85450` |

## Shape reference
| Component | Shape style |
|---|---|
| Generic service / box | `rounded=1` |
| Database | `shape=cylinder3` |
| Message queue | `shape=mxgraph.cisco.servers.standard_server` |
| User / actor | `shape=mxgraph.flowchart.start_2` |

## Full XML template

```xml
<mxGraphModel dx="1422" dy="762" grid="1" gridSize="20" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1169" pageHeight="827" math="0" shadow="0">
  <root>
    <mxCell id="0"/>
    <mxCell id="1" parent="0"/>

    <!-- Frontend service -->
    <mxCell id="10" value="React Frontend"
      style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=14;fontStyle=1;
             spacingLeft=12;spacingRight=12;spacingTop=10;spacingBottom=10;"
      vertex="1" parent="1">
      <mxGeometry x="100" y="200" width="160" height="60" as="geometry"/>
    </mxCell>

    <!-- API Gateway -->
    <mxCell id="11" value="API Gateway"
      style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;fontSize=14;fontStyle=1;
             spacingLeft=12;spacingRight=12;spacingTop=10;spacingBottom=10;"
      vertex="1" parent="1">
      <mxGeometry x="360" y="200" width="160" height="60" as="geometry"/>
    </mxCell>

    <!-- Microservice -->
    <mxCell id="12" value="Auth Service"
      style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;fontSize=13;
             spacingLeft=12;spacingRight=12;spacingTop=10;spacingBottom=10;"
      vertex="1" parent="1">
      <mxGeometry x="620" y="120" width="140" height="60" as="geometry"/>
    </mxCell>

    <!-- Database cylinder -->
    <mxCell id="13" value="PostgreSQL"
      style="shape=cylinder3;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;fontSize=12;"
      vertex="1" parent="1">
      <mxGeometry x="640" y="300" width="110" height="80" as="geometry"/>
    </mxCell>

    <!-- Message queue -->
    <mxCell id="14" value="RabbitMQ"
      style="shape=mxgraph.cisco.servers.standard_server;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;fontSize=12;"
      vertex="1" parent="1">
      <mxGeometry x="360" y="380" width="80" height="80" as="geometry"/>
    </mxCell>

    <!-- Connections with labels -->
    <mxCell id="20" value="HTTPS"
      style="edgeStyle=orthogonalEdgeStyle;endArrow=block;endFill=1;fontSize=11;"
      edge="1" parent="1" source="10" target="11">
      <mxGeometry relative="1" as="geometry"/>
    </mxCell>

    <mxCell id="21" value="REST"
      style="edgeStyle=orthogonalEdgeStyle;endArrow=block;endFill=1;fontSize=11;"
      edge="1" parent="1" source="11" target="12">
      <mxGeometry relative="1" as="geometry"/>
    </mxCell>

    <mxCell id="22" value="SQL"
      style="edgeStyle=orthogonalEdgeStyle;endArrow=block;endFill=1;fontSize=11;"
      edge="1" parent="1" source="12" target="13">
      <mxGeometry relative="1" as="geometry"/>
    </mxCell>

  </root>
</mxGraphModel>
```

---
