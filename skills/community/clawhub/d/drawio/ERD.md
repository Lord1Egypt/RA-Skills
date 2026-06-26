## TYPE 1: ERD / Database Diagram

### Qué pedirle al usuario
- Lista de tablas con columnas y tipos
- PK/FK y cardinalidades (1:1, 1:N, N:M)
- Reglas de negocio relevantes (unicidad, nullable)
- Tablas lookup o junction si existen

### Checklist ERD
- IDs `mxCell` secuenciales sin saltos
- Alturas: `30 + (columnas x 30)`
- FK conectadas a la fila, no al contenedor
- Sin `\n` en `value`
- Spacing mínimo: 120px horizontal, 100px vertical

### Template mínimo ERD
```xml
<mxGraphModel page="1" pageWidth="1169" pageHeight="827">
  <root>
    <mxCell id="0"/>
    <mxCell id="1" parent="0"/>
    <mxCell id="10" value="Tabla"
      style="shape=table;startSize=30;container=1;collapsible=0;childLayout=tableLayout;fixedRows=1;rowLines=0;fontStyle=1;fontSize=14;align=center;fillColor=#dae8fc;strokeColor=#6c8ebf;"
      vertex="1" parent="1">
      <mxGeometry x="80" y="80" width="220" height="90" as="geometry"/>
    </mxCell>
    <mxCell id="11" value="" style="shape=tableRow;horizontal=0;bottom=1;" vertex="1" parent="10">
      <mxGeometry y="30" width="220" height="30" as="geometry"/>
    </mxCell>
    <mxCell id="12" value="PK" style="shape=partialRectangle;fillColor=#fff2cc;strokeColor=#d6b656;" vertex="1" parent="11">
      <mxGeometry width="40" height="30" as="geometry"/>
    </mxCell>
    <mxCell id="13" value="id INT" style="shape=partialRectangle;fillColor=none;" vertex="1" parent="11">
      <mxGeometry x="40" width="180" height="30" as="geometry"/>
    </mxCell>
  </root>
</mxGraphModel>
```

### Reglas de layout
- Usar grilla de 4 tablas cuando aplique
- Separación mínima 120px/100px
- No cruzar relaciones por headers

### Errores comunes
- Relación conectada al contenedor en vez de la fila
- Altura incorrecta del contenedor
- Reutilizar IDs
- Usar rectángulos genéricos

### Cuándo preguntar
- Cardinalidades no especificadas
- FK no identificadas
- Columnas sin tipos

### Visual reference
Tables must look like real database tables:
- A **header row** with the table name (colored background)
- **Individual rows** for each column, with PK/FK badges on the left
- **Relationship lines** with crow's foot notation connecting FK rows to PK rows

### Table height formula
```
table_height = 30 (header) + (number_of_columns x 30)
Example: 5 columns -> height = 30 + (5 x 30) = 180
```

### Color palette by table type
| Table role | fillColor | strokeColor |
|---|---|---|
| Primary / main entity | `#dae8fc` | `#6c8ebf` |
| Secondary entity | `#e1d5e7` | `#9673a6` |
| Junction / pivot table | `#d5e8d4` | `#82b366` |
| Lookup / catalog table | `#fff2cc` | `#d6b656` |

### Column badge colors
| Badge | fillColor | strokeColor |
|---|---|---|
| PK | `#fff2cc` | `#d6b656` |
| FK | `#f8cecc` | `#b85450` |
| UK (unique) | `#d5e8d4` | `#82b366` |
| (none) | `none` | `none` |

### Full XML template

