## TYPE 3: Sequence Diagram

### Qué pedirle al usuario
- Participantes y orden de aparición
- Mensajes con numeración y tipo (sync/async/return)
- Condiciones (alt/opt/loop) si existen

### Checklist Sequence
- IDs secuenciales sin saltos
- Lifelines con estilo dashed
- Activations alineadas a mensajes
- Flechas con estilos correctos
- Spacing mínimo 120px/100px

### Template mínimo Sequence
```xml
<mxGraphModel page="1" pageWidth="1169" pageHeight="827">
  <root>
    <mxCell id="0"/>
    <mxCell id="1" parent="0"/>
    <mxCell id="10" value=":User" style="shape=mxgraph.flowchart.start_2;" vertex="1" parent="1">
      <mxGeometry x="80" y="40" width="50" height="60" as="geometry"/>
    </mxCell>
    <mxCell id="11" value=":Service" style="rounded=0;" vertex="1" parent="1">
      <mxGeometry x="220" y="50" width="140" height="40" as="geometry"/>
    </mxCell>
    <mxCell id="20" value="" style="dashed=1;endArrow=none;" edge="1" parent="1" source="10">
      <mxGeometry relative="1" as="geometry">
        <Array as="points"><mxPoint x="105" y="100"/><mxPoint x="105" y="500"/></Array>
      </mxGeometry>
    </mxCell>
    <mxCell id="21" value="" style="dashed=1;endArrow=none;" edge="1" parent="1" source="11">
      <mxGeometry relative="1" as="geometry">
        <Array as="points"><mxPoint x="290" y="90"/><mxPoint x="290" y="500"/></Array>
      </mxGeometry>
    </mxCell>
    <mxCell id="30" value="1: request()" style="endArrow=block;endFill=1;" edge="1" parent="1">
      <mxGeometry relative="1" as="geometry">
        <Array as="points"><mxPoint x="105" y="160"/><mxPoint x="290" y="160"/></Array>
      </mxGeometry>
    </mxCell>
  </root>
</mxGraphModel>
```

### Reglas de layout
- Participantes de izquierda a derecha
- Mensajes de arriba hacia abajo
- Frames cubren el rango de mensajes

### Errores comunes
- Lifelines sin dashed
- Activations fuera de alineación
- Flechas de retorno no dashed

### Cuándo preguntar
- Tipo de mensaje no especificado
- Faltan participantes

### Visual reference
Sequence diagrams must include:
- **Actor** on the far left (stick figure or person shape)
- **Lifelines** as vertical dashed lines below each participant header
- **Activation boxes** (narrow tall rectangles) on lifelines when a participant is active
- **Message arrows** — solid filled for calls, dashed open for returns
- **Alt/Loop/Opt frames** as large containers for conditional sections
- Numbered messages following UML notation (1, 1.1, 1.2, 1.2.1, etc.)

### Participant header shapes
| Participant type | Shape style |
|---|---|
| Human actor | `shape=mxgraph.flowchart.start_2` with label below |
| Object / class instance | Plain rectangle `rounded=0` |
| Database | `shape=cylinder3` |
| Boundary / UI | `ellipse` or rectangle |
| External system | `rounded=1` with different color |

### Message arrow styles
```xml
<!-- Synchronous call (solid filled arrowhead) -->
style="endArrow=block;endFill=1;startArrow=none;edgeStyle=orthogonalEdgeStyle;"

<!-- Return / response (dashed open arrow) -->
style="endArrow=open;endFill=0;dashed=1;startArrow=none;edgeStyle=orthogonalEdgeStyle;"

<!-- Asynchronous message (open arrowhead) -->
style="endArrow=open;endFill=0;startArrow=none;edgeStyle=orthogonalEdgeStyle;"

<!-- Self-call (routes out right and back on the same x position) -->
<!-- Use explicit waypoints in the geometry Array -->
```

### Full XML template

