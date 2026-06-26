# FacturaScripts 2025 - Guía Avanzada de Controladores

Guía avanzada con ejemplos prácticos y patrones comunes en FacturaScripts.

---

## TABLA DE CONTENIDOS

1. [Patrones de Diseño Comunes](#patrones)
2. [Filtros Avanzados](#filtros-avanzados)
3. [Validación y Permisos](#validacion)
4. [Traits y Mixins](#traits)
5. [Casos de Uso Reales](#casos-uso)

---

## PATRONES DE DISEÑO COMUNES {#patrones}

### Patrón 1: ListController con Múltiples Vistas

Útil cuando necesitas mostrar múltiples listados relacionados.

```php
<?php
class ListVentas extends ListController
{
    protected function createViews()
    {
        // Vista principal: facturas
        $this->addView('ListFacturaCliente', 'FacturaCliente', 'Facturas');
        $this->addFilterSelect('ListFacturaCliente', 'estado', 'Estado', 
            'estado', ['borrador' => 'Borrador', 'publicada' => 'Publicada']);
        
        // Vista secundaria: pedidos
        $this->addView('ListPedidoCliente', 'PedidoCliente', 'Pedidos');
        
        // Vista secundaria: albaranes
        $this->addView('ListAlbaranCliente', 'AlbaranCliente', 'Albaranes');
    }
    
    protected function loadData($viewName, $view)
    {
        parent::loadData($viewName, $view);
        // Aquí puedes agregar lógica específica por vista
    }
}
```

### Patrón 2: EditController con Vistas Relacionadas

Mostrar datos principales junto con registros relacionados.

```php
<?php
class EditCliente extends EditController
{
    public function getModelClassName(): string
    {
        return 'Cliente';
    }

    protected function createViews()
    {
        parent::createViews();
        
        // Vista de direcciones
        $this->addListView('ListDirecciones', 'Direccion', 'Direcciones');
        
        // Vista editable de contactos
        $this->addEditListView('ListContactos', 'Contacto', 'Contactos');
        
        // Vista de documentos (solo lectura)
        $view = $this->addListView('ListDocumentos', 'FacturaCliente', 'Documentos');
        $view->setSettings('btnNew', false)
             ->setSettings('btnDelete', false);
    }

    protected function loadData($viewName, $view)
    {
        $mainViewName = $this->getMainViewName();
        
        if ($viewName === $mainViewName) {
            parent::loadData($viewName, $view);
        } elseif ($this->hasData) {
            // Cargar solo si existe registro principal
            $clienteId = $this->getModel()->primaryColumnValue();
            $where = [new DataBaseWhere('codcliente', $clienteId)];
            $view->loadData('', $where);
        }
    }
}
```

### Patrón 3: Filtros Dinámicos

Crear filtros que se generan según datos de la base de datos.

```php
<?php
protected function createViews()
{
    $this->addView('ListProducto', 'Producto', 'Productos');
    
    // Obtener familias dinámicamente
    $familias = $this->codeModel->all('familias', 'codigo', 'nombre');
    
    if (count($familias) < CodeModel::getLimit()) {
        // Si hay pocas familias, usar select estático
        $this->addFilterSelect('ListProducto', 'familia', 'Familia', 'codfamilia', $familias);
    } else {
        // Si hay muchas, usar autocomplete
        $this->addFilterAutocomplete('ListProducto', 'familia', 'Familia', 
            'codfamilia', 'familias', 'codigo', 'nombre');
    }
}
```

### Patrón 4: Acciones Personalizadas

Agregar acciones específicas al controlador.

```php
<?php
protected function execPreviousAction($action)
{
    switch ($action) {
        case 'duplicate':
            return $this->duplicateAction();
            
        case 'mass-edit':
            return $this->massEditAction();
            
        case 'export-csv':
            return $this->exportCsvAction();
    }
    
    return parent::execPreviousAction($action);
}

private function duplicateAction(): bool
{
    $code = $this->request->input('code');
    $model = $this->views[$this->active]->model;
    
    if ($model->loadFromCode($code) && $model->duplicate()) {
        Tools::log()->notice('record-duplicated-successfully');
        return true;
    }
    
    Tools::log()->warning('duplicate-error');
    return false;
}
```

---

## FILTROS AVANZADOS {#filtros-avanzados}

### Filtro Personalizado Completo

Crear un filtro personalizado extendiendo BaseFilter.

```php
<?php
namespace FacturaScripts\Core\Lib\ListFilter;

use FacturaScripts\Core\Base\DataBase\DataBaseWhere;
use FacturaScripts\Core\Tools;

class RangeFilter extends BaseFilter
{
    /**
     * @var string
     */
    private $valueMin;

    /**
     * @var string
     */
    private $valueMax;

    /**
     * @param string $key
     * @param string $field
     * @param string $label
     */
    public function __construct(string $key, string $field = '', string $label = '')
    {
        parent::__construct($key, $field, $label);
        $this->autosubmit = false;
    }

    /**
     * Obtiene condición WHERE para este filtro
     */
    public function getDataBaseWhere(array &$where): bool
    {
        $hasMin = '' !== $this->valueMin && null !== $this->valueMin;
        $hasMax = '' !== $this->valueMax && null !== $this->valueMax;

        if ($hasMin) {
            $where[] = new DataBaseWhere($this->field, $this->valueMin, '>=');
        }

        if ($hasMax) {
            $where[] = new DataBaseWhere($this->field, $this->valueMax, '<=');
        }

        return $hasMin || $hasMax;
    }

    /**
     * Renderiza HTML del filtro
     */
    public function render(): string
    {
        $label = static::$i18n->trans($this->label);
        $name = $this->name();
        $nameMin = $name . 'Min';
        $nameMax = $name . 'Max';

        return '<div class="form-group">'
            . '<label>' . $label . '</label>'
            . '<div class="row">'
            . '<div class="col-md-6">'
            . '<input type="number" name="' . $nameMin . '" class="form-control" '
            . 'placeholder="Mínimo" value="' . $this->valueMin . '"/>'
            . '</div>'
            . '<div class="col-md-6">'
            . '<input type="number" name="' . $nameMax . '" class="form-control" '
            . 'placeholder="Máximo" value="' . $this->valueMax . '"/>'
            . '</div>'
            . '</div>'
            . '</div>';
    }

    /**
     * Carga valores desde request
     */
    public function setValueFromRequest($request)
    {
        parent::setValueFromRequest($request);
        
        $nameMin = $this->name() . 'Min';
        $nameMax = $this->name() . 'Max';
        
        $this->valueMin = Tools::noHtml($request->request->get($nameMin));
        $this->valueMax = Tools::noHtml($request->request->get($nameMax));
    }
}
```

### Usar Filtro Personalizado

```php
protected function createViews()
{
    $view = $this->addView('ListProducto', 'Producto', 'Productos');
    
    // Usar filtro personalizado
    $filter = new RangeFilter('preciorange', 'precio', 'Rango de Precio');
    $view->filters[] = $filter;
}
```

### Combinación de Filtros (AND/OR)

```php
protected function createViews()
{
    $this->addView('ListCliente', 'Cliente', 'Clientes');
    
    // Crear opciones de filtro complejas
    $values = [
        [
            'label' => 'Clientes de alto riesgo',
            'where' => [
                new DataBaseWhere('riesgoalcanzado', 1000, '>='),
                new DataBaseWhere('debaja', false)
            ]
        ],
        [
            'label' => 'Clientes inactivos con deuda',
            'where' => [
                new DataBaseWhere('debaja', true),
                new DataBaseWhere('total', 0, '>')
            ]
        ],
        [
            'label' => 'Todos',
            'where' => []
        ]
    ];
    
    $this->addFilterSelectWhere('ListCliente', 'riesgo', $values);
}
```

---

## VALIDACION Y PERMISOS {#validacion}

### Verificación de Permisos

```php
<?php
protected function execPreviousAction($action)
{
    // Verificar permisos específicos antes de ejecutar acción
    if ($action === 'delete') {
        if (false === $this->permissions->allowDelete) {
            Tools::log()->warning('not-allowed-delete');
            return false;
        }
    }
    
    if ($action === 'export') {
        if (false === $this->permissions->allowExport) {
            Tools::log()->warning('not-allowed-export');
            return false;
        }
    }
    
    return parent::execPreviousAction($action);
}
```

### Filtrado por Propietario

```php
<?php
protected function loadData($viewName, $view)
{
    $where = [];
    
    // Si solo ve sus propios datos
    if ($this->permissions->onlyOwnerData) {
        // Obtener filtro de propietario
        $where = $this->getOwnerFilter($view->model);
    }
    
    $view->loadData('', $where);
}
```

### Validación de Datos en Modelo

```php
<?php
// En la clase del modelo
public function test()
{
    // Validar campo requerido
    if (empty($this->nombre)) {
        Tools::log()->error('nombre-required');
        return false;
    }
    
    // Validar formato de email
    if (!filter_var($this->email, FILTER_VALIDATE_EMAIL)) {
        Tools::log()->error('invalid-email');
        return false;
    }
    
    // Validar unicidad
    $other = new self();
    if ($other->loadFromCode($this->codigo) && $other->codigo !== $this->codigo) {
        Tools::log()->error('codigo-duplicated');
        return false;
    }
    
    return parent::test();
}
```

---

## TRAITS Y MIXINS {#traits}

### ListViewFiltersTrait

Proporciona métodos para agregar filtros a ListView. Ya está integrado en ListController.

**Archivo**: `/Core/Lib/ExtendedController/ListViewFiltersTrait.php`

Métodos disponibles:
- `addFilterAutocomplete()` - Filtro de autocompletado
- `addFilterCheckbox()` - Filtro booleano
- `addFilterDatePicker()` - Filtro de fecha
- `addFilterNumber()` - Filtro numérico
- `addFilterPeriod()` - Filtro de período
- `addFilterSelect()` - Filtro de selección
- `addFilterSelectWhere()` - Filtro con WHERE personalizado

### ListBusinessActionTrait

Proporciona acciones comunes para documentos comerciales.

**Archivo**: `/Core/Lib/ExtendedController/ListBusinessActionTrait.php`

Acciones:
- Cambiar estado de documento
- Duplicar documento
- Crear documento relacionado (ej: pedido a albarán)
- Anular documento

### DocFilesTrait

Gestiona archivos adjuntos a documentos.

**Archivo**: `/Core/Lib/ExtendedController/DocFilesTrait.php`

Funcionalidad:
- Subir archivos
- Listar archivos adjuntos
- Descargar archivos
- Eliminar archivos

### LogAuditTrait

Proporciona auditoría de cambios.

**Archivo**: `/Core/Lib/ExtendedController/LogAuditTrait.php`

Registra:
- Qué usuario realizó cambios
- Cuándo se realizaron
- Qué datos cambiaron

### ProductImagesTrait

Gestiona imágenes de productos.

**Archivo**: `/Core/Lib/ExtendedController/ProductImagesTrait.php`

Funcionalidad:
- Subir imágenes
- Establecer imagen principal
- Eliminar imágenes
- Reordenar imágenes

---

## CASOS DE USO REALES {#casos-uso}

### Caso 1: Listado de Facturas con Filtros Complejos

```php
<?php
class ListFacturaCliente extends ListBusinessDocument
{
    protected function createViews()
    {
        $this->addView('ListFacturaCliente', 'FacturaCliente', 'Facturas');
        
        // Búsqueda
        $this->addSearchFields('ListFacturaCliente', 
            ['numero', 'nombre', 'email']);
        
        // Filtro de estado
        $this->addFilterSelectWhere('ListFacturaCliente', 'estado', [
            ['label' => 'Pendientes de pago', 
             'where' => [new DataBaseWhere('estado', 'pendiente')]],
            ['label' => 'Pagadas', 
             'where' => [new DataBaseWhere('estado', 'pagada')]],
            ['label' => 'Anuladas', 
             'where' => [new DataBaseWhere('estado', 'anulada')]],
            ['label' => 'Todas', 'where' => []]
        ]);
        
        // Filtro de fecha
        $this->addFilterPeriod('ListFacturaCliente', 'fecha', 
            'Período', 'fecha');
        
        // Filtro de cliente
        $this->addFilterAutocomplete('ListFacturaCliente', 'cliente', 
            'Cliente', 'codcliente', 'clientes', 'codigo', 'nombre');
        
        // Filtro de importe
        $this->addFilterNumber('ListFacturaCliente', 'total', 
            'Total desde', 'total', '>=');
        
        // Ordenamientos
        $this->addOrderBy('ListFacturaCliente', ['numero'], 'Número');
        $this->addOrderBy('ListFacturaCliente', ['fecha'], 'Fecha', 2);
        $this->addOrderBy('ListFacturaCliente', ['total'], 'Total');
        
        // Colores
        $this->addColor('ListFacturaCliente', 'estado', 'pagada', 
            'success', 'Pagada');
        $this->addColor('ListFacturaCliente', 'estado', 'pendiente', 
            'warning', 'Pendiente');
        $this->addColor('ListFacturaCliente', 'estado', 'anulada', 
            'danger', 'Anulada');
    }
    
    protected function loadData($viewName, $view)
    {
        parent::loadData($viewName, $view);
        
        // Lógica adicional específica
        $this->addCustomLogic($view);
    }
    
    private function addCustomLogic($view)
    {
        // Procesar datos si es necesario
    }
}
```

### Caso 2: Panel de Administración Completo

```php
<?php
class AdminPanel extends PanelController
{
    public function getPageData(): array
    {
        $data = parent::getPageData();
        $data['title'] = 'Panel de Administración';
        $data['menu'] = 'admin';
        $data['icon'] = 'fas fa-cogs';
        $data['showonmenu'] = true;
        return $data;
    }

    protected function createViews()
    {
        $this->setTabsPosition('left');
        
        // Pestaña de usuarios
        $this->addEditView('EditUsuarios', 'Usuario', 'Usuarios');
        $this->addListView('ListRoles', 'Rol', 'Roles', 'fas fa-shield');
        
        // Pestaña de configuración
        $this->addHtmlView('ConfigAjustes', 'Admin/settings', 'Usuario', 'Ajustes');
        
        // Pestaña de logs
        $this->addListView('ListLogs', 'LogMessage', 'Registros', 'fas fa-file-alt');
        $this->tab('ListLogs')
            ->addFilterSelect('ListLogs', 'tipo', 'Tipo', 'tipo', 
                ['error' => 'Error', 'warning' => 'Advertencia', 'info' => 'Info'])
            ->addOrderBy(['fecha'], 'Fecha', 2);
    }

    protected function loadData($viewName, $view)
    {
        switch ($viewName) {
            case 'EditUsuarios':
                $codigo = $this->request->query('code', '');
                $view->loadData($codigo);
                break;
                
            case 'ListLogs':
                // Mostrar últimos 100 logs
                $where = [];
                $view->loadData('', $where, [], 0, 100);
                break;
                
            default:
                parent::loadData($viewName, $view);
        }
    }
}
```

### Caso 3: Controlador con Validaciones Personalizadas

```php
<?php
class EditCliente extends EditController
{
    public function getModelClassName(): string
    {
        return 'Cliente';
    }

    protected function execPreviousAction($action)
    {
        if ($action === 'save') {
            return $this->saveAction();
        }
        
        return parent::execPreviousAction($action);
    }

    private function saveAction(): bool
    {
        // Obtener modelo
        $model = $this->views[$this->active]->model;
        
        // Validaciones personalizadas
        if (!$this->validateClienteData($model)) {
            return false;
        }
        
        // Procesar datos de formulario
        $this->views[$this->active]->processFormData($this->request, 'edit');
        
        // Guardar
        if ($model->save()) {
            Tools::log()->notice('record-updated-correctly');
            return true;
        }
        
        Tools::log()->error('record-save-error');
        return false;
    }

    private function validateClienteData($model): bool
    {
        // Validar CIF/NIF
        if (!$this->validateCIF($model->cifnif)) {
            Tools::log()->error('invalid-cif-nif');
            return false;
        }
        
        // Validar email
        if (!empty($model->email) && !filter_var($model->email, FILTER_VALIDATE_EMAIL)) {
            Tools::log()->error('invalid-email');
            return false;
        }
        
        // Validar que no exista otro cliente con mismo CIF
        $other = new Cliente();
        $other->loadFromCode($model->cifnif, 'cifnif');
        if ($other->exists() && $other->codcliente !== $model->codcliente) {
            Tools::log()->error('cif-duplicated');
            return false;
        }
        
        return true;
    }

    private function validateCIF(string $cif): bool
    {
        // Implementar validación de CIF español
        if (empty($cif)) {
            return true;
        }
        
        // Aquí iría la lógica de validación
        return strlen($cif) >= 9;
    }
}
```

### Caso 4: Listado con Búsqueda Global

```php
<?php
class ListProducto extends ListController
{
    protected function createViews()
    {
        $this->addView('ListProducto', 'Producto', 'Productos');
        
        // Campos donde busca la megabúsqueda
        $this->addSearchFields('ListProducto', [
            'codigo',
            'referencia',
            'nombre',
            'descripcion',
            'CAST(codbarras AS CHAR(50))',
            'email_contacto'
        ]);
        
        // Nota: Para campos numéricos usar CAST para que funcione LIKE
        
        // Habilitar megabúsqueda
        $this->setSettings('ListProducto', 'megasearch', true);
    }
}
```

---

## MEJORES PRACTICAS

### 1. Seguridad

- Siempre verificar permisos antes de acciones críticas
- Validar tokens de formulario (validateFormToken)
- Usar DataBaseWhere para construir queries seguras
- No usar concatenación de strings en SQL

### 2. Rendimiento

- Usar índices en base de datos
- Limitar resultados con LIMIT
- Usar cache para datos estáticos
- Considerar paginación en listas grandes

### 3. Mantenibilidad

- Documentar acciones personalizadas
- Usar nombres descriptivos para vistas y filtros
- Separar lógica en métodos pequeños
- Reutilizar traits y mixins

### 4. Experiencia de Usuario

- Agregar mensajes de confirmación
- Mostrar indicadores de carga
- Validar datos en cliente y servidor
- Proporcionar ayuda en tooltips

---

**Documento generado para FacturaScripts 2025**
**Versión: 1.0 - Guía Avanzada**
**Fecha: Abril 2026**
