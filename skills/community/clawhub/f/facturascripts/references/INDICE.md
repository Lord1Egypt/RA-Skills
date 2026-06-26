# Indice Rápido - FacturaScripts 2025 Views & Widgets

## Acceso Rápido a Widgets por Tipo de Dato

### Texto
- **WidgetText** - Texto simple con límite de caracteres
- **WidgetTextarea** - Texto multilínea
- **WidgetPassword** - Contraseña con toggle show/hide
- **WidgetLink** - URLs con validación
- **WidgetJson** - Datos JSON estructurados

### Números
- **WidgetNumber** - Números con decimales configurables
- **WidgetMoney** - Dinero con símbolo de moneda automático
- **WidgetPercentage** - Porcentajes (0-100%)
- **WidgetBytes** - Tamaños de archivo formateados
- **WidgetSeconds** - Duraciones en formato HH:MM:SS

### Selecciones
- **WidgetSelect** - Selector desplegable estándar
- **WidgetAutocomplete** - Búsqueda mientras escribes (jQuery)
- **WidgetDatalist** - HTML5 datalist nativo
- **WidgetRadio** - Botones de radio con opciones visuales
- **WidgetCheckbox** - Checkbox booleano

### Fechas y Horas
- **WidgetDate** - Selector de fecha (HTML5)
- **WidgetDatetime** - Selector de fecha y hora
- **WidgetTime** - Selector de hora

### Archivos
- **WidgetFile** - Carga simple de archivos
- **WidgetLibrary** - Seleccionar o cargar desde biblioteca

### Especializados
- **WidgetColor** - Selector de color con jscolor
- **WidgetStars** - Calificación por estrellas (1-5)
- **WidgetVariante** - Variantes de productos
- **WidgetSubcuenta** - Subcuentas contables

---

## Archivos XMLView Más Usados

### Clientes y Proveedores
- ListCliente / EditCliente
- ListProveedor / EditProveedor
- ListContacto / EditContacto

### Productos
- ListProducto / EditProducto
- ListFamilia / EditFamilia
- ListVariante / EditVariante
- ListStock / EditStock

### Documentos Comerciales
- ListFacturaCliente / EditFacturaCliente
- ListFacturaProveedor / EditFacturaProveedor
- ListPresupuestoCliente / EditPresupuestoCliente
- ListPedidoCliente / EditPedidoCliente

### Contabilidad
- ListAsiento / EditAsiento
- ListCuenta / ListSubcuenta
- ListDiario / EditDiario
- ListEjercicio / EditEjercicio

### Configuración
- ListUsuario / EditUsuario
- ListRole / EditRole
- ListAlmacen / EditAlmacen
- EditEmpresa
- ConfigEmail

---

## Estructura Típica de un XMLView

```xml
<?xml version="1.0" encoding="UTF-8"?>
<view>
    <columns>
        <!-- Columnas simples (para List) -->
        <column name="code" order="100">
            <widget type="text" fieldname="codigo" onclick="EditMiModelo" />
        </column>
        
        <!-- Grupos (para Edit) -->
        <group name="basic" title="basic-data" numcolumns="12">
            <column name="name" numcolumns="6" order="100">
                <widget type="text" fieldname="nombre" required="true" />
            </column>
        </group>
    </columns>
    
    <rows>
        <!-- Colorear filas según condiciones -->
        <row type="status">
            <option color="danger" title="inactive" fieldname="estado">0</option>
            <option color="success" title="active" fieldname="estado">1</option>
        </row>
        
        <!-- Mostrar estadísticas en Edit -->
        <row type="statistics">
            <datalabel icon="fa-solid fa-file" label="total-docs" function="countDocs" />
        </row>
    </rows>
</view>
```

---

## Atributos Comunes

### En Widgets
- `fieldname` (requerido): Campo del modelo
- `required="true"`: Campo obligatorio
- `readonly="true"`: Solo lectura
- `readonly="dinamic"`: Readonly después de crear
- `icon="fa-solid fa-..."`: Ícono FontAwesome
- `onclick="EditOtro"`: Enlace al hacer clic
- `class="..."`: Clases CSS

### En Columns
- `name`: ID único (para traducción)
- `order`: Número (100, 110, 120...)
- `numcolumns`: 1-12 en Bootstrap (solo en grupos)
- `display="none"`: Ocultar por defecto
- `title`: Título personalizado
- `description`: Texto de ayuda

