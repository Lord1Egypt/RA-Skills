# FacturaScripts 2025 - Referencia Completa del Sistema de Base de Datos

## Tabla de Contenidos

1. [Abstraccion de Base de Datos](#1-abstraccion-de-base-de-datos)
2. [Motores Soportados](#2-motores-soportados)
3. [DbQuery - Constructor de Consultas](#3-dbquery---constructor-de-consultas)
4. [Where - Clausulas de Filtrado](#4-where---clausulas-de-filtrado)
5. [DbUpdater - Actualizacion de Esquema](#5-dbupdater---actualizacion-de-esquema)
6. [Migraciones](#6-migraciones)
7. [NextCode - Generacion de Codigos Secuenciales](#7-nextcode---generacion-de-codigos-secuenciales)
8. [Esquema Completo de Base de Datos](#8-esquema-completo-de-base-de-datos)
9. [Formato XML de Tablas](#9-formato-xml-de-tablas)
10. [Ejemplos Practicos](#10-ejemplos-practicos)

---

## 1. Abstraccion de Base de Datos

La clase `DataBase` (ubicada en `/Core/Base/DataBase.php`) proporciona una capa de abstraccion completa para interactuar con bases de datos MySQL y PostgreSQL de manera uniforme.

### Inicializacion y Conexion

```php
use FacturaScripts\Core\Base\DataBase;

$db = new DataBase();
$db->connect();  // Retorna bool

// Verificar conexion
if ($db->connected()) {
    // hacer algo
}

// Desconectar
$db->close();
```

### Propiedades Principales

- `engine`: Instancia de `DataBaseEngine` (MysqlEngine o PostgresqlEngine)
- `link`: Recurso de conexion a la base de datos
- `tables`: Cache de nombres de tablas
- `type`: Tipo de motor ('mysql' o 'postgresql')

### Metodos de Conexion

#### `connect(): bool`
Establece la conexion con la base de datos usando las credenciales de configuracion (FS_DB_HOST, FS_DB_USER, FS_DB_PASS, FS_DB_NAME, FS_DB_PORT).

#### `connected(): bool`
Retorna true si hay una conexion activa con la base de datos.

#### `close(): bool`
Cierra la conexion con la base de datos. Si hay una transaccion abierta, hace rollback.

#### `version(): string`
Retorna la version del motor de base de datos y el nombre del motor. Ej: "MySQL 8.0.23" o "POSTGRESQL 13.2"

### Metodos de Consultas

#### `select(string $sql): array`
Ejecuta una consulta SELECT sin paginacion y retorna un array con los resultados.

```php
$sql = 'SELECT * FROM clientes WHERE codcliente = "001";';
$results = $db->select($sql);
foreach ($results as $row) {
    echo $row['nombre'];
}
```

#### `selectLimit(string $sql, int $limit = FS_ITEM_LIMIT, int $offset = 0): array`
Ejecuta una consulta SELECT con paginacion. Automaticamente agrega LIMIT y OFFSET.

```php
$sql = 'SELECT * FROM clientes;';
$results = $db->selectLimit($sql, 10, 20);  // 10 resultados a partir del registro 20
```

#### `exec(string $sql): bool`
Ejecuta sentencias DDL (CREATE, ALTER, DROP) o DML (INSERT, UPDATE, DELETE). Maneja automaticamente transacciones:
- Si no hay transaccion abierta, crea una, ejecuta y la cierra
- Si hay transaccion abierta, solo ejecuta
- Retorna bool indicando exito/fallo

```php
$sql = 'INSERT INTO clientes (codcliente, nombre) VALUES ("002", "Cliente Nuevo");';
if ($db->exec($sql)) {
    echo 'Insercion exitosa';
} else {
    echo 'Error: ' . $db->getEngine()->errorMessage($db->link);
}
```

### Metodos de Esquema

#### `tableExists(string $tableName, array $list = []): bool`
Verifica si una tabla existe en la base de datos.

```php
if ($db->tableExists('clientes')) {
    echo 'La tabla clientes existe';
}
```

#### `getTables(): array`
Retorna un array con los nombres de todas las tablas en la base de datos. Los resultados se cachean.

```php
$tables = $db->getTables();
// ['clientes', 'proveedores', 'productos', ...]
```

#### `getColumns(string $tableName): array`
Retorna un array asociativo con las columnas de una tabla. Cada columna tiene:
- `name`: Nombre de la columna
- `type`: Tipo de dato
- `is_nullable`: 'YES' o 'NO'
- `default`: Valor por defecto
- `extra`: Informacion adicional (MySQL)

```php
$columns = $db->getColumns('clientes');
// [
//   'codcliente' => ['name' => 'codcliente', 'type' => 'varchar(10)', 'is_nullable' => 'NO', ...],
//   'nombre' => ['name' => 'nombre', 'type' => 'varchar(100)', 'is_nullable' => 'NO', ...],
//   ...
// ]
```

#### `getConstraints(string $tableName, bool $extended = false): array`
Retorna un array con las restricciones (constraints) de una tabla. Cada restriccion tiene:
- `name`: Nombre de la restriccion
- `type`: Tipo ('PRIMARY KEY', 'FOREIGN KEY', 'UNIQUE', etc.)
- Si $extended=true, tambien incluye: `column_name`, `foreign_table_name`, `foreign_column_name`, `on_update`, `on_delete`

```php
$constraints = $db->getConstraints('clientes');
// Incluye claves primarias, foraneas, unique, etc.

$constraints = $db->getConstraints('clientes', true);
// Incluye detalles de columnas y acciones ON UPDATE/DELETE
```

#### `getIndexes(string $tableName): array`
Retorna un array con los indices de la tabla que comienzan con 'fs_' (indices de FacturaScripts).

```php
$indexes = $db->getIndexes('clientes');
// [
//   ['name' => 'fs_codagente', 'column' => 'codagente'],
//   ['name' => 'fs_codpago', 'column' => 'codpago'],
//   ...
// ]
```

#### `getAllIndexes(string $tableName): array`
Retorna TODOS los indices de una tabla, incluyendo los del sistema.

### Metodos de Escape

#### `escapeString(mixed $str): string`
Escapa una cadena para usarla de manera segura en una consulta SQL. Previene inyecciones SQL.

```php
$clienteNombre = "O'Reilly & Associates";
$escapedName = $db->escapeString($clienteNombre);  // O\'Reilly & Associates
$sql = "SELECT * FROM clientes WHERE nombre = '" . $escapedName . "'";
```

#### `escapeColumn(string $name): string`
Escapa un nombre de columna/tabla. En MySQL usa backticks (`), en PostgreSQL usa comillas dobles (").

```php
$escapedCol = $db->escapeColumn('tabla.columna');
// MySQL: `tabla`.`columna`
// PostgreSQL: "tabla"."columna"
```

#### `var2str(mixed $val): string`
Convierte una variable a su representacion SQL segura:
- null -> NULL
- true -> TRUE
- false -> FALSE
- fecha (formato Y-m-d) -> '2025-04-12'
- fecha-hora -> '2025-04-12 14:30:00'
- cadena -> 'valor escapado'

```php
$val1 = $db->var2str(null);           // 'NULL'
$val2 = $db->var2str(true);           // 'TRUE'
$val3 = $db->var2str('Jose');         // "'Jose'"
$val4 = $db->var2str('2025-04-12');   // "'2025-04-12'"
```

### Transacciones

Una transaccion es un grupo de operaciones que se ejecutan atomicamente. Si alguna falla, todas se revierten.

#### `beginTransaction(): bool`
Inicia una transaccion. Si ya hay una abierta, retorna true sin hacer nada.

#### `commit(): bool`
Confirma la transaccion y aplica todos los cambios realizados. Retorna bool indicando exito/fallo.

#### `rollback(): bool`
Revierte la transaccion y descarta todos los cambios pendientes.

#### `inTransaction(): bool`
Verifica si hay una transaccion abierta actualmente.

```php
try {
    $db->beginTransaction();
    
    $db->exec('INSERT INTO clientes (codcliente, nombre) VALUES ("001", "Cliente 1");');
    $db->exec('INSERT INTO clientes (codcliente, nombre) VALUES ("002", "Cliente 2");');
    
    if ($db->commit()) {
        echo 'Transaccion completada exitosamente';
    } else {
        throw new Exception('Error al confirmar transaccion');
    }
} catch (Exception $e) {
    $db->rollback();
    echo 'Error: ' . $e->getMessage();
}
```

### Metodos Utilitarios

#### `lastval(): int|bool`
Retorna el ultimo ID generado por una sentencia INSERT (AUTOINCREMENT).

```php
$db->exec('INSERT INTO productos (referencia) VALUES ("PROD001");');
$lastId = $db->lastval();  // Retorna el ID generado
```

#### `castInteger(string $col): string`
Genera una expresion SQL para convertir una columna a entero. Difiere segun el motor:
- MySQL: CAST(columna AS unsigned)
- PostgreSQL: CAST(columna AS integer)

```php
$castExpr = $db->castInteger('codigo');  // Para usar en ORDER BY, WHERE, etc.
```

#### `getOperator(string $operator): string`
Retorna el operador SQL equivalente para el motor actual. Util para operadores especiales como REGEXP.

```php
$op = $db->getOperator('REGEXP');
// MySQL: REGEXP
// PostgreSQL: ~
```

#### `updateSequence(string $tableName, array $fields): void`
Actualiza las secuencias de PostgreSQL (las autoincrementales). Se llama automaticamente al crear tablas.

---

## 2. Motores Soportados

### DataBaseEngine Interface

La clase abstracta `DataBaseEngine` define la interfaz que deben implementar todos los motores. Contiene metodos abstractos y concretos que proporcionan la funcionalidad basica.

#### Metodos Abstractos (deben implementar MysqlEngine y PostgresqlEngine)

- `beginTransaction($link): bool`
- `castInteger($link, $column): string`
- `close($link): bool`
- `columnFromData($colData): array`
- `commit($link): bool`
- `connect(&$error): resource`
- `errorMessage($link): string`
- `escapeColumn($link, $name): string`
- `escapeString($link, $str): string`
- `exec($link, $sql): bool`
- `getSQL(): DataBaseQueries`
- `inTransaction($link): bool`
- `listTables($link): array`
- `rollback($link): bool`
- `select($link, $sql): array`
- `version($link): string`

#### Metodos Concretos

- `clearError(): void` - Limpia el ultimo mensaje de error
- `compareDataTypes($dbType, $xmlType): bool` - Compara tipos de datos entre BD y XML
- `dateStyle(): string` - Retorna el formato de fecha (por defecto 'Y-m-d')
- `getOperator($operator): string` - Retorna el operador para el motor
- `hasError(): bool` - Indica si hay un error almacenado
- `updateSequence($link, $tableName, $fields): void` - Actualiza secuencias (PostgreSQL)

### MySQL Engine

**Clase**: `MysqlEngine`
**Ubicacion**: `/Core/Base/DataBase/MysqlEngine.php`
**Requisito**: Extension mysqli de PHP

#### Caracteristicas Especiales

- Usa backticks (`) para escapar identificadores: \`tabla\`.\`columna\`
- Para castear a integer usa: CAST(columna AS unsigned)
- Gestiona transacciones con START TRANSACTION, COMMIT, ROLLBACK
- Admite charset y collation configurables (FS_MYSQL_CHARSET, FS_MYSQL_COLLATE)
- Soporta foreign key checks (FS_DB_FOREIGN_KEYS)
- Tipos de datos:
  - varchar(n) -> character varying(n)
  - tinyint(1) -> boolean
  - int -> integer
  - double -> double precision
  - text -> text
  - timestamp -> timestamp
  - date -> date
  - time -> time

#### Ejemplo de Conexion MySQL

```php
// En config.php
define('FS_DB_TYPE', 'mysql');
define('FS_DB_HOST', 'localhost');
define('FS_DB_USER', 'usuario');
define('FS_DB_PASS', 'contraseña');
define('FS_DB_NAME', 'facturascripts');
define('FS_DB_PORT', 3306);
define('FS_MYSQL_CHARSET', 'utf8mb4');
define('FS_MYSQL_COLLATE', 'utf8mb4_unicode_ci');
```

### PostgreSQL Engine

**Clase**: `PostgresqlEngine`
**Ubicacion**: `/Core/Base/DataBase/PostgresqlEngine.php`
**Requisito**: Extension pg_* (PostgreSQL) de PHP

#### Caracteristicas Especiales

- Usa comillas dobles (") para escapar identificadores: "tabla"."columna"
- Para castear a integer usa: CAST(columna AS integer)
- Gestiona transacciones con BEGIN TRANSACTION, COMMIT, ROLLBACK
- Utiliza secuencias para autoincremento: tabla_columna_seq
- El operador REGEXP se traduce a ~ (expresion regular de PostgreSQL)
- Soporta SSL y connection strings avanzadas
- Tipos de datos:
  - character varying(n) -> character varying(n)
  - boolean -> boolean
  - integer -> integer
  - double precision -> double precision
  - text -> text
  - timestamp -> timestamp
  - date -> date
  - time -> time

#### Ejemplo de Conexion PostgreSQL

```php
// En config.php
define('FS_DB_TYPE', 'postgresql');
define('FS_DB_HOST', 'localhost');
define('FS_DB_USER', 'usuario');
define('FS_DB_PASS', 'contraseña');
define('FS_DB_NAME', 'facturascripts');
define('FS_DB_PORT', 5432);
define('FS_PGSQL_SSL', 'prefer');  // opcional: require, prefer, allow, disable
define('FS_PGSQL_ENDPOINT', '');   // opcional: para Aurora PostgreSQL
```

### Diferencias Clave entre Motores

| Aspecto | MySQL | PostgreSQL |
|---------|-------|-----------|
| Delimitador de ID | Backtick (`) | Comilla Doble (") |
| Autoincrement | AUTO_INCREMENT | Secuencias (SERIAL/SEQUENCE) |
| Cast a Integer | CAST AS unsigned | CAST AS integer |
| REGEXP | REGEXP | ~ (tilde) |
| Transacciones | START/COMMIT/ROLLBACK | BEGIN/COMMIT/ROLLBACK |
| Charset | Configurable (utf8, utf8mb4) | UTF-8 por defecto |
| Foreign Keys | Pueden desactivarse | Siempre activas |
| Collation | Configurable | No configurable |

---

## 3. DbQuery - Constructor de Consultas

**Clase**: `DbQuery`
**Ubicacion**: `/Core/DbQuery.php`

DbQuery es un query builder fluent que permite construir consultas SQL de manera segura y orientada a objetos, sin escribir SQL raw. Soporta todos los operadores SQL comunes, agregaciones, agrupaciones, ordenes, limites y offsets.

### Inicializacion

```php
use FacturaScripts\Core\DbQuery;

// Crear una consulta
$query = DbQuery::table('clientes');

// O instancia directa
$query = new DbQuery('clientes');
```

### Propiedades Publicas

- `fields`: Campos a seleccionar (default: '*')
- `groupBy`: Clausula GROUP BY
- `having`: Clausula HAVING
- `limit`: Numero de registros a retornar (default: 0)
- `offset`: Desplazamiento (default: 0)
- `orderBy`: Array de campos de ordenamiento
- `where`: Array de clausulas WHERE

### Metodos de Seleccion

#### `select(string $fields): self`
Define los campos a seleccionar. Acepta campos separados por coma.

```php
$query = DbQuery::table('clientes')
    ->select('codcliente, nombre, email');
```

#### `selectRaw(string $fields): self`
Define campos usando expresiones SQL raw sin escapar.

```php
$query = DbQuery::table('facturascli')
    ->selectRaw('codigo, COUNT(*) as total, SUM(total) as subtotal');
```

#### `get(): array`
Ejecuta la consulta y retorna un array con todos los resultados (respeta limit y offset).

```php
$clientes = DbQuery::table('clientes')
    ->whereEq('debaja', false)
    ->orderBy('nombre')
    ->get();
```

#### `first(): array`
Ejecuta la consulta y retorna solo el primer resultado (establece automaticamente limit=1, offset=0).

```php
$cliente = DbQuery::table('clientes')
    ->whereEq('codcliente', '001')
    ->first();
```

#### `count(string $field = ''): int`
Retorna el numero de registros que cumplen las condiciones. Si se especifica $field, cuenta registros DISTINCT del campo.

```php
$total = DbQuery::table('clientes')->count();  // Total de clientes

$agentes = DbQuery::table('clientes')
    ->count('codagente');  // Clientes con agente diferente (DISTINCT)
```

### Metodos de Agregacion

#### `sum(string $field, ?int $decimals = null): float`
Retorna la suma de un campo numerico.

```php
$total = DbQuery::table('facturascli')
    ->whereEq('pagada', false)
    ->sum('total');  // Suma de facturas sin pagar

$redondeado = DbQuery::table('facturascli')
    ->sum('total', 2);  // Redondeado a 2 decimales
```

#### `avg(string $field, ?int $decimals = null): float`
Retorna el promedio de un campo.

```php
$promedio = DbQuery::table('facturascli')
    ->avg('total');  // Promedio de importes
```

#### `min(string $field, ?int $decimals = null): float`
#### `minString(string $field): string`
Retorna el valor minimo de un campo.

```php
$minimo = DbQuery::table('facturascli')->min('total');
$minimoStr = DbQuery::table('facturascli')->minString('total');  // Sin conversion
```

#### `max(string $field, ?int $decimals = null): float`
#### `maxString(string $field): string`
Retorna el valor maximo de un campo.

```php
$maximo = DbQuery::table('facturascli')->max('total');
```

#### `sumArray(string $field, string $groupByKey): array`
Suma agrupada por un campo. Retorna array clave->suma.

```php
$totalesPorAgente = DbQuery::table('facturascli')
    ->sumArray('total', 'codagente');
// ['001' => 5000, '002' => 3500, ...]
```

#### `avgArray(string $field, string $groupByKey): array`
Promedio agrupado por un campo.

#### `minArray(string $field, string $groupByKey): array`
Minimo agrupado por un campo.

#### `maxArray(string $field, string $groupByKey): array`
Maximo agrupado por un campo.

#### `countArray(string $field, string $groupByKey): array`
Conteo agrupado por un campo.

```php
$conteosPorSerie = DbQuery::table('facturascli')
    ->countArray('codigo', 'codserie');
// ['A' => 100, 'B' => 50, ...]
```

#### `array(string $key, string $value): array`
Retorna los resultados como un array asociativo clave->valor.

```php
$clientes = DbQuery::table('clientes')
    ->array('codcliente', 'nombre');
// ['001' => 'Cliente A', '002' => 'Cliente B', ...]
```

### Metodos de Clausulas WHERE

#### `where(array $where): self`
Agrega clausulas WHERE. Acepta array de instancias de `Where`.

```php
use FacturaScripts\Core\Where;

$where = [
    Where::eq('debaja', false),
    Where::like('nombre', 'jose')
];
$clientes = DbQuery::table('clientes')->where($where)->get();
```

#### `whereEq(string $field, mixed $value): self`
Igualdad: WHERE campo = valor

```php
DbQuery::table('clientes')->whereEq('codcliente', '001')->get();
```

#### `whereNotEq(string $field, mixed $value): self`
Desigualdad: WHERE campo != valor

```php
DbQuery::table('clientes')->whereNotEq('debaja', true)->get();
```

#### `whereGt(string $field, mixed $value): self`
Mayor que: WHERE campo > valor

```php
DbQuery::table('facturascli')->whereGt('total', 1000)->get();
```

#### `whereGte(string $field, mixed $value): self`
Mayor o igual: WHERE campo >= valor

#### `whereLt(string $field, mixed $value): self`
Menor que: WHERE campo < valor

#### `whereLte(string $field, mixed $value): self`
Menor o igual: WHERE campo <= valor

#### `whereBetween(string $field, mixed $value1, mixed $value2): self`
Entre: WHERE campo BETWEEN valor1 AND valor2

```php
$facturasEnRango = DbQuery::table('facturascli')
    ->whereBetween('fecha', '2025-01-01', '2025-03-31')
    ->get();
```

#### `whereLike(string $field, string $value): self`
Busqueda parcial: WHERE LOWER(campo) LIKE '%valor%'
(Automaticamente agrega % si no estan presentes)

```php
$clientes = DbQuery::table('clientes')
    ->whereLike('nombre', 'jose')  // Busca "jose" en cualquier posicion
    ->get();
```

#### `whereIn(string $field, array $values): self`
Pertenencia a lista: WHERE campo IN (valor1, valor2, ...)

```php
$facturas = DbQuery::table('facturascli')
    ->whereIn('codserie', ['A', 'B', 'C'])
    ->get();
```

#### `whereNotIn(string $field, array $values): self`
No pertenencia a lista: WHERE campo NOT IN (...)

#### `whereNull(string $field): self`
Es nulo: WHERE campo IS NULL

```php
$clientesSinAgente = DbQuery::table('clientes')
    ->whereNull('codagente')
    ->get();
```

#### `whereNotNull(string $field): self`
No es nulo: WHERE campo IS NOT NULL

#### Llamadas Magicas (Dynamic Where)
Se puede usar `where<NombreCampo>()` para condiciones de igualdad.

```php
// Equivalente a: ->whereEq('codcliente', '001')
DbQuery::table('clientes')->whereCodcliente('001')->get();

// Equivalente a: ->whereEq('debaja', false)
DbQuery::table('clientes')->whereDebaja(false)->get();
```

### Metodos de Agrupacion y Ordenamiento

#### `groupBy(string $fields): self`
Define campos para agrupar resultados. Campos separados por coma.

```php
$ventasPorAgente = DbQuery::table('facturascli')
    ->select('codagente, SUM(total) as total')
    ->groupBy('codagente')
    ->get();
```

#### `having(string $having): self`
Define clausula HAVING (filtrado despues de GROUP BY).

```php
$agentesAltos = DbQuery::table('facturascli')
    ->select('codagente, SUM(total) as total')
    ->groupBy('codagente')
    ->having('SUM(total) > 5000')
    ->get();
```

#### `orderBy(string $field, string $order = 'ASC'): self`
Ordena resultados por un campo. $order puede ser 'ASC' o 'DESC'.

```php
DbQuery::table('clientes')
    ->orderBy('nombre', 'ASC')
    ->get();
```

**Opciones especiales para $field**:
- `lower:nombre` -> Ordena por LOWER(nombre)
- `upper:nombre` -> Ordena por UPPER(nombre)
- `integer:codigo` -> Castea a integer y ordena numericamente
- `LOWER(nombre)` -> Expresion SQL permitida
- `CAST(codigo AS INTEGER)` -> Expresion SQL permitida

```php
// Ordenamiento con transformacion
DbQuery::table('clientes')
    ->orderBy('lower:nombre', 'ASC')  // Case-insensitive
    ->get();

// Ordenamiento numerico de campo alfanumerico
DbQuery::table('productos')
    ->orderBy('integer:codigo', 'ASC')
    ->get();
```

#### `orderMulti(array $fields): self`
Ordena por multiples campos. Array con campo => orden.

```php
DbQuery::table('facturascli')
    ->orderMulti([
        'codagente' => 'ASC',
        'fecha' => 'DESC'
    ])
    ->get();
```

#### `reorder(): self`
Limpia todos los ordenes establecidos.

```php
$query = DbQuery::table('clientes')->orderBy('nombre');
$query->reorder();  // Elimina el ORDER BY
```

### Metodos de Paginacion

#### `limit(int $limit): self`
Define el numero maximo de registros a retornar.

#### `offset(int $offset): self`
Define el desplazamiento (numero de registros a saltar desde el inicio).

```php
// Pagina 1: registros 1-10
$pagina1 = DbQuery::table('clientes')
    ->limit(10)
    ->offset(0)
    ->get();

// Pagina 2: registros 11-20
$pagina2 = DbQuery::table('clientes')
    ->limit(10)
    ->offset(10)
    ->get();

// Pagina 3: registros 21-30
$pagina3 = DbQuery::table('clientes')
    ->limit(10)
    ->offset(20)
    ->get();
```

### Metodos de Modificacion de Datos

#### `insert(array $data): bool`
Inserta uno o multiples registros en la tabla.

```php
// Insercion simple
$exito = DbQuery::table('clientes')->insert([
    'codcliente' => '001',
    'nombre' => 'Cliente Nuevo',
    'cifnif' => '12345678A'
]);

// Insercion multiple
$datos = [
    ['codcliente' => '001', 'nombre' => 'Cliente 1'],
    ['codcliente' => '002', 'nombre' => 'Cliente 2'],
    ['codcliente' => '003', 'nombre' => 'Cliente 3']
];
$exito = DbQuery::table('clientes')->insert($datos);
```

#### `insertGetId(array $data): ?int`
Inserta un registro y retorna el ID generado (AUTOINCREMENT), o null si falla.

```php
$idProducto = DbQuery::table('productos')->insertGetId([
    'referencia' => 'PROD001',
    'descripcion' => 'Mi Producto'
]);

if ($idProducto) {
    echo "Producto creado con ID: $idProducto";
}
```

#### `update(array $data): bool`
Actualiza registros que cumplen las condiciones WHERE.

```php
$exito = DbQuery::table('clientes')
    ->whereEq('codcliente', '001')
    ->update([
        'nombre' => 'Cliente Actualizado',
        'email' => 'nuevo@email.com'
    ]);
```

#### `delete(): bool`
Elimina registros que cumplen las condiciones WHERE.

```php
$exito = DbQuery::table('clientes')
    ->whereEq('codcliente', '001')
    ->delete();
```

### Metodos Utilitarios

#### `sql(): string`
Retorna la consulta SQL sin ejecutarla. Util para debugging.

```php
$sql = DbQuery::table('clientes')
    ->whereEq('debaja', false)
    ->orderBy('nombre')
    ->sql();

echo $sql;  
// SELECT * FROM `clientes` WHERE `debaja` = FALSE ORDER BY `nombre` ASC
```

### Ejemplo Completo de DbQuery

```php
use FacturaScripts\Core\DbQuery;

// Consulta basica
$clientes = DbQuery::table('clientes')
    ->select('codcliente, nombre, email')
    ->whereEq('debaja', false)
    ->whereLike('nombre', 'jose')
    ->orderBy('nombre')
    ->limit(10)
    ->get();

// Con agregaciones
$totalPorAgente = DbQuery::table('facturascli')
    ->select('codagente')
    ->selectRaw('SUM(total) as total, COUNT(*) as cantidad')
    ->groupBy('codagente')
    ->having('SUM(total) > 1000')
    ->get();

// INSERT
$insertar = [
    'codcliente' => '010',
    'nombre' => 'Cliente Nuevo',
    'cifnif' => '12345678A',
    'debaja' => false
];
DbQuery::table('clientes')->insert($insertar);

// UPDATE
DbQuery::table('clientes')
    ->whereEq('codcliente', '010')
    ->update(['nombre' => 'Cliente Actualizado']);

// DELETE
DbQuery::table('clientes')
    ->whereEq('codcliente', '010')
    ->delete();

// Construccion de paginacion
$pagina = 2;
$porPagina = 20;
$clientes = DbQuery::table('clientes')
    ->limit($porPagina)
    ->offset(($pagina - 1) * $porPagina)
    ->get();
```

---

## 4. Where - Clausulas de Filtrado

**Clase**: `Where`
**Ubicacion**: `/Core/Where.php`

La clase `Where` proporciona metodos estaticos para construir clausulas WHERE de manera segura y orientada a objetos.

### Operadores Basicos

#### `eq(string $field, mixed $value): Where`
Igualdad: WHERE campo = valor (o IS NULL si valor es null)

```php
Where::eq('debaja', false)
Where::eq('codcliente', '001')
Where::eq('email', null)  // IS NULL
```

#### `notEq(string $field, mixed $value): Where`
Desigualdad: WHERE campo != valor (o IS NOT NULL si valor es null)

```php
Where::notEq('debaja', true)
Where::notEq('email', null)  // IS NOT NULL
```

#### `gt(string $field, mixed $value): Where`
Mayor que: WHERE campo > valor

```php
Where::gt('total', 1000)
Where::gt('fecha', '2025-01-01')
```

#### `gte(string $field, mixed $value): Where`
Mayor o igual: WHERE campo >= valor

#### `lt(string $field, mixed $value): Where`
Menor que: WHERE campo < valor

#### `lte(string $field, mixed $value): Where`
Menor o igual: WHERE campo <= valor

#### `in(string $field, array $values): Where`
Pertenencia a lista: WHERE campo IN (valor1, valor2, ...)

```php
Where::in('codserie', ['A', 'B', 'C'])
Where::in('codagente', ['001', '002'])
```

#### `notIn(string $field, array $values): Where`
No pertenencia: WHERE campo NOT IN (...)

#### `like(string $field, string $value): Where`
Busqueda parcial: WHERE LOWER(campo) LIKE '%valor%'

```php
Where::like('nombre', 'carlos')   // Busca "carlos" en cualquier posicion
Where::like('email', '@gmail')    // Busca dominios gmail
```

#### `notLike(string $field, string $value): Where`
Negacion de busqueda: WHERE LOWER(campo) NOT LIKE '%valor%'

#### `xlike(string $field, string $value): Where`
Busqueda extendida: busca todas las palabras en el campo (AND entre palabras).

```php
Where::xlike('nombre', 'jose carlos')
// Equivalente a: (LOWER(campo) LIKE '%jose%') AND (LOWER(campo) LIKE '%carlos%')
```

#### `between(string $field, mixed $value1, mixed $value2): Where`
Rango: WHERE campo BETWEEN valor1 AND valor2

```php
Where::between('fecha', '2025-01-01', '2025-03-31')
Where::between('total', 100, 1000)
```

#### `notBetween(string $field, mixed $value1, mixed $value2): Where`
Rango negativo: WHERE campo NOT BETWEEN valor1 AND valor2

#### `isNull(string $field): Where`
Es nulo: WHERE campo IS NULL

```php
Where::isNull('codagente')
```

#### `isNotNull(string $field): Where`
No es nulo: WHERE campo IS NOT NULL

#### `regexp(string $field, string $value): Where`
Expresion regular: WHERE campo REGEXP 'valor' (MySQL) o ~ 'valor' (PostgreSQL)

```php
Where::regexp('codigo', '^[A-Z]{3}[0-9]{3}$')  // Codigo con patron
```

### Operadores con OR

Todos los operadores tienen equivalentes con `or` al inicio:

```php
Where::or('campo', 'valor', '=')      // OR campo = valor
Where::orEq('campo', 'valor')
Where::orNotEq('campo', 'valor')
Where::orGt('campo', 'valor')
Where::orGte('campo', 'valor')
Where::orLt('campo', 'valor')
Where::orLte('campo', 'valor')
Where::orIn('campo', ['val1', 'val2'])
Where::orNotIn('campo', ['val1', 'val2'])
Where::orLike('campo', 'valor')
Where::orNotLike('campo', 'valor')
Where::orBetween('campo', 'val1', 'val2')
Where::orNotBetween('campo', 'val1', 'val2')
Where::orIsNull('campo')
Where::orIsNotNull('campo')
Where::orRegexp('campo', 'patron')
Where::orXlike('campo', 'valor')
```

### Constructor Avanzado

#### `__construct(string $fields, mixed $value, string $operator = '=', string $operation = 'AND', bool $useField = false)`

Permite crear clausulas personalizadas:
- `$fields`: Campo o campos (pueden usar separador | para multiples)
- `$value`: Valor a comparar
- `$operator`: Operador SQL ('=', '!=', '>', '<', '>=', '<=', 'LIKE', 'IN', 'BETWEEN', 'REGEXP', etc.)
- `$operation`: 'AND' o 'OR' para conectar con otras clausulas
- `$useField`: Si true, el valor se interpreta como nombre de campo

```php
// Comparacion entre campos
$where = new Where('total', 'field:totalcoste', '>', 'AND', true);
// WHERE total > totalcoste

// Operacion con OR
$where = new Where('debaja', true, '=', 'OR');
// OR debaja = true
```

#### `useField(): self`
Especifica que el valor debe interpretarse como nombre de campo en lugar de valor.

```php
$where = Where::eq('total', 'field:netosindto')->useField();
// WHERE total = netosindto
```

### Clausulas Complejas

#### `sub(array $where, string $operation = 'AND'): Where`
Crea un subgrupo de clausulas entre parentesis.

```php
$subgrupo = Where::sub([
    Where::eq('debaja', false),
    Where::orEq('codagente', '001')
]);
// WHERE (debaja = FALSE OR codagente = '001')

$consulta = DbQuery::table('clientes')
    ->where([
        Where::like('nombre', 'jose'),
        $subgrupo
    ])
    ->get();
// WHERE nombre LIKE '%jose%' AND (debaja = FALSE OR codagente = '001')
```

#### `orSub(array $where): Where`
Subgrupo conectado con OR.

```php
$subgrupo = Where::orSub([
    Where::eq('debaja', false),
    Where::eq('codagente', null)
]);
// OR (debaja = FALSE OR codagente IS NULL)
```

### Campos Multiples

Usando el separador `|`, se pueden especificar multiples campos. Se genera un OR entre ellos.

```php
Where::like('nombre|razonsocial', 'carlos')
// WHERE (LOWER(nombre) LIKE '%carlos%') OR (LOWER(razonsocial) LIKE '%carlos%')
```

### Metodos Estaticos para SQL Raw

#### `multiSql(array $where): string`
Convierte un array de clausulas Where a SQL raw (sin WHERE inicial).

#### `multiSqlLegacy(array $where): string`
Convierte a SQL raw con WHERE inicial (compatible con legacy).

```php
$where = [
    Where::eq('debaja', false),
    Where::like('nombre', 'jose')
];

$sql = Where::multiSqlLegacy($where);
// WHERE `debaja` = FALSE AND LOWER(`nombre`) LIKE '%jose%'
```

### Ejemplos Complejos

```php
use FacturaScripts\Core\DbQuery;
use FacturaScripts\Core\Where;

// Consulta con multiples condiciones
$clientes = DbQuery::table('clientes')->where([
    Where::eq('debaja', false),
    Where::like('nombre', 'jose'),
    Where::gt('riesgoalcanzado', 0)
])->get();

// Consulta con OR
$clientes = DbQuery::table('clientes')->where([
    Where::like('nombre|razonsocial', 'consultoria'),
    Where::orEq('personafisica', true)
])->get();
// WHERE (LOWER(nombre|razonsocial) LIKE '%consultoria%') OR personafisica = TRUE

// Consulta con subgrupo
$clientes = DbQuery::table('clientes')->where([
    Where::gte('riesgomax', 5000),
    Where::sub([
        Where::eq('debaja', false),
        Where::orIsNull('codagente')
    ])
])->get();
// WHERE riesgomax >= 5000 AND (debaja = FALSE OR codagente IS NULL)

// Comparacion entre campos
$movimientos = DbQuery::table('partidas')->where([
    Where::eq('debe', 'field:haber')->useField()
])->get();
// WHERE debe = haber
```

---

## 5. DbUpdater - Actualizacion de Esquema

**Clase**: `DbUpdater`
**Ubicacion**: `/Core/DbUpdater.php`

DbUpdater gestiona la creacion y actualizacion de tablas comparando la definicion XML con la estructura actual de la base de datos.

### Archivos de Control

DbUpdater mantiene dos archivos JSON en MyFiles para rastrear cambios:

- `db-updater.json`: Lista de tablas ya verificadas
- `db-changelog.json`: Registro de todos los cambios aplicados

### Metodos Principales

#### `createTable(string $tableName, array $structure = [], string $sqlAfter = ''): bool`
Crea una tabla nueva en la base de datos. Lee la definicion desde el archivo XML.

```php
DbUpdater::createTable('mi_tabla');  // Lee mi_tabla.xml

// O con estructura personalizada
$estructura = [
    'columns' => [
        'id' => ['name' => 'id', 'type' => 'serial', 'null' => 'NO'],
        'nombre' => ['name' => 'nombre', 'type' => 'varchar(100)', 'null' => 'YES']
    ],
    'constraints' => [
        'tabla_pkey' => ['name' => 'tabla_pkey', 'constraint' => 'PRIMARY KEY (id)']
    ],
    'indexes' => [
        'nombre_idx' => ['name' => 'nombre_idx', 'columns' => 'nombre']
    ]
];
DbUpdater::createTable('mi_tabla', $estructura);

// Con SQL adicional
DbUpdater::createTable('mi_tabla', [], 'CREATE INDEX idx_custom ON mi_tabla (campo);');
```

#### `updateTable(string $tableName, array $structure = []): bool`
Actualiza una tabla existente. Compara columnas, restricciones e indices.

```php
DbUpdater::updateTable('clientes');  // Lee clientes.xml

// Procesos internos:
// 1. Compara columnas (agrega nuevas, modifica tipos, defaults, null)
// 2. Compara restricciones (elimina las no definidas, agrega nuevas)
// 3. Compara indices (elimina los no definidos, agrega nuevos)
```

#### `createOrUpdateTable(string $tableName, array $structure = [], string $sqlAfter = ''): bool`
Crea la tabla si no existe, si existe la actualiza.

```php
DbUpdater::createOrUpdateTable('clientes');
```

#### `dropTable(string $tableName): bool`
Elimina una tabla de la base de datos.

```php
if (DbUpdater::dropTable('tabla_antigua')) {
    echo 'Tabla eliminada';
}
```

### Lectura de XML

#### `readTableXml(string $filePath): array`
Lee un archivo XML de tabla y retorna su estructura en formato array.

```php
$estructura = DbUpdater::readTableXml('/ruta/a/tabla.xml');
// Retorna array con 'columns', 'constraints', 'indexes'
```

#### `getTableXmlLocation(string $tableName): string`
Retorna la ruta al archivo XML de una tabla. Busca primero en Dinamic, luego en Core.

```php
$ruta = DbUpdater::getTableXmlLocation('clientes');
// /ruta/facturascripts/Dinamic/Table/clientes.xml
// o /ruta/facturascripts/Core/Table/clientes.xml
```

### Control de Tablas Verificadas

#### `isTableChecked(string $tableName): bool`
Verifica si una tabla ya ha sido procesada (para evitar reprocesamiento).

```php
if (DbUpdater::isTableChecked('clientes')) {
    echo 'Tabla ya fue actualizada';
}
```

#### `rebuild(): void`
Elimina el archivo de control, forzando a revertificar todas las tablas.

```php
DbUpdater::rebuild();  // Proxima ejecucion verificara todas las tablas
```

### Manejo de Errores

#### `getLastError(): string`
Retorna el ultimo error ocurrido.

```php
if (!DbUpdater::createTable('clientes')) {
    echo 'Error: ' . DbUpdater::getLastError();
}
```

### Comparacion de Columnas

DbUpdater detecta y aplica estos cambios en columnas:

1. **Nuevas columnas**: Las agrega con ADD COLUMN
2. **Columnas renombradas**: Las detecta si tienen atributo <rename> y usa RENAME COLUMN
3. **Cambios de tipo**: Usa ALTER MODIFY COLUMN
4. **Cambios de default**: Usa ALTER COLUMN SET DEFAULT
5. **Cambios en NULL**: Usa ALTER COLUMN SET/DROP NOT NULL

```php
// En el XML
<column>
    <name>nuevo_nombre</name>
    <type>varchar(100)</type>
    <null>NO</null>
    <default>''</default>
    <rename>nombre_antiguo</rename>  <!-- Renombracion -->
</column>
```

### Comparacion de Restricciones

DbUpdater detecta y aplica estos cambios:

1. **Foreign keys perdidas**: Las elimina
2. **Unique perdidos**: Los elimina
3. **Nuevas restricciones**: Las agrega

```php
// En el XML
<constraint>
    <name>ca_tabla_referencia</name>
    <type>FOREIGN KEY (codref) REFERENCES referencia (codref) ON DELETE SET NULL ON UPDATE CASCADE</type>
</constraint>
```

### Comparacion de Indices

DbUpdater detecta:

1. **Indices perdidos**: Los elimina
2. **Nuevos indices**: Los crea con prefijo fs_

```php
// En el XML
<index>
    <name>codigo</name>
    <columns>codigo</columns>
</index>
<!-- Se crea como: fs_codigo -->
```

### Proceso de Actualizacion Completo

```php
use FacturaScripts\Core\DbUpdater;

// Actualizar tablas del sistema
DbUpdater::createOrUpdateTable('clientes');
DbUpdater::createOrUpdateTable('productos');
DbUpdater::createOrUpdateTable('facturascli');

// En caso de error
$error = DbUpdater::getLastError();
if (!empty($error)) {
    Tools::log()->error('db-update-error', ['%error%' => $error]);
}

// Forzar re-verificacion si es necesario
DbUpdater::rebuild();
```

---

## 6. Migraciones

**Clase**: `Migrations`
**Ubicacion**: `/Core/Migrations.php`

El sistema de migraciones permite aplicar cambios en datos y estructura de manera controlada. Hay migraciones del core y del sistema de plugins.

### Migraciones del Core

Las migraciones del core se ejecutan automaticamente y son controladas por version. Se ejecutan una sola vez.

#### Migraciones Actuales (2025)

1. **clearLogs** - Limpia logs antiguos cuando hay demasiados
2. **fixSeries** - Actualiza tipo de serie a 'R' (rectificativa) si estaba marcada
3. **fixAgentes** - Desvincula agentes que no existen en tabla agentes
4. **fixApiKeysUsers** - Desvincula api_keys de usuarios eliminados
5. **fixAgenciasTransporte** - Desvincula agencias de transporte inexistentes
6. **fixFormasPago** - Crea formas de pago fantasma para documentos huerfanos
7. **fixRectifiedInvoices** - Limpia referencias a facturas rectificadas inexistentes

### Metodos Publicos

#### `run(): void`
Ejecuta todas las migraciones del core que aun no se hayan ejecutado.

```php
Migrations::run();  // Se ejecuta automaticamente en el kernel
```

#### `runPluginMigration(MigrationClass $migration): void`
Ejecuta una migracion de un plugin (una sola vez).

```php
$migration = new MigrationClass();
Migrations::runPluginMigration($migration);
```

#### `runPluginMigrations(array $migrations): void`
Ejecuta multiples migraciones de un plugin.

```php
$migraciones = [
    new MigrationCrearTabla1(),
    new MigrationCrearTabla2(),
    new MigrationActualizarDatos()
];
Migrations::runPluginMigrations($migraciones);
```

### Archivo de Control

Las migraciones ejecutadas se registran en `MyFiles/migrations.json`:

```json
[
    "clearLogs",
    "fixSeries",
    "fixAgentes",
    "miplugin:v1_crear_tabla_custom",
    "miplugin:v2_actualizar_datos"
]
```

Solo se ejecutan migraciones que no esten en esta lista.

### Crear una Migracion Personalizada

```php
namespace FacturaScripts\Plugins\MiPlugin\Migrations;

use FacturaScripts\Core\Template\MigrationClass;
use FacturaScripts\Core\Base\DataBase;

class Version001CreateTablaCustom extends MigrationClass
{
    public function run(): void
    {
        $db = new DataBase();
        $db->connect();
        
        // Crear tabla
        $sql = 'CREATE TABLE mi_tabla_custom (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );';
        
        $db->exec($sql);
    }
    
    public function getFullMigrationName(): string
    {
        return 'miplugin:v1_crear_tabla_custom';
    }
}

// En el inicializador del plugin
use FacturaScripts\Core\Migrations;

Migrations::runPluginMigration(new Version001CreateTablaCustom());
```

---

## 7. NextCode - Generacion de Codigos Secuenciales

**Clase**: `NextCode`
**Ubicacion**: `/Core/NextCode.php`

NextCode genera numeros secuenciales siguiendo el ultimo numero registrado en una columna, manejando concurrencia mediante archivos lock.

### Metodos

#### `get(string $table, string $column, string $type = 'int'): ?int`
Obtiene el proximo numero secuencial para una tabla/columna. Maneja bloqueos para evitar duplicados.

```php
use FacturaScripts\Core\NextCode;

// Obtener proximo numero de factura
$nextNumber = NextCode::get('facturascli', 'numero');
// Retorna: 1, 2, 3, 4, ...

// Si en el futuro el numero esta ocupado, incrementa
$nextNumber = NextCode::get('facturascli', 'numero');  // Retorna el proximo disponible

// Para campos no numericos que contienen numeros
$nextCode = NextCode::get('productos', 'codigo', 'int');
// Busca numeros en el codigo y retorna el proximo
```

#### `clearOld(): void`
Limpia archivos lock antiguos (mas de 1 hora). Se llama periodicamente.

```php
NextCode::clearOld();  // Libera bloqueos abandonados
```

### Mecanismo de Bloqueo

NextCode usa archivos `.lock` en `MyFiles/Tmp/` para evitar condiciones de carrera:

```
facturascli_numero_150.lock  -> Bloquea numero 150
facturascli_numero_151.lock  -> Bloquea numero 151
```

Si un proceso se cuelga, el archivo lock expira despues de 1 hora y es eliminado.

### Ejemplo de Uso

```php
use FacturaScripts\Core\NextCode;

// En un modelo
public function getNextNumber(): ?int
{
    return NextCode::get(self::tableName(), 'numero');
}

// En un controlador
$factura = new FacturaCliente();
$factura->numero = NextCode::get('facturascli', 'numero');
if ($factura->numero === null) {
    echo 'No se pudo generar numero';
    return;
}

$factura->save();
```

---

## 8. Esquema Completo de Base de Datos

### Area Funcional: Maestros de Negocio

#### Tabla: clientes
**Proposito**: Almacena informacion de clientes.
**Clave primaria**: codcliente

| Columna | Tipo | NULL | Default | Descripcion |
|---------|------|------|---------|-------------|
| cifnif | varchar(30) | NO | | CIF/NIF del cliente |
| codagente | varchar(10) | SI | | Codigo del agente asignado |
| codcliente | varchar(10) | NO | | Codigo unico del cliente |
| codgrupo | varchar(6) | SI | | Grupo de cliente |
| codpago | varchar(10) | SI | | Forma de pago por defecto |
| codproveedor | varchar(10) | SI | | Si tambien es proveedor |
| codretencion | varchar(10) | SI | | Tipo de retencion |
| codserie | varchar(4) | SI | | Serie de documentos |
| codsubcuenta | varchar(15) | SI | | Subcuenta contable |
| codtarifa | varchar(6) | SI | | Tarifa por defecto |
| debaja | boolean | SI | false | Marcado como dado de baja |
| diaspago | varchar(10) | SI | | Dias de pago (ej: 30) |
| excepcioniva | varchar(20) | SI | | Excepcion de IVA |
| email | varchar(100) | SI | | Email del cliente |
| fax | varchar(30) | SI | | Numero de fax |
| fechaalta | date | SI | | Fecha de alta |
| fechabaja | date | SI | | Fecha de baja |
| idcontactoenv | integer | SI | | Contacto para envios |
| idcontactofact | integer | SI | | Contacto para facturacion |
| langcode | varchar(10) | SI | | Idioma preferido |
| nombre | varchar(100) | NO | | Nombre comercial |
| observaciones | text | SI | | Notas |
| personafisica | boolean | SI | true | Es persona fisica |
| razonsocial | varchar(100) | SI | | Razon social |
| regimeniva | varchar(20) | SI | | Regimen de IVA |
| riesgoalcanzado | double | SI | | Riesgo actual |
| riesgomax | double | SI | | Limite de riesgo |
| telefono1 | varchar(30) | SI | | Telefono principal |
| telefono2 | varchar(30) | SI | | Telefono secundario |
| tipoidfiscal | varchar(25) | SI | | Tipo de identificacion fiscal |
| web | varchar(100) | SI | | Sitio web |

**Indices**: codagente, codpago, codgrupo, codretencion, codserie, codtarifa
**Restricciones FK**: agentes, formaspago, gruposclientes, retenciones, series, tarifas

---

#### Tabla: proveedores
**Proposito**: Almacena informacion de proveedores.
**Clave primaria**: codproveedor

| Columna | Tipo | NULL | Default | Descripcion |
|---------|------|------|---------|-------------|
| acreedor | boolean | SI | false | Es acreedor |
| cifnif | varchar(30) | NO | | CIF/NIF del proveedor |
| codcliente | varchar(10) | SI | | Si tambien es cliente |
| codimpuestoportes | varchar(10) | SI | | Impuesto de portes |
| codpago | varchar(10) | SI | | Forma de pago por defecto |
| codproveedor | varchar(10) | NO | | Codigo unico |
| codretencion | varchar(10) | SI | | Tipo de retencion |
| codserie | varchar(4) | SI | | Serie de documentos |
| codsubcuenta | varchar(15) | SI | | Subcuenta contable |
| debaja | boolean | SI | false | Dado de baja |
| email | varchar(100) | SI | | Email |
| fax | varchar(30) | SI | | Fax |
| fechaalta | date | SI | | Fecha de alta |
| fechabaja | date | SI | | Fecha de baja |
| idcontacto | integer | SI | | Contacto principal |
| langcode | varchar(10) | SI | | Idioma |
| nombre | varchar(100) | NO | | Nombre comercial |
| observaciones | text | SI | | Notas |
| personafisica | boolean | SI | true | Persona fisica |
| razonsocial | varchar(100) | SI | | Razon social |
| regimeniva | varchar(20) | SI | | Regimen IVA |
| telefono1 | varchar(30) | SI | | Telefono 1 |
| telefono2 | varchar(30) | SI | | Telefono 2 |
| tipoidfiscal | varchar(25) | SI | | Tipo identificacion |
| web | varchar(100) | SI | | Sitio web |

**Restricciones FK**: formaspago, retenciones, series

---

#### Tabla: productos
**Proposito**: Catalogo de productos y servicios.
**Clave primaria**: idproducto (auto-increment)

| Columna | Tipo | NULL | Default | Descripcion |
|---------|------|------|---------|-------------|
| actualizado | timestamp | SI | | Ultima actualizacion |
| bloqueado | boolean | SI | false | Bloqueado para edicion |
| codfabricante | varchar(8) | SI | | Fabricante |
| codfamilia | varchar(8) | SI | | Familia de producto |
| codimpuesto | varchar(10) | SI | | Impuesto aplicable |
| codsubcuentacom | varchar(15) | SI | | Subcuenta compra |
| codsubcuentairpfcom | varchar(15) | SI | | Subcuenta IRPF compra |
| codsubcuentaven | varchar(15) | SI | | Subcuenta venta |
| descripcion | text | SI | | Descripcion completa |
| excepcioniva | varchar(20) | SI | | Excepcion IVA |
| fechaalta | date | SI | | Fecha de alta |
| idproducto | serial | NO | | ID unico |
| nostock | boolean | SI | false | No controla stock |
| observaciones | text | SI | | Notas |
| precio | double | SI | 0 | Precio de venta |
| publico | boolean | SI | false | Visible en tienda |
| referencia | varchar(30) | NO | | Codigo de producto (UNIQUE) |
| secompra | boolean | SI | true | Se compra |
| sevende | boolean | SI | true | Se vende |
| stockfis | double | SI | 0 | Stock fisico |
| tipo | varchar(50) | SI | | Tipo (articulo, servicio, etc.) |
| ventasinstock | boolean | SI | false | Permite venta sin stock |

**Indices**: referencia (UNIQUE), fabricante, familia, impuesto
**Restricciones FK**: fabricantes, familias, impuestos

---

### Area Funcional: Documentos de Venta

#### Tabla: facturascli
**Proposito**: Facturas de clientes (ventas).
**Clave primaria**: idfactura (auto-increment)

| Columna | Tipo | NULL | Default | Descripcion |
|---------|------|------|---------|-------------|
| apartado | varchar(10) | SI | | Apartado postal |
| cifnif | varchar(30) | NO | | CIF/NIF cliente |
| ciudad | varchar(100) | SI | | Ciudad facturacion |
| codagente | varchar(10) | SI | | Agente que realizo venta |
| codalmacen | varchar(4) | SI | | Almacen origen |
| codcliente | varchar(10) | SI | | Codigo cliente |
| coddivisa | varchar(3) | NO | | Moneda |
| codejercicio | varchar(4) | NO | | Ejercicio fiscal |
| codigo | varchar(20) | NO | | Codigo interno (UNIQUE con empresa) |
| codigoenv | varchar(200) | SI | | Referencia envio |
| codigorect | varchar(20) | SI | | Factura que rectifica |
| codpago | varchar(10) | NO | | Forma de pago |
| codpais | varchar(20) | SI | | Pais cliente |
| codpostal | varchar(10) | SI | | Codigo postal |
| codserie | varchar(4) | NO | | Serie factura |
| codtrans | varchar(8) | SI | | Agencia transporte |
| direccion | varchar(200) | SI | | Direccion facturacion |
| dtopor1 | double | SI | | Descuento 1 % |
| dtopor2 | double | SI | | Descuento 2 % |
| editable | boolean | SI | | Permite modificacion |
| fecha | date | NO | | Fecha factura |
| fechadevengo | date | SI | | Fecha devengo (para IVA) |
| femail | date | SI | | Fecha envio por mail |
| hora | time | SI | | Hora de emision |
| idasiento | integer | SI | | Asiento contable vinculado |
| idcontactoenv | integer | SI | | Contacto envio |
| idcontactofact | integer | SI | | Contacto facturacion |
| idempresa | integer | SI | | Empresa que factura |
| idestado | integer | SI | | Estado documento |
| idfactura | serial | NO | | ID unico |
| idfacturarect | integer | SI | | Factura rectificada por esta |
| irpf | double | SI | | % IRPF |
| neto | double | SI | | Total sin IVA |
| netosindto | double | SI | 0 | Total antes descuentos |
| nick | varchar(50) | SI | | Usuario que creo |
| nombrecliente | varchar(100) | NO | | Nombre cliente |
| numdocs | integer | SI | 0 | Numero documentos adjuntos |
| numero | varchar(12) | NO | | Numero factura (UNIQUE con serie, ejercicio, empresa) |
| numero2 | varchar(50) | SI | | Numero secundario |
| observaciones | text | SI | | Notas |
| operacion | varchar(20) | SI | | Tipo operacion |
| pagada | boolean | SI | false | Marcado como pagado |
| provincia | varchar(100) | SI | | Provincia facturacion |
| tasaconv | double | SI | | Tasa conversion moneda |
| total | double | SI | | Importe total |
| totalbeneficio | double | SI | | Beneficio estimado |
| totalcoste | double | SI | | Costo estimado |
| totaleuros | double | SI | | Total en euros |
| totalirpf | double | SI | | Total IRPF |
| totaliva | double | SI | | Total IVA |
| totalrecargo | double | SI | | Total recargo equivalencia |
| totalsuplidos | double | SI | 0 | Total gastos suplidos |
| vencida | boolean | SI | false | Vencida (sin pagar) |

**Indices**: codagente, codalmacen, codcliente, coddivisa, codejercicio, codpago, codserie, codtrans, idasiento, idempresa, idestado, nick
**Restricciones FK**: agentes, almacenes, clientes, divisas, ejercicios, formaspago, series, agenciastrans, asientos, empresas, estados_documentos, facturascli (idfacturarect), users

---

#### Tabla: lineasfacturascli
**Proposito**: Lineas de detalle de facturas a clientes.
**Clave primaria**: idlinea (auto-increment)

Almacena articulos/servicios incluidos en cada factura con precio, cantidad, impuestos, etc.

| Columna | Tipo | Descripcion |
|---------|------|-------------|
| idfactura | integer | ID factura (FK) |
| idlinea | serial | ID linea |
| idproducto | integer | Producto (FK) |
| cantidad | double | Cantidad |
| pvunitario | double | Precio unitario |
| pvtotal | double | Precio total |
| dto | double | Descuento % |
| codimpuesto | varchar(10) | Impuesto aplicado |
| iva | double | % IVA |
| recargo | double | % Recargo equivalencia |
| irpf | double | % IRPF |
| descripcion | text | Descripcion linea |

---

### Area Funcional: Documentos de Compra

#### Tabla: facturasprov
**Proposito**: Facturas de proveedores (compras).
**Clave primaria**: idfactura (auto-increment)

Estructura similar a facturascli pero para compras.

| Columna | Tipo | NULL | Default | Descripcion |
|---------|------|------|---------|-------------|
| cifnif | varchar(30) | NO | | CIF/NIF proveedor |
| codalmacen | varchar(4) | SI | | Almacen destino |
| coddivisa | varchar(3) | NO | | Moneda |
| codejercicio | varchar(4) | NO | | Ejercicio fiscal |
| codigo | varchar(20) | NO | | Codigo interno (UNIQUE) |
| codigorect | varchar(20) | SI | | Factura rectificada |
| codpago | varchar(10) | NO | | Forma de pago |
| codproveedor | varchar(10) | SI | | Proveedor |
| codserie | varchar(4) | NO | | Serie |
| dtopor1 | double | SI | | Descuento 1 % |
| dtopor2 | double | SI | | Descuento 2 % |
| editable | boolean | SI | | Editable |
| fecha | date | NO | | Fecha |
| fechadevengo | date | SI | | Fecha devengo |
| femail | date | SI | | Fecha mail |
| hora | time | SI | | Hora |
| idasiento | integer | SI | | Asiento contable |
| idempresa | integer | SI | | Empresa |
| idestado | integer | SI | | Estado |
| idfactura | serial | NO | | ID factura |
| idfacturarect | integer | SI | | Factura rectificada por |
| irpf | double | SI | | IRPF % |
| neto | double | SI | | Total sin IVA |
| netosindto | double | SI | 0 | Total s/descuentos |
| nick | varchar(50) | SI | | Usuario |
| numdocs | integer | SI | 0 | Documentos adjuntos |
| nombre | varchar(100) | NO | | Nombre proveedor |
| numero | varchar(12) | NO | | Numero factura |
| numproveedor | varchar(50) | SI | | Numero en proveedor |
| observaciones | text | SI | | Notas |
| operacion | varchar(20) | SI | | Tipo operacion |
| pagada | boolean | SI | false | Pagada |
| tasaconv | double | SI | | Tasa conversion |
| total | double | SI | | Total |
| totaleuros | double | SI | | Total euros |
| totalirpf | double | SI | | Total IRPF |
| totaliva | double | SI | | Total IVA |
| totalrecargo | double | SI | | Total recargo |
| totalsuplidos | double | SI | 0 | Suplidos |
| vencida | boolean | SI | false | Vencida |

**Restricciones FK**: almacenes, divisas, ejercicios, formaspago, proveedores, series, asientos, empresas, estados_documentos, users

---

### Area Funcional: Contabilidad

#### Tabla: ejercicios
**Proposito**: Ejercicios fiscales (periodos contables).
**Clave primaria**: codejercicio

| Columna | Tipo | NULL | Default | Descripcion |
|---------|------|------|---------|-------------|
| codejercicio | varchar(4) | NO | | Codigo ejercicio (ej: 2025) |
| nombre | varchar(50) | SI | | Nombre ejercicio |
| fechainicio | date | SI | | Fecha inicio |
| fechafin | date | SI | | Fecha fin |
| estado | varchar(20) | SI | | Estado (abierto, cerrado) |
| longsubcuenta | integer | SI | | Longitud subcuentas |

---

#### Tabla: asientos
**Proposito**: Apuntes contables.
**Clave primaria**: idasiento (auto-increment)

| Columna | Tipo | NULL | Default | Descripcion |
|---------|------|------|---------|-------------|
| canal | integer | SI | | Canal origen |
| codejercicio | varchar(4) | NO | | Ejercicio |
| concepto | varchar(255) | SI | | Concepto asiento |
| documento | varchar(50) | SI | | Documento vinculado |
| editable | boolean | NO | | Permite edicion |
| fecha | date | NO | | Fecha asiento |
| idasiento | serial | NO | | ID unico |
| iddiario | integer | SI | | Diario contable |
| idempresa | integer | SI | | Empresa |
| importe | double | NO | 0 | Importe total |
| numero | integer | NO | | Numero secuencial |
| operacion | varchar(1) | SI | | Tipo operacion (E,G) |

**Indices**: fecha, codejercicio, numero
**Restricciones FK**: diarios, ejercicios, empresas

---

#### Tabla: partidas
**Proposito**: Partidas de apuntes contables (debe/haber).
**Clave primaria**: idpartida (auto-increment)

| Columna | Tipo | Descripcion |
|---------|------|-------------|
| idasiento | integer | Asiento (FK) |
| idpartida | serial | ID partida |
| idsubcuenta | integer | Subcuenta (FK) |
| concepto | varchar(255) | Concepto |
| debe | double | Importe debe |
| haber | double | Importe haber |
| codigodocumento | varchar(50) | Doc vinculado |
| tipoasiento | varchar(50) | Tipo asiento |

**Restricciones FK**: asientos, subcuentas

---

#### Tabla: cuentas
**Proposito**: Plan contable de cuentas.
**Clave primaria**: idcuenta (auto-increment)

| Columna | Tipo | NULL | Default | Descripcion |
|---------|------|------|---------|-------------|
| codcuenta | varchar(10) | NO | | Codigo cuenta |
| codcuentaesp | varchar(6) | SI | | Cuenta especial |
| codejercicio | varchar(4) | NO | | Ejercicio |
| debe | double | SI | | Totales debe |
| descripcion | varchar(255) | SI | | Descripcion |
| haber | double | SI | | Totales haber |
| idcuenta | serial | NO | | ID unico |
| parent_codcuenta | varchar(10) | SI | | Cuenta padre |
| parent_idcuenta | integer | SI | | ID padre |
| saldo | double | SI | | Saldo |

**Indices**: codcuenta, codejercicio (UNIQUE)
**Restricciones FK**: cuentasesp, ejercicios, cuentas (parent)

---

#### Tabla: subcuentas
**Proposito**: Subcuentas dentro de cuentas (6 digitos adicionales).
**Clave primaria**: idsubcuenta (auto-increment)

| Columna | Tipo | Descripcion |
|---------|------|-------------|
| idcuenta | integer | Cuenta (FK) |
| codsubcuenta | varchar(15) | Codigo subcuenta |
| descripcion | varchar(255) | Descripcion |
| debe | double | Totales debe |
| haber | double | Totales haber |
| saldo | double | Saldo actual |

**Restricciones FK**: cuentas

---

### Area Funcional: Usuarios y Seguridad

#### Tabla: users
**Proposito**: Usuarios del sistema.
**Clave primaria**: nick

| Columna | Tipo | NULL | Default | Descripcion |
|---------|------|------|---------|-------------|
| admin | boolean | NO | false | Es administrador |
| codagente | varchar(10) | SI | | Agente asociado |
| codalmacen | varchar(4) | SI | | Almacen por defecto |
| codserie | varchar(4) | SI | | Serie por defecto |
| creationdate | date | SI | | Fecha creacion |
| email | varchar(100) | SI | | Email usuario |
| enabled | boolean | NO | true | Habilitado |
| homepage | varchar(30) | SI | | Pagina inicio |
| idempresa | integer | SI | | Empresa por defecto |
| langcode | varchar(10) | SI | | Idioma |
| lastactivity | timestamp | SI | | Ultima actividad |
| lastbrowser | varchar(200) | SI | | Navegador ultima sesion |
| lastip | varchar(40) | SI | | IP ultima sesion |
| level | integer | SI | | Nivel acceso |
| logkey | varchar(100) | SI | | Clave login |
| nick | varchar(50) | NO | | Usuario |
| password | varchar(255) | NO | | Hash password |
| two_factor_enabled | boolean | NO | false | 2FA habilitado |
| two_factor_secret_key | varchar(32) | SI | | Clave 2FA |

**Restricciones FK**: pages, empresas, series

---

#### Tabla: roles
**Proposito**: Roles de acceso del sistema.
**Clave primaria**: idrol (auto-increment)

| Columna | Tipo | Descripcion |
|---------|------|-------------|
| idrol | serial | ID rol |
| nombre | varchar(100) | Nombre rol |
| descripcion | text | Descripcion |

---

#### Tabla: roles_access
**Proposito**: Permisos por rol.
**Clave primaria**: idaccess (auto-increment)

| Columna | Tipo | Descripcion |
|---------|------|-------------|
| idrol | integer | Rol (FK) |
| idaccess | serial | ID acceso |
| pagename | varchar(100) | Pagina/funcionalidad |
| allowdelete | boolean | Permite borrar |
| allowexport | boolean | Permite exportar |
| allowimport | boolean | Permite importar |
| allowupdate | boolean | Permite modificar |

---

#### Tabla: roles_users
**Proposito**: Asignacion de roles a usuarios.
**Clave primaria**: ID rol + usuario

| Columna | Tipo | Descripcion |
|---------|------|-------------|
| idrol | integer | Rol (FK) |
| nick | varchar(50) | Usuario (FK) |

---

### Area Funcional: Configuracion y Datos Maestros

#### Tabla: empresas
**Proposito**: Datos de empresa(s) del sistema.
**Clave primaria**: idempresa (auto-increment)

| Columna | Tipo | NULL | Default | Descripcion |
|---------|------|------|---------|-------------|
| administrador | varchar(100) | SI | | Nombre administrador |
| apartado | varchar(10) | SI | | Apartado postal |
| cifnif | varchar(30) | SI | | CIF/NIF |
| ciudad | varchar(100) | SI | | Ciudad |
| codpais | varchar(20) | SI | | Pais |
| codpostal | varchar(10) | SI | | Codigo postal |
| direccion | varchar(200) | SI | | Direccion |
| excepcioniva | varchar(20) | SI | | Excepcion IVA |
| email | varchar(100) | SI | | Email |
| fax | varchar(30) | SI | | Fax |
| fechaalta | date | SI | | Fecha creacion |
| idempresa | serial | NO | | ID unico |
| idlogo | integer | SI | | Logo (FK attached_files) |
| nombre | varchar(100) | NO | | Nombre empresa |
| nombrecorto | varchar(32) | SI | | Nombre corto (32 chars max) |
| observaciones | text | SI | | Notas |
| personafisica | boolean | SI | false | Persona fisica |
| provincia | varchar(100) | SI | | Provincia |
| regimeniva | varchar(50) | SI | | Regimen IVA |
| telefono1 | varchar(30) | SI | | Telefono 1 |
| telefono2 | varchar(30) | SI | | Telefono 2 |
| tipoidfiscal | varchar(25) | SI | | Tipo identificacion |
| web | varchar(100) | SI | | Sitio web |

---

#### Tabla: series
**Proposito**: Series de facturacion (A, B, C, etc.).
**Clave primaria**: codserie

| Columna | Tipo | NULL | Default | Descripcion |
|---------|------|------|---------|-------------|
| canal | integer | SI | | Canal de venta |
| codserie | varchar(4) | NO | | Codigo serie |
| descripcion | varchar(100) | SI | | Descripcion |
| iddiario | integer | SI | | Diario contable |
| siniva | boolean | NO | false | Sin IVA |
| tipo | varchar(4) | SI | | Tipo (V, C, R) |

**Restricciones FK**: diarios

---

#### Tabla: divisas
**Proposito**: Monedas soportadas.
**Clave primaria**: coddivisa

| Columna | Tipo | Descripcion |
|---------|------|-------------|
| coddivisa | varchar(3) | Codigo ISO (EUR, USD, etc.) |
| descripcion | varchar(100) | Nombre |
| tasa | double | Tasa cambio respecto EUR |

---

#### Tabla: formaspago
**Proposito**: Formas/metodos de pago.
**Clave primaria**: codpago

| Columna | Tipo | Descripcion |
|---------|------|-------------|
| codpago | varchar(10) | Codigo |
| descripcion | varchar(100) | Descripcion |
| genbanking | boolean | Genera movimientos bancarios |
| domiciliado | boolean | Domiciliado |
| activa | boolean | Activa |

---

#### Tabla: impuestos
**Proposito**: Tipos de IVA y otros impuestos.
**Clave primaria**: codimpuesto

| Columna | Tipo | Descripcion |
|---------|------|-------------|
| codimpuesto | varchar(10) | Codigo |
| descripcion | varchar(100) | Descripcion |
| iva | double | Porcentaje IVA |
| recargo | double | Recargo equivalencia % |
| activo | boolean | Activo |

---

#### Tabla: almacenes
**Proposito**: Almacenes/ubicaciones.
**Clave primaria**: codalmacen

| Columna | Tipo | Descripcion |
|---------|------|-------------|
| codalmacen | varchar(4) | Codigo |
| nombre | varchar(100) | Nombre |
| pais | varchar(20) | Pais |
| provincia | varchar(100) | Provincia |
| poblacion | varchar(100) | Ciudad |
| descripcion | text | Descripcion |

---

#### Tabla: stocks
**Proposito**: Stock actual de productos por almacen.
**Clave primaria**: ID producto + almacen

| Columna | Tipo | Descripcion |
|---------|------|-------------|
| idproducto | integer | Producto (FK) |
| codalmacen | varchar(4) | Almacen (FK) |
| cantidad | double | Cantidad stock |
| reservada | double | Cantidad reservada |
| actualizado | timestamp | Ultima actualizacion |

---

#### Tabla: tarifas
**Proposito**: Listas de precios.
**Clave primaria**: codtarifa

| Columna | Tipo | Descripcion |
|---------|------|-------------|
| codtarifa | varchar(6) | Codigo |
| nombre | varchar(100) | Nombre |
| descripcion | text | Descripcion |

---

#### Tabla: settings
**Proposito**: Configuracion del sistema (clave-valor).
**Clave primaria**: name

| Columna | Tipo | Descripcion |
|---------|------|-------------|
| name | varchar(100) | Clave configuracion |
| value | text | Valor |

---

### Area Funcional: Miscellaneous

#### Tabla: logs
**Proposito**: Registro de eventos y errores.
**Clave primaria**: idlog (auto-increment)

| Columna | Tipo | Descripcion |
|---------|------|-------------|
| idlog | serial | ID |
| channel | varchar(50) | Canal (master, controller, database, etc.) |
| level | varchar(20) | Nivel (debug, info, warning, error, critical) |
| message | text | Mensaje |
| context | json | Contexto adicional |
| time | timestamp | Timestamp |

---

#### Tabla: attached_files
**Proposito**: Archivos adjuntos a documentos.
**Clave primaria**: idfile (auto-increment)

| Columna | Tipo | Descripcion |
|---------|------|-------------|
| idfile | serial | ID |
| filename | varchar(255) | Nombre archivo |
| mimetype | varchar(100) | Tipo MIME |
| size | integer | Tamaño bytes |
| path | text | Ruta en servidor |
| createddate | timestamp | Fecha creacion |
| createdby | varchar(50) | Usuario creador |

---

#### Tabla: pages
**Proposito**: Paginas/secciones del sistema.
**Clave primaria**: name

| Columna | Tipo | Descripcion |
|---------|------|-------------|
| name | varchar(100) | Nombre pagina |
| title | varchar(255) | Titulo |
| menu | varchar(50) | Menu padre |
| submenu | varchar(50) | Submenu |
| showonmenu | boolean | Mostrar en menu |
| icon | varchar(100) | Icono |
| order | integer | Orden visualizacion |

---

#### Tabla: pages_filters
**Proposito**: Filtros guardados por pagina.
**Clave primaria**: idfilter (auto-increment)

| Columna | Tipo | Descripcion |
|---------|------|-------------|
| idfilter | serial | ID |
| pagename | varchar(100) | Pagina (FK pages) |
| nick | varchar(50) | Usuario (FK users) |
| name | varchar(100) | Nombre filtro |
| filters | json | Filtros JSON |
| isdefault | boolean | Es filtro por defecto |

---

#### Tabla: pages_options
**Proposito**: Opciones/preferencias de visualizacion por pagina.
**Clave primaria**: ID pagina + usuario

| Columna | Tipo | Descripcion |
|---------|------|-------------|
| pagename | varchar(100) | Pagina |
| nick | varchar(50) | Usuario |
| columns | json | Columnas visibles |
| pagesize | integer | Registros por pagina |
| ordering | varchar(100) | Campo ordenamiento |
| direction | varchar(4) | ASC/DESC |

---

#### Tabla: api_keys
**Proposito**: Claves API para acceso programatico.
**Clave primaria**: id (auto-increment)

| Columna | Tipo | Descripcion |
|---------|------|-------------|
| id | serial | ID |
| nick | varchar(50) | Usuario propietario (FK) |
| apikey | varchar(255) | Clave API (UNIQUE) |
| creation | timestamp | Fecha creacion |
| lastuse | timestamp | Ultimo uso |
| enabled | boolean | Habilitada |

---

## 9. Formato XML de Tablas

Las tablas se definen en archivos XML ubicados en `/Core/Table/` (o `/Dinamic/Table/` para personalizaciones).

### Estructura Basica

```xml
<?xml version="1.0" encoding="UTF-8"?>
<table>
    <!-- Definicion de columnas -->
    <column>
        <name>id</name>
        <type>serial</type>
        <null>NO</null>
    </column>
    <column>
        <name>nombre</name>
        <type>character varying(100)</type>
        <null>NO</null>
        <default></default>
    </column>
    
    <!-- Restricciones -->
    <constraint>
        <name>tabla_pkey</name>
        <type>PRIMARY KEY (id)</type>
    </constraint>
    <constraint>
        <name>fk_tabla_referencia</name>
        <type>FOREIGN KEY (id_ref) REFERENCES referencia (id) ON DELETE CASCADE ON UPDATE CASCADE</type>
    </constraint>
    <constraint>
        <name>unique_nombre</name>
        <type>UNIQUE (nombre)</type>
    </constraint>
    
    <!-- Indices -->
    <index>
        <name>nombre</name>
        <columns>nombre</columns>
    </index>
    <index>
        <name>fecha_estado</name>
        <columns>fecha, estado</columns>
    </index>
</table>
```

### Elementos Column

#### `<name>`
Nombre de la columna.

#### `<type>`
Tipo de dato. Valores comunes:
- `serial` - Autoincremento (se convierte a BIGINT con secuencia en PostgreSQL, BIGINT AUTO_INCREMENT en MySQL)
- `integer` - Numero entero de 32 bits
- `bigint` - Numero entero de 64 bits
- `double precision` - Numero decimal doble precision
- `character varying(n)` - Cadena variable hasta n caracteres
- `char(n)` - Cadena fija n caracteres
- `text` - Texto largo sin limite
- `boolean` - Verdadero/Falso
- `date` - Solo fecha (YYYY-MM-DD)
- `time` - Solo hora (HH:MM:SS)
- `timestamp` - Fecha y hora

#### `<null>`
Si la columna puede ser nula. Valores:
- `NO` - Not null (requerido)
- `YES` (o omitir) - Nullable (opcional)

#### `<default>`
Valor por defecto:
- `true` / `false` para booleanos
- Numeros: `0`, `1`, etc.
- Cadenas: `''`, `'valor'`
- `CURRENT_TIMESTAMP` para timestamp
- Omitir para sin valor por defecto

#### `<rename>`
Si la columna fue renombrada, especifica el nombre antiguo. Util en migraciones.

```xml
<column>
    <name>nuevo_nombre</name>
    <type>varchar(100)</type>
    <rename>nombre_antiguo</rename>
</column>
```

### Elementos Constraint

#### `<name>`
Nombre de la restriccion (debe ser unico en la tabla).

#### `<type>`
Definicion SQL de la restriccion:

**PRIMARY KEY**
```xml
<type>PRIMARY KEY (idproducto)</type>
<type>PRIMARY KEY (codejercicio, codcuenta)</type>
```

**FOREIGN KEY**
```xml
<type>FOREIGN KEY (codagente) REFERENCES agentes (codagente) ON DELETE SET NULL ON UPDATE CASCADE</type>
<type>FOREIGN KEY (idproducto) REFERENCES productos (idproducto) ON DELETE RESTRICT ON UPDATE CASCADE</type>
```

Opciones ON DELETE:
- `CASCADE` - Borrar registros dependientes
- `SET NULL` - Poner nulo
- `RESTRICT` - Impedir borrado si hay dependencias
- `NO ACTION` - No hacer nada

Opciones ON UPDATE:
- `CASCADE` - Actualizar registros dependientes
- `RESTRICT` - Impedir cambio si hay dependencias
- `NO ACTION` - No hacer nada

**UNIQUE**
```xml
<type>UNIQUE (email)</type>
<type>UNIQUE (codigo, idempresa)</type>
```

### Elementos Index

#### `<name>`
Nombre del indice (sin prefijo, se agrega automaticamente `fs_`).

#### `<columns>`
Columnas a indexar (separadas por coma para indices multiples).

```xml
<index>
    <name>codagente</name>
    <columns>codagente</columns>
</index>
<index>
    <name>fecha_estado</name>
    <columns>fecha, estado</columns>
</index>
```

### Ejemplo Completo: Tabla Personalizada

```xml
<?xml version="1.0" encoding="UTF-8"?>
<table>
    <column>
        <name>id</name>
        <type>serial</type>
        <null>NO</null>
    </column>
    <column>
        <name>codigo</name>
        <type>character varying(20)</type>
        <null>NO</null>
    </column>
    <column>
        <name>descripcion</name>
        <type>text</type>
    </column>
    <column>
        <name>activo</name>
        <type>boolean</type>
        <default>true</default>
    </column>
    <column>
        <name>fecha_creacion</name>
        <type>timestamp</type>
        <default>CURRENT_TIMESTAMP</default>
    </column>
    <column>
        <name>idempresa</name>
        <type>integer</type>
        <null>NO</null>
    </column>
    
    <constraint>
        <name>mi_tabla_pkey</name>
        <type>PRIMARY KEY (id)</type>
    </constraint>
    <constraint>
        <name>fk_mi_tabla_empresas</name>
        <type>FOREIGN KEY (idempresa) REFERENCES empresas (idempresa) ON DELETE CASCADE ON UPDATE CASCADE</type>
    </constraint>
    <constraint>
        <name>uniq_codigo_empresa</name>
        <type>UNIQUE (codigo, idempresa)</type>
    </constraint>
    
    <index>
        <name>codigo</name>
        <columns>codigo</columns>
    </index>
    <index>
        <name>fecha_empresa</name>
        <columns>fecha_creacion, idempresa</columns>
    </index>
</table>
```

---

## 10. Ejemplos Practicos

### Ejemplo 1: Consulta Basica con DbQuery

```php
use FacturaScripts\Core\DbQuery;

// Obtener clientes no dados de baja
$clientes = DbQuery::table('clientes')
    ->select('codcliente, nombre, email, telefono1')
    ->whereEq('debaja', false)
    ->orderBy('nombre', 'ASC')
    ->limit(50)
    ->get();

foreach ($clientes as $cliente) {
    echo $cliente['codcliente'] . ' - ' . $cliente['nombre'] . ' (' . $cliente['email'] . ')' . PHP_EOL;
}
```

### Ejemplo 2: Busqueda Avanzada

```php
use FacturaScripts\Core\DbQuery;
use FacturaScripts\Core\Where;

$nombre = 'Jose';
$ciudad = 'Madrid';

$clientes = DbQuery::table('clientes')
    ->whereLike('nombre|razonsocial', $nombre)
    ->where([
        Where::isNotNull('email'),
        Where::orEq('ciudad', $ciudad)
    ])
    ->orderBy('nombre')
    ->get();
```

### Ejemplo 3: Agregaciones y Agrupaciones

```php
use FacturaScripts\Core\DbQuery;

// Ventas por agente en el periodo
$ventasPorAgente = DbQuery::table('facturascli')
    ->select('codagente')
    ->selectRaw('COUNT(*) as cantidad, SUM(total) as total, AVG(total) as promedio')
    ->whereBetween('fecha', '2025-01-01', '2025-12-31')
    ->whereEq('pagada', false)
    ->groupBy('codagente')
    ->having('SUM(total) > 5000')
    ->orderBy('total', 'DESC')
    ->get();

foreach ($ventasPorAgente as $row) {
    printf(
        "Agente: %s | Facturas: %d | Total: %.2f | Promedio: %.2f%n",
        $row['codagente'],
        $row['cantidad'],
        $row['total'],
        $row['promedio']
    );
}
```

### Ejemplo 4: INSERT, UPDATE, DELETE

```php
use FacturaScripts\Core\DbQuery;

// Insertar nuevo cliente
$nuevoCliente = [
    'codcliente' => '999',
    'nombre' => 'Cliente Nuevo',
    'cifnif' => '12345678A',
    'personafisica' => true,
    'debaja' => false,
    'fechaalta' => date('Y-m-d')
];

if (DbQuery::table('clientes')->insert($nuevoCliente)) {
    echo 'Cliente creado exitosamente';
}

// Actualizar cliente
DbQuery::table('clientes')
    ->whereEq('codcliente', '999')
    ->update(['email' => 'cliente@example.com', 'telefono1' => '555-1234']);

// Eliminar cliente (si es posible)
DbQuery::table('clientes')
    ->whereEq('codcliente', '999')
    ->delete();
```

### Ejemplo 5: Transacciones

```php
use FacturaScripts\Core\Base\DataBase;
use FacturaScripts\Core\DbQuery;

$db = new DataBase();
$db->connect();

try {
    $db->beginTransaction();
    
    // Crear factura
    $idfactura = DbQuery::table('facturascli')->insertGetId([
        'codigo' => 'FAC-001',
        'numero' => 1,
        'codserie' => 'A',
        'codejercicio' => '2025',
        'codcliente' => '001',
        'coddivisa' => 'EUR',
        'codpago' => '001',
        'fecha' => date('Y-m-d'),
        'nombrecliente' => 'Cliente A',
        'cifnif' => '12345678A',
        'total' => 1000
    ]);
    
    if (!$idfactura) {
        throw new Exception('No se pudo crear factura');
    }
    
    // Crear linea de factura
    DbQuery::table('lineasfacturascli')->insert([
        'idfactura' => $idfactura,
        'idproducto' => 1,
        'cantidad' => 10,
        'pvunitario' => 100,
        'pvtotal' => 1000,
        'codimpuesto' => 'IVA21'
    ]);
    
    // Actualizar stock
    DbQuery::table('stocks')
        ->whereEq('idproducto', 1)
        ->whereEq('codalmacen', 'ALM1')
        ->update(['cantidad' => 0]);  // Reduce stock
    
    $db->commit();
    echo 'Factura creada exitosamente';
    
} catch (Exception $e) {
    $db->rollback();
    echo 'Error: ' . $e->getMessage();
}
```

### Ejemplo 6: Construccion Dinamica de Consultas

```php
use FacturaScripts\Core\DbQuery;

function buscarFacturas($codcliente = null, $desde = null, $hasta = null, $minimo = null)
{
    $query = DbQuery::table('facturascli');
    
    if (!empty($codcliente)) {
        $query->whereEq('codcliente', $codcliente);
    }
    
    if (!empty($desde)) {
        $query->whereGte('fecha', $desde);
    }
    
    if (!empty($hasta)) {
        $query->whereLte('fecha', $hasta);
    }
    
    if (!empty($minimo)) {
        $query->whereGt('total', $minimo);
    }
    
    return $query
        ->orderBy('fecha', 'DESC')
        ->get();
}

// Uso
$facturas = buscarFacturas('001', '2025-01-01', '2025-03-31', 500);
```

### Ejemplo 7: Paginacion

```php
use FacturaScripts\Core\DbQuery;

class ListadoClientes
{
    private $porPagina = 20;
    
    public function getPagina($pagina = 1)
    {
        $offset = ($pagina - 1) * $this->porPagina;
        
        return DbQuery::table('clientes')
            ->whereEq('debaja', false)
            ->orderBy('nombre')
            ->limit($this->porPagina)
            ->offset($offset)
            ->get();
    }
    
    public function getTotalPaginas()
    {
        $total = DbQuery::table('clientes')
            ->whereEq('debaja', false)
            ->count();
        
        return ceil($total / $this->porPagina);
    }
}

// Uso
$listado = new ListadoClientes();

for ($i = 1; $i <= $listado->getTotalPaginas(); $i++) {
    $clientes = $listado->getPagina($i);
    echo "Pagina $i: " . count($clientes) . " registros" . PHP_EOL;
}
```

### Ejemplo 8: Comparacion entre Campos

```php
use FacturaScripts\Core\DbQuery;
use FacturaScripts\Core\Where;

// Productos con precio diferente al calculado
$discrepancias = DbQuery::table('productos')
    ->select('idproducto, referencia, precio')
    ->where([
        Where::notEq('precio', 'field:preciocoste')->useField()
    ])
    ->get();
```

### Ejemplo 9: Consultas Raw con DbQuery

```php
use FacturaScripts\Core\DbQuery;

// Usar selectRaw para expresiones complejas
$resultado = DbQuery::table('facturascli')
    ->selectRaw('
        YEAR(fecha) as año,
        MONTH(fecha) as mes,
        COUNT(*) as cantidad,
        SUM(total) as total,
        AVG(total) as promedio
    ')
    ->groupBy('YEAR(fecha), MONTH(fecha)')
    ->orderBy('año, mes', 'DESC')
    ->get();
```

### Ejemplo 10: Manejo de Migraciones

```php
use FacturaScripts\Core\DbUpdater;

// En el inicializador del plugin
public function initialize()
{
    // Actualizar estructura de tablas
    DbUpdater::createOrUpdateTable('tabla_personalizada');
    
    // O crear tabla nueva
    if (!DbUpdater::createTable('tabla_nueva')) {
        Tools::log()->error('No se pudo crear tabla', [
            '%error%' => DbUpdater::getLastError()
        ]);
    }
}
```

---

## Conclusiones

El sistema de base de datos de FacturaScripts 2025 proporciona:

1. **Abstraccion multicapa**: Permite cambiar entre MySQL y PostgreSQL sin modificar codigo
2. **Query builder fluent**: Construccion segura de consultas sin SQL raw
3. **Manejo automatico de esquema**: Sincronizacion XML-BD automatica
4. **Transacciones completas**: Control de integridad de datos
5. **Migraciones versionadas**: Cambios controlados en estructura y datos
6. **Seguridad**: Escape automatico de parametros, prevencion de inyecciones SQL

La documentacion completa de cada clase esta disponible en los archivos fuente con comentarios PHPDoc detallados.
