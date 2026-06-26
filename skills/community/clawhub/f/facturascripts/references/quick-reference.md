# FacturaScripts 2025 - Referencia Rápida de Controladores

Guía de referencia rápida para desarrolladores de FacturaScripts.

---

## JERARQUIA DE CLASES

```
Controller (Base de FacturaScripts)
    └── BaseController (Controlador abstracto base)
        ├── ListController (Listados de datos)
        │   └── ListBusinessDocument (Documentos comerciales)
        ├── PanelController (Pestañas/Paneles)
        │   ├── EditController (Editar un registro)
        │   │   └── ComercialContactController (Contactos comerciales)
        │   └── SalesController (Documentos de venta AJAX)
        │       └── PurchasesController (Documentos de compra AJAX)
```

---

## METODOS PRINCIPALES POR CLASE

### BaseController

**Abstractos (Obligatorios)**:
- `createViews(): void` - Crear vistas
- `loadData($viewName, $view): void` - Cargar datos

**Principales**:
- `tab($viewName): BaseView` - Acceder a vista
- `listView($viewName): ListView` - Acceder a ListView
- `addButton($viewName, $btnArray): BaseView` - Agregar botón
- `getPageData(): array` - Información de página (heredado)
- `deleteAction(): bool` - Eliminar registros
- `autocompleteAction(): array` - Autocompletado

### ListController

**Abstractos (Heredados)**:
- `createViews()` - Implementar
- `loadData()` - Implementar típicamente como: `parent::loadData()`

**Crear Vistas**:
- `addView($viewName, $modelName, $title, $icon): ListView` - Crear ListView

**Agregar Filtros**:
- `addFilterAutocomplete($viewName, $key, $label, $field, $table, ...)`
- `addFilterCheckbox($viewName, $key, $label, $field, $operation, $matchValue)`
- `addFilterDatePicker($viewName, $key, $label, $field, $operation)`
- `addFilterNumber($viewName, $key, $label, $field, $operation)`
- `addFilterPeriod($viewName, $key, $label, $field, $dateTime)`
- `addFilterSelect($viewName, $key, $label, $field, $values)`
- `addFilterSelectWhere($viewName, $key, $values, $label)`

**Búsqueda y Orden**:
- `addSearchFields($viewName, $fields): ListView` - Campos para buscar
- `addOrderBy($viewName, $fields, $label, $default): ListView` - Opción de orden

**Personalización**:
- `addColor($viewName, $fieldName, $value, $color, $title): ListView` - Colorear filas

### PanelController

**Crear Vistas**:
- `addEditView($viewName, $modelName, $title, $icon): EditView`
- `addListView($viewName, $modelName, $title, $icon): ListView`
- `addEditListView($viewName, $modelName, $title, $icon): EditListView`
- `addHtmlView($viewName, $fileName, $modelName, $title, $icon): HtmlView`

**Configuración**:
- `setTabsPosition($position): void` - Posición de pestañas (left, bottom, top, left-bottom)

### EditController

**Abstracto (Obligatorio)**:
- `getModelClassName(): string` - Nombre del modelo (ej: 'Cliente')

**Principales**:
- `getModel(): ModelClass` - Obtener modelo de vista principal

---

## VISTA RÁPIDA DE ACCIONES COMUNES

### En ListController

```php
protected function createViews()
{
    // Crear vista
    $this->addView('ListMiModelo', 'MiModelo', 'Mi Listado');
    
    // Búsqueda
    $this->addSearchFields('ListMiModelo', ['nombre', 'codigo']);
    
    // Filtros
    $this->addFilterSelect('ListMiModelo', 'estado', 'Estado', 
        'estado', ['activo' => 'Activo', 'inactivo' => 'Inactivo']);
    $this->addFilterDatePicker('ListMiModelo', 'desde', 'Desde', 'fecha', '>=');
    
    // Orden
    $this->addOrderBy('ListMiModelo', ['nombre'], 'Nombre');
    $this->addOrderBy('ListMiModelo', ['fecha'], 'Fecha', 2);
    
    // Color
    $this->addColor('ListMiModelo', 'estado', 'inactivo', 'danger');
}

protected function loadData($viewName, $view)
{
    parent::loadData($viewName, $view);
}
```

### En PanelController

```php
protected function createViews()
{
    $this->setTabsPosition('left');
    
    $this->addEditView('EditPrincipal', 'MiModelo', 'Principal');
    $this->addListView('ListSecundario', 'ItemRelacionado', 'Items');
    $this->addHtmlView('ViewPersonalizado', 'MiModelo/custom', 'MiModelo', 'Custom');
}

protected function loadData($viewName, $view)
{
    if ($viewName === 'EditPrincipal') {
        $codigo = $this->request->query('code', '');
        $view->loadData($codigo);
    } elseif ($this->hasData) {
        $codigo = $this->getModel()->primaryColumnValue();
        $view->loadData($codigo);
    }
}
```