### En Rows
- `type="status"`: Colorear filas
- `type="statistics"`: Estadísticas
- Colores: danger, success, warning, info, dark, secondary, primary, light

---

## Directorio de Ubicaciones

- XMLViews: `/Core/XMLView/*.xml`
- Widgets: `/Core/Lib/Widget/Widget*.php`
- Plantillas: `/Core/View/Master/*.twig`
- Macros: `/Core/View/Macro/*.twig`
- Controladores: `/Controller/*.php`
- Modelos: `/Model/*.php`

---

## Las 26 Clases de Widget Principales

1. WidgetText
2. WidgetTextarea
3. WidgetNumber
4. WidgetMoney
5. WidgetPercentage
6. WidgetDate
7. WidgetDatetime
8. WidgetTime
9. WidgetCheckbox
10. WidgetSelect
11. WidgetAutocomplete
12. WidgetDatalist
13. WidgetRadio
14. WidgetPassword
15. WidgetFile
16. WidgetLibrary
17. WidgetLink
18. WidgetColor
19. WidgetJson
20. WidgetBytes
21. WidgetSeconds
22. WidgetStars
23. WidgetVariante
24. WidgetSubcuenta
25. WidgetCalc (cálculos automáticos)
26. Tipos HTML5 (email, tel, url, integer, hidden)

---

## Las 5 Clases Row Principales

1. RowStatus - Colores según condiciones
2. RowStatistics - Datos agregados
3. RowHeader - Encabezado especial
4. RowFooter - Pie especial
5. RowActions - Acciones disponibles

---

## Traducción de Etiquetas

Las etiquetas se traducen automáticamente según:

- `column-{name}` → Título de columna
- `group-{name}` → Título de grupo
- `{fieldname}-title` → Título personalizado
- `{fieldname}-description` → Descripción del campo
- Valores con `translate="true"` se traducen automáticamente

Ejemplo:
```xml
<column name="code" order="100">
    <!-- Se traduce "column-code" para el título -->
    <widget type="text" fieldname="codigo" />
</column>
```

---

## Fuentes de Datos para Select/Autocomplete

```xml
<!-- Desde tabla (CodeModel) -->
<values source="familias" fieldcode="codfamilia" fieldtitle="descripcion" />

<!-- Valores estáticos -->
<values title="active">1</values>
<values title="inactive">0</values>

<!-- Rango numérico -->
<values start="1" end="12" step="1" />
```

---

## Colores Bootstrap para Status Rows

| Color | Clase | Uso |
|-------|-------|-----|
| danger | table-danger | Rojo - Crítico, error, suspendido |
| success | table-success | Verde - Activo, completado, aprobado |
| warning | table-warning | Naranja - Pendiente, atención, bajo stock |
| info | table-info | Azul claro - Información adicional |
| dark | table-dark | Gris oscuro - Archivado, inactivo |
| secondary | table-secondary | Gris - Secundario |
| primary | table-primary | Azul - Principal |
| light | table-light | Blanco - Muy claro |

---

## Métodos Útiles en Controladores

```php
// Crear vista de listado
$this->createViewList('ListMiModelo', 'MiModelo', 'list', 'my-title');

// Crear vista de edición
$this->createViewEdit('EditMiModelo', 'MiModelo', 'edit', 'my-title');

// Agregar ordenamiento
$this->addOrderBy('ListMiModelo', 'nombre', 'name');

// Agregar filtro
$this->addFilterSelectWhere('ListMiModelo', 'estado', 'estado', [1 => 'Activo', 0 => 'Inactivo']);

// Obtener el modelo
$model = $this->getModel();

// Obtener la vista actual
$view = $this->views[$this->active];
```

---

## Documentación Completa

Para documentación exhaustiva, ver: `views-widgets.md`

Este documento contiene:
- 2,787 líneas de referencia detallada
- 26 widgets documentados completamente
- 133 XMLViews listados y categorizados
- Ejemplos de código completos
- Patrones y buenas prácticas
- Casos de uso comunes

---

**Generado:** 12 de abril de 2026  
**Versión:** FacturaScripts 2025.001  
**Idioma:** Español
