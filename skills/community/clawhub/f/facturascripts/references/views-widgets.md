# FacturaScripts 2025 - Sistema de Vistas, XMLViews y Widgets - Referencia Exhaustiva

**Versión:** 2025.001  
**Fecha:** Abril 2026  
**Idioma:** Español

## Tabla de Contenidos

1. [Sistema de Vistas XML](#sistema-de-vistas-xml)
2. [Catálogo Completo de Widgets](#catálogo-completo-de-widgets)
3. [Plantillas Twig](#plantillas-twig)
4. [Lista Completa de XMLViews del Core](#lista-completa-de-xmlviews-del-core)
5. [Como Crear Vistas Personalizadas](#como-crear-vistas-personalizadas)

---

## 1. Sistema de Vistas XML

### 1.1 Introducción al Sistema de Vistas

FacturaScripts utiliza archivos XML para definir la estructura de vistas en la interfaz de usuario. Estos archivos XML (conocidos como XMLViews) describen cómo se visualizan y editan los datos de los modelos. El sistema es muy flexible y permite crear:

- **Listados (List views)**: Muestran múltiples registros en forma de tabla
- **Formularios de edición (Edit views)**: Permiten editar un registro individual
- **Vistas especiales**: Configuraciones, estadísticas, etc.

### 1.2 Estructura de un Archivo XMLView

Un archivo XMLView tiene la siguiente estructura raíz:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<view>
    <columns>
        <!-- Definición de columnas -->
    </columns>
    <rows>
        <!-- Definición de filas especiales (estado, estadísticas, etc.) -->
    </rows>
</view>
```

**Componentes principales:**
- `<view>`: Elemento raíz
- `<columns>`: Contenedor de definición de columnas
- `<rows>`: Contenedor de filas especiales (opcional)

### 1.3 Elementos del Sistema: Columns, Rows, Modals

#### 1.3.1 Elemento Columns

El elemento `<columns>` contiene:
- `<column>`: Columnas individuales
- `<group>`: Grupos de columnas (solo en Edit views)
- `<modal>`: Diálogos modales (opcional)

```xml
<columns>
    <column name="code" order="100">
        <widget type="text" fieldname="codproducto" />
    </column>
    
    <group name="datos" title="data-group" numcolumns="12">
        <column name="name" numcolumns="6" order="100">
            <widget type="text" fieldname="nombre" required="true" />
        </column>
    </group>
    
    <modal name="modal_name">
        <!-- Contenido del modal -->
    </modal>
</columns>
```

**Atributos de `<column>`:**
- `name` (requerido): Identificador único de la columna, usado para traducción (ej: "name" busca "column-name")
- `order` (opcional): Número para ordenar columnas (defecto: 100)
- `display` (opcional): "none" para ocultar por defecto, "center" para centrar
- `description` (opcional): Clave de traducción para descripción debajo del widget
- `titleurl` (opcional): URL a la que ir al hacer clic en el título
- `title` (opcional): Título personalizado (si no se proporciona, se traduce "column-{name}")
- `numcolumns` (opcional): Número de columnas Bootstrap (1-12, solo en grupos)

#### 1.3.2 Elemento Group

El elemento `<group>` organiza columnas en formularios de edición:

```xml
<group name="data" title="personal-data" numcolumns="12">
    <column name="name" numcolumns="6" order="100">
        <widget type="text" fieldname="nombre" required="true" />
    </column>
    <column name="email" numcolumns="6" order="110">
        <widget type="email" fieldname="email" />
    </column>
</group>
```

**Atributos de `<group>`:**
- `name` (requerido): Identificador del grupo
- `title` (opcional): Clave de traducción para el título del grupo
- `numcolumns` (requerido): Ancho total del grupo (siempre 12 para Bootstrap)
- `display` (opcional): "none" para ocultar el grupo

#### 1.3.3 Elemento Rows

El elemento `<rows>` define filas especiales que aparecen en listados o formularios:

```xml
<rows>
    <row type="status">
        <option color="success" title="active" fieldname="activo">1</option>
        <option color="danger" title="suspended" fieldname="debaja">1</option>
    </row>
    
    <row type="statistics">
        <datalabel icon="fa-solid fa-copy" label="documents" function="countDocuments" />
        <datalabel icon="fa-solid fa-euro-sign" label="total-amount" function="getTotalAmount" />
    </row>
</rows>
```

**Tipos de filas (`type`):**

**a) status**: Colorea filas según condiciones
```xml
<row type="status">
    <option color="danger" title="estado-cancelado" fieldname="estado">Cancelado</option>
    <option color="warning" title="estado-pendiente" fieldname="estado">Pendiente</option>
    <option color="success" title="estado-completado" fieldname="estado">Completado</option>
</row>
```

**b) statistics**: Muestra estadísticas en formularios de edición
```xml
<row type="statistics">
    <datalabel icon="fa-solid fa-money-bill" label="total-invoices" function="getTotalFacturas" color="success" />
    <datalabel icon="fa-solid fa-file" label="pending" function="getPendingDocuments" color="warning" />
</row>
```

**c) header**: Encabezado especial (poco usado)

**d) footer**: Pie especial (poco usado)

**Atributos de `<option>` en status:**
- `color`: Color de Bootstrap (success, danger, warning, info, light, dark, primary, secondary)
- `title`: Clave de traducción del texto mostrado
- `fieldname`: Campo a verificar (si no se especifica, usa el del row)
- Valor de texto: Valor del campo que activa esta opción
- `operator` (opcional): Operador de comparación (=, !=, <, >, <=, >=)

**Atributos de `<datalabel>` en statistics:**
- `icon`: Clase de FontAwesome
- `label`: Clave de traducción
- `function`: Nombre del método en el controlador a ejecutar
- `color` (opcional): Clase de botón (btn-success, btn-danger, etc.)
- `link` (opcional): URL destino al hacer clic
- `id` (opcional): ID del elemento HTML
- `class` (opcional): Clases CSS adicionales

#### 1.3.4 Elemento Modal

Los modales son diálogos que pueden ser invocados desde otros widgets:

```xml
<modal name="modal_example" title="my-modal">
    <column name="col1" order="100">
        <widget type="text" fieldname="field1" />
    </column>
</modal>
```

No se utilizan frecuentemente en XMLViews directas, pero pueden ser referenciados por JavaScript.

### 1.4 Grupos de Columnas (Group)

Los grupos permiten organizar campos en formularios:

```xml
<view>
    <columns>
        <!-- Datos principales -->
        <group name="basic" title="basic-data" numcolumns="12">
            <column name="code" numcolumns="2" order="100">
                <widget type="text" fieldname="codigo" readonly="dinamic" />
            </column>
            <column name="name" numcolumns="4" order="110">
                <widget type="text" fieldname="nombre" required="true" maxlength="100" />
            </column>
            <column name="status" numcolumns="2" order="120">
                <widget type="select" fieldname="estado" translate="true">
                    <values title="active">1</values>
                    <values title="inactive">0</values>
                </widget>
            </column>
        </group>
        
        <!-- Datos de contacto -->
        <group name="contact" title="contact-info" numcolumns="12">
            <column name="email" numcolumns="6" order="100">
                <widget type="email" fieldname="email" />
            </column>
            <column name="phone" numcolumns="6" order="110">
                <widget type="tel" fieldname="telefono" />
            </column>
        </group>
    </columns>
</view>
```

**Características de los grupos:**
- `numcolumns="12"`: Siempre 12 (ancho completo)
- Las columnas dentro pueden ser 1-12
- Se renderizan como secciones colapsables en formularios
- El título se traduce automáticamente

### 1.5 Tipos de Columnas y Sus Atributos

Las columnas contienen widgets y pueden tener los siguientes atributos:

```xml
<column 
    name="identificador"                          <!-- Clave única, para traducción -->
    order="100"                                   <!-- Orden de visualización -->
    numcolumns="6"                                <!-- Ancho (solo en grupos) -->
    display="none"                                <!-- Ocultar por defecto -->
    title="custom-title"                          <!-- Título personalizado -->
    description="help-text"                       <!-- Descripción/ayuda -->
    titleurl="EditSettings?tab=email"             <!-- URL del título -->
    class="extra-class">                          <!-- Clases CSS adicionales -->
    <widget ... />
</column>
```

**Atributos de columna:**
- `name`: Identificador (se traduce como "column-{name}")
- `order`: Posición (números: 100, 110, 120, etc.)
- `numcolumns`: Ancho en Bootstrap (1-12, solo en Edit views con grupos)
- `display`: "none" para ocultar
- `title`: Título custom (si no, se traduce automáticamente)
- `description`: Texto de ayuda debajo del widget
- `titleurl`: Enlace al hacer clic en el título
- `class`: Clases CSS para la celda/contenedor

### 1.6 Filas Especiales: Status, Statistics, Header, Footer

#### 1.6.1 Row Type: Status

Colorea filas de un listado según condiciones de campos:

```xml
<row type="status">
    <!-- Si debaja = 1, la fila será roja -->
    <option color="danger" title="suspended" fieldname="debaja">1</option>
    
    <!-- Si estado = "Completado", la fila será verde -->
    <option color="success" title="completed" fieldname="estado">Completado</option>
    
    <!-- Si cantidad < 10, mostrar advertencia -->
    <option color="warning" title="low-stock" fieldname="cantidad" operator="<">10</option>
    
    <!-- Info si es creditor -->
    <option color="info" title="is-creditor" fieldname="acreedor">1</option>
</row>
```

**Colores disponibles:**
- `danger`: Rojo (Bootstrap table-danger)
- `success`: Verde (Bootstrap table-success)
- `warning`: Naranja (Bootstrap table-warning)
- `info`: Azul claro (Bootstrap table-info)
- `light`: Gris claro (Bootstrap table-light)
- `dark`: Gris oscuro (Bootstrap table-dark)
- `primary`: Azul (Bootstrap table-primary)
- `secondary`: Gris (Bootstrap table-secondary)

**Operadores en status:**
- Sin operador: Igualdad (=)
- `operator="!="`: No igual
- `operator="<"`: Menor que
- `operator=">"`: Mayor que
- `operator="<="`: Menor o igual
- `operator=">="`: Mayor o igual

**Interpolación de campos en texto:**
```xml
<option color="info" text="Cliente: field:nombre, saldo: field:saldo" fieldname="estado">Activo</option>
```
Los valores `field:nombreCampo` se reemplazan por el valor del campo en el modelo.

#### 1.6.2 Row Type: Statistics

Muestra datos agregados en la parte superior de un formulario de edición:

```xml
<row type="statistics">
    <datalabel 
        icon="fa-solid fa-file-invoice" 
        label="total-invoices" 
        function="getTotalInvoices"
        color="success"
        link="ListFacturaCliente?search=codcliente|{value}"
        id="stat-invoices"
        class="custom-stat" />
    
    <datalabel 
        icon="fa-solid fa-money-bill-alt" 
        label="pending-amount" 
        function="getPendingAmount"
        color="warning" />
</row>
```

**La función se ejecuta en el controlador:**
```php
// En el controlador (ej: EditCliente)
public function getTotalInvoices(): string
{
    $model = $this->getModel();
    $count = // contar facturas...
    return (string)$count;
}
```

#### 1.6.3 Row Type: Header

Encabezado especial (rara vez utilizado):

```xml
<row type="header">
    <datalabel label="titulo-especial" function="getHeaderInfo" />
</row>
```

#### 1.6.4 Row Type: Footer

Pie especial (rara vez utilizado):

```xml
<row type="footer">
    <datalabel label="pie-especial" function="getFooterInfo" />
</row>
```

### 1.7 Modales

Los modales son diálogos que se pueden abrir desde widgets:

```xml
<columns>
    <modal name="modal_info" title="additional-information">
        <column name="notes" order="100">
            <widget type="textarea" fieldname="notas" rows="5" />
        </column>
    </modal>
    
    <!-- En otro lado, un botón que abre el modal -->
    <column name="open_modal" order="200">
        <widget type="button" label="open-info" modal="modal_info" />
    </column>
</columns>
```

Los modales se renderizan como diálogos Bootstrap y pueden ser disparados por JavaScript.

### 1.8 Ejemplo Completo de ListXxx.xml (Listado)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<view>
    <columns>
        <!-- Columna de código con enlace a edición -->
        <column name="code" order="100">
            <widget type="text" fieldname="codigo" onclick="EditProducto" />
        </column>
        
        <!-- Columna de nombre -->
        <column name="name" order="110">
            <widget type="text" fieldname="nombre" />
        </column>
        
        <!-- Columna de cantidad con totales -->
        <column name="stock" order="120">
            <widget type="number" fieldname="cantidad" totals="true" decimal="2" />
        </column>
        
        <!-- Columna de precio con formato moneda -->
        <column name="price" order="130">
            <widget type="money" fieldname="precio" />
        </column>
        
        <!-- Columna de familia (select) -->
        <column name="family" order="140">
            <widget type="select" fieldname="codfamilia" onclick="EditFamilia">
                <values source="familias" fieldcode="codfamilia" fieldtitle="descripcion" />
            </widget>
        </column>
        
        <!-- Columna oculta por defecto -->
        <column name="description" display="none" order="150">
            <widget type="textarea" fieldname="descripcion" />
        </column>
    </columns>
    
    <rows>
        <!-- Filas de estado: colorea según condiciones -->
        <row type="status">
            <!-- Rojo si está desactivado -->
            <option color="danger" title="disabled" fieldname="desactivado">1</option>
            
            <!-- Naranja si stock bajo -->
            <option color="warning" title="low-stock" fieldname="cantidad" operator="<">10</option>
            
            <!-- Verde si activo y stock suficiente -->
            <option color="success" title="active" fieldname="activo">1</option>
        </row>
    </rows>
</view>
```

### 1.9 Ejemplo Completo de EditXxx.xml (Formulario)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<view>
    <columns>
        <!-- Grupo de datos básicos -->
        <group name="basic" title="basic-data" numcolumns="12">
            <column name="code" numcolumns="2" order="100">
                <widget type="text" fieldname="codigo" icon="fa-solid fa-hashtag" 
                        maxlength="10" readonly="dinamic" />
            </column>
            <column name="name" numcolumns="6" order="110">
                <widget type="text" fieldname="nombre" maxlength="100" required="true" />
            </column>
            <column name="reference" numcolumns="4" order="120">
                <widget type="text" fieldname="referencia" maxlength="30" />
            </column>
        </group>
        
        <!-- Grupo de clasificación -->
        <group name="classification" title="classification" numcolumns="12">
            <column name="family" numcolumns="3" order="100">
                <widget type="select" fieldname="codfamilia" onclick="EditFamilia" required="true">
                    <values source="familias" fieldcode="codfamilia" fieldtitle="descripcion" />
                </widget>
            </column>
            <column name="manufacturer" numcolumns="3" order="110">
                <widget type="select" fieldname="codfabricante" onclick="EditFabricante">
                    <values source="fabricantes" fieldcode="codfabricante" fieldtitle="nombre" />
                </widget>
            </column>
            <column name="type" numcolumns="3" order="120">
                <widget type="select" fieldname="tipo" translate="true">
                    <values title="standard">STD</values>
                    <values title="service">SRV</values>
                </widget>
            </column>
            <column name="state" numcolumns="3" order="130">
                <widget type="select" fieldname="activo" translate="true">
                    <values title="active">1</values>
                    <values title="inactive">0</values>
                </widget>
            </column>
        </group>
        
        <!-- Grupo de precios -->
        <group name="prices" title="prices" numcolumns="12">
            <column name="cost-price" numcolumns="4" order="100">
                <widget type="money" fieldname="costeprecio" decimal="6" />
            </column>
            <column name="sell-price" numcolumns="4" order="110">
                <widget type="money" fieldname="precioventa" decimal="6" required="true" />
            </column>
            <column name="discount" numcolumns="4" order="120">
                <widget type="percentage" fieldname="descuento" decimal="2" />
            </column>
        </group>
        
        <!-- Grupo de descripción -->
        <group name="description" numcolumns="12">
            <column name="description" order="100">
                <widget type="textarea" fieldname="descripcion" rows="5" />
            </column>
        </group>
    </columns>
    
    <rows>
        <!-- Estadísticas: información agregada -->
        <row type="statistics">
            <datalabel icon="fa-solid fa-boxes" label="total-stock" 
                      function="getTotalStock" color="info" />
            <datalabel icon="fa-solid fa-money-bill" label="total-cost" 
                      function="getTotalCost" color="warning" />
            <datalabel icon="fa-solid fa-file-invoice" label="total-sales" 
                      function="getTotalSales" color="success" />
        </row>
    </rows>
</view>
```

---

## 2. Catálogo Completo de Widgets

### 2.1 Estructura de Documentación de Widgets

Cada widget está documentado con:
- **Clase PHP**: Nombre de la clase en `Core/Lib/Widget/`
- **Tipo XML**: Valor del atributo `type` en XMLView
- **Propiedades configurables**: Atributos XML soportados
- **Comportamiento de renderizado**: Cómo se muestra en edit y list views
- **Ejemplo de uso**: Fragmento de XML
- **Casos de uso**: Cuándo utilizarlo

### 2.2 WidgetText - Texto Simple

**Clase:** `WidgetText.php`  
**Tipo XML:** `type="text"`

**Propiedades configurables:**
- `fieldname` (requerido): Nombre del campo en el modelo
- `maxlength` (opcional): Longitud máxima de caracteres (defecto: 0, ilimitado)
- `required` (opcional): "true" para campo obligatorio
- `readonly` (opcional): "true" o "dinamic" (dinamic = readonly si tiene valor)
- `icon` (opcional): Clase de FontAwesome para ícono
- `onclick` (opcional): Página de destino al hacer clic (ej: "EditProveedor")
- `tabindex` (opcional): Índice de tabulación
- `autocomplete` (opcional): "on" u "off"
- `class` (opcional): Clases CSS adicionales
- `placeholder` (opcional): Texto de marcador de posición

**Renderizado:**
- **Edit view**: Input text HTML5
- **List view**: Texto plano, con opción de enlace si `onclick` está presente

**Ejemplo:**
```xml
<column name="name" order="100">
    <widget type="text" fieldname="nombre" maxlength="100" required="true" 
            icon="fa-solid fa-user" placeholder="Ingrese el nombre" />
</column>
```

**Casos de uso:**
- Nombres, direcciones, descripciones cortas
- Códigos, referencias, identificadores
- Cualquier campo de texto simple

---

### 2.3 WidgetTextarea - Texto Multilínea

**Clase:** `WidgetTextarea.php`  
**Tipo XML:** `type="textarea"`

**Propiedades configurables:**
- `fieldname` (requerido): Nombre del campo
- `maxlength` (opcional): Longitud máxima
- `required` (opcional): "true"
- `readonly` (opcional): "true" o "dinamic"
- `rows` (opcional): Número de filas (defecto: 3)
- `icon` (opcional): Clase FontAwesome
- `class` (opcional): Clases CSS

**Renderizado:**
- **Edit view**: Textarea HTML con número de filas configurable
- **List view**: Texto truncado a 60 caracteres con "..."

**Ejemplo:**
```xml
<column name="observations" order="100">
    <widget type="textarea" fieldname="observaciones" rows="5" 
            icon="fa-solid fa-sticky-note" />
</column>
```

**Casos de uso:**
- Notas, comentarios, descripciones largas
- Observaciones, instrucciones especiales

---

### 2.4 WidgetNumber - Números

**Clase:** `WidgetNumber.php`  
**Tipo XML:** `type="number"`

**Propiedades configurables:**
- `fieldname` (requerido): Nombre del campo
- `decimal` (opcional): Número de decimales (defecto: FS_NF0)
- `min` (opcional): Valor mínimo
- `max` (opcional): Valor máximo
- `step` (opcional): Incremento (defecto: "any")
- `totals` (opcional): "true" para mostrar suma en columnas de listado
- `required` (opcional): "true"
- `readonly` (opcional): "true" o "dinamic"
- `icon` (opcional): Clase FontAwesome
- `class` (opcional): Clases CSS

**Renderizado:**
- **Edit view**: Input type="number" con atributos numéricos
- **List view**: Número formateado, con suma si `totals="true"`

**Ejemplo:**
```xml
<column name="quantity" order="100">
    <widget type="number" fieldname="cantidad" decimal="2" min="0" step="0.01" 
            totals="true" icon="fa-solid fa-cubes" />
</column>
```

**Casos de uso:**
- Cantidades, stocks, valores numéricos
- Cualquier campo que deba ser un número

---

### 2.5 WidgetMoney - Dinero/Moneda

**Clase:** `WidgetMoney.php`  
**Tipo XML:** `type="money"`

**Propiedades configurables:**
- `fieldname` (requerido): Nombre del campo
- `decimal` (opcional): Decimales (defecto: FS_NF0)
- `min` (opcional): Valor mínimo
- `max` (opcional): Valor máximo
- `step` (opcional): Incremento
- `totals` (opcional): "true" para mostrar suma
- `required` (opcional): "true"
- `readonly` (opcional): "true" o "dinamic"
- `class` (opcional): Clases CSS

**Renderizado:**
- **Edit view**: Input number con símbolo de moneda como ícono
- **List view**: Formato moneda (ej: "1.234,56 EUR")
- **Símbolo de moneda automático**: EUR (€), USD ($), etc.

**Ejemplo:**
```xml
<column name="total" order="100">
    <widget type="money" fieldname="total" decimal="2" totals="true" />
</column>
```

**Casos de uso:**
- Precios, montos, importes
- Totales en listados

---

### 2.6 WidgetPercentage - Porcentaje

**Clase:** `WidgetPercentage.php`  
**Tipo XML:** `type="percentage"`

**Propiedades configurables:**
- `fieldname` (requerido): Nombre del campo
- `decimal` (opcional): Decimales
- `min` (opcional): Valor mínimo (defecto: 0)
- `max` (opcional): Valor máximo (defecto: 100)
- `step` (opcional): Incremento
- `icon` (opcional): Clase FontAwesome (defecto: fa-solid fa-percentage)
- `required` (opcional): "true"
- `readonly` (opcional): "true" o "dinamic"

**Renderizado:**
- **Edit view**: Input number, muestra símbolo % al lado
- **List view**: Número seguido de %

**Ejemplo:**
```xml
<column name="discount" order="100">
    <widget type="percentage" fieldname="descuento" decimal="2" min="0" max="100" />
</column>
```

**Casos de uso:**
- Descuentos, márgenes, comisiones
- Porcentajes en general

---

### 2.7 WidgetDate - Fecha

**Clase:** `WidgetDate.php`  
**Tipo XML:** `type="date"`

**Propiedades configurables:**
- `fieldname` (requerido): Nombre del campo
- `required` (opcional): "true"
- `readonly` (opcional): "true" o "dinamic"
- `icon` (opcional): Clase FontAwesome
- `class` (opcional): Clases CSS

**Renderizado:**
- **Edit view**: Input type="date" (nativo del navegador)
- **List view**: Formato "dd-mm-yyyy", negrilla si es hoy o futuro

**Ejemplo:**
```xml
<column name="birthday" order="100">
    <widget type="date" fieldname="fechanacimiento" icon="fa-solid fa-birthday-cake" />
</column>
```

**Casos de uso:**
- Fechas de nacimiento, creación, vencimiento
- Cualquier fecha del modelo

---

### 2.8 WidgetDatetime - Fecha y Hora

**Clase:** `WidgetDatetime.php`  
**Tipo XML:** `type="datetime"`

**Propiedades configurables:**
- `fieldname` (requerido): Nombre del campo
- `required` (opcional): "true"
- `readonly` (opcional): "true" o "dinamic"
- `icon` (opcional): Clase FontAwesome
- `class` (opcional): Clases CSS

**Renderizado:**
- **Edit view**: Input type="datetime-local"
- **List view**: Formato "dd-mm-yyyy hh:mm:ss", negrilla si futuro

**Ejemplo:**
```xml
<column name="created-at" order="100">
    <widget type="datetime" fieldname="fechacreacion" readonly="true" 
            icon="fa-solid fa-clock" />
</column>
```

**Casos de uso:**
- Timestamps, fechas de creación/modificación
- Registros con hora precisa

---

### 2.9 WidgetTime - Hora

**Clase:** `WidgetTime.php`  
**Tipo XML:** `type="time"`

**Propiedades configurables:**
- `fieldname` (requerido): Nombre del campo
- `min` (opcional): Hora mínima (formato "HH:MM")
- `max` (opcional): Hora máxima
- `step` (opcional): Incremento en segundos (si >= 60, no muestra segundos)
- `required` (opcional): "true"
- `readonly` (opcional): "true" o "dinamic"
- `icon` (opcional): Clase FontAwesome
- `class` (opcional): Clases CSS

**Renderizado:**
- **Edit view**: Input type="time" (nativo)
- **List view**: Texto HH:MM o HH:MM:SS

**Ejemplo:**
```xml
<column name="opening-time" order="100">
    <widget type="time" fieldname="horaapertura" min="08:00" max="22:00" 
            step="1800" icon="fa-solid fa-door-open" />
</column>
```

**Casos de uso:**
- Horarios de apertura/cierre
- Horas de trabajo, alarmas

---

### 2.10 WidgetCheckbox - Casilla de Verificación

**Clase:** `WidgetCheckbox.php`  
**Tipo XML:** `type="checkbox"`

**Propiedades configurables:**
- `fieldname` (requerido): Nombre del campo
- `required` (opcional): "true"
- `readonly` (opcional): "true" o "dinamic"
- `icon` (opcional): Clase FontAwesome (no se usa típicamente)
- `class` (opcional): Clases CSS

**Renderizado:**
- **Edit view**: Checkbox HTML5 con etiqueta
- **List view**: Ícono de check (✓) si true, guión (-) si false
- **Valor en modelo**: true/false, se convierte automáticamente

**Ejemplo:**
```xml
<column name="active" order="100">
    <widget type="checkbox" fieldname="activo" />
</column>
```

**Casos de uso:**
- Campos booleanos (activo/inactivo, sí/no)
- Flags, banderas, opciones binarias

---

### 2.11 WidgetSelect - Selector Desplegable

**Clase:** `WidgetSelect.php`  
**Tipo XML:** `type="select"`

**Propiedades configurables:**
- `fieldname` (requerido): Nombre del campo
- `multiple` (opcional): "true" para múltiples selecciones
- `translate` (opcional): "true" para traducir valores
- `parent` (opcional): Campo padre para dependencias
- `required` (opcional): "true"
- `readonly` (opcional): "true" o "dinamic"
- `icon` (opcional): Clase FontAwesome
- `class` (opcional): Clases CSS
- `<values>` (hijo): Define opciones

**Elemento `<values>` - Tres formas:**

**a) Valores estáticos:**
```xml
<widget type="select" fieldname="estado">
    <values title="active">1</values>
    <values title="inactive">0</values>
</widget>
```

**b) Valores desde fuente de datos:**
```xml
<widget type="select" fieldname="codfamilia" onclick="EditFamilia">
    <values source="familias" fieldcode="codfamilia" fieldtitle="descripcion" />
</widget>
```

**c) Valores desde rango:**
```xml
<widget type="select" fieldname="mes">
    <values start="1" end="12" step="1" />
</widget>
```

**Renderizado:**
- **Edit view**: Select HTML5 estándar
- **List view**: Texto del valor seleccionado

**Ejemplo completo:**
```xml
<column name="family" order="100">
    <widget type="select" fieldname="codfamilia" onclick="EditFamilia" 
            icon="fa-solid fa-sitemap">
        <values source="familias" fieldcode="codfamilia" fieldtitle="descripcion" />
    </widget>
</column>
```

**Atributos de `<values>`:**
- `title`: Clave de traducción del texto (para valores estáticos)
- `source`: Nombre de la fuente de datos (tabla, generalmente el plural del modelo)
- `fieldcode`: Campo que se guarda (código/ID)
- `fieldtitle`: Campo que se muestra (descripción/nombre)
- `fieldfilter` (opcional): Campo para filtrar
- `start`, `end`, `step`: Para rangos numéricos
- `translate` (heredado de widget): Si es "true", traduce los valores

**Casos de uso:**
- Seleccionar de una lista de opciones
- Relaciones con otros modelos
- Enumeraciones

---

### 2.12 WidgetAutocomplete - Autocompletado

**Clase:** `WidgetAutocomplete.php`  
**Tipo XML:** `type="autocomplete"`

**Propiedades configurables:**
- `fieldname` (requerido): Nombre del campo
- `strict` (opcional): "true" (defecto) o "false" para permitir valores libres
- `translate` (opcional): "true"
- `parent` (opcional): Campo padre
- `required` (opcional): "true"
- `readonly` (opcional): "true" o "dinamic"
- `icon` (opcional): Clase FontAwesome
- `class` (opcional): Clases CSS
- `<values>` (hijo): Define opciones

**Diferencia con Select:**
- Permite buscar/filtrar mientras escribes
- Si `strict="false"`, permite valores que no están en la lista
- Mejor UX para listas grandes

**Renderizado:**
- **Edit view**: Input text con sugeriencias en tiempo real (jQuery UI Autocomplete)
- **List view**: Texto del valor

**Ejemplo:**
```xml
<column name="provider" order="100">
    <widget type="autocomplete" fieldname="codproveedor" strict="true" 
            onclick="EditProveedor" icon="fa-solid fa-building">
        <values source="proveedores" fieldcode="codproveedor" fieldtitle="nombre" />
    </widget>
</column>
```

**Casos de uso:**
- Selecciones de listas grandes (clientes, proveedores)
- Búsqueda rápida mientras escribes

---

### 2.13 WidgetDatalist - Lista de Datos

**Clase:** `WidgetDatalist.php`  
**Tipo XML:** `type="datalist"`

**Propiedades configurables:**
- `fieldname` (requerido): Nombre del campo
- `translate` (opcional): "true"
- `parent` (opcional): Campo padre para dependencias
- `required` (opcional): "true"
- `readonly` (opcional): "true" o "dinamic"
- `icon` (opcional): Clase FontAwesome
- `class` (opcional): Clases CSS
- `<values>` (hijo): Define opciones

**Renderizado:**
- **Edit view**: Input text HTML5 con elemento `<datalist>` nativo
- **List view**: Texto del valor

**Diferencia con Autocomplete:**
- Usa datalist HTML5 nativo (más ligero)
- Menos personalizable que Autocomplete
- Mejor rendimiento con listas muy grandes

**Ejemplo:**
```xml
<column name="country" order="100">
    <widget type="datalist" fieldname="codpais" icon="fa-solid fa-globe">
        <values source="paises" fieldcode="codpais" fieldtitle="nombre" />
    </widget>
</column>
```

**Casos de uso:**
- Alternativa ligera a Autocomplete
- Listas de referencia estables

---

### 2.14 WidgetRadio - Botones de Radio

**Clase:** `WidgetRadio.php`  
**Tipo XML:** `type="radio"`

**Propiedades configurables:**
- `fieldname` (requerido): Nombre del campo
- `translate` (opcional): "true" para traducir valores
- `images` (opcional): "true" para mostrar imágenes
- `path` (opcional): Ruta a las imágenes si `images="true"`
- `required` (opcional): "true"
- `readonly` (opcional): "true" o "dinamic"
- `class` (opcional): Clases CSS
- `<values>` (hijo): Define opciones

**Renderizado:**
- **Edit view**: Botones de radio HTML5, opcionalmente con imágenes
- **List view**: Texto del valor seleccionado

**Ejemplo sin imágenes:**
```xml
<column name="status" order="100">
    <widget type="radio" fieldname="estado" translate="true">
        <values title="active">1</values>
        <values title="inactive">0</values>
        <values title="pending">2</values>
    </widget>
</column>
```

**Ejemplo con imágenes:**
```xml
<column name="color" order="100">
    <widget type="radio" fieldname="color" images="true" path="/Colors/">
        <values title="red">rojo</values>
        <values title="blue">azul</values>
        <values title="green">verde</values>
    </widget>
</column>
```

**Casos de uso:**
- Opciones visibles y seleccionables
- Estados con pocas opciones
- Selecciones visuales (colores, imágenes)

---

### 2.15 WidgetPassword - Contraseña

**Clase:** `WidgetPassword.php`  
**Tipo XML:** `type="password"`

**Propiedades configurables:**
- `fieldname` (requerido): Nombre del campo
- `maxlength` (opcional): Longitud máxima
- `required` (opcional): "true"
- `readonly` (opcional): "true" o "dinamic"
- `icon` (opcional): Clase FontAwesome (defecto: eye icon)
- `class` (opcional): Clases CSS

**Renderizado:**
- **Edit view**: Input text con ícono de ojo para mostrar/ocultar
- **List view**: Nunca muestra el valor, solo guión (-)
- **JavaScript dinámico**: Cambia entre type="password" y type="text"

**Ejemplo:**
```xml
<column name="password" order="100">
    <widget type="password" fieldname="password" required="true" 
            maxlength="64" icon="fa-solid fa-key" />
</column>
```

**Casos de uso:**
- Campos de contraseña y tokens
- Datos sensibles que deben ocultarse

---

### 2.16 WidgetFile - Carga de Archivos

**Clase:** `WidgetFile.php`  
**Tipo XML:** `type="file"`

**Propiedades configurables:**
- `fieldname` (requerido): Nombre del campo
- `accept` (opcional): Tipos MIME aceptados (ej: "image/*,.pdf")
- `multiple` (opcional): "true" para múltiples archivos
- `required` (opcional): "true"
- `readonly` (opcional): "true" o "dinamic"
- `icon` (opcional): Clase FontAwesome
- `class` (opcional): Clases CSS

**Renderizado:**
- **Edit view**: Input type="file" con restricción de tipos
- **List view**: Nombre del archivo con enlace de descarga

**Ejemplo:**
```xml
<column name="invoice-pdf" order="100">
    <widget type="file" fieldname="archivopdf" accept=".pdf" 
            icon="fa-solid fa-file-pdf" />
</column>
```

**Casos de uso:**
- Cargar documentos, imágenes, PDFs
- Adjuntos en modelos

---

### 2.17 WidgetLibrary - Biblioteca de Archivos

**Clase:** `WidgetLibrary.php`  
**Tipo XML:** `type="library"`

**Propiedades configurables:**
- `fieldname` (requerido): Nombre del campo
- `accept` (opcional): Tipos MIME aceptados
- `required` (opcional): "true"
- `readonly` (opcional): "true" o "dinamic"
- `icon` (opcional): Clase FontAwesome

**Renderizado:**
- **Edit view**: Botón que abre modal con biblioteca de archivos
- Modal contiene: búsqueda, filtros de fecha, carga de nuevos archivos
- **List view**: Nombre del archivo con enlace

**Ejemplo:**
```xml
<column name="document" order="100">
    <widget type="library" fieldname="iddocumento" accept=".pdf,.docx" 
            icon="fa-solid fa-file" />
</column>
```

**Casos de uso:**
- Seleccionar de una biblioteca existente o cargar nuevo
- Documentos reutilizables

---

### 2.18 WidgetLink - Enlace/URL

**Clase:** `WidgetLink.php`  
**Tipo XML:** `type="link"`

**Propiedades configurables:**
- `fieldname` (requerido): Nombre del campo
- `maxlength` (opcional): Longitud máxima
- `required` (opcional): "true"
- `readonly` (opcional): "true" o "dinamic"
- `icon` (opcional): Clase FontAwesome (defecto: fa-solid fa-link)
- `class` (opcional): Clases CSS

**Renderizado:**
- **Edit view**: Input text para URL
- **List view**: Enlace clickeable (target="_blank") si es URL válida
- **Validación**: Verifica que sea URL válida antes de renderizar como enlace

**Ejemplo:**
```xml
<column name="website" order="100">
    <widget type="link" fieldname="web" maxlength="255" 
            icon="fa-solid fa-globe" />
</column>
```

**Casos de uso:**
- URLs, sitios web, enlaces HTTP
- Campos de dirección web

---

### 2.19 WidgetColor - Selector de Color

**Clase:** `WidgetColor.php`  
**Tipo XML:** `type="color"`

**Propiedades configurables:**
- `fieldname` (requerido): Nombre del campo
- `required` (opcional): "true"
- `readonly` (opcional): "true" o "dinamic"
- `icon` (opcional): Clase FontAwesome
- `class` (opcional): Clases CSS

**Renderizado:**
- **Edit view**: Input type="color" (nativo) con librería jscolor avanzada
- **List view**: Cuadrado de color con código hexadecimal
- **Biblioteca externa**: Usa @eastdesire/jscolor

**Ejemplo:**
```xml
<column name="brand-color" order="100">
    <widget type="color" fieldname="colorprincipal" 
            icon="fa-solid fa-palette" />
</column>
```

**Casos de uso:**
- Colores de marca, temas personalizados
- Códigos de color hexadecimal

---

### 2.20 WidgetJson - JSON Estruturado

**Clase:** `WidgetJson.php`  
**Tipo XML:** `type="json"`

**Propiedades configurables:**
- `fieldname` (requerido): Nombre del campo
- `rows` (opcional): Número de filas del textarea
- `required` (opcional): "true"
- `readonly` (opcional): "true" o "dinamic"
- `maxlength` (opcional): Longitud máxima
- `class` (opcional): Clases CSS

**Renderizado:**
- **Edit view**: Textarea para JSON con sintaxis resaltada
- **List view**: Estructura JSON representada en formato legible
- **Validación**: Verifica que el JSON sea válido

**Ejemplo:**
```xml
<column name="metadata" order="100">
    <widget type="json" fieldname="metadatos" rows="10" />
</column>
```

**Casos de uso:**
- Almacenar datos estructurados en formato JSON
- Configuraciones, metadatos, arrays

---

### 2.21 WidgetBytes - Tamaño de Bytes

**Clase:** `WidgetBytes.php`  
**Tipo XML:** `type="bytes"`

**Propiedades configurables:**
- `fieldname` (requerido): Nombre del campo
- `required` (opcional): "true"
- `readonly` (opcional): "true" o "dinamic"
- `class` (opcional): Clases CSS

**Renderizado:**
- **Edit view**: Input numérico (bytes)
- **List view**: Formateado como KB, MB, GB automáticamente

**Ejemplo:**
```xml
<column name="file-size" order="100">
    <widget type="bytes" fieldname="tamanyo" readonly="true" />
</column>
```

**Casos de uso:**
- Tamaños de archivos
- Espacios en disco

---

### 2.22 WidgetSeconds - Duración en Segundos

**Clase:** `WidgetSeconds.php`  
**Tipo XML:** `type="seconds"`

**Propiedades configurables:**
- `fieldname` (requerido): Nombre del campo
- `required` (opcional): "true"
- `readonly` (opcional): "true" o "dinamic"
- `class` (opcional): Clases CSS

**Renderizado:**
- **Edit view**: Input numérico (segundos)
- **List view**: Formateado como hh:mm:ss

**Ejemplo:**
```xml
<column name="duration" order="100">
    <widget type="seconds" fieldname="duracion" />
</column>
```

**Casos de uso:**
- Duraciones, tiempos transcurridos
- Cálculos de horas

---

### 2.23 WidgetStars - Calificación por Estrellas

**Clase:** `WidgetStars.php`  
**Tipo XML:** `type="stars"`

**Propiedades configurables:**
- `fieldname` (requerido): Nombre del campo
- `required` (opcional): "true"
- `readonly` (opcional): "true" o "dinamic"
- `class` (opcional): Clases CSS

**Renderizado:**
- **Edit view**: Estrellas clickeables (1-5) para calificar
- **List view**: Estrellas representando la calificación
- **JavaScript**: Maneja interactividad de estrellas

**Ejemplo:**
```xml
<column name="rating" order="100">
    <widget type="stars" fieldname="calificacion" />
</column>
```

**Casos de uso:**
- Calificaciones de clientes
- Puntuaciones, evaluaciones

---

### 2.24 WidgetVariante - Variantes de Producto

**Clase:** `WidgetVariante.php`  
**Tipo XML:** `type="variante"`

**Propiedades configurables:**
- `fieldname` (requerido): Nombre del campo
- `required` (opcional): "true"
- `readonly` (opcional): "true" o "dinamic"
- `class` (opcional): Clases CSS

**Renderizado:**
- **Edit view**: Selector especializado para variantes de productos
- **List view**: Código de variante

**Casos de uso:**
- Seleccionar variantes de productos (talla, color, etc.)
- En líneas de documentos

---

### 2.25 WidgetSubcuenta - Subcuenta Contable

**Clase:** `WidgetSubcuenta.php`  
**Tipo XML:** `type="subcuenta"`

**Propiedades configurables:**
- `fieldname` (requerido): Nombre del campo
- `required` (opcional): "true"
- `readonly` (opcional): "true" o "dinamic"
- `icon` (opcional): Clase FontAwesome
- `class` (opcional): Clases CSS

**Renderizado:**
- **Edit view**: Selector avanzado para subcuentas contables
- **List view**: Código de subcuenta
- **Búsqueda**: Autocompletado especializado

**Casos de uso:**
- Contabilidad, asientos contables
- Asignación de cuentas

---

### 2.26 Tipos especiales de Input (HTML5)

FacturaScripts soporta tipos HTML5 adicionales directamente:

```xml
<!-- Email -->
<widget type="email" fieldname="email" />

<!-- Teléfono -->
<widget type="tel" fieldname="telefono" />

<!-- URL -->
<widget type="url" fieldname="sitio" />

<!-- Número (similar a number pero para enteros) -->
<widget type="integer" fieldname="cantidad" />

<!-- Oculto (no se muestra en formulario) -->
<widget type="hidden" fieldname="campo_oculto" />
```

---

## 3. Plantillas Twig

### 3.1 Estructura de Plantillas Master

Las plantillas maestras en `Core/View/Master/` definen la estructura base de páginas:

**Plantillas principales:**
- `BaseView.html.twig`: Plantilla base vacía (herencia)
- `ListView.html.twig`: Listados de registros
- `EditView.html.twig`: Formularios de edición
- `EditListView.html.twig`: Tablas editable dentro de formularios
- `EditViewReadOnly.html.twig`: Formularios solo lectura
- `ListController.html.twig`: Controlador de listados
- `PanelController.html.twig`: Paneles de control
- `MenuTemplate.html.twig`: Menú principal
- `MicroTemplate.html.twig`: Plantilla para vista API/AJAX

### 3.2 Estructura de Bloques Principales

Cada plantilla define bloques que pueden ser extendidos:

```twig
{# Bloques principales en BaseView #}
{% block meta %}
    <!-- Meta tags, título, etc. -->
{% endblock %}

{% block css %}
    <!-- Enlaces a CSS -->
{% endblock %}

{% block body %}
    <!-- Contenido HTML -->
{% endblock %}

{% block javascript %}
    <!-- Scripts JavaScript -->
{% endblock %}

{% block modals %}
    <!-- Diálogos modales -->
{% endblock %}

{% block messages %}
    <!-- Mensajes de éxito/error -->
{% endblock %}
```

### 3.3 Macros Disponibles

**Macro Forms.html.twig:**
```twig
{{ macros.simpleInput(id, name, value, type, label, icon, attributes) }}
{{ macros.simpleSelect(id, name, value, allValues, label, icon, attributes) }}
{{ macros.simpleTextarea(id, name, value, label, icon, attributes) }}
```

**Macro Menu.html.twig:**
```twig
{{ macros.getMenu() }}
{{ macros.getSubMenu(menuname) }}
```

**Macro Utils.html.twig:**
```twig
{{ macros.simpleButton(label, url, type, icon) }}
{{ macros.confirmDelete(text) }}
```

### 3.4 Variables Disponibles en Plantillas

En cualquier plantilla Twig, están disponibles:

```twig
{{ fsc }}                           <!-- Objeto controlador actual -->
{{ fsc.title }}                     <!-- Título de la página -->
{{ fsc.subtitle }}                  <!-- Subtítulo -->
{{ user }}                          <!-- Usuario actual -->
{{ user.nick }}                     <!-- Nick del usuario -->
{{ user.email }}                    <!-- Email del usuario -->
{{ config }}                        <!-- Configuración global -->
{{ config('company', 'name') }}     <!-- Nombre de empresa -->
{{ now }}                           <!-- Fecha/hora actual -->
{{ tableName }}                     <!-- Nombre de tabla -->
{{ modelClassName }}                <!-- Clase del modelo -->
```

### 3.5 Funciones Twig Personalizadas

FacturaScripts proporciona funciones Twig customizadas:

```twig
{# Asset - incluir archivos CSS/JS #}
{{ asset('path/to/file.css') }}
{{ asset('path/to/file.js') }}

{# Traducción #}
{{ trans('my-key') }}
{{ trans('key-with-params', {'%name%': 'value'}) }}

{# Dinero/Moneda #}
{{ money(1234.56) }}
{{ money(1234.56, 'EUR') }}
{{ money(1234.56, 'USD', 2) }}

{# Número formateado #}
{{ number(1234.567, 2) }}

{# Caché #}
{{ cache('cache-key') }}
{% set cached = cache('key', 3600) %} {# 1 hora #}

{# Configuración #}
{{ config('company', 'name') }}
{{ config('accounting', 'method') }}

{# Acceso HTML seguro #}
{{ trans(key)|raw }}

{# Escaping HTML #}
{{ content|escape }}

{# Longitud de strings #}
{{ mystring|length }}

{# Mayúsculas/minúsculas #}
{{ text|upper }}
{{ text|lower }}
{{ text|capitalize }}

{# Sustitución de variables en strings #}
{{ trans('hello-user', {'%user%': username}) }}
```

### 3.6 Como Extender Plantillas desde un Plugin

Desde un plugin, puedes extender plantillas del core:

**Estructura de carpetas:**
```
Plugin/
    View/
        Master/
            ListView.html.twig      (extiende core ListView)
        Tab/
            TabName.html.twig       (nueva pestaña)
        Macro/
            CustomMacro.html.twig   (nuevas macros)
```

**Ejemplo de extensión:**
```twig
{# Plugin/View/Master/ListView.html.twig #}
{% extends 'Master/ListView.html.twig' %}

{% block body %}
    {{ parent() }}
    
    {# Tu contenido adicional aquí #}
    <div class="my-plugin-widget">
        <!-- contenido personalizado -->
    </div>
{% endblock %}

{% block javascript %}
    {{ parent() }}
    
    <script>
        // Tu JavaScript aquí
    </script>
{% endblock %}
```

### 3.7 Acceso a Datos del Modelo en Plantillas

```twig
{# Desde un controlador Edit #}
{% if this.model %}
    <p>Código: {{ this.model.codigo }}</p>
    <p>Nombre: {{ this.model.nombre }}</p>
{% endif %}

{# Acceso a tablas relacionadas #}
{% set lines = this.model.getLines() %}
{% for line in lines %}
    <tr>
        <td>{{ line.concepto }}</td>
        <td>{{ line.cantidad }}</td>
        <td>{{ line.pvpunitario }}</td>
    </tr>
{% endfor %}
```

### 3.8 Condiciones y Loops en Twig

```twig
{# Condicionales #}
{% if user.isAdmin() %}
    <p>Área administrativa</p>
{% elseif user.isEditor() %}
    <p>Área de edición</p>
{% else %}
    <p>Área de visualización</p>
{% endif %}

{# Loops #}
{% for item in items %}
    <p>{{ item.nombre }}</p>
    
    {% if loop.first %}
        <p>Primer elemento</p>
    {% endif %}
    
    {% if loop.last %}
        <p>Último elemento</p>
    {% endif %}
{% endfor %}

{# Loop vacío #}
{% for item in items %}
    ...
{% else %}
    <p>No hay elementos</p>
{% endfor %}
```

---

## 4. Lista Completa de XMLViews del Core

FacturaScripts incluye **133 XMLViews** en el core. A continuación, se organizan por área funcional:

### 4.1 XMLViews de Configuración y Seguridad

| Vista | Modelo | Descripción |
|-------|--------|-------------|
| ConfigEmail | (configuración) | Configuración de correo electrónico |
| EditRole | Role | Editar roles de usuario |
| EditUser | User | Editar usuarios |
| ListRole | Role | Listar roles |
| ListUser | User | Listar usuarios |
| EditApiKey | ApiKey | Claves API |
| ListApiKey | ApiKey | Listar claves API |
| EditPageOption | PageOption | Opciones de página |
| ListPageOption | PageOption | Listar opciones |

### 4.2 XMLViews de Empresa y Establecimientos

| Vista | Modelo | Descripción |
|-------|--------|-------------|
| EditEmpresa | Empresa | Datos de empresa |
| EditAlmacen | Almacen | Almacén/depósito |
| EditDivisa | Divisa | Monedas y divisas |
| EditDiario | Diario | Diarios contables |
| EditSerie | Serie | Series de documentos |
| EditFormaPago | FormaPago | Formas de pago |
| EditSecuenciaDocumento | SecuenciaDocumento | Secuencias documentales |
| ListAlmacen | Almacen | Listar almacenes |
| ListDivisa | Divisa | Listar divisas |
| ListDiario | Diario | Listar diarios |
| ListSerie | Serie | Listar series |
| ListFormaPago | FormaPago | Listar formas de pago |
| ListSecuenciaDocumento | SecuenciaDocumento | Listar secuencias |

### 4.3 XMLViews de Terceros (Clientes/Proveedores)

| Vista | Modelo | Descripción |
|-------|--------|-------------|
| EditCliente | Cliente | Editar cliente |
| EditProveedor | Proveedor | Editar proveedor |
| EditContacto | Contacto | Contactos de clientes/proveedores |
| EditDireccionContacto | DireccionContacto | Direcciones de contacto |
| ListCliente | Cliente | Listar clientes |
| ListProveedor | Proveedor | Listar proveedores |
| ListContacto | Contacto | Listar contactos |
| EditGrupoClientes | GrupoClientes | Grupos de clientes |
| ListGrupoClientes | GrupoClientes | Listar grupos |
| EditCuentaBancoCliente | CuentaBancoCliente | Cuentas bancarias de clientes |
| EditCuentaBancoProveedor | CuentaBancoProveedor | Cuentas bancarias de proveedores |
| ListCuentaBancoCliente | CuentaBancoCliente | Listar cuentas de clientes |

### 4.4 XMLViews de Productos

| Vista | Modelo | Descripción |
|-------|--------|-------------|
| EditProducto | Producto | Editar producto |
| EditVariante | Variante | Variantes de producto |
| EditProductoProveedor | ProductoProveedor | Relación producto-proveedor |
| EditFamilia | Familia | Familia de productos |
| EditFabricante | Fabricante | Fabricantes |
| EditAtributo | Atributo | Atributos de productos |
| EditAtributoValor | AtributoValor | Valores de atributos |
| EditTarifa | Tarifa | Tarifas de precios |
| ListProducto | Producto | Listar productos |
| ListVariante | Variante | Listar variantes |
| ListProductoProveedor | ProductoProveedor | Listar relaciones |
| ListFamilia | Familia | Listar familias |
| ListFabricante | Fabricante | Listar fabricantes |
| ListAtributo | Atributo | Listar atributos |
| ListAtributoValor | AtributoValor | Listar valores |
| ListTarifa | Tarifa | Listar tarifas |
| ListTarifaProducto | TarifaProducto | Tarifas por producto |
| EditStock | Stock | Stock en almacén |
| ListStock | Stock | Listar stock |

### 4.5 XMLViews de Documentos Comerciales

| Vista | Modelo | Descripción |
|-------|--------|-------------|
| EditPresupuestoCliente | PresupuestoCliente | Presupuesto a cliente |
| EditPedidoCliente | PedidoCliente | Pedido de cliente |
| EditAlbaranCliente | AlbaranCliente | Albarán de cliente |
| EditFacturaCliente | FacturaCliente | Factura de cliente |
| EditPresupuestoProveedor | PresupuestoProveedor | Presupuesto a proveedor |
| EditPedidoProveedor | PedidoProveedor | Pedido a proveedor |
| EditAlbaranProveedor | AlbaranProveedor | Albarán de proveedor |
| EditFacturaProveedor | FacturaProveedor | Factura de proveedor |
| ListPresupuestoCliente | PresupuestoCliente | Presupuestos de clientes |
| ListPedidoCliente | PedidoCliente | Pedidos de clientes |
| ListAlbaranCliente | AlbaranCliente | Albaranes de clientes |
| ListFacturaCliente | FacturaCliente | Facturas de clientes |
| ListPresupuestoProveedor | PresupuestoProveedor | Presupuestos de proveedores |
| ListPedidoProveedor | PedidoProveedor | Pedidos de proveedores |
| ListAlbaranProveedor | AlbaranProveedor | Albaranes de proveedores |
| ListFacturaProveedor | FacturaProveedor | Facturas de proveedores |
| EditReciboCliente | ReciboCliente | Recibos de cliente |
| EditReciboProveedor | ReciboProveedor | Recibos de proveedor |
| ListReciboCliente | ReciboCliente | Listar recibos |
| ListReciboProveedor | ReciboProveedor | Listar recibos |
| EditPagoCliente | PagoCliente | Pagos de clientes |
| EditPagoProveedor | PagoProveedor | Pagos a proveedores |
| ListPagoCliente | PagoCliente | Listar pagos |
| ListPagoProveedor | PagoProveedor | Listar pagos |

### 4.6 XMLViews de Líneas de Documentos

| Vista | Modelo | Descripción |
|-------|--------|-------------|
| ListLineaPresupuestoCliente | LineaPresupuestoCliente | Líneas de presupuesto |
| ListLineaPedidoCliente | LineaPedidoCliente | Líneas de pedido |
| ListLineaAlbaranCliente | LineaAlbaranCliente | Líneas de albarán |
| ListLineaFacturaCliente | LineaFacturaCliente | Líneas de factura |
| ListLineaPresupuestoProveedor | LineaPresupuestoProveedor | Líneas presupuesto proveedor |
| ListLineaPedidoProveedor | LineaPedidoProveedor | Líneas pedido proveedor |
| ListLineaAlbaranProveedor | LineaAlbaranProveedor | Líneas albarán proveedor |
| ListLineaFacturaProveedor | LineaFacturaProveedor | Líneas factura proveedor |
| FacturaClienteProducto | LineaFacturaCliente | Productos en factura cliente |
| FacturaProveedorProducto | LineaFacturaProveedor | Productos en factura proveedor |

### 4.7 XMLViews de Contabilidad

| Vista | Modelo | Descripción |
|-------|--------|-------------|
| EditAsiento | Asiento | Asiento contable |
| EditPartida | Partida | Partida de asiento |
| EditCuenta | Cuenta | Cuentas contables |
| EditSubcuenta | Subcuenta | Subcuentas |
| EditCuentaBanco | CuentaBanco | Cuentas bancarias |
| EditCuentaEspecial | CuentaEspecial | Cuentas especiales |
| EditEjercicio | Ejercicio | Ejercicios contables |
| ListAsiento | Asiento | Listar asientos |
| ListPartida | Partida | Listar partidas |
| ListPartidaAsiento | Partida | Partidas de asiento |
| ListCuenta | Cuenta | Listar cuentas |
| ListSubcuenta | Subcuenta | Listar subcuentas |
| ListCuentaBanco | CuentaBanco | Listar cuentas bancarias |
| ListCuentaEspecial | CuentaEspecial | Listar cuentas especiales |
| ListEjercicio | Ejercicio | Listar ejercicios |

### 4.8 XMLViews de Impuestos y Retenciones

| Vista | Modelo | Descripción |
|-------|--------|-------------|
| EditImpuesto | Impuesto | Impuestos (IVA, etc.) |
| EditImpuestoZona | ImpuestoZona | Impuestos por zona |
| EditRetencion | Retencion | Retenciones |
| ListImpuesto | Impuesto | Listar impuestos |
| ListRetencion | Retencion | Listar retenciones |

### 4.9 XMLViews de Ubicaciones Geográficas

| Vista | Modelo | Descripción |
|-------|--------|-------------|
| EditPais | Pais | País |
| EditProvincia | Provincia | Provincia |
| EditCiudad | Ciudad | Ciudad |
| EditCodigoPostal | CodigoPostal | Código postal |
| ListPais | Pais | Listar países |
| ListProvincia | Provincia | Listar provincias |
| ListCiudad | Ciudad | Listar ciudades |
| ListCodigoPostal | CodigoPostal | Listar códigos postales |

### 4.10 XMLViews de Agentes y Logística

| Vista | Modelo | Descripción |
|-------|--------|-------------|
| EditAgente | Agente | Agentes de ventas |
| EditAgenciaTransporte | AgenciaTransporte | Agencias de transporte |
| ListAgente | Agente | Listar agentes |
| ListAgenciaTransporte | AgenciaTransporte | Listar agencias |

### 4.11 XMLViews de Documentos Especiales

| Vista | Modelo | Descripción |
|-------|--------|-------------|
| EditAttachedFile | AttachedFile | Archivo adjunto |
| ListAttachedFile | AttachedFile | Listar adjuntos |
| ListAttachedFileRelation | AttachedFileRelation | Relaciones de adjuntos |
| EditWorkEvent | WorkEvent | Evento de trabajo |
| ListWorkEvent | WorkEvent | Listar eventos |
| EditCronJob | CronJob | Tareas programadas |
| ListCronJob | CronJob | Listar tareas |

### 4.12 XMLViews de Sistema y Mantenimiento

| Vista | Modelo | Descripción |
|-------|--------|-------------|
| EditEstadoDocumento | EstadoDocumento | Estados de documento |
| EditFormatoDocumento | FormatoDocumento | Formatos de documento |
| EditIdentificadorFiscal | IdentificadorFiscal | Identificadores fiscales |
| EditConceptoPartida | ConceptoPartida | Conceptos de partida |
| ListEstadoDocumento | EstadoDocumento | Listar estados |
| ListFormatoDocumento | FormatoDocumento | Listar formatos |
| ListIdentificadorFiscal | IdentificadorFiscal | Listar identificadores |
| ListConceptoPartida | ConceptoPartida | Listar conceptos |
| EditEmailNotification | EmailNotification | Notificaciones por email |
| ListEmailNotification | EmailNotification | Listar notificaciones |
| EditEmailSent | EmailSent | Emails enviados |
| ListEmailSent | EmailSent | Listar emails |
| EditLogMessage | LogMessage | Registro de mensajes |
| ListLogMessage | LogMessage | Listar mensajes |
| EditRoleUser | RoleUser | Roles de usuario |
| SettingsDefault | Settings | Configuración general |

### 4.13 XMLViews de Puntos de Interés

| Vista | Modelo | Descripción |
|-------|--------|-------------|
| EditPuntoInteresCiudad | PuntoInteresCiudad | Punto de interés |
| ListPuntoInteresCiudad | PuntoInteresCiudad | Listar puntos |

---

## 5. Como Crear Vistas Personalizadas

### 5.1 Crear un XMLView para un Listado (ListView)

**Paso 1: Crear el archivo XML**

Crea `Plugins/MiPlugin/XMLView/ListMiModelo.xml`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<view>
    <columns>
        <!-- Columna de código/ID -->
        <column name="code" order="100">
            <widget type="text" fieldname="codigo" onclick="EditMiModelo" />
        </column>
        
        <!-- Columna de nombre -->
        <column name="name" order="110">
            <widget type="text" fieldname="nombre" />
        </column>
        
        <!-- Columna de descripción (oculta por defecto) -->
        <column name="description" display="none" order="120">
            <widget type="textarea" fieldname="descripcion" />
        </column>
        
        <!-- Columna de fecha de creación -->
        <column name="creation-date" order="130">
            <widget type="date" fieldname="fechacreacion" />
        </column>
        
        <!-- Columna de estado -->
        <column name="status" order="140">
            <widget type="select" fieldname="estado" translate="true">
                <values title="active">1</values>
                <values title="inactive">0</values>
            </widget>
        </column>
    </columns>
    
    <rows>
        <!-- Filas de estado: colorea según el valor -->
        <row type="status">
            <option color="danger" title="inactive" fieldname="estado">0</option>
            <option color="success" title="active" fieldname="estado">1</option>
        </row>
    </rows>
</view>
```

**Paso 2: Crear el controlador**

Crea `Plugins/MiPlugin/Controller/ListMiModelo.php`:

```php
<?php
namespace FacturaScripts\Plugins\MiPlugin\Controller;

use FacturaScripts\Core\Base\Controller\ListController;

class ListMiModelo extends ListController
{
    public function getPageData()
    {
        $data = parent::getPageData();
        $data['title'] = 'my-models';
        $data['icon'] = 'fa-solid fa-cube';
        $data['showfilter'] = true;
        return $data;
    }

    protected function createViews()
    {
        $this->createViewList('ListMiModelo', 'MiModelo', 'list', 'my-models');
        
        // Aquí puedes agregar columnas, filtros, etc.
        $this->addOrderBy('ListMiModelo', 'codigo', 'code');
        $this->addOrderBy('ListMiModelo', 'nombre', 'name');
        $this->addOrderBy('ListMiModelo', 'fechacreacion', 'creation-date');
    }
}
```

### 5.2 Crear un XMLView para un Formulario de Edición (EditView)

**Paso 1: Crear el archivo XML**

Crea `Plugins/MiPlugin/XMLView/EditMiModelo.xml`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<view>
    <columns>
        <!-- Grupo de datos básicos -->
        <group name="basic" title="basic-data" numcolumns="12">
            <column name="code" numcolumns="2" order="100">
                <widget type="text" fieldname="codigo" icon="fa-solid fa-hashtag" 
                        maxlength="10" readonly="dinamic" required="true" />
            </column>
            <column name="name" numcolumns="10" order="110">
                <widget type="text" fieldname="nombre" maxlength="100" 
                        required="true" icon="fa-solid fa-user" />
            </column>
        </group>
        
        <!-- Grupo de descripción y estado -->
        <group name="details" title="details" numcolumns="12">
            <column name="description" numcolumns="9" order="100">
                <widget type="textarea" fieldname="descripcion" rows="4" />
            </column>
            <column name="status" numcolumns="3" order="110">
                <widget type="select" fieldname="estado" translate="true" required="true">
                    <values title="active">1</values>
                    <values title="inactive">0</values>
                </widget>
            </column>
        </group>
        
        <!-- Grupo de información adicional -->
        <group name="additional" title="additional-info" numcolumns="12">
            <column name="creation-date" numcolumns="3" order="100">
                <widget type="date" fieldname="fechacreacion" readonly="true" 
                        icon="fa-solid fa-calendar" />
            </column>
            <column name="modification-date" numcolumns="3" order="110">
                <widget type="datetime" fieldname="fechamodificacion" readonly="true" 
                        icon="fa-solid fa-clock" />
            </column>
            <column name="percentage" numcolumns="3" order="120">
                <widget type="percentage" fieldname="porcentaje" decimal="2" />
            </column>
            <column name="amount" numcolumns="3" order="130">
                <widget type="money" fieldname="importe" decimal="2" />
            </column>
        </group>
    </columns>
    
    <rows>
        <!-- Estadísticas en la parte superior -->
        <row type="statistics">
            <datalabel icon="fa-solid fa-file" label="documents" 
                      function="countDocuments" color="info" />
            <datalabel icon="fa-solid fa-money-bill" label="total-amount" 
                      function="getTotalAmount" color="success" />
        </row>
    </rows>
</view>
```

**Paso 2: Crear el modelo**

Crea `Plugins/MiPlugin/Model/MiModelo.php`:

```php
<?php
namespace FacturaScripts\Plugins\MiPlugin\Model;

use FacturaScripts\Core\Model\Base\ModelClass;

class MiModelo extends ModelClass
{
    public $codigo;
    public $nombre;
    public $descripcion;
    public $estado;
    public $fechacreacion;
    public $fechamodificacion;
    public $porcentaje;
    public $importe;
    
    public static function tableName()
    {
        return 'mimodelos';
    }
    
    // Métodos para las estadísticas
    public function countDocuments()
    {
        return '15';  // Implementar según lógica
    }
    
    public function getTotalAmount()
    {
        return '1,250.00';  // Implementar según lógica
    }
}
```

**Paso 3: Crear el controlador**

Crea `Plugins/MiPlugin/Controller/EditMiModelo.php`:

```php
<?php
namespace FacturaScripts\Plugins\MiPlugin\Controller;

use FacturaScripts\Core\Base\Controller\EditController;

class EditMiModelo extends EditController
{
    public function getModelClassName()
    {
        return 'MiModelo';
    }

    public function getPageData()
    {
        $data = parent::getPageData();
        $data['title'] = 'my-model';
        $data['icon'] = 'fa-solid fa-cube';
        $data['showfilter'] = false;
        return $data;
    }

    protected function createViews()
    {
        parent::createViews();
        $this->createViewEdit('EditMiModelo', 'MiModelo', 'edit', 'my-model');
    }
}
```

### 5.3 Añadir Modales

Los modales son diálogos que se pueden abrir desde botones o enlaces:

```xml
<columns>
    <!-- Botón que abre el modal -->
    <column name="open-info" order="200">
        <widget type="link" fieldname="infourl" onclick="...">
            <!-- Esto abre un modal #}
        </widget>
    </column>
    
    <!-- El modal mismo -->
    <modal name="modal_info" title="additional-information">
        <column name="notes" order="100">
            <widget type="textarea" fieldname="notas" rows="5" />
        </column>
        <column name="related-items" order="110">
            <widget type="select" fieldname="itemrelacionado">
                <values source="items" fieldcode="id" fieldtitle="nombre" />
            </widget>
        </column>
    </modal>
</columns>
```

Para abrir el modal desde JavaScript:
```javascript
// Abrir modal
bootstrap.Modal.getOrCreateInstance('#modal_info').show();

// Cerrar modal
bootstrap.Modal.getInstance('#modal_info').hide();
```

### 5.4 Añadir Filas de Estado (Colores según Estado)

```xml
<rows>
    <row type="status">
        <!-- Rojo si está cancelado -->
        <option color="danger" title="canceled" fieldname="estado">Cancelado</option>
        
        <!-- Naranja si está pendiente -->
        <option color="warning" title="pending" fieldname="estado">Pendiente</option>
        
        <!-- Verde si está completado -->
        <option color="success" title="completed" fieldname="estado">Completado</option>
        
        <!-- Azul si está en progreso -->
        <option color="info" title="in-progress" fieldname="estado">En Progreso</option>
        
        <!-- Usar operadores para comparaciones numéricas -->
        <option color="warning" title="low-stock" fieldname="cantidad" operator="<">10</option>
        <option color="success" title="adequate-stock" fieldname="cantidad" operator=">=">10</option>
    </row>
</rows>
```

Los colores disponibles son:
- `danger`: Rojo (crítico, error)
- `success`: Verde (éxito, completado)
- `warning`: Naranja/amarillo (advertencia, precaución)
- `info`: Azul claro (información)
- `dark`: Gris oscuro
- `secondary`: Gris claro
- `primary`: Azul primario
- `light`: Blanco/gris muy claro

### 5.5 Ejemplo Completo Integrado

Este es un ejemplo completo de modelo, vistas y controlador para una tabla de "Clientes VIP":

**Archivo 1: Plugins/MiPlugin/XMLView/ListClienteVIP.xml**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<view>
    <columns>
        <column name="code" order="100">
            <widget type="text" fieldname="codigo" onclick="EditClienteVIP" />
        </column>
        <column name="name" order="110">
            <widget type="text" fieldname="nombre" />
        </column>
        <column name="email" order="120">
            <widget type="email" fieldname="email" />
        </column>
        <column name="phone" order="130">
            <widget type="tel" fieldname="telefono" />
        </column>
        <column name="level" order="140">
            <widget type="select" fieldname="nivel" translate="true">
                <values title="gold">GOLD</values>
                <values title="silver">SILVER</values>
                <values title="bronze">BRONZE</values>
            </widget>
        </column>
        <column name="discount" order="150">
            <widget type="percentage" fieldname="descuento" decimal="2" />
        </column>
        <column name="status" order="160">
            <widget type="checkbox" fieldname="activo" />
        </column>
    </columns>
    <rows>
        <row type="status">
            <option color="danger" title="inactive" fieldname="activo">0</option>
            <option color="success" title="active" fieldname="activo">1</option>
        </row>
    </rows>
</view>
```

**Archivo 2: Plugins/MiPlugin/XMLView/EditClienteVIP.xml**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<view>
    <columns>
        <group name="basic" title="basic-info" numcolumns="12">
            <column name="code" numcolumns="2" order="100">
                <widget type="text" fieldname="codigo" readonly="dinamic" required="true" />
            </column>
            <column name="name" numcolumns="5" order="110">
                <widget type="text" fieldname="nombre" required="true" maxlength="100" />
            </column>
            <column name="level" numcolumns="2" order="120">
                <widget type="select" fieldname="nivel" translate="true" required="true">
                    <values title="gold">GOLD</values>
                    <values title="silver">SILVER</values>
                    <values title="bronze">BRONZE</values>
                </widget>
            </column>
            <column name="status" numcolumns="3" order="130">
                <widget type="checkbox" fieldname="activo" />
            </column>
        </group>
        
        <group name="contact" title="contact-info" numcolumns="12">
            <column name="email" numcolumns="6" order="100">
                <widget type="email" fieldname="email" required="true" />
            </column>
            <column name="phone" numcolumns="6" order="110">
                <widget type="tel" fieldname="telefono" />
            </column>
        </group>
        
        <group name="commercial" title="commercial-info" numcolumns="12">
            <column name="discount" numcolumns="3" order="100">
                <widget type="percentage" fieldname="descuento" decimal="2" />
            </column>
            <column name="credit-limit" numcolumns="3" order="110">
                <widget type="money" fieldname="limiteCredito" decimal="2" />
            </column>
            <column name="registration-date" numcolumns="3" order="120">
                <widget type="date" fieldname="fechaRegistro" readonly="true" />
            </column>
            <column name="last-purchase" numcolumns="3" order="130">
                <widget type="date" fieldname="fechaUltimaCompra" readonly="true" />
            </column>
        </group>
        
        <group name="notes" numcolumns="12">
            <column name="observations" order="100">
                <widget type="textarea" fieldname="observaciones" rows="4" />
            </column>
        </group>
    </columns>
    
    <rows>
        <row type="statistics">
            <datalabel icon="fa-solid fa-file-invoice" label="total-invoices" 
                      function="getTotalInvoices" color="info" />
            <datalabel icon="fa-solid fa-money-bill" label="total-amount" 
                      function="getTotalAmount" color="success" />
            <datalabel icon="fa-solid fa-box" label="total-items" 
                      function="getTotalItems" color="warning" />
        </row>
    </rows>
</view>
```

**Archivo 3: Plugins/MiPlugin/Model/ClienteVIP.php**

```php
<?php
namespace FacturaScripts\Plugins\MiPlugin\Model;

use FacturaScripts\Core\Model\Base\ModelClass;
use FacturaScripts\Core\Tools;

class ClienteVIP extends ModelClass
{
    public $codigo;
    public $nombre;
    public $email;
    public $telefono;
    public $nivel;
    public $descuento;
    public $activo;
    public $limiteCredito;
    public $fechaRegistro;
    public $fechaUltimaCompra;
    public $observaciones;
    
    public static function tableName()
    {
        return 'clientesvip';
    }
    
    public static function primaryColumn()
    {
        return 'codigo';
    }
    
    public function getTotalInvoices()
    {
        // Implementar lógica para contar facturas
        return '25';
    }
    
    public function getTotalAmount()
    {
        // Implementar lógica para sumar importes
        return Tools::money(15000, 'EUR', 2);
    }
    
    public function getTotalItems()
    {
        // Implementar lógica para contar items
        return '156';
    }
}
```

**Archivo 4: Plugins/MiPlugin/Controller/ListClienteVIP.php**

```php
<?php
namespace FacturaScripts\Plugins\MiPlugin\Controller;

use FacturaScripts\Core\Base\Controller\ListController;

class ListClienteVIP extends ListController
{
    public function getPageData()
    {
        $data = parent::getPageData();
        $data['title'] = 'vip-clients';
        $data['icon'] = 'fa-solid fa-crown';
        $data['showfilter'] = true;
        return $data;
    }

    protected function createViews()
    {
        $this->createViewList('ListClienteVIP', 'ClienteVIP', 'list', 'vip-clients');
        
        $this->addOrderBy('ListClienteVIP', 'codigo', 'code');
        $this->addOrderBy('ListClienteVIP', 'nombre', 'name');
        $this->addOrderBy('ListClienteVIP', 'nivel', 'level');
        $this->addOrderBy('ListClienteVIP', 'descuento', 'discount');
    }
}
```

**Archivo 5: Plugins/MiPlugin/Controller/EditClienteVIP.php**

```php
<?php
namespace FacturaScripts\Plugins\MiPlugin\Controller;

use FacturaScripts\Core\Base\Controller\EditController;

class EditClienteVIP extends EditController
{
    public function getModelClassName()
    {
        return 'ClienteVIP';
    }

    public function getPageData()
    {
        $data = parent::getPageData();
        $data['title'] = 'vip-client';
        $data['icon'] = 'fa-solid fa-crown';
        return $data;
    }

    protected function createViews()
    {
        parent::createViews();
        $this->createViewEdit('EditClienteVIP', 'ClienteVIP', 'edit', 'vip-client');
    }
}
```

### 5.6 Buenas Prácticas

**Convenciones de nombres:**
- XMLView: `List{Modelo}.xml` y `Edit{Modelo}.xml`
- Controllers: `List{Modelo}.php` y `Edit{Modelo}.php`
- Campos: snake_case en la base de datos, camelCase en propiedades PHP
- Orden de campos: Usar múltiplos de 10 (100, 110, 120...)

**Estructura recomendada:**
- Grupo "basic" o "data": Datos fundamentales
- Grupo "contact": Información de contacto
- Grupo "commercial": Términos comerciales
- Grupo "notes": Notas y observaciones

**Colores y estados:**
- `danger` (rojo): Estados críticos, errores, suspensiones
- `success` (verde): Completado, activo, aprobado
- `warning` (naranja): Pendiente, atención, bajo stock
- `info` (azul): Información adicional

**Validación:**
- Usa `required="true"` para campos obligatorios
- Usa `readonly="dinamic"` para campos que son de lectura después de crearse
- Usa `readonly="true"` para campos completamente de solo lectura
- Define límites con `min`, `max` en números

---

## Resumen de Referencias Rápidas

### Widgets por Tipo de Dato

| Tipo de Dato | Widgets Recomendados |
|--------------|----------------------|
| Texto simple | text, textarea |
| Código/ID | text (con icon fa-hashtag) |
| Nombre | text, autocomplete |
| Email | email |
| Teléfono | tel |
| URL | link |
| Fecha | date |
| Fecha y hora | datetime |
| Hora | time |
| Número | number, integer |
| Dinero | money |
| Porcentaje | percentage |
| Booleano | checkbox, radio, select |
| Selección única | select, autocomplete, radio |
| Archivo | file, library |
| Color | color |
| Contraseña | password |
| JSON | json |
| Tamaño bytes | bytes |
| Duración | seconds |
| Calificación | stars |
| Variante producto | variante |
| Subcuenta | subcuenta |

### Atributos Comunes a Todos los Widgets

```xml
<widget 
    type="text"                     <!-- Tipo de widget -->
    fieldname="campo"               <!-- Campo del modelo (requerido) -->
    required="true"                 <!-- Campo obligatorio -->
    readonly="true"                 <!-- Solo lectura -->
    readonly="dinamic"              <!-- Solo lectura si tiene valor -->
    icon="fa-solid fa-user"         <!-- Ícono FontAwesome -->
    class="custom-class"            <!-- Clases CSS adicionales -->
    tabindex="1"                    <!-- Índice de tabulación -->
    autocomplete="off"              <!-- Autocomplete del navegador -->
    onclick="EditOtro"              <!-- Página de destino al hacer clic -->
/>
```

### Estructura de Grupos (Edit Views)

```xml
<group name="identificador" title="clave-traduccion" numcolumns="12">
    <column name="..." numcolumns="6" order="100">
        <!-- numcolumns: 1-12 (ancho Bootstrap) -->
        <!-- order: múltiplos de 10 (100, 110, 120...) -->
        <widget ... />
    </column>
</group>
```

### Elementos de Estadísticas

```xml
<row type="statistics">
    <datalabel 
        icon="fa-solid fa-chart"        <!-- Ícono FontAwesome -->
        label="clave-traduccion"        <!-- Texto etiqueta -->
        function="getNombreFuncion"     <!-- Método en controlador -->
        color="success"                 <!-- Color botón (optional) -->
        link="EditOtro"                 <!-- URL destino (optional) -->
        id="stat-id"                    <!-- ID elemento (optional) -->
        class="custom-class"            <!-- Clases CSS (optional) -->
    />
</row>
```

---

**Fin de la documentación exhaustiva de FacturaScripts 2025 - Sistema de Vistas y Widgets.**

Para más información, consulta la documentación oficial en https://www.facturascripts.com/docs

---

## APENDICE A: Listado Alfabético Completo de 133 XMLViews

Las siguientes 133 vistas XML están disponibles en el core de FacturaScripts 2025:

### Vistas de Configuración (Edit)
1. ConfigEmail
2. EditAgenciaTransporte
3. EditAgente
4. EditAlmacen
5. EditApiKey
6. EditAsiento
7. EditAtributo
8. EditAtributoValor
9. EditAttachedFile
10. EditCiudad
11. EditCliente
12. EditCodigoPostal
13. EditConceptoPartida
14. EditContacto
15. EditCronJob
16. EditCuenta
17. EditCuentaBanco
18. EditCuentaBancoCliente
19. EditCuentaBancoProveedor
20. EditCuentaEspecial
21. EditDiario
22. EditDireccionContacto
23. EditDivisa
24. EditEjercicio
25. EditEmailNotification
26. EditEmailSent
27. EditEmpresa
28. EditEstadoDocumento
29. EditFabricante
30. EditFamilia
31. EditFormaPago
32. EditFormatoDocumento
33. EditGrupoClientes
34. EditIdentificadorFiscal
35. EditImpuesto
36. EditImpuestoZona
37. EditLogMessage
38. EditPais
39. EditPartida
40. EditProducto
41. EditProductoProveedor
42. EditProveedor
43. EditProvincia
44. EditPuntoInteresCiudad
45. EditReciboCliente
46. EditReciboProveedor
47. EditRetencion
48. EditRole
49. EditRoleUser
50. EditSecuenciaDocumento
51. EditSerie
52. EditStock
53. EditSubcuenta
54. EditTarifa
55. EditUser
56. EditVariante
57. EditWorkEvent

### Vistas de Listado (List)
58. FacturaClienteProducto
59. FacturaProveedorProducto
60. ListAgenciaTransporte
61. ListAgente
62. ListAlbaranCliente
63. ListAlbaranProveedor
64. ListAlmacen
65. ListApiKey
66. ListAsiento
67. ListAtributo
68. ListAtributoValor
69. ListAttachedFile
70. ListAttachedFileRelation
71. ListCiudad
72. ListCliente
73. ListCodigoPostal
74. ListConceptoPartida
75. ListContacto
76. ListCronJob
77. ListCuenta
78. ListCuentaBanco
79. ListCuentaBancoCliente
80. ListCuentaEspecial
81. ListDiario
82. ListDivisa
83. ListEjercicio
84. ListEmailNotification
85. ListEmailSent
86. ListEmpresa
87. ListEstadoDocumento
88. ListFabricante
89. ListFacturaCliente
90. ListFacturaProveedor
91. ListFamilia
92. ListFormaPago
93. ListFormatoDocumento
94. ListGrupoClientes
95. ListImpuesto
96. ListLineaAlbaranCliente
97. ListLineaAlbaranProveedor
98. ListLineaFacturaCliente
99. ListLineaFacturaProveedor
100. ListLineaPedidoCliente
101. ListLineaPedidoProveedor
102. ListLineaPresupuestoCliente
103. ListLineaPresupuestoProveedor
104. ListLogMessage
105. ListPageOption
106. ListPagoCliente
107. ListPagoProveedor
108. ListPais
109. ListPartida
110. ListPartidaAsiento
111. ListPedidoCliente
112. ListPedidoProveedor
113. ListPresupuestoCliente
114. ListPresupuestoProveedor
115. ListProducto
116. ListProductoProveedor
117. ListProveedor
118. ListProvincia
119. ListPuntoInteresCiudad
120. ListReciboCliente
121. ListReciboProveedor
122. ListRetencion
123. ListRole
124. ListSecuenciaDocumento
125. ListSerie
126. ListStock
127. ListSubcuenta
128. ListTarifa
129. ListTarifaProducto
130. ListUser
131. ListVariante
132. ListWorkEvent

### Vistas Especiales
133. SettingsDefault

---

## APENDICE B: Propiedades Heredadas en BaseWidget

Todos los widgets heredan de `BaseWidget`, que proporciona:

**Propiedades del constructor:**
- `$autocomplete`: bool - Habilita autocompletado HTML5
- `$fieldname`: string - Nombre del campo (requerido)
- `$icon`: string - Clase FontAwesome para el ícono
- `$onclick`: string - Ruta para navegación al hacer clic
- `$options`: array - Opciones del widget (para selects)
- `$readonly`: string - "true", "false", o "dinamic"
- `$required`: bool - Campo obligatorio
- `$tabindex`: int - Índice de tabulación
- `$value`: mixed - Valor actual del widget
- `$class`: string - Clases CSS personalizado
- `$id`: string - ID único del elemento

**Métodos heredados:**
- `edit()`: Renderiza el widget en modo edición
- `tableCell()`: Renderiza en tabla/listado
- `plainText()`: Renderiza como texto plano
- `inputHidden()`: Input hidden para formularios
- `processFormData()`: Procesa datos POST del formulario
- `setCustomValue()`: Establece valor personalizado
- `gridFormat()`: Formatos para grillas JavaScript

---

## APENDICE C: Jerarquía de Clases de Widgets

```
VisualItem (clase base)
    ├── BaseWidget (base de todos los widgets)
    │   ├── WidgetText
    │   │   ├── WidgetTextarea
    │   │   ├── WidgetPassword
    │   │   └── WidgetLink
    │   ├── WidgetNumber
    │   │   ├── WidgetMoney
    │   │   ├── WidgetPercentage
    │   │   ├── WidgetBytes
    │   │   └── WidgetSeconds
    │   ├── WidgetDate
    │   ├── WidgetDatetime
    │   ├── WidgetTime
    │   ├── WidgetCheckbox
    │   ├── WidgetSelect
    │   │   ├── WidgetAutocomplete
    │   │   └── WidgetDatalist
    │   ├── WidgetRadio
    │   ├── WidgetFile
    │   ├── WidgetLibrary
    │   ├── WidgetColor
    │   ├── WidgetJson
    │   ├── WidgetStars
    │   ├── WidgetVariante
    │   ├── WidgetSubcuenta
    │   └── [otros widgets especializados]
    ├── RowStatus (filas de estado)
    ├── RowStatistics (estadísticas)
    ├── RowHeader (encabezado)
    ├── RowFooter (pie)
    ├── RowActions (acciones)
    ├── RowButton (botones)
    ├── RowBusiness (datos de negocio)
    ├── ColumnItem (elemento de columna)
    ├── GroupItem (grupo de columnas)
    └── VisualItemLoadEngine (cargador visual)
```

---

## APENDICE D: Casos de Uso Comunes

### Caso de Uso 1: Crear un Listado Simple

```xml
<?xml version="1.0" encoding="UTF-8"?>
<view>
    <columns>
        <column name="code" order="100">
            <widget type="text" fieldname="codigo" onclick="EditMiModelo" />
        </column>
        <column name="name" order="110">
            <widget type="text" fieldname="nombre" />
        </column>
        <column name="status" order="120">
            <widget type="select" fieldname="estado" translate="true">
                <values title="active">1</values>
                <values title="inactive">0</values>
            </widget>
        </column>
    </columns>
    <rows>
        <row type="status">
            <option color="success" title="active" fieldname="estado">1</option>
            <option color="danger" title="inactive" fieldname="estado">0</option>
        </row>
    </rows>
</view>
```

### Caso de Uso 2: Crear un Formulario Completo

```xml
<?xml version="1.0" encoding="UTF-8"?>
<view>
    <columns>
        <group name="basic" title="basic-data" numcolumns="12">
            <column name="name" numcolumns="6" order="100">
                <widget type="text" fieldname="nombre" required="true" />
            </column>
            <column name="code" numcolumns="6" order="110">
                <widget type="text" fieldname="codigo" readonly="dinamic" />
            </column>
        </group>
        <group name="contact" title="contact-info" numcolumns="12">
            <column name="email" numcolumns="6" order="100">
                <widget type="email" fieldname="email" />
            </column>
            <column name="phone" numcolumns="6" order="110">
                <widget type="tel" fieldname="telefono" />
            </column>
        </group>
    </columns>
    <rows>
        <row type="statistics">
            <datalabel icon="fa-solid fa-file" label="documents" function="countDocuments" />
        </row>
    </rows>
</view>
```

### Caso de Uso 3: Tablas Editable (Líneas de Documentos)

Para mostrar un tabla dentro de un formulario (como líneas en una factura):

```php
// En el controlador, crear una vista adicional
protected function createViews()
{
    parent::createViews();
    $this->createViewEdit('EditMiModelo');
    $this->createViewList('ListMiModelo', 'MiModelo');  // Tabla dentro del Edit
}
```

Luego en la plantilla Twig:
```twig
{# Ver líneas como tabla editable #}
{{ include('Master/EditListView.html.twig') }}
```

### Caso de Uso 4: Relaciones Entre Documentos

Enlazar un cliente a partir del listado:

```xml
<column name="customer" order="100">
    <widget type="autocomplete" fieldname="codcliente" strict="true" 
            onclick="EditCliente" icon="fa-solid fa-user">
        <values source="clientes" fieldcode="codcliente" fieldtitle="nombre" />
    </widget>
</column>
```

---

## APENDICE E: Códigos de Colores Bootstrap

FacturaScripts utiliza las clases de color estándar de Bootstrap:

**Para filas de status:**
- `danger`: `class="table-danger"` - Fondo rojo
- `success`: `class="table-success"` - Fondo verde
- `warning`: `class="table-warning"` - Fondo naranja/amarillo
- `info`: `class="table-info"` - Fondo azul claro
- `dark`: `class="table-dark"` - Fondo gris oscuro
- `secondary`: `class="table-secondary"` - Fondo gris
- `primary`: `class="table-primary"` - Fondo azul primario
- `light`: `class="table-light"` - Fondo blanco/gris muy claro

**Para texto en opciones:**
- `text-danger`, `text-success`, `text-warning`, etc.

**Para botones en estadísticas:**
- `btn-danger`, `btn-success`, `btn-warning`, `btn-info`, etc.

---

## APENDICE F: Recursos de Traducción

Los textos en XMLViews se traducen automáticamente. Para agregar traducciones personalizadas:

**Crear archivo:** `Plugins/MiPlugin/Translation/es_ES.json`

```json
{
    "my-custom-label": "Mi Etiqueta Personalizada",
    "my-custom-description": "Descripción del campo personalizado",
    "column-my-field": "Mi Campo",
    "group-my-group": "Mi Grupo",
    "row-status": "Estado del Registro"
}
```

Luego usar en XMLView:
```xml
<column name="my-field" order="100">
    <widget type="text" fieldname="campo" />
</column>
<!-- Se traduce como "column-my-field" automáticamente -->
```

---

**DOCUMENTO COMPLETADO**  
Última actualización: 12 de abril de 2026  
Versión: FacturaScripts 2025.001

