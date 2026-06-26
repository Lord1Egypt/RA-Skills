# Referencia Completa de Modelos FacturaScripts 2025

**Versión:** 2025.01
**Fecha:** 2026-04-12
**Lenguaje:** PHP
**Namespace base:** FacturaScripts\Core\Model

## Tabla de Contenidos

1. [Clases Base](#clases-base)
2. [Traits](#traits)
3. [Modelos de Dominio](#modelos-de-dominio)
4. [Modelos Join](#modelos-join)
5. [Relaciones entre Modelos](#relaciones-entre-modelos)
6. [Patrones Comunes](#patrones-comunes)

---

## Clases Base

### ModelCore

**Namespace:** `FacturaScripts\Core\Model\Base`
**Clase abstracta:** Sí
**Descripción:** Clase base fundamental de la que heredan todos los modelos. Proporciona acceso a la base de datos, gestión de tablas y operaciones CRUD básicas.

#### Propiedades Estáticas Protegidas
- `static DataBase $dataBase`: Conexión directa a la base de datos

#### Constantes
- `AUDIT_CHANNEL = 'audit'`: Canal para registros de auditoría
- `DATE_STYLE = 'd-m-Y'`: Formato de fecha
- `DATETIME_STYLE = 'd-m-Y H:i:s'`: Formato de fecha y hora
- `HOUR_STYLE = 'H:i:s'`: Formato de hora

#### Métodos Abstractos Requeridos
- `abstract public static function addExtension($extension);` - Añade extensiones
- `abstract public function getModelFields(): array;` - Retorna campos del modelo
- `abstract public function hasExtension($extension): bool;` - Verifica si existe extensión
- `abstract protected function loadModelFields(DataBase &$dataBase, string $tableName);` - Carga campos desde BD
- `abstract public function modelClassName(): string;` - Nombre de la clase
- `abstract protected function modelName(): string;` - Nombre del modelo
- `abstract public function pipe($name, ...$arguments);` - Ejecuta métodos de extensiones
- `abstract public function pipeFalse($name, ...$arguments): bool;` - Ejecuta hasta retornar false
- `abstract public static function primaryColumn(): string;` - Columna clave primaria
- `abstract public static function tableName(): string;` - Nombre de tabla

#### Métodos Públicos

```php
public function __construct(array $data = []);
```
Constructor que inicializa el modelo, verifica la tabla en BD y carga datos.

```php
public function changePrimaryColumnValue($newValue): bool;
```
Cambia el valor de la clave primaria.

```php
public function clear();
```
Reinicia todas las propiedades a null.

```php
public function install(): string;
```
SQL para ejecutar después de crear la tabla.

```php
public function loadFromData(array $data = [], array $exclude = []): void;
```
Asigna valores desde array, con conversión automática de tipos.

```php
public function primaryColumnValue();
```
Retorna el valor actual de la clave primaria.

```php
public function toArray(): array;
```
Convierte el modelo a array.

---

### ModelClass

**Namespace:** `FacturaScripts\Core\Model\Base`
**Extiende:** `ModelCore`
**Descripción:** Proporciona operaciones CRUD completas, búsqueda y gestión de modelos.

#### Métodos Estáticos

```php
public static function all(array $where = [], array $order = [], int $offset = 0, int $limit = 50): array;
```
Retorna array de instancias del modelo con filtros opcionales.

#### Métodos Públicos

```php
public function codeModelAll(string $fieldCode = ''): array;
```
Retorna CodeModel de todos los registros para autocompletes.

```php
public function codeModelSearch(string $query, string $fieldCode = '', array $where = []): array;
```
Busca registros por texto.

```php
public function count(array $where = []): int;
```
Cuenta registros (usa cache si no hay filtros).

```php
public function delete(): bool;
```
Elimina el registro actual.

```php
public function exists(): bool;
```
Verifica si el registro existe en BD.

```php
public function get($code);
```
Carga un registro por código primario.

```php
public function loadFromCode($code, array $where = [], array $order = []): bool;
```
Carga un registro por clave primaria.

```php
public function newCode(string $field = '', array $where = []);
```
Genera un nuevo código único.

```php
public function primaryDescriptionColumn(): string;
```
Columna usada como descripción principal.

```php
public function primaryDescription();
```
Valor de la descripción principal.

```php
public function save(): bool;
```
Guarda el modelo (INSERT o UPDATE).

```php
public function test(): bool;
```
Valida los datos del modelo.

```php
public function totalSum(string $field, array $where = []): float;
```
Suma de un campo con filtros.

```php
public function url(string $type = 'auto', string $list = 'List'): string;
```
Genera URLs para acceder al modelo ('edit', 'delete', 'list', etc).

---

### JoinModel

**Namespace:** `FacturaScripts\Core\Model\Base`
**Descripción:** Clase base para vistas de base de datos (modelos Join). Solo lectura.

#### Métodos Principales

```php
public function __construct(array $data = []);
public function all(array $where, array $order = [], int $offset = 0, int $limit = 0): array;
public function clear();
public function count(array $where = []): int;
public function delete(): bool;  // Retorna false (no soporta delete)
public function exists(): bool;
public function getModelFields(): array;
public function loadFromCode($cod, array $where = [], array $orderby = []): bool;
public function primaryColumnValue();
public function totalSum(string $field, array $where = []): float;
public function url(string $type = 'auto', string $list = 'List'): string;
```

---

## Traits

### CompanyRelationTrait

Proporciona relación con empresa para modelos multi-empresa.

```php
public $idempresa;  // ID de empresa
public function getCompany(): Empresa;  // Retorna objeto Empresa
```

**Modelos:** Cliente, Proveedor, Almacen, Usuario, Series, etc.

---

### CurrencyRelationTrait

Proporciona relación con divisa.

```php
public $coddivisa;      // Código de divisa (EUR, USD, etc.)
public $tasaconv;       // Tasa de conversión
public function setCurrency($coddivisa, $purchase = false): void;
```

**Modelos:** FacturaCliente, FacturaProveedor, Documentos de venta/compra

---

### EmailAndPhonesTrait

Proporciona propiedades de contacto.

```php
public $email;          // Email principal
public $fax;            // Número de fax
public $telefono;       // Teléfono principal
public $telefono2;      // Teléfono secundario
```

**Modelos:** Cliente, Proveedor, Empresa, Contacto

---

### ExerciseRelationTrait

Proporciona relación con ejercicio fiscal.

```php
public $codejercicio;   // Código del ejercicio
public function getExercise(string $codejercicio = ''): Ejercicio;
```

**Modelos:** Asiento, Partida, documentos contables

---

### FiscalNumberTrait

Proporciona manejo de números fiscales (NIF, CIF, etc).

```php
public $cifnif;  // Número de identificación fiscal
```

**Modelos:** Cliente, Proveedor, Empresa

---

### GravatarTrait

Proporciona integración con Gravatar.

```php
public function gravatar(int $size = 80): string;  // URL del avatar
```

**Modelos:** User, Contacto

---

### IbanTrait

Proporciona validación y manejo de IBAN.

```php
public $iban;  // Número IBAN

public function getIban(bool $spaced = false, bool $censure = false): string;
public function setDisableIbanTest(bool $value): void;
public function verifyIBAN(string $iban): bool;
```

**Modelos:** CuentaBanco, Cliente, Proveedor

---

### IntracomunitariaTrait

Soporte para operaciones intracomunitarias (UE).

```php
public function setIntracomunitaria(): bool;
```

**Modelos:** FacturaCliente, FacturaProveedor

---

### InvoiceLineTrait

Métodos para líneas de facturas con devoluciones.

```php
abstract public function hasRefundedQuantity(): bool;
public function refundedQuantity(): float;
```

**Modelos:** LineaFacturaCliente, LineaFacturaProveedor

---

### InvoiceTrait

Métodos comunes para facturas.

```php
public function delete(): bool;
public function getRefunds(): array;
public function install(): string;
public function paid(): bool;
public function parentDocuments(): array;
public static function primaryColumn(): string;
abstract public static function all(array $where = [], ...): array;
abstract public function getReceipts(): array;
abstract public function testDate(): bool;
```

**Modelos:** FacturaCliente, FacturaProveedor

---

### PaymentRelationTrait

Relación con forma de pago.

```php
public $codpago;  // Código de forma pago
public function getPaymentMethod(): FormaPago;
```

**Modelos:** FacturaCliente, FacturaProveedor, Cliente, Proveedor

---

### ProductRelationTrait

Relación con producto.

```php
public $idproducto;  // ID del producto
public function getProducto(): Producto;
```

**Modelos:** Variante, Stock, líneas de documentos

---

### SerieRelationTrait

Relación con serie de documentos.

```php
public $codserie;  // Código de serie
public function getSerie(): Serie;
```

**Modelos:** FacturaCliente, FacturaProveedor, PresupuestoCliente, etc.

---

### TaxRelationTrait

Relación con impuestos.

```php
public $codimpuesto;  // Código de impuesto
```

**Modelos:** Producto, líneas de documentos

---

### AccEntryRelationTrait

Relación con asiento contable.

```php
public function getAccountingEntry(): Asiento;
```

**Modelos:** Documentos con asiento contable

---

## Modelos de Dominio

### Maestros Basicos

#### Pais

- **Tabla:** `paises` | **PK:** `codpais`
- **Propiedades:** `codpais` (string), `nombre` (string), `codiso` (string)
- **Métodos:** `test()`, `save()`

#### Divisa

- **Tabla:** `divisas` | **PK:** `coddivisa`
- **Propiedades:** `coddivisa` (string), `nombre` (string), `simbolo` (string), `tasaconv` (float)
- **Métodos:** `test()`, `save()`

#### Almacen

- **Tabla:** `almacenes` | **PK:** `codalmacen`
- **Traits:** CompanyRelationTrait, EmailAndPhonesTrait
- **Propiedades:** `codalmacen`, `nombre`, `idempresa`, `telefono`, `email`, `provincia`, `ciudad`, `codpostal`, `direccion`, `contacto`, `pais`
- **Métodos:** `test()`, `save()`

#### Empresa

- **Tabla:** `empresas` | **PK:** `idempresa`
- **Traits:** EmailAndPhonesTrait, FiscalNumberTrait, GravatarTrait, IbanTrait
- **Propiedades:** `idempresa` (int), `nombre` (string), `nombrecorto` (string), `cifnif` (string), `direccion`, `ciudad`, `codpostal`, `provincia`, `pais`, `coddivisa`, `email`, `telefono`, `telefono2`, `fax`, `iban`, `administrador` (bool), `acreedor` (bool), `deudor` (bool)
- **Métodos:** `test()`, `save()`, `gravatar()`, `getIban()`

#### AgenciaTransporte

- **Tabla:** `agenciastransporte` | **PK:** `codagencia`
- **Propiedades:** `codagencia` (string), `nombre` (string), `web` (string), `telefono` (string)
- **Métodos:** `test()`, `save()`

---

### Clientes y Proveedores

#### Cliente

- **Tabla:** `clientes` | **PK:** `codcliente`
- **Traits:** CompanyRelationTrait, EmailAndPhonesTrait, FiscalNumberTrait, GravatarTrait, IbanTrait, PaymentRelationTrait, TaxRelationTrait
- **Propiedades:** `codcliente`, `nombre`, `nombrecorto`, `cifnif`, `codgrupo`, `email`, `telefono`, `telefono2`, `fax`, `codpago`, `iban`, `direccion`, `ciudad`, `codpostal`, `provincia`, `pais`, `idempresa`, `activo` (bool), `codimpuesto`, `recargo` (bool), `rating` (int), `actualizado`
- **Métodos:** `test()`, `save()`, `delete()`, `getContacts()`, `getInvoices()`, `getPaymentMethod()`, `getCompany()`

#### Proveedor

- **Tabla:** `proveedores` | **PK:** `codproveedor`
- **Traits:** CompanyRelationTrait, EmailAndPhonesTrait, FiscalNumberTrait, GravatarTrait, IbanTrait, PaymentRelationTrait, TaxRelationTrait
- **Propiedades:** `codproveedor`, `nombre`, `nombrecorto`, `cifnif`, `email`, `telefono`, `telefono2`, `fax`, `codpago`, `iban`, `direccion`, `ciudad`, `codpostal`, `provincia`, `pais`, `idempresa`, `activo`, `codimpuesto`, `recargo`, `rating`, `actualizado`
- **Métodos:** `test()`, `save()`, `delete()`, `getPaymentMethod()`, `getInvoices()`, `getPurchaseOrders()`

#### Contacto

- **Tabla:** `contactos` | **PK:** `idcontacto`
- **Traits:** GravatarTrait, EmailAndPhonesTrait
- **Propiedades:** `idcontacto` (int), `codcliente`, `codproveedor`, `nombre`, `apellidos`, `cargo`, `direccion`, `ciudad`, `codpostal`, `provincia`, `pais`, `email`, `telefono`, `telefono2`, `fax`, `activo` (bool)
- **Métodos:** `test()`, `save()`, `gravatar()`

#### GrupoClientes

- **Tabla:** `gruposclientes` | **PK:** `codgrupo`
- **Propiedades:** `codgrupo` (string), `nombre` (string), `porcentajebonificacion` (float)
- **Métodos:** `test()`, `save()`

---

### Productos

#### Producto

- **Tabla:** `productos` | **PK:** `idproducto`
- **Traits:** ModelTrait, TaxRelationTrait
- **Propiedades:** `idproducto` (int), `referencia` (string), `descripcion` (string), `codfamilia` (string), `codfabricante` (string), `codimpuesto` (string), `precio` (float), `preciocoste` (float), `codsubcuentaven` (string), `codsubcuentacom` (string), `codsubcuentairpfcom` (string), `excepcioniva` (string), `bloqueado` (bool), `publico` (bool), `nostock` (bool), `ventasinstock` (bool), `actualizado` (string), `fechaalta` (string), `observaciones` (string)
- **Métodos:** `test()`, `save()`, `delete()`, `getVariants()`, `getStocks()`, `getImages()`, `getManufacturer()`, `getFamily()`

#### Variante

- **Tabla:** `variantes` | **PK:** `idvariante`
- **Traits:** ProductRelationTrait
- **Propiedades:** `idvariante` (int), `idproducto` (int), `referencia` (string), `codigo` (string), `descripcion` (string), `precio` (float), `actualizado` (string)
- **Métodos:** `test()`, `save()`, `getProducto()`, `getStocks()`

#### Stock

- **Tabla:** `stocks` | **PK:** `idstock`
- **Traits:** ProductRelationTrait
- **Propiedades:** `idstock` (int), `idproducto` (int), `codalmacen` (string), `cantidad` (float), `reservada` (float), `disponible` (float), `actualizado` (string)
- **Métodos:** `test()`, `save()`, `getProducto()`, `transfer()`

#### Familia

- **Tabla:** `familias` | **PK:** `codfamilia`
- **Propiedades:** `codfamilia` (string), `nombre` (string), `madre` (string)
- **Métodos:** `test()`, `save()`

#### Fabricante

- **Tabla:** `fabricantes` | **PK:** `codfabricante`
- **Propiedades:** `codfabricante` (string), `nombre` (string), `web` (string)
- **Métodos:** `test()`, `save()`

#### Atributo

- **Tabla:** `atributos` | **PK:** `idatributo`
- **Propiedades:** `idatributo` (int), `nombre` (string), `codejercicio` (string)
- **Métodos:** `test()`, `save()`, `getValues()`

#### AtributoValor

- **Tabla:** `atributosvalores` | **PK:** `idatributovalor`
- **Propiedades:** `idatributovalor` (int), `idatributo` (int), `valor` (string)
- **Métodos:** `test()`, `save()`

#### Tarifa

- **Tabla:** `tarifas` | **PK:** `codtarifa`
- **Propiedades:** `codtarifa` (string), `nombre` (string), `descripcion` (string), `aplicar` (string), `activa` (bool)
- **Métodos:** `test()`, `save()`, `getLines()`

#### ProductoImagen

- **Tabla:** `productoimagenes` | **PK:** `idimagen`
- **Traits:** ProductRelationTrait
- **Propiedades:** `idimagen` (int), `idproducto` (int), `imagen` (blob), `mime` (string), `principal` (bool)
- **Métodos:** `test()`, `save()`, `delete()`

#### ProductoProveedor

- **Tabla:** `productosproveedores` | **PK:** `idproductoproveedor`
- **Traits:** ProductRelationTrait
- **Propiedades:** `idproductoproveedor` (int), `idproducto` (int), `codproveedor` (string), `refproveedor` (string), `precio` (float), `preciocoste` (float), `impuesto` (bool), `plazoentrega` (int), `cantidadminima` (float), `actualizado` (string)
- **Métodos:** `test()`, `save()`, `getProducto()`

---

### Documentos de Venta

#### PresupuestoCliente

- **Tabla:** `presupuestosclientes` | **PK:** `idpresupuesto`
- **Extiende:** SalesDocument
- **Traits:** CompanyRelationTrait, CurrencyRelationTrait, ExerciseRelationTrait, PaymentRelationTrait, SerieRelationTrait
- **Propiedades:** `idpresupuesto`, `codigo`, `codcliente`, `numero` (int), `fecha`, `hora`, `codserie`, `idempresa`, `coddivisa`, `codejercicio`, `codpago`, `cifnif`, `nombre`, `neto`, `totaliva`, `totalirpf`, `total`, `dtopor1`, `dtopor2`, `editable`, `observaciones`
- **Métodos:** `test()`, `save()`, `delete()`, `getLines()`, `getNewLine()`, `getNewProductLine()`, `paid()` (siempre false), `getSerie()`, `getCompany()`, `getPaymentMethod()`, `url()`

#### PedidoCliente

- **Tabla:** `pedidosclientes` | **PK:** `idpedido`
- **Extiende:** SalesDocument
- **Propiedades:** `idpedido`, `codigo`, `codcliente`, `numero`, `fecha`, `hora`, `codserie`, `idempresa`, `coddivisa`, `codejercicio`, `codpago`, `neto`, `totaliva`, `totalirpf`, `total`, `editable`, `idestado`, `observaciones`
- **Métodos:** `test()`, `save()`, `delete()`, `getLines()`, `getNewLine()`, `paid()`, `getSerie()`, `getPaymentMethod()`

#### AlbaranCliente

- **Tabla:** `albaranesclientes` | **PK:** `idalbaran`
- **Extiende:** SalesDocument
- **Propiedades:** `idalbaran`, `codigo`, `codcliente`, `numero`, `fecha`, `hora`, `codserie`, `idempresa`, `coddivisa`, `codejercicio`, `codpago`, `neto`, `totaliva`, `totalirpf`, `total`, `editable`, `idestado`, `observaciones`
- **Métodos:** `test()`, `save()`, `delete()`, `getLines()`, `getNewLine()`, `paid()`, `parentDocuments()`

#### FacturaCliente

- **Tabla:** `facturascli` | **PK:** `idfactura`
- **Extiende:** SalesDocument
- **Traits:** CompanyRelationTrait, CurrencyRelationTrait, ExerciseRelationTrait, PaymentRelationTrait, SerieRelationTrait, InvoiceTrait
- **Propiedades:** `idfactura` (int), `codigo` (string), `codcliente` (string), `numero` (int), `numero2` (string), `fecha` (string), `hora` (string), `codserie` (string), `idempresa` (int), `coddivisa` (string), `codejercicio` (string), `codpago` (string), `idasiento` (int), `neto` (float), `totaliva` (float), `totalirpf` (float), `total` (float), `pagada` (bool), `femail` (string), `editable` (bool), `observaciones` (string)
- **Métodos:** `test()`, `save()`, `delete()`, `getLines()`, `getNewLine()`, `getNewProductLine()`, `getReceipts()`, `paid()`, `getRefunds()`, `parentDocuments()`, `getSerie()`, `getPaymentMethod()`, `getCompany()`, `url()`

#### LineaPresupuestoCliente

- **Tabla:** `lineaspresupuestosclientes` | **PK:** `idlinea`
- **Extiende:** SalesDocumentLine
- **Propiedades:** `idlinea`, `idpresupuesto`, `idproducto`, `referencia`, `descripcion`, `cantidad` (float), `pvpunitario` (float), `pvptotal` (float), `codimpuesto`, `iva`, `irpf`, `recargo`, `dtopor`, `orden` (int)
- **Métodos:** `test()`, `save()`, `delete()`, `getDocument()`, `documentColumnValue()`

#### LineaPedidoCliente

- **Tabla:** `lineaspedidosclientes` | **PK:** `idlinea`
- **Extiende:** SalesDocumentLine
- **Propiedades:** `idlinea`, `idpedido`, `idproducto`, `referencia`, `descripcion`, `cantidad`, `pvpunitario`, `pvptotal`, `codimpuesto`, `iva`, `irpf`, `recargo`, `dtopor`, `orden`

#### LineaAlbaranCliente

- **Tabla:** `lineasalbaranesclientes` | **PK:** `idlinea`
- **Extiende:** SalesDocumentLine
- **Propiedades:** `idlinea`, `idalbaran`, `idproducto`, `referencia`, `descripcion`, `cantidad`, `pvpunitario`, `pvptotal`, `codimpuesto`, `iva`, `irpf`, `recargo`, `dtopor`, `orden`

#### LineaFacturaCliente

- **Tabla:** `lineasfacturascli` | **PK:** `idlinea`
- **Extiende:** SalesDocumentLine, InvoiceLineTrait
- **Propiedades:** `idlinea`, `idfactura`, `idproducto`, `referencia`, `descripcion`, `cantidad`, `pvpunitario`, `pvptotal`, `codimpuesto`, `iva`, `irpf`, `recargo`, `dtopor`, `orden`, `cantidadrect` (float), `idlineadevo` (int)
- **Métodos:** `test()`, `save()`, `delete()`, `getDocument()`, `documentColumnValue()`, `hasRefundedQuantity()`, `refundedQuantity()`

---

### Documentos de Compra

#### PresupuestoProveedor

- **Tabla:** `presupuestosproveedores` | **PK:** `idpresupuesto`
- **Extiende:** PurchaseDocument
- **Propiedades:** `idpresupuesto`, `codigo`, `codproveedor`, `numero`, `fecha`, `neto`, `totaliva`, `total`
- **Métodos:** `test()`, `save()`, `getLines()`, `getNewLine()`

#### PedidoProveedor

- **Tabla:** `pedidosproveedores` | **PK:** `idpedido`
- **Extiende:** PurchaseDocument
- **Propiedades:** `idpedido`, `codigo`, `codproveedor`, `numero`, `fecha`, `neto`, `totaliva`, `total`

#### AlbaranProveedor

- **Tabla:** `albaranesproveedores` | **PK:** `idalbaran`
- **Extiende:** PurchaseDocument
- **Propiedades:** `idalbaran`, `codigo`, `codproveedor`, `numero`, `fecha`, `neto`, `totaliva`, `total`

#### FacturaProveedor

- **Tabla:** `facturasprov` | **PK:** `idfactura`
- **Extiende:** PurchaseDocument
- **Traits:** InvoiceTrait
- **Propiedades:** `idfactura`, `codigo`, `codproveedor`, `numero`, `fecha`, `neto`, `totaliva`, `totalirpf`, `total`, `pagada`, `idasiento`
- **Métodos:** `test()`, `save()`, `delete()`, `getLines()`, `getReceipts()`, `paid()`, `parentDocuments()`

#### LineaFacturaProveedor

- **Tabla:** `lineasfacturasprov` | **PK:** `idlinea`
- **Extiende:** PurchaseDocumentLine, InvoiceLineTrait
- **Propiedades:** `idlinea`, `idfactura`, `idproducto`, `referencia`, `descripcion`, `cantidad`, `pvpunitario`, `pvptotal`, `codimpuesto`, `iva`, `irpf`, `recargo`, `dtopor`, `orden`

---

### Pagos y Recibos

#### ReciboCliente

- **Tabla:** `reciboscli` | **PK:** `idrecibo`
- **Propiedades:** `idrecibo` (int), `idfactura` (int), `codcliente` (string), `numero` (int), `fecha` (string), `fechavencimiento` (string), `codpago` (string), `codigo` (string), `importe` (float), `pagado` (bool), `fechapago` (string), `irpf` (float)
- **Métodos:** `test()`, `save()`, `delete()`

#### PagoCliente

- **Tabla:** `pagoscli` | **PK:** `idpago`
- **Propiedades:** `idpago` (int), `codcliente` (string), `fecha` (string), `importe` (float), `codpago` (string), `coddivisa` (string), `numero` (string), `observaciones` (string)
- **Métodos:** `test()`, `save()`

#### ReciboProveedor

- **Tabla:** `recibosprov` | **PK:** `idrecibo`
- **Propiedades:** `idrecibo`, `idfactura`, `codproveedor`, `numero`, `fecha`, `fechavencimiento`, `codpago`, `codigo`, `importe`, `pagado`

#### PagoProveedor

- **Tabla:** `pagosprov` | **PK:** `idpago`
- **Propiedades:** `idpago`, `codproveedor`, `fecha`, `importe`, `codpago`, `coddivisa`, `numero`

---

### Contabilidad

#### Ejercicio

- **Tabla:** `ejercicios` | **PK:** `codejercicio`
- **Traits:** CompanyRelationTrait
- **Propiedades:** `codejercicio` (string), `nombre` (string), `fechainicio` (string), `fechafin` (string), `idempresa` (int), `estado` (string), `plancontable` (string)
- **Métodos:** `test()`, `save()`, `isOpen()`, `close()`, `getAccounts()`

#### Cuenta

- **Tabla:** `cuentas` | **PK:** `idcuenta`
- **Traits:** CompanyRelationTrait
- **Propiedades:** `idcuenta` (int), `codejercicio` (string), `idempresa` (int), `codcuenta` (string), `descripcion` (string), `tipo` (string)
- **Métodos:** `test()`, `save()`, `getSubaccounts()`, `getBalance()`

#### Subcuenta

- **Tabla:** `subcuentas` | **PK:** `idsubcuenta`
- **Traits:** CompanyRelationTrait, TaxRelationTrait
- **Propiedades:** `idsubcuenta` (int), `codejercicio` (string), `idcuenta` (int), `codsubcuenta` (string), `descripcion` (string), `debe` (float), `haber` (float), `saldo` (float), `idempresa` (int)
- **Métodos:** `test()`, `save()`, `getBalance()`, `getMovements()`

#### CuentaEspecial

- **Tabla:** `cuentasespeciales` | **PK:** `idcuentaespecial`
- **Traits:** CompanyRelationTrait
- **Propiedades:** `idcuentaespecial` (int), `idempresa` (int), `codejercicio` (string), `codcuentaespecial` (string), `codsubcuenta` (string), `descripcion` (string)
- **Descripción:** Mapea cuentas a propósitos especiales (CAJA, BANCO, IVA, etc.)

#### Asiento

- **Tabla:** `asientos` | **PK:** `idasiento`
- **Traits:** CompanyRelationTrait, ExerciseRelationTrait
- **Propiedades:** `idasiento` (int), `numero` (int), `codejercicio` (string), `idempresa` (int), `fecha` (string), `concepto` (string), `importe` (float), `iddiario` (int), `editable` (bool)
- **Métodos:** `test()`, `save()`, `delete()`, `getLines()`, `getNewLine()`, `isBalanced()`

#### Partida

- **Tabla:** `partidas` | **PK:** `idpartida`
- **Traits:** ExerciseRelationTrait
- **Propiedades:** `idpartida` (int), `idasiento` (int), `codsubcuenta` (string), `concepto` (string), `debe` (float), `haber` (float), `contrapartida` (string), `concepto2` (string), `coddivisa` (string), `tasaconv` (float), `documento` (string), `numero` (string)
- **Métodos:** `test()`, `save()`, `delete()`, `getEntry()`

#### Diario

- **Tabla:** `diarios` | **PK:** `iddiario`
- **Propiedades:** `iddiario` (int), `codigo` (string), `descripcion` (string), `tipo` (string), `editable` (bool)

---

### Impuestos

#### Impuesto

- **Tabla:** `impuestos` | **PK:** `codimpuesto`
- **Propiedades:** `codimpuesto` (string), `descripcion` (string), `tipo` (string), `porcentaje` (float)
- **Métodos:** `test()`, `save()`, `getZones()`

#### ImpuestoZona

- **Tabla:** `impuestoszonas` | **PK:** `idimpuestozona`
- **Propiedades:** `idimpuestozona` (int), `codimpuesto` (string), `codigopais` (string), `porcentaje` (float)

#### Retencion

- **Tabla:** `retenciones` | **PK:** `codretencion`
- **Propiedades:** `codretencion` (string), `descripcion` (string), `porcentaje` (float), `tipo` (string)

---

### Configuracion

#### Serie

- **Tabla:** `series` | **PK:** `codserie`
- **Traits:** CompanyRelationTrait
- **Propiedades:** `codserie` (string), `descripcion` (string), `idempresa` (int), `numfactura` (int), `numfacturaproveedor` (int), `numalbaran` (int), `numalbaran2` (int), `numpedido` (int), `numpedido2` (int), `numbudget` (int), `numbudget2` (int), `numorden` (int), `codejercicio` (string), `codalmacen` (string)
- **Métodos:** `test()`, `save()`, `getNextNumber()`

#### FormaPago

- **Tabla:** `formas_pago` | **PK:** `codpago`
- **Propiedades:** `codpago` (string), `descripcion` (string), `tipo` (string), `codcuentaesp` (string), `genbancos` (bool), `gencuentas` (bool), `plazo` (int), `domiciliacion` (bool)

#### Settings

- **Tabla:** `settings` | **PK:** `id`
- **Propiedades:** `id` (string), `valor` (string)
- **Descripción:** Almacena configuraciones generales del sistema

#### CronJob

- **Tabla:** `cronjobs` | **PK:** `id`
- **Propiedades:** `id` (string), `task` (string), `lastrun` (string), `nextrun` (string), `periodo` (int), `activo` (bool)

---

### Usuarios y Permisos

#### User

- **Tabla:** `users` | **PK:** `id`
- **Traits:** GravatarTrait, EmailAndPhonesTrait
- **Propiedades:** `id` (string), `nombre` (string), `email` (string), `telefono` (string), `contrasenia` (string), `admin` (bool), `activo` (bool), `idempresa` (int), `codalmacen` (string), `language` (string), `theme` (string), `token` (string)
- **Métodos:** `test()`, `save()`, `setPassword()`, `verifyPassword()`, `gravatar()`, `getRoles()`

#### Role

- **Tabla:** `roles` | **PK:** `codrole`
- **Propiedades:** `codrole` (string), `descripcion` (string)
- **Métodos:** `test()`, `save()`, `getAccess()`

#### RoleAccess

- **Tabla:** `rol_access` | **PK:** `id`
- **Propiedades:** `id` (int), `codrole` (string), `pagename` (string), `allowdelete` (bool), `allowupdate` (bool), `allowinsert` (bool)

#### RoleUser

- **Tabla:** `rol_user` | **PK:** `id`
- **Propiedades:** `id` (int), `codrole` (string), `user` (string)

---

### API

#### ApiKey

- **Tabla:** `apikeys` | **PK:** `id`
- **Propiedades:** `id` (string), `user` (string), `apikey` (string), `activo` (bool), `fechaalta` (string), `ultimouso` (string)

#### ApiAccess

- **Tabla:** `apiaccess` | **PK:** `id`
- **Propiedades:** `id` (int), `idapikey` (int), `modelname` (string), `allowget` (bool), `allowpost` (bool), `allowput` (bool), `allowdelete` (bool)

---

### Paginas

#### Page

- **Tabla:** `pages` | **PK:** `name`
- **Propiedades:** `name` (string), `title` (string), `icon` (string), `menu` (string), `ordernum` (int), `showonmenu` (bool)

#### PageFilter

- **Tabla:** `pagefilters` | **PK:** `id`
- **Propiedades:** `id` (int), `pagename` (string), `name` (string), `description` (string), `filterquery` (string), `user` (string), `shared` (bool)

#### PageOption

- **Tabla:** `pageoptions` | **PK:** `id`
- **Propiedades:** `id` (int), `pagename` (string), `user` (string), `columnorder` (text), `hiddencolumns` (text)

---

### Archivos

#### AttachedFile

- **Tabla:** `attached_files` | **PK:** `id`
- **Propiedades:** `id` (int), `filename` (string), `filepath` (string), `mimetype` (string), `size` (int), `uploadtime` (string), `uploader` (string)

#### AttachedFileRelation

- **Tabla:** `attached_file_relation` | **PK:** `id`
- **Propiedades:** `id` (int), `idfile` (int), `modelname` (string), `modelid` (string)

---

### Notificaciones

#### LogMessage

- **Tabla:** `logmessages` | **PK:** `id`
- **Propiedades:** `id` (int), `channel` (string), `level` (string), `message` (string), `context` (text), `time` (string)

#### WorkEvent

- **Tabla:** `workevents` | **PK:** `id`
- **Propiedades:** `id` (int), `user` (string), `modelname` (string), `modelid` (string), `operation` (string), `created` (bool), `timestamp` (string)

#### EmailNotification

- **Tabla:** `emailnotifications` | **PK:** `id`
- **Propiedades:** `id` (int), `user` (string), `modelname` (string), `modelid` (string), `subject` (string), `body` (text), `sent` (bool), `sendtime` (string)

#### EmailSent

- **Tabla:** `emailsent` | **PK:** `id`
- **Propiedades:** `id` (int), `model` (string), `modelid` (string), `to` (string), `subject` (string), `body` (text), `date` (string), `user` (string)

---

### Transformacion

#### DocTransformation

- **Tabla:** `doctransformations` | **PK:** `id`
- **Propiedades:** `id` (int), `origintype` (string), `originid` (int), `desttype` (string), `destid` (int)
- **Descripción:** Mapea relaciones entre documentos (ej: presupuesto -> pedido -> factura)

---

### Cuentas Banco

#### CuentaBanco

- **Tabla:** `cuentasbanco` | **PK:** `idcuenta`
- **Traits:** CompanyRelationTrait, IbanTrait
- **Propiedades:** `idcuenta` (int), `descripcion` (string), `iban` (string), `swift` (string), `entidad` (string), `oficina` (string), `cuenta` (string), `digitos` (string), `codsubcuenta` (string), `idempresa` (int), `activo` (bool), `saldo` (float)
- **Métodos:** `test()`, `save()`, `getIban()`

#### CuentaBancoCliente

- **Tabla:** `cuentasbancoclientes` | **PK:** `id`
- **Propiedades:** `id` (int), `codcliente` (string), `iban` (string), `entidad` (string), `swift` (string)

#### CuentaBancoProveedor

- **Tabla:** `cuentasbancoproveedor` | **PK:** `id`
- **Propiedades:** `id` (int), `codproveedor` (string), `iban` (string), `entidad` (string), `swift` (string)

---

## Modelos Join

Los modelos Join representan vistas SQL que combinan datos de múltiples tablas. Son solo lectura (no soportan INSERT, UPDATE, DELETE).

### FacturaClienteProducto

Vista que combina: FacturaCliente + LineaFacturaCliente + Producto

Campos calculados: `idfactura`, `codigo_factura`, `fecha`, `referencia`, `descripcion`, `cantidad`, `pvpunitario`, `pvptotal`, `codcliente`, `nombre_cliente`

### AlbaranClienteProducto

Vista que combina: AlbaranCliente + LineaAlbaranCliente + Producto

### FacturaProveedorProducto

Vista que combina: FacturaProveedor + LineaFacturaProveedor + Producto

### AlbaranProveedorProducto

Vista que combina: AlbaranProveedor + LineaAlbaranProveedor + Producto

### StockProducto

Vista que combina: Producto + Stock + Almacen

Campos: `referencia`, `descripcion`, `codalmacen`, `nombre_almacen`, `cantidad`, `reservada`, `disponible`

### VarianteProducto

Vista que combina: Producto + Variante

### TarifaProducto

Vista que combina: Tarifa + líneas de tarifa + Producto

### PartidaAsiento

Vista que combina: Asiento + Partida + Subcuenta

Campos: `idasiento`, `numero`, `fecha`, `concepto`, `codsubcuenta`, `descripcion_subcuenta`, `debe`, `haber`

### SubcuentaSaldo

Subcuentas con saldos calculados

Campos: `codsubcuenta`, `descripcion`, `saldo_inicial`, `debe`, `haber`, `saldo_final`

### SalesDocLineAccount

Líneas de venta con información contable

### PurchasesDocLineAccount

Líneas de compra con información contable

### PurchasesDocIrpfAccount

Documentos de compra con cuentas IRPF

---

## Relaciones entre Modelos

### Estructura Jerárquica Principal

```
Empresa
├── Almacen (1:N)
├── CuentaBanco (1:N)
├── Serie (1:N)
├── Ejercicio (1:N)
└── Usuario (default)

Cliente (1:N con Contacto, FacturaCliente, etc.)
├── Contacto (1:N)
├── FacturaCliente (1:N)
│   ├── LineaFacturaCliente (1:N)
│   ├── Producto (N:1)
│   └── ReciboCliente (1:N)
├── AlbaranCliente (1:N)
├── PedidoCliente (1:N)
└── PresupuestoCliente (1:N)

Producto
├── Variante (1:N)
├── Stock (1:N - uno por almacén)
├── ProductoImagen (1:N)
├── ProductoProveedor (1:N)
├── Familia (N:1)
├── Fabricante (N:1)
├── Tarifa (N:M implícito)
└── Impuesto (N:1)

Ejercicio
├── Cuenta (1:N)
│   └── Subcuenta (1:N)
└── Asiento (1:N)
    └── Partida (1:N)
```

### Relaciones Clave

- **1-1:** Usuario -> Empresa (por defecto)
- **1-N:** Empresa -> Almacén, Cliente -> Factura, Producto -> Stock
- **N-M:** Usuario -> Role (via RoleUser)
- **Jerárquica:** Familia -> Familia (madre), Cuenta -> Subcuenta

---

## Patrones Comunes

### Crear un Nuevo Modelo

```php
<?php
namespace FacturaScripts\Core\Model;

use FacturaScripts\Core\Model\Base\ModelClass;
use FacturaScripts\Core\Model\Base\ModelTrait;

class MiModelo extends ModelClass
{
    use ModelTrait;

    public $idmimodelo;
    public $codigo;
    public $nombre;
    public $activo;

    public static function tableName(): string
    {
        return 'mimodelo';
    }

    public static function primaryColumn(): string
    {
        return 'idmimodelo';
    }

    public function primaryDescriptionColumn(): string
    {
        return 'nombre';
    }

    public function test(): bool
    {
        if (empty($this->codigo)) {
            $this->toolBox()->i18nLog()->error('codigo-required');
            return false;
        }
        return parent::test();
    }

    public function save(): bool
    {
        if (!$this->test()) {
            return false;
        }
        $this->codigo = mb_strtoupper($this->codigo);
        return parent::save();
    }
}
```

### Obtener y Guardar Registros

```php
// Obtener todos
$modelos = MiModelo::all(['activo' => true], ['nombre' => 'ASC']);

// Obtener uno
$modelo = new MiModelo();
if ($modelo->get('CODIGO001')) {
    echo $modelo->nombre;
}

// Crear
$modelo = new MiModelo();
$modelo->codigo = 'NEW001';
$modelo->nombre = 'Nuevo';
if ($modelo->test() && $modelo->save()) {
    echo "Guardado: " . $modelo->idmimodelo;
}

// Actualizar
$modelo->nombre = 'Actualizado';
$modelo->save();

// Eliminar
$modelo->delete();

// Buscar
$resultados = $modelo->codeModelSearch('buscar');
$total = $modelo->count(['activo' => true]);
```

### Trabajar con Relaciones

```php
// Obtener cliente de factura
$factura = new FacturaCliente();
$factura->get('FAC001');
$cliente = $factura->getSubject();

// Obtener líneas
$lineas = $factura->getLines();
foreach ($lineas as $linea) {
    $producto = $linea->getProducto();
}

// Obtener empresa
$serie = $factura->getSerie();
$empresa = $serie->getCompany();

// Obtener forma de pago
$pago = $factura->getPaymentMethod();
```

### Transacciones Contables

```php
$asiento = new Asiento();
$asiento->codejercicio = '2025';
$asiento->fecha = date('d-m-Y');
$asiento->concepto = 'Factura venta';
$asiento->idempresa = 1;

// Línea debe
$linea1 = $asiento->getNewLine();
$linea1->codsubcuenta = '7000000';
$linea1->debe = 100.00;

// Línea haber
$linea2 = $asiento->getNewLine();
$linea2->codsubcuenta = '4300000';
$linea2->haber = 100.00;

if ($asiento->isBalanced() && $asiento->save()) {
    echo "Asiento guardado";
}
```

---

**Fin de Referencia Completa de Modelos FacturaScripts 2025**
