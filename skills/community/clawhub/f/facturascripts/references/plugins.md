# Referencia Completa: Sistema de Plugins FacturaScripts 2025

## Tabla de Contenidos

1. [Estructura Fundamental de un Plugin](#1-estructura-fundamental-de-un-plugin)
2. [Archivo facturascripts.ini](#2-archivo-facturascriptsini)
3. [Clase Init.php](#3-clase-initphp)
4. [Ciclo de Vida Completo del Plugin](#4-ciclo-de-vida-completo-del-plugin)
5. [Sistema Mod (Hooks y Modificadores)](#5-sistema-mod-hooks-y-modificadores)
6. [Crear Modelos en un Plugin](#6-crear-modelos-en-un-plugin)
7. [Crear Controladores en un Plugin](#7-crear-controladores-en-un-plugin)
8. [Crear Vistas en un Plugin](#8-crear-vistas-en-un-plugin)
9. [Crear un Worker](#9-crear-un-worker)
10. [Sistema de Migraciones](#10-sistema-de-migraciones)
11. [Traducciones en Plugins](#11-traducciones-en-plugins)
12. [Assets CSS/JavaScript](#12-assets-cssjavascript)
13. [Ejemplo Completo: Plugin Personalizado](#13-ejemplo-completo-plugin-personalizado)

---

## 1. Estructura Fundamental de un Plugin

### 1.1 Estructura de Directorios

La estructura basica de un plugin es la siguiente:

```
Plugins/
└── NombrePlugin/
    ├── facturascripts.ini          (requerido)
    ├── Init.php                     (requerido)
    ├── Controller/                  (opcional)
    │   ├── ListProductoCustom.php
    │   └── EditProductoCustom.php
    ├── Model/                       (opcional)
    │   └── ProductoCustom.php
    ├── Table/                       (opcional)
    │   └── productoCustom.xml
    ├── XMLView/                     (opcional)
    │   ├── ListProductoCustom.xml
    │   └── EditProductoCustom.xml
    ├── View/                        (opcional)
    │   └── custom-view.html.twig
    ├── Translation/                 (opcional)
    │   ├── es_ES.json
    │   ├── en_EN.json
    │   └── ca_ES.json
    ├── Assets/                      (opcional)
    │   ├── CSS/
    │   │   └── custom-styles.css
    │   └── JS/
    │       └── custom-script.js
    ├── Mod/                         (opcional)
    │   └── CustomCalculatorMod.php
    ├── Worker/                      (opcional)
    │   └── CustomWorker.php
    ├── Lib/                         (opcional)
    │   └── CustomHelper.php
    └── Extension/                   (opcional)
        └── XMLView/
            ├── ListCliente.xml
            └── EditProducto.xml
```

### 1.2 Requisitos Minimos

Cada plugin DEBE contener:

1. **facturascripts.ini**: Archivo de configuracion del plugin
2. **Init.php**: Clase de inicializacion con namespace `FacturaScripts\Plugins\NombrePlugin`

El nombre de la carpeta del plugin DEBE coincidir exactamente con el campo `name` del archivo `facturascripts.ini`.

---

## 2. Archivo facturascripts.ini

### 2.1 Estructura Completa

El archivo `facturascripts.ini` debe estar en la raiz del directorio del plugin y contiene toda la metadata:

```ini
[plugin]
name = MiPlugin
description = Descripcion breve del plugin
version = 1.0.0
min_version = 2025
min_php = 8.0
require = OtroPlugin,AnotherPlugin
require_php = curl,json,pdo
hidden = false
```

### 2.2 Campos Disponibles

| Campo | Tipo | Requerido | Descripcion | Ejemplo |
|-------|------|-----------|-------------|---------|
| `name` | string | Si | Nombre unico del plugin. Debe coincidir con el nombre de la carpeta. Usar PascalCase. | `MiPlugin` |
| `description` | string | Si | Descripcion del plugin. Breve pero descriptiva. | `Plugin para personalizar clientes` |
| `version` | float | Si | Numero de version del plugin. Se usa para detectar actualizaciones. | `1.0.0` o `1.5` |
| `min_version` | float | Si | Version minima de FacturaScripts requerida. A partir de 2025 es obligatorio usar 2025 o superior. | `2025` |
| `min_php` | float | No | Version minima de PHP. Por defecto es 8.0. | `8.0` o `8.2` |
| `require` | string | No | Plugins requeridos separados por comas. Si no estan activos, este plugin no se podra activar. | `Core,OtroPlugin` |
| `require_php` | string | No | Extensiones PHP requeridas separadas por comas. | `curl,json,pdo,mysqli` |
| `hidden` | bool | No | Si es true, el plugin no apareceera en el listado de Administracion/Plugins. Por defecto es false. | `false` |

### 2.3 Validaciones del facturascripts.ini

- El campo `min_version` DEBE ser >= 2025. Plugins con min_version < 2025 se consideran incompatibles.
- El campo `name` DEBE usar caracteres alfanumericos sin espacios (PascalCase recomendado).
- La version PHP DEBE ser compatible con el servidor donde se instale.
- Los plugins en `require` DEBEN estar disponibles para ser activados.

### 2.4 Ejemplo Completo

```ini
[plugin]
name = GestorServicios
description = Plugin para gestionar servicios adicionales de los clientes
version = 2.1.5
min_version = 2025
min_php = 8.1
require = Core
require_php = curl,json,pdo
hidden = false
```

---

## 3. Clase Init.php

### 3.1 Estructura Basica

El archivo `Init.php` es la clase controladora del ciclo de vida del plugin:

```php
<?php

namespace FacturaScripts\Plugins\MiPlugin;

use FacturaScripts\Core\Base\InitClass;
use FacturaScripts\Core\Migrations;
use FacturaScripts\Core\Tools;

class Init extends InitClass
{
    public function init(): void
    {
        // Ejecutado SIEMPRE que el plugin esta activo
        // Aqui se registran workers, listeners, etc.
    }

    public function update(): void
    {
        // Ejecutado SOLO cuando el plugin se actualiza
        // Aqui van las migraciones de datos
    }

    public function uninstall(): void
    {
        // Ejecutado cuando el plugin se desactiva
        // Aqui se limpian datos, se eliminan tablas, etc.
    }
}
```

### 3.2 Metodo init()

Se ejecuta en CADA carga de la aplicacion si el plugin esta activo. Aqui se:

- Registran workers
- Se cargan configuraciones del plugin
- Se inicializan servicios
- Se registran hooks (mediante extensiones)

```php
public function init(): void
{
    // Registrar un worker que se ejecuta periodicamente
    if ($this->myFirstTime()) {
        // Tareas de inicializacion primera vez
        Tools::log()->info('MiPlugin se ha inicializado por primera vez');
    }

    // Registrar acciones que se ejecutan en cada carga
    // (mediante el sistema de eventos/listeners si existe)
}
```

### 3.3 Metodo update()

Se ejecuta SOLO en las siguientes situaciones:

1. Cuando el plugin se actualiza a una version mas reciente
2. Cuando la propiedad `post_enable` del plugin es `true` (cuando se activa)
3. El lock del update se gestiona automaticamente

Aqui se deben:

- Crear nuevas tablas
- Modificar tablas existentes
- Migrar datos
- Actualizar configuraciones

```php
public function update(): void
{
    // Ejemplo: crear tabla si no existe
    if (!$this->tables->tableExists('tabla_custom')) {
        // La tabla se crea desde el XML en Table/
        // Este metodo solo se usa para validaciones o datos iniciales
    }

    // Ejecutar migraciones
    $migrations = [
        new \FacturaScripts\Plugins\MiPlugin\Migrations\Migration001(),
        new \FacturaScripts\Plugins\MiPlugin\Migrations\Migration002(),
    ];
    Migrations::runPluginMigrations($migrations);

    Tools::log()->notice('MiPlugin actualizado correctamente');
}
```

### 3.4 Metodo uninstall()

Se ejecuta SOLO cuando:

1. El plugin se desactiva con el flag `post_disable = true`
2. El lock del uninstall se gestiona automaticamente

Aqui se deben:

- Eliminar tablas propias del plugin
- Limpiar datos de configuracion
- Restaurar datos al estado anterior

```php
public function uninstall(): void
{
    // Eliminar tabla del plugin si existe
    if ($this->tables->tableExists('tabla_custom')) {
        $this->tables->exec('DROP TABLE tabla_custom;');
    }

    // Limpiar datos relacionados
    // NO eliminar datos compartidos con otros plugins

    Tools::log()->notice('MiPlugin desinstalado correctamente');
}
```

### 3.5 Metodos Utiles Disponibles

Dentro de la clase `Init`, heredada de `InitClass`, estan disponibles:

```php
// Acceso a la base de datos
$this->tables;  // Instancia DataBase

// Comprobar si es la primera vez que se ejecuta
$this->myFirstTime(): bool;

// Acceso a configuracion
Tools::config('key', 'default');
Tools::settings('section', 'key', 'default');
Tools::settingsSet('section', 'key', 'value');
Tools::settingsSave();

// Logging
Tools::log()->notice('mensaje');
Tools::log()->warning('aviso');
Tools::log()->error('error');
Tools::log()->debug('debug');

// Traducciones
Tools::trans('key', ['%param%' => 'valor']);

// Obtener carpeta del plugin
$pluginFolder = $this->getFolder();  // Devuelve ruta del plugin
```

---

## 4. Ciclo de Vida Completo del Plugin

### 4.1 Flujo de Instalacion

```
1. Usuario sube ZIP del plugin
2. FacturaScripts extrae el ZIP en Plugins/NombrePlugin/
3. Lee facturascripts.ini y valida compatibilidad
4. Añade plugin a MyFiles/plugins.json (instalado pero no activado)
5. Se puede proceder a activar
```

### 4.2 Flujo de Activacion

```
1. Usuario activa el plugin desde AdminPlugins
2. FacturaScripts:
   a) Valida dependencias (plugins requeridos, extensiones PHP)
   b) Valida que carpeta == nombre en facturascripts.ini
   c) Marca post_enable = true en plugins.json
   d) Ejecuta Plugins::deploy() que:
      - Crea enlaces dinamicos en Dinamic/Controller, Dinamic/Model, etc.
      - Fusiona XMLView con extensiones
      - Ejecuta Migrations::run() del core
      - Reconstruye rutas y cachés
      - Ejecuta PluginsDeploy::initControllers()
   e) Llama init() de Init.php con post_enable=true
   f) Ejecuta update() si post_enable=true
   g) Ejecuta init() en cada request
```

### 4.3 Flujo de Desactivacion

```
1. Usuario desactiva el plugin desde AdminPlugins
2. FacturaScripts:
   a) Marca post_disable = true en plugins.json
   b) Ejecuta Plugins::deploy() que regenera todo
   c) Llama init() de Init.php con post_disable=true
   d) Ejecuta uninstall() si post_disable=true
   e) Limpia las referencias del plugin
```

### 4.4 Flujo de Eliminacion

```
1. Plugin DEBE estar desactivado
2. Usuario elimina plugin desde AdminPlugins
3. FacturaScripts:
   a) Elimina directorio Plugins/NombrePlugin/
   b) Elimina entrada de MyFiles/plugins.json
3. Plugin ya no esta disponible
```

### 4.5 Flujo de Actualizacion

```
1. Plugin DEBE estar activo
2. Usuario carga versión nueva
3. FacturaScripts:
   a) Detecta version diferente en facturascripts.ini
   b) Reemplaza archivos del plugin
   c) Marca post_enable = true
   d) Ejecuta update() en Init.php
   e) Ejecuta deploy() nuevamente
```

---

## 5. Sistema Mod (Hooks y Modificadores)

### 5.1 Concepto Fundamental

El sistema `Mod` permite que plugins extiendan la funcionalidad del core sin modificar archivos del core. Se implementan mediante interfaces que deben cumplir ciertas firmas de metodos.

Los Mods se usan para:

- Modificar calculos de impuestos
- Personalizar validaciones
- Extender comportamiento de documentos
- Cambiar comportamiento de exportacion/importacion

### 5.2 Interfaz CalculatorModInterface

Esta es la interfaz MOD principal para personalizar calculos:

```php
namespace FacturaScripts\Core\Contract;

interface CalculatorModInterface
{
    /**
     * Aplica modificaciones a un documento completo
     * Se ejecuta ANTES de recalcular
     *
     * @param BusinessDocument $doc Documento a modificar
     * @param BusinessDocumentLine[] $lines Lineas del documento
     * @return bool true si todo fue correcto, false si hay error
     */
    public function apply(BusinessDocument &$doc, array &$lines): bool;

    /**
     * Calcula valores a nivel de documento
     * Se ejecuta DESPUES de apply()
     *
     * @param BusinessDocument $doc Documento
     * @param BusinessDocumentLine[] $lines Lineas
     * @return bool true si todo fue correcto
     */
    public function calculate(BusinessDocument &$doc, array &$lines): bool;

    /**
     * Calcula valores a nivel de LINEA
     * Se ejecuta para cada linea nueva
     *
     * @param BusinessDocument $doc Documento padre
     * @param BusinessDocumentLine $line Linea a calcular
     * @return bool true si todo fue correcto
     */
    public function calculateLine(BusinessDocument $doc, BusinessDocumentLine &$line): bool;

    /**
     * Limpia valores especificos
     * Se ejecuta ANTES de apply()
     *
     * @param BusinessDocument $doc Documento
     * @param BusinessDocumentLine[] $lines Lineas
     * @return bool true si todo fue correcto
     */
    public function clear(BusinessDocument &$doc, array &$lines): bool;

    /**
     * Calcula subtotales por impuesto
     * Estructura especifica para España con IVA, IRPF, etc.
     *
     * @param array $subtotals Array de subtotales (referencia)
     * @param BusinessDocument $doc Documento
     * @param BusinessDocumentLine[] $lines Lineas
     * @return bool true si todo fue correcto
     */
    public function getSubtotals(array &$subtotals, BusinessDocument $doc, array $lines): bool;
}
```

### 5.3 Ejemplo Completo de CalculatorMod

```php
<?php

namespace FacturaScripts\Plugins\MiPlugin\Mod;

use FacturaScripts\Core\Contract\CalculatorModInterface;
use FacturaScripts\Core\Model\Base\BusinessDocument;
use FacturaScripts\Core\Model\Base\BusinessDocumentLine;
use FacturaScripts\Core\Tools;

class MiCalculatorMod implements CalculatorModInterface
{
    public function apply(BusinessDocument &$doc, array &$lines): bool
    {
        // Aplicar cambios PREVIOS al calculo
        // Por ejemplo, modificar descuentos segun cliente
        if ($doc->subjectColumn() === 'codcliente') {
            // Es una venta
            $subject = $doc->getSubject();
            if ($subject->esempresa) {
                // Cliente empresa: aplicar descuento extra
                foreach ($lines as &$line) {
                    $line->dtopor = max($line->dtopor, 5.0);
                }
            }
        }
        return true;
    }

    public function calculate(BusinessDocument &$doc, array &$lines): bool
    {
        // Calcular valores a nivel DOCUMENTO despues de apply()
        // Por ejemplo, aplicar un descuento fijo adicional
        $totalBruto = array_sum(array_map(function($line) {
            return $line->pvptotal;
        }, $lines));

        if ($totalBruto > 1000) {
            // Gran pedido: aplicar descuento adicional
            $doc->dtopor1 = 10.0;
        }
        return true;
    }

    public function calculateLine(BusinessDocument $doc, BusinessDocumentLine &$line): bool
    {
        // Calcular valores a nivel LINEA
        // Se ejecuta cuando se crea una nueva linea
        if (empty($line->id())) {
            // Es una linea nueva
            // Ejemplo: multiplicar precio por factor
            $line->pvpunitario = $line->pvpunitario * 1.05;
        }
        return true;
    }

    public function clear(BusinessDocument &$doc, array &$lines): bool
    {
        // Limpiar valores especificos ANTES de apply()
        // Por ejemplo, resetear descuentos previos
        return true;
    }

    public function getSubtotals(array &$subtotals, BusinessDocument $doc, array $lines): bool
    {
        // Personalizar estructura de subtotales
        // IMPORTANTE: Esta estructura es muy especifica para España
        // Debe mantener los campos estandar

        // Por defecto, la clase base ya maneja:
        // - subtotals['iva'] = array de impuestos
        // - subtotals['totaliva'] = total IVA
        // - subtotals['neto'] = neto sin impuestos

        // Aqui se pueden AÑADIR campos personalizados:
        $subtotals['descuento_custom'] = 0.0;

        foreach ($lines as $line) {
            if ($line->referencia === 'PROMO') {
                $subtotals['descuento_custom'] += $line->pvptotal;
            }
        }

        return true;
    }
}
```

### 5.4 Registrar un Mod en Init.php

Para que FacturaScripts reconozca un Mod, debe estar en el directorio `Mod/` del plugin:

```
Plugins/MiPlugin/
└── Mod/
    └── MiCalculatorMod.php
```

FacturaScripts detecta automaticamente los Mods que implementan interfaces del core durante el `deploy()`.

### 5.5 Otros Tipos de Mods Posibles

Aunque el ejemplo detallado es `CalculatorModInterface`, el sistema esta diseñado para permitir otras interfaces:

- Mods para validacion
- Mods para exportacion
- Mods para importacion
- Mods para transformacion de datos

Cualquier interfaz en `FacturaScripts\Core\Contract\*Interface` puede ser implementada en `Plugins/NombrePlugin/Mod/*`.

---

## 6. Crear Modelos en un Plugin

### 6.1 Estructura de Directorio

Los modelos deben ir en `Plugins/NombrePlugin/Model/`:

```
Plugins/MiPlugin/
├── Table/
│   └── servicioCliente.xml
└── Model/
    └── ServicioCliente.php
```

### 6.2 Archivo XML de Tabla

Primero se define la tabla en XML:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<table>
    <name>servicios_cliente</name>
    <primaryKey>id</primaryKey>
    <column>
        <name>id</name>
        <type>serial</type>
        <null>NO</null>
    </column>
    <column>
        <name>codcliente</name>
        <type>varchar</type>
        <length>6</length>
        <null>NO</null>
    </column>
    <column>
        <name>descripcion</name>
        <type>varchar</type>
        <length>255</length>
        <null>YES</null>
    </column>
    <column>
        <name>precio</name>
        <type>numeric</type>
        <numericPrecision>12</numericPrecision>
        <numericScale>2</numericScale>
        <null>NO</null>
        <default>0.00</default>
    </column>
    <column>
        <name>fecha</name>
        <type>datetime</type>
        <null>YES</null>
    </column>
    <column>
        <name>activo</name>
        <type>tinyint</type>
        <null>NO</null>
        <default>1</default>
    </column>
    <constraint>
        <name>servicios_cliente_ibfk_1</name>
        <type>foreign</type>
        <columns>codcliente</columns>
        <references>clientes(codcliente)</references>
        <onUpdate>CASCADE</onUpdate>
        <onDelete>CASCADE</onDelete>
    </constraint>
    <index>
        <name>ix_servicios_cliente_codcliente</name>
        <columns>codcliente</columns>
    </index>
</table>
```

### 6.3 Clase Model

Luego se crea la clase modelo:

```php
<?php

namespace FacturaScripts\Plugins\MiPlugin\Model;

use FacturaScripts\Core\Model\Base\ModelClass;

class ServicioCliente extends ModelClass
{
    /**
     * Nombre de la tabla de base de datos
     *
     * @return string
     */
    public static function tableName(): string
    {
        return 'servicios_cliente';
    }

    /**
     * Nombre de la columna primaria
     *
     * @return string
     */
    public static function primaryColumn(): string
    {
        return 'id';
    }

    // Propiedades del modelo
    public $id = null;
    public $codcliente = '';
    public $descripcion = '';
    public $precio = 0.00;
    public $fecha = null;
    public $activo = 1;

    /**
     * Obtener todos los servicios de un cliente
     *
     * @param string $codcliente Codigo del cliente
     * @return array Array de objetos ServicioCliente
     */
    public function getAllByCliente($codcliente)
    {
        $where = ['codcliente' => $codcliente];
        return $this->all($where);
    }

    /**
     * Validacion personalizada
     *
     * @return bool true si es valido
     */
    public function test(): bool
    {
        if (empty($this->codcliente)) {
            $this->toolBox()->i18nLog()->error('cliente-requerido');
            return false;
        }

        if ($this->precio < 0) {
            $this->toolBox()->i18nLog()->error('precio-debe-ser-positivo');
            return false;
        }

        return parent::test();
    }
}
```

### 6.4 Tipos de Datos XML Disponibles

| Tipo XML | Tipo MySQL | Descripcion |
|----------|-----------|-------------|
| `serial` | AUTO_INCREMENT INT | Entero auto incremento |
| `varchar` | VARCHAR(n) | Texto variable con length |
| `text` | TEXT | Texto largo |
| `integer` | INT | Entero |
| `numeric` | DECIMAL(p,s) | Decimal precision |
| `float` | FLOAT | Punto flotante |
| `boolean` | TINYINT(1) | Booleano 0/1 |
| `date` | DATE | Fecha YYYY-MM-DD |
| `datetime` | DATETIME | Fecha y hora |
| `time` | TIME | Hora HH:MM:SS |
| `json` | JSON | Datos JSON |

---

## 7. Crear Controladores en un Plugin

### 7.1 ListController Personalizado

```php
<?php

namespace FacturaScripts\Plugins\MiPlugin\Controller;

use FacturaScripts\Core\Lib\ExtendedController\ListController;
use FacturaScripts\Core\Tools;
use FacturaScripts\Core\Base\DataBase\DataBaseWhere;

class ListServicioCliente extends ListController
{
    /**
     * Metadata de la pagina: titulo, menu, icono
     *
     * @return array
     */
    public function getPageData(): array
    {
        $data = parent::getPageData();
        $data['menu'] = 'sales';              // Menu donde aparece
        $data['title'] = 'servicios-cliente'; // Clave traduccion
        $data['icon'] = 'fa-solid fa-wrench'; // Icono FontAwesome
        return $data;
    }

    /**
     * Crear vistas del controlador
     */
    protected function createViews()
    {
        // Vista principal de lista
        $this->createListView('ListServicioCliente', 'ServicioCliente', 'servicios-cliente', 'fa-solid fa-wrench');

        $mainView = $this->views['ListServicioCliente'];

        // Campos de busqueda
        $mainView->addSearchFields([
            'codcliente',
            'descripcion'
        ]);

        // Campos para ordenar
        $mainView->addOrderBy(['codcliente'], 'customer', 1);
        $mainView->addOrderBy(['descripcion'], 'description');
        $mainView->addOrderBy(['precio'], 'price');
        $mainView->addOrderBy(['fecha'], 'date');

        // Filtros
        $this->addFilterSelect(
            'ListServicioCliente',
            'activo',
            'active',
            'activo',
            [
                ['code' => '1', 'description' => Tools::trans('active')],
                ['code' => '0', 'description' => Tools::trans('inactive')]
            ]
        );

        // Filtro con donde
        $this->addFilterSelectWhere(
            'ListServicioCliente',
            'tipo',
            'type',
            [
                [
                    'label' => Tools::trans('active'),
                    'where' => [new DataBaseWhere('activo', 1)]
                ],
                [
                    'label' => Tools::trans('all'),
                    'where' => []
                ]
            ]
        );

        // Configurar vista
        $this->setSettings('ListServicioCliente', 'checkBoxes', true);
        $this->setSettings('ListServicioCliente', 'btnNew', true);
        $this->setSettings('ListServicioCliente', 'btnPrint', true);
    }
}
```

### 7.2 EditController Personalizado

```php
<?php

namespace FacturaScripts\Plugins\MiPlugin\Controller;

use FacturaScripts\Core\Lib\ExtendedController\EditController;
use FacturaScripts\Core\Tools;

class EditServicioCliente extends EditController
{
    /**
     * Nombre del modelo principal
     *
     * @return string
     */
    public function getModelClassName(): string
    {
        return 'ServicioCliente';
    }

    /**
     * Metadata de la pagina
     *
     * @return array
     */
    public function getPageData(): array
    {
        $data = parent::getPageData();
        $data['menu'] = 'sales';
        $data['title'] = 'servicio-cliente';
        $data['icon'] = 'fa-solid fa-wrench';
        return $data;
    }

    /**
     * Crear vistas (pestañas)
     */
    protected function createViews()
    {
        // Vista principal de edicion
        parent::createViews();

        // Personalizar vista principal
        $this->createEditView('EditServicioCliente', 'ServicioCliente', 'general', 'fa-solid fa-pencil');

        // Vista relacionada de facturas del cliente
        $this->addListView('ListFacturaCliente', 'FacturaCliente', 'invoices', 'fa-solid fa-file-invoice');
    }

    /**
     * Ejecutar acciones POST
     *
     * @param string $action
     * @return bool
     */
    protected function execPreviousAction($action)
    {
        if ($action === 'custom-action') {
            return $this->customAction();
        }

        return parent::execPreviousAction($action);
    }

    /**
     * Accion personalizada
     *
     * @return bool
     */
    private function customAction(): bool
    {
        Tools::log()->notice('Accion personalizada ejecutada');
        return true;
    }
}
```

### 7.3 PanelController con Multiples Pestañas

```php
<?php

namespace FacturaScripts\Plugins\MiPlugin\Controller;

use FacturaScripts\Core\Lib\ExtendedController\PanelController;
use FacturaScripts\Core\Tools;

class AdminServicios extends PanelController
{
    public function getPageData(): array
    {
        $data = parent::getPageData();
        $data['menu'] = 'admin';
        $data['title'] = 'servicios-admin';
        $data['icon'] = 'fa-solid fa-gears';
        return $data;
    }

    protected function createViews()
    {
        // Pestaña 1: Lista de servicios
        $this->addListView('ListServicios', 'ServicioCliente', 'servicios', 'fa-solid fa-list');

        // Pestaña 2: Resumen
        $this->createTemplate('ListResumen');

        // Pestaña 3: Configuracion
        $this->createTemplate('ListConfig');
    }
}
```

### 7.4 getPageData() - Metadata Completa

El metodo `getPageData()` debe devolver un array con esta estructura:

```php
public function getPageData(): array
{
    return [
        'name' => 'ControllerName',        // Nombre controlador (autom.)
        'title' => 'translation-key',      // Clave para traduccion
        'menu' => 'sales',                 // Menu principal donde aparece
        'submenu' => 'sub-menu-name',      // Submenu (opcional)
        'icon' => 'fa-solid fa-icon',      // Icono FontAwesome 6
        'showonmenu' => true,              // Mostrar en menu
        'order' => 100,                    // Orden en el menu
    ];
}
```

Menus disponibles: `admin`, `sales`, `buying`, `warehouse`, `accounting`, `tools`

---

## 8. Crear Vistas en un Plugin

### 8.1 Vistas XML para ListController

```xml
<?xml version="1.0" encoding="UTF-8"?>
<view>
    <!-- Definir columnas principales -->
    <columns>
        <column>
            <name>id</name>
            <title>id</title>
            <type>text</type>
            <display>none</display>
        </column>
        <column>
            <name>codcliente</name>
            <title>customer</title>
            <type>text</type>
        </column>
        <column>
            <name>descripcion</name>
            <title>description</title>
            <type>text</type>
        </column>
        <column>
            <name>precio</name>
            <title>price</title>
            <type>money</type>
        </column>
        <column>
            <name>fecha</name>
            <title>date</title>
            <type>date</type>
        </column>
        <column>
            <name>activo</name>
            <title>active</title>
            <type>toggle</type>
        </column>
    </columns>
</view>
```

### 8.2 Vistas XML para EditController

```xml
<?xml version="1.0" encoding="UTF-8"?>
<view>
    <sections>
        <!-- Seccion 1: Informacion General -->
        <section>
            <name>general</name>
            <description>Informacion General</description>
            <columns>2</columns>
            <rows>
                <row>
                    <fieldname>codcliente</fieldname>
                    <fieldname>precio</fieldname>
                </row>
                <row>
                    <fieldname>descripcion</fieldname>
                    <fieldname>fecha</fieldname>
                </row>
                <row>
                    <fieldname>activo</fieldname>
                </row>
            </rows>
        </section>
    </sections>
</view>
```

### 8.3 Tipos de Campos en XMLView

| Tipo | Descripcion | Atributos |
|------|-------------|-----------|
| `text` | Texto simple | readonly, maxlength |
| `password` | Contraseña | - |
| `email` | Email | - |
| `number` | Numero | min, max, step |
| `date` | Fecha | - |
| `datetime` | Fecha y hora | - |
| `money` | Dinero formateado | - |
| `percentage` | Porcentaje | - |
| `select` | Desplegable | icon, addsearch, onchange |
| `autocomplete` | Autocompletado | icon |
| `checkbox` | Casilla verificacion | - |
| `toggle` | Boton si/no | - |
| `textarea` | Area texto | rows, cols |
| `html` | Editor HTML | - |
| `json` | Editor JSON | - |
| `file` | Carga archivo | accept |

### 8.4 Plantillas Twig Personalizadas

En `Plugins/MiPlugin/View/` se pueden crear plantillas Twig:

```twig
{% extends "Master/PanelController.html.twig" %}

{% block content %}
<div class="container-fluid">
    <h2>{{ trans('titulo-personalizado') }}</h2>

    {% if datos %}
        <table class="table table-striped">
            <thead>
                <tr>
                    <th>{{ trans('columna1') }}</th>
                    <th>{{ trans('columna2') }}</th>
                </tr>
            </thead>
            <tbody>
                {% for item in datos %}
                    <tr>
                        <td>{{ item.campo1 }}</td>
                        <td>{{ item.campo2 }}</td>
                    </tr>
                {% endfor %}
            </tbody>
        </table>
    {% else %}
        <p class="alert alert-info">{{ trans('sin-datos') }}</p>
    {% endif %}
</div>
{% endblock %}
```

### 8.5 Extender Vistas del Core

Para extender una vista del core con contenido personalizado, crear en:

```
Plugins/MiPlugin/Extension/XMLView/
```

Por ejemplo, para extender `EditCliente.xml`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<view>
    <sections>
        <section>
            <name>servicios</name>
            <description>Servicios del Cliente</description>
            <columns>1</columns>
            <rows>
                <row>
                    <fieldname>servicios_activos</fieldname>
                </row>
            </rows>
        </section>
    </sections>
</view>
```

FacturaScripts fusionara automaticamente esta extension con la vista original durante `PluginsDeploy::run()`.

---

## 9. Crear un Worker

### 9.1 Concepto de Worker

Un Worker es una clase que se ejecuta periodicamente en background. Ideal para:

- Enviar correos programados
- Procesar datos en lote
- Ejecutar tareas largas sin bloquear
- Mantenimiento de base de datos

### 9.2 Estructura del Worker

```php
<?php

namespace FacturaScripts\Plugins\MiPlugin\Worker;

use FacturaScripts\Core\Base\Worker;
use FacturaScripts\Core\Tools;

class MiWorker extends Worker
{
    /**
     * Nombre unico del worker
     *
     * @return string
     */
    public static function name(): string
    {
        return 'mi-worker';
    }

    /**
     * Metodo principal que se ejecuta
     *
     * @return bool true si completado
     */
    public function run(): bool
    {
        Tools::log()->info('MiWorker ejecutandose...');

        // Obtener registros sin procesar
        $servicios = $this->getUnprocessedServicios();

        if (empty($servicios)) {
            Tools::log()->info('No hay servicios pendientes');
            return true;
        }

        // Procesar cada registro
        foreach ($servicios as $servicio) {
            try {
                $this->processServicio($servicio);
                $servicio->save();
            } catch (\Exception $e) {
                Tools::log()->error('Error procesando servicio: ' . $e->getMessage());
            }
        }

        Tools::log()->info('MiWorker completado');
        return true;
    }

    /**
     * Obtener servicios sin procesar
     *
     * @return array
     */
    private function getUnprocessedServicios(): array
    {
        // SQL para obtener registros a procesar
        $sql = "SELECT * FROM servicios_cliente WHERE procesado = 0 LIMIT 100";
        return $this->database->select($sql);
    }

    /**
     * Procesar un servicio individual
     *
     * @param array $servicio
     * @return void
     */
    private function processServicio($servicio): void
    {
        // Lógica de procesamiento
        $servicio['procesado'] = 1;
        $servicio['fecha_procesamiento'] = date('Y-m-d H:i:s');

        // Actualizar en base de datos
        $this->database->update(
            'servicios_cliente',
            $servicio,
            "id = " . intval($servicio['id'])
        );
    }
}
```

### 9.3 Registrar Worker en Init.php

```php
public function init(): void
{
    // Registrar el worker
    // Los workers se ejecutan segun la configuracion del sistema
    // Tipicamente cada 5-15 minutos

    Tools::log()->debug('MiPlugin con worker registrado');
}
```

Los workers se detectan automaticamente en el directorio `Worker/` durante `PluginsDeploy::run()`.

---

## 10. Sistema de Migraciones

### 10.1 Migraciones Automaticas via XML

Las migraciones mas simples ocurren automaticamente cuando se crea una tabla XML:

1. FacturaScripts detecta el archivo XML en `Table/`
2. En `update()` automaticamente crea la tabla si no existe
3. En `uninstall()` puede eliminarse

### 10.2 Migraciones Manuales en Init.php

Para cambios complejos, usar la clase `MigrationClass`:

```php
<?php

namespace FacturaScripts\Plugins\MiPlugin\Migrations;

use FacturaScripts\Core\Template\MigrationClass;

class Migration001 extends MigrationClass
{
    /**
     * Nombre unico de la migracion
     *
     * @return string
     */
    public function getFullMigrationName(): string
    {
        return 'MiPlugin_Migration_001';
    }

    /**
     * Ejecutar la migracion
     *
     * @return void
     */
    public function run(): void
    {
        // Crear tabla si no existe
        if (!$this->database->tableExists('tabla_custom')) {
            $sql = "CREATE TABLE tabla_custom (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(255) NOT NULL,
                fecha DATETIME DEFAULT CURRENT_TIMESTAMP
            )";
            $this->database->exec($sql);
        }

        // Añadir columna si no existe
        $this->addTableField('tabla_custom', 'nuevo_campo', 'varchar(100)');

        // Actualizar datos
        $sql = "UPDATE tabla_custom SET nombre = 'Valor' WHERE nombre IS NULL";
        $this->database->exec($sql);
    }
}
```

### 10.3 Usar Migraciones en update()

```php
public function update(): void
{
    $migrations = [
        new \FacturaScripts\Plugins\MiPlugin\Migrations\Migration001(),
        new \FacturaScripts\Plugins\MiPlugin\Migrations\Migration002(),
    ];

    Migrations::runPluginMigrations($migrations);

    Tools::log()->notice('Migraciones completadas');
}
```

### 10.4 Metodos Utiles en MigrationClass

```php
// Comprobar si tabla existe
$this->database->tableExists('nombre_tabla')

// Ejecutar SQL
$this->database->exec('SQL QUERY')

// Seleccionar datos
$results = $this->database->select('SELECT ...')

// Añadir campo
$this->addTableField('tabla', 'campo', 'VARCHAR(100)')

// Modificar campo
$this->modifyTableField('tabla', 'campo', 'INT')

// Eliminar campo
$this->dropTableField('tabla', 'campo')
```

---

## 11. Traducciones en Plugins

### 11.1 Estructura de Carpeta

Las traducciones van en `Plugins/MiPlugin/Translation/`:

```
Plugins/MiPlugin/Translation/
├── es_ES.json
├── en_EN.json
├── ca_ES.json
└── fr_FR.json
```

### 11.2 Formato de Archivo JSON

```json
{
  "mi-plugin": "Mi Plugin",
  "servicios-cliente": "Servicios del Cliente",
  "servicio-cliente": "Servicio del Cliente",
  "descripcion": "Descripcion",
  "precio": "Precio",
  "cliente-requerido": "El cliente es requerido",
  "precio-debe-ser-positivo": "El precio debe ser positivo",
  "servicios-admin": "Administracion de Servicios",
  "sin-datos": "No hay datos disponibles",
  "columna1": "Primera Columna",
  "columna2": "Segunda Columna",
  "titulo-personalizado": "Titulo Personalizado"
}
```

### 11.3 Usar Traducciones en Codigo

En PHP:

```php
// Simple
Tools::trans('clave-traduccion');

// Con parametros
Tools::trans('mensaje', ['%nombre%' => 'Carlos']);

// En validaciones
$this->toolBox()->i18nLog()->error('error-key');
$this->toolBox()->i18nLog()->warning('warning-key');
$this->toolBox()->i18nLog()->notice('notice-key');
```

En Twig:

```twig
{{ trans('clave-traduccion') }}
{{ trans('mensaje', {'%nombre%': 'Carlos'}) }}
```

En XMLView:

```xml
<column>
    <title>clave-traduccion</title>
</column>
```

### 11.4 Convenciones de Nomenclatura

- `controlador-nombre`: Nombre de controlador
- `modelo-nombre`: Nombre de modelo
- `campo-nombre`: Nombre de campo
- `accion-descripcion`: Descripcion de accion
- `error-mensaje`: Mensaje de error
- `warning-mensaje`: Mensaje de advertencia
- `info-mensaje`: Mensaje informativo

---

## 12. Assets CSS/JavaScript

### 12.1 Estructura de Assets

```
Plugins/MiPlugin/Assets/
├── CSS/
│   └── custom-styles.css
├── JS/
│   └── custom-script.js
└── images/
    └── icon.png
```

### 12.2 Incluir CSS en Vistas

En Twig:

```twig
{% set css_files = css_files|default([])|merge([
    asset('Plugins/MiPlugin/Assets/CSS/custom-styles.css')
]) %}

<link rel="stylesheet" href="{{ asset('Plugins/MiPlugin/Assets/CSS/custom-styles.css') }}">
```

En XMLView (no es el metodo principal pero posible):

Las vistas XML se renderizan en Twig, por lo que CSS se añade en la plantilla base.

### 12.3 Incluir JavaScript en Vistas

```twig
{% set js_files = js_files|default([])|merge([
    asset('Plugins/MiPlugin/Assets/JS/custom-script.js')
]) %}

<script src="{{ asset('Plugins/MiPlugin/Assets/JS/custom-script.js') }}"></script>
```

### 12.4 Ejemplo de CSS Personalizado

```css
/* Plugins/MiPlugin/Assets/CSS/custom-styles.css */

.miplugin-container {
    padding: 20px;
    background-color: #f5f5f5;
    border-radius: 4px;
}

.miplugin-alert {
    color: #d9534f;
    font-weight: bold;
    margin: 10px 0;
}

.miplugin-button {
    background-color: #337ab7;
    color: white;
    padding: 10px 20px;
    border-radius: 3px;
    cursor: pointer;
}

.miplugin-button:hover {
    background-color: #286090;
}
```

### 12.5 Ejemplo de JavaScript

```javascript
// Plugins/MiPlugin/Assets/JS/custom-script.js

document.addEventListener('DOMContentLoaded', function() {
    console.log('MiPlugin scripts loaded');

    // Obtener referencia a elemento
    const container = document.querySelector('.miplugin-container');
    if (container) {
        container.addEventListener('click', function() {
            console.log('Container clicked');
        });
    }

    // Función personalizada
    window.miPluginFunction = function(param) {
        console.log('Custom function called with:', param);
        return true;
    };
});
```

### 12.6 Acceder a Assets en Templates

```twig
<!-- En plantillas Twig -->
<link rel="stylesheet" href="{{ asset('Plugins/MiPlugin/Assets/CSS/custom-styles.css') }}">
<img src="{{ asset('Plugins/MiPlugin/Assets/images/icon.png') }}" alt="Icon">
<script src="{{ asset('Plugins/MiPlugin/Assets/JS/custom-script.js') }}"></script>
```

---

## 13. Ejemplo Completo: Plugin Personalizado

### 13.1 Resumen: Plugin GestorServicios

Crearemos un plugin completo que:

1. Define una tabla `servicios_cliente` con servicios adicionales
2. Crea List y Edit controllers
3. Permite gestionar servicios por cliente
4. Tiene migraciones y traducciones
5. Incluye un Mod para personalizar calculos

### 13.2 Estructura Final

```
Plugins/GestorServicios/
├── facturascripts.ini
├── Init.php
├── Controller/
│   ├── ListServicioCliente.php
│   └── EditServicioCliente.php
├── Model/
│   └── ServicioCliente.php
├── Table/
│   └── servicioCliente.xml
├── XMLView/
│   ├── ListServicioCliente.xml
│   └── EditServicioCliente.xml
├── Mod/
│   └── ServiciosCalculatorMod.php
├── Migrations/
│   └── Migration001.php
├── Translation/
│   └── es_ES.json
├── Assets/
│   └── CSS/
│       └── servicios.css
└── View/
    └── custom-panel.html.twig
```

### 13.3 1. facturascripts.ini

```ini
[plugin]
name = GestorServicios
description = Gestor de Servicios Adicionales para Clientes
version = 1.0.0
min_version = 2025
min_php = 8.1
require =
require_php = curl,json,pdo
hidden = false
```

### 13.4 2. Init.php Completo

```php
<?php

namespace FacturaScripts\Plugins\GestorServicios;

use FacturaScripts\Core\Base\InitClass;
use FacturaScripts\Core\Migrations;
use FacturaScripts\Core\Tools;

class Init extends InitClass
{
    public function init(): void
    {
        // Se ejecuta en cada carga si el plugin esta activo
        Tools::log()->debug('GestorServicios plugin activo');
    }

    public function update(): void
    {
        // Ejecutar migraciones
        $migrations = [
            new Migrations\Migration001(),
        ];

        Migrations::runPluginMigrations($migrations);

        Tools::log()->notice('GestorServicios actualizado correctamente');
    }

    public function uninstall(): void
    {
        // Eliminar tabla si existe
        if ($this->tables->tableExists('servicios_cliente')) {
            $this->tables->exec('DROP TABLE servicios_cliente');
        }

        Tools::log()->notice('GestorServicios desinstalado');
    }
}
```

### 13.5 3. Model - ServicioCliente.php

```php
<?php

namespace FacturaScripts\Plugins\GestorServicios\Model;

use FacturaScripts\Core\Model\Base\ModelClass;

class ServicioCliente extends ModelClass
{
    public static function tableName(): string
    {
        return 'servicios_cliente';
    }

    public static function primaryColumn(): string
    {
        return 'id';
    }

    public $id = null;
    public $codcliente = '';
    public $descripcion = '';
    public $precio = 0.00;
    public $cantidad = 1;
    public $fecha_inicio = null;
    public $fecha_fin = null;
    public $activo = 1;

    public function test(): bool
    {
        if (empty($this->codcliente)) {
            $this->toolBox()->i18nLog()->error('cliente-requerido');
            return false;
        }

        if (empty($this->descripcion)) {
            $this->toolBox()->i18nLog()->error('descripcion-requerida');
            return false;
        }

        if ($this->precio < 0) {
            $this->toolBox()->i18nLog()->error('precio-positivo');
            return false;
        }

        return parent::test();
    }

    public function getClienteName(): string
    {
        // Obtener nombre del cliente
        $sql = "SELECT nombre FROM clientes WHERE codcliente = " . $this->database->var2str($this->codcliente);
        $result = $this->database->select($sql);
        return !empty($result) ? $result[0]['nombre'] : 'Desconocido';
    }

    public function totalMensual(): float
    {
        return $this->precio * $this->cantidad;
    }
}
```

### 13.6 4. Table XML - servicioCliente.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<table>
    <name>servicios_cliente</name>
    <primaryKey>id</primaryKey>
    <column>
        <name>id</name>
        <type>serial</type>
        <null>NO</null>
    </column>
    <column>
        <name>codcliente</name>
        <type>varchar</type>
        <length>6</length>
        <null>NO</null>
    </column>
    <column>
        <name>descripcion</name>
        <type>varchar</type>
        <length>255</length>
        <null>NO</null>
    </column>
    <column>
        <name>precio</name>
        <type>numeric</type>
        <numericPrecision>12</numericPrecision>
        <numericScale>2</numericScale>
        <null>NO</null>
        <default>0.00</default>
    </column>
    <column>
        <name>cantidad</name>
        <type>integer</type>
        <null>NO</null>
        <default>1</default>
    </column>
    <column>
        <name>fecha_inicio</name>
        <type>date</type>
        <null>YES</null>
    </column>
    <column>
        <name>fecha_fin</name>
        <type>date</type>
        <null>YES</null>
    </column>
    <column>
        <name>activo</name>
        <type>tinyint</type>
        <null>NO</null>
        <default>1</default>
    </column>
    <constraint>
        <name>servicios_cliente_ibfk_1</name>
        <type>foreign</type>
        <columns>codcliente</columns>
        <references>clientes(codcliente)</references>
        <onUpdate>CASCADE</onUpdate>
        <onDelete>CASCADE</onDelete>
    </constraint>
    <index>
        <name>ix_servicios_cliente_codcliente</name>
        <columns>codcliente</columns>
    </index>
</table>
```

### 13.7 5. ListServicioCliente.php Controller

```php
<?php

namespace FacturaScripts\Plugins\GestorServicios\Controller;

use FacturaScripts\Core\Lib\ExtendedController\ListController;
use FacturaScripts\Core\Tools;
use FacturaScripts\Core\Base\DataBase\DataBaseWhere;

class ListServicioCliente extends ListController
{
    public function getPageData(): array
    {
        $data = parent::getPageData();
        $data['menu'] = 'sales';
        $data['title'] = 'servicios-cliente';
        $data['icon'] = 'fa-solid fa-cogs';
        return $data;
    }

    protected function createViews()
    {
        $this->createListView('ListServicioCliente', 'ServicioCliente', 'servicios-cliente', 'fa-solid fa-cogs');

        $mainView = $this->views['ListServicioCliente'];
        $mainView->addSearchFields(['codcliente', 'descripcion']);
        $mainView->addOrderBy(['codcliente'], 'customer', 1);
        $mainView->addOrderBy(['descripcion'], 'description');
        $mainView->addOrderBy(['precio'], 'price');
        $mainView->addOrderBy(['fecha_inicio'], 'start-date');

        $this->addFilterSelectWhere(
            'ListServicioCliente',
            'activo',
            'status',
            [
                [
                    'label' => Tools::trans('active'),
                    'where' => [new DataBaseWhere('activo', 1)]
                ],
                [
                    'label' => Tools::trans('inactive'),
                    'where' => [new DataBaseWhere('activo', 0)]
                ],
                [
                    'label' => Tools::trans('all'),
                    'where' => []
                ]
            ]
        );

        $this->setSettings('ListServicioCliente', 'checkBoxes', true);
    }
}
```

### 13.8 6. EditServicioCliente.php Controller

```php
<?php

namespace FacturaScripts\Plugins\GestorServicios\Controller;

use FacturaScripts\Core\Lib\ExtendedController\EditController;
use FacturaScripts\Core\Tools;

class EditServicioCliente extends EditController
{
    public function getModelClassName(): string
    {
        return 'ServicioCliente';
    }

    public function getPageData(): array
    {
        $data = parent::getPageData();
        $data['menu'] = 'sales';
        $data['title'] = 'servicio-cliente';
        $data['icon'] = 'fa-solid fa-cogs';
        return $data;
    }

    protected function createViews()
    {
        parent::createViews();

        $this->createEditView('EditServicioCliente', 'ServicioCliente', 'general', 'fa-solid fa-pencil');

        // Mostrar facturas del cliente (si el servicio esta guardado)
        if (!empty($this->getViewModelValue('EditServicioCliente', 'codcliente'))) {
            $codcliente = $this->getViewModelValue('EditServicioCliente', 'codcliente');
            $this->addListView('ListFacturaCliente', 'FacturaCliente', 'invoices', 'fa-solid fa-file-invoice')
                ->addWhereFromView('ListFacturaCliente', 'codcliente', $codcliente);
        }
    }
}
```

### 13.9 7. XMLView - ListServicioCliente.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<view>
    <columns>
        <column>
            <name>id</name>
            <title>id</title>
            <type>text</type>
            <display>none</display>
        </column>
        <column>
            <name>codcliente</name>
            <title>customer</title>
            <type>text</type>
        </column>
        <column>
            <name>descripcion</name>
            <title>description</title>
            <type>text</type>
        </column>
        <column>
            <name>precio</name>
            <title>price</title>
            <type>money</type>
        </column>
        <column>
            <name>cantidad</name>
            <title>quantity</title>
            <type>number</type>
        </column>
        <column>
            <name>fecha_inicio</name>
            <title>start-date</title>
            <type>date</type>
        </column>
        <column>
            <name>fecha_fin</name>
            <title>end-date</title>
            <type>date</type>
        </column>
        <column>
            <name>activo</name>
            <title>active</title>
            <type>toggle</type>
        </column>
    </columns>
</view>
```

### 13.10 8. XMLView - EditServicioCliente.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<view>
    <sections>
        <section>
            <name>general</name>
            <description>general-information</description>
            <columns>2</columns>
            <rows>
                <row>
                    <fieldname>codcliente</fieldname>
                    <fieldname>activo</fieldname>
                </row>
                <row>
                    <fieldname>descripcion</fieldname>
                </row>
                <row>
                    <fieldname>precio</fieldname>
                    <fieldname>cantidad</fieldname>
                </row>
                <row>
                    <fieldname>fecha_inicio</fieldname>
                    <fieldname>fecha_fin</fieldname>
                </row>
            </rows>
        </section>
    </sections>
</view>
```

### 13.11 9. Mod - ServiciosCalculatorMod.php

```php
<?php

namespace FacturaScripts\Plugins\GestorServicios\Mod;

use FacturaScripts\Core\Contract\CalculatorModInterface;
use FacturaScripts\Core\Model\Base\BusinessDocument;
use FacturaScripts\Core\Model\Base\BusinessDocumentLine;

class ServiciosCalculatorMod implements CalculatorModInterface
{
    public function apply(BusinessDocument &$doc, array &$lines): bool
    {
        return true;
    }

    public function calculate(BusinessDocument &$doc, array &$lines): bool
    {
        // Añadir servicios del cliente como lineas adicionales
        if ($doc->subjectColumn() === 'codcliente') {
            $codcliente = $doc->codcliente;
            $this->addClienteServicios($doc, $lines, $codcliente);
        }
        return true;
    }

    public function calculateLine(BusinessDocument $doc, BusinessDocumentLine &$line): bool
    {
        return true;
    }

    public function clear(BusinessDocument &$doc, array &$lines): bool
    {
        return true;
    }

    public function getSubtotals(array &$subtotals, BusinessDocument $doc, array $lines): bool
    {
        return true;
    }

    private function addClienteServicios(BusinessDocument &$doc, array &$lines, string $codcliente): void
    {
        // Obtener servicios activos del cliente
        // (Este es un ejemplo conceptual; requeriria acceso a base de datos)
    }
}
```

### 13.12 10. Migraciones - Migration001.php

```php
<?php

namespace FacturaScripts\Plugins\GestorServicios\Migrations;

use FacturaScripts\Core\Template\MigrationClass;

class Migration001 extends MigrationClass
{
    public function getFullMigrationName(): string
    {
        return 'GestorServicios_Migration_001_CreateTable';
    }

    public function run(): void
    {
        // Validar que la tabla se crea desde el XML
        if (!$this->database->tableExists('servicios_cliente')) {
            throw new \Exception('La tabla servicios_cliente no se creo correctamente');
        }

        // Insertar datos iniciales si es necesario
        // (Opcional)
    }
}
```

### 13.13 11. Translation - es_ES.json

```json
{
  "servicios-cliente": "Servicios del Cliente",
  "servicio-cliente": "Servicio del Cliente",
  "servicios-admin": "Administracion de Servicios",
  "cliente-requerido": "El cliente es requerido",
  "descripcion-requerida": "La descripcion es requerida",
  "precio-positivo": "El precio debe ser positivo",
  "start-date": "Fecha de Inicio",
  "end-date": "Fecha de Fin",
  "general-information": "Informacion General",
  "quantity": "Cantidad",
  "invoices": "Facturas"
}
```

### 13.14 12. CSS - servicios.css

```css
.servicios-container {
    padding: 15px;
    background-color: #f9f9f9;
}

.servicios-list {
    margin-top: 20px;
}

.servicio-card {
    border: 1px solid #ddd;
    padding: 10px;
    margin-bottom: 10px;
    border-radius: 4px;
}

.servicio-card-header {
    font-weight: bold;
    color: #333;
}

.servicio-card-body {
    margin-top: 5px;
    color: #666;
}
```

---

## NOTAS FINALES Y MEJORES PRACTICAS

### Estructura de Carpetas Recomendada

Mantener organizacion clara:
- `Controller/`: Todos los controladores
- `Model/`: Todos los modelos
- `Table/`: Definiciones XML de tablas
- `XMLView/`: Vistas en XML
- `View/`: Plantillas Twig personalizadas
- `Mod/`: Modificadores (hooks)
- `Worker/`: Tareas asincronas
- `Translation/`: Traducciones
- `Assets/`: CSS, JS, imagenes
- `Lib/`: Clases utilitarias
- `Migrations/`: Clases de migracion

### Seguridad

1. **Validar SIEMPRE entrada del usuario**: En el metodo `test()` del modelo
2. **Usar prepared statements**: Con `$this->database->var2str()`
3. **Validar permisos**: Antes de acceder a datos sensibles
4. **Registrar acciones**: Especialmente cambios en datos
5. **No almacenar secretos**: En archivos de plugin

### Rendimiento

1. **Usar indices en bases de datos**: En XML de tabla
2. **Limitar resultados**: En consultas grandes
3. **Cachear datos** cuando sea posible
4. **Evitar N+1 queries**: Cargar datos relacionados en lote

### Testing

1. Crear ejemplos de datos para testing
2. Validar migraciones en ambiente de desarrollo
3. Probar con multiples idiomas
4. Verificar compatibilidad con versiones core

### Documentacion

1. Documentar en README del plugin
2. Incluir ejemplos de uso
3. Documentar APIs personalizadas
4. Mantener changelog de versiones

---

**Ultima actualizacion**: 2026-04-12
**Version**: FacturaScripts 2025
**Autor**: Documentacion oficial FacturaScripts
