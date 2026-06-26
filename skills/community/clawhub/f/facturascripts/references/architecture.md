# Referencia Arquitectonica FacturaScripts 2025

## TABLA DE CONTENIDOS

1. [Punto de Entrada (index.php)](#1-punto-de-entrada-indexphp)
2. [Kernel](#2-kernel)
3. [Request](#3-request)
4. [Response](#4-response)
5. [Session](#5-session)
6. [Plugins](#6-plugins)
7. [Cache](#7-cache)
8. [Logger](#8-logger)
9. [Tools](#9-tools)
10. [Html (Twig)](#10-html-twig)
11. [Http](#11-http)
12. [Translator](#12-translator)
13. [Validator](#13-validator)
14. [DbQuery](#14-dbquery)
15. [Where](#15-where)
16. [WorkQueue](#16-workqueue)
17. [NextCode](#17-nextcode)
18. [Migrations](#18-migrations)
19. [DbUpdater](#19-dbupdater)
20. [Base/Controller](#20-basecontroller)
21. [Base/DataBase](#21-basedatabase)
22. [Contratos e Interfaces](#22-contratos-e-interfaces)
23. [Error Handlers](#23-error-handlers)
24. [DataSrc](#24-datasrc)
25. [Internal](#25-internal)
26. [CrashReport, DebugBar, Telemetry, UploadedFile](#26-crashreport-debugbar-telemetry-uploadedfile)

---

## 1. PUNTO DE ENTRADA (index.php)

El archivo `/index.php` es el punto de entrada de toda la aplicación FacturaScripts.

### Flujo de Ejecución Completo

```
1. Requiere vendor/autoload.php (composer)
2. Define constante: FS_FOLDER = __DIR__
3. Carga config.php si existe (configuracion opcional)
4. Desactiva limite de tiempo: set_time_limit(0)
5. Ignora abortamiento de usuario: ignore_user_abort(true)
6. Obtiene zona horaria de config: Tools::config('timezone', 'Europe/Madrid')
7. Establece zona horaria: date_default_timezone_set($timeZone)
8. Inicializa manejador de errores: CrashReport::init()
9. Inicializa kernel: Kernel::init()
10. Carga plugins (excepto si URL es /deploy): Plugins::init()
11. Ejecuta controlador: Kernel::run($url)
12. Si base de datos conectada:
    - Ejecuta cola de trabajos: WorkQueue::run()
    - Actualiza telemetria: Telemetry::init()->update()
    - Guarda logs: MiniLog::save()
    - Cierra conexion BD: $db->close()
    - Limpia archivos temporales antiguos: NextCode::clearOld()
```

### Constantes Principales

- `FS_FOLDER`: Ruta raiz de la aplicacion
- `FS_CODPAIS`: Codigo pais (por defecto 'ESP')
- `FS_CURRENCY_POS`: Posicion moneda ('right' o 'left')
- `FS_ITEM_LIMIT`: Limite items por pagina
- `FS_NF0`: Numero de decimales (por defecto 2)
- `FS_NF1`: Separador decimal (por defecto ',')
- `FS_NF2`: Separador miles (por defecto ' ')

---

## 2. KERNEL

Clase: `FacturaScripts\Core\Kernel`

Corazon del sistema que gestiona rutas y ejecuta controladores.

### Propiedades Privadas Estaticas

```
private static $routes = []                    // Array de rutas registradas
private static $routesCallbacks = []           // Array de Closure para añadir rutas dinamicamente
private static $timers = []                    // Array de timers para medir performance
```

### Constantes

- `version()`: `2025.81` (retorna float)

### Metodos Publicos Estaticos

#### Manejo de Rutas

- `addRoute(string $route, string $controller, int $position = 0, string $customId = ''): void`
  - Añade una nueva ruta
  - Si customId existe, reemplaza ruta anterior con ese ID
  - position: orden en que se evalua la ruta (menor = mas prioridad)
  - Ejemplo: `Kernel::addRoute('/mirutaa', '\\FacturaScripts\\Dinamic\\Controller\\MiControlador')`

- `clearRoutes(): void`
  - Limpia todas las rutas registradas

- `addRoutes(Closure $closure): void`
  - Registra callback para añadir rutas dinamicamente
  - El closure recibe $routes como parametro
  - Ejemplo: `Kernel::addRoutes(function(&$routes) { ... })`

- `rebuildRoutes(): void`
  - Reconstruye todas las rutas desde cero
  - Lee carpeta Dinamic/Controller
  - Busca pagina por defecto de config (homepage)
  - Ejecuta callbacks registrados
  - Ordena por posicion

- `loadRoutes(): void` (privado)
  - Carga rutas por defecto
  - Lee archivo MyFiles/routes.json si existe
  - Ordena rutas por posicion

- `saveRoutes(): bool`
  - Guarda rutas en MyFiles/routes.json
  - Retorna true si exito

#### Ejecucion de Controladores

- `run(string $url): void`
  - Punto de entrada para ejecutar un controlador
  - Carga rutas, ejecuta controlador, finaliza request
  - Si Exception: obtiene error handler y ejecuta
  - Limpia ultimos errores: `error_clear_last()`

- `runController(string $url): void` (privado)
  - Busca ruta que coincida con URL
  - Instancia controlador y llama `$app->run()`
  - Si no encuentra ruta: lanza `KernelException('PageNotFound', $url)`

- `matchesRoute(string $url, string $route): bool` (privado)
  - Compara URL con ruta exacta o con comodin (*)
  - Si ruta termina en *, compara prefijo
  - Ejemplo: `/api/*` coincide con `/api/usuarios`, `/api/productos`

- `checkControllerClass(string $controller): array` (privado)
  - Retorna `[$controller, $name]`
  - Si controller no tiene namespace, lo agrega
  - Busca en Dinamic\Controller, luego en Core\Controller

#### Performance/Timers

- `startTimer(string $name): void`
  - Inicia cronometro
  - Registra: start time, start memory usage

- `stopTimer(string $name): float`
  - Detiene cronometro
  - Retorna tiempo transcurrido (5 decimales)
  - Registra: stop time, stop memory usage

- `getTimer(string $name): float`
  - Obtiene tiempo de timer (retorna 0.0 si no existe)

- `getTimers(): array`
  - Retorna array de todos los timers con start/stop times

- `getExecutionTime(int $decimals = 5): float`
  - Tiempo total desde inicio kernel
  - Retorna diferencia entre ahora y kernel::init::start

#### Bloqueos (Locks)

- `lock(string $processName): bool`
  - Crea archivo de bloqueo en MyFiles/lock_[hash].lock
  - Si existe y tiene mas de 2 horas, lo elimina
  - Retorna true si se crea nuevo lock

- `unlock(string $processName): bool`
  - Elimina archivo de bloqueo
  - Retorna true si lo elimina exitosamente

#### Rutas por Defecto Registradas

```
'/'                                    => 'Root'
'/AdminPlugins'                        => 'AdminPlugins'
'/api'                                 => 'ApiRoot'
'/api/3/attachedfiles'                 => 'ApiAttachedFiles'
'/api/3/crearAlbaranCliente'           => 'ApiCreateDocument'
'/api/3/crearFacturaCliente'           => 'ApiCreateDocument'
'/api/3/exportarFacturaCliente/*'      => 'ApiExportDocument'
'/Core/Assets/*'                       => 'Files'
'/cron'                                => 'Cron'
'/deploy'                              => 'Deploy'
'/Dinamic/Assets/*'                    => 'Files'
'/login'                               => 'Login'
'/MyFiles/*'                           => 'Myfiles'
'/node_modules/*'                      => 'Files'
'/Plugins/*'                           => 'Files'
'/Updater'                             => 'Updater'
```

### Manejo de Excepciones

- `getErrorHandler(Exception $exception): ErrorControllerInterface` (privado)
  - Si es KernelException: obtiene handler del atributo handler
  - Busca en Dinamic\Error\[handler], luego Core\Error\[handler]
  - Si no es KernelException: busca DefaultError en Dinamic o Core

- `finishRequest(): void` (privado)
  - Solo en entorno web (no CLI)
  - Si tiene fastcgi_finish_request(): lo llama
  - Si no: envía headers de cierre y flushea buffer

---

## 3. REQUEST

Clase: `FacturaScripts\Core\Request`

Encapsula datos de request HTTP (GET, POST, headers, cookies, archivos).

### Constantes de Metodos HTTP

```
const METHOD_GET = 'GET'
const METHOD_POST = 'POST'
const METHOD_PUT = 'PUT'
const METHOD_PATCH = 'PATCH'
```

### Propiedades Publicas

```
public $cookies                        // SubRequest con cookies
public $files                          // RequestFiles con archivos subidos
public $headers                        // Headers con headers HTTP
public $query                          // SubRequest con parametros GET
public $request                        // SubRequest con datos POST/PUT/PATCH
```

### Propiedades Privadas

```
private $rawInput                      // string|null contenido raw del body
```

### Constructor

```php
public function __construct(array $data = [])
```

- Crea SubRequest/RequestFiles desde array de datos
- Atributos esperados: cookies, files, headers, query, input, request

- `createFromGlobals(): self` (static)
  - Crea Request desde globales $_GET, $_POST, $_FILES, $_COOKIE, $_SERVER
  - Parsea datos POST para PUT/PATCH si content-type es form-urlencoded

### Metodos de Datos

#### Headers y Metodo

- `header(string $key, $default = null): ?string`
  - Obtiene header HTTP

- `method(): string`
  - Retorna REQUEST_METHOD ($_SERVER)

- `isMethod(string $method): bool`
  - Comprueba si metodo coincide con parámetro

- `protocol(): string`
  - Retorna SERVER_PROTOCOL

- `isSecure(): bool`
  - Retorna true si protocolo es https

#### IP y Host

- `ip(): string`
  - Detecta IP del cliente (Cloudflare, proxy, o REMOTE_ADDR)
  - Retorna '::1' si no encuentra

- `host(): string`
  - Retorna HTTP_HOST ($_SERVER)

#### User Agent

- `userAgent(): string`
  - Retorna HTTP_USER_AGENT

- `browser(): string`
  - Retorna navegador detectado: 'chrome', 'edge', 'firefox', 'safari', 'opera', 'ie', 'unknown'

- `os(): string`
  - Retorna SO detectado: 'windows', 'mac', 'linux', 'unix', 'sun', 'bsd', 'unknown'

#### URLs

- `url(?int $position = null): string`
  - Retorna URL sin parametros GET
  - Si position es null: retorna URL completa
  - Si position >= 0: retorna parte en esa posicion
  - Si position < 0: cuenta desde el final
  - Ejemplo: `/Ventas/ListFactura?modo=1` sin FS_ROUTE retorna `/Ventas/ListFactura`

- `urlWithQuery(): string`
  - Retorna URL + QUERY_STRING

- `fullUrl(): string`
  - Retorna protocolo + host + URL + query

- `getBasePath(): string`
  - Retorna componente PATH de REQUEST_URI

#### Acceso a Datos GET/POST

Métodos nuevos (recomendados):

- `input(string $key, $default = null): ?string` - Obtiene de POST/PUT/PATCH
- `query(string $key, $default = null): ?string` - Obtiene de GET
- `inputOrQuery(string $key, $default = null): ?string` - POST si existe, si no GET
- `queryOrInput(string $key, $default = null): ?string` - GET si existe, si no POST

- `cookie(string $key, $default = null): ?string`
  - Obtiene cookie

- `file(string $key): ?UploadedFile`
  - Obtiene archivo subido

- `has(string ...$key): bool`
  - Retorna true si TODOS los parametros existen (GET o POST)

- `json(?string $key = null, $default = null)`
  - Parsea body como JSON
  - Si $key es null: retorna todo el JSON decodificado
  - Si $key: retorna solo esa clave del JSON

- `getContent(): string`
  - Retorna contenido raw del body
  - Si no hay rawInput: lee de php://input

#### Acceso a Datos SubRequest (deprecated)

Estos metodos usan SubRequest internamente y son deprecated:

- `all(string ...$key): array` - Retorna todos los parametros
- `get(string $key, $default = null): ?string` - Obtiene parametro
- `getArray(string $key): array` - Obtiene parametro como array
- `getAlnum(string $key): string` - Alfanumerico
- `getBool(string $key, ?bool $default = null): ?bool`
- `getDate(string $key, ?string $default = null): ?string`
- `getDateTime(string $key, ?string $default = null): ?string`
- `getEmail(string $key, ?string $default = null): ?string`
- `getFloat(string $key, ?float $default = null): ?float`
- `getHour(string $key, ?string $default = null): ?string`
- `getInt(string $key, ?int $default = null): ?int`
- `getOnly(string $key, array $values): ?string`
- `getString(string $key, ?string $default = null): ?string`
- `getUrl(string $key, ?string $default = null): ?string`

### Parsing de Datos

- `parseRequestData(): array` (static)
  - Lee $_POST
  - Si REQUEST_METHOD es PUT/PATCH y content-type es form-urlencoded: parsea php://input con parse_str()
  - Retorna array de datos parseados

---

## 4. RESPONSE

Clase: `FacturaScripts\Core\Response`

Representa respuesta HTTP con contenido, headers y cookies.

### Constantes de Codigos HTTP

```
const HTTP_OK = 200
const HTTP_BAD_REQUEST = 400
const HTTP_UNAUTHORIZED = 401
const HTTP_FORBIDDEN = 403
const HTTP_NOT_FOUND = 404
const HTTP_METHOD_NOT_ALLOWED = 405
const HTTP_CONFLICT = 409
const HTTP_UNPROCESSABLE_ENTITY = 422
const HTTP_INTERNAL_SERVER_ERROR = 500
```

### Propiedades Privadas

```
private $content                       // string contenido de respuesta
private $cookies                       // array de cookies a enviar
private $http_code                     // int codigo HTTP (default 200)
private $send_disabled = false         // bool si esta deshabilitado el envio
private $sent = false                  // bool si ya se envio la respuesta
```

### Propiedades Publicas

```
public $headers                        // ResponseHeaders objeto de headers
```

### Constructor

```php
public function __construct(int $http_code = 200)
```

- Inicializa response con codigo HTTP
- Crea ResponseHeaders vacio
- Content vacio, cookies vacio

### Metodos HTTP

#### Cookies

- `cookie(string $name, ?string $value, int $expire = 0, bool $httpOnly = true, ?bool $secure = null, string $sameSite = 'Lax'): self`
  - Registra cookie para enviar
  - Si expire es 0: usa cookies_expire de config
  - secure: auto-detecta si HTTPS si es null
  - sameSite: 'Lax' por defecto (puede ser 'Strict', 'None')
  - Retorna $this para encadenamiento

#### Archivos y Descargas

- `file(string $file_path, string $file_name = '', string $disposition = 'inline'): void`
  - Envia archivo desde disco
  - Valida que archivo existe y es legible
  - disposition: 'inline' o 'attachment'

- `download(string $file_path, string $file_name = ''): void`
  - Envia archivo como descarga (disposition='attachment')

#### Control de Envio

- `disableSend(bool $disable = true): self`
  - Deshabilita envio de respuesta
  - Retorna $this para encadenamiento

### Control de Respuesta

- `send_disabled`: Bloquea envio si esta true
- `sent`: Indica si response ya fue enviada

---

## 5. SESSION

Clase: `FacturaScripts\Core\Session`

Gestiona datos de sesion del usuario en memoria.

### Propiedades Privadas Estaticas

```
private static $data = []              // array con datos de sesion
```

### Metodos Publicos Estaticos

#### Acceso a Datos

- `set(string $key, $value): void`
  - Almacena valor en sesion

- `get(string $key)`
  - Obtiene valor de sesion
  - Retorna null si no existe

- `clear(): void`
  - Limpia todos los datos de sesion

#### Usuario y Permisos

- `user(): User`
  - Obtiene usuario actual de sesion
  - Si no existe en sesion: retorna instancia vacia User o DinUser
  - Si clase DinUser existe (en Dinamic): la usa en lugar de User core

- `permissions(): ControllerPermissions`
  - Obtiene permisos del usuario actual
  - Si no existe en sesion: retorna ControllerPermissions vacio

#### IP del Cliente

- `getClientIp(): string`
  - Detecta IP real del cliente
  - Comprueba en orden: HTTP_CF_CONNECTING_IP (Cloudflare), HTTP_X_FORWARDED_FOR (proxies), REMOTE_ADDR
  - Retorna '::1' si no encuentra ninguna

---

## 6. PLUGINS

Clase: `FacturaScripts\Core\Plugins`

Sistema de gestion de plugins: instalacion, activacion, desactivacion, eliminacion.

### Constantes

```
const FILE_NAME = 'plugins.json'       // Archivo de configuracion de plugins
```

### Propiedades Privadas Estaticas

```
private static $plugins                // Plugin[] array de plugins cargados
```

### Metodos Publicos Estaticos

#### Ciclo de Vida de Plugins

- `init(): void`
  - Ejecuta procesos init de plugins habilitados
  - Ordena por 'order'
  - Si algun plugin retorna true de init(): guarda cambios

- `add(string $zipPath, string $zipName = 'plugin.zip', bool $force = false): bool`
  - Instala plugin desde archivo ZIP
  - Comprueba disable_add_plugins config (puede forzarse con $force=true)
  - Valida ZIP con facturascripts.ini
  - Verifica compatibilidad ($plugin->compatible)
  - Elimina version anterior si existe
  - Descomprime ZIP
  - Renombra carpeta si es necesario
  - Si ya estaba habilitado: marca post_enable=true
  - Llama deploy() si esta habilitado

- `enable(string $pluginName): bool`
  - Activa plugin deshabilitado
  - Comprueba que carpeta del plugin coincida con nombre
  - Verifica dependencias con $plugin->dependenciesOk()
  - Incrementa order (orden de ejecucion)
  - Marca post_enable=true, post_disable=false
  - Llama deploy(false, true)

- `disable(string $pluginName, bool $runPostDisable = true): bool`
  - Desactiva plugin habilitado
  - Marca post_enable=false
  - post_disable=$runPostDisable
  - Llama deploy(true, true)

- `remove(string $pluginName): bool`
  - Elimina plugin completamente
  - Comprueba disable_rm_plugins config
  - Solo se puede eliminar si esta deshabilitado
  - Elimina directorio del plugin
  - Elimina de lista en plugins.json

- `deploy(bool $clean = true, bool $initControllers = false): void`
  - Ejecuta despliegue de plugins
  - clean: borra carpeta Cache si true
  - initControllers: inicializa controladores si true
  - Llama PluginsDeploy::run()
  - Reconstruye rutas: Kernel::rebuildRoutes(), Kernel::saveRoutes()
  - Reconstruye BD: DbUpdater::rebuild()

#### Lectura de Plugins

- `load(): void`
  - Carga lista de plugins desde archivo
  - Busca plugins nuevos en carpeta Plugins/
  - Solo ejecuta si $plugins es null

- `list(bool $hidden = false, string $orderBy = 'name'): Plugin[]`
  - Retorna array de plugins
  - $hidden: incluir plugins ocultos
  - $orderBy: 'name' (alfabetico) o 'order' (por orden de ejecucion)

- `get(string $pluginName): ?Plugin`
  - Obtiene plugin por nombre
  - Retorna null si no existe

- `enabled(): array`
  - Retorna array de nombres de plugins habilitados
  - Ordenados por 'order'

#### Consultas

- `isInstalled(string $pluginName): bool`
  - Comprueba si plugin esta instalado

- `isEnabled(string $pluginName): bool`
  - Comprueba si plugin esta habilitado

- `folder(): string`
  - Retorna ruta de carpeta de plugins: Tools::folder('Plugins')

#### Metodos Privados

- `maxOrder(): int`
  - Obtiene maximo valor de order entre plugins

- `save(): void`
  - Guarda lista de plugins en plugins.json
  - Verifica dependencias antes de guardar
  - Si plugin habilitado no cumple dependencias: se deshabilita automaticamente

- `loadFromFile(): void`
  - Carga plugins desde plugins.json en MyFiles/

- `loadFromFolder(): void`
  - Busca plugins en carpeta Plugins/ que no esten en archivo

- `testZipFile(ZipArchive &$zipFile, string $zipPath, string $zipName): bool`
  - Valida estructura del ZIP
  - Comprueba que existe facturascripts.ini en raiz
  - Comprueba que solo hay un directorio raiz

---

## 7. CACHE

Clase: `FacturaScripts\Core\Cache`

Sistema de cache en archivos con TTL.

### Constantes

```
const EXPIRATION = 3600                // TTL default (1 hora)
const FILE_PATH = '/MyFiles/Tmp/FileCache'  // Ubicacion cache
```

### Metodos Publicos Estaticos

#### Almacenamiento

- `set(string $key, $value): void`
  - Guarda valor en cache
  - Serializa con serialize()
  - Crea carpeta si no existe
  - Nombre archivo: key convertido (/ y \ reemplazados por _) + .cache

- `get(string $key, $default = null)`
  - Obtiene valor de cache
  - Comprueba que archivo no haya expirado (filemtime >= time() - EXPIRATION)
  - Unserializa valor
  - Si error deserializando: retorna $default

- `has(string $key): bool`
  - Comprueba si cache existe y no ha expirado

- `delete(string $key): void`
  - Elimina archivo de cache

- `deleteMulti(string $prefix): void`
  - Elimina todos los cache que empiezan con prefix

- `clear(): void`
  - Elimina todos los archivos .cache

- `expire(): void`
  - Elimina todos los cache expirados

#### Patron Remember

- `remember(string $key, Closure $callback)`
  - Si cache existe: retorna valor cacheado
  - Si no existe: ejecuta callback, guarda resultado, lo retorna
  - Uso: `Cache::remember('usuarios', fn() => obtenerUsuarios())`

#### Cache Hibrido

- `withMemory(): CacheWithMemory`
  - Retorna instancia de CacheWithMemory
  - Combina cache de memoria con cache de archivos
  - Mas rapido pero consume memoria

---

## 8. LOGGER

Clase: `FacturaScripts\Core\Logger`

Sistema de logging con multiples canales y niveles.

### Constantes

#### Niveles de Log

```
const LEVEL_DEBUG = 'debug'
const LEVEL_INFO = 'info'
const LEVEL_NOTICE = 'notice'
const LEVEL_WARNING = 'warning'
const LEVEL_ERROR = 'error'
const LEVEL_CRITICAL = 'critical'
const MAX_ITEMS = 5000                 // Limite de mensajes en memoria
```

#### Metodos de Guardado

```
const SAVE_METHOD_DB = 'db'            // Guardar en base de datos
const SAVE_METHOD_FILE = 'file'        // Guardar en archivo JSON
```

### Propiedades Privadas

```
private $current_channels = ['master'] // Canales actuales de logger
private static $current_context = []   // Contexto adicional para mensajes
private static $data = []              // Array de mensajes registrados
private static $disabled = false       // Si logging esta deshabilitado
private static $last_log_filename      // Ruta ultimo archivo guardado
private static $save_method = 'db'     // Metodo de guardado (db o file)
private $translator                    // Translator para traducir mensajes
```

### Constructor y Creacion

```php
public function __construct(array $channels = [])
```

- Si no hay canales: usa ['master']
- Convierte canales vacios a 'master'
- Elimina duplicados

#### Creacion Rapida

- `channel(string $name): self` (static)
  - Crea logger con un canal especifico

- `stack(array $channels): self` (static)
  - Crea logger con multiples canales

### Metodos de Logging

Todos retornan $this para encadenamiento:

- `debug(string $message, array $context = []): self`
  - Solo se registra si config debug=true

- `info(string $message, array $context = []): self`
- `notice(string $message, array $context = []): self`
- `warning(string $message, array $context = []): self`
- `error(string $message, array $context = []): self`
- `critical(string $message, array $context = []): self`

### Lectura de Logs

- `read(string $channel = '', array $levels = [], int $num = 0): array`
  - Retorna mensajes filtrados por canal y niveles
  - Si $num=0: todos, si $num>0: primeros $num, si $num<0: ultimos $num

- `readAll(int $num = 0): array`
  - Retorna todos los mensajes

- `readChannel(string $channel, array $levels = [], int $num = 0): array`
  - Retorna mensajes de canal especifico

- `readLevel(string $level, int $num = 0): array`
  - Retorna mensajes de nivel especifico

- `getChannels(): array`
  - Retorna array de canales unicos usados

### Guardar Logs

#### Guardado Global

- `save(): bool`
  - Guarda todos los mensajes
  - Si save_method='db': intenta guardar en BD, si falla en archivo
  - Si save_method='file': guarda en archivo JSON

- `saveToDB(): bool`
  - Guarda mensajes en modelo LogMessage (BD)
  - Del canal 'master' solo guarda error/critical
  - Elimina del array los guardados exitosamente

- `saveToFile(): bool`
  - Guarda en archivo JSON en MyFiles/
  - Nombre: log_[fecha]_[uniqid].json
  - Del canal 'master' solo guarda error/critical

#### Guardado por Canal

- `saveChannelToDB(string $channel): bool`
  - Guarda solo mensajes del canal especifico

- `saveChannelToFile(string $channel): bool`
  - Guarda solo mensajes del canal especifico

#### Configuracion de Guardado

- `saveMethod(string $method): bool`
  - Configura metodo de guardado ('db' o 'file')
  - Retorna true si es valido

- `getLastLogFilename(): ?string` (static)
  - Retorna ruta del ultimo archivo guardado

### Control Global

- `disable(bool $value = true): void` (static)
  - Deshabilita/habilita logging

- `disabled(): bool` (static)
  - Comprueba si logging esta deshabilitado

- `clear(): void` (static)
  - Limpia todos los mensajes y contexto

- `clearChannel(string $channel): void` (static)
  - Limpia mensajes de canal

- `clearContext(): void` (static)
  - Limpia contexto actual

### Contexto

- `withContext(array $context): void` (static)
  - Añade contexto adicional a todos los mensajes
  - Ejemplo: `Logger::withContext(['nick' => $user->nick])`

---

## 9. TOOLS

Clase: `FacturaScripts\Core\Tools`

Coleccion exhaustiva de funciones utiles.

### Constantes

#### Mapeo de Caracteres ASCII

```
const ASCII = [...]                    // Array de reemplazos acentos a ASCII
// Ejemplos: 'á' => 'a', 'ñ' => 'n', 'é' => 'e'
```

#### Caracteres HTML

```
const HTML_CHARS = ['<', '>', '"', "'"]
const HTML_REPLACEMENTS = ['&lt;', '&gt;', '&quot;', '&#39;']
```

#### Formatos de Fecha/Hora

```
const DATE_STYLE = 'd-m-Y'             // 31-12-2025
const DATETIME_STYLE = 'd-m-Y H:i:s'   // 31-12-2025 23:59:59
const HOUR_STYLE = 'H:i:s'             // 23:59:59
```

### Propiedades Privadas Estaticas

```
private static $settings               // array de configuracion cacheada
private static $translator             // Translator instancia
```

### Funciones de Conversion

#### ASCII

- `ascii(string $text): string`
  - Convierte caracteres acentuados a equivalentes ASCII
  - Usa tabla const ASCII
  - Ejemplo: `Tools::ascii('niño') => 'nino'`

#### Bytes

- `bytes($size, int $decimals = 2): string`
  - Convierte bytes a formato legible
  - 1073741824 bytes = 1 GB
  - 1048576 bytes = 1 MB
  - 1024 bytes = 1 KB
  - Ejemplo: `Tools::bytes(5368709120) => '5.00 GB'`

#### Configuracion

- `config(string $key, $default = null)`
  - Obtiene constante de configuracion
  - Busca en orden: $key, strtoupper($key), 'FS_' . strtoupper($key)
  - Ejemplo: `Tools::config('timezone', 'Europe/Madrid')`

- `settings(string $property, string $key, $default = null)`
  - Obtiene parametro de tabla settings
  - Acceso: Settings::get($property)->$key

#### Numeros y Decimales

- `decimals(): int`
  - Retorna numero de decimales configurado (default 2)

- `number($number, int $decimals = 0, string $decimalSeparator = null, string $thousandsSeparator = null): string`
  - Formatea numero con decimales
  - decimalSeparator default: ','
  - thousandsSeparator default: ' '
  - Ejemplo: `Tools::number(1234567.891234, 2) => '1 234 567,89'`

#### Fechas y Horas

- `date(?string $date = null): string`
  - Formatea fecha segun DATE_STYLE
  - Si $date vacio: usa fecha actual
  - Ejemplo: `Tools::date('2025-12-31') => '31-12-2025'`

- `dateTime(?string $date = null): string`
  - Formatea fecha y hora segun DATETIME_STYLE
  - Si $date vacio: usa fecha/hora actual

- `hour(?string $date = null): string`
  - Formatea solo hora segun HOUR_STYLE

- `dateOperation(string $date, string $operation): ?string`
  - Realiza operacion sobre fecha
  - operation: "+1 day", "-2 months", etc. (formato strtotime)
  - Retorna fecha formateada o null si error
  - Ejemplo: `Tools::dateOperation('2025-01-01', '+1 day') => '02-01-2025'`

- `timeToDateTime($time): string`
  - Convierte timestamp/tiempo a datetime formateado

- `dateTimeToTime(string $date): int`
  - Convierte string datetime a timestamp

### Carpetas y Archivos

#### Gestion de Carpetas

- `folder(string $type, string ...$subFolder): string`
  - Obtiene ruta de carpeta especial
  - tipos: 'Core', 'Dinamic', 'Plugins', 'MyFiles', 'Tmp', etc.
  - Soporta subfolders: `Tools::folder('MyFiles', 'Cache', 'temp')`
  - Retorna ruta completa

- `folderScan(string $path, string $extension = ''): array`
  - Escanea directorio
  - Si $extension especificada: solo esos archivos
  - Retorna array de nombres de archivos/carpetas

- `folderCheckOrCreate(string $path): bool`
  - Comprueba si carpeta existe, sino la crea
  - Permisos: 0755

- `folderDelete(string $path): bool`
  - Elimina carpeta recursivamente

#### URLs

- `url(string $path): string`
  - Genera URL desde ruta relativa
  - Ejemplo: `Tools::url('/Core/Assets/CSS/default.css')`

#### Slugs

- `slug(string $text, string $separator = '-', int $maxLength = 0): string`
  - Convierte texto a slug URL-safe
  - Ejemplo: `Tools::slug('Ventas de Marzo') => 'ventas-de-marzo'`

### Logging

- `log(string $channel = 'master'): Logger`
  - Crea Logger para canal especifico
  - Equivalente a `Logger::channel($channel)`

#### Mensajes Rapidos

- `logMessage(string $message, bool $log = true): void`
  - Añade mensaje a MiniLog
  - Si $log: tambien lo registra en Logger

- `logError(string $message): void`
  - Alias para log()->error()

- `logWarning(string $message): void`
  - Alias para log()->warning()

### Validacion

- `ipBanned(): bool`
  - Comprueba si IP esta baneada
  - Lee de tabla IpBanned

### Traducciones

- `trans(string $key, array $parameters = []): string`
  - Traduce cadena de texto
  - $parameters: reemplazos %clave%

---

## 10. HTML (TWIG)

Clase: `FacturaScripts\Core\Html`

Motor de plantillas Twig con extensiones personalizadas.

### Propiedades Privadas Estaticas

```
private static $functions = []         // TwigFunction[] funciones registradas
private static $loader                 // FilesystemLoader
private static $paths = []             // array de rutas de plantillas
private static $plugins = true         // bool permitir plugins
private static $twig                   // Environment instancia Twig
```

### Metodos Publicos Estaticos

#### Configuracion

- `addPath(string $name, string $path): void`
  - Añade ruta de plantillas a Twig
  - Nombre espacio de nombres para plantillas

- `addFunction(TwigFunction $function): void`
  - Registra funcion Twig personalizada

- `disablePlugins(bool $disable = true): void`
  - Habilita/deshabilita plugins en plantillas

#### Renderizado

- `render(string $template, array $params = []): string`
  - Renderiza plantilla Twig
  - Inyecta variables globales:
    - `assetManager`: gestor de assets (CSS/JS)
    - `debugBarRender`: barra debug (si debug=true)
    - `i18n`: instancia Translator
    - `log`: instancia MiniLog
  - Retorna HTML renderizado

### Funciones Twig Registradas

#### asset()

```twig
{{ asset('img/logo.png') }}
```

- Obtiene URL de asset
- Usa AssetManager
- Añade FS_ROUTE si esta configurado

#### cache()

```twig
{{ cache('clave') }}
```

- Obtiene valor de Cache
- Retorna vacio si no existe

#### config()

```twig
{{ config('timezone') }}
```

- Obtiene configuracion con Tools::config()

#### trans()

```twig
{{ trans('key-to-translate', {'%param%': value}) }}
```

- Traduce clave usando Translator
- Soporta parametros %clave%

#### money()

```twig
{{ money(1234.567) }}
```

- Formatea numero como moneda
- Usa configuracion de separadores

#### number()

```twig
{{ number(1234.567, 2) }}
```

- Formatea numero con decimales

#### date()

```twig
{{ date('2025-12-31') }}
```

- Formatea fecha con DATE_STYLE

#### dateTime()

```twig
{{ dateTime('2025-12-31 23:59:59') }}
```

- Formatea fecha y hora con DATETIME_STYLE

#### bytes()

```twig
{{ bytes(5368709120) }}
```

- Formatea bytes a formato legible

---

## 11. HTTP

Clase: `FacturaScripts\Core\Http`

Cliente HTTP basado en cURL para realizar peticiones.

### Propiedades Protegidas

```
protected $body                        // string respuesta
protected $data                        // mixed datos para enviar
protected $method                      // string metodo HTTP
protected $url                         // string URL destino
```

### Propiedades Privadas

```
private $curlOptions = []              // array opciones cURL
private $executed = false              // bool si se ejecuto
private $headers = []                  // array headers a enviar
private $responseHeaders = []          // array headers recibidos
private $statusCode = 0                // int codigo HTTP respuesta
public $error                          // string error si ocurrio
```

### Opciones cURL Default

```
CURLOPT_AUTOREFERER => 1               // Auto referer
CURLOPT_FOLLOWLOCATION => 1            // Seguir redirects
CURLOPT_RETURNTRANSFER => 1            // Retornar respuesta
CURLOPT_TIMEOUT => 30                  // Timeout 30 segundos
CURLOPT_USERAGENT => 'FacturaScripts [version]'
```

### Constructor y Creacion

```php
public function __construct(string $method, string $url, $data = [])
```

#### Factory Methods

- `get(string $url, $data = []): self` (static)
- `post(string $url, $data = []): self` (static)
- `put(string $url, $data = []): self` (static)
- `patch(string $url, $data = []): self` (static)
- `delete(string $url, $data = []): self` (static)

### Configuracion

- `header(string $name, string $value): self`
  - Añade header a peticion
  - Retorna $this para encadenamiento

- `bearerToken(string $token): self`
  - Añade header Authorization: Bearer $token

- `setTimeout(int $seconds): self`
  - Configura timeout en segundos
  - Default 30

### Ejecucion

- `exec(): self` (privado)
  - Ejecuta peticion cURL
  - Prepara headers, body, opciones
  - Guarda respuesta y codigo HTTP
  - Retorna $this

### Resultados

- `body(): string`
  - Retorna body de respuesta
  - Ejecuta si aun no se ejecuto

- `statusCode(): int`
  - Retorna codigo HTTP de respuesta

- `responseHeaders(): array`
  - Retorna array de headers recibidos

- `json()`
  - Parsea body como JSON
  - Decodifica con json_decode

#### Estados

- `ok(): bool`
  - Retorna true si status 200-299

- `failed(): bool`
  - Retorna true si no ok()

- `errorMessage(): string`
  - Retorna mensaje de error si fallo

---

## 12. TRANSLATOR

Clase: `FacturaScripts\Core\Translator`

Sistema de traduccion multiidioma.

### Propiedades Privadas Estaticas

```
private static $defaultLang = 'es_ES' // Idioma default
private static $languages = []        // array idiomas cargados
private static $notFound = []         // array traducciones no encontradas
private static $translations = []     // array de traducciones
```

### Propiedades Privadas

```
private $lang                          // string idioma actual
```

### Constructor

```php
public function __construct(?string $langCode = '')
```

- Si $langCode vacio: usa idioma default
- Si existe: carga ese idioma

### Metodos Publicos

#### Traduccion

- `trans(string $key, array $parameters = []): string`
  - Traduce clave de idioma actual
  - Soporta parametros %clave%
  - Si no encuentra: retorna la clave

- `customTrans(?string $langCode, ?string $txt, array $parameters = []): string`
  - Traduce texto en idioma especifico
  - Si $langCode vacio: usa default
  - $parameters: array con reemplazos

#### Idioma

- `setLang(string $langCode): void`
  - Configura idioma actual de instancia

- `getLang(): string`
  - Obtiene idioma actual

- `setDefaultLang(string $langCode): void` (static)
  - Configura idioma por defecto global

- `getDefaultLang(): string` (static)
  - Obtiene idioma por defecto

#### Carga de Idiomas

- `load(string $langCode): void` (privado)
  - Carga traducciones de idioma
  - Lee archivos JSON de Translation/
  - Crea clave: "nombre_traduccion@codigo_idioma"

#### Deployment

- `deploy(): void` (static)
  - Compila todas las traducciones
  - Lee carpetas Core/Translation y Plugins/*/Translation
  - Busca archivos .json por cada idioma
  - Genera archivo compilado en Dinamic/Translation

---

## 13. VALIDATOR

Clase: `FacturaScripts\Core\Validator`

Coleccion de validadores para diferentes tipos de datos.

### Metodos Publicos Estaticos

#### Strings

- `alphaNumeric(string $text, string $extra = '', int $min = 1, int $max = 99): bool`
  - Valida alfanumerico con caracteres opcionales
  - $extra: caracteres adicionales permitidos
  - min/max: longitud

- `string(string $text, int $min = 1, int $max = 99): bool`
  - Valida longitud de string
  - Retorna true si strlen entre min y max

#### Email

- `email(string $email): bool`
  - Valida email con FILTER_VALIDATE_EMAIL

#### URLs

- `url(string $url, bool $strict = false): bool`
  - Valida URL
  - Si $strict=false: interpreta 'www.' como https://www.
  - Valida javascript: como invalida siempre

#### Fechas

- `date(string $date): bool`
  - Valida fecha formato ESTRICTO 'd-m-Y' o 'Y-m-d'
  - Ejemplos: "31-12-2023", "2023-12-31"
  - Retorna true si es valida

#### Otros

- `numeric(string $value): bool`
  - Valida que sea numero

- `float(string $value): bool`
  - Valida que sea decimal

- `integer(string $value): bool`
  - Valida que sea entero

---

## 14. DBQUERY

Clase: `FacturaScripts\Core\DbQuery`

Query builder fluent para construir queries SQL de forma programatica.

### Propiedades Publicas

```
public $fields = '*'                   // string campos a seleccionar
public $groupBy                        // string clausula GROUP BY
public $having                         // string clausula HAVING
public $limit = 0                      // int LIMIT de resultados
public $offset = 0                     // int OFFSET de resultados
public $orderBy = []                   // array campos para ORDER BY
```

### Propiedades Privadas

```
private $table                         // string tabla
private $where = []                    // Where[] condiciones WHERE
```

### Constructor

```php
public function __construct(string $table)
```

### Magic Methods

- `__call(string $method, array $parameters)`
  - Permite llamadas dinamicas whereNombre(), whereCiudad(), etc.
  - Convierte a whereEq($field, $value)

### Metodos SELECT

#### Proyeccion

- `select(string $fields): self`
  - Configura campos a seleccionar
  - Default: '*'

#### Filtraje

- `where(string $fields, $value, string $operator = '=', string $operation = 'AND'): self`
  - Añade condicion WHERE
  - operation: 'AND' o 'OR'

- `whereEq(string $fields, $value): self`
  - WHERE campo = valor (AND)

- `whereNot(string $fields, $value): self`
  - WHERE campo != valor

- `whereGt(string $fields, $value): self`
  - WHERE campo > valor

- `whereGte(string $fields, $value): self`
  - WHERE campo >= valor

- `whereLt(string $fields, $value): self`
  - WHERE campo < valor

- `whereLte(string $fields, $value): self`
  - WHERE campo <= valor

- `whereLike(string $fields, $value): self`
  - WHERE campo LIKE %valor%

- `whereBetween(string $fields, $value1, $value2): self`
  - WHERE campo BETWEEN valor1 AND valor2

- `whereIn(string $fields, array $values): self`
  - WHERE campo IN (valores)

- `whereRaw(string $sql): self`
  - Añade WHERE raw SQL

#### Agrupamiento

- `groupBy(string $field): self`
  - Añade GROUP BY

- `having(string $having): self`
  - Añade HAVING

#### Ordenamiento

- `orderBy(string $field, string $direction = 'ASC'): self`
  - Añade ORDER BY
  - Soporta multiples campos

- `orderByRaw(string $sql): self`
  - ORDER BY raw SQL

#### Paginacion

- `limit(int $limit): self`
  - LIMIT de resultados

- `offset(int $offset): self`
  - OFFSET en resultados

- `paginate(int $page, int $perPage): self`
  - Pagina automatica
  - Calcula offset = (page-1)*perPage

### Metodos Agregacion

- `count(string $field = ''): int`
  - Cuenta filas
  - Si $field: COUNT(DISTINCT $field)

- `countArray(string $field, string $groupByKey): array`
  - Cuenta agrupado por clave

- `avg(string $field, ?int $decimals = null): float`
  - Promedio de campo

- `avgArray(string $field, string $groupByKey): array`
  - Promedio agrupado

- `sum(string $field, ?int $decimals = null): float`
  - Suma de campo

- `sumArray(string $field, string $groupByKey): array`
  - Suma agrupada

### Metodos Ejecucion

- `get(): array`
  - Ejecuta SELECT y retorna array de filas

- `first(): array`
  - Ejecuta SELECT LIMIT 1
  - Retorna primera fila o array vacio

- `array(string $key, string $value): array`
  - Retorna array asociativo [key => value]

- `delete(): bool`
  - Ejecuta DELETE WHERE
  - Retorna true si exito

- `update(array $values): bool`
  - Ejecuta UPDATE SET
  - Retorna true si exito

---

## 15. WHERE

Clase: `FacturaScripts\Core\Where`

Construccion de clausulas WHERE SQL.

### Constantes

```
const FIELD_SEPARATOR = '|'            // Separador para multiples campos
```

### Propiedades Publicas

```
public $fields                         // string campo(s)
public $operator                       // string operador (=, >, <, LIKE, IN, etc.)
public $operation                      // string AND u OR
public $subWhere = []                  // Where[] subcondiciones
public $useField                       // bool si el valor es otro campo
public $value                          // mixed valor a comparar
```

### Constructor

```php
public function __construct(string $fields, $value, string $operator = '=', string $operation = 'AND', bool $useField = false)
```

### Factory Methods (static)

#### Operadores Igualdad

- `eq(string $fields, $value): self`
  - WHERE campo = valor

- `neq(string $fields, $value): self`
  - WHERE campo != valor

#### Operadores Comparacion

- `gt(string $fields, $value): self`
  - WHERE campo > valor

- `gte(string $fields, $value): self`
  - WHERE campo >= valor

- `lt(string $fields, $value): self`
  - WHERE campo < valor

- `lte(string $fields, $value): self`
  - WHERE campo <= valor

#### Operadores de Texto

- `like(string $fields, $value): self`
  - WHERE campo LIKE %valor%

- `startsWith(string $fields, $value): self`
  - WHERE campo LIKE valor%

- `endsWith(string $fields, $value): self`
  - WHERE campo LIKE %valor

- `regexp(string $fields, $value): self`
  - WHERE campo REGEXP valor

#### Operadores de Rango

- `between(string $fields, $value1, $value2): self`
  - WHERE campo BETWEEN valor1 AND valor2

- `in(string $fields, $values): self`
  - WHERE campo IN (valores)

- `notIn(string $fields, $values): self`
  - WHERE campo NOT IN (valores)

#### Operadores Avanzados

- `column(string $fields, $value, string $operator = '=', string $operation = 'AND'): self`
  - Comparacion entre campos (campo1 = campo2)

### Metodos de Instancia

- `useField(): self`
  - Marca que $value es otro campo, no valor literal
  - Retorna $this para encadenamiento

### Metodos Privados Estaticos

- `multiSql(Where[] $where): string`
  - Genera SQL desde array de Where
  - Combina con operadores AND/OR

---

## 16. WORKQUEUE

Clase: `FacturaScripts\Core\WorkQueue`

Cola de trabajos en segundo plano (eventos y workers).

### Propiedades Privadas Estaticas

```
private static $new_events = []       // array de eventos nuevos a procesar
private static $prevent_new_events = [] // array de eventos a no procesar
private static $workers_list = []     // array de workers registrados
```

### Metodos Publicos Estaticos

#### Registro de Workers

- `addWorker(string $worker_name, string $event = '*', int $position = 0): void`
  - Registra worker para procesar eventos
  - $event: patron de evento ('Model.Usuario.Save', 'Model.*', etc.)
  - $position: orden de ejecucion
  - Obtiene clase del worker: FacturaScripts\Dinamic\Worker\[worker_name]Worker

#### Manejo de Eventos

- `newEvent(string $event, array $data = []): void`
  - Registra evento nuevo para procesar
  - Si event esta en prevent_new_events: no se registra

- `preventNewEvents(array $event_names): void`
  - Lista de eventos a no procesar en esta ejecucion
  - Ejemplo: `WorkQueue::preventNewEvents(['Model.Usuario.Save'])`

#### Coincidencia de Eventos

- `matchEvent(string $pattern, string $event): bool` (static)
  - Compara patron con evento
  - $pattern='*' coincide con todo
  - $pattern='Model.*' coincide con 'Model.Usuario.Save'

#### Ejecucion

- `run(): bool`
  - Ejecuta cola de trabajos
  - Crea lock para evitar duplicacion
  - Lee WorkEvent de BD con creation_date <= ahora y done=false
  - Para cada evento: ejecuta workers que coincidan
  - Retorna true si se ejecuto algo

### Metodos Privados Estaticos

- `getWorkersList(): array`
  - Retorna array de workers registrados

- `preventDuplicated(WorkEvent $event): void`
  - Evita procesar el mismo evento varias veces

- `clear(): void`
  - Limpia listas de eventos y workers

---

## 17. NEXTCODE

Clase: `FacturaScripts\Core\NextCode`

Generacion de codigos secuenciales con bloqueo.

### Metodos Publicos Estaticos

#### Generacion

- `get(string $table, string $column, string $type = 'int'): ?int`
  - Obtiene proximo codigo secuencial para tabla/columna
  - type: 'int', 'integer', 'serial' u otro (se trata como texto)
  - Si no numerico: busca numeros dentro de texto
  - Retorna proximo numero disponible o null si falla lock
  - Usa sistema de archivos .lock para evitar duplicacion

#### Limpieza

- `clearOld(): void`
  - Elimina archivos .lock mas antiguos de 1 hora
  - Scan carpeta MyFiles/Tmp
  - Borra .lock expirados

### Metodos Privados

- `lock(string $table, string $column, int $value): ?int`
  - Intenta crear archivo de bloqueo para codigo
  - Nombre: table_column_value.lock
  - Retorna $value si exito, incrementa y reintenta si existe
  - Intenta max 9 veces
  - Retorna null si no consigue lock despues de intentos

---

## 18. MIGRATIONS

Clase: `FacturaScripts\Core\Migrations`

Sistema de migraciones para cambios de BD.

### Constantes

```
const FILE_NAME = 'migrations.json'   // Archivo que registra migraciones ejecutadas
```

### Propiedades Privadas Estaticas

```
private static $database               // DataBase instancia
```

### Metodos Publicos Estaticos

#### Migraciones Core

- `run(): void`
  - Ejecuta todas las migraciones core
  - clearLogs, fixSeries, fixAgentes, fixApiKeysUsers, etc.
  - Cada una se ejecuta solo una vez

#### Migraciones de Plugins

- `runPluginMigration(MigrationClass $migration): void`
  - Ejecuta una migracion de plugin
  - Verifica que no este ejecutada
  - Marca como ejecutada

- `runPluginMigrations(array $migrations): void`
  - Ejecuta array de migraciones de plugin

### Metodos Privados Estaticos

- `runMigration(string $name, callable $callback): void`
  - Ejecuta una migracion si no esta marcada como ejecutada
  - Marca como ejecutada en migrations.json

- `isMigrationExecuted(string $name): bool`
  - Comprueba si migracion ya se ejecuto

- `markMigrationAsExecuted(string $name): void`
  - Marca migracion como ejecutada

- `clearLogs(): void`
  - Elimina logs antiguos si hay mas de 20000

- `fixSeries(), fixAgentes(), etc.`
  - Migraciones especificas para corregir datos

---

## 19. DBUPDATER

Clase: `FacturaScripts\Core\DbUpdater`

Actualiza estructura de BD desde definiciones XML.

### Constantes

```
const FILE_NAME = 'db-updater.json'   // Archivo que registra tablas checadas
const CHANGELOG_FILE = 'db-changelog.json' // Log de cambios
```

### Propiedades Privadas Estaticas

```
private static $checked_tables        // array de tablas ya procesadas
private static $db                    // DataBase instancia
private static $last_error            // string ultimo error
private static $sql_tool              // DataBaseQueries herramienta SQL
```

### Metodos Publicos Estaticos

#### Creacion/Actualizacion de Tablas

- `createOrUpdateTable(string $table_name, array $structure = [], string $sql_after = ''): bool`
  - Si tabla existe: actualiza
  - Si no existe: crea

- `createTable(string $table_name, array $structure = [], string $sql_after = ''): bool`
  - Crea tabla desde estructura
  - Si $structure vacio: lee de XML
  - $sql_after: SQL adicional despues de CREATE

- `updateTable(string $table_name, array $structure = [], array $oldStructure = []): bool`
  - Actualiza tabla con nueva estructura
  - Compara con estructura antigua y aplica ALTER TABLE necesarios

- `dropTable(string $table_name): bool`
  - Elimina tabla
  - Registra en changelog

#### Columnas

- `createColumn(string $table_name, string $column_name, array $columnDef): bool`
  - Añade columna a tabla

- `dropColumn(string $table_name, string $column_name): bool`
  - Elimina columna

- `modifyColumn(string $table_name, string $column_name, array $columnDef): bool`
  - Modifica definicion de columna

#### Indices y Restricciones

- `createIndex(string $table_name, array $indexData): bool`
  - Crea indice

- `createConstraint(string $table_name, array $constraintData): bool`
  - Crea constraint (FK, UNIQUE, etc.)

- `dropConstraint(string $table_name, string $constraint_name): bool`
  - Elimina constraint

#### Rebuild

- `rebuild(): void`
  - Reconstruye estructura de BD desde XML
  - Valida todas las tablas core y plugins
  - Aplica cambios necesarios

#### Obtener Info

- `getTableStructure(string $table_name): array`
  - Obtiene estructura actual de tabla desde BD

- `getLastError(): ?string`
  - Retorna ultimo error ocurrido

---

## 20. BASE/CONTROLLER

Clase: `FacturaScripts\Core\Base\Controller`

Clase base de la que heredan todos los controladores.

### Propiedades Protegidas

```
protected $dataBase                   // DataBase acceso a BD
protected $response                   // Response objeto respuesta HTTP
```

### Propiedades Publicas

```
public $empresa                       // Empresa seleccionada
public $permissions                   // ControllerPermissions permisos
public $request                       // Request objeto peticion HTTP
public $title                         // string titulo pagina
public $uri                           // string URI solicitada
public $user                          // User|false usuario logueado
public $multiRequestProtection        // MultiRequestProtection CSRF
```

### Propiedades Privadas

```
private $className                    // string nombre clase controlador
private $template                     // string|false nombre template
```

### Constructor

```php
public function __construct(string $className, string $uri = '')
```

- Inicializa todas las propiedades
- Obtiene datos de pagina con getPageData()
- Configura titulo
- Carga assets para pagina
- Valida version PHP >= 8.0

### Metodos Publicos Abstractos (implementar en subclase)

- `getPageData(): array`
  - Retorna array con propiedades pagina
  - Propiedades esperadas: title, menu, showonmenu, icon, orden, etc.

- `run(): void`
  - Metodo principal de ejecucion
  - Implementado por subclases

### Metodos de Respuesta

- `setTemplate(string $template): void`
  - Configura nombre plantilla Twig

- `getTemplate(): string`
  - Obtiene nombre plantilla

- `render(): string`
  - Renderiza plantilla con parametros

- `json($data, int $statusCode = 200): void`
  - Devuelve JSON
  - Configura header application/json

- `view(string $template, array $params = []): string`
  - Renderiza vista y devuelve contenido

### Metodos de Seguridad

- `checkPermission(string $permission): bool`
  - Valida que usuario tenga permiso

- `checkLogin(): bool`
  - Valida que usuario este logueado

- `getUserLogged(): User|false`
  - Obtiene usuario logueado

---

## 21. BASE/DATABASE

Clase: `FacturaScripts\Core\Base\DataBase`

Abstraccion de acceso a BD (soporta MySQL y PostgreSQL).

### Propiedades Privadas

```
private $connected = false            // bool si esta conectado
private $engine                       // DataBaseEngine MySQL o PostgreSQL
private $link                         // conexion BD
```

### Metodos Publicos

#### Conexion

- `connect(): bool`
  - Conecta a BD segun config
  - Lee DB_TYPE, DB_HOST, DB_USER, DB_PASSWORD, DB_NAME
  - Retorna true si exito

- `connected(): bool`
  - Retorna true si esta conectado

- `close(): bool`
  - Cierra conexion a BD

#### Transacciones

- `beginTransaction(): bool`
  - Inicia transaccion

- `commit(): bool`
  - Confirma cambios

- `rollback(): bool`
  - Revierte cambios

#### Consultas SQL

- `exec(string $sql): bool`
  - Ejecuta SQL (INSERT, UPDATE, DELETE)
  - Retorna true si exito

- `select(string $sql): array`
  - Ejecuta SELECT
  - Retorna array de filas (asociativo)

- `selectSingle(string $sql): array`
  - Ejecuta SELECT LIMIT 1
  - Retorna primera fila o array vacio

#### Estructura BD

- `tableExists(string $tableName): bool`
  - Comprueba si tabla existe

- `getColumns(string $tableName): array`
  - Obtiene columnas de tabla
  - Retorna array con definiciones

- `getConstraints(string $tableName): array`
  - Obtiene constraints (FK, UNIQUE) de tabla

- `getIndexes(string $tableName): array`
  - Obtiene indices de tabla

#### Escapado

- `escapeColumn(string $name): string`
  - Escapa nombre de columna con comillas apropiadaa para BD

- `escapeString(string $value): string`
  - Escapa string para SQL

- `escapeLike(string $value): string`
  - Escapa para clausula LIKE

#### Info BD

- `type(): string`
  - Retorna tipo de BD: 'mysql' o 'postgresql'

- `version(): string`
  - Retorna version de BD

- `getEngine(): DataBaseEngine`
  - Retorna engine actual (MySQL o PostgreSQL)

---

## 22. CONTRATOS E INTERFACES

### ErrorControllerInterface

Interfaz: `FacturaScripts\Core\Contract\ErrorControllerInterface`

```php
public function run(): void            // Ejecutar manejo de error
```

### ControllerInterface

Interfaz: `FacturaScripts\Core\Contract\ControllerInterface`

```php
public function run(): void            // Metodo principal
public function getPageData(): array   // Datos de la pagina
```

### CalculatorModInterface

Interfaz: `FacturaScripts\Core\Contract\CalculatorModInterface`

```php
public function apply(LineaCompra|LineaVenta $line): void
public function applyTaxToLine(LineaCompra|LineaVenta $line): void
public function orderBy(): int         // Orden de aplicacion
```

### SalesModInterface

Interfaz: `FacturaScripts\Core\Contract\SalesModInterface`

```php
public function applyHeaders(FacturaCliente $invoice): void
```

### PurchasesModInterface

Interfaz: `FacturaScripts\Core\Contract\PurchasesModInterface`

```php
public function applyHeaders(FacturaProveedor $invoice): void
```

### SalesLineModInterface

Interfaz: `FacturaScripts\Core\Contract\SalesLineModInterface`

```php
public function apply(LineaFacturaCliente $line): void
```

### PurchasesLineModInterface

Interfaz: `FacturaScripts\Core\Contract\PurchasesLineModInterface`

```php
public function apply(LineaFacturaProveedor $line): void
```

---

## 23. ERROR HANDLERS

Clases en `FacturaScripts\Core\Error\`:

### DefaultError

Manejador default para excepciones no especificadas.

- Captura excepciones genericas
- Muestra pantalla de error con detalles

### PageNotFound

Manejador para rutas no encontradas (404).

### AccessDenied

Manejador para acceso denegado (403).

### AuthenticationRequired

Manejador para autenticacion requerida (401).

### DatabaseError

Manejador para errores de BD.

### InvalidApiToken

Manejador para token API invalido.

### InvalidApiVersion

Manejador para version API invalida.

### InvalidApiResource

Manejador para recurso API invalido.

### IpBannedOnApi

Manejador para IP baneada en API.

### UnsafeFile, UnsafeFolder

Manejadores para acceso a archivos inseguros.

### FileNotFound

Manejador para archivo no encontrado.

### MissingApiVersion

Manejador para version API faltante.

### AlreadyInstalled

Manejador para instalacion duplicada.

---

## 24. DATASRC

Clases en `FacturaScripts\Core\DataSrc\`:

Proporcionan datos precargados y cacheados.

### Agentes

- `all(): Agente[]` - Todos los agentes
- `get(string $code): ?Agente` - Agente por codigo
- `getDefault(): ?Agente` - Agente por defecto

### Almacenes

- `all(): Almacen[]` - Todos los almacenes
- `get(string $code): ?Almacen` - Almacen por codigo
- `getDefault(): ?Almacen` - Almacen por defecto

### Divisas

- `all(): Divisa[]` - Todas las divisas
- `get(string $code): ?Divisa` - Divisa por codigo
- `getDefault(): ?Divisa` - Divisa por defecto

### Empresas

- `all(): Empresa[]` - Todas las empresas
- `get(string $code): ?Empresa` - Empresa por codigo
- `getDefault(): ?Empresa` - Empresa por defecto

### Formas de Pago

- `all(): FormaPago[]` - Todas las formas de pago
- `get(string $code): ?FormaPago` - Forma de pago por codigo

### Series

- `all(): Serie[]` - Todas las series
- `get(string $code): ?Serie` - Serie por codigo
- `getDefault(): ?Serie` - Serie por defecto

---

## 25. INTERNAL

### Plugin

Clase: `FacturaScripts\Core\Internal\Plugin`

Representa un plugin instalado.

#### Propiedades Publicas

```
public $author                        // string autor
public $compatible                    // bool compatibilidad
public $description                   // string descripcion
public $enabled                       // bool si esta habilitado
public $folder                        // string carpeta del plugin
public $hidden                        // bool si esta oculto
public $installed                     // bool si esta instalado
public $name                          // string nombre unico
public $order                         // int orden ejecucion
public $post_disable                  // bool ejecutar post_disable
public $post_enable                   // bool ejecutar post_enable
public $requirements                  // array dependencias
public $version                       // string version
```

#### Metodos

- `getFromZip(string $zipPath): ?Plugin` (static)
  - Crea Plugin desde archivo ZIP
  - Lee facturascripts.ini

- `delete(): bool`
  - Elimina carpeta del plugin

- `disabled(): bool`
  - Retorna !$enabled

- `exists(): bool`
  - Comprueba si carpeta del plugin existe

- `dependenciesOk(array $enabledPlugins, bool $log = false): bool`
  - Valida que dependencias esten habilitadas

### Headers

Clase: `FacturaScripts\Core\Internal\Headers`

Manejo de headers HTTP.

- Constructor desde array $_SERVER
- Metodos para acceder headers normalizados

### ResponseHeaders

Clase: `FacturaScripts\Core\Internal\ResponseHeaders`

Headers de respuesta HTTP.

### SubRequest

Clase: `FacturaScripts\Core\Internal\SubRequest`

Encapsula datos de un tipo de request (GET, POST, cookies).

- `get(string $key, $default = null)`
- `getArray(string $key): array`
- `getInt(string $key, ?int $default = null): ?int`
- `getFloat(string $key, ?float $default = null): ?float`
- `getBool(string $key, ?bool $default = null): ?bool`
- `getString(string $key, ?string $default = null): ?string`
- `getAlnum(string $key): string`
- `getEmail(string $key, ?string $default = null): ?string`
- `getDate(string $key, ?string $default = null): ?string`
- `getDateTime(string $key, ?string $default = null): ?string`
- `getHour(string $key, ?string $default = null): ?string`
- `getUrl(string $key, ?string $default = null): ?string`
- `getOnly(string $key, array $values): ?string`
- `has(string $key): bool`
- `all(): array`

### RequestFiles

Clase: `FacturaScripts\Core\Internal\RequestFiles`

Manejo de archivos subidos.

### PluginsDeploy

Clase: `FacturaScripts\Core\Internal\PluginsDeploy`

Despliegue de plugins.

- `run(array $enabledPlugins, bool $clean = true): void` (static)
  - Ejecuta despliegue de plugins habilitados
  - Copia archivos a carpetas Dinamic

- `initControllers(): void` (static)
  - Inicializa controladores de plugins

---

## 26. CRASHREPORT, DEBUGBAR, TELEMETRY, UPLOADEDFILE

### CrashReport

Clase: `FacturaScripts\Core\CrashReport`

Manejo de errores fatales.

- `init(): void` (static)
  - Registra handler de shutdown
  - Inicia buffering de salida

- `getErrorFragment(string $file, int $line, int $linesToShow = 10, bool $html = false): string` (static)
  - Obtiene fragmento de codigo fuente con error

- `getErrorInfo(int $code, string $message, string $file, int $line): array` (static)
  - Obtiene informacion completa del error
  - Genera hash y URL de reporte

- `shutdown(): void` (static)
  - Ejecutado al cierre de script
  - Captura errores fatales

### DebugBar

Clase: `FacturaScripts\Core\DebugBar`

Barra de debug que se muestra en pie de pagina.

- `render(): string`
  - Renderiza HTML de barra de debug

- `renderHead(): string`
  - Renderiza CSS y JS de barra

### Telemetry

Clase: `FacturaScripts\Core\Telemetry`

Envio de telemetria anonima (si esta registrada).

- `__construct()`
  - Lee datos de telemetria de configuracion

- `claimUrl(): string`
  - Genera URL para reclamar instalacion

- `getMetadata(): array`
  - Obtiene metadata del servidor

- `update(): self`
  - Actualiza telemetria si es necesario

- `collectData(bool $onlyClaim = false): array` (privado)
  - Recopia datos para telemetria

### UploadedFile

Clase: `FacturaScripts\Core\UploadedFile`

Representa archivo subido.

#### Propiedades Publicas

```
public $error                         // int codigo de error
public $name                          // string nombre original
public $size                          // int tamaño en bytes
public $tmp_name                      // string ruta temporal
public $type                          // string mime type
public $test = false                  // bool si es modo test
```

#### Metodos

- `extension(): string`
  - Obtiene extension del archivo

- `getClientMimeType(): string`
  - Obtiene mime type

- `getClientOriginalName(): string`
  - Obtiene nombre original

- `getClientOriginalExtension(): string` (deprecated)
  - Alias de extension()

- `getErrorMessage(): string`
  - Obtiene mensaje de error

- `isValid(): bool`
  - Comprueba que archivo sea valido

- `move(string $destination, string $newName = ''): bool`
  - Mueve archivo a carpeta destino

---

**Documento generado para FacturaScripts 2025 - Referencia Arquitectonica Completa**