### En EditController

```php
public function getModelClassName(): string
{
    return 'MiModelo';
}

public function getPageData(): array
{
    $data = parent::getPageData();
    $data['title'] = 'Mi Modelo';
    $data['menu'] = 'ventas';
    $data['icon'] = 'fas fa-cube';
    return $data;
}

protected function createViews()
{
    parent::createViews(); // Crea automáticamente vista principal
    
    // Agregar vistas adicionales si es necesario
    $this->addListView('ListItems', 'Item', 'Items');
}
```

---

## OPERADORES DE FILTRO

| Operador | Significado | Uso |
|----------|-------------|-----|
| `=` | Igual | campo = valor |
| `!=` | No igual | campo != valor |
| `>` | Mayor que | campo > valor |
| `<` | Menor que | campo < valor |
| `>=` | Mayor o igual | campo >= valor |
| `<=` | Menor o igual | campo <= valor |
| `LIKE` | Contiene | campo LIKE '%valor%' |
| `NOT LIKE` | No contiene | campo NOT LIKE '%valor%' |
| `IN` | En lista | campo IN (v1, v2, v3) |
| `NOT IN` | No en lista | campo NOT IN (v1, v2, v3) |
| `IS` | Es NULL | campo IS NULL |
| `IS NOT` | No es NULL | campo IS NOT NULL |
| `OR` | Condición OR | (cond1 OR cond2) |

---

## CONFIGURACION DE VISTA (settings)

```php
$view->setSettings($property, $value)

// Propiedades disponibles:
'active'        => bool    // Mostrar/ocultar vista
'btnDelete'     => bool    // Botón eliminar
'btnNew'        => bool    // Botón nuevo
'btnPrint'      => bool    // Botón imprimir
'btnSave'       => bool    // Botón guardar
'btnUndo'       => bool    // Botón deshacer
'btnOptions'    => bool    // Menú opciones
'card'          => bool    // Mostrar como tarjeta
'checkBoxes'    => bool    // Casillas de selección
'clickable'     => bool    // Filas clickables
'customized'    => bool    // Columnas personalizadas
'itemLimit'     => int     // Items por página
'megasearch'    => bool    // En megabúsqueda
'saveFilters'   => bool    // Guardar filtros usuario
```

---

## EJEMPLOS DE FILTROS

### SelectWhere (Filtro Avanzado)

```php
$values = [
    [
        'label' => 'Solo activos',
        'where' => [new DataBaseWhere('activo', true)]
    ],
    [
        'label' => 'Solo suspendidos',
        'where' => [new DataBaseWhere('suspendido', true)]
    ],
    [
        'label' => 'Todos',
        'where' => []
    ]
];
$this->addFilterSelectWhere('ListMiModelo', 'estado', $values);
```

### Filtro de Rango (Múltiples condiciones)

```php
$where = [
    new DataBaseWhere('precio', 100, '>='),
    new DataBaseWhere('precio', 500, '<=')
];
// Se aplica: precio >= 100 AND precio <= 500
```

### Filtro de Período

```php
$this->addFilterPeriod('ListVentas', 'periodo', 'Período', 'fecha', false);
// Genera: Hoy, Ayer, Última semana, Último mes, etc.
```

---

## FLUJOS DE EJECUCION

### ListController (privateCore)

```
1. Obtiene acción del request
2. Ejecuta execPreviousAction($action)
   - 'autocomplete' -> JSON de resultados
   - 'clear-filters' -> Limpia filtros
   - 'delete' -> Elimina registros
   - 'delete-filter' -> Elimina filtro guardado
   - 'save-filter' -> Guarda filtro actual
3. Para cada vista:
   - processFormData() (load, preload)
   - loadData()
4. Ejecuta execAfterAction($action)
   - 'delete-ok' -> Mensaje
   - 'export' -> Exporta datos
   - 'megasearch' -> Búsqueda global
```

### PanelController (privateCore)

```
1. Obtiene acción del request
2. Ejecuta execPreviousAction($action)
3. Para cada vista:
   - Si es secundaria y sin datos de principal, desactiva
   - processFormData() (load, preload)
   - loadData()
   - Si es principal con datos, activa vistas secundarias
4. Ejecuta execAfterAction($action)
```

### EditController (heredado de PanelController)

