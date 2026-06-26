# FacturaScripts 2025 - Referencia Exhaustiva de Controladores

Documento de referencia completo para FacturaScripts 2025 (v2025) que documenta todos los controladores del core, arquitectura de extensión y sistema de vistas.

---

## INDICE DE CONTENIDOS

1. [Arquitectura de Controladores Extendidos](#arquitectura)
2. [Sistema de Vistas](#sistema-vistas)
3. [Sistema de Filtros](#sistema-filtros)
4. [AjaxForms para Documentos Comerciales](#ajaxforms)
5. [Controladores del Core por Categoría](#controladores-core)
6. [Como Crear un Nuevo Controlador](#crear-controlador)

---

## ARQUITECTURA DE CONTROLADORES EXTENDIDOS {#arquitectura}

### Conceptos Fundamentales

FacturaScripts utiliza un sistema jerárquico de controladores para gestionar la presentación y lógica de negocio:

- **BaseController**: Clase abstracta base que implementa funcionalidad común
- **ListController**: Extiende BaseController para mostrar listados de datos
- **PanelController**: Extiende BaseController para mostrar datos en pestañas/paneles
- **EditController**: Extiende PanelController para editar registros individuales
- **ListBusinessDocument**: Extiende ListController para documentos comerciales
- **ComercialContactController**: Extiende EditController para contactos comerciales

### BaseController: Propiedades y Métodos Principales

#### Propiedades Publicas

```
public $active: string
  - Nombre de la pestaña/vista activa actualmente mostrada

public $views: BaseView[]
  - Array asociativo de vistas gestionadas por el controlador
  - Clave: nombre de la vista (string)
  - Valor: objeto BaseView (ListView, EditView, EditListView, HtmlView)

public $codeModel: CodeModel
  - Modelo para búsquedas de autocomplete y select
  - Utilizado por filtros y widgets de selección

public $exportManager: ExportManager
  - Gestor para exportar datos a diferentes formatos (PDF, CSV, Excel)
```

#### Métodos Abstractos (deben implementarse en clases hijas)

```php
abstract protected function createViews(): void
  - Propósito: Definir y agregar todas las vistas del controlador
  - Llamada: En privateCore() de BaseController
  - Ejemplo: $this->addView('ListCliente', 'Cliente', 'Clientes');
  
abstract protected function loadData($viewName, $view): void
  - Parámetros:
    * string $viewName: Nombre de la vista a cargar
    * BaseView $view: Objeto de la vista
  - Propósito: Cargar datos en la vista especificada
  - Implementación típica: $view->loadData($code, $where, $order);
```

#### Métodos Publicos Principales

```php
public function __construct(string $className, string $uri = '')
  - Inicializa el controlador
  - Parámetros:
    * string $className: Nombre de la clase del controlador
    * string $uri: URI (opcional)
  - Inicializa: $this->active, $this->codeModel, $this->exportManager

public function tab(string $viewName): BaseView
  - Accede a una vista por nombre
  - Lanza Exception si la vista no existe
  - Retorna: BaseView

public function listView(string $viewName): ListView
  - Accede a una ListView específicamente
  - Verifica que sea instancia de ListView
  - Retorna: ListView
  - Lanza: Exception si no es ListView

public function addCustomView(string $viewName, BaseView $view): BaseView
  - Agrega una vista personalizada al controlador
  - Parámetros:
    * string $viewName: Identificador único de la vista
    * BaseView $view: Objeto de vista (ListView, EditView, etc.)
  - Verifica que $viewName coincida con $view->name
  - Retorna: BaseView (la vista agregada)

public function addButton(string $viewName, array $btnArray): BaseView
  - Agrega un botón a una vista
  - Parámetros:
    * string $viewName: Nombre de la vista destino
    * array $btnArray: Configuración del botón
      - 'name' (string): Nombre del botón
      - 'icon' (string): Clase de icono
      - 'label' (string): Etiqueta visible
      - 'action' (string): Acción a ejecutar
      - 'row' (opcional): Si está presente, botón en pie de página
  - Retorna: BaseView

public function getCurrentView(): BaseView
  - Obtiene la vista actualmente siendo procesada
  - Retorna: BaseView

public function getMainViewName(): string
  - Obtiene el nombre de la vista principal (primera agregada)
  - Retorna: string (nombre de vista) o '' si no hay vistas

public function getSettings(string $viewName, string $property): mixed
  - Obtiene valor de configuración de una vista
  - Parámetros:
    * string $viewName: Nombre de la vista
    * string $property: Nombre de la propiedad
  - Retorna: mixed (null si no existe)

public function setSettings(string $viewName, string $property, $value): BaseView
  - Establece configuración de una vista
  - Retorna: BaseView para encadenamiento de métodos

public function getViewModelValue(string $viewName, string $fieldName): mixed
  - Obtiene valor de un campo del modelo de una vista
  - Parámetros:
    * string $viewName: Nombre de la vista
    * string $fieldName: Nombre del campo del modelo
  - Retorna: mixed (null si no existe)

public function setCurrentView(string $viewName): void
  - Establece qué vista se está procesando actualmente
```

#### Métodos Protegidos para Acciones

```php
protected function deleteAction(): bool
  - Elimina registros
  - Verifica permisos: permissions->allowDelete
  - Verifica token de formulario
  - Soporta eliminación múltiple (array 'codes') y simple ('code')
  - Retorna: bool (éxito o fallo)

protected function exportAction(): void
  - Exporta datos de vista activa
  - Verifica: settings['btnPrint'] y permissions->allowExport
  - Parámetros desde request:
    * 'option': Formato de exportación
    * 'idformat': ID de formato (para PDF)
    * 'langcode': Código de idioma
  - Utiliza: $this->exportManager

protected function autocompleteAction(): array
  - Acción para autocompletado en campos
  - Parámetros esperados (via request):
    * 'field': Campo del formulario
    * 'source': Tabla a buscar
    * 'fieldcode': Campo código en tabla
    * 'fieldtitle': Campo descripción en tabla
    * 'term': Término de búsqueda
    * 'strict': Si solo valores exactos (0=permisivo, 1=estricto)
  - Retorna: array [['key' => código, 'value' => descripción], ...]

protected function selectAction(): array
  - Acción para SELECT en campos
  - Similar a autocompleteAction pero para listas completas
  - Retorna: array de resultados

protected function datalistAction(): array
  - Acción para datalist HTML5
  - Retorna: array de resultados
```

#### Métodos Protegidos Utilitarios

```php
protected function requestGet(array $keys): array
  - Obtiene múltiples parámetros de request
  - Parámetros:
    * array $keys: Lista de nombres de parámetros
  - Retorna: array con los parámetros solicitados

protected function checkOwnerData($model): bool
  - Verifica si usuario es propietario de datos
  - Valida: permissions->onlyOwnerData
  - Comprueba: $model->nick o $model->codagente
  - Retorna: bool (tiene permiso)

protected function getAutocompleteValues(string $viewName, string $fieldName): array
  - Obtiene valores predefinidos de un widget
  - Retorna: array de valores [['key' => x, 'value' => y], ...]
```

---

### ListController: Controlador de Listados

Extiende **BaseController** para mostrar datos en formato de tabla con filtros y paginación.

#### Flujo de Ejecución en privateCore()

1. Obtiene acción: `$action = $this->request->inputOrQuery('action', '')`
2. Ejecuta **execPreviousAction($action)** - acciones antes de cargar datos
3. Para cada vista:
   - Si es la vista activa: `$view->processFormData($this->request, 'load')`
   - Si no: `$view->processFormData($this->request, 'preload')`
   - Llama: `$this->loadData($viewName, $view)`
4. Ejecuta **execAfterAction($action)** - acciones después de cargar datos

#### Acciones Ejecutadas

**execPreviousAction($action): bool**
- 'autocomplete': Devuelve JSON con resultados de autocompletado
- 'clear-filters': Limpia filtros guardados
- 'delete': Elimina registros
- 'delete-filter': Elimina filtro guardado
- 'save-filter': Guarda filtro actual

**execAfterAction($action)**
- 'delete-ok': Muestra mensaje de éxito en eliminación
- 'export': Exporta datos
- 'megasearch': Realiza búsqueda mega

#### Métodos para Crear Vistas

```php
protected function addView(string $viewName, string $modelName, 
                          string $viewTitle = '', string $icon = ''): ListView
  - Crea y agrega una ListView al controlador
  - Parámetros:
    * string $viewName: Identificador (ej: 'ListCliente')
    * string $modelName: Clase modelo sin namespace (ej: 'Cliente')
    * string $viewTitle: Título mostrado (usa $this->title si vacío)
    * string $icon: Icono FontAwesome
  - Configuración automática:
    * btnPrint = true
    * card = false
    * megasearch = true
    * saveFilters = true
  - Retorna: ListView
```

#### Métodos para Agregar Filtros

```php
protected function addFilterAutocomplete(string $viewName, string $key, 
                                        string $label, string $field, 
                                        string $table, string $fieldcode = '', 
                                        string $fieldtitle = '', 
                                        array $where = []): ListView
  - Filtro con autocompletado (busca en otra tabla)
  - Parámetros:
    * key: Identificador del filtro
    * label: Etiqueta visible
    * field: Campo del modelo a filtrar
    * table: Tabla para búsqueda
    * fieldcode: Campo de código (uses codeModel)
    * fieldtitle: Campo de descripción
    * where: Condiciones adicionales

protected function addFilterCheckbox(string $viewName, string $key, 
                                     string $label = '', string $field = '', 
                                     string $operation = '=', $matchValue = true, 
                                     array $default = []): ListView
  - Filtro de casilla de verificación (booleano)
  - Parámetros:
    * key: Identificador del filtro
    * label: Etiqueta visible
    * field: Campo del modelo
    * operation: Operación ('=', '!=', etc.)
    * matchValue: Valor cuando está marcado

protected function addFilterDatePicker(string $viewName, string $key, 
                                       string $label = '', string $field = '', 
                                       string $operation = '>='): ListView
  - Filtro de fecha con calendario
  - operation: '>=', '<=', '>', '<', '=', '!='

protected function addFilterNumber(string $viewName, string $key, 
                                   string $label = '', string $field = '', 
                                   string $operation = '>='): ListView
  - Filtro numérico (enteros y decimales)

protected function addFilterPeriod(string $viewName, string $key, 
                                   string $label, string $field, 
                                   bool $dateTime = false): ListView
  - Filtro de período (período predefinido + fecha inicio/fin)
  - Períodos: Hoy, Ayer, Última semana, Último mes, etc.
  - dateTime: true si incluye hora

protected function addFilterSelect(string $viewName, string $key, 
                                   string $label, string $field, 
                                   array $values = []): ListView
  - Filtro de selección estática
  - Parámetros:
    * values: Array de opciones ['valor' => 'Etiqueta', ...]

protected function addFilterSelectWhere(string $viewName, string $key, 
                                        array $values, string $label = ''): ListView
  - Filtro con condiciones WHERE personalizadas
  - values estructura:
    [
      ['label' => 'Solo activos', 'where' => [new DataBaseWhere('suspended', false)]],
      ['label' => 'Solo suspendidos', 'where' => [new DataBaseWhere('suspended', true)]],
      ['label' => 'Todos', 'where' => []]
    ]
```

#### Métodos para Búsqueda y Orden

```php
protected function addSearchFields(string $viewName, array $fields): ListView
  - Define campos donde se busca con megabúsqueda
  - Parámetros:
    * fields: Array de campos del modelo
  - Nota: Para campos numéricos usar CAST(columnName AS CHAR(50))

protected function addOrderBy(string $viewName, array $fields, 
                              string $label = '', int $default = 0): ListView
  - Opción de ordenamiento disponible
  - Parámetros:
    * fields: Array con campos para ordenar
    * label: Etiqueta mostrada
    * default: 0=sin orden, 1=ASC, 2=DESC
  - Retorna: ListView
```

#### Métodos para Personalizar Listado

```php
protected function addColor(string $viewName, string $fieldName, 
                           $value, string $color, string $title = ''): ListView
  - Agrega color a filas según valor de campo
  - Parámetros:
    * fieldName: Campo a evaluar
    * value: Valor que activa el color
    * color: Clase de color ('success', 'danger', 'warning', etc.)
    * title: Título del tooltip
```

#### Métodos para Gestionar Filtros

```php
protected function clearFiltersAction(): void
  - Limpia todos los filtros guardados
  - Elimina de caché y request

protected function deleteFilterAction(): void
  - Elimina un filtro guardado específico
  - Parámetro request: 'loadfilter' (ID del filtro)

protected function saveFilterAction(): void
  - Guarda configuración de filtros actual
  - Almacena en base de datos (PageFilter)
```

#### Método para Cargar Datos

```php
protected function loadData($viewName, $view)
  - Implementación base en ListController:
    * Obtiene filtro de propietario si permissions->onlyOwnerData
    * Llama: $view->loadData('', $where)
  - Puede ser sobrescrito en controladores específicos
```

#### Método para Búsqueda Global

```php
protected function megaSearchAction(): void
  - Busca en todas las vistas que tengan searchFields
  - Retorna JSON con resultados
  - Configurable: setSettings($viewName, 'megasearch', true/false)
```

---

### PanelController: Controlador con Pestañas

Extiende **BaseController** para mostrar múltiples vistas en pestañas/paneles.

#### Propiedades Principales

```
public $hasData: bool
  - Indica si la vista principal tiene datos
  - Usado para habilitar/deshabilitar vistas secundarias

public $tabsPosition: string
  - Posición de las pestañas: 'left' (default), 'bottom', 'top', 'left-bottom'
  - Afecta template y stilos
```

#### Flujo de Ejecución

1. Obtiene acción
2. Ejecuta **execPreviousAction($action)**
3. Para cada vista:
   - Si es secundaria y $hasData=false, desactiva la vista
   - Si vista está activa: procesa como 'load'
   - Si no: procesa como 'preload'
   - Llama: $this->loadData($viewName, $view)
   - Si es vista principal y existe modelo, $hasData=true
4. Ejecuta **execAfterAction($action)**

#### Métodos para Crear Vistas

```php
protected function addEditView(string $viewName, string $modelName, 
                              string $viewTitle, string $viewIcon = ''): EditView
  - Crea una vista de edición
  - Parámetros: viewName, modelName (sin namespace), titulo, icono
  - Retorna: EditView
  - Configuración automática de card según tabsPosition

protected function addListView(string $viewName, string $modelName, 
                              string $viewTitle, string $viewIcon = ''): ListView
  - Crea una vista de listado dentro del panel
  - Retorna: ListView

protected function addEditListView(string $viewName, string $modelName, 
                                   string $viewTitle, string $viewIcon = ''): EditListView
  - Crea una vista editable en línea (tabla con edición inline)
  - Retorna: EditListView

protected function addHtmlView(string $viewName, string $fileName, 
                              string $modelName, string $viewTitle, 
                              string $viewIcon = ''): HtmlView
  - Crea una vista HTML personalizada
  - Parámetros:
    * fileName: Archivo Twig dentro de Resources/templates
  - Retorna: HtmlView
```

#### Métodos de Configuración

```php
public function setTabsPosition(string $position): void
  - Establece posición de pestañas
  - Valores: 'left' (default), 'bottom', 'top', 'left-bottom'
  - Cambia automáticamente el template
  - Ajusta configuración 'card' de vistas

public function getImageUrl(): string
  - Obtiene URL de imagen para mostrar
  - Implementación base retorna string vacío
  - Puede sobrescribirse en subclases
```

#### Métodos de Edición

```php
protected function editAction(): bool
  - Ejecuta acción de guardar edición
  - Pasos:
    1. Verifica permissions->allowUpdate
    2. Valida token de formulario
    3. Carga modelo desde código
    4. Procesa datos de formulario
    5. Maneja cambios en clave primaria
    6. Guarda modelo
  - Retorna: bool (éxito)

protected function saveAction(): bool
  - Ejecuta acción de guardar nuevo registro
  - Similar a editAction pero para creación

protected function newAction(): bool
  - Prepara para crear nuevo registro
  - Limpia modelo
  - Permite introducir datos iniciales
```

---

### EditController: Controlador de Edición

Extiende **PanelController** para editar un registro individual.

#### Métodos Abstractos

```php
abstract public function getModelClassName(): string
  - Retorna nombre de la clase del modelo (sin namespace)
  - Ejemplo: 'Cliente', 'Proveedor', etc.
```

#### Métodos Principales

```php
public function getModel()
  - Obtiene referencia al modelo de la vista principal
  - Retorna: ModelClass

public function getPageData(): array
  - Obtiene datos de página (heredado de Controller)
  - Establece: showonmenu = false (no mostrar en menú)
  - Retorna: array con configuración

public function createViews()
  - Implementación automática:
    * Obtiene nombre modelo: getModelClassName()
    * Crea viewName: 'Edit' + ModelClassName
    * Crea EditView
    * Habilita btnPrint
```

#### Flujo de Carga de Datos

```
loadData() recibe:
  - viewName: nombre de la vista
  - view: objeto BaseView

En vista principal:
  - Obtiene código: request->input() o request->query()
  - Llama: view->loadData($code)
  - Verifica: checkOwnerData()
  - Si acción vacía y código existe pero modelo no, muestra error
  - Actualiza título con descripción del modelo

En otras vistas:
  - Carga normalmente sus datos
```

---

### ListBusinessDocument: Controlador de Documentos Comerciales

Extiende **ListController** para gestionar documentos (facturas, pedidos, albaranes, etc.).

Proporciona funcionalidad específica para:
- Gestión de estados de documento
- Acciones comerciales (cambiar estado, duplicar, etc.)
- Filtros específicos de documentos
- Integración con numeración

---

### ComercialContactController: Controlador de Contactos Comerciales

Extiende **EditController** para gestionar contactos de clientes/proveedores.

Características:
- Edición de datos de contacto
- Vistas secundarias para información relacionada
- Validación de datos comerciales

---

## SISTEMA DE VISTAS {#sistema-vistas}

### BaseView: Clase Base de Vistas

Clase abstracta que define interfaz común para todas las vistas.

#### Propiedades Principales

```
public $name: string
  - Identificador único de la vista

public $title: string
  - Título mostrado en pestaña

public $icon: string
  - Clase de icono FontAwesome

public $model: ModelClass
  - Instancia del modelo asociado

public $template: string
  - Template Twig a renderizar (default: Master/BaseView.html.twig)

public $cursor: array
  - Array de modelos cargados para mostrar

public $count: int
  - Total de registros que coinciden con filtros

public $offset: int
  - Desplazamiento en paginación (fila inicial)

public $order: array
  - Configuración de ordenamiento aplicado

public $where: DataBaseWhere[]
  - Condiciones WHERE para filtrar datos

public $settings: array
  - Configuración de la vista:
    * active (bool): Vista visible y activa
    * btnDelete (bool): Mostrar botón eliminar
    * btnNew (bool): Mostrar botón nuevo
    * btnPrint (bool): Mostrar botón imprimir
    * btnSave (bool): Mostrar botón guardar
    * btnUndo (bool): Mostrar botón deshacer
    * btnOptions (bool): Mostrar menú opciones
    * card (bool): Mostrar como tarjeta
    * checkBoxes (bool): Mostrar casillas de selección
    * clickable (bool): Filas son clickables
    * customized (bool): Columnas personalizadas
    * itemLimit (int): Items por página
    * megasearch (bool): Incluir en megabúsqueda
    * saveFilters (bool): Guardar filtros usuario

public $pageOption: PageOption
  - Configuración de columnas y opciones de página
```

#### Métodos Abstractos

```php
abstract public function loadData($code = '', $where = [], $order = [], 
                                  $offset = 0, $limit = 0): void
  - Carga datos del modelo según parámetros
  - Debe llenar: $this->cursor, $this->count, $this->where

abstract public function processFormData($request, $case): void
  - Procesa datos de formulario
  - $case: 'load' (cargar vista), 'preload' (precarga), 'edit' (guardar), 'delete' (borrar)

abstract public function export(&$exportManager, $codes): bool
  - Exporta datos a formato especificado
  - Retorna: bool (éxito)
```

#### Métodos Publicos de Configuración

```php
public function getViewName(): string
  - Retorna nombre/identificador de la vista

public function setSettings(string $property, $value): BaseView
  - Establece configuración de la vista
  - Retorna: $this (para encadenamiento)

public function getColumns(): GroupItem[]
  - Retorna columnas visibles configuradas
  - GroupItem contiene ColumnItem

public function getRows(): array
  - Retorna filas configuradas (acciones, pie de página, etc.)

public function getRow(string $type): VisualItem|null
  - Obtiene fila de tipo especificado
  - Tipos: 'header', 'footer', 'actions'

public function columnForField(string $fieldName): ColumnItem|null
  - Obtiene columna para un campo del modelo

public function columnModalForName(string $columnName): ColumnItem|null
  - Obtiene columna para mostrar en modal
```

#### Métodos Publicos de Utilidad

```php
public function loadPageOptions($user): void
  - Carga opciones de página guardadas del usuario
  - Personalización de columnas, filtros, etc.

public function getPageOption(): PageOption
  - Obtiene objeto de opciones de página
```

---

### ListView: Vista de Listado

Extiende **BaseView** para mostrar datos en forma de tabla.

#### Propiedades Específicas

```
public $filters: BaseFilter[]
  - Array de filtros disponibles para esta vista

public $searchFields: array
  - Campos donde busca la megabúsqueda

public $orderBy: array
  - Opciones de ordenamiento disponibles

public $colors: array
  - Colores para filas según condiciones
```

#### Métodos de Filtrado

```php
public function addFilterAutocomplete(string $key, string $label, 
                                      string $field, string $table, 
                                      string $fieldcode = '', 
                                      string $fieldtitle = ''): self
  - Agrega filtro de autocompletado
  - Retorna: $this

public function addFilterCheckbox(string $key, string $label = '', 
                                  string $field = '', string $operation = '=', 
                                  $matchValue = true): self
  - Agrega filtro checkbox

public function addFilterDatePicker(string $key, string $label = '', 
                                    string $field = '', 
                                    string $operation = '>='): self
  - Agrega filtro de fecha

public function addFilterNumber(string $key, string $label = '', 
                                string $field = '', 
                                string $operation = '>='): self
  - Agrega filtro numérico

public function addFilterPeriod(string $key, string $label, 
                                string $field, bool $dateTime = false): self
  - Agrega filtro de período

public function addFilterSelect(string $key, string $label, 
                                string $field, array $values = []): self
  - Agrega filtro de selección

public function addFilterSelectWhere(string $key, array $values, 
                                     string $label = ''): self
  - Agrega filtro con condiciones WHERE personalizadas
```

#### Métodos de Búsqueda y Orden

```php
public function addSearchFields(array $fields): self
  - Define campos para megabúsqueda

public function addOrderBy(array $fields, string $label = '', 
                          int $default = 0): self
  - Agrega opción de ordenamiento
  - default: 0=sin orden, 1=ASC, 2=DESC
```

#### Métodos de Personalización

```php
public function addColor(string $fieldName, $value, string $color, 
                        string $title = ''): self
  - Agrega color condicional a fila

public function deletePageFilter(int $id): bool
  - Elimina filtro guardado

public function savePageFilter($request, $user): string
  - Guarda filtro actual
  - Retorna: ID del filtro guardado
```

---

### EditView: Vista de Edición

Extiende **BaseView** para mostrar formulario de edición.

Características:
- Formulario de edición de un registro
- Validación de datos
- Guardado de cambios
- Generación de clave primaria si es necesario

---

### EditListView: Vista de Lista Editable

Extiende **BaseView** para mostrar tabla con edición inline.

Características:
- Tabla con filas editables
- Agregar/eliminar filas
- Validación en línea

---

### HtmlView: Vista HTML Personalizada

Extiende **BaseView** para mostrar contenido HTML personalizado.

Propiedades:
```
protected $fileName: string
  - Archivo Twig a renderizar (en Resources/templates)

protected $modelName: string
  - Nombre del modelo asociado
```

---

## SISTEMA DE FILTROS {#sistema-filtros}

Ubicación: `/Core/Lib/ListFilter/`

### BaseFilter: Clase Base de Filtros

Clase abstracta para todos los tipos de filtros.

#### Propiedades Publicas

```
public $key: string
  - Identificador único del filtro en la vista

public $field: string
  - Campo del modelo a filtrar

public $label: string
  - Etiqueta mostrada en interfaz

public $autosubmit: bool
  - Enviar formulario automáticamente al cambiar

public $readonly: bool
  - Filtro solo lectura

public $ordernum: int
  - Número de orden en la lista de filtros
```

#### Métodos Abstractos

```php
abstract public function getDataBaseWhere(array &$where): bool
  - Convierte valor del filtro en condición WHERE
  - Parámetro: array $where (pasado por referencia)
  - Retorna: bool (true si filtro tiene valor, false si está vacío)

abstract public function render(): string
  - Renderiza HTML del filtro
  - Retorna: HTML del control del filtro
```

#### Métodos Publicos

```php
public function getValue(): mixed
  - Obtiene valor actual del filtro

public function setValue($value): void
  - Establece valor del filtro

public function setValueFromRequest(Request &$request): void
  - Carga valor desde datos de formulario

public function name(): string
  - Retorna nombre HTML del control: 'filter' + key
```

---

### AutocompleteFilter

Filtro con campo de autocompletado.

```
Estructura:
- Campo de entrada con búsqueda en tabla
- Muestra coincidencias mientras escribe
- Selecciona código exacto

Parámetros adicionales:
  - $table: Tabla a buscar
  - $fieldcode: Campo de código
  - $fieldtitle: Campo de descripción
  - $where: Condiciones adicionales
```

---

### CheckboxFilter

Filtro de casilla de verificación.

```
Características:
- Booleano (marcado/no marcado)
- Puede usar operación '=' o '!='
- matchValue: Valor cuando está marcado

Ejemplo:
  addFilterCheckbox('active', 'Solo activos', 'active', '=', true)
```

---

### DateFilter

Filtro de fecha con selector de calendario.

```
Características:
- Selector de fecha con jQuery UI Datepicker
- Operaciones: '>=', '<=', '>', '<', '=', '!='
- Formato: YYYY-MM-DD

Ejemplo:
  addFilterDatePicker('fechadesde', 'Desde', 'fecha', '>=')
```

---

### NumberFilter

Filtro numérico.

```
Características:
- Campo para entrada numérica
- Soporta enteros y decimales
- Operaciones: '>=', '<=', '>', '<', '=', '!='

Ejemplo:
  addFilterNumber('totaldesde', 'Total desde', 'total', '>=')
```

---

### PeriodFilter

Filtro de período de tiempo.

```
Características:
- Selector de período predefinido
- Fecha inicio y fecha fin
- Períodos: Hoy, Ayer, Última semana, Último mes, Últimos 3 meses, Último año, etc.

Parámetro $dateTime:
  - false: Solo fechas (YYYY-MM-DD)
  - true: Fechas con hora (YYYY-MM-DD HH:MM:SS)

Ejemplo:
  addFilterPeriod('periodo', 'Período', 'fecha', false)
```

---

### SelectFilter

Filtro de selección estática.

```
Características:
- Dropdown con opciones predefinidas
- Valores pueden ser de cualquier tipo

Ejemplo:
  addFilterSelect('estado', 'Estado', 'estado', ['pendiente' => 'Pendiente', 'completado' => 'Completado'])
```

---

### SelectWhereFilter

Filtro de selección con condiciones WHERE personalizadas.

```
Características:
- Selector con múltiples condiciones WHERE
- Útil para filtros complejos

Estructura de valores:
[
  'label' => 'Etiqueta visible',
  'where' => [DataBaseWhere[], ...] // Condiciones para esta opción
]

Ejemplo:
  $values = [
    ['label' => 'Solo activos', 'where' => [new DataBaseWhere('suspended', false)]],
    ['label' => 'Todos', 'where' => []]
  ];
  addFilterSelectWhere('estado', $values, 'Estado')
```

---

## AJAXFORMS PARA DOCUMENTOS COMERCIALES {#ajaxforms}

Ubicación: `/Core/Lib/AjaxForms/`

Sistema para renderizar formularios AJAX para documentos comerciales (Ventas, Compras).

### SalesController

Controlador base para formularios AJAX de documentos de venta.

Métodos principales:
```php
public function createViews(): void
  - Crea vistas para documento de venta
  - Líneas del documento
  - Totales

public function loadData($viewName, $view): void
  - Carga datos del documento
  - Carga líneas asociadas

public function editAction(): bool
  - Guarda cambios en documento

public function newAction(): bool
  - Crea nuevo documento
```

---

### SalesLineHTML

Renderiza HTML para línea de documento de venta.

```
Propiedades:
- Código de producto
- Descripción
- Cantidad
- Precio unitario
- Descuento
- Total

Métodos:
  render(): string
    Genera HTML de la línea
    
  getLineTotal(): float
    Calcula total de la línea
```

---

### SalesFooterHTML

Renderiza pie de página del documento (totales).

```
Muestra:
- Subtotal
- Descuentos
- Impuestos (IVA, etc.)
- Total final
```

---

### SalesHeaderHTML

Renderiza encabezado del documento.

```
Muestra:
- Número de documento
- Cliente
- Fecha
- Moneda
```

---

### SalesModalHTML

Renderiza modal para seleccionar productos.

```
Características:
- Búsqueda de productos
- Selección de cantidad
- Confirmación de agregación
```

---

### PurchasesController, PurchasesLineHTML, etc.

Similar a Sales pero para documentos de compra.

---

## CONTROLADORES DEL CORE POR CATEGORÍA {#controladores-core}

### A. DASHBOARD Y CONFIGURACION

#### Dashboard.php
- **Clase**: Dashboard
- **Extiende**: PanelController
- **Modelo**: Ninguno (dashboard general)
- **Propósito**: Panel principal con información resumida del sistema
- **getPageData()**:
  - title: "Panel de control"
  - menu: "admin"
  - icon: "fas fa-object-group"
  - showonmenu: true
- **createViews()**:
  - Vista principal con widgets de resumen
  - Últimas facturas, pedidos, etc.
  - Información de stocks críticos
  - Alertas del sistema
- **Acciones especiales**: Muestra datos de todas las áreas de negocio

#### Root.php
- **Clase**: Root
- **Extiende**: Controller
- **Propósito**: Página de inicio/raíz del sistema
- **Funcionalidad**: Redirección y validación inicial

#### Login.php
- **Clase**: Login
- **Extiende**: Controller
- **Propósito**: Autenticación de usuarios
- **Procesos**: Verificación de credenciales, sesión

#### ConfigEmail.php
- **Clase**: ConfigEmail
- **Extiende**: EditController
- **Modelo**: EmailConfig
- **Propósito**: Configurar parámetros de correo electrónico
- **getPageData()**:
  - title: "Configuración de correo electrónico"
  - icon: "fas fa-at"
- **Configuración**: SMTP, usuario, contraseña, etc.

#### About.php
- **Clase**: About
- **Extiende**: Controller
- **Propósito**: Información sobre FacturaScripts
- **Muestra**: Versión, autores, licencia

---

### B. CLIENTES Y CONTACTOS

#### ListCliente.php
- **Clase**: ListCliente
- **Extiende**: ListController
- **Modelo**: Cliente
- **Propósito**: Listado de clientes
- **createViews()**:
  - Vista principal "ListCliente"
- **Filtros**: Nombre, ciudad, código postal, activo
- **Búsqueda**: En nombre, código, correo electrónico
- **Acciones**: Crear, editar, eliminar, duplicar

#### EditCliente.php
- **Clase**: EditCliente
- **Extiende**: EditController
- **Modelo**: Cliente
- **Propósito**: Editar datos de cliente
- **createViews()**:
  - Pestaña principal "EditCliente"
  - Pestaña "Direcciones" (EditableList de direcciones)
  - Pestaña "Contactos"
  - Pestaña "Documentos" (Facturas relacionadas)
- **getPageData()**:
  - title: "Cliente"
  - icon: "fas fa-users"

#### EditContacto.php
- **Clase**: EditContacto
- **Extiende**: ComercialContactController
- **Modelo**: Contacto
- **Propósito**: Gestionar contactos de clientes/proveedores
- **Propiedades**: Nombre, puesto, correo, teléfono

#### ListDireccion.php / EditDireccion.php
- **Clase**: ListDireccion / EditDireccion
- **Modelo**: Direccion
- **Propósito**: Gestionar direcciones de clientes

---

### C. PROVEEDORES

#### ListProveedor.php
- **Clase**: ListProveedor
- **Extiende**: ListController
- **Modelo**: Proveedor
- **Propósito**: Listado de proveedores
- **Similar a**: ListCliente pero para proveedores

#### EditProveedor.php
- **Clase**: EditProveedor
- **Extiende**: EditController
- **Modelo**: Proveedor
- **Propósito**: Editar datos de proveedor
- **Vistas**: Similar a EditCliente

---

### D. PRODUCTOS Y STOCK

#### ListProducto.php
- **Clase**: ListProducto
- **Extiende**: ListController
- **Modelo**: Producto
- **Propósito**: Listado de productos
- **Filtros**: Familia, referencia, descripción, stock
- **Búsqueda**: En referencia, descripción, código EAN
- **Acciones especiales**: 
  - Actualizar stock
  - Importar desde CSV
  - Exportar listado

#### EditProducto.php
- **Clase**: EditProducto
- **Extiende**: EditController
- **Modelo**: Producto
- **Propósito**: Editar datos de producto
- **createViews()**:
  - Pestaña principal "EditProducto"
  - Pestaña "Imágenes"
  - Pestaña "Atributos"
  - Pestaña "Stock por almacén"
  - Pestaña "Movimientos"
- **getPageData()**:
  - title: "Producto"
  - icon: "fas fa-cube"

#### ListAlmacen.php / EditAlmacen.php
- **Modelo**: Almacen
- **Propósito**: Gestionar almacenes/depósitos

#### ListStock.php
- **Modelo**: Stock
- **Propósito**: Control de stock por almacén
- **Información**: Producto, almacén, cantidad, movimientos

#### ListFamilia.php / EditFamilia.php
- **Modelo**: Familia
- **Propósito**: Categorías de productos

#### ListAtributo.php / EditAtributo.php
- **Modelo**: Atributo
- **Propósito**: Atributos personalizados de productos

---

### E. DOCUMENTOS DE VENTA

#### ListPresupuestoCliente.php
- **Clase**: ListPresupuestoCliente
- **Extiende**: ListBusinessDocument
- **Modelo**: PresupuestoCliente
- **Propósito**: Listado de presupuestos de cliente
- **Filtros**: Cliente, fecha, estado, total
- **Acciones**: Crear, editar, cambiar estado, duplicar a pedido

#### EditPresupuestoCliente.php
- **Clase**: EditPresupuestoCliente
- **Extiende**: EditController
- **Modelo**: PresupuestoCliente
- **Propósito**: Editar presupuesto
- **Vistas**: Formulario principal, líneas de presupuesto, totales

#### ListPedidoCliente.php
- **Clase**: ListPedidoCliente
- **Extiende**: ListBusinessDocument
- **Modelo**: PedidoCliente
- **Propósito**: Listado de pedidos de cliente
- **Similar a**: Presupuesto

#### EditPedidoCliente.php
- **Extiende**: EditController
- **Modelo**: PedidoCliente
- **Acciones especiales**: Duplicar a albarán

#### ListAlbaranCliente.php / EditAlbaranCliente.php
- **Modelo**: AlbaranCliente
- **Propósito**: Albaranes de entrega a clientes
- **Acciones especiales**: Crear factura desde albarán

#### ListFacturaCliente.php / EditFacturaCliente.php
- **Modelo**: FacturaCliente
- **Propósito**: Facturas de venta
- **Vistas adicionales**:
  - Rectificativas (notas de crédito)
  - Pagos registrados
- **Acciones especiales**: 
  - Cambiar estado
  - Enviar por correo
  - Imprimir

---

### F. DOCUMENTOS DE COMPRA

#### ListPresupuestoProveedor.php / EditPresupuestoProveedor.php
- **Modelo**: PresupuestoProveedor
- **Propósito**: Presupuestos de proveedores (solicitudes)

#### ListPedidoProveedor.php / EditPedidoProveedor.php
- **Modelo**: PedidoProveedor
- **Propósito**: Pedidos a proveedores

#### ListAlbaranProveedor.php / EditAlbaranProveedor.php
- **Modelo**: AlbaranProveedor
- **Propósito**: Albaranes recibidos de proveedores

#### ListFacturaProveedor.php / EditFacturaProveedor.php
- **Modelo**: FacturaProveedor
- **Propósito**: Facturas de proveedores
- **Vistas adicionales**:
  - Inversión del IVA
  - Pagos registrados

---

### G. CONTABILIDAD

#### ListAsiento.php / EditAsiento.php
- **Modelo**: Asiento
- **Propósito**: Registros contables (asientos)
- **Componentes**:
  - Encabezado del asiento
  - Líneas del asiento (Partida)
  - Validación de cuadre

#### ListCuenta.php / EditCuenta.php
- **Modelo**: Cuenta
- **Propósito**: Plan de cuentas
- **Estructura**: Jerarquía de cuentas

#### ListDiario.php / EditDiario.php
- **Modelo**: Diario
- **Propósito**: Diarios contables (Ventas, Compras, Banco, etc.)

#### ListEjercicio.php / EditEjercicio.php
- **Modelo**: Ejercicio
- **Propósito**: Ejercicios fiscales (años contables)

#### ListSubcuenta.php / EditSubcuenta.php
- **Modelo**: Subcuenta
- **Propósito**: Cuentas detalladas dentro de una cuenta principal

#### ListPartida.php
- **Modelo**: Partida
- **Propósito**: Líneas individuales de asientos contables

---

### H. ADMINISTRACION

#### ListUsuario.php / EditUsuario.php
- **Modelo**: Usuario
- **Propósito**: Gestión de usuarios del sistema
- **Configuración**: Nick, nombre, rol, permisos

#### ListRol.php / EditRol.php
- **Modelo**: Rol
- **Propósito**: Roles y permisos de usuario

#### ListApiKey.php / EditApiKey.php
- **Modelo**: ApiKey
- **Propósito**: Claves de acceso para API REST

#### AdminPlugins.php
- **Clase**: AdminPlugins
- **Propósito**: Gestión de plugins/extensiones
- **Funciones**: Instalar, activar, desactivar, actualizar

#### ApiRoot.php
- **Clase**: ApiRoot
- **Propósito**: Punto de entrada de API REST
- **Métodos**: GET, POST, PUT, DELETE para acceso a modelos

---

### I. INFORMES Y REPORTES

#### ListAlerta.php
- **Modelo**: Alerta
- **Propósito**: Alertas del sistema (stock bajo, etc.)

#### ListFacturaRectificativaCliente.php
- **Modelo**: FacturaRectificativaCliente
- **Propósito**: Notas de crédito de venta

#### ListNotaCreditoProveedor.php
- **Modelo**: NotaCreditoProveedor
- **Propósito**: Notas de crédito de compra

#### ListAsientoIVA.php
- **Modelo**: AsientoIVA
- **Propósito**: Asientos derivados de documentos comerciales

---

### J. DATOS BASICOS

#### ListAgenciaTransporte.php / EditAgenciaTransporte.php
- **Modelo**: AgenciaTransporte
- **Propósito**: Transportistas/empresas de logística

#### ListAgente.php / EditAgente.php
- **Modelo**: Agente
- **Propósito**: Agentes comerciales (vendedores)

#### ListCiudad.php / EditCiudad.php
- **Modelo**: Ciudad
- **Propósito**: Ciudades/municipios

#### ListCodigoPostal.php / EditCodigoPostal.php
- **Modelo**: CodigoPostal
- **Propósito**: Códigos postales

#### ListDivisa.php / EditDivisa.php
- **Modelo**: Divisa
- **Propósito**: Monedas/divisas

#### ListEmpresa.php / EditEmpresa.php
- **Modelo**: Empresa
- **Propósito**: Configuración de empresa(s)

#### ListImpuesto.php / EditImpuesto.php
- **Modelo**: Impuesto
- **Propósito**: Impuestos (IVA, etc.)

#### ListNaturaleza.php / EditNaturaleza.php
- **Modelo**: Naturaleza
- **Propósito**: Naturalezas contables de operaciones

#### ListPais.php / EditPais.php
- **Modelo**: Pais
- **Propósito**: Países

#### ListBanco.php / EditBanco.php
- **Modelo**: Banco
- **Propósito**: Bancos/entidades financieras

#### ListCuentaBanco.php / EditCuentaBanco.php
- **Modelo**: CuentaBanco
- **Propósito**: Cuentas bancarias de la empresa

#### ListFactura.php
- **Modelo**: Factura
- **Propósito**: Listado unificado de todas las facturas

---

## COMO CREAR UN NUEVO CONTROLADOR {#crear-controlador}

### Ejemplo 1: Crear un ListController

```php
<?php
namespace FacturaScripts\Dinamic\Controller;

use FacturaScripts\Core\Lib\ExtendedController\ListController;
use FacturaScripts\Core\Lib\ExtendedController\ListView;

class ListMiModelo extends ListController
{
    public function getPageData(): array
    {
        $data = parent::getPageData();
        $data['title'] = 'Mi Listado';
        $data['menu'] = 'ventas';
        $data['icon'] = 'fas fa-list';
        $data['showonmenu'] = true;
        return $data;
    }

    protected function createViews()
    {
        // Crear vista principal
        $this->addView('ListMiModelo', 'MiModelo', 'Mi Modelo', 'fas fa-cube');
        
        // Configurar búsqueda
        $this->addSearchFields('ListMiModelo', ['nombre', 'codigo', 'descripcion']);
        
        // Agregar filtros
        $this->addFilterCheckbox('ListMiModelo', 'activo', 'Activos', 'activo');
        $this->addFilterSelect('ListMiModelo', 'familia', 'Familia', 'familia_id', 
            ['A' => 'Familia A', 'B' => 'Familia B']);
        $this->addFilterDatePicker('ListMiModelo', 'fecha', 'Desde', 'fecha_creacion', '>=');
        
        // Agregar opciones de ordenamiento
        $this->addOrderBy('ListMiModelo', ['nombre'], 'Nombre');
        $this->addOrderBy('ListMiModelo', ['fecha_creacion'], 'Fecha Creación', 2);
        
        // Agregar colores condicionales
        $this->addColor('ListMiModelo', 'activo', false, 'danger', 'Inactivo');
    }

    protected function loadData($viewName, $view)
    {
        // Implementación base carga los datos
        parent::loadData($viewName, $view);
        
        // Aquí puede agregar lógica adicional
    }
}
```

### Ejemplo 2: Crear un EditController

```php
<?php
namespace FacturaScripts\Dinamic\Controller;

use FacturaScripts\Core\Lib\ExtendedController\EditController;

class EditMiModelo extends EditController
{
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
        parent::createViews();
        
        // Esto crea automáticamente la vista principal "EditMiModelo"
        // Agregar vistas secundarias si es necesario
        
        // Vista secundaria: lista de items relacionados
        $this->addListView('ListItems', 'Item', 'Items', 'fas fa-list');
        
        // Vista secundaria: formulario HTML personalizado
        $this->addHtmlView('ViewNotes', 'MiModelo/notes', 'MiModelo', 'Notas');
    }

    protected function loadData($viewName, $view)
    {
        switch ($viewName) {
            case 'EditMiModelo':
                parent::loadData($viewName, $view);
                break;
                
            case 'ListItems':
                // Cargar items relacionados al modelo actual
                $codigo = $this->request->query('code');
                $view->loadData($codigo);
                break;
                
            default:
                parent::loadData($viewName, $view);
        }
    }
}
```

### Ejemplo 3: Crear un PanelController

```php
<?php
namespace FacturaScripts\Dinamic\Controller;

use FacturaScripts\Core\Lib\ExtendedController\PanelController;

class PanelDashboard extends PanelController
{
    public function getPageData(): array
    {
        $data = parent::getPageData();
        $data['title'] = 'Mi Dashboard';
        $data['menu'] = 'admin';
        $data['icon'] = 'fas fa-chart-line';
        $data['showonmenu'] = true;
        return $data;
    }

    protected function createViews()
    {
        // Vista principal: datos principales
        $this->addEditView('EditPrincipal', 'MiModelo', 'Información Principal');
        
        // Vista secundaria: tabla de datos
        $this->addListView('ListDetalle', 'Detalle', 'Detalles');
        
        // Vista secundaria: HTML personalizado
        $this->addHtmlView('ViewChart', 'Dashboard/chart', 'MiModelo', 'Gráficos');
        
        // Cambiar posición de pestañas
        $this->setTabsPosition('bottom');
    }

    protected function loadData($viewName, $view)
    {
        switch ($viewName) {
            case 'EditPrincipal':
                $codigo = $this->request->query('code', '');
                $view->loadData($codigo);
                break;
                
            case 'ListDetalle':
                // Cargar detalles del registro principal
                if ($this->hasData) {
                    $codigo = $this->getModel()->primaryColumnValue();
                    $view->loadData($codigo);
                }
                break;
        }
    }
}
```

### Pasos para Implementar un Nuevo Controlador

1. **Crear archivo PHP** en `/Dinamic/Controller/NombreControlador.php`

2. **Declarar namespace y clase**:
   ```php
   namespace FacturaScripts\Dinamic\Controller;
   ```

3. **Extender clase base** (ListController, EditController, o PanelController)

4. **Implementar getPageData()**:
   ```php
   public function getPageData(): array
   {
       $data = parent::getPageData();
       $data['title'] = 'Título mostrado';
       $data['menu'] = 'menu_principal'; // admin, ventas, compras, etc.
       $data['icon'] = 'fas fa-iconname';
       $data['showonmenu'] = true; // Mostrar en menú
       return $data;
   }
   ```

5. **Implementar createViews()**:
   - Llamar a métodos para agregar vistas
   - Configurar filtros, búsqueda, orden
   - Establecer propiedades de vistas

6. **Implementar loadData()**:
   - Cargar datos de modelos
   - Aplicar filtros personalizados
   - Filtrar datos por propietario si aplica

7. **Registrar en sistema** (si es plugin):
   - Agregar entrada en `controllers.xml`
   - Crear tabla del modelo si es necesario

### Configuración del Menu

En `controllers.xml`:
```xml
<controller>
    <name>ListMiModelo</name>
    <title>Mi Listado</title>
    <menu>ventas</menu>
    <icon>fas fa-cube</icon>
</controller>
```

### Plantilla Model

Si crea un nuevo modelo, debe tener:
```php
namespace FacturaScripts\Dinamic\Model;

class MiModelo extends ModelClass
{
    public function tableName(): string
    {
        return 'mimodelo';
    }

    public function primaryColumn(): string
    {
        return 'id';
    }

    protected function saveInsert(array $values = [])
    {
        // Lógica de inserción
    }

    protected function saveUpdate(array $values = [])
    {
        // Lógica de actualización
    }

    public function delete()
    {
        // Lógica de eliminación
    }

    public function test()
    {
        // Validación de datos
    }
}
```

---

## NOTAS FINALES

- Siempre verificar permisos del usuario antes de acciones críticas
- Usar validaciones en modelo (test method)
- Implementar logs para auditoría
- Validar tokens de formulario contra CSRF
- Considerar cache en consultas complejas
- Documentar acciones y filtros personalizados
- Usar DataBaseWhere para construir condiciones seguras

---

**Documento generado para FacturaScripts 2025**
**Versión: 1.0**
**Fecha: Abril 2026**
