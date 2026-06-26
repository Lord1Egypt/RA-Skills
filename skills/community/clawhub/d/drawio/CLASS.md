## TYPE 2: UML Class Diagram

### Qué pedirle al usuario
- Lista de clases con atributos y métodos
- Visibilidad (+/-/#/~) y tipos
- Herencia, implementación, asociaciones y multiplicidades

### Checklist Class
- IDs secuenciales sin saltos
- Tres compartimentos visibles
- Separador entre atributos y métodos
- Sin `\n` en `value` (usar `&#xa;`)
- Spacing mínimo 120px/100px

### Template mínimo Class
```xml
<mxGraphModel page="1" pageWidth="1169" pageHeight="827">
  <root>
    <mxCell id="0"/>
    <mxCell id="1" parent="0"/>
    <mxCell id="10" value="ClassName"
      style="swimlane;fontStyle=1;align=center;startSize=30;fontSize=14;fillColor=#dae8fc;strokeColor=#6c8ebf;"
      vertex="1" parent="1">
      <mxGeometry x="80" y="80" width="220" height="120" as="geometry"/>
    </mxCell>
    <mxCell id="11" value="+attr: Type"
      style="text;strokeColor=none;fillColor=none;align=left;verticalAlign=top;spacingLeft=4;"
      vertex="1" parent="10">
      <mxGeometry y="30" width="220" height="50" as="geometry"/>
    </mxCell>
    <mxCell id="12" value="" style="line;strokeWidth=1;strokeColor=#6c8ebf;" vertex="1" parent="10">
      <mxGeometry y="80" width="220" height="10" as="geometry"/>
    </mxCell>
    <mxCell id="13" value="+method(): Type"
      style="text;strokeColor=none;fillColor=none;align=left;verticalAlign=top;spacingLeft=4;"
      vertex="1" parent="10">
      <mxGeometry y="90" width="220" height="30" as="geometry"/>
    </mxCell>
  </root>
</mxGraphModel>
```

### Reglas de layout
- Herencia de arriba hacia abajo
- Asociaciones laterales
- Mantener alineación por filas

### Errores comunes
- Sin separador entre atributos y métodos
- Multilínea con `\n` en `value`
- Conectar relaciones a celdas de texto

### Cuándo preguntar
- Multiplicidades no indicadas
- Tipos o visibilidades faltantes

### Visual reference
Classes must have three compartments:
1. **Class name** — top section, bold, colored background
2. **Attributes** — middle section, with visibility prefix (+/-/#) and type
3. **Methods** — bottom section, with visibility prefix and return type

### Visibility prefixes
| Symbol | Meaning |
|---|---|
| `+` | public |
| `-` | private |
| `#` | protected |
| `~` | package |

### Color palette by class role
| Role | fillColor | strokeColor |
|---|---|---|
| Regular class | `#dae8fc` | `#6c8ebf` |
| Abstract class | `#e1d5e7` | `#9673a6` |
| Interface | `#d5e8d4` | `#82b366` |
| Enum | `#fff2cc` | `#d6b656` |

### Full XML template

```xml
<mxGraphModel dx="1422" dy="762" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1169" pageHeight="827" math="0" shadow="0">
  <root>
    <mxCell id="0"/>
    <mxCell id="1" parent="0"/>

    <!-- CLASS: Address -->
    <mxCell id="10" value="Address"
      style="swimlane;fontStyle=1;align=center;startSize=30;fontSize=14;fillColor=#dae8fc;strokeColor=#6c8ebf;"
      vertex="1" parent="1">
      <mxGeometry x="300" y="40" width="220" height="160" as="geometry"/>
    </mxCell>
    <!-- Attributes (use &#xa; for line breaks within text cells) -->
    <mxCell id="11" value="+String street&#xa;+String city&#xa;+String state&#xa;+int postalCode&#xa;+String country"
      style="text;strokeColor=none;fillColor=none;align=left;verticalAlign=top;spacingLeft=4;spacingRight=4;overflow=hidden;rotatable=0;fontSize=12;"
      vertex="1" parent="10">
      <mxGeometry y="30" width="220" height="100" as="geometry"/>
    </mxCell>
    <!-- Divider line between attributes and methods -->
    <mxCell id="12" value=""
      style="line;strokeWidth=1;fillColor=none;align=left;strokeColor=#6c8ebf;"
      vertex="1" parent="10">
      <mxGeometry y="130" width="220" height="10" as="geometry"/>
    </mxCell>
    <!-- Methods -->
    <mxCell id="13" value="-validate()&#xa;+outputAsLabel()"
      style="text;strokeColor=none;fillColor=none;align=left;verticalAlign=top;spacingLeft=4;spacingRight=4;overflow=hidden;rotatable=0;fontSize=12;"
      vertex="1" parent="10">
      <mxGeometry y="140" width="220" height="50" as="geometry"/>
    </mxCell>

    <!-- CLASS: Person -->
    <mxCell id="20" value="Person"
      style="swimlane;fontStyle=1;align=center;startSize=30;fontSize=14;fillColor=#dae8fc;strokeColor=#6c8ebf;"
      vertex="1" parent="1">
      <mxGeometry x="300" y="280" width="220" height="140" as="geometry"/>
    </mxCell>
    <mxCell id="21" value="+String name&#xa;+int phoneNumber&#xa;+String emailAddress"
      style="text;strokeColor=none;fillColor=none;align=left;verticalAlign=top;spacingLeft=4;spacingRight=4;overflow=hidden;rotatable=0;fontSize=12;"
      vertex="1" parent="20">
      <mxGeometry y="30" width="220" height="70" as="geometry"/>
    </mxCell>
    <mxCell id="22" value=""
      style="line;strokeWidth=1;fillColor=none;strokeColor=#6c8ebf;"
      vertex="1" parent="20">
      <mxGeometry y="100" width="220" height="10" as="geometry"/>
    </mxCell>
    <mxCell id="23" value="+purchaseParkingPass()"
      style="text;strokeColor=none;fillColor=none;align=left;verticalAlign=top;spacingLeft=4;spacingRight=4;overflow=hidden;rotatable=0;fontSize=12;"
      vertex="1" parent="20">
      <mxGeometry y="110" width="220" height="30" as="geometry"/>
    </mxCell>

    <!-- CLASS: Student (subclass of Person) -->
    <mxCell id="30" value="Student"
      style="swimlane;fontStyle=1;align=center;startSize=30;fontSize=14;fillColor=#e1d5e7;strokeColor=#9673a6;"
      vertex="1" parent="1">
      <mxGeometry x="100" y="520" width="220" height="140" as="geometry"/>
    </mxCell>
    <mxCell id="31" value="+int studentNumber&#xa;+int averageMark"
      style="text;strokeColor=none;fillColor=none;align=left;verticalAlign=top;spacingLeft=4;spacingRight=4;overflow=hidden;rotatable=0;fontSize=12;"
      vertex="1" parent="30">
      <mxGeometry y="30" width="220" height="60" as="geometry"/>
    </mxCell>
    <mxCell id="32" value=""
      style="line;strokeWidth=1;fillColor=none;strokeColor=#9673a6;"
      vertex="1" parent="30">
      <mxGeometry y="90" width="220" height="10" as="geometry"/>
    </mxCell>
    <mxCell id="33" value="+isEligibleToEnroll()&#xa;+getSeminarsTaken()"
      style="text;strokeColor=none;fillColor=none;align=left;verticalAlign=top;spacingLeft=4;spacingRight=4;overflow=hidden;rotatable=0;fontSize=12;"
      vertex="1" parent="30">
      <mxGeometry y="100" width="220" height="50" as="geometry"/>
    </mxCell>

    <!-- CLASS: Professor (subclass of Person) -->
    <mxCell id="40" value="Professor"
      style="swimlane;fontStyle=1;align=center;startSize=30;fontSize=14;fillColor=#e1d5e7;strokeColor=#9673a6;"
      vertex="1" parent="1">
      <mxGeometry x="500" y="520" width="220" height="100" as="geometry"/>
    </mxCell>
    <mxCell id="41" value="+int salary"
      style="text;strokeColor=none;fillColor=none;align=left;verticalAlign=top;spacingLeft=4;spacingRight=4;overflow=hidden;rotatable=0;fontSize=12;"
      vertex="1" parent="40">
      <mxGeometry y="30" width="220" height="30" as="geometry"/>
    </mxCell>
    <mxCell id="42" value=""
      style="line;strokeWidth=1;fillColor=none;strokeColor=#9673a6;"
      vertex="1" parent="40">
      <mxGeometry y="60" width="220" height="10" as="geometry"/>
    </mxCell>

    <!-- RELATIONSHIP: Address -> Person (association "lives at" 0..1) -->
    <mxCell id="80" value="lives at"
      style="edgeStyle=orthogonalEdgeStyle;endArrow=open;endFill=0;startArrow=none;fontSize=11;"
      edge="1" parent="1" source="10" target="20">
      <mxGeometry relative="1" as="geometry"/>
    </mxCell>
    <mxCell id="81" value="0..1" style="resizable=0;align=left;verticalAlign=bottom;labelBackgroundColor=none;fontSize=11;" connectable="0" vertex="1" parent="80">
      <mxGeometry x="-0.7" relative="1" as="geometry"><mxPoint as="offset"/></mxGeometry>
    </mxCell>

    <!-- RELATIONSHIP: Student extends Person (inheritance - hollow triangle) -->
    <mxCell id="82" value=""
      style="edgeStyle=orthogonalEdgeStyle;endArrow=block;endFill=0;startArrow=none;fontSize=11;"
      edge="1" parent="1" source="30" target="20">
      <mxGeometry relative="1" as="geometry"/>
    </mxCell>

    <!-- RELATIONSHIP: Professor extends Person (inheritance - hollow triangle) -->
    <mxCell id="83" value=""
      style="edgeStyle=orthogonalEdgeStyle;endArrow=block;endFill=0;startArrow=none;fontSize=11;"
      edge="1" parent="1" source="40" target="20">
      <mxGeometry relative="1" as="geometry"/>
    </mxCell>

  </root>
</mxGraphModel>
```

### Class Diagram relationship styles
```xml
<!-- Inheritance / Generalization (hollow triangle) -->
style="endArrow=block;endFill=0;startArrow=none;edgeStyle=orthogonalEdgeStyle;"

<!-- Interface implementation (dashed + hollow triangle) -->
style="endArrow=block;endFill=0;startArrow=none;dashed=1;edgeStyle=orthogonalEdgeStyle;"

<!-- Association (open arrow) -->
style="endArrow=open;endFill=0;startArrow=none;edgeStyle=orthogonalEdgeStyle;"

<!-- Aggregation (hollow diamond) -->
style="endArrow=open;startArrow=diamondThin;startFill=0;edgeStyle=orthogonalEdgeStyle;"

<!-- Composition (filled diamond) -->
style="endArrow=open;startArrow=diamondThin;startFill=1;edgeStyle=orthogonalEdgeStyle;"

<!-- Dependency (dashed open arrow) -->
style="endArrow=open;endFill=0;dashed=1;edgeStyle=orthogonalEdgeStyle;"
```

---