```
Similar a PanelController pero:
- Vista principal: Carga modelo por código
- Otras vistas: Se activan si existe dato principal
- Soporta cambio de clave primaria
```

---

## PERMISOS Y SEGURIDAD

### Verificar Permisos

```php
$this->permissions->allowCreate    // Crear registros
$this->permissions->allowDelete    // Eliminar registros
$this->permissions->allowExport    // Exportar datos
$this->permissions->allowUpdate    // Actualizar registros
$this->permissions->onlyOwnerData  // Solo datos del usuario
```

### Validar Token CSRF

```php
if (false === $this->validateFormToken()) {
    return false;
}
```

### Verificar Propietario

```php
if (false === $this->checkOwnerData($model)) {
    $this->setTemplate('Error/AccessDenied');
    return;
}
```

---

## CONSTANTES UTILES

```php
FS_ITEM_LIMIT               // Límite de items por página (config)
self::MODEL_NAMESPACE       // Namespace de modelos
static::DEFAULT_TEMPLATE    // Template por defecto de vista
```

---

## ARCHIVOS IMPORTANTES

### Directorios

- `/Core/Lib/ExtendedController/` - Clases base de controladores
- `/Core/Lib/ListFilter/` - Tipos de filtros
- `/Core/Lib/AjaxForms/` - Formularios AJAX para documentos
- `/Core/Controller/` - Todos los controladores del core

### Clases Base

- `BaseController.php` - Clase abstracta base
- `ListController.php` - Lista de datos
- `PanelController.php` - Pestañas/Paneles
- `EditController.php` - Editar registro
- `BaseView.php` - Vista abstracta
- `ListView.php` - Vista de listado
- `EditView.php` - Vista de edición
- `EditListView.php` - Vista editable
- `HtmlView.php` - Vista HTML personalizada

### Filtros

- `BaseFilter.php` - Filtro abstracto
- `AutocompleteFilter.php` - Autocompletado
- `CheckboxFilter.php` - Booleano
- `DateFilter.php` - Fecha
- `NumberFilter.php` - Número
- `PeriodFilter.php` - Período
- `SelectFilter.php` - Selección
- `SelectWhereFilter.php` - Selección con WHERE

---

## LOGGING Y DEBUGGING

### Registrar Mensajes

```php
Tools::log()->critical($message);  // Crítico
Tools::log()->error($message);     // Error
Tools::log()->warning($message);   // Advertencia
Tools::log()->notice($message);    // Aviso
Tools::log()->info($message);      // Información
```

### Traducción

```php
Tools::trans('translation-key')    // Obtener traducción
Tools::trans('key', ['%var%' => 'value'])  // Con variables
```

---

## OPERADORES EN URL

Al acceder a controladores via URL:

```
/index.php?page=MiControlador
  &activetab=ListaView          // Pestaña activa
  &code=123                       // Código del registro
  &action=delete                  // Acción a ejecutar
  &sortby=nombre                  // Campo de ordenamiento
  &updown=DESC                    // Dirección orden (ASC/DESC)
  &offset=100                     // Desplazamiento paginación
  &limit=50                       // Límite de registros
```

---

## EVENTOS Y HOOKS (Pipes)

```php
$this->pipe('createViews');
$this->pipe('loadData', $viewName, $view);
$this->pipe('execPreviousAction', $action);
$this->pipe('execAfterAction', $action);
```

Los plugins pueden enganchar estos eventos.

---

## TIPS Y TRUCOS

1. **Búsqueda en campos numéricos**: Usar `CAST(campo AS CHAR(50))`
2. **Múltiples condiciones**: Agregar múltiples `DataBaseWhere` al array
3. **Datos del usuario**: Acceder con `$this->user`
4. **Modelo actual**: `$this->getModel()` en EditController
5. **Vista actual**: `$this->getCurrentView()` o `$this->views[$this->active]`
6. **Encadenamiento**: Los métodos retornan `$this` o el objeto para encadenar

---

## CHECKLIST CREAR CONTROLADOR

- [ ] Extender clase base (List/Edit/Panel/SalesController)
- [ ] Implementar métodos abstractos (createViews, loadData)
- [ ] Implementar getPageData() con title, menu, icon
- [ ] Crear vistas con addView/addEditView/etc
- [ ] Agregar filtros si es necesario
- [ ] Agregar búsqueda si es necesario
- [ ] Configurar permisos y seguridad
- [ ] Registrar en controllers.xml (si es plugin)
- [ ] Probar con diferentes niveles de permisos
- [ ] Documentar en código
- [ ] Agregar traducciones

---

**Referencia Rápida - FacturaScripts 2025**
**Versión: 1.0**
**Fecha: Abril 2026**
