## TYPE 4: Flowchart

### Qué pedirle al usuario
- Lista de pasos y decisiones
- Entradas/salidas y documentos
- Condiciones para ramas

### Checklist Flowchart
- IDs secuenciales sin saltos
- Formas correctas por tipo
- Decisiones con salidas Sí/No
- Spacing mínimo 180px horizontal / 140px vertical
- Aumentar `pageWidth`/`pageHeight` si hay muchos nodos

### Template mínimo Flowchart
```xml
<mxGraphModel page="1" pageWidth="850" pageHeight="1100">
  <root>
    <mxCell id="0"/>
    <mxCell id="1" parent="0"/>
    <mxCell id="10" value="Start" style="ellipse;" vertex="1" parent="1">
      <mxGeometry x="300" y="40" width="120" height="50" as="geometry"/>
    </mxCell>
    <mxCell id="11" value="Process" style="rounded=1;" vertex="1" parent="1">
      <mxGeometry x="300" y="140" width="150" height="50" as="geometry"/>
    </mxCell>
    <mxCell id="20" value="" style="endArrow=block;endFill=1;" edge="1" parent="1" source="10" target="11">
      <mxGeometry relative="1" as="geometry"/>
    </mxCell>
  </root>
</mxGraphModel>
```

### Reglas de layout
- Flujo principal vertical
- Ramas laterales con separaciones claras
- Usar grilla más grande para separar: `gridSize=20`
- Separación recomendada: 200px entre columnas y 160px entre filas
- Si hay más de 8 nodos, duplicar ancho o alto de página

### Errores comunes
- Decisiones dibujadas como procesos
- Flechas sin etiquetas Sí/No

### Cuándo preguntar
- Falta condición de decisión
- No queda claro el inicio/fin

### Shape reference
| Shape | Style keyword | Use for |
|---|---|---|
| Start / End | `ellipse` | Terminal nodes |
| Process / Action | `rounded=1` | Steps and actions |
| Decision | `rhombus` | Yes/No branches |
| Document | `shape=document` | Reports or output documents |
| Data | `shape=parallelogram` | Input or output data |

### Color palette
| Shape | fillColor | strokeColor |
|---|---|---|
| Start | `#d5e8d4` | `#82b366` |
| Process | `#dae8fc` | `#6c8ebf` |
| Decision | `#fff2cc` | `#d6b656` |
| End | `#f8cecc` | `#b85450` |

### XML template
```xml
<mxGraphModel dx="1422" dy="762" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="850" pageHeight="1100" math="0" shadow="0">
  <root>
    <mxCell id="0"/>
    <mxCell id="1" parent="0"/>

    <mxCell id="10" value="Start"
      style="ellipse;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;fontSize=13;fontStyle=1;"
      vertex="1" parent="1">
      <mxGeometry x="300" y="40" width="120" height="50" as="geometry"/>
    </mxCell>

    <mxCell id="11" value="Receive Request"
      style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=12;"
      vertex="1" parent="1">
      <mxGeometry x="300" y="140" width="150" height="50" as="geometry"/>
    </mxCell>

    <mxCell id="12" value="Is Valid?"
      style="rhombus;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;fontSize=12;"
      vertex="1" parent="1">
      <mxGeometry x="280" y="245" width="190" height="70" as="geometry"/>
    </mxCell>

    <mxCell id="13" value="Process Data"
      style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=12;"
      vertex="1" parent="1">
      <mxGeometry x="300" y="370" width="150" height="50" as="geometry"/>
    </mxCell>

    <mxCell id="14" value="Show Error"
      style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;fontSize=12;"
      vertex="1" parent="1">
      <mxGeometry x="530" y="245" width="130" height="50" as="geometry"/>
    </mxCell>

    <mxCell id="15" value="End"
      style="ellipse;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;fontSize=13;fontStyle=1;"
      vertex="1" parent="1">
      <mxGeometry x="310" y="480" width="120" height="50" as="geometry"/>
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
