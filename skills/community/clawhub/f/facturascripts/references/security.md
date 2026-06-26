# Sistema de Seguridad de FacturaScripts 2025 - Referencia Exhaustiva

## Indice de contenidos

1. [Modelo User - Usuarios y Autenticacion](#1-modelo-user---usuarios-y-autenticacion)
2. [Sistema de Roles - Control de Permisos](#2-sistema-de-roles---control-de-permisos)
3. [Permisos por Pagina - RoleAccess](#3-permisos-por-pagina---roleaccess)
4. [Sesion y Autenticacion - Login](#4-sesion-y-autenticacion---login)
5. [Proteccion CSRF - MultiRequestProtection](#5-proteccion-csrf---multirequestprotection)
6. [Seguridad de API](#6-seguridad-de-api)
7. [Validacion de Datos](#7-validacion-de-datos)
8. [Manejo de Errores de Seguridad](#8-manejo-de-errores-de-seguridad)
9. [Como Implementar Seguridad en un Plugin](#9-como-implementar-seguridad-en-un-plugin)

---

## 1. Modelo User - Usuarios y Autenticacion

El modelo `User` se encuentra en `/Core/Model/User.php` y es la clase central para gestionar usuarios en FacturaScripts.

### Propiedades principales del User

```php
public $admin;                          // Boolean - Indica si es administrador
public $codagente;                      // String - Codigo del agente asociado
public $codalmacen;                     // String - Codigo del almacen por defecto
public $codserie;                       // String - Codigo de serie por defecto
public $creationdate;                   // String - Fecha de creacion del usuario
public $email;                          // String - Email del usuario
public $enabled;                        // Boolean - Estado activo/inactivo del usuario
public $homepage;                       // String - Pagina de inicio del usuario
public $langcode;                       // String - Codigo de idioma (ej: 'es_ES')
public $lastactivity;                   // String - Fecha/hora de ultima actividad
public $lastbrowser;                    // String - Navegador utilizado en ultima actividad
public $lastip;                         // String - Ultima direccion IP utilizada
public $level;                          // Integer - Nivel de usuario (0-99, admin=99)
public $logkey;                         // String - Clave de sesion aleatoria de 99 caracteres
public $nick;                           // String - Nombre de usuario (clave primaria)
public $newPassword;                    // String - Nueva contrasena (no persistida)
public $newPassword2;                   // String - Confirmacion de nueva contrasena (no persistida)
public $password;                       // String - Hash de la contrasena con PASSWORD_DEFAULT
public $two_factor_enabled;             // Boolean - Autenticacion de dos factores activada
public $two_factor_secret_key;          // String - Clave secreta TOTP del usuario
```

### Constantes del User

- `DEFAULT_LEVEL = 2` - Nivel por defecto para nuevos usuarios no administradores
- `UPDATE_ACTIVITY_PERIOD = 3600` - Periodo en segundos para actualizar actividad del usuario (1 hora)

### Metodos principales de autenticacion y seguridad

#### `public function setPassword($value): bool`

Establece una nueva contrasena con validacion de seguridad.

**Validaciones realizadas:**
- Longitud minima: 8 caracteres
- Debe contener al menos un numero: `/[0-9]/`
- Debe contener al menos una letra: `/[a-zA-Z]/`

**Proceso:**
1. Si valida, hashea la contrasena usando `password_hash($value, PASSWORD_DEFAULT)`
2. Genera un nuevo logkey por seguridad
3. Retorna true si es exitoso, false si falla validacion

**Ejemplo:**
```php
$user = new User();
$user->load('admin');
if ($user->setPassword('NewSecure123')) {
    $user->save();
}
```

#### `public function verifyPassword(string $value): bool`

Verifica si la contrasena proporcionada coincide con el hash almacenado.

**Proceso:**
1. Utiliza `password_verify($value, $this->password)` para comparacion segura
2. Si verifica correctamente y el hash necesita rehashing (algoritmo antiguo):
   - Automaticamente rehashea la contrasena con `setPassword($value)`
   - Esto asegura que los passwords se actualizen a algoritmos mas nuevos
3. Retorna true si la contrasena es correcta

#### `public function newLogkey(string $ipAddress, string $browser = ''): string`

Genera una nueva clave de sesion aleatoria para el usuario.

**Proceso:**
1. Llama `updateActivity($ipAddress, $browser)` para registrar actividad
2. Genera logkey con `Tools::randomString(99)` - cadena aleatoria de 99 caracteres
3. Retorna la clave generada

**Uso tipico:**
```php
$user->newLogkey(Session::getClientIp(), $request->userAgent());
$user->save();
```

#### `public function updateActivity(string $ipAddress, string $browser = ''): void`

Actualiza los registros de actividad del usuario.

**Campos actualizados:**
- `lastactivity` - Establecido con `Tools::dateTime()` (timestamp actual)
- `lastip` - Direccion IP desde la que se conecta
- `lastbrowser` - Identificador del navegador (maximo 200 caracteres tras sanitizar)

#### `public function verifyLogkey(string $value): bool`

Verifica si la clave de sesion proporcionada coincide con la almacenada.

**Implementacion:**
```php
return $this->logkey === $value;
```

### Autenticacion de dos factores (2FA)

#### `public function enableTwoFactor(string $key = ''): string`

Activa la autenticacion de dos factores TOTP (Time-based One-Time Password).

**Parametros:**
- `$key` (opcional) - Clave secreta personalizada. Si esta vacia, se genera una nueva

**Retorna:**
- String con la clave secreta (codigo QR)

**Proceso:**
1. Si ya esta habilitado, retorna la clave existente
2. Establece `two_factor_enabled = true`
3. Genera o usa la clave secreta (se guarda en `two_factor_secret_key`)
4. Retorna la clave para mostrar como codigo QR

#### `public function disableTwoFactor(): void`

Desactiva la autenticacion de dos factores.

**Proceso:**
```php
$this->two_factor_enabled = false;
$this->two_factor_secret_key = null;
```

#### `public function verifyTwoFactorCode(string $code): bool`

Verifica un codigo TOTP de 6 digitos.

**Proceso:**
1. Comprueba que `two_factor_enabled == true` y que existe `two_factor_secret_key`
2. Valida el codigo con `TwoFactorManager::verifyCode()`
3. El codigo puede tener cierta tolerancia temporal (normalmente +/- 30 segundos)

#### `public function getTwoFactorUrl(): string`

Retorna la URL para generar el codigo QR (formato OTPAuth).

**Formato:**
```
otpauth://totp/CompanyName:email@example.com?secret=XXXXX&issuer=FacturaScripts
```

#### `public function getTwoFactorQR(): string`

Retorna la imagen del codigo QR en formato HTML si 2FA esta habilitado.

### Validacion del Usuario (test())

El metodo `test()` realiza validaciones extensivas antes de guardar:

**Validacion del nick:**
- Patron: `/^[A-Z0-9_@\+\.\-]{3,50}$/i`
- Rango: 3 a 50 caracteres
- Permite: letras, numeros, @, +, ., -

**Validacion del email:**
- Si no esta vacio, valida con `FILTER_VALIDATE_EMAIL`
- Se convierte a minusculas
- Se sanitiza HTML

**Campos actualizados automaticamente:**
- Si creationdate esta vacio, se establece a fecha actual
- Si admin=true, level se establece a 99
- Si admin=false y level es null, se establece a 0

**Validaciones adicionales:**
- Valida que el agente exista (si se proporciona codagente)
- Valida que el almacen exista (si se proporciona codalmacen)

### Gestion de Roles

#### `public function addRole(?string $code): bool`

Anade un rol al usuario.

**Validaciones:**
1. Comprueba que el codigo no este vacio
2. Verifica que el usuario no tenga ya ese rol
3. Verifica que el rol exista en la base de datos
4. Si el usuario no tiene homepage, asigna una desde los accesos del rol

**Retorna:** true si se anadio correctamente, false en caso contrario

#### `public function removeRole(?string $code): bool`

Elimina un rol del usuario.

**Validaciones:**
1. Comprueba que el codigo no este vacio
2. Verifica que el usuario tenga ese rol

#### `public function getRoles(): array`

Retorna array de objetos `Role` asignados al usuario.

**Implementacion:**
```php
$where = [new DataBaseWhere('nick', $this->nick)];
return DinRoleUser::all($where, [], 0, 0) as $role
```

### Control de Acceso

#### `public function can(string $pageName, string $permission = 'access'): bool`

Verifica si el usuario tiene acceso a una pagina y permisos especificos.

**Logica:**
1. Si `enabled = false`, retorna false (usuario deshabilitado no puede acceder)
2. Si `admin = true`:
   - Verifica que la pagina exista
   - Retorna true a menos que el permiso sea 'only-owner-data' (admin no tiene restriccion de owner)
3. Si no es admin:
   - Busca en `RoleAccess::allFromUser()` los roles del usuario en esa pagina
   - Para cada acceso, verifica si el permiso solicitado es permitido con `$access->can($permission)`

**Permisos validos:**
- `'access'` - Acceso basico a la pagina
- `'delete'` - Permiso para eliminar
- `'update'` - Permiso para modificar
- `'export'` - Permiso para exportar
- `'import'` - Permiso para importar
- `'only-owner-data'` - Solo datos del propietario

### Deleccion de Usuarios

#### `public function delete(): bool`

Previene la deleccion del ultimo usuario del sistema.

**Validacion:**
```php
if ($this->count() === 1) {
    Tools::log()->error('cant-delete-last-user');
    return false;
}
```

---

## 2. Sistema de Roles - Control de Permisos

El sistema de roles en FacturaScripts se compone de tres modelos: `Role`, `RoleUser` y `RoleAccess`.

### Modelo Role

Ubicacion: `/Core/Model/Role.php`

**Propiedades:**

```php
public $codrole;        // String - Codigo del rol (clave primaria, 1-20 caracteres)
public $descripcion;    // String - Descripcion del rol
```

**Validaciones en el rol:**
- El codigo debe cumplir patron `/^[A-Z0-9_\+\.\-]{1,20}$/i`
- Se sanitiza HTML en la descripcion
- Si no existe codigo, se genera automaticamente con `newCode()`

#### `public function addPage(string $page_name): bool`

Anade una pagina al rol con todos los permisos por defecto.

**Proceso:**
1. Crea un objeto `RoleAccess`
2. Asigna codrole y pagename
3. Guarda el acceso

#### `public function removePage(string $page_name): bool`

Elimina una pagina del rol.

**Validaciones:**
- Busca el acceso existente
- Si no existe, registra warning y retorna false

#### `public function addUser(string $nick): bool`

Anade un usuario al rol.

**Proceso:**
1. Crea un objeto `RoleUser`
2. Asigna codrole y nick
3. Guarda la relacion

#### `public function removeUser(string $nick): bool`

Elimina un usuario del rol.

#### `public function getAccesses(): array`

Retorna array de `RoleAccess` ordenados por pagename.

#### `public function getUsers(): array`

Retorna array de `RoleUser` ordenados por nick.

### Modelo RoleUser

Ubicacion: `/Core/Model/RoleUser.php`

**Propiedades:**

```php
public $id;             // Integer - Clave primaria (autoincrementable)
public $codrole;        // String - Codigo del rol
public $nick;           // String - Nombre del usuario
```

**Tabla:** `roles_users`

#### `public function getRole(): Role`

Retorna el objeto `Role` asociado.

#### `public function getUser(): User`

Retorna el objeto `User` asociado.

#### `public function getRoleAccess(string $page_name = ''): array`

Retorna los accesos de este rol, opcionalmente filtrados por pagina.

### Modelo RoleAccess

Ubicacion: `/Core/Model/RoleAccess.php`

Define los permisos especificos de cada pagina dentro de un rol.

**Propiedades:**

```php
public $id;                 // Integer - Clave primaria (autoincrementable)
public $codrole;            // String - Codigo del rol
public $pagename;           // String - Nombre de la pagina
public $allowdelete;        // Boolean - Permiso para eliminar (defecto: true)
public $allowexport;        // Boolean - Permiso para exportar (defecto: true)
public $allowimport;        // Boolean - Permiso para importar (defecto: true)
public $allowupdate;        // Boolean - Permiso para actualizar (defecto: true)
public $onlyownerdata;      // Boolean - Restriccion solo datos del propietario (defecto: false)
```

**Tabla:** `roles_access`

#### `public function can(string $permission): bool`

Verifica si el permiso esta habilitado en este acceso.

**Permisos y mapeo:**

```php
'access'          -> siempre true (si existe acceso a la pagina)
'delete'          -> $this->allowdelete
'export'          -> $this->allowexport
'import'          -> $this->allowimport
'update'          -> $this->allowupdate
'only-owner-data' -> $this->onlyownerdata
```

#### `public static function allFromUser(string $nick, string $page_name): array`

Metodo estatico que retorna todos los accesos de un usuario a una pagina especifica.

**Implementacion:**
```php
$sql_in = 'SELECT codrole FROM roles_users WHERE nick = ?';
$where = [
    Where::in('codrole', $sql_in),
    Where::eq('pagename', $page_name)
];
return static::all($where, [], 0, 0);
```

**Nota:** Este metodo es la base del control de permisos en `User::can()`

#### `public static function addPagesToRole(string $codrole, array $pages): bool`

Anade multiples paginas a un rol de una sola vez.

**Parametros:**
- `$codrole` - Codigo del rol
- `$pages` - Array de objetos Page a anadirse al rol

**Proceso:**
- Por cada pagina, si el acceso no existe, lo crea
- Si la pagina ya tiene acceso en el rol, la salta
- Todos los permisos se activan por defecto

---

## 3. Permisos por Pagina - RoleAccess

### Modelo Page

Ubicacion: `/Core/Model/Page.php`

**Propiedades:**

```php
public $name;           // String - Nombre unico de la pagina (clave primaria)
public $title;          // String - Titulo de la pagina
public $menu;           // String - Opcion de menu principal
public $submenu;        // String - Opcion de submenu
public $icon;           // String - Icono Font Awesome
public $ordernum;       // Integer - Orden en el menu (defecto: 100)
public $showonmenu;     // Boolean - Mostrar en menu (defecto: true)
```

**Tabla:** `pages`

### Flujo de verificacion de permisos

1. **Usuario intenta acceder a una pagina**

2. **En el controlador:**
   ```php
   if (!$this->user->can('EditInvoice', 'access')) {
       throw new AccessDeniedException();
   }
   ```

3. **En User::can()**
   - Verifica si usuario esta habilitado
   - Si es admin y la pagina existe, retorna true (salvo 'only-owner-data')
   - Si no es admin, obtiene `RoleAccess::allFromUser($nick, $pageName)`
   - Para cada acceso, verifica `$access->can($permission)`

4. **Resultado:**
   - Si al menos uno de los roles tiene el permiso, retorna true
   - Si ninguno tiene el permiso, retorna false

### Tipos de permisos y su significado

#### Access
El permiso basico para ver la pagina. Si un usuario tiene un acceso a una pagina en cualquier rol, puede verla.

#### Delete
Permite eliminar registros en la pagina.
- Controlado por: `allowdelete` en RoleAccess
- Normalmente validado en controladores: `$this->user->can('PageName', 'delete')`

#### Update
Permite modificar registros existentes.
- Controlado por: `allowupdate` en RoleAccess
- Normalmente validado en controladores: `$this->user->can('PageName', 'update')`

#### Export
Permite exportar datos desde la pagina (CSV, PDF, Excel, etc.).
- Controlado por: `allowexport` en RoleAccess

#### Import
Permite importar datos en la pagina.
- Controlado por: `allowimport` en RoleAccess

#### Only-Owner-Data
Restringe el acceso solo a datos del propietario del usuario (campo owner).
- Controlado por: `onlyownerdata` en RoleAccess
- Nunca es true para usuarios admin
- Normalmente validado como: `$this->user->can('PageName', 'only-owner-data')`
- Requiere logica adicional en el controlador para filtrar datos

### Ejemplo de implementacion de permisos en un plugin

```php
// En el controlador del plugin
public function privateAccess()
{
    // Verificar acceso a la pagina
    if (!$this->user->can('MyCustomPage', 'access')) {
        throw new AccessDeniedException('No tienes acceso a esta pagina');
    }
    
    // Verificar permiso para actualizar
    if (!$this->user->can('MyCustomPage', 'update')) {
        $this->permissions->update = false;
    }
    
    // Verificar permiso para eliminar
    if (!$this->user->can('MyCustomPage', 'delete')) {
        $this->permissions->delete = false;
    }
    
    // Filtrar datos si solo puede ver datos del propietario
    if ($this->user->can('MyCustomPage', 'only-owner-data')) {
        $where[] = Where::eq('owner', $this->user->nick);
    }
}
```

---

## 4. Sesion y Autenticacion - Login

### Clase Session

Ubicacion: `/Core/Session.php`

**Proposito:** Proporciona acceso al contexto de sesion del usuario autenticado.

#### Propiedades estaticas privadas

```php
private static $data = [];  // Array que almacena datos de sesion en memoria
```

#### Metodos principales

##### `public static function user(): User`

Retorna el usuario autenticado actualmente.

**Logica:**
1. Verifica si existe un usuario en `self::$data['user']` que sea instancia de `User`
2. Si existe, lo retorna
3. Si no existe:
   - Intenta cargar la clase dinamica `\FacturaScripts\Dinamic\Model\User`
   - Si existe, retorna instancia de esa clase
   - Si no existe, retorna instancia de `\FacturaScripts\Core\Model\User`

**Uso tipico:**
```php
$user = Session::user();
$canAccess = $user->can('ListInvoices');
```

##### `public static function set(string $key, $value): void`

Establece un valor en la sesion.

```php
Session::set('user', $userObject);
Session::set('controllerName', 'EditInvoice');
```

##### `public static function get(string $key)`

Obtiene un valor de la sesion.

```php
$user = Session::get('user');
$controller = Session::get('controllerName');
```

##### `public static function clear(): void`

Limpia todos los datos de sesion.

##### `public static function getClientIp(): string`

Obtiene la direccion IP del cliente, considerando proxies.

**Orden de busqueda:**
1. `HTTP_CF_CONNECTING_IP` - IP real desde Cloudflare
2. `HTTP_X_FORWARDED_FOR` - IP desde proxy X-Forwarded-For
3. `REMOTE_ADDR` - IP directa de la conexion
4. Defecto: `'::1'` (localhost IPv6)

##### `public static function permissions(): ControllerPermissions`

Retorna los permisos del usuario en el controlador actual.

### Clase Login

Ubicacion: `/Core/Controller/Login.php`

**Proposito:** Manejar login, logout, cambio de contrasena y validacion de 2FA.

#### Constantes de seguridad

```php
const INCIDENT_EXPIRATION_TIME = 600;  // Tiempo de expiracion de incidente (10 min)
const IP_LIST = 'login-ip-list';       // Clave para cache de IPs
const MAX_INCIDENT_COUNT = 6;          // Cantidad de intentos fallidos permitidos
const USER_LIST = 'login-user-list';   // Clave para cache de usuarios
```

#### Acciones de Login

##### `protected function loginAction(Request $request): void`

Realiza el proceso de autenticacion.

**Validaciones:**

1. **Token CSRF:** Valida el token multirequest con `validateFormToken()`
   - Si no es valido, se rechaza la peticion
   - Si el token fue usado antes (duplicado), se rechaza

2. **Campos obligatorios:**
   - `fsNick` - Nombre de usuario
   - `fsPassword` - Contrasena

3. **Bloqueo por intentos fallidos:**
   - Verifica si la IP o usuario tiene muchos incidentes
   - Si supera `MAX_INCIDENT_COUNT`, rechaza con log 'ip-banned'

4. **Validacion del usuario:**
   - Carga el usuario desde la BD
   - Verifica que sea enabled
   - Verifica la contrasena con `User::verifyPassword()`

5. **Autenticacion de dos factores:**
   - Si `two_factor_enabled = true`:
     - Cambia el template a 'Login/TwoFactor.html.twig'
     - Guarda el nick del usuario para la siguiente accion
     - NO redirige, permite que el usuario ingrese el codigo TOTP

6. **Redireccion:**
   - Si todo es correcto y sin 2FA:
     - Llama `updateUserAndRedirect()`
     - Redirige a la `homepage` del usuario

**Registros de incidentes:**
- Se registra en cache cuando:
  - Usuario no existe
  - Contrasena incorrecta
  - Muchos intentos desde una IP

##### `protected function twoFactorValidationAction(Request $request): void`

Valida el codigo TOTP de dos factores.

**Proceso:**

1. Carga el usuario por el nick proporcionado
2. Valida el codigo TOTP con `User::verifyTwoFactorCode()`
3. Si es invalido:
   - Registra incidente
   - Retorna sin redirigir
4. Si es valido:
   - Llama `updateUserAndRedirect()`

##### `protected function changePasswordAction(Request $request): void`

Permite cambiar la contrasena del usuario (requiere acceso a BD).

**Validaciones:**

1. **Token CSRF:** Valida formToken
2. **Bloqueo por intentos:** Verifica incidentes
3. **Contrasena de BD:** Requiere coincidencia exacta con `Tools::config('db_pass')`
4. **Campos obligatorios:**
   - `fsNewUserPasswd` - Nombre de usuario
   - `fsNewPasswd` - Nueva contrasena
   - `fsNewPasswd2` - Confirmacion
5. **Validacion de contrasena:** Las dos deben coincidir
6. **Fortaleza de contrasena:** Se valida en `User::setPassword()`

**Desactivacion de 2FA:**
- Si el usuario tiene 2FA activado, se desactiva automaticamente
- Se guarda en la BD

##### `protected function logoutAction(Request $request): void`

Cierra la sesion del usuario.

**Proceso:**

1. Valida token CSRF
2. Elimina cookies:
   - `fsNick`
   - `fsLogkey`
   - `fsLang`
3. Reinicia la semilla del MultiRequestProtection (limpia cache)
4. Registra log de logout exitoso

#### Metodo de validacion de token

##### `protected function validateFormToken(Request $request): bool`

Valida el token CSRF (MultiRequestProtection).

**Proceso:**

1. Crea instancia de `MultiRequestProtection`
2. Si hay cookie `fsNick` autenticada:
   - Anade el nick como semilla adicional
   - Esto hace que los tokens sean unicos por usuario
3. Obtiene el token de `multireqtoken` (GET o POST)
4. Valida el token con `multiRequestProtection->validate()`
   - Comprueba que sea de formato correcto (SHA1|random)
   - Comprueba que la parte SHA1 sea de la hora actual o hace hasta 4 horas
5. Verifica que no haya sido usado antes con `tokenExist()`
   - Si fue usado, se rechaza como duplicado
6. Si todo es correcto, retorna true

**Retorna:**
- true si el token es valido
- false en cualquier caso de error (invalido, duplicado, expirado)

#### Gestion de incidentes

##### `public function saveIncident(string $ip, string $user = '', ?int $time = null): void`

Registra un intento fallido de login.

**Proceso:**

1. Anade la IP a `IP_LIST` en cache
2. Si se proporciona usuario, tambien lo anade a `USER_LIST`
3. Asocia cada incidente con timestamp actual o proporcionado

##### `public function userHasManyIncidents(string $ip, string $username = ''): bool`

Verifica si hay muchos incidentes para una IP o usuario.

**Logica:**

1. Cuenta incidentes para la IP
2. Si >= `MAX_INCIDENT_COUNT` (6), retorna true
3. Si se proporciona usuario, cuenta incidentes para ese usuario
4. Si >= `MAX_INCIDENT_COUNT`, retorna true
5. Si no hay muchos incidentes, retorna false

##### `protected function getIpList(): array` y `protected function getUserList(): array`

Obtienen la lista de incidentes del cache, filtrando por tiempo de expiracion.

**Proceso:**
- Obtiene lista del cache
- Elimina entradas mas antiguas de `INCIDENT_EXPIRATION_TIME` (600 segundos = 10 minutos)
- Retorna lista actualizada

#### Metodo de redireccion

##### `protected function updateUserAndRedirect(User $user, string $ip, Request $request): void`

Actualiza datos del usuario y redirige a su pagina de inicio.

**Proceso:**

1. **Actualiza sesion:**
   - `Session::set('user', $user)`

2. **Actualiza actividad del usuario:**
   - Obtiene user agent del navegador
   - Llama `$user->newLogkey($ip, $browser)`
   - Esto genera una nueva clave de sesion

3. **Guarda cambios en BD:**
   - Llama `$user->save()`

4. **Guarda cookies:**
   - Llama `saveCookies($user, $request)`

5. **Redirige:**
   - Si no hay homepage, usa raiz del sitio
   - Realiza HTTP redirect a la URL

#### Manejo de cookies

##### `protected function saveCookies(User $user, Request $request): void`

Establece las cookies de sesion del usuario.

**Cookies establecidas:**

```php
fsNick      // Nombre del usuario
fsLogkey    // Clave de sesion (99 caracteres aleatorios)
fsLang      // Codigo de idioma del usuario
```

**Configuracion de las cookies:**

```php
$expiration = time() + (int)Tools::config('cookies_expire', 31536000);
// Por defecto, expira en 1 ano (31536000 segundos)

$secure = $request->isSecure();
// Solo HTTPS si la conexion es segura

setcookie($name, $value, $expiration, $path, '', $secure, true);
// HttpOnly=true (no accesible por JavaScript)
```

---

## 5. Proteccion CSRF - MultiRequestProtection

Ubicacion: `/Core/Lib/MultiRequestProtection.php`

### Proposito

Prevenir ataques CSRF (Cross-Site Request Forgery) y peticiones duplicadas mediante tokens unicos.

### Constantes

```php
const CACHE_KEY = 'MultiRequestProtection';    // Clave del cache
const MAX_TOKEN_AGE = 4;                       // Edad maxima del token en horas
const MAX_TOKENS = 500;                        // Maximo de tokens en cache
const RANDOM_STRING_LENGTH = 6;                // Longitud del numero aleatorio
```

### Propiedades

```php
protected static $seed;  // Semilla unica por instalacion + usuario
```

### Metodo de inicializacion

#### `public function __construct()`

Inicializa la semilla del MultiRequestProtection en la primera instancia.

**Semilla:**
```php
$seed = PHP_VERSION . __FILE__ . Tools::config('db_name') . Tools::config('db_pass');
```

Esta semilla es unica porque:
- Depende de la version de PHP
- Depende de la ruta de instalacion
- Depende del nombre de la BD
- Depende de la contrasena de la BD

### Metodos de configuracion

#### `public function clearSeed(): void`

Reinicia la semilla a su valor base.

#### `public function addSeed(string $seed): void`

Anade informacion adicional a la semilla.

**Uso tipico:**
- En el login, se anade el nick del usuario
- Esto hace que los tokens sean unicos por usuario

### Generacion de tokens

#### `public function newToken(): string`

Genera un nuevo token CSRF.

**Formato del token:**
```
SHA1_HASH | RANDOM_NUMBER

Ejemplo: a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0 | 3a2b1c
```

**Proceso:**

1. Obtiene numero variable en el tiempo:
   ```php
   $num = intval(date('YmdH')) + strlen($seed);
   // Cambia cada hora (YmdH = Ano-Mes-Dia-Hora)
   ```

2. Combina semilla + numero:
   ```php
   $value = $seed . $num;
   ```

3. Genera SHA1 del valor:
   ```php
   $hash = sha1($value);
   ```

4. Anade numero aleatorio:
   ```php
   $random = $this->getRandomStr();  // 6 caracteres aleatorios
   ```

5. Retorna:
   ```php
   return $hash . '|' . $random;
   ```

### Validacion de tokens

#### `public function validate(string $token): bool`

Valida la estructura y antigüedad del token.

**Validaciones:**

1. **Formato:**
   - Debe contener exactamente 1 pipe (|)
   - Retorna false si no

2. **Parte SHA1:**
   - Genera los 5 SHA1 validos (hora actual + 4 horas atras)
   - Verifica que la parte SHA1 del token coincida con uno valido
   - Esto significa que el token no puede ser mas viejo de 4 horas

**Ejemplo de tokens validos en un momento dado:**
```
Token generado hace 0 horas -> SHA1(seed + num_ahora)
Token generado hace 1 hora  -> SHA1(seed + num_hace1h)
Token generado hace 2 horas -> SHA1(seed + num_hace2h)
Token generado hace 3 horas -> SHA1(seed + num_hace3h)
Token generado hace 4 horas -> SHA1(seed + num_hace4h)

Mas viejo de 4 horas -> SHA1 no valido -> rechazado
```

**Retorna:**
- true si el token es valido
- false si es invalido, expirado o mal formado

#### `public function tokenExist(string $token): bool`

Verifica si el token ya fue usado (prevencion de duplicados).

**Proceso:**

1. Obtiene lista de tokens usados del cache
2. Verifica si el token actual esta en la lista
3. Si esta en la lista (fue usado), retorna true
4. Si no esta en la lista (es nuevo), lo anade y retorna false

**Logica:**
- Retorna true si el token es duplicado (ya fue usado)
- Retorna false si es nuevo (primera vez que se ve)

Esta es la logica inversa a la expectativa comun, por lo que en el codigo se valida:
```php
if ($multiRequestProtection->tokenExist($token)) {
    Tools::log()->warning('duplicated-request');
    return false;  // rechazar porque es duplicado
}
```

### Manejo de cache

#### `protected function getTokens(): array`

Obtiene los tokens almacenados en cache.

**Proceso:**

1. Obtiene tokens del cache con clave `CACHE_KEY`
2. Si no existen, retorna array vacio
3. Si hay mas de `MAX_TOKENS` (500), mantiene solo los ultimos 10
   ```php
   return array_slice($tokens, -10);
   ```

#### `protected function saveToken(string $token): bool`

Guarda un nuevo token en el cache.

**Proceso:**

1. Obtiene tokens actuales (con limpieza de overflow)
2. Anade el nuevo token al array
3. Guarda en cache

### Numero aleatorio

#### `protected function getRandomStr(): string`

Genera una cadena aleatoria de 6 caracteres.

**Caracteres permitidos:**
```
0-9, a-z, A-Z
```

**Proceso:**
```php
$chars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
return substr(str_shuffle($chars), 0, 6);
```

### Uso del MultiRequestProtection en formularios

En los templates (Twig), se incluye asi:

```twig
<form method="POST" action="">
    <input type="hidden" name="multireqtoken" value="{{ object.multiRequestProtection.newToken() }}">
    <!-- resto del formulario -->
</form>
```

El controlador valida:
```php
if (!$this->multiRequestProtection->validate($request->input('multireqtoken'))) {
    throw new InvalidRequest();
}
```

---

## 6. Seguridad de API

### Modelo ApiKey

Ubicacion: `/Core/Model/ApiKey.php`

**Proposito:** Gestionar claves API para acceso a recursos REST.

#### Propiedades

```php
public $id;              // Integer - Clave primaria (autoincrementable)
public $apikey;          // String - Clave API unica generada aleatoriamente (20 caracteres)
public $nick;            // String - Usuario propietario de la clave
public $description;     // String - Descripcion de la clave
public $creationdate;    // String - Fecha de creacion
public $enabled;         // Boolean - Estado de la clave (activo/inactivo)
public $fullaccess;      // Boolean - Acceso total a todos los recursos
```

**Tabla:** `api_keys`

#### Inicializacion

##### `public function clear(): void`

Establece valores por defecto.

```php
$this->apikey = Tools::randomString(20);          // Clave aleatoria de 20 caracteres
$this->creationdate = Tools::date();              // Fecha actual
$this->enabled = true;                            // Habilitada por defecto
$this->fullaccess = false;                        // Sin acceso total por defecto
```

#### Gestion de accesos

##### `public function addAccess(string $resource, bool $state = false): bool`

Anade acceso a un recurso.

**Parametros:**

- `$resource` - Nombre del recurso (ej: 'invoices', 'customers')
- `$state` - Permisos iniciales (aplica a todos los metodos)

**Logica:**

1. Si el recurso ya existe, retorna true (no duplica)
2. Crea objeto `ApiAccess`
3. Establece todos los permisos con el valor `$state`:
   - `allowget = $state`
   - `allowpost = $state`
   - `allowput = $state`
   - `allowdelete = $state`
4. Guarda el acceso

##### `public function getAccesses(): array`

Retorna todos los accesos de esta clave API.

##### `public function getAccess(string $resource): ?ApiAccess`

Obtiene el acceso para un recurso especifico.

**Retorna:**
- Objeto `ApiAccess` si existe
- null si no existe

##### `public function hasAccess(string $resource, string $permission = 'get'): bool`

Verifica si la clave tiene permiso para una accion en un recurso.

**Logica:**

1. Si `fullaccess = true`, retorna true automaticamente
2. Si no, obtiene el acceso al recurso
3. Si el recurso no existe, retorna false
4. Verifica el permiso especifico:
   - 'delete' -> `$access->allowdelete`
   - 'get' -> `$access->allowget`
   - 'post' -> `$access->allowpost`
   - 'put' -> `$access->allowput`

### Modelo ApiAccess

Ubicacion: `/Core/Model/ApiAccess.php`

**Proposito:** Definir permisos especificos de HTTP para cada recurso.

#### Propiedades

```php
public $id;             // Integer - Clave primaria (autoincrementable)
public $idapikey;       // Integer - ID de la clave API
public $resource;       // String - Nombre del recurso
public $allowget;       // Boolean - Permite GET (lectura)
public $allowpost;      // Boolean - Permite POST (creacion)
public $allowput;       // Boolean - Permite PUT (actualizacion)
public $allowdelete;    // Boolean - Permite DELETE (eliminacion)
```

**Tabla:** `api_access`

#### Inicializacion

##### `public function clear(): void`

Establece todos los permisos activos por defecto.

```php
$this->allowdelete = true;
$this->allowget = true;
$this->allowpost = true;
$this->allowput = true;
```

#### Gestion de permisos

##### `public function setAllowed(bool $get, bool $post, bool $put, bool $delete): bool`

Actualiza todos los permisos de una sola vez.

**Parametros:**
- `$get` - Permitir GET
- `$post` - Permitir POST
- `$put` - Permitir PUT
- `$delete` - Permitir DELETE

**Proceso:**
```php
$this->allowget = $get;
$this->allowpost = $post;
$this->allowput = $put;
$this->allowdelete = $delete;
return $this->save();
```

#### Batch operations

##### `public static function addResourcesToApiKey(int $idApiKey, array $resources, bool $state = false): bool`

Anade multiples recursos a una clave API.

**Parametros:**

- `$idApiKey` - ID de la clave API
- `$resources` - Array de nombres de recursos
- `$state` - Permisos iniciales (false = denegado, true = permitido)

**Proceso:**

1. Para cada recurso en el array:
   - Verifica que no exista ya (para no duplicar)
   - Crea objeto `ApiAccess`
   - Establece todos los permisos con `$state`
   - Guarda

2. Si alguno falla, retorna false

### Validacion de ApiKey

#### `public function test(): bool`

Valida la clave API.

- Sanitiza HTML en: `apikey`, `description`, `nick`
- Llamará a validaciones padres

### Flujo de autenticacion API

**Tipico en ApiController:**

```php
// 1. Obtener apikey del header o query parameter
$apiKey = $request->header('X-API-KEY') ?? $request->input('apikey');

// 2. Cargar la clave API
$apiKeyObj = new ApiKey();
if (!$apiKeyObj->loadBy('apikey', $apiKey)) {
    return $this->response->setStatusCode(401, 'Unauthorized');
}

// 3. Verificar que este habilitada
if (!$apiKeyObj->enabled) {
    return $this->response->setStatusCode(403, 'Forbidden');
}

// 4. Verificar permiso para el recurso y metodo
$method = strtolower($request->method());  // 'get', 'post', 'put', 'delete'
if (!$apiKeyObj->hasAccess('invoices', $method)) {
    return $this->response->setStatusCode(403, 'Forbidden');
}

// 5. Procesar la peticion
```

---

## 7. Validacion de Datos

Ubicacion: `/Core/Validator.php`

### Proposito

Proporcionar metodos estaticos para validacion de datos de entrada.

### Metodos de validacion

#### `public static function alphaNumeric(string $text, string $extra = '', int $min = 1, int $max = 99): bool`

Valida que el texto contenga solo numeros, letras y caracteres permitidos adicionales.

**Parametros:**

- `$text` - Texto a validar
- `$extra` - Caracteres adicionales permitidos (ej: '-_.@')
- `$min` - Longitud minima
- `$max` - Longitud maxima

**Proceso:**

1. Los caracteres especiales en `$extra` se escapan para la regex
2. Crea patron: `/^[a-zA-Z0-9{extra}]{min,max}$/`
3. Valida el patron

**Ejemplo:**
```php
Validator::alphaNumeric('user-123', '-', 3, 20);  // true
Validator::alphaNumeric('user@name', '@', 1, 20); // true
Validator::alphaNumeric('user@name!', '@', 1, 20); // false (! no esta permitido)
```

#### `public static function email(string $email): bool`

Valida que sea un email valido.

**Implementacion:**
```php
return filter_var($email, FILTER_VALIDATE_EMAIL) !== false;
```

#### `public static function string(string $text, int $min = 1, int $max = 99): bool`

Valida que la longitud este entre min y max caracteres.

```php
return strlen($text) >= $min && strlen($text) <= $max;
```

#### `public static function url(string $url, bool $strict = false): bool`

Valida que sea una URL valida.

**Validaciones:**

1. Si esta vacia -> false
2. Si comienza por 'javascript:' -> false
3. Si `$strict = false` y comienza por 'www.' -> anade 'https://'
4. Valida con `FILTER_VALIDATE_URL`

**Ejemplo:**
```php
Validator::url('https://example.com');      // true
Validator::url('www.example.com', false);   // true (anade https://)
Validator::url('javascript:alert()');       // false
```

#### `public static function date(string $date): bool`

Valida que sea una fecha valida en formato estricto.

**Formatos aceptados:**

- `d-m-Y` (ej: "31-12-2023")
- `Y-m-d` (ej: "2023-12-31")

**Validaciones:**

1. No puede estar vacia
2. Intenta parsear con cada formato
3. Si parsea, verifica que el formato parsea identico
4. Valida que sea fecha calendario valida con `checkdate()`

#### `public static function datetime(string $datetime): bool`

Valida que sea fecha y hora en formato estricto.

**Formatos aceptados:**

- `d-m-Y H:i:s` (ej: "31-12-2023 23:59:59")
- `d-m-Y H:i` (ej: "31-12-2023 23:59")
- `Y-m-d H:i:s` (ej: "2023-12-31 23:59:59")
- `Y-m-d H:i` (ej: "2023-12-31 23:59")
- Con separador ISO 8601 (T en lugar de espacio)

**Proceso:**

1. Separa fecha y hora por espacio o T
2. Valida fecha con `date()`
3. Valida hora con `hour()`

#### `public static function hour(string $time): bool`

Valida que sea una hora valida.

**Formatos aceptados:**

- `H:i:s` (ej: "23:59:59")
- `H:i` (ej: "23:59")

**Validaciones:**

1. Patron regex: `/^([01]?\d|2[0-3]):([0-5]?\d)(?::([0-5]?\d))?$/`
   - Hora: 0-23
   - Minutos: 0-59
   - Segundos: 0-59 (opcional)

### Uso del Validator en la aplicacion

**En validacion de entrada:**

```php
// Validar nick de usuario
if (!Validator::alphaNumeric($nick, '-_.@', 3, 50)) {
    Tools::log()->error('invalid-username');
    return false;
}

// Validar email
if ($email && !Validator::email($email)) {
    Tools::log()->error('invalid-email');
    return false;
}

// Validar fecha
if (!Validator::date($dateStr)) {
    Tools::log()->error('invalid-date');
    return false;
}
```

### Sanitizacion de HTML

Nota: Aunque el Validator no sanitiza, FacturaScripts utiliza `Tools::noHtml()` para esto:

```php
$this->email = Tools::noHtml(mb_strtolower($email ?? '', 'UTF8'));
```

---

## 8. Manejo de Errores de Seguridad

### Excepciones de seguridad

En los controladores se lanzan excepciones cuando se deniega acceso:

```php
use FacturaScripts\Core\Exception\AccessDeniedException;

if (!$this->user->can('EditInvoice', 'update')) {
    throw new AccessDeniedException('No tienes permisos para editar facturas');
}
```

### Logging de eventos de seguridad

Se utiliza `Tools::log()` para registrar eventos:

```php
// Login exitoso
Tools::log()->notice('login-user-ok', ['%nick%' => $user->nick]);

// Intento fallido
Tools::log()->warning('login-password-fail');

// Acceso denegado
Tools::log()->error('access-denied', ['%page%' => $pageName]);

// Token invalido
Tools::log()->warning('invalid-request');

// Token duplicado
Tools::log()->warning('duplicated-request');

// Contrasena debil
Tools::log()->warning('weak-password', ['%userNick%' => $nick]);

// Usuario deshabilitado
Tools::log()->warning('login-user-disabled');
```

### Respuesta a errores de seguridad

**Tipicamente se responde con:**

1. Log del evento
2. Mensaje generico al usuario (sin detallar por que se rechazo)
3. Sin redireccion o redireccion a login

**Ejemplo:**
```php
if (!$user->can('DeleteInvoice', 'delete')) {
    Tools::log()->warning('delete-denied', ['%user%' => $user->nick, '%id%' => $id]);
    // No informar al usuario cual es el motivo especifico
    throw new AccessDeniedException('No tienes permiso para esta accion');
}
```

---

## 9. Como Implementar Seguridad en un Plugin

### Estructura basica de un controlador seguro

```php
<?php
namespace FacturaScripts\Plugins\MyPlugin\Controller;

use FacturaScripts\Core\Base\Controller;
use FacturaScripts\Core\Exception\AccessDeniedException;
use FacturaScripts\Core\Tools;

class MyPageController extends Controller
{
    // 1. VERIFICAR ACCESO EN CONSTRUCTOR O INIT
    public function __construct(string $className, string $uri = '')
    {
        parent::__construct($className, $uri);
        
        // Verificar que el usuario este autenticado
        if (!$this->user) {
            throw new AccessDeniedException();
        }
        
        // Verificar que tenga acceso a esta pagina
        if (!$this->user->can($this->className, 'access')) {
            throw new AccessDeniedException();
        }
    }
    
    // 2. VERIFICAR PERMISOS ESPECIFICOS POR ACCION
    public function privateAccess()
    {
        // Verificar acceso general
        if (!$this->user->can('MyPage', 'access')) {
            throw new AccessDeniedException();
        }
        
        // Para actualizar
        if (!$this->user->can('MyPage', 'update')) {
            $this->permissions->update = false;
            Tools::log()->warning('update-denied', ['%user%' => $this->user->nick]);
        }
        
        // Para eliminar
        if (!$this->user->can('MyPage', 'delete')) {
            $this->permissions->delete = false;
            Tools::log()->warning('delete-denied', ['%user%' => $this->user->nick]);
        }
        
        // Para datos del propietario
        if ($this->user->can('MyPage', 'only-owner-data')) {
            $where[] = Where::eq('owner', $this->user->nick);
        }
    }
    
    // 3. VALIDAR TOKEN CSRF EN POST
    protected function saveAction()
    {
        // Validar token CSRF
        if (!$this->multiRequestProtection->validate($this->request->input('multireqtoken'))) {
            Tools::log()->warning('invalid-request');
            return;
        }
        
        // Verificar que no sea duplicado
        if ($this->multiRequestProtection->tokenExist($token)) {
            Tools::log()->warning('duplicated-request');
            return;
        }
        
        // Verificar permiso
        if (!$this->user->can('MyPage', 'update')) {
            throw new AccessDeniedException();
        }
        
        // Guardar cambios...
    }
    
    // 4. VALIDAR ENTRADAS CON VALIDATOR
    protected function validateInput(string $field, string $value)
    {
        use FacturaScripts\Core\Validator;
        
        switch ($field) {
            case 'username':
                return Validator::alphaNumeric($value, '-_.@', 3, 50);
            case 'email':
                return Validator::email($value);
            case 'date':
                return Validator::date($value);
            default:
                return false;
        }
    }
    
    // 5. REGISTRAR ACCIONES IMPORTANTES
    protected function deleteAction()
    {
        if (!$this->user->can('MyPage', 'delete')) {
            Tools::log()->warning('delete-denied', ['%user%' => $this->user->nick]);
            return;
        }
        
        $id = $this->request->input('id');
        $model = new MyModel();
        if ($model->load($id) && $model->delete()) {
            Tools::log()->notice('record-deleted', [
                '%user%' => $this->user->nick,
                '%id%' => $id,
                '%model%' => $this->className
            ]);
        }
    }
    
    // 6. SANITIZAR SALIDA HTML
    public function getTemplateData()
    {
        return [
            'username' => Tools::noHtml($this->user->nick),
            'email' => Tools::noHtml($this->user->email),
            // todos los datos del usuario se sanitizan antes de mostrar
        ];
    }
}
```

### Template Twig seguro

```twig
<!-- 1. Token CSRF en formularios -->
<form method="POST" action="">
    <input type="hidden" name="multireqtoken" value="{{ object.multiRequestProtection.newToken() }}">
    
    <!-- 2. Mostrar campos solo si el usuario tiene permisos -->
    {% if permissions.update %}
        <input type="text" name="description" value="{{ entity.description|escape }}">
        <button type="submit" name="action" value="save">Guardar</button>
    {% endif %}
    
    {% if permissions.delete %}
        <button type="submit" name="action" value="delete">Eliminar</button>
    {% endif %}
</form>

<!-- 3. Escapar todas las variables de usuario -->
<div class="user-info">
    <p>Conectado como: {{ user.nick|escape }}</p>
    <p>Email: {{ user.email|escape }}</p>
</div>
```

### Crear una pagina nueva en el sistema

Para que la pagina tenga control de accesos:

```php
// En tu plugin, registrar la pagina
class MyModel extends ModelClass {
    public function getPageData(): array
    {
        return [
            'name' => 'MyCustomPage',
            'title' => 'Mi pagina personalizada',
            'icon' => 'fa-solid fa-heart',
            'menu' => 'Parametros',
            'submenu' => null,
            'showonmenu' => true,
            'ordernum' => 100
        ];
    }
}
```

Luego en Settings, asignar roles con permisos a esa pagina en EditRole.

### Validar acceso a recursos especificos

```php
// Para datos del propietario
if ($model->owner !== $this->user->nick && !$this->user->can('MyPage', 'only-owner-data')) {
    throw new AccessDeniedException('No puedes acceder a datos de otros usuarios');
}

// Para empresas
if ($model->idempresa !== $this->empresa->idempresa && !$this->user->admin) {
    throw new AccessDeniedException('No puedes acceder a datos de otras empresas');
}
```

### Generar y validar tokens API

```php
// En ApiController
public function run()
{
    // Obtener apikey
    $apikey = $this->request->header('X-API-KEY') 
        ?? $this->request->input('apikey');
    
    // Cargar y validar
    $key = new ApiKey();
    if (!$key->loadBy('apikey', $apikey) || !$key->enabled) {
        return $this->response->setStatusCode(401, 'Unauthorized');
    }
    
    // Verificar permiso para el recurso
    $resource = $this->request->input('resource', 'invoices');
    $method = strtolower($this->request->method());
    
    if (!$key->hasAccess($resource, $method)) {
        return $this->response->setStatusCode(403, 'Forbidden');
    }
    
    // Procesar solicitud...
}
```

### Prevenir ataques comunes

#### Inyeccion SQL
- Usar siempre `Where` helpers en lugar de concatenacion de strings
- Usar parametros de prepared statements

```php
// MALO - susceptible a inyeccion
$where = "nickname = '" . $_GET['user'] . "'";

// BUENO - usar Where
$where = [Where::eq('nick', $this->request->input('user'))];
```

#### XSS (Cross-Site Scripting)
- Usar `Tools::noHtml()` en modelos
- Usar `|escape` filter en Twig
- Nunca mostrar datos de usuario sin escapar

```php
// En el modelo
$this->description = Tools::noHtml($this->description);

// En el template
{{ product.name|escape }}
{{ user.comments|escape }}
```

#### CSRF
- Validar token en todo POST/PUT/DELETE
- Token debe ser validado Y no debe ser duplicado

```php
if (!$this->multiRequestProtection->validate($token)) {
    return false;
}
if ($this->multiRequestProtection->tokenExist($token)) {
    return false;
}
```

#### Exposicion de informacion
- No mostrar errores detallados en produccion
- Usar logs en lugar de mostrar al usuario
- No incluir datos sensibles en respuestas de error

```php
// MALO
throw new Exception('Usuario no encontrado en BD con SQL: ' . $query);

// BUENO
Tools::log()->error('user-not-found', ['%nick%' => $nick]);
throw new AccessDeniedException('Usuario no encontrado');
```

---

## Apendice: Resumen de flujos de seguridad

### Flujo de Login

```
Usuario ingresa credenciales
    |
    v
Validar token CSRF (MultiRequestProtection::validate)
    |
    v
Verificar que token no sea duplicado (MultiRequestProtection::tokenExist)
    |
    v
Verificar bloqueo por intentos fallidos (userHasManyIncidents)
    |
    v
Cargar usuario de BD
    |
    v
Verificar que usuario este habilitado (enabled = true)
    |
    v
Verificar contrasena (User::verifyPassword con password_verify)
    |
    v
Si tiene 2FA habilitado:
    - Mostrar formulario 2FA
    - Usuario ingresa codigo TOTP
    - Validar codigo (User::verifyTwoFactorCode)
    |
    v
Generar nuevo logkey (User::newLogkey - 99 caracteres aleatorios)
    |
    v
Actualizar actividad (User::updateActivity)
    |
    v
Guardar usuario en BD
    |
    v
Guardar cookies:
    - fsNick (nombre usuario)
    - fsLogkey (clave sesion)
    - fsLang (idioma)
    |
    v
Redirigir a homepage del usuario
```

### Flujo de verificacion de acceso a pagina

```
Usuario intenta acceder a pagina
    |
    v
Controller.__construct() -> inicializa multiRequestProtection
    |
    v
User::can('PageName', 'access')
    |
    v
¿Usuario esta habilitado (enabled)?
    NO -> false (acceso denegado)
    |
    YES
    |
    v
¿Usuario es admin?
    SI -> true (acceso permitido)
    NO -> continuar
    |
    v
RoleAccess::allFromUser($nick, $pageName)
    |
    v
Para cada acceso, verificar RoleAccess::can($permission)
    |
    v
Si al menos uno permite -> true
Si ninguno permite -> false
```

### Flujo de proteccion CSRF

```
GET request para mostrar formulario:
    |
    v
Controller genera token: multiRequestProtection->newToken()
    |
    v
Token tiene formato: SHA1_HASH|RANDOM_6_CHARS
    |
    v
Se incluye token en formulario HTML
    |
    v
    
POST request con datos:
    |
    v
Obtener token del formulario
    |
    v
multiRequestProtection->validate($token)
    |
    v
¿Token tiene formato correcto (SHA1|random)?
    NO -> false
    |
    YES
    |
    v
¿SHA1 del token valida contra seed+hora actual?
    NO -> comprobar hasta 4 horas atras
    |
    v
¿SHA1 coincide con una hora valida?
    NO -> false (token expirado)
    |
    YES
    |
    v
multiRequestProtection->tokenExist($token)
    |
    v
¿Token ya fue usado antes?
    SI -> true (duplicado, rechazar)
    NO -> agregar a cache y retornar false (nuevo, permitir)
    |
    v
Si todo ok, procesar formulario
```

---

Documento generado para FacturaScripts 2025 - Referencia exhaustiva de seguridad
Ultima actualizacion: 2025
