## TYPE 5: Architecture Diagram

### Qué pedirle al usuario
- Componentes/servicios y responsabilidades
- Protocolos o tipos de conexión
- Límites del sistema (externos/internos)

### Checklist Architecture
- IDs secuenciales sin saltos
- Iconografía consistente
- Conexiones etiquetadas
- Spacing mínimo 220px horizontal / 180px vertical
- Aumentar `pageWidth`/`pageHeight` si hay muchos componentes

### Template mínimo Architecture
```xml
<mxGraphModel page="1" pageWidth="1169" pageHeight="827">
  <root>
    <mxCell id="0"/>
    <mxCell id="1" parent="0"/>
    <mxCell id="10" value="Frontend" style="rounded=1;" vertex="1" parent="1">
      <mxGeometry x="100" y="200" width="160" height="60" as="geometry"/>
    </mxCell>
    <mxCell id="11" value="API" style="rounded=1;" vertex="1" parent="1">
      <mxGeometry x="360" y="200" width="160" height="60" as="geometry"/>
    </mxCell>
    <mxCell id="20" value="HTTPS" style="endArrow=block;endFill=1;" edge="1" parent="1" source="10" target="11">
      <mxGeometry relative="1" as="geometry"/>
    </mxCell>
  </root>
</mxGraphModel>
```

### Reglas de layout
- Frontend a la izquierda, datos a la derecha
- Servicios centrales alineados horizontalmente
- Usar grilla más grande para separar: `gridSize=20`
- Separación recomendada: 220px entre columnas y 180px entre filas
- Si hay más de 6 componentes, duplicar el ancho de página

### Errores comunes
- Conexiones sin protocolo
- Mezclar estilos de shapes

### Cuándo preguntar
- Protocolo no especificado
- Faltan límites del sistema

```xml
<!-- Frontend service -->
<mxCell id="10" value="React Frontend"
  style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=14;fontStyle=1;"
  vertex="1" parent="1">
  <mxGeometry x="100" y="200" width="160" height="60" as="geometry"/>
</mxCell>

<!-- API Gateway -->
<mxCell id="11" value="API Gateway"
  style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;fontSize=14;fontStyle=1;"
  vertex="1" parent="1">
  <mxGeometry x="360" y="200" width="160" height="60" as="geometry"/>
</mxCell>

<!-- Microservice -->
<mxCell id="12" value="Auth Service"
  style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;fontSize=13;"
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
```
