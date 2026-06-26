# Sistema de Traducciones de FacturaScripts 2025

Este documento describe el sistema completo de traducciones e internacionalizacion de FacturaScripts 2025, incluyendo su arquitectura, formatos, uso en PHP y Twig, y como crear plugins multiidioma.

## Tabla de Contenidos

1. [Sistema de Traducciones](#sistema-de-traducciones)
2. [Clase Translator](#clase-translator)
3. [Formato de Archivos](#formato-de-archivos)
4. [Idiomas Soportados](#idiomas-soportados)
5. [Como Usar Traducciones](#como-usar-traducciones)
6. [Parametros en Traducciones](#parametros-en-traducciones)
7. [Traducciones en Plugins](#traducciones-en-plugins)
8. [Datos por Pais](#datos-por-pais)
9. [Ejemplo Completo](#ejemplo-completo)

---

## Sistema de Traducciones

### Arquitectura General

El sistema de traducciones de FacturaScripts esta basado en:

- **Clase Translator**: Responsable de cargar y gestionar traducciones
- **Archivos JSON**: Almacenan pares clave-valor de traducciones
- **Metodos globales**: `Tools::lang()` y `Tools::trans()` para acceso facil
- **Filtro Twig**: `trans()` para usar en plantillas
- **Sistema de deploy**: Fusiona traducciones del core y plugins

### Archivo Principal: Translator.php

Ubicacion: `/Core/Translator.php`

La clase `Translator` es la que gestiona todo el sistema de traducciones. Caracteristicas principales:

- Soporta multiples idiomas simultaneamente
- Cache de traducciones cargadas
- Rastreo de traducciones no encontradas
- Sustitucion de parametros en traducciones
- Idioma por defecto: `es_ES`

---

## Clase Translator

### Constructor

```php
public function __construct(?string $langCode = '')
{
    $this->setLang($langCode);
}
```

Crea una instancia del traductor para un idioma especifico.

**Parametros:**
- `$langCode`: Codigo de idioma (ej: 'es_ES', 'en_EN'). Si esta vacio, usa el idioma por defecto.

**Ejemplo:**
```php
$translator = new Translator('en_EN');
$translation = $translator->trans('account');
```

### Metodos Principales

#### trans()

```php
public function trans(?string $txt, array $parameters = []): string
```

Traduce una cadena de texto al idioma actual del traductor.

**Parametros:**
- `$txt`: Clave de traduccion o texto
- `$parameters`: Array asociativo de parametros para reemplazar en la traduccion

**Retorna:** La cadena traducida con parametros reemplazados

**Ejemplo:**
```php
$translator = Tools::lang('es_ES');
echo $translator->trans('account-balance');
// Output: Saldo de la cuenta

echo $translator->trans('account-bad-parent', 
    ['%codcuenta%' => '4700']
);
// Output: La cuenta 4700 tiene asociada una cuenta padre equivocada.
```

#### customTrans()

```php
public function customTrans(?string $langCode, ?string $txt, array $parameters = []): string
```

Traduce una cadena a un idioma especifico, sin cambiar el idioma actual del traductor.

**Parametros:**
- `$langCode`: Codigo de idioma destino
- `$txt`: Clave de traduccion
- `$parameters`: Array de parametros

**Retorna:** La cadena traducida en el idioma especificado

**Ejemplo:**
```php
$translator = Tools::lang('es_ES');

// Obtiene la traduccion en ingles sin cambiar el idioma del traductor
$english = $translator->customTrans('en_EN', 'account-balance');
echo $english; // Output: Account Balance

// El traductor sigue siendo es_ES
echo $translator->trans('account-balance');
// Output: Saldo de la cuenta
```

#### setLang()

```php
public function setLang(?string $langCode): void
```

Cambia el idioma actual del traductor.

**Ejemplo:**
```php
$translator = Tools::lang();
$translator->setLang('en_EN');
echo $translator->trans('account'); // Output: Account
```

#### getLang()

```php
public function getLang(): string
```

Retorna el codigo de idioma actual.

```php
$translator = Tools::lang('fr_FR');
echo $translator->getLang(); // Output: fr_FR
```

#### getAvailableLanguages()

```php
public function getAvailableLanguages(): array
```

Retorna un array con los idiomas disponibles. Las claves son los codigos de idioma y los valores son los nombres traducidos.

**Retorna:** Array con formato: `['es_ES' => 'Espanol', 'en_EN' => 'English', ...]`

**Ejemplo:**
```php
$translator = Tools::lang();
$languages = $translator->getAvailableLanguages();

foreach ($languages as $code => $name) {
    echo "$code: $name\n";
}
```

#### getMissingStrings()

```php
public function getMissingStrings(): array
```

Retorna un array con las traducciones que no fueron encontradas. Util para debugging.

**Retorna:** Array con claves de traducciones no encontradas

**Ejemplo:**
```php
$translator = Tools::lang();
$translator->trans('no-existe-esta-clave');
$translator->trans('tampoco-existe');

$missing = $translator->getMissingStrings();
// Output: ['no-existe-esta-clave@es_ES' => 'no-existe-esta-clave', ...]
```

#### getUsedStrings()

```php
public function getUsedStrings(): array
```

Retorna todas las traducciones que han sido cargadas y usadas.

#### static deploy()

```php
public static function deploy(): void
```

Fusiona todas las traducciones del Core y los plugins activos, generando archivos JSON compilados en la carpeta `Dinamic/Translation`.

**Como funciona:**
1. Escanea `/Core/Translation`
2. Escanea `/Plugins/[Plugin]/Translation` de cada plugin activo
3. Fusiona todas las traducciones por idioma
4. Guarda en `/Dinamic/Translation/[idioma].json`

**Cuando se ejecuta:**
- Automaticamente durante la instalacion
- Cuando se activa/desactiva un plugin
- Manualmente si se llama explicitamente

**Ejemplo:**
```php
// Recompilar todas las traducciones
Translator::deploy();
```

#### static setDefaultLang()

```php
public static function setDefaultLang(?string $langCode): void
```

Establece el idioma por defecto global para toda la aplicacion.

**Ejemplo:**
```php
Translator::setDefaultLang('en_EN');
```

#### static reload()

```php
public static function reload(): void
```

Limpia todas las traducciones cargadas en cache. Util para testing o cuando se modifican traducciones dinamicamente.

```php
Translator::reload();
```

---

## Formato de Archivos

### Ubicacion de Archivos

**Core:**
```
/Core/Translation/
├── es_ES.json
├── en_EN.json
├── de_DE.json
└── ...
```

**Plugins:**
```
/Plugins/[NombrePlugin]/Translation/
├── es_ES.json
├── en_EN.json
└── ...
```

**Dinamicos (generados):**
```
/Dinamic/Translation/
├── es_ES.json (compilado del core + plugins)
├── en_EN.json
└── ...
```

**Personalizados:**
```
/MyFiles/Translation/
├── es_ES.json (sobreescribe dinamic)
└── ...
```

### Estructura JSON

Los archivos de traduccion son JSON con estructura clave-valor:

```json
{
    "clave-simple": "Valor traducido",
    "clave-con-parametros": "Cuenta %codcuenta% con saldo %saldo%",
    "clave-con-html": "<p>Texto <strong>formateado</strong></p>",
    "languages-es_ES": "Espanol",
    "languages-en_EN": "English"
}
```

### Convenciones de Claves

Las claves de traduccion siguen estas convenciones:

**1. Nombres de Idiomas:**
```json
"languages-es_ES": "Espanol",
"languages-en_EN": "English",
"languages-de_DE": "Deutsch"
```

**2. Terminos Comunes:**
```json
"accept": "Aceptar",
"cancel": "Cancelar",
"save": "Guardar",
"delete": "Eliminar",
"close": "Cerrar"
```

**3. Mensajes de Error:**
```json
"access-denied": "Acceso denegado",
"record-not-found": "Registro no encontrado",
"invalid-data": "Datos invalidos"
```

**4. Terminos del Dominio (con prefijo):**
```json
"accounting-entries": "Asientos",
"accounting-entry": "Asiento",
"accounting-account": "Cuenta contable",
"accounting-balance": "Balance contable"
```

**5. Formas Singular/Plural:**
```json
"customer-invoice": "Factura del cliente",
"customer-invoices": "Facturas del cliente"
```

**6. Descripciones Largas:**
```json
"account-dot-code": "Punto para autocompletar ceros. Ejemplo: 11.1 = 1100000001",
"accounting-entry-macros-text": "<p>Puede usar palabras clave especiales..."
```

### Orden de Busqueda de Traducciones

Cuando se solicita una traduccion, el sistema busca en este orden:

1. `/Dinamic/Translation/[idioma].json` (compiladas)
2. `/MyFiles/Translation/[idioma].json` (personalizadas)
3. `/Core/Translation/[idioma].json` (del core)

Las traducciones posteriores sobreescriben las anteriores.

---

## Idiomas Soportados

FacturaScripts 2025 incluye traducciones para los siguientes idiomas:

### Idiomas Principales

| Codigo | Idioma | Codigo ISO |
|--------|--------|-----------|
| es_ES | Espanol (Espana) | es |
| en_EN | English (United Kingdom) | en |
| de_DE | Deutsch | de |
| fr_FR | Francais | fr |
| it_IT | Italiano | it |
| pt_PT | Portugues (Portugal) | pt |
| pl_PL | Polski | pl |

### Variantes de Espanol Latinoamericano

| Codigo | Pais |
|--------|------|
| es_MX | Mexico |
| es_AR | Argentina |
| es_CL | Chile |
| es_CO | Colombia |
| es_PE | Peru |
| es_EC | Ecuador |
| es_CR | Costa Rica |
| es_PA | Panama |
| es_GT | Guatemala |
| es_UY | Uruguay |
| es_DO | Republica Dominicana |

### Idiomas Regionales

| Codigo | Idioma | Region |
|--------|--------|--------|
| ca_ES | Catalan | Cataluna |
| eu_ES | Euskera | Pais Vasco |
| gl_ES | Gallego | Galicia |
| va_ES | Valenciano | Valencia |
| pt_BR | Portugues | Brasil |
| cs_CZ | Cesky | Republica Checa |

### Archivo de Nombres de Idiomas

En `/Core/Translation/es_ES.json`:

```json
{
    "languages-es_ES": "Espanol",
    "languages-en_EN": "English",
    "languages-de_DE": "Deutsch",
    "languages-fr_FR": "Francais",
    "languages-it_IT": "Italiano",
    ...
}
```

---

## Como Usar Traducciones

### En PHP - Metodo 1: Tools::trans()

Forma rapida de traducir sin crear instancia:

```php
// Traduccion simple
echo Tools::trans('accept');

// Con parametros
echo Tools::trans('account-bad-parent', 
    ['%codcuenta%' => '4700']
);

// El idioma usado es el actual de la aplicacion
```

### En PHP - Metodo 2: Tools::lang()

Para trabajar con idiomas especificos:

```php
// Crear instancia del traductor
$translator = Tools::lang();

// Traducir al idioma actual
echo $translator->trans('account');

// Traducir a otro idioma sin cambiar el actual
echo $translator->customTrans('en_EN', 'account');

// Cambiar el idioma actual
$translator->setLang('fr_FR');
echo $translator->trans('account'); // Ahora en frances
```

### En PHP - Metodo 3: Instancia Directa

```php
use FacturaScripts\Core\Translator;

$translator = new Translator('es_ES');
echo $translator->trans('account-balance');
// Output: Saldo de la cuenta

$translator = new Translator('en_EN');
echo $translator->trans('account-balance');
// Output: Account Balance
```

### En Plantillas Twig

FacturaScripts proporciona un filtro Twig `trans()`:

```twig
{# Traduccion simple #}
<h1>{{ trans('account') }}</h1>

{# Con parametros #}
<p>{{ trans('account-bad-parent', {'%codcuenta%': account.codcuenta}) }}</p>

{# En atributos #}
<button title="{{ trans('accept') }}">OK</button>

{# Traduccion de variables #}
{% set key = 'accept' %}
<button>{{ trans(key) }}</button>
```

### Ejemplo Completo en Controlador

```php
<?php
namespace FacturaScripts\MyPlugin\Controller;

use FacturaScripts\Core\Base\Controller;
use FacturaScripts\Core\Tools;

class MyController extends Controller
{
    public function privateCore(&$response, $user, $permissions)
    {
        parent::privateCore($response, $user, $permissions);
        
        // Obtener el idioma actual
        $translator = Tools::lang();
        
        // Traducir mensajes
        $this->title = $translator->trans('my-page-title');
        $this->description = $translator->trans('my-page-description');
        
        // Para formularios, obtener opciones en el idioma actual
        $languages = $translator->getAvailableLanguages();
        
        // Pasar al template
        $this->pageData['languages'] = $languages;
    }
}
```

### Ejemplo en Template

```twig
{% extends "Master/BusinessDocuments.html.twig" %}

{% block body %}
<div class="container">
    <h1>{{ trans('my-page-title') }}</h1>
    <p>{{ trans('my-page-description') }}</p>
    
    <form method="post">
        <label>{{ trans('language') }}</label>
        <select name="language">
            {% for code, name in fsc.pageData.languages %}
                <option value="{{ code }}">{{ name }}</option>
            {% endfor %}
        </select>
        
        <button type="submit">{{ trans('save') }}</button>
    </form>
</div>
{% endblock %}
```

---

## Parametros en Traducciones

### Sintaxis de Parametros

Los parametros en traducciones se definen usando `%nombre%`:

```json
{
    "hello-user": "Hola %username%",
    "balance-message": "La cuenta %code% tiene saldo de %amount%",
    "period-range": "Del %startDate% al %endDate%"
}
```

### Reglas para Parametros

1. **Delimitadores obligatorios**: Deben empezar y terminar con `%`
2. **Valores permitidos**: Solo string o numerico
3. **Otros valores ignorados**: Arrays, objetos se ignoran silenciosamente
4. **Case-sensitive**: Los nombres distinguen mayusculas/minusculas

### Ejemplo de Uso

```php
// En PHP
$translator = Tools::lang();

$result = $translator->trans('hello-user', 
    ['%username%' => 'Carlos']
);
// Output: "Hola Carlos"

// Con multiples parametros
$result = $translator->trans('balance-message',
    [
        '%code%' => '4700',
        '%amount%' => '1500.50'
    ]
);
// Output: "La cuenta 4700 tiene saldo de 1500.50"

// Parametro no definido se pasa como string vacio
$result = $translator->trans('period-range',
    [
        '%startDate%' => '2025-01-01',
        // falta %endDate%
    ]
);
// Output: "Del 2025-01-01 al "
```

### En Twig

```twig
<p>{{ trans('hello-user', {'%username%': user.nickname}) }}</p>

<p>{{ trans('balance-message', {
    '%code%': account.codcuenta,
    '%amount%': account.saldo | money
}) }}</p>
```

### Malas Practicas a Evitar

```php
// INCORRECTO: Sin delimitadores
$trans->trans('user-message', ['username' => 'Carlos']);

// INCORRECTO: Valores invalidos
$trans->trans('data-message', 
    ['%data%' => ['array' => 'value']]
);

// CORRECTO:
$trans->trans('user-message', ['%username%' => 'Carlos']);
$trans->trans('data-message', ['%data%' => json_encode($array)]);
```

---

## Traducciones en Plugins

### Estructura de Carpetas

Los plugins deben crear una carpeta `Translation` en su raiz:

```
/Plugins/MiPlugin/
├── Extension/
├── Model/
├── Controller/
├── View/
├── Translation/          <-- Aqui van las traducciones
│   ├── es_ES.json
│   ├── en_EN.json
│   ├── de_DE.json
│   └── ...
└── Init.php
```

### Archivo de Traduccion del Plugin

**Archivo: `/Plugins/MiPlugin/Translation/es_ES.json`**

```json
{
    "mi-plugin": "Mi Plugin",
    "mi-plugin-description": "Descripcion de mi plugin",
    "mi-feature": "Mi caracteristica",
    "mi-feature-description": "Descripcion de la caracteristica",
    "mi-error": "Ha ocurrido un error en mi plugin",
    "mi-success": "Operacion completada con exito"
}
```

**Archivo: `/Plugins/MiPlugin/Translation/en_EN.json`**

```json
{
    "mi-plugin": "My Plugin",
    "mi-plugin-description": "Description of my plugin",
    "mi-feature": "My feature",
    "mi-feature-description": "Feature description",
    "mi-error": "An error occurred in my plugin",
    "mi-success": "Operation completed successfully"
}
```

### Convenciones de Nomenclatura en Plugins

Use un prefijo para evitar conflictos con otras traducciones:

```json
{
    "miplugin-feature-1": "Caracteristica 1",
    "miplugin-feature-2": "Caracteristica 2",
    "miplugin-error-invalid-data": "Datos invalidos",
    "miplugin-success-saved": "Guardado correctamente"
}
```

### Usar Traducciones del Plugin

En controladores:

```php
<?php
namespace FacturaScripts\MyPlugin\Controller;

use FacturaScripts\Core\Base\Controller;
use FacturaScripts\Core\Tools;

class MyFeature extends Controller
{
    public function privateCore(&$response, $user, $permissions)
    {
        parent::privateCore($response, $user, $permissions);
        
        $translator = Tools::lang();
        
        // Las traducciones del plugin se cargan automaticamente
        $this->title = $translator->trans('miplugin-feature-1');
        
        // Igual que con core
        $message = $translator->trans('miplugin-success-saved');
    }
}
```

En plantillas:

```twig
<h1>{{ trans('miplugin-feature-1') }}</h1>

<p>{{ trans('miplugin-feature-description') }}</p>

<div class="alert alert-success">
    {{ trans('miplugin-success-saved') }}
</div>
```

### Deploy Automatico

El sistema de deploy se ejecuta automaticamente cuando:

1. Se activa un plugin via `Plugins::enable()`
2. Se desactiva un plugin via `Plugins::disable()`
3. Se instala FacturaScripts

Para forzar manualmente:

```php
use FacturaScripts\Core\Translator;

Translator::deploy();
```

### Sobrescribir Traducciones del Plugin

Para sobrescribir traducciones de un plugin sin modificar su codigo:

**Archivo: `/MyFiles/Translation/es_ES.json`**

```json
{
    "miplugin-feature-1": "Mi caracteristica personalizada",
    "miplugin-success-saved": "Se ha guardado perfectamente"
}
```

---

## Datos por Pais

### Sistema de Datos Localizados

Ademas del sistema de traducciones, FacturaScripts incluye datos especificos por pais/idioma en:

```
/Core/Data/Lang/
├── ES/
│   ├── paises.csv
│   ├── divisas.csv
│   ├── almacenes.csv
│   ├── diarios.csv
│   ├── series.csv
│   ├── formaspago.csv
│   └── ...
├── EN/
│   ├── paises.csv
│   ├── divisas.csv
│   └── ...
└── eu_ES/
    ├── paises.csv
    └── ...
```

### Estructura de Datos CSV

Los datos se almacenan en formato CSV con delimitador `;`:

**Archivo: `/Core/Data/Lang/ES/paises.csv`**

```csv
"codpais";"codiso";"nombre";"latitude";"longitude";"telephone_prefix"
"ABW";"AW";"Aruba";"12.5211";"-69.9683";"+297"
"AFG";"AF";"Afganistan";"33.9391";"67.7100";"+93"
"AGO";"AO";"Angola";"11.2027";"17.8739";"+244"
"AND";"AD";"Andorra";"42.5463";"1.6016";"+376"
"ARG";"AR";"Argentina";"38.4161";"-63.6167";"+54"
...
```

### Tipos de Datos Disponibles

1. **paises.csv** - Paises, codigos ISO, coordenadas, prefijos telefonicos
2. **divisas.csv** - Monedas y sus simbolos
3. **almacenes.csv** - Almacenes predefinidos
4. **diarios.csv** - Diarios contables
5. **series.csv** - Series de documentos
6. **formaspago.csv** - Formas de pago
7. **cuentasesp.csv** - Cuentas contables especiales
8. **familias.csv** - Familias de productos
9. **estados_documentos.csv** - Estados de documentos
10. **roles.csv** - Roles predefinidos

### Acceso a Datos Localizados

Los datos se cargan automaticamente en la base de datos durante la instalacion, segun el idioma seleccionado.

Para acceder en codigo:

```php
use FacturaScripts\Core\Model\Pais;

// Obtener un pais
$pais = new Pais();
$pais->codpais = 'ES';
if ($pais->loadFromCode()) {
    echo $pais->nombre; // Output: Espana
    echo $pais->codiso; // Output: ES
}
```

---

## Ejemplo Completo

### Crear un Plugin Multiidioma Completo

#### Paso 1: Estructura del Plugin

```
/Plugins/InvoiceReport/
├── Extension/
├── Model/
│   └── InvoiceReportConfig.php
├── Controller/
│   └── InvoiceReport.php
├── View/
│   └── InvoiceReport/
│       └── list.html.twig
├── Translation/
│   ├── es_ES.json
│   ├── en_EN.json
│   └── de_DE.json
└── Init.php
```

#### Paso 2: Crear Traducciones

**Archivo: `/Plugins/InvoiceReport/Translation/es_ES.json`**

```json
{
    "invoicereport": "Informe de Facturas",
    "invoicereport-description": "Genera informes detallados de facturas",
    "invoicereport-start-date": "Fecha inicio",
    "invoicereport-end-date": "Fecha fin",
    "invoicereport-customer": "Cliente",
    "invoicereport-total-amount": "Importe total",
    "invoicereport-generate": "Generar informe",
    "invoicereport-success": "Informe generado correctamente",
    "invoicereport-no-data": "No hay datos para el rango de fechas seleccionado",
    "invoicereport-error-dates": "La fecha inicio debe ser anterior a la fecha fin",
    "invoicereport-export-pdf": "Descargar PDF",
    "invoicereport-export-excel": "Descargar Excel"
}
```

**Archivo: `/Plugins/InvoiceReport/Translation/en_EN.json`**

```json
{
    "invoicereport": "Invoice Report",
    "invoicereport-description": "Generate detailed invoice reports",
    "invoicereport-start-date": "Start date",
    "invoicereport-end-date": "End date",
    "invoicereport-customer": "Customer",
    "invoicereport-total-amount": "Total amount",
    "invoicereport-generate": "Generate report",
    "invoicereport-success": "Report generated successfully",
    "invoicereport-no-data": "No data found for the selected date range",
    "invoicereport-error-dates": "Start date must be before end date",
    "invoicereport-export-pdf": "Download PDF",
    "invoicereport-export-excel": "Download Excel"
}
```

**Archivo: `/Plugins/InvoiceReport/Translation/de_DE.json`**

```json
{
    "invoicereport": "Rechnungsbericht",
    "invoicereport-description": "Generieren Sie detaillierte Rechnungsberichte",
    "invoicereport-start-date": "Startdatum",
    "invoicereport-end-date": "Enddatum",
    "invoicereport-customer": "Kunde",
    "invoicereport-total-amount": "Gesamtbetrag",
    "invoicereport-generate": "Bericht generieren",
    "invoicereport-success": "Bericht erfolgreich erstellt",
    "invoicereport-no-data": "Keine Daten fur den ausgewahlten Datumsbereich",
    "invoicereport-error-dates": "Startdatum muss vor dem Enddatum liegen",
    "invoicereport-export-pdf": "PDF herunterladen",
    "invoicereport-export-excel": "Excel herunterladen"
}
```

#### Paso 3: Controlador con Traducciones

**Archivo: `/Plugins/InvoiceReport/Controller/InvoiceReport.php`**

```php
<?php
namespace FacturaScripts\Plugins\InvoiceReport\Controller;

use FacturaScripts\Core\Base\Controller;
use FacturaScripts\Core\Tools;
use FacturaScripts\Core\Model\FacturaCliente;

class InvoiceReport extends Controller
{
    public function privateCore(&$response, $user, $permissions)
    {
        parent::privateCore($response, $user, $permissions);
        
        $translator = Tools::lang();
        
        // Establecer titulo y descripcion
        $this->title = $translator->trans('invoicereport');
        $this->description = $translator->trans('invoicereport-description');
        
        // Procesamiento del formulario
        if ($this->request->getMethod() === 'POST') {
            $this->processForm($translator);
        }
        
        // Preparar datos para la vista
        $this->prepareViewData($translator);
    }
    
    private function processForm($translator)
    {
        $startDate = $this->request->request->get('start-date');
        $endDate = $this->request->request->get('end-date');
        
        // Validar fechas
        if ($startDate >= $endDate) {
            $this->toolBox()->i18nLog()->warning(
                $translator->trans('invoicereport-error-dates')
            );
            return;
        }
        
        // Obtener facturas
        $invoiceModel = new FacturaCliente();
        $where = [
            new DataBaseWhere('fecha', $startDate, '>='),
            new DataBaseWhere('fecha', $endDate, '<=')
        ];
        
        $invoices = $invoiceModel->all($where);
        
        if (empty($invoices)) {
            $this->toolBox()->i18nLog()->info(
                $translator->trans('invoicereport-no-data')
            );
            return;
        }
        
        // Guardar resultado en pageData
        $this->pageData['invoices'] = $invoices;
        $this->pageData['total'] = array_sum(
            array_map(fn($inv) => $inv->total, $invoices)
        );
        
        $this->toolBox()->i18nLog()->notice(
            $translator->trans('invoicereport-success')
        );
    }
    
    private function prepareViewData($translator)
    {
        $this->pageData['languages'] = $translator->getAvailableLanguages();
    }
}
```

#### Paso 4: Plantilla con Traducciones

**Archivo: `/Plugins/InvoiceReport/View/InvoiceReport/list.html.twig`**

```twig
{% extends "Master/AdminPanel.html.twig" %}

{% block body %}
<div class="container-fluid">
    <h1 class="mb-4">{{ trans('invoicereport') }}</h1>
    
    <div class="card">
        <div class="card-header">
            <h5 class="card-title">{{ trans('invoicereport-description') }}</h5>
        </div>
        <div class="card-body">
            <form method="post" class="row g-3">
                <div class="col-md-3">
                    <label class="form-label">{{ trans('invoicereport-start-date') }}</label>
                    <input type="date" name="start-date" class="form-control" required>
                </div>
                
                <div class="col-md-3">
                    <label class="form-label">{{ trans('invoicereport-end-date') }}</label>
                    <input type="date" name="end-date" class="form-control" required>
                </div>
                
                <div class="col-md-3">
                    <label class="form-label">{{ trans('invoicereport-customer') }}</label>
                    <input type="text" name="customer" class="form-control">
                </div>
                
                <div class="col-md-3 d-flex align-items-end">
                    <button type="submit" class="btn btn-primary w-100">
                        <i class="fas fa-search"></i> {{ trans('invoicereport-generate') }}
                    </button>
                </div>
            </form>
        </div>
    </div>
    
    {% if fsc.pageData.invoices %}
    <div class="card mt-4">
        <div class="card-header">
            <h5 class="card-title">
                {{ trans('invoicereport') }}
                <span class="badge bg-info float-end">{{ fsc.pageData.invoices | length }}</span>
            </h5>
        </div>
        <div class="table-responsive">
            <table class="table table-hover">
                <thead>
                    <tr>
                        <th>Numero</th>
                        <th>{{ trans('invoicereport-customer') }}</th>
                        <th>Fecha</th>
                        <th class="text-end">{{ trans('invoicereport-total-amount') }}</th>
                    </tr>
                </thead>
                <tbody>
                    {% for invoice in fsc.pageData.invoices %}
                    <tr>
                        <td>{{ invoice.numero }}</td>
                        <td>{{ invoice.nombrecliente }}</td>
                        <td>{{ invoice.fecha | date('d/m/Y') }}</td>
                        <td class="text-end">{{ invoice.total | money }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
                <tfoot>
                    <tr class="table-primary fw-bold">
                        <td colspan="3">Total</td>
                        <td class="text-end">{{ fsc.pageData.total | money }}</td>
                    </tr>
                </tfoot>
            </table>
        </div>
        
        <div class="card-footer">
            <button class="btn btn-outline-secondary" onclick="window.print()">
                <i class="fas fa-print"></i> {{ trans('invoicereport-export-pdf') }}
            </button>
            <a href="/export-excel" class="btn btn-outline-secondary">
                <i class="fas fa-download"></i> {{ trans('invoicereport-export-excel') }}
            </a>
        </div>
    </div>
    {% endif %}
</div>
{% endblock %}
```

#### Paso 5: Archivo Init.php

**Archivo: `/Plugins/InvoiceReport/Init.php`**

```php
<?php
namespace FacturaScripts\Plugins\InvoiceReport;

use FacturaScripts\Core\Base\InitClass;

class Init extends InitClass
{
    public function init()
    {
        // El sistema de traducciones se carga automaticamente
    }
    
    public function update()
    {
        // Si es necesario, recompilar traducciones
        \FacturaScripts\Core\Translator::deploy();
    }
}
```

### Resultado Final

El usuario puede usar el plugin en:
- Espanol: Con traducciones de `/Plugins/InvoiceReport/Translation/es_ES.json`
- Ingles: Con traducciones de `/Plugins/InvoiceReport/Translation/en_EN.json`
- Aleman: Con traducciones de `/Plugins/InvoiceReport/Translation/de_DE.json`

Las traducciones se cargan automaticamente segun el idioma seleccionado en la aplicacion.

---

## Mejores Practicas

### Do's (Haga)

1. Usar claves descriptivas y consistentes
2. Prefijo para plugins evita conflictos
3. Usar parametros para valores dinamicos
4. Traducir a minusculas, salvo necesidad
5. Incluir todas las claves en todos los idiomas
6. Usar `Tools::trans()` para acceso simple
7. Usar `Tools::lang()` para control avanzado

### Don'ts (No Haga)

1. Traducir HTML directamente, use plantillas
2. Mezclar idiomas en una sola clave
3. Usar caracteres especiales sin necesidad
4. Dejar claves sin traducir en otros idiomas
5. Cambiar idiomas frecuentemente sin necesidad
6. Hardcodear cadenas en lugar de traducirlas
7. Crear parametros sin delimitadores `%`

---

## Referencia Rapida de Metodos

```php
// Obtener traductor
$trans = Tools::lang();
$trans = Tools::lang('en_EN');
$trans = new Translator('fr_FR');

// Traducir
$text = Tools::trans('clave');
$text = $trans->trans('clave');
$text = $trans->trans('clave', ['%param%' => $value]);
$text = $trans->customTrans('en_EN', 'clave');

// Informacion
$code = $trans->getLang();
$langs = $trans->getAvailableLanguages();
$missing = $trans->getMissingStrings();
$used = $trans->getUsedStrings();

// Configuracion
$trans->setLang('es_ES');
Translator::setDefaultLang('en_EN');
Translator::reload();
Translator::deploy();
```

---

## Recursos Adicionales

- Carpeta Core: `/facturascripts/Core/Translator.php`
- Traducciones: `/facturascripts/Core/Translation/`
- Datos locales: `/facturascripts/Core/Data/Lang/`
- Tools: `/facturascripts/Core/Tools.php`