```xml
<mxGraphModel dx="1422" dy="762" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1169" pageHeight="827" math="0" shadow="0">
  <root>
    <mxCell id="0"/>
    <mxCell id="1" parent="0"/>

    <!-- PARTICIPANT HEADERS -->

    <!-- Actor: Customer -->
    <mxCell id="10" value=":Customer"
      style="shape=mxgraph.flowchart.start_2;fillColor=#f5f5f5;strokeColor=#666666;fontColor=#333333;fontSize=12;fontStyle=1;align=center;verticalLabelPosition=bottom;verticalAlign=top;"
      vertex="1" parent="1">
      <mxGeometry x="60" y="40" width="50" height="60" as="geometry"/>
    </mxCell>

    <!-- Object: SearchForm -->
    <mxCell id="11" value=":SearchForm"
      style="rounded=0;whiteSpace=wrap;html=1;fillColor=#FFE6CC;strokeColor=#d79b00;fontStyle=1;fontSize=13;align=center;"
      vertex="1" parent="1">
      <mxGeometry x="220" y="50" width="140" height="40" as="geometry"/>
    </mxCell>

    <!-- Object: SearchResults -->
    <mxCell id="12" value=":SearchResults"
      style="rounded=0;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontStyle=1;fontSize=13;align=center;"
      vertex="1" parent="1">
      <mxGeometry x="440" y="50" width="140" height="40" as="geometry"/>
    </mxCell>

    <!-- Object: ItemDatabase (circle/boundary) -->
    <mxCell id="13" value=":ItemDatabase"
      style="ellipse;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;fontStyle=1;fontSize=12;align=center;"
      vertex="1" parent="1">
      <mxGeometry x="650" y="35" width="130" height="60" as="geometry"/>
    </mxCell>

    <!-- Object: ResultList -->
    <mxCell id="14" value=":ResultList"
      style="rounded=0;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;fontStyle=1;fontSize=13;align=center;"
      vertex="1" parent="1">
      <mxGeometry x="850" y="50" width="120" height="40" as="geometry"/>
    </mxCell>

    <!-- LIFELINES (vertical dashed lines) -->
    <!-- Draw each as a tall thin rectangle with dashed style -->

    <mxCell id="20" value=""
      style="edgeStyle=none;dashed=1;endArrow=none;startArrow=none;strokeColor=#666666;exitX=0.5;exitY=1;exitDx=0;exitDy=0;"
      edge="1" parent="1" source="10">
      <mxGeometry relative="1" as="geometry">
        <Array as="points">
          <mxPoint x="85" y="100"/>
          <mxPoint x="85" y="640"/>
        </Array>
      </mxGeometry>
    </mxCell>

    <mxCell id="21" value=""
      style="edgeStyle=none;dashed=1;endArrow=none;startArrow=none;strokeColor=#d79b00;exitX=0.5;exitY=1;exitDx=0;exitDy=0;"
      edge="1" parent="1" source="11">
      <mxGeometry relative="1" as="geometry">
        <Array as="points">
          <mxPoint x="290" y="90"/>
          <mxPoint x="290" y="640"/>
        </Array>
      </mxGeometry>
    </mxCell>

    <mxCell id="22" value=""
      style="edgeStyle=none;dashed=1;endArrow=none;startArrow=none;strokeColor=#6c8ebf;exitX=0.5;exitY=1;exitDx=0;exitDy=0;"
      edge="1" parent="1" source="12">
      <mxGeometry relative="1" as="geometry">
        <Array as="points">
          <mxPoint x="510" y="90"/>
          <mxPoint x="510" y="640"/>
        </Array>
      </mxGeometry>
    </mxCell>

    <mxCell id="23" value=""
      style="edgeStyle=none;dashed=1;endArrow=none;startArrow=none;strokeColor=#9673a6;exitX=0.5;exitY=1;exitDx=0;exitDy=0;"
      edge="1" parent="1" source="13">
      <mxGeometry relative="1" as="geometry">
        <Array as="points">
          <mxPoint x="715" y="95"/>
          <mxPoint x="715" y="640"/>
        </Array>
      </mxGeometry>
    </mxCell>

    <mxCell id="24" value=""
      style="edgeStyle=none;dashed=1;endArrow=none;startArrow=none;strokeColor=#82b366;exitX=0.5;exitY=1;exitDx=0;exitDy=0;"
      edge="1" parent="1" source="14">
      <mxGeometry relative="1" as="geometry">
        <Array as="points">
          <mxPoint x="910" y="90"/>
          <mxPoint x="910" y="640"/>
        </Array>
      </mxGeometry>
    </mxCell>

    <!-- ACTIVATION BOXES (narrow rectangles on lifelines) -->

    <mxCell id="30" value="" style="fillColor=#f5f5f5;strokeColor=#666666;" vertex="1" parent="1">
      <mxGeometry x="78" y="135" width="14" height="400" as="geometry"/>
    </mxCell>

    <mxCell id="31" value="" style="fillColor=#FFE6CC;strokeColor=#d79b00;" vertex="1" parent="1">
      <mxGeometry x="283" y="155" width="14" height="360" as="geometry"/>
    </mxCell>

    <mxCell id="32" value="" style="fillColor=#e1d5e7;strokeColor=#9673a6;" vertex="1" parent="1">
      <mxGeometry x="708" y="235" width="14" height="90" as="geometry"/>
    </mxCell>

    <mxCell id="33" value="" style="fillColor=#d5e8d4;strokeColor=#82b366;" vertex="1" parent="1">
      <mxGeometry x="903" y="255" width="14" height="60" as="geometry"/>
    </mxCell>

    <!-- ALT FRAME -->
    <mxCell id="40" value="alt"
      style="swimlane;startSize=20;swimlaneLine=1;fillColor=none;strokeColor=#666666;align=left;spacingLeft=5;fontSize=12;fontStyle=1;"
      vertex="1" parent="1">
      <mxGeometry x="120" y="168" width="840" height="360" as="geometry"/>
    </mxCell>

    <!-- Alt condition text -->
    <mxCell id="41" value="[itemName=valid]"
      style="text;strokeColor=none;fillColor=none;align=left;fontSize=11;fontStyle=2;"
      vertex="1" parent="1">
      <mxGeometry x="125" y="172" width="160" height="20" as="geometry"/>
    </mxCell>

    <!-- Else divider line -->
    <mxCell id="42" value=""
      style="edgeStyle=none;dashed=1;endArrow=none;startArrow=none;strokeColor=#666666;"
      edge="1" parent="1">
      <mxGeometry relative="1" as="geometry">
        <Array as="points">
          <mxPoint x="120" y="400"/>
          <mxPoint x="960" y="400"/>
        </Array>
      </mxGeometry>
    </mxCell>
    <mxCell id="43" value="[else]"
      style="text;strokeColor=none;fillColor=none;align=left;fontSize=11;fontStyle=2;"
      vertex="1" parent="1">
      <mxGeometry x="125" y="402" width="80" height="20" as="geometry"/>
    </mxCell>

    <!-- MESSAGE ARROWS -->

    <!-- 1: itemSearch(itemName) Customer -> SearchForm -->
    <mxCell id="50" value="1: itemSearch(itemName)"
      style="edgeStyle=orthogonalEdgeStyle;endArrow=block;endFill=1;startArrow=none;fontSize=11;"
      edge="1" parent="1">
      <mxGeometry relative="1" as="geometry">
        <Array as="points">
          <mxPoint x="92" y="155"/>
          <mxPoint x="283" y="155"/>
        </Array>
      </mxGeometry>
    </mxCell>

    <!-- 1.1: validSearch() SearchForm self-call -->
    <mxCell id="51" value="1.1: validSearch()"
      style="edgeStyle=orthogonalEdgeStyle;endArrow=block;endFill=1;startArrow=none;fontSize=11;"
      edge="1" parent="1">
      <mxGeometry relative="1" as="geometry">
        <Array as="points">
          <mxPoint x="297" y="190"/>
          <mxPoint x="340" y="190"/>
          <mxPoint x="340" y="215"/>
          <mxPoint x="297" y="215"/>
        </Array>
      </mxGeometry>
    </mxCell>

    <!-- 1.2: SearchItems(itemName) SearchForm -> ItemDatabase -->
    <mxCell id="52" value="1.2: SearchItems(itemName)"
      style="edgeStyle=orthogonalEdgeStyle;endArrow=block;endFill=1;startArrow=none;fontSize=11;"
      edge="1" parent="1">
      <mxGeometry relative="1" as="geometry">
        <Array as="points">
          <mxPoint x="297" y="240"/>
          <mxPoint x="708" y="240"/>
        </Array>
      </mxGeometry>
    </mxCell>

    <!-- 1.2.1: listResults() ItemDatabase -> ResultList -->
    <mxCell id="53" value="1.2.1: listResults()"
      style="edgeStyle=orthogonalEdgeStyle;endArrow=block;endFill=1;startArrow=none;fontSize=11;"
      edge="1" parent="1">
      <mxGeometry relative="1" as="geometry">
        <Array as="points">
          <mxPoint x="722" y="265"/>
          <mxPoint x="903" y="265"/>
        </Array>
      </mxGeometry>
    </mxCell>

    <!-- 1.2.1.1: displayResults() ResultList -> SearchResults (return dashed) -->
    <mxCell id="54" value="1.2.1.1: displayResults()"
      style="edgeStyle=orthogonalEdgeStyle;endArrow=open;endFill=0;dashed=1;startArrow=none;fontSize=11;"
      edge="1" parent="1">
      <mxGeometry relative="1" as="geometry">
        <Array as="points">
          <mxPoint x="903" y="300"/>
          <mxPoint x="510" y="300"/>
        </Array>
      </mxGeometry>
    </mxCell>

    <!-- 1.3: displayError() SearchForm -> Customer (else branch) -->
    <mxCell id="55" value="1.3: displayError()"
      style="edgeStyle=orthogonalEdgeStyle;endArrow=block;endFill=1;startArrow=none;fontSize=11;"
      edge="1" parent="1">
      <mxGeometry relative="1" as="geometry">
        <Array as="points">
          <mxPoint x="283" y="430"/>
          <mxPoint x="92" y="430"/>
        </Array>
      </mxGeometry>
    </mxCell>

    <!-- Return dashed arrow back to Customer -->
    <mxCell id="56" value=""
      style="edgeStyle=orthogonalEdgeStyle;endArrow=open;endFill=0;dashed=1;startArrow=none;fontSize=11;"
      edge="1" parent="1">
      <mxGeometry relative="1" as="geometry">
        <Array as="points">
          <mxPoint x="283" y="510"/>
          <mxPoint x="92" y="510"/>
        </Array>
      </mxGeometry>
    </mxCell>

  </root>
</mxGraphModel>
```

---