```xml
<mxGraphModel dx="1422" dy="762" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1169" pageHeight="827" math="0" shadow="0">
  <root>
    <mxCell id="0"/>
    <mxCell id="1" parent="0"/>

    <!-- TABLE: Cliente | height = 30 + (5 x 30) = 180 -->
    <mxCell id="10" value="Cliente"
      style="shape=table;startSize=30;container=1;collapsible=0;childLayout=tableLayout;fixedRows=1;rowLines=0;fontStyle=1;fontSize=14;align=center;fillColor=#dae8fc;strokeColor=#6c8ebf;fontColor=#000000;swimlaneLine=1;"
      vertex="1" parent="1">
      <mxGeometry x="80" y="80" width="220" height="180" as="geometry"/>
    </mxCell>

    <!-- Row: ID (PK) - bottom=1 adds separator line after PK -->
    <mxCell id="11" value=""
      style="shape=tableRow;horizontal=0;startSize=0;swimlaneHead=0;swimlaneBody=0;fillColor=#dae8fc;collapsible=0;dropTarget=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;fontSize=12;top=0;left=0;right=0;bottom=1;"
      vertex="1" parent="10">
      <mxGeometry y="30" width="220" height="30" as="geometry"/>
    </mxCell>
    <mxCell id="12" value="PK"
      style="shape=partialRectangle;connectable=0;fillColor=#fff2cc;strokeColor=#d6b656;top=0;left=0;bottom=0;right=0;fontStyle=1;fontSize=11;overflow=hidden;align=center;"
      vertex="1" parent="11">
      <mxGeometry width="40" height="30" as="geometry"><mxRectangle width="40" height="30" as="alternateBounds"/></mxGeometry>
    </mxCell>
    <mxCell id="13" value="ID INT"
      style="shape=partialRectangle;connectable=0;fillColor=none;top=0;left=0;bottom=0;right=0;overflow=hidden;fontSize=12;"
      vertex="1" parent="11">
      <mxGeometry x="40" width="180" height="30" as="geometry"><mxRectangle width="180" height="30" as="alternateBounds"/></mxGeometry>
    </mxCell>

    <!-- Row: Nombre -->
    <mxCell id="14" value=""
      style="shape=tableRow;horizontal=0;startSize=0;swimlaneHead=0;swimlaneBody=0;fillColor=none;collapsible=0;dropTarget=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;fontSize=12;top=0;left=0;right=0;bottom=0;"
      vertex="1" parent="10">
      <mxGeometry y="60" width="220" height="30" as="geometry"/>
    </mxCell>
    <mxCell id="15" value=""
      style="shape=partialRectangle;connectable=0;fillColor=none;top=0;left=0;bottom=0;right=0;overflow=hidden;"
      vertex="1" parent="14">
      <mxGeometry width="40" height="30" as="geometry"><mxRectangle width="40" height="30" as="alternateBounds"/></mxGeometry>
    </mxCell>
    <mxCell id="16" value="Nombre VARCHAR(100)"
      style="shape=partialRectangle;connectable=0;fillColor=none;top=0;left=0;bottom=0;right=0;overflow=hidden;fontSize=12;"
      vertex="1" parent="14">
      <mxGeometry x="40" width="180" height="30" as="geometry"><mxRectangle width="180" height="30" as="alternateBounds"/></mxGeometry>
    </mxCell>

    <!-- Row: Apellidos -->
    <mxCell id="17" value=""
      style="shape=tableRow;horizontal=0;startSize=0;swimlaneHead=0;swimlaneBody=0;fillColor=none;collapsible=0;dropTarget=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;fontSize=12;top=0;left=0;right=0;bottom=0;"
      vertex="1" parent="10">
      <mxGeometry y="90" width="220" height="30" as="geometry"/>
    </mxCell>
    <mxCell id="18" value=""
      style="shape=partialRectangle;connectable=0;fillColor=none;top=0;left=0;bottom=0;right=0;overflow=hidden;"
      vertex="1" parent="17">
      <mxGeometry width="40" height="30" as="geometry"><mxRectangle width="40" height="30" as="alternateBounds"/></mxGeometry>
    </mxCell>
    <mxCell id="19" value="Apellidos VARCHAR(100)"
      style="shape=partialRectangle;connectable=0;fillColor=none;top=0;left=0;bottom=0;right=0;overflow=hidden;fontSize=12;"
      vertex="1" parent="17">
      <mxGeometry x="40" width="180" height="30" as="geometry"><mxRectangle width="180" height="30" as="alternateBounds"/></mxGeometry>
    </mxCell>

    <!-- Row: Movil -->
    <mxCell id="20" value=""
      style="shape=tableRow;horizontal=0;startSize=0;swimlaneHead=0;swimlaneBody=0;fillColor=none;collapsible=0;dropTarget=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;fontSize=12;top=0;left=0;right=0;bottom=0;"
      vertex="1" parent="10">
      <mxGeometry y="120" width="220" height="30" as="geometry"/>
    </mxCell>
    <mxCell id="21" value=""
      style="shape=partialRectangle;connectable=0;fillColor=none;top=0;left=0;bottom=0;right=0;overflow=hidden;"
      vertex="1" parent="20">
      <mxGeometry width="40" height="30" as="geometry"><mxRectangle width="40" height="30" as="alternateBounds"/></mxGeometry>
    </mxCell>
    <mxCell id="22" value="Movil VARCHAR(20)"
      style="shape=partialRectangle;connectable=0;fillColor=none;top=0;left=0;bottom=0;right=0;overflow=hidden;fontSize=12;"
      vertex="1" parent="20">
      <mxGeometry x="40" width="180" height="30" as="geometry"><mxRectangle width="180" height="30" as="alternateBounds"/></mxGeometry>
    </mxCell>

    <!-- Row: EMail -->
    <mxCell id="23" value=""
      style="shape=tableRow;horizontal=0;startSize=0;swimlaneHead=0;swimlaneBody=0;fillColor=none;collapsible=0;dropTarget=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;fontSize=12;top=0;left=0;right=0;bottom=0;"
      vertex="1" parent="10">
      <mxGeometry y="150" width="220" height="30" as="geometry"/>
    </mxCell>
    <mxCell id="24" value=""
      style="shape=partialRectangle;connectable=0;fillColor=none;top=0;left=0;bottom=0;right=0;overflow=hidden;"
      vertex="1" parent="23">
      <mxGeometry width="40" height="30" as="geometry"><mxRectangle width="40" height="30" as="alternateBounds"/></mxGeometry>
    </mxCell>
    <mxCell id="25" value="EMail VARCHAR(150)"
      style="shape=partialRectangle;connectable=0;fillColor=none;top=0;left=0;bottom=0;right=0;overflow=hidden;fontSize=12;"
      vertex="1" parent="23">
      <mxGeometry x="40" width="180" height="30" as="geometry"><mxRectangle width="180" height="30" as="alternateBounds"/></mxGeometry>
    </mxCell>

    <!-- TABLE: Pedido | height = 30 + (3 x 30) = 120 -->
    <mxCell id="30" value="Pedido"
      style="shape=table;startSize=30;container=1;collapsible=0;childLayout=tableLayout;fixedRows=1;rowLines=0;fontStyle=1;fontSize=14;align=center;fillColor=#e1d5e7;strokeColor=#9673a6;fontColor=#000000;swimlaneLine=1;"
      vertex="1" parent="1">
      <mxGeometry x="80" y="380" width="220" height="120" as="geometry"/>
    </mxCell>

    <!-- Row: ID (PK) -->
    <mxCell id="31" value=""
      style="shape=tableRow;horizontal=0;startSize=0;swimlaneHead=0;swimlaneBody=0;fillColor=#e1d5e7;collapsible=0;dropTarget=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;fontSize=12;top=0;left=0;right=0;bottom=1;"
      vertex="1" parent="30">
      <mxGeometry y="30" width="220" height="30" as="geometry"/>
    </mxCell>
    <mxCell id="32" value="PK"
      style="shape=partialRectangle;connectable=0;fillColor=#fff2cc;strokeColor=#d6b656;top=0;left=0;bottom=0;right=0;fontStyle=1;fontSize=11;overflow=hidden;align=center;"
      vertex="1" parent="31">
      <mxGeometry width="40" height="30" as="geometry"><mxRectangle width="40" height="30" as="alternateBounds"/></mxGeometry>
    </mxCell>
    <mxCell id="33" value="ID INT"
      style="shape=partialRectangle;connectable=0;fillColor=none;top=0;left=0;bottom=0;right=0;overflow=hidden;fontSize=12;"
      vertex="1" parent="31">
      <mxGeometry x="40" width="180" height="30" as="geometry"><mxRectangle width="180" height="30" as="alternateBounds"/></mxGeometry>
    </mxCell>

    <!-- Row: Fecha -->
    <mxCell id="34" value=""
      style="shape=tableRow;horizontal=0;startSize=0;swimlaneHead=0;swimlaneBody=0;fillColor=none;collapsible=0;dropTarget=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;fontSize=12;top=0;left=0;right=0;bottom=0;"
      vertex="1" parent="30">
      <mxGeometry y="60" width="220" height="30" as="geometry"/>
    </mxCell>
    <mxCell id="35" value=""
      style="shape=partialRectangle;connectable=0;fillColor=none;top=0;left=0;bottom=0;right=0;overflow=hidden;"
      vertex="1" parent="34">
      <mxGeometry width="40" height="30" as="geometry"><mxRectangle width="40" height="30" as="alternateBounds"/></mxGeometry>
    </mxCell>
    <mxCell id="36" value="Fecha DATE"
      style="shape=partialRectangle;connectable=0;fillColor=none;top=0;left=0;bottom=0;right=0;overflow=hidden;fontSize=12;"
      vertex="1" parent="34">
      <mxGeometry x="40" width="180" height="30" as="geometry"><mxRectangle width="180" height="30" as="alternateBounds"/></mxGeometry>
    </mxCell>

    <!-- Row: ClienteID (FK) -->
    <mxCell id="37" value=""
      style="shape=tableRow;horizontal=0;startSize=0;swimlaneHead=0;swimlaneBody=0;fillColor=none;collapsible=0;dropTarget=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;fontSize=12;top=0;left=0;right=0;bottom=0;"
      vertex="1" parent="30">
      <mxGeometry y="90" width="220" height="30" as="geometry"/>
    </mxCell>
    <mxCell id="38" value="FK"
      style="shape=partialRectangle;connectable=0;fillColor=#f8cecc;strokeColor=#b85450;top=0;left=0;bottom=0;right=0;fontStyle=1;fontSize=11;overflow=hidden;align=center;"
      vertex="1" parent="37">
      <mxGeometry width="40" height="30" as="geometry"><mxRectangle width="40" height="30" as="alternateBounds"/></mxGeometry>
    </mxCell>
    <mxCell id="39" value="ClienteID INT"
      style="shape=partialRectangle;connectable=0;fillColor=none;top=0;left=0;bottom=0;right=0;overflow=hidden;fontSize=12;"
      vertex="1" parent="37">
      <mxGeometry x="40" width="180" height="30" as="geometry"><mxRectangle width="180" height="30" as="alternateBounds"/></mxGeometry>
    </mxCell>

    <!-- RELATIONSHIP: Cliente 1 to N Pedido -->
    <!-- source=FK row of Pedido, target=PK row of Cliente -->
    <mxCell id="90" value=""
      style="edgeStyle=entityRelationEdgeStyle;endArrow=ERmandOne;startArrow=ERzeroToMany;exitX=0;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;fontSize=11;"
      edge="1" parent="1" source="37" target="11">
      <mxGeometry relative="1" as="geometry"/>
    </mxCell>

  </root>
</mxGraphModel>
```

### ERD Relationship styles (crow's foot notation)
```xml
<!-- One-to-Many (1:N) -->
style="edgeStyle=entityRelationEdgeStyle;endArrow=ERmandOne;startArrow=ERzeroToMany;"

<!-- One-to-Many mandatory -->
style="edgeStyle=entityRelationEdgeStyle;endArrow=ERmandOne;startArrow=ERmandMany;"

<!-- Zero-or-One to Many -->
style="edgeStyle=entityRelationEdgeStyle;endArrow=ERzeroToOne;startArrow=ERzeroToMany;"

<!-- Many-to-Many (N:M) -->
style="edgeStyle=entityRelationEdgeStyle;endArrow=ERzeroToMany;startArrow=ERzeroToMany;"
```

### ERD Layout positions (4-table grid)
```
Table A (primary):   x=80,  y=80
Table B (primary):   x=420, y=80
Table C (secondary): x=80,  y=380
Table D (junction):  x=420, y=380
```
For 5+ tables: set `pageWidth="1654" pageHeight="1169"` in mxGraphModel.

---
