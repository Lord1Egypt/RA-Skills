# Referencia Completa de la API REST de FacturaScripts 2025

## Tabla de Contenidos

1. [Arquitectura de la API](#arquitectura-de-la-api)
2. [Recursos Automaticos por Modelo](#recursos-automaticos-por-modelo)
3. [Gestion de API Keys](#gestion-de-api-keys)
4. [Recursos Personalizados](#recursos-personalizados)
5. [Ejemplos Practicos de Uso](#ejemplos-practicos-de-uso)
6. [Uso desde Codigo Externo](#uso-desde-codigo-externo)
7. [Como Crear un MCP Server para FacturaScripts](#como-crear-un-mcp-server-para-facturascripts)

---

## Arquitectura de la API

### Introduccion General

FacturaScripts proporciona una API REST completamente funcional en la versión 3 (API_VERSION = 3) que permite acceder y manipular todos los datos del sistema de manera programatica. La API está construida sobre un sistema de autenticación robusto, control de acceso granular y manejo de errores comprensivo.

### Flujo General de una Peticion API

Cuando se realiza una peticion a la API, el flujo es el siguiente:

1. **Solicitud HTTP** llega al servidor en la URL `/api/3/{recurso}/{id?}/{parametros?}`
2. **ApiController** (clase base: `FacturaScripts\Core\Template\ApiController`) recibe la solicitud
3. **Validacion de Habilitacion**: Se verifica que la API esté habilitada (config `api_key` o setting `enable_api`)
4. **CORS y OPTIONS**: Se manejan solicitudes preflight CORS automaticamente
5. **Verificacion de IP Bloqueada**: Se comprueba si la IP tiene demasiados intentos fallidos (cache de incidentes)
6. **Validacion del Token**: Se verifica el header `X-Auth-Token` o `Token` contra:
   - Token global configurado en `config('api_key')` (acceso completo)
   - Token de base de datos en tabla `api_keys` (acceso controlado)
7. **Verificacion de Permisos**: Se comprueba si la API Key tiene permiso para el recurso solicitado
8. **Validacion de Version**: Se verifica que se use API v3
9. **Enrutamiento de Recurso**: Se carga la clase API correspondiente del recurso
10. **Procesamiento**: Se llama al metodo correspondiente (`doGET()`, `doPOST()`, `doPUT()`, `doDELETE()`)
11. **Respuesta JSON**: Se devuelve la respuesta en JSON con el codigo HTTP apropriado

### Clase ApiController

**Ubicacion**: `/Core/Template/ApiController.php`

**Constantes principales**:
```php
const API_VERSION = 3;                     // Version actual de la API
const INCIDENT_EXPIRATION_TIME = 600;      // Tiempo de expiracion de incidentes (segundos)
const IP_LIST = 'api-ip-list';            // Clave del cache para lista de IPs
const MAX_INCIDENT_COUNT = 5;              // Numero maximo de incidentes antes de bloquear IP
```

**Atributos principales**:
- `$apiKey`: Objeto ApiKey con datos de la clave autenticada
- `$request`: Objeto Request con acceso a parametros HTTP
- `$response`: Objeto Response para enviar respuestas
- `$url`: La URL de la solicitud

**Flujo detallado del metodo run()**:

```php
1. Verifica si API está habilitada
2. Si es solicitud OPTIONS, responde headers CORS y sale
3. Verifica si IP está bloqueada (MAX_INCIDENT_COUNT excedido)
4. Valida el token de autenticacion
5. Verifica permisos para el recurso
6. Valida la version de API (debe ser v3)
7. Establece headers CORS en respuesta
8. Ejecuta runResource() (implementado en subclases)
9. Envia la respuesta
```

**Metodos de utilidad**:

- `getUriParam(int $num): string` - Obtiene un parametro de la URL por posicion
- `db(): DataBase` - Obtiene conexion a base de datos (singleton)

### Clase APIResourceClass (Base Abstracta)

**Ubicacion**: `/Core/Lib/API/Base/APIResourceClass.php`

Esta es la clase base para todos los recursos de API. Define la estructura para procesar peticiones HTTP.

**Atributos protegidos**:
```php
protected $method;       // HTTP method (GET, POST, PUT, DELETE, PATCH)
protected $params;       // Array de parametros de URL (/api/3/recurso/{param1}/{param2})
protected $request;      // Objeto Request
protected $response;     // Objeto Response
```

**Metodos abstractos que deben implementarse**:
```php
abstract public function getResources(): array;
```

Debe devolver un array asociativo donde cada clave es el nombre publico del recurso y el valor es un array con:
```php
[
    'API' => 'Clase\Del\Recurso\API',  // Clase que procesa el recurso
    'Name' => 'NombreDelModelo'         // Nombre del modelo para cargar
]
```

**Metodos de procesamiento HTTP** (pueden ser sobrescritos):
```php
public function doDELETE(): bool
public function doGET(): bool
public function doPOST(): bool
public function doPUT(): bool
```

**Flujo en processResource()**:
```php
1. Obtiene el metodo HTTP de la solicitud
2. Segun el metodo, llama al metodo correspondiente (doGET, doPOST, etc.)
3. Si ocurre una excepcion, la captura y responde con error 500
4. Devuelve true si fue exitoso, false si hay error
```

**Metodos de respuesta protegidos**:

```php
protected function returnResult(array $data): void
// Responde con HTTP_OK (200) y devuelve datos JSON

protected function setOk(string $message, ?array $data = null): void
// Responde exitosamente con mensaje de confirmacion
// Estructura: { "ok": "mensaje", "data": {...} }

protected function setError(string $message, ?array $data = null, 
                           int $status = HTTP_BAD_REQUEST): void
// Responde con error y codigo HTTP especifico
// Estructura: { "error": "mensaje", "data": {...} }
```

### Clase APIModel

**Ubicacion**: `/Core/Lib/API/APIModel.php`

Extiende `APIResourceClass` y proporciona CRUD automatico para cualquier modelo de la aplicacion.

**Funcionalidad CRUD**:

**doGET()**:
- Sin parametros: lista todos los registros con filtros, paginacion y ordenamiento
- Con "schema": devuelve el esquema del modelo (tipos de campos, defaults, nullable)
- Con ID: devuelve un registro especifico

**doPOST()**:
- Crea un nuevo registro
- Los datos se envian en el body de la solicitud
- Verifica que no sea un duplicado

**doPUT()**:
- Actualiza un registro existente
- Requiere el ID en la URL o en los datos
- El registro debe existir

**doDELETE()**:
- Elimina un registro
- Requiere el ID en la URL

**Filtrado, Paginacion y Ordenamiento en GET**:

El metodo `listAll()` procesa:
- `filter`: Array de filtros (parametros de query: `filter[campo_operador]=valor`)
- `limit`: Numero de registros a devolver (default: 50)
- `offset`: Desplazamiento para paginacion (default: 0)
- `operation`: Operador logico entre filtros ('AND' o 'OR')
- `sort`: Array de campos para ordenamiento

**Operadores de Filtro soportados**:

Los filtros se especifican aniadiendo sufijos al nombre del campo:

| Sufijo | Operador SQL | Ejemplo |
|--------|--------------|---------|
| `_gt` | `>` | `field_gt=100` |
| `_gte` | `>=` | `field_gte=100` |
| `_lt` | `<` | `field_lt=50` |
| `_lte` | `<=` | `field_lte=50` |
| `_neq` | `!=` | `field_neq=valor` |
| `_like` | `LIKE` | `field_like=%patron%` |
| `_null` | `IS NULL` | `field_null` |
| `_notnull` | `IS NOT NULL` | `field_notnull` |
| `_isnot` | `IS NOT` | `field_isnot=valor` |
| (sin sufijo) | `=` | `field=valor` |

**Metodo getResourcesFromFolder()**:

Escanea la carpeta `Dinamic/Model` y crea recursos automaticamente para cada modelo disponible. El nombre del recurso es el plural del nombre del modelo:
- Cliente -> clientes
- Proveedor -> proveedores
- FacturaCliente -> facturasclientes
- Etc.

**Reglas de pluralizacion**:
- Si termina en 's': no cambia
- Si termina en 'a', 'e', 'i', 'o', 'u', 'k': agrega 's'
- Si termina en 'ser': agrega 's'
- Si termina en 'tion': agrega 's'
- En otro caso: agrega 'es'

### Autenticacion

La API soporta dos metodos de autenticacion:

#### 1. Token Global (Acceso Completo)

Se configura en `config('api_key')` o mediante la constante en el archivo de configuracion.

Proporciona acceso completo a todos los recursos sin restricciones.

Uso en solicitudes:
```http
GET /api/3/clientes HTTP/1.1
X-Auth-Token: token_secreto_global
```

O alternativamente:
```http
GET /api/3/clientes HTTP/1.1
Token: token_secreto_global
```

#### 2. API Keys de Base de Datos

Se crean en la interfaz de FacturaScripts y se almacenan en la tabla `api_keys`.

Permiten control granular de permisos por recurso y operacion.

Uso en solicitudes:
```http
GET /api/3/clientes HTTP/1.1
X-Auth-Token: clave_api_de_base_datos
```

**Validacion de Token**:
- Se extrae del header `X-Auth-Token` (o `Token` como respaldo)
- Se compara contra `config('api_key')` para acceso global
- Si no coincide, se busca en tabla `api_keys` con condiciones:
  - `apikey = token`
  - `enabled = true`

Si ninguno coincide, se rechaza la solicitud con error 401 (Unauthorized).

**Proteccion contra ataques de fuerza bruta**:

Cada intento fallido registra un "incidente":
- Se almacena en cache: `IP -> tiempo_actual`
- Si una IP genera 5 incidentes en 600 segundos, queda bloqueada
- Error: 429 (Too Many Requests)

### Formato de Respuestas

Todas las respuestas de API son en formato JSON.

#### Respuesta Exitosa (GET con datos):
```json
[
  {
    "id": 1,
    "nombre": "Cliente A",
    "email": "cliente@ejemplo.com",
    ...
  },
  ...
]
```

**Con header especial**:
```
X-Total-Count: 150
```

Este header contiene el numero total de registros (sin paginacion) para facilitar la paginacion cliente-side.

#### Respuesta Exitosa (POST/PUT/DELETE):
```json
{
  "ok": "Registro actualizado correctamente",
  "data": {
    "id": 1,
    "nombre": "Nuevo Nombre",
    ...
  }
}
```

#### Respuesta GET de Schema:
```json
{
  "id": {
    "type": "int",
    "default": null,
    "is_nullable": false
  },
  "nombre": {
    "type": "string",
    "default": "",
    "is_nullable": true
  },
  ...
}
```

#### Respuesta de Error:
```json
{
  "error": "Descripcion del error",
  "data": { ... }  // Opcional, solo en algunos casos
}
```

### Codigos de Error HTTP

La API usa los siguientes codigos de estado HTTP:

| Codigo | Significado | Caso de Uso |
|--------|------------|-----------|
| 200 OK | Exito | Solicitud procesada correctamente |
| 400 Bad Request | Solicitud invalida | Datos incompletos o invalidos |
| 401 Unauthorized | Token invalido | Token inexistente o incorrecto |
| 403 Forbidden | Permiso denegado | API Key sin acceso al recurso |
| 404 Not Found | Recurso no encontrado | Recurso o registro inexistente |
| 405 Method Not Allowed | Metodo no permitido | Usando GET en endpoint POST-only |
| 409 Conflict | API deshabilitada | API no activada en configuracion |
| 422 Unprocessable Entity | Error en validacion/guardado | Datos que no cumplen validacion |
| 429 Too Many Requests | IP bloqueada | Demasiados intentos fallidos |
| 500 Internal Server Error | Error del servidor | Excepcion no controlada |

**Handlers de error específicos para API**:

1. **DisabledApi** (409): API no habilitada
2. **InvalidApiToken** (401): Token incorrecto o ausente
3. **InvalidApiVersion** (400): Version de API incorrecta
4. **InvalidApiResource** (404): Recurso no existe
5. **ForbiddenApiEndpoint** (403): Sin permisos para recurso
6. **IpBannedOnApi** (429): IP bloqueada por incidentes

### Endpoint del Directorio de Recursos

**GET /api/3/**

Sin parametros, lista todos los recursos disponibles:

```json
{
  "resources": [
    "clientes",
    "proveedores",
    "productos",
    "facturas",
    "crearFacturaCliente",
    "crearAlbaranCliente",
    ...
  ]
}
```

Util para descubrir dinamicamente los recursos disponibles.

---

## Recursos Automaticos por Modelo

### Concepto General

Cada modelo en FacturaScripts expone automaticamente una interfaz CRUD a traves de la API. No requiere codigo adicional.

El mapeo es dinamico: se escanea la carpeta `Dinamic/Model` y se genera un recurso para cada modelo encontrado.

### URL de Recursos

**Patron general**:
```
/api/3/{recurso}           # Listar todos
/api/3/{recurso}/{id}      # Obtener uno
/api/3/{recurso}           # Crear (POST)
/api/3/{recurso}/{id}      # Actualizar (PUT)
/api/3/{recurso}/{id}      # Eliminar (DELETE)
/api/3/{recurso}/schema    # Obtener esquema
```

### Operacion GET (Listar)

**Solicitud**:
```http
GET /api/3/clientes?offset=0&limit=25&filter[nombre_like]=Acme&sort[]=nombre HTTP/1.1
X-Auth-Token: token_aqui
```

**Parametros de Query**:
- `offset` (int): Desplazamiento para paginacion (default: 0)
- `limit` (int): Cantidad de registros a devolver (default: 50, max recomendado: 500)
- `filter[campo_operador]` (array): Filtros a aplicar
- `operation[campo]` (array): Operador logico para ese filtro ('AND' o 'OR')
- `sort[]` (array): Campos para ordenamiento (puede ser array de objetos con direccion)

**Respuesta exitosa**:
```json
[
  {
    "id": 1,
    "nombre": "Acme Corp",
    "codigo": "CLI001",
    "email": "contacto@acme.com",
    "telefono": "+34 91 123 4567",
    ...
  }
]
```

**Headers de respuesta**:
- `X-Total-Count: 1500` - Total de registros sin paginacion

### Operacion GET (Obtener uno)

**Solicitud**:
```http
GET /api/3/clientes/1 HTTP/1.1
X-Auth-Token: token_aqui
```

**Respuesta**:
```json
{
  "id": 1,
  "nombre": "Acme Corp",
  "codigo": "CLI001",
  "email": "contacto@acme.com",
  "cifnif": "A12345678",
  ...
}
```

Si el registro no existe, devuelve 404.

### Operacion GET (Esquema)

**Solicitud**:
```http
GET /api/3/clientes/schema HTTP/1.1
X-Auth-Token: token_aqui
```

**Respuesta**:
```json
{
  "id": {
    "type": "int",
    "default": null,
    "is_nullable": false
  },
  "nombre": {
    "type": "string",
    "default": "",
    "is_nullable": false
  },
  "codigo": {
    "type": "string",
    "default": "",
    "is_nullable": false
  },
  "email": {
    "type": "string",
    "default": "",
    "is_nullable": true
  },
  "cifnif": {
    "type": "string",
    "default": null,
    "is_nullable": true
  },
  ...
}
```

Util para validacion cliente-side y generacion de formularios dinamicos.

### Operacion POST (Crear)

**Solicitud**:
```http
POST /api/3/clientes HTTP/1.1
X-Auth-Token: token_aqui
Content-Type: application/x-www-form-urlencoded

nombre=Cliente+Nuevo&codigo=CLI999&email=nuevo@ejemplo.com&cifnif=A87654321
```

O con JSON (si se procesa correctamente):
```http
POST /api/3/clientes HTTP/1.1
X-Auth-Token: token_aqui
Content-Type: application/json

{
  "nombre": "Cliente Nuevo",
  "codigo": "CLI999",
  "email": "nuevo@ejemplo.com",
  "cifnif": "A87654321"
}
```

**Comportamiento**:
- Verifica que no exista un registro con el mismo codigo (PK)
- Si existe, devuelve 400 (duplicate-record)
- Asigna valores a las propiedades del modelo
- Si valor es string "null", convierte a null PHP
- Ejecuta validacion del modelo (metodo test())
- Guarda en base de datos

**Respuesta exitosa (201 Created)**:
```json
{
  "ok": "Registro actualizado correctamente",
  "data": {
    "id": 100,
    "nombre": "Cliente Nuevo",
    "codigo": "CLI999",
    "email": "nuevo@ejemplo.com",
    ...
  }
}
```

**Posibles errores**:
- 400: Codigo duplicado
- 400: Sin datos en la solicitud
- 422: Error en validacion o guardado

### Operacion PUT (Actualizar)

**Solicitud**:
```http
PUT /api/3/clientes/100 HTTP/1.1
X-Auth-Token: token_aqui
Content-Type: application/x-www-form-urlencoded

nombre=Cliente+Actualizado&email=nuevo@ejemplo.com
```

O en body:
```http
PUT /api/3/clientes HTTP/1.1
X-Auth-Token: token_aqui
Content-Type: application/x-www-form-urlencoded

id=100&nombre=Cliente+Actualizado&email=nuevo@ejemplo.com
```

**Comportamiento**:
- Busca el registro por ID (de URL o de datos)
- Si no existe, devuelve 404
- Actualiza solo los campos enviados
- Valida y guarda cambios

**Respuesta exitosa (200 OK)**:
```json
{
  "ok": "Registro actualizado correctamente",
  "data": {
    "id": 100,
    "nombre": "Cliente Actualizado",
    "codigo": "CLI999",
    "email": "nuevo@ejemplo.com",
    ...
  }
}
```

**Nota**: PATCH se trata igual que PUT.

### Operacion DELETE (Eliminar)

**Solicitud**:
```http
DELETE /api/3/clientes/100 HTTP/1.1
X-Auth-Token: token_aqui
```

**Comportamiento**:
- Busca el registro por ID
- Si no existe, devuelve 404
- Ejecuta metodo delete() del modelo
- Si hay validaciones o restricciones, puede fallar

**Respuesta exitosa (200 OK)**:
```json
{
  "ok": "Registro eliminado correctamente",
  "data": {
    "id": 100,
    "nombre": "Cliente Eliminado",
    ...
  }
}
```

**Posibles errores**:
- 404: Registro no encontrado
- 422: Error al eliminar (restricciones, etc.)

### Ejemplos Detallados de Filtrado

#### Listar clientes por nombre

```http
GET /api/3/clientes?filter[nombre_like]=Acme HTTP/1.1
X-Auth-Token: token_aqui
```

#### Listar facturas de cierta fecha

```http
GET /api/3/facturasclientes?filter[fecha_gte]=2025-01-01&filter[fecha_lte]=2025-01-31 HTTP/1.1
X-Auth-Token: token_aqui
```

#### Listar productos con precio mayor a 100

```http
GET /api/3/productos?filter[pvp_gt]=100 HTTP/1.1
X-Auth-Token: token_aqui
```

#### Listar con operadores logicos complejos

```http
GET /api/3/clientes?
  filter[nombre_like]=Acme&
  filter[ciudad]=Madrid&
  operation[nombre_like]=OR&
  operation[ciudad]=AND&
  sort[]=nombre&
  limit=50 HTTP/1.1
X-Auth-Token: token_aqui
```

Este ejemplo lista clientes donde (nombre contiene "Acme" O ciudad es Madrid) con ordenamiento por nombre.

#### Listar registros con campos NULL

```http
GET /api/3/clientes?filter[email_null]=1 HTTP/1.1
X-Auth-Token: token_aqui
```

#### Listar registros donde campo NO es NULL

```http
GET /api/3/clientes?filter[email_notnull]=1 HTTP/1.1
X-Auth-Token: token_aqui
```

### Ordenamiento

El parametro `sort` puede ser un array:

```http
GET /api/3/clientes?sort[]=nombre&sort[]=-fecha HTTP/1.1
```

El prefijo `-` indica orden descendente.

---

## Gestion de API Keys

### Crear API Key desde Interfaz

1. Acceder al panel de administracion
2. Ir a Administracion > Configuracion > Configuracion
3. Abrir pestaña "API Keys"
4. Hacer clic en "Nuevo" (icono +)
5. Rellenar campos:
   - **Nombre** (descripcion): Nombre para identificar la clave
   - **Nick**: Identificador corto para el usuario
   - **Descripcion**: Texto descriptivo del proposito
   - **Habilitada**: Checkbox para activar/desactivar
   - **Acceso completo**: Si checked, ignora permisos granulares

6. Guardar
7. Se genera automaticamente un `apikey` unico
8. Copiar y guardar el apikey (no se puede recuperar si se pierde)
9. Si no es acceso completo, asignar permisos por recurso

### Modelo ApiKey

**Ubicacion**: `/Core/Model/ApiKey.php`

**Tabla base de datos**: `api_keys`

**Propiedades principales**:

```php
public $id;              // int - Identificador unico (auto-incremento)
public $apikey;          // string - Token unico para autenticacion (20 caracteres)
public $nick;            // string - Nombre corto del usuario/aplicacion
public $description;     // string - Descripcion del proposito
public $enabled;         // bool - Indica si esta habilitada (default: true)
public $fullaccess;      // bool - Acceso completo sin restricciones (default: false)
public $creationdate;    // string - Fecha de creacion (auto)
```

**Metodos principales**:

```php
public function addAccess(string $resource, bool $state = false): bool
```
Agrega un acceso (permiso) para un recurso especifico.
- Si el recurso ya existe, devuelve true sin cambios
- Crea entrada en `api_access` con los 4 permisos al valor $state
- Retorna true si se crea o ya existe, false si falla

```php
public function getAccesses(): array
```
Devuelve array de todos los permisos asignados a esta API Key.
Retorna array de objetos `ApiAccess`.

```php
public function getAccess(string $resource): ?ApiAccess
```
Obtiene el acceso para un recurso especifico.
Retorna el objeto `ApiAccess` o null si no existe.

```php
public function hasAccess(string $resource, string $permission = 'get'): bool
```
Verifica si tiene permiso para una operacion especifica.
- Si `fullaccess` es true, siempre devuelve true
- $permission: 'get', 'post', 'put' o 'delete'
- Retorna true si tiene el permiso, false en otro caso

**Generacion del apikey**:

```php
public function clear(): void
{
    parent::clear();
    $this->apikey = Tools::randomString(20);  // String aleatorio de 20 caracteres
    $this->creationdate = Tools::date();       // Fecha actual
    $this->enabled = true;
    $this->fullaccess = false;
}
```

Se genera automaticamente cuando se crea una nueva instancia.

### Modelo ApiAccess

**Ubicacion**: `/Core/Model/ApiAccess.php`

**Tabla base de datos**: `api_access`

**Propiedades principales**:

```php
public $id;           // int - Identificador unico
public $idapikey;     // int - Referencia a api_keys.id (FK)
public $resource;     // string - Nombre del recurso ('clientes', 'proveedores', etc.)
public $allowget;     // bool - Permite operacion GET
public $allowpost;    // bool - Permite operacion POST (crear)
public $allowput;     // bool - Permite operacion PUT (actualizar)
public $allowdelete;  // bool - Permite operacion DELETE (eliminar)
```

**Metodos principales**:

```php
public static function addResourcesToApiKey(int $idApiKey, array $resources, 
                                           bool $state = false): bool
```
Agrega multiples recursos a una API Key en una sola operacion.
- $idApiKey: ID de la api_keys a actualizar
- $resources: Array de nombres de recurso ['clientes', 'proveedores', ...]
- $state: Estado inicial de todos los permisos (default: false)
- Salta recursos que ya existen
- Retorna true si todo bien, false si falla alguno

```php
public function setAllowed(bool $get, bool $post, bool $put, bool $delete): bool
```
Actualiza todos los permisos del acceso de una vez.
Guarda cambios en base de datos.
Retorna true si se guarda correctamente.

```php
public function getKey(): ApiKey
```
Carga y devuelve el objeto ApiKey padre.

**Permisos granulares**:

La ventaja del control granular es que permite:
- Una aplicacion externa solo lee datos (GET)
- Otra aplicacion puede crear facturas (POST) pero no eliminar
- Una integracion de e-commerce puede actualizar stock (PUT) pero no ver precios

### Acceso Completo vs Granular

**Acceso Completo** (`fullaccess = true`):
- Proporciona todos los permisos para todos los recursos
- No requiere entradas en `api_access`
- Ideal para aplicaciones internas o partners confiables
- Riesgo mayor de seguridad si se filtra el token

**Acceso Granular** (`fullaccess = false`):
- Requiere entradas explícitas en `api_access`
- Cada recurso tiene 4 permisos independientes
- Mas seguro, aplicaciones externas solo pueden hacer lo necesario
- Requiere mas configuracion inicial

**Flujo de verificacion de permisos**:

```php
// En ApiController::isAllowed()
if ($resource === '' || $this->apiKey->fullaccess) {
    return true;  // Acceso completo o sin recurso especifico
}

// Buscar en api_access
$apiAccess = new ApiAccess();
$where = [Where::eq('idapikey', $this->apiKey->id), 
          Where::eq('resource', $resource)];
if ($apiAccess->loadWhere($where)) {
    // Verificar el permiso especifico segun el metodo HTTP
    switch ($this->request->method()) {
        case 'DELETE':
            return $apiAccess->allowdelete;
        case 'GET':
            return $apiAccess->allowget;
        case 'PUT':
        case 'PATCH':
            return $apiAccess->allowput;
        case 'POST':
            return $apiAccess->allowpost;
    }
}

return false;  // Sin permiso
```

### Ejemplo de Configuracion de API Key

Crear una API Key para integracion de e-commerce que solo puede leer y actualizar productos:

```php
$apiKey = new ApiKey();
$apiKey->nick = 'ecommerce_sync';
$apiKey->description = 'Sincronizacion de productos desde e-commerce';
$apiKey->enabled = true;
$apiKey->fullaccess = false;  // Acceso granular
$apiKey->save();

// Agregar permiso para leer productos (GET)
$apiKey->addAccess('productos', false);
$access = $apiKey->getAccess('productos');
$access->allowget = true;   // Permitir lectura
$access->allowput = true;   // Permitir actualizacion de stock
$access->allowpost = false; // No permitir creacion
$access->allowdelete = false; // No permitir eliminacion
$access->save();
```

---

## Recursos Personalizados

### Concepto

Ademas de los recursos automaticos de modelos, FacturaScripts permite crear recursos API personalizados para operaciones especiales, procesos complejos o endpoints personalizados.

Los recursos personalizados son clases que extienden `APIResourceClass` y pueden procesar solicitudes de manera customizada.

### Estructura de un Recurso Personalizado

**Ubicacion**: `/Dinamic/Lib/API/MiRecursoAPI.php`

Ejemplo basico:

```php
<?php
namespace FacturaScripts\Dinamic\Lib\API;

use FacturaScripts\Core\Lib\API\Base\APIResourceClass;
use FacturaScripts\Core\Response;

class MiRecursoAPI extends APIResourceClass
{
    public function getResources(): array
    {
        return [
            'mi_recurso' => $this->setResource('MiRecurso'),
            'otro_recurso' => $this->setResource('OtroRecurso'),
        ];
    }

    public function doGET(): bool
    {
        // Implementar logica para GET
        $data = [
            'mensaje' => 'GET procesado',
            'params' => $this->params,
        ];
        $this->returnResult($data);
        return true;
    }

    public function doPOST(): bool
    {
        // Implementar logica para POST
        $input = $this->request->request->all();
        $data = [
            'mensaje' => 'POST procesado',
            'datos_recibidos' => $input,
        ];
        $this->setOk('Datos procesados', $data);
        return true;
    }

    public function doPUT(): bool
    {
        // Implementar logica para PUT
        $this->setError('PUT no soportado en este recurso', 
                        null, 
                        Response::HTTP_METHOD_NOT_ALLOWED);
        return false;
    }

    public function doDELETE(): bool
    {
        // Implementar logica para DELETE
        $this->setError('DELETE no soportado en este recurso', 
                        null, 
                        Response::HTTP_METHOD_NOT_ALLOWED);
        return false;
    }
}
```

### Estructura en un Plugin

Para crear el recurso en un plugin:

1. Crear carpeta: `MyPlugin/Lib/API/`
2. Crear archivo: `MyPlugin/Lib/API/MyResourceAPI.php`

El namespace debe ser: `FacturaScripts\Plugins\MyPlugin\Lib\API`

```php
<?php
namespace FacturaScripts\Plugins\MyPlugin\Lib\API;

use FacturaScripts\Core\Lib\API\Base\APIResourceClass;
use FacturaScripts\Core\Response;

class MyResourceAPI extends APIResourceClass
{
    // ... implementacion
}
```

### Registro del Recurso Personalizado

El recurso se registra automaticamente en la clase `ApiRoot` si está en la carpeta correcta.

Tambien puedes registrar recursos manualmente:

```php
// En el bootstrap del plugin
use FacturaScripts\Core\Controller\ApiRoot;

ApiRoot::addCustomResource('mi_recurso_personalizado');
```

### Ejemplo Completo: Recurso de Reporte de Ventas

```php
<?php
namespace FacturaScripts\Dinamic\Lib\API;

use FacturaScripts\Core\Lib\API\Base\APIResourceClass;
use FacturaScripts\Core\Response;
use FacturaScripts\Dinamic\Model\FacturaCliente;
use FacturaScripts\Dinamic\Model\AlbaranCliente;

class VentasReporteAPI extends APIResourceClass
{
    public function getResources(): array
    {
        return [
            'ventasreporte' => $this->setResource('VentasReporte'),
        ];
    }

    public function doGET(): bool
    {
        // params[0] podria ser la fecha inicial
        // params[1] podria ser la fecha final
        
        $fechaIni = $this->params[0] ?? date('Y-m-01');
        $fechaFin = $this->params[1] ?? date('Y-m-d');
        
        $data = $this->generarReporte($fechaIni, $fechaFin);
        $this->returnResult($data);
        return true;
    }

    protected function generarReporte(string $fechaIni, string $fechaFin): array
    {
        // Obtener filtro de tipo (facturas, albaranes, etc.)
        $tipo = $this->request->query->get('tipo', 'facturas');
        $estado = $this->request->query->get('estado', '');

        $totales = [
            'cantidad' => 0,
            'neto' => 0.0,
            'impuestos' => 0.0,
            'total' => 0.0,
            'documentos' => [],
        ];

        if ($tipo === 'facturas') {
            $factura = new FacturaCliente();
            $where = [];
            $where[] = new \FacturaScripts\Core\Base\DataBase\DataBaseWhere(
                'fecha', 
                $fechaIni, 
                '>='
            );
            $where[] = new \FacturaScripts\Core\Base\DataBase\DataBaseWhere(
                'fecha', 
                $fechaFin, 
                '<='
            );
            
            if (!empty($estado)) {
                $where[] = new \FacturaScripts\Core\Base\DataBase\DataBaseWhere(
                    'estado', 
                    $estado, 
                    '='
                );
            }

            foreach ($factura->all($where) as $f) {
                $totales['cantidad']++;
                $totales['neto'] += $f->neto;
                $totales['impuestos'] += $f->total - $f->neto;
                $totales['total'] += $f->total;
                
                $totales['documentos'][] = [
                    'numero' => $f->numero,
                    'fecha' => $f->fecha,
                    'cliente' => $f->nombrecliente,
                    'total' => $f->total,
                ];
            }
        }

        return $totales;
    }

    public function doPOST(): bool
    {
        $this->setError('POST no soportado en este recurso', 
                        null, 
                        Response::HTTP_METHOD_NOT_ALLOWED);
        return false;
    }
}
```

Uso:

```http
GET /api/3/ventasreporte/2025-01-01/2025-01-31?tipo=facturas&estado=Aprobada
X-Auth-Token: token_aqui
```

### Acceso a Modelos y Servicios desde Recursos

Dentro de un recurso personalizado puedes acceder a:

```php
// Modelo
$cliente = new \FacturaScripts\Dinamic\Model\Cliente();

// Base de datos (desde ApiController padre)
$db = $this->db();

// Tools (utilidades)
use FacturaScripts\Core\Tools;
$fecha = Tools::date();

// Otros servicios mediante inyeccion en el constructor si es necesario
```

---

## Ejemplos Practicos de Uso

### Ejemplo 1: Listar Clientes con Filtros

Listar todos los clientes con ciudad "Madrid" y email no vacio, ordenados por nombre:

**cURL**:
```bash
curl -X GET "http://localhost/api/3/clientes?filter[ciudad]=Madrid&filter[email_notnull]=1&sort[]=nombre" \
  -H "X-Auth-Token: mi_api_key" \
  -H "Accept: application/json"
```

**JavaScript/Fetch**:
```javascript
const token = 'mi_api_key';
const response = await fetch(
  'http://localhost/api/3/clientes?filter[ciudad]=Madrid&filter[email_notnull]=1&sort[]=nombre',
  {
    method: 'GET',
    headers: {
      'X-Auth-Token': token,
      'Accept': 'application/json',
    }
  }
);

const clientes = await response.json();
console.log(`Se encontraron ${clientes.length} clientes`);
clientes.forEach(cliente => {
  console.log(`${cliente.nombre} (${cliente.codigo})`);
});
```

**PHP**:
```php
<?php
$token = 'mi_api_key';
$url = 'http://localhost/api/3/clientes?filter[ciudad]=Madrid&filter[email_notnull]=1&sort[]=nombre';

$context = stream_context_create([
    'http' => [
        'method' => 'GET',
        'header' => [
            'X-Auth-Token: ' . $token,
            'Accept: application/json',
        ],
    ],
]);

$response = file_get_contents($url, false, $context);
$clientes = json_decode($response, true);

echo "Se encontraron " . count($clientes) . " clientes\n";
foreach ($clientes as $cliente) {
    echo $cliente['nombre'] . " (" . $cliente['codigo'] . ")\n";
}
?>
```

**Python**:
```python
import requests

token = 'mi_api_key'
url = 'http://localhost/api/3/clientes'
params = {
    'filter[ciudad]': 'Madrid',
    'filter[email_notnull]': '1',
    'sort[]': 'nombre',
}
headers = {'X-Auth-Token': token}

response = requests.get(url, params=params, headers=headers)
clientes = response.json()

print(f"Se encontraron {len(clientes)} clientes")
for cliente in clientes:
    print(f"{cliente['nombre']} ({cliente['codigo']})")
```

### Ejemplo 2: Crear una Factura con Lineas

**cURL**:
```bash
curl -X POST "http://localhost/api/3/crearFacturaCliente" \
  -H "X-Auth-Token: mi_api_key" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "codcliente=CLI001&codalmacen=ALM1&fecha=2025-04-12&lineas=$(cat <<'EOF'
[
  {
    "referencia": "PROD001",
    "cantidad": 2,
    "pvpunitario": 100,
    "dtopor": 10
  },
  {
    "referencia": "PROD002",
    "cantidad": 1,
    "pvpunitario": 250,
    "dtopor": 0
  }
]
EOF
)"
```

Mejor con datos JSON en archivo:

```bash
cat > factura.json << 'EOF'
{
  "codcliente": "CLI001",
  "codalmacen": "ALM1",
  "fecha": "2025-04-12",
  "lineas": [
    {
      "referencia": "PROD001",
      "cantidad": 2,
      "pvpunitario": 100,
      "dtopor": 10
    },
    {
      "referencia": "PROD002",
      "cantidad": 1,
      "pvpunitario": 250,
      "dtopor": 0
    }
  ]
}
EOF

# Convertir JSON a URL-encoded
curl -X POST "http://localhost/api/3/crearFacturaCliente" \
  -H "X-Auth-Token: mi_api_key" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  --data-urlencode "codcliente=CLI001" \
  --data-urlencode "codalmacen=ALM1" \
  --data-urlencode "fecha=2025-04-12" \
  --data-urlencode "lineas=$(cat factura.json | jq -c .)"
```

**JavaScript/Fetch**:
```javascript
const token = 'mi_api_key';

const facturaData = {
  codcliente: 'CLI001',
  codalmacen: 'ALM1',
  fecha: '2025-04-12',
  lineas: JSON.stringify([
    {
      referencia: 'PROD001',
      cantidad: 2,
      pvpunitario: 100,
      dtopor: 10,
    },
    {
      referencia: 'PROD002',
      cantidad: 1,
      pvpunitario: 250,
      dtopor: 0,
    },
  ]),
};

// Convertir a URL-encoded
const formData = new URLSearchParams();
for (const [key, value] of Object.entries(facturaData)) {
  formData.append(key, value);
}

const response = await fetch('http://localhost/api/3/crearFacturaCliente', {
  method: 'POST',
  headers: {
    'X-Auth-Token': token,
    'Content-Type': 'application/x-www-form-urlencoded',
  },
  body: formData.toString(),
});

const resultado = await response.json();
console.log('Factura creada:');
console.log('  Numero:', resultado.doc.numero);
console.log('  Total:', resultado.doc.total);
console.log('  Lineas:', resultado.lines.length);
```

**PHP**:
```php
<?php
$token = 'mi_api_key';
$url = 'http://localhost/api/3/crearFacturaCliente';

$lineas = [
    [
        'referencia' => 'PROD001',
        'cantidad' => 2,
        'pvpunitario' => 100,
        'dtopor' => 10,
    ],
    [
        'referencia' => 'PROD002',
        'cantidad' => 1,
        'pvpunitario' => 250,
        'dtopor' => 0,
    ],
];

$data = [
    'codcliente' => 'CLI001',
    'codalmacen' => 'ALM1',
    'fecha' => '2025-04-12',
    'lineas' => json_encode($lineas),
];

$context = stream_context_create([
    'http' => [
        'method' => 'POST',
        'header' => [
            'X-Auth-Token: ' . $token,
            'Content-Type: application/x-www-form-urlencoded',
        ],
        'content' => http_build_query($data),
    ],
]);

$response = file_get_contents($url, false, $context);
$resultado = json_decode($response, true);

echo "Factura creada:\n";
echo "  Numero: " . $resultado['doc']['numero'] . "\n";
echo "  Total: " . $resultado['doc']['total'] . "\n";
echo "  Lineas: " . count($resultado['lines']) . "\n";
?>
```

**Python**:
```python
import requests
import json

token = 'mi_api_key'
url = 'http://localhost/api/3/crearFacturaCliente'

lineas = [
    {
        'referencia': 'PROD001',
        'cantidad': 2,
        'pvpunitario': 100,
        'dtopor': 10,
    },
    {
        'referencia': 'PROD002',
        'cantidad': 1,
        'pvpunitario': 250,
        'dtopor': 0,
    },
]

data = {
    'codcliente': 'CLI001',
    'codalmacen': 'ALM1',
    'fecha': '2025-04-12',
    'lineas': json.dumps(lineas),
}

headers = {'X-Auth-Token': token}

response = requests.post(url, data=data, headers=headers)
resultado = response.json()

print("Factura creada:")
print(f"  Numero: {resultado['doc']['numero']}")
print(f"  Total: {resultado['doc']['total']}")
print(f"  Lineas: {len(resultado['lines'])}")
```

### Ejemplo 3: Actualizar Stock de Productos

**cURL**:
```bash
curl -X PUT "http://localhost/api/3/productos/PROD001" \
  -H "X-Auth-Token: mi_api_key" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  --data-urlencode "stockalm=500" \
  --data-urlencode "stockmin=50"
```

**JavaScript**:
```javascript
const token = 'mi_api_key';

const stockData = {
  stockalm: 500,
  stockmin: 50,
};

const response = await fetch('http://localhost/api/3/productos/PROD001', {
  method: 'PUT',
  headers: {
    'X-Auth-Token': token,
    'Content-Type': 'application/x-www-form-urlencoded',
  },
  body: new URLSearchParams(stockData).toString(),
});

const resultado = await response.json();
console.log('Stock actualizado para', resultado.data.referencia);
console.log('Stock actual:', resultado.data.stockalm);
```

**PHP**:
```php
<?php
$token = 'mi_api_key';
$url = 'http://localhost/api/3/productos/PROD001';

$data = [
    'stockalm' => 500,
    'stockmin' => 50,
];

$context = stream_context_create([
    'http' => [
        'method' => 'PUT',
        'header' => [
            'X-Auth-Token: ' . $token,
            'Content-Type: application/x-www-form-urlencoded',
        ],
        'content' => http_build_query($data),
    ],
]);

$response = file_get_contents($url, false, $context);
$resultado = json_decode($response, true);

echo "Stock actualizado para " . $resultado['data']['referencia'] . "\n";
echo "Stock actual: " . $resultado['data']['stockalm'] . "\n";
?>
```

### Ejemplo 4: Buscar Productos

**cURL**:
```bash
curl -X GET "http://localhost/api/3/productos?filter[descripcion_like]=%teclado%&filter[precio_gt]=50&limit=10" \
  -H "X-Auth-Token: mi_api_key"
```

**JavaScript**:
```javascript
const token = 'mi_api_key';

const params = new URLSearchParams({
  'filter[descripcion_like]': '%teclado%',
  'filter[precio_gt]': '50',
  'limit': '10',
});

const response = await fetch(`http://localhost/api/3/productos?${params}`, {
  method: 'GET',
  headers: {
    'X-Auth-Token': token,
  },
});

const productos = await response.json();
console.log(`Se encontraron ${productos.length} productos:`);
productos.forEach(p => {
  console.log(`- ${p.descripcion} ($${p.precio})`);
});
```

### Ejemplo 5: Obtener Datos Contables de Facturas

**cURL**:
```bash
curl -X GET "http://localhost/api/3/facturasclientes?filter[fecha_gte]=2025-01-01&filter[estado]=Aprobada&limit=100&offset=0" \
  -H "X-Auth-Token: mi_api_key" | jq '[.[] | {numero, fecha, total, neto, irpf}]'
```

**Python**:
```python
import requests
from datetime import datetime, timedelta

token = 'mi_api_key'
url = 'http://localhost/api/3/facturasclientes'

# Facturas del ultimo mes
fecha_inicio = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
fecha_fin = datetime.now().strftime('%Y-%m-%d')

params = {
    'filter[fecha_gte]': fecha_inicio,
    'filter[fecha_lte]': fecha_fin,
    'filter[estado]': 'Aprobada',
    'limit': 100,
}

headers = {'X-Auth-Token': token}

response = requests.get(url, params=params, headers=headers)
facturas = response.json()

# Calcular totales
total_neto = sum(f['neto'] for f in facturas)
total_impuestos = sum(f['total'] - f['neto'] for f in facturas)
total = sum(f['total'] for f in facturas)

print(f"Periodo: {fecha_inicio} a {fecha_fin}")
print(f"Facturas: {len(facturas)}")
print(f"Total Neto: {total_neto:,.2f}")
print(f"Total Impuestos: {total_impuestos:,.2f}")
print(f"Total: {total:,.2f}")
```

### Ejemplo 6: Autenticacion desde Sistema Externo

Un sistema de terceros que necesita acceder a datos de clientes:

**cURL con autenticacion basica + token API**:
```bash
#!/bin/bash
TOKEN="mi_api_key_produccion"
BASE_URL="https://facturascripts.miempresa.com"

# Obtener cliente
CLIENTE=$(curl -s -X GET "${BASE_URL}/api/3/clientes/CLI001" \
  -H "X-Auth-Token: ${TOKEN}")

echo "Datos del cliente:"
echo "${CLIENTE}" | jq '.| {nombre, email, telefono, direccion}'

# Buscar facturas del cliente
FACTURAS=$(curl -s -X GET "${BASE_URL}/api/3/facturasclientes?filter[codcliente]=CLI001&limit=5" \
  -H "X-Auth-Token: ${TOKEN}")

echo "Ultimas facturas:"
echo "${FACTURAS}" | jq '.[] | {numero, fecha, total}'
```

**Node.js - Integracion en middleware Express**:
```javascript
const express = require('express');
const axios = require('axios');
const app = express();

const FACTURASCRIPTS_API = 'https://facturascripts.miempresa.com/api/3';
const FACTURASCRIPTS_TOKEN = 'mi_api_key_produccion';

const apiClient = axios.create({
  baseURL: FACTURASCRIPTS_API,
  headers: {
    'X-Auth-Token': FACTURASCRIPTS_TOKEN,
    'Accept': 'application/json',
  },
});

// Endpoint que expone datos de cliente desde FacturaScripts
app.get('/api/clientes/:codigo', async (req, res) => {
  try {
    const response = await apiClient.get(`/clientes/${req.params.codigo}`);
    res.json(response.data);
  } catch (error) {
    res.status(error.response?.status || 500).json({
      error: 'Error al obtener cliente',
    });
  }
});

// Endpoint para crear pedido de cliente
app.post('/api/pedidos', async (req, res) => {
  try {
    const response = await apiClient.post('/crearPedidoCliente', req.body);
    res.json(response.data);
  } catch (error) {
    res.status(error.response?.status || 500).json({
      error: error.response?.data?.error || 'Error al crear pedido',
    });
  }
});

app.listen(3000, () => {
  console.log('Servidor escuchando en puerto 3000');
});
```

---

## Uso desde Codigo Externo

### Metodo 1: cURL

cURL es la herramienta mas universal para probar y usar la API.

**Headers basicos**:
```bash
-H "X-Auth-Token: token_aqui"
-H "Content-Type: application/x-www-form-urlencoded"
-H "Accept: application/json"
```

**GET - Listar con paginacion**:
```bash
curl -X GET "http://localhost/api/3/clientes?limit=50&offset=0" \
  -H "X-Auth-Token: token_aqui"
```

**POST - Crear registro**:
```bash
curl -X POST "http://localhost/api/3/clientes" \
  -H "X-Auth-Token: token_aqui" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  --data "nombre=Nuevo Cliente&codigo=CLI999&email=nuevo@ejemplo.com"
```

**PUT - Actualizar registro**:
```bash
curl -X PUT "http://localhost/api/3/clientes/CLI999" \
  -H "X-Auth-Token: token_aqui" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  --data "email=actualizado@ejemplo.com"
```

**DELETE - Eliminar registro**:
```bash
curl -X DELETE "http://localhost/api/3/clientes/CLI999" \
  -H "X-Auth-Token: token_aqui"
```

**Manejo de respuestas con jq**:
```bash
# Listar solo nombres de clientes
curl -s -X GET "http://localhost/api/3/clientes" \
  -H "X-Auth-Token: token_aqui" | jq '.[].nombre'

# Contar registros
curl -s -X GET "http://localhost/api/3/clientes" \
  -H "X-Auth-Token: token_aqui" | jq 'length'

# Filtrar y transformar
curl -s -X GET "http://localhost/api/3/clientes" \
  -H "X-Auth-Token: token_aqui" | jq '.[] | select(.ciudad=="Madrid") | {nombre, email}'
```

### Metodo 2: PHP con file_get_contents

**Clase helper para la API**:
```php
<?php
class FacturaScriptsAPI
{
    private $baseUrl;
    private $token;
    private $lastResponse;

    public function __construct(string $baseUrl, string $token)
    {
        $this->baseUrl = rtrim($baseUrl, '/');
        $this->token = $token;
    }

    public function get(string $resource, array $query = []): array
    {
        $url = $this->baseUrl . '/api/3/' . $resource;
        if (!empty($query)) {
            $url .= '?' . http_build_query($query);
        }
        return $this->request('GET', $url);
    }

    public function post(string $resource, array $data = []): array
    {
        $url = $this->baseUrl . '/api/3/' . $resource;
        return $this->request('POST', $url, $data);
    }

    public function put(string $resource, array $data = []): array
    {
        $url = $this->baseUrl . '/api/3/' . $resource;
        return $this->request('PUT', $url, $data);
    }

    public function delete(string $resource): array
    {
        $url = $this->baseUrl . '/api/3/' . $resource;
        return $this->request('DELETE', $url);
    }

    private function request(string $method, string $url, array $data = []): array
    {
        $options = [
            'http' => [
                'method' => $method,
                'header' => [
                    'X-Auth-Token: ' . $this->token,
                    'Accept: application/json',
                ],
            ],
        ];

        if (!empty($data)) {
            $options['http']['header'][] = 'Content-Type: application/x-www-form-urlencoded';
            $options['http']['content'] = http_build_query($data);
        }

        $context = stream_context_create($options);
        $response = @file_get_contents($url, false, $context);

        if ($response === false) {
            return [
                'error' => 'Error en la solicitud HTTP',
                'http_code' => 500,
            ];
        }

        $httpCode = 200;
        if (!empty($http_response_header)) {
            foreach ($http_response_header as $header) {
                if (preg_match('/HTTP\/\d\.\d\s+(\d+)/', $header, $matches)) {
                    $httpCode = (int)$matches[1];
                }
            }
        }

        return [
            'success' => $httpCode >= 200 && $httpCode < 300,
            'http_code' => $httpCode,
            'data' => json_decode($response, true),
        ];
    }
}

// Uso
$api = new FacturaScriptsAPI('http://localhost', 'mi_api_key');

// Listar clientes
$response = $api->get('clientes', ['limit' => 10]);
if ($response['success']) {
    foreach ($response['data'] as $cliente) {
        echo $cliente['nombre'] . "\n";
    }
}

// Crear cliente
$response = $api->post('clientes', [
    'nombre' => 'Nuevo Cliente',
    'codigo' => 'CLI999',
    'email' => 'nuevo@ejemplo.com',
]);
if ($response['success']) {
    echo "Cliente creado: " . $response['data']['data']['id'] . "\n";
}
?>
```

### Metodo 3: PHP con biblioteca HTTP

Si FacturaScripts tiene una clase HTTP propia:

```php
<?php
use FacturaScripts\Core\Net\HttpClient;

$http = new HttpClient();
$token = 'mi_api_key';
$baseUrl = 'http://localhost';

// GET
$response = $http->get(
    $baseUrl . '/api/3/clientes?limit=10',
    ['X-Auth-Token' => $token]
);

if ($response->getStatusCode() === 200) {
    $clientes = json_decode($response->getBody(), true);
    foreach ($clientes as $cliente) {
        echo $cliente['nombre'] . "\n";
    }
}

// POST
$response = $http->post(
    $baseUrl . '/api/3/clientes',
    [
        'nombre' => 'Nuevo Cliente',
        'codigo' => 'CLI999',
    ],
    ['X-Auth-Token' => $token]
);
?>
```

### Metodo 4: JavaScript/Fetch

**Funcion helper asincrona**:
```javascript
class FacturaScriptsAPI {
  constructor(baseUrl, token) {
    this.baseUrl = baseUrl.replace(/\/$/, '');
    this.token = token;
  }

  async request(method, resource, data = null, query = {}) {
    let url = `${this.baseUrl}/api/3/${resource}`;

    // Agregar query parameters
    if (Object.keys(query).length > 0) {
      const params = new URLSearchParams();
      for (const [key, value] of Object.entries(query)) {
        if (Array.isArray(value)) {
          value.forEach(v => params.append(key, v));
        } else {
          params.append(key, value);
        }
      }
      url += '?' + params.toString();
    }

    const options = {
      method,
      headers: {
        'X-Auth-Token': this.token,
        'Accept': 'application/json',
      },
    };

    if (data) {
      const formData = new URLSearchParams();
      for (const [key, value] of Object.entries(data)) {
        formData.append(key, value);
      }
      options.headers['Content-Type'] = 'application/x-www-form-urlencoded';
      options.body = formData.toString();
    }

    const response = await fetch(url, options);
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || `HTTP ${response.status}`);
    }

    return response.json();
  }

  async get(resource, query = {}) {
    return this.request('GET', resource, null, query);
  }

  async post(resource, data) {
    return this.request('POST', resource, data);
  }

  async put(resource, data) {
    return this.request('PUT', resource, data);
  }

  async delete(resource) {
    return this.request('DELETE', resource);
  }
}

// Uso
const api = new FacturaScriptsAPI('http://localhost', 'mi_api_key');

// Listar clientes
const clientes = await api.get('clientes', { limit: 10 });
clientes.forEach(cliente => {
  console.log(cliente.nombre);
});

// Crear cliente
const nuevoCliente = await api.post('clientes', {
  nombre: 'Nuevo Cliente',
  codigo: 'CLI999',
  email: 'nuevo@ejemplo.com',
});
console.log('ID:', nuevoCliente.data.id);
```

**Con manejo de errores**:
```javascript
async function listarClientesSeguro() {
  try {
    const clientes = await api.get('clientes', { 
      limit: 25,
      offset: 0,
    });
    console.log(`Se obtuvieron ${clientes.length} clientes`);
    return clientes;
  } catch (error) {
    console.error('Error al listar clientes:', error.message);
    // Mostrar mensaje al usuario
    alert('No se pudo conectar con la API');
    return [];
  }
}
```

### Metodo 5: Python con requests

**Clase wrapper completa**:
```python
import requests
from typing import Any, Dict, List, Optional

class FacturaScriptsAPI:
    def __init__(self, base_url: str, token: str):
        self.base_url = base_url.rstrip('/')
        self.token = token
        self.session = requests.Session()
        self.session.headers.update({
            'X-Auth-Token': self.token,
            'Accept': 'application/json',
        })

    def get(self, resource: str, query: Optional[Dict] = None) -> Any:
        """GET request"""
        url = f"{self.base_url}/api/3/{resource}"
        response = self.session.get(url, params=query)
        response.raise_for_status()
        return response.json()

    def post(self, resource: str, data: Dict) -> Any:
        """POST request"""
        url = f"{self.base_url}/api/3/{resource}"
        response = self.session.post(url, data=data)
        response.raise_for_status()
        return response.json()

    def put(self, resource: str, data: Dict) -> Any:
        """PUT request"""
        url = f"{self.base_url}/api/3/{resource}"
        response = self.session.put(url, data=data)
        response.raise_for_status()
        return response.json()

    def delete(self, resource: str) -> Any:
        """DELETE request"""
        url = f"{self.base_url}/api/3/{resource}"
        response = self.session.delete(url)
        response.raise_for_status()
        return response.json()

# Uso
api = FacturaScriptsAPI('http://localhost', 'mi_api_key')

# Listar clientes
clientes = api.get('clientes', {'limit': 10})
for cliente in clientes:
    print(f"{cliente['nombre']} - {cliente['email']}")

# Crear cliente
nuevo = api.post('clientes', {
    'nombre': 'Nuevo Cliente',
    'codigo': 'CLI999',
    'email': 'nuevo@ejemplo.com',
})
print(f"Cliente creado con ID: {nuevo['data']['id']}")

# Actualizar
actualizado = api.put('clientes/CLI999', {
    'email': 'actualizado@ejemplo.com',
})

# Eliminar
api.delete('clientes/CLI999')
```

**Con retry y reintentos**:
```python
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

def crear_sesion_con_reintentos():
    session = requests.Session()
    retry = Retry(
        total=3,
        backoff_factor=0.5,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

api.session = crear_sesion_con_reintentos()
```

### Metodo 6: JavaScript - Axios

```javascript
const axios = require('axios');

const apiClient = axios.create({
  baseURL: 'http://localhost/api/3',
  headers: {
    'X-Auth-Token': 'mi_api_key',
    'Accept': 'application/json',
  },
});

// Interceptor para manejo de errores
apiClient.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      console.error('Token invalido o expirado');
    } else if (error.response?.status === 403) {
      console.error('Permisos insuficientes');
    } else if (error.response?.status === 429) {
      console.error('Demasiadas solicitudes, IP bloqueada');
    }
    return Promise.reject(error);
  }
);

// Uso
async function obtenerClientes() {
  try {
    const response = await apiClient.get('/clientes', {
      params: {
        limit: 25,
        offset: 0,
      },
    });
    return response.data;
  } catch (error) {
    console.error('Error:', error.message);
  }
}

async function crearCliente(datosCliente) {
  try {
    const response = await apiClient.post('/clientes', datosCliente);
    return response.data;
  } catch (error) {
    console.error('Error al crear cliente:', error.response?.data?.error);
  }
}
```

---

## Como Crear un MCP Server para FacturaScripts

### Concepto de MCP (Model Context Protocol)

MCP (Model Context Protocol) es un protocolo de comunicacion que permite que aplicaciones externas (como Claude o otros clientes inteligentes) interactúen con sistemas a traves de herramientas bien definidas.

Un MCP Server para FacturaScripts exponeria la funcionalidad de la API como herramientas que pueden ser llamadas por Claude u otros clientes.

### Ventajas de un MCP Server

1. **Integracion Natural**: Claude puede interactuar con FacturaScripts sin necesidad de scripts externos
2. **Context Aware**: Claude entiende los parametros y respuestas del servidor
3. **Reutilizable**: Una sola definicion del servidor puede usarse en multiples clientes
4. **Type Safe**: Los parametros y respuestas estan fuertemente tipados
5. **Error Handling**: Manejo robusto de errores y reintentos

### Estructura Basica de un MCP Server para FacturaScripts

**Ubicacion**: `/mnt/mcp-servers/facturascripts/`

```
facturascripts/
├── package.json
├── tsconfig.json
├── src/
│   ├── index.ts
│   ├── api-client.ts
│   └── tools/
│       ├── clientes.ts
│       ├── productos.ts
│       ├── facturas.ts
│       └── documentos.ts
└── README.md
```

### Herramientas Basicas Recomendadas

#### 1. Listar Facturas

```typescript
{
  name: "listar_facturas",
  description: "Lista facturas con filtros opcionales (fecha, estado, cliente)",
  inputSchema: {
    type: "object",
    properties: {
      fecha_inicio: {
        type: "string",
        description: "Fecha inicio (YYYY-MM-DD)"
      },
      fecha_fin: {
        type: "string",
        description: "Fecha fin (YYYY-MM-DD)"
      },
      estado: {
        type: "string",
        enum: ["Borrador", "Aprobada", "Anulada"],
        description: "Estado de la factura"
      },
      codcliente: {
        type: "string",
        description: "Codigo del cliente"
      },
      limit: {
        type: "integer",
        default: 50,
        description: "Numero de registros a devolver"
      }
    }
  }
}
```

#### 2. Crear Factura

```typescript
{
  name: "crear_factura",
  description: "Crea una nueva factura de cliente con lineas",
  inputSchema: {
    type: "object",
    required: ["codcliente", "lineas"],
    properties: {
      codcliente: {
        type: "string",
        description: "Codigo del cliente"
      },
      codalmacen: {
        type: "string",
        description: "Codigo del almacen (default: ALM1)"
      },
      fecha: {
        type: "string",
        description: "Fecha de factura (YYYY-MM-DD)"
      },
      lineas: {
        type: "array",
        items: {
          type: "object",
          required: ["referencia", "cantidad"],
          properties: {
            referencia: {
              type: "string",
              description: "Codigo del producto"
            },
            cantidad: {
              type: "number",
              description: "Cantidad a facturar"
            },
            pvpunitario: {
              type: "number",
              description: "Precio unitario"
            },
            dtopor: {
              type: "number",
              description: "Descuento porcentaje"
            }
          }
        }
      }
    }
  }
}
```

#### 3. Consultar Stock Producto

```typescript
{
  name: "consultar_stock_producto",
  description: "Obtiene informacion de stock de un producto",
  inputSchema: {
    type: "object",
    required: ["referencia"],
    properties: {
      referencia: {
        type: "string",
        description: "Codigo/referencia del producto"
      },
      almacen: {
        type: "string",
        description: "Codigo del almacen (opcional)"
      }
    }
  }
}
```

#### 4. Buscar Clientes

```typescript
{
  name: "buscar_clientes",
  description: "Busca clientes por nombre, email o ciudad",
  inputSchema: {
    type: "object",
    properties: {
      nombre: {
        type: "string",
        description: "Nombre del cliente (busqueda parcial)"
      },
      email: {
        type: "string",
        description: "Email del cliente"
      },
      ciudad: {
        type: "string",
        description: "Ciudad del cliente"
      },
      limit: {
        type: "integer",
        default: 25,
        description: "Numero de resultados"
      }
    }
  }
}
```

#### 5. Obtener Resumen Contable

```typescript
{
  name: "resumen_contable",
  description: "Genera resumen contable de un periodo",
  inputSchema: {
    type: "object",
    required: ["fecha_inicio", "fecha_fin"],
    properties: {
      fecha_inicio: {
        type: "string",
        description: "Fecha inicio periodo (YYYY-MM-DD)"
      },
      fecha_fin: {
        type: "string",
        description: "Fecha fin periodo (YYYY-MM-DD)"
      },
      estado: {
        type: "string",
        enum: ["Todos", "Aprobadas", "Pendientes"],
        description: "Filtro por estado"
      }
    }
  }
}
```

### Implementacion Basica en TypeScript

**api-client.ts**:
```typescript
import fetch from 'node-fetch';

interface ApiConfig {
  baseUrl: string;
  token: string;
}

export class FacturaScriptsClient {
  private config: ApiConfig;

  constructor(baseUrl: string, token: string) {
    this.config = {
      baseUrl: baseUrl.replace(/\/$/, ''),
      token,
    };
  }

  async request(
    method: 'GET' | 'POST' | 'PUT' | 'DELETE',
    resource: string,
    data?: Record<string, any>,
    query?: Record<string, any>
  ) {
    let url = `${this.config.baseUrl}/api/3/${resource}`;

    if (query && method === 'GET') {
      const params = new URLSearchParams();
      for (const [key, value] of Object.entries(query)) {
        if (Array.isArray(value)) {
          value.forEach(v => params.append(key, v));
        } else {
          params.append(key, value);
        }
      }
      url += '?' + params.toString();
    }

    const headers: Record<string, string> = {
      'X-Auth-Token': this.config.token,
      'Accept': 'application/json',
    };

    let body: string | undefined = undefined;
    if (data && method !== 'GET') {
      headers['Content-Type'] = 'application/x-www-form-urlencoded';
      body = new URLSearchParams(data).toString();
    }

    const response = await fetch(url, {
      method,
      headers,
      body,
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || `HTTP ${response.status}`);
    }

    return response.json();
  }

  async listFacturas(filtros: {
    fechaInicio?: string;
    fechaFin?: string;
    estado?: string;
    codcliente?: string;
    limit?: number;
  }) {
    const query: Record<string, any> = {
      limit: filtros.limit || 50,
    };

    if (filtros.fechaInicio) {
      query['filter[fecha_gte]'] = filtros.fechaInicio;
    }
    if (filtros.fechaFin) {
      query['filter[fecha_lte]'] = filtros.fechaFin;
    }
    if (filtros.estado) {
      query['filter[estado]'] = filtros.estado;
    }
    if (filtros.codcliente) {
      query['filter[codcliente]'] = filtros.codcliente;
    }

    return this.request('GET', 'facturasclientes', undefined, query);
  }

  async crearFactura(datos: {
    codcliente: string;
    codalmacen?: string;
    fecha?: string;
    lineas: Array<{
      referencia: string;
      cantidad: number;
      pvpunitario?: number;
      dtopor?: number;
    }>;
  }) {
    const postData: Record<string, any> = {
      codcliente: datos.codcliente,
      lineas: JSON.stringify(datos.lineas),
    };

    if (datos.codalmacen) {
      postData.codalmacen = datos.codalmacen;
    }
    if (datos.fecha) {
      postData.fecha = datos.fecha;
    }

    return this.request('POST', 'crearFacturaCliente', postData);
  }

  async consultarStockProducto(referencia: string) {
    return this.request('GET', `productos/${referencia}`);
  }

  async buscarClientes(filtros: {
    nombre?: string;
    email?: string;
    ciudad?: string;
    limit?: number;
  }) {
    const query: Record<string, any> = {
      limit: filtros.limit || 25,
    };

    if (filtros.nombre) {
      query['filter[nombre_like]'] = `%${filtros.nombre}%`;
    }
    if (filtros.email) {
      query['filter[email_like]'] = `%${filtros.email}%`;
    }
    if (filtros.ciudad) {
      query['filter[ciudad]'] = filtros.ciudad;
    }

    return this.request('GET', 'clientes', undefined, query);
  }

  async resumenContable(filtros: {
    fechaInicio: string;
    fechaFin: string;
    estado?: string;
  }) {
    const query: Record<string, any> = {
      'filter[fecha_gte]': filtros.fechaInicio,
      'filter[fecha_lte]': filtros.fechaFin,
      'filter[estado]': filtros.estado || 'Aprobada',
    };

    const facturas = await this.request(
      'GET',
      'facturasclientes',
      undefined,
      query
    );

    // Calcular resumen
    const resumen = {
      periodo: {
        inicio: filtros.fechaInicio,
        fin: filtros.fechaFin,
      },
      cantidad_facturas: facturas.length,
      total_neto: 0,
      total_impuestos: 0,
      total_general: 0,
      facturas: [],
    };

    for (const factura of facturas) {
      resumen.total_neto += factura.neto || 0;
      resumen.total_impuestos += (factura.total - factura.neto) || 0;
      resumen.total_general += factura.total || 0;
      resumen.facturas.push({
        numero: factura.numero,
        fecha: factura.fecha,
        cliente: factura.nombrecliente,
        total: factura.total,
      });
    }

    return resumen;
  }
}
```

**index.ts** (servidor MCP basico):
```typescript
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  Tool,
} from '@modelcontextprotocol/sdk/types.js';
import { FacturaScriptsClient } from './api-client.js';

const FS_BASE_URL = process.env.FACTURASCRIPTS_URL || 'http://localhost';
const FS_TOKEN = process.env.FACTURASCRIPTS_TOKEN || '';

const client = new FacturaScriptsClient(FS_BASE_URL, FS_TOKEN);

const tools: Tool[] = [
  {
    name: 'listar_facturas',
    description: 'Lista facturas con filtros opcionales',
    inputSchema: {
      type: 'object' as const,
      properties: {
        fecha_inicio: {
          type: 'string',
          description: 'Fecha inicio (YYYY-MM-DD)',
        },
        fecha_fin: {
          type: 'string',
          description: 'Fecha fin (YYYY-MM-DD)',
        },
        estado: {
          type: 'string',
          enum: ['Borrador', 'Aprobada', 'Anulada'],
        },
        codcliente: {
          type: 'string',
          description: 'Codigo del cliente',
        },
        limit: {
          type: 'integer',
          default: 50,
        },
      },
    },
  },
  {
    name: 'buscar_clientes',
    description: 'Busca clientes por nombre, email o ciudad',
    inputSchema: {
      type: 'object' as const,
      properties: {
        nombre: {
          type: 'string',
        },
        email: {
          type: 'string',
        },
        ciudad: {
          type: 'string',
        },
        limit: {
          type: 'integer',
          default: 25,
        },
      },
    },
  },
  {
    name: 'consultar_stock_producto',
    description: 'Obtiene informacion de stock de un producto',
    inputSchema: {
      type: 'object' as const,
      required: ['referencia'],
      properties: {
        referencia: {
          type: 'string',
          description: 'Codigo/referencia del producto',
        },
      },
    },
  },
  {
    name: 'crear_factura',
    description: 'Crea una nueva factura de cliente con lineas',
    inputSchema: {
      type: 'object' as const,
      required: ['codcliente', 'lineas'],
      properties: {
        codcliente: {
          type: 'string',
        },
        codalmacen: {
          type: 'string',
        },
        fecha: {
          type: 'string',
          description: 'YYYY-MM-DD',
        },
        lineas: {
          type: 'array',
          items: {
            type: 'object',
            required: ['referencia', 'cantidad'],
            properties: {
              referencia: {
                type: 'string',
              },
              cantidad: {
                type: 'number',
              },
              pvpunitario: {
                type: 'number',
              },
              dtopor: {
                type: 'number',
              },
            },
          },
        },
      },
    },
  },
  {
    name: 'resumen_contable',
    description: 'Genera resumen contable de un periodo',
    inputSchema: {
      type: 'object' as const,
      required: ['fecha_inicio', 'fecha_fin'],
      properties: {
        fecha_inicio: {
          type: 'string',
          description: 'YYYY-MM-DD',
        },
        fecha_fin: {
          type: 'string',
          description: 'YYYY-MM-DD',
        },
        estado: {
          type: 'string',
          enum: ['Todos', 'Aprobadas', 'Pendientes'],
        },
      },
    },
  },
];

const server = new Server(
  {
    name: 'facturascripts-mcp',
    version: '1.0.0',
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools,
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    let result;

    switch (name) {
      case 'listar_facturas':
        result = await client.listFacturas({
          fechaInicio: args.fecha_inicio,
          fechaFin: args.fecha_fin,
          estado: args.estado,
          codcliente: args.codcliente,
          limit: args.limit,
        });
        break;

      case 'buscar_clientes':
        result = await client.buscarClientes({
          nombre: args.nombre,
          email: args.email,
          ciudad: args.ciudad,
          limit: args.limit,
        });
        break;

      case 'consultar_stock_producto':
        result = await client.consultarStockProducto(args.referencia);
        break;

      case 'crear_factura':
        result = await client.crearFactura({
          codcliente: args.codcliente,
          codalmacen: args.codalmacen,
          fecha: args.fecha,
          lineas: args.lineas,
        });
        break;

      case 'resumen_contable':
        result = await client.resumenContable({
          fechaInicio: args.fecha_inicio,
          fechaFin: args.fecha_fin,
          estado: args.estado,
        });
        break;

      default:
        return {
          content: [
            {
              type: 'text',
              text: `Herramienta desconocida: ${name}`,
            },
          ],
          isError: true,
        };
    }

    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify(result, null, 2),
        },
      ],
    };
  } catch (error) {
    return {
      content: [
        {
          type: 'text',
          text: `Error: ${error instanceof Error ? error.message : String(error)}`,
        },
      ],
      isError: true,
    };
  }
});

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error('FacturaScripts MCP server running on stdio');
}

main().catch(console.error);
```

### Configuracion e Instalacion

**package.json**:
```json
{
  "name": "mcp-facturascripts",
  "version": "1.0.0",
  "description": "MCP Server para FacturaScripts",
  "main": "build/index.js",
  "scripts": {
    "build": "tsc",
    "start": "node build/index.js",
    "dev": "ts-node src/index.ts"
  },
  "dependencies": {
    "@modelcontextprotocol/sdk": "^0.5.0",
    "node-fetch": "^3.0.0"
  },
  "devDependencies": {
    "@types/node": "^20.0.0",
    "typescript": "^5.0.0",
    "ts-node": "^10.0.0"
  }
}
```

**Variables de entorno**:
```bash
export FACTURASCRIPTS_URL=http://localhost
export FACTURASCRIPTS_TOKEN=tu_api_token_aqui
```

### Ventajas y Casos de Uso

**Casos de uso ideales para MCP Server**:

1. **Automatizacion de procesos**: Claude puede crear facturas, gestionar pedidos
2. **Consultas e informes**: Generar reportes contables, listar clientes
3. **Integracion con flujos de trabajo**: Conectar FacturaScripts con otros sistemas
4. **Asistencia inteligente**: Responder preguntas sobre datos de negocio
5. **Validacion de datos**: Verificar existencia de clientes, productos antes de procesos

**Ejemplo de uso en conversacion con Claude**:

> Usuario: "Necesito un resumen de ventas del mes de abril"
> 
> Claude usa herramienta: `resumen_contable` con fecha_inicio=2025-04-01, fecha_fin=2025-04-30
> 
> Claude responde: "En abril se realizaron 45 facturas por un total de 125,450.75 euros..."

---

## Notas Finales y Mejores Practicas

### Seguridad

1. **Nunca expongas tokens API en codigo fuente**
   - Usar variables de entorno
   - Guardar en archivos .env (excluidos de git)
   - Usar gestores de secretos en produccion

2. **Rota tokens periodicamente**
   - Cambiar API Keys cada 90 dias
   - Crear nuevas claves antes de eliminar las viejas
   - Monitorear uso sospechoso (IP_LIST en cache)

3. **Limita permisos al minimo necesario**
   - No usar fullaccess a menos que sea absolutamente necesario
   - Crear una API Key por aplicacion/integracion
   - Especificar permisos por recurso y operacion

4. **HTTPS en produccion**
   - Siempre usar HTTPS en URL de la API
   - Validar certificados SSL

### Optimizacion

1. **Paginacion**
   - Siempre usar limit razonable (25-50)
   - Usar offset para navegar resultados
   - No pedir X-Total-Count si no lo necesitas

2. **Cacheo cliente-side**
   - Cachear datos que no cambian frecuentemente (listados maestros)
   - Invalidar cache cuando sea apropiado
   - Usar ETags si se implementan

3. **Batch operations**
   - Si necesitas varias operaciones, usa transacciones donde sea posible
   - Agrupa POST/PUT cuando sea factible

### Mantenibilidad

1. **Versionamiento**
   - La API es v3, cualquier cambio futuro sera v4
   - Tus clientes/integraciones deben especificar version

2. **Documentacion**
   - Documentar endpoints personalizados
   - Mantener ejemplos actualizados
   - Registrar cambios de API

3. **Testing**
   - Probar solicitudes antes de automatizar
   - Validar respuestas esperadas
   - Manejar errores gracefully

---

Fin de la Referencia Completa de la API REST de FacturaScripts 2025
