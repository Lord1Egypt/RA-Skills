# Referencia Completa del Sistema de Librerías - FacturaScripts 2025

## Tabla de Contenidos

1. [Sistema de Exportacion](#sistema-de-exportacion)
2. [Sistema PDF](#sistema-pdf)
3. [Sistema de Email](#sistema-de-email)
4. [Sistema de Importacion](#sistema-de-importacion)
5. [Sistema de Contabilidad](#sistema-de-contabilidad)
6. [Sistema Mod (Modificadores)](#sistema-mod-modificadores)
7. [Sistema de Workers (Cola de Trabajos)](#sistema-de-workers-cola-de-trabajos)

---

## Sistema de Exportacion

### Descripcion General

El sistema de exportacion permite exportar datos de modelos de FacturaScripts a diferentes formatos: CSV, XLS, PDF y Email. Cada exportador extiende la clase `ExportBase` y proporciona métodos especializados para cada formato.

### Clase Base: ExportBase

**Namespace:** `FacturaScripts\Core\Lib\Export`

**Propiedades Protegidas:**
- `$fileName: string` - Nombre del archivo a exportar

**Métodos Abstractos:**
- `addBusinessDocPage($model): bool` - Añade una página con datos de documento de negocio
- `addListModelPage($model, $where, $order, $offset, $columns, $title = ''): bool` - Añade tabla con listado de modelos
- `addModelPage($model, $columns, $title = ''): bool` - Añade página con datos de un modelo
- `addTablePage($headers, $rows, $options = [], $title = ''): bool` - Añade página con tabla genérica
- `getDoc()` - Devuelve el documento completo generado
- `newDoc(string $title, int $idformat, string $langcode)` - Crea nuevo documento en blanco
- `setOrientation(string $orientation)` - Establece orientacion de página
- `show(Response &$response)` - Establece headers y envía contenido a respuesta

**Métodos Protegidos:**
- `getColumnAlignments(array $columns): array` - Obtiene alineaciones de columnas
- `getColumnTitles(array $columns): array` - Obtiene títulos de columnas
- `getColumnWidgets(array $columns): array` - Obtiene widgets de columnas
- `getCursorData(array $cursor, array $columns): array` - Obtiene datos de cursor con formato de widgets
- `getCursorRawData(array $cursor, array $fields = []): array` - Obtiene datos crudos de cursor
- `getDocumentFormat($model): FormatoDocumento` - Obtiene formato de documento aplicable
- `getModelColumnsData(mixed $model, array $columns): array` - Obtiene datos de modelo con títulos
- `getModelFields($model): array` - Obtiene campos del modelo
- `getFileName(): string` - Obtiene nombre de archivo
- `setFileName(string $name)` - Establece nombre de archivo

### Clase CSVExport

**Namespace:** `FacturaScripts\Core\Lib\Export`

**Constantes:**
- `LIST_LIMIT = 1000` - Límite de registros por lote

**Propiedades:**
- `$csv: array` - Datos CSV en array
- `$delimiter: string` - Delimitador de texto (por defecto `"`)
- `$separator: string` - Separador de campos (por defecto `;`)

**Métodos Públicos:**
- `addBusinessDocPage($model): bool` - Exporta documento de negocio con líneas
- `addListModelPage($model, $where, $order, $offset, $columns, $title = ''): bool` - Exporta listado de modelos
- `addModelPage($model, $columns, $title = ''): bool` - Exporta modelo individual
- `addTablePage($headers, $rows, $options = [], $title = ''): bool` - Exporta tabla genérica
- `getDelimiter(): string` - Obtiene delimitador actual
- `getDoc(): string` - Devuelve contenido CSV completo
- `getSeparator(): string` - Obtiene separador actual
- `newDoc(string $title, int $idformat, string $langcode)` - Inicializa documento CSV
- `setDelimiter(string $del)` - Establece delimitador
- `setOrientation(string $orientation)` - No implementado para CSV
- `setSeparator(string $sep)` - Establece separador
- `show(Response &$response)` - Envía archivo CSV a respuesta
- `writeData(array $data, array $fields = [])` - Escribe datos en CSV

**Métodos Privados:**
- `writeHeader(array $fields)` - Escribe fila de encabezado

### Clase XLSExport

**Namespace:** `FacturaScripts\Core\Lib\Export`

**Constantes:**
- `LIST_LIMIT = 5000` - Límite de registros por lote

**Propiedades:**
- `$numSheets: int` - Número de hojas creadas
- `$writer: XLSXWriter` - Objeto escritor XLSX

**Métodos Públicos:**
- `addBusinessDocPage($model): bool` - Exporta documento con sus líneas en hojas separadas
- `addListModelPage($model, $where, $order, $offset, $columns, $title = ''): bool` - Exporta listado con paginacion
- `addModelPage($model, $columns, $title = ''): bool` - Exporta modelo individual
- `addTablePage($headers, $rows, $options = [], $title = ''): bool` - Exporta tabla genérica
- `getDoc(): string` - Devuelve contenido XLSX
- `newDoc(string $title, int $idformat, string $langcode)` - Inicializa documento XLSX
- `setOrientation(string $orientation)` - No implementado para XLS
- `show(Response &$response)` - Envía archivo XLSX a respuesta

**Métodos Protegidos:**
- `getColumnHeaders(array $columns): array` - Obtiene tipos de columnas para XLSX
- `getCursorRawData(array $cursor, array $fields = []): array` - Obtiene datos y aplica fixHtml
- `getModelHeaders($model): array` - Obtiene tipos de datos de campos del modelo

### Clase PDFExport

**Namespace:** `FacturaScripts\Core\Lib\Export`

Extiende: `PDFDocument`

**Constantes:**
- `LIST_LIMIT = 500` - Límite de registros por lote

**Métodos Públicos:**
- `addBusinessDocPage($model): bool` - Exporta documento de negocio con encabezado, cuerpo y pie
- `addListModelPage($model, $where, $order, $offset, $columns, $title = ''): bool` - Exporta listado en tablas
- `addModelPage($model, $columns, $title = ''): bool` - Exporta modelo individual
- `addTablePage($headers, $rows, $options = [], $title = ''): bool` - Exporta tabla con cabecera
- `getDoc(): mixed` - Devuelve documento PDF generado
- `newDoc(string $title, int $idformat, string $langcode)` - Inicializa documento PDF
- `setCompany(int $idempresa): void` - Establece empresa e inserta encabezado
- `show(Response &$response)` - Envía PDF a respuesta

### Clase MAILExport

**Namespace:** `FacturaScripts\Core\Lib\Export`

Extiende: `PDFExport`

**Propiedades:**
- `$sendParams: array` - Parámetros para envío de correo

**Métodos Públicos:**
- `addBusinessDocPage($model): bool` - Prepara documento para envío por correo
- `addModelPage($model, $columns, $title = ''): bool` - Prepara modelo para envío
- `show(Response &$response)` - Genera PDF temporal y redirige a SendMail

**Constantess:**
- `ATTACHMENTS_TMP_PATH = 'MyFiles/Tmp/Email/'` - Ruta de archivos temporales

### Clase AsientoExport

**Namespace:** `FacturaScripts\Core\Lib\Export`

**Métodos Públicos Estáticos:**
- `show(Asiento $asiento, string $option, string $title, int $idformat, string $langcode, &$response): void` - Exporta asiento contable con líneas, impuestos y totales

**Métodos Privados Estáticos:**
- `addLines(Asiento $asiento, ExportManager $exportManager): void` - Añade tabla de líneas del asiento
- `addTaxData(Asiento $asiento, ExportManager $exportManager)` - Añade tabla de datos de IVA
- `addTotals(ExportManager &$exportManager)` - Añade tabla de totales
- `hasVatRegister(Partida &$line): bool` - Verifica si la línea tiene registro de IVA

**Propiedades Estáticas Privadas:**
- `$debe: float` - Total debe acumulado
- `$haber: float` - Total haber acumulado
- `$saldo: float` - Saldo acumulado

---

## Sistema PDF

### Clase PDFCore

**Namespace:** `FacturaScripts\Core\Lib\PDF`

Extiende: `ExportBase`

**Constantes:**
- `CONTENT_X = 30` - Posición X para escribir contenido
- `FONT_SIZE = 9` - Tamaño de fuente base
- `FOOTER_Y = 10` - Posición Y del pie de página
- `MAX_TITLE_LEN = 12` - Longitud máxima de títulos

**Propiedades Protegidas:**
- `$i18n: Translator` - Objeto traductor
- `$insertedHeader: bool` - Indica si se ha insertado encabezado
- `$pdf: Cezpdf` - Objeto PDF
- `$tableWidth: float` - Ancho disponible para tablas

**Métodos Públicos:**
- `getOrientation(): string` - Obtiene orientación actual
- `newPage(string $orientation = 'portrait', bool $forceNewPage = false)` - Crea nueva página
- `setOrientation(string $orientation)` - Establece orientación

**Métodos Protegidos:**
- `addImageFromAttachedFile(AttachedFile $file, $xPos, $yPos, $width, $height)` - Añade imagen de archivo adjunto
- `addImageFromFile(string $filePath, $xPos, $yPos, $width, $height)` - Añade imagen de archivo
- `calcImageSize(string $filePath): array` - Calcula tamaño de imagen
- `fixValue(string $value): string` - Limpia valores especiales (€, etc)
- `getTableData(array $cursor, array $tableCols, array $tableOptions): array` - Extrae datos de cursor
- `insertParallelTable(array $tableData, string $title = '', array $options = [])` - Inserta tabla con 2 columnas clave/valor
- `newLine()` - Añade línea horizontal
- `newLongTitles(array &$titles, array $columns)` - Añade descripción de títulos largos
- `parallelTableData(array $table, string $colName1 = 'key', string $colName2 = 'value', string $finalColName1 = 'data1', string $finalColName2 = 'data2'): array` - Transforma tabla a 2 columnas
- `removeEmptyCols(array &$tableData, array &$tableColsTitle, $customEmptyValue = '0')` - Elimina columnas vacías
- `removeLongTitles(array &$longTitles, array &$titles)` - Reemplaza títulos largos por referencias numeradas
- `setTableColumns(array &$columns, array &$tableCols, array &$tableColsTitle, array &$tableOptions)` - Configura columnas de tabla

### Clase PDFDocument

**Namespace:** `FacturaScripts\Core\Lib\PDF`

Extiende: `PDFCore`

**Constantes:**
- `INVOICE_TOTALS_Y = 200` - Posición Y para totales de factura

**Propiedades Protegidas:**
- `$format: FormatoDocumento` - Formato de documento aplicado

**Métodos Protegidos:**
- `combineAddress($model): string` - Combina dirección con datos adicionales
- `getDocAddress($subject, $model): string` - Obtiene dirección apropiada de documento
- `getBankData($receipt): string` - Obtiene información bancaria de recibo
- `getCountryName($code): string` - Obtiene nombre de país
- `getDivisaName($code): string` - Obtiene nombre de divisa
- `getLineHeaders(): array` - Obtiene encabezados de líneas de documento
- `getTaxesRows($model)` - Obtiene filas de impuestos con cálculos
- `insertBusinessDocBody($model)` - Inserta cuerpo con líneas del documento
- `insertBusinessDocFooter($model)` - Inserta pie con observaciones, impuestos y totales
- `insertBusinessDocHeader($model)` - Inserta encabezado con datos de documento
- `insertBusinessDocShipping($model)` - Inserta dirección de envío
- `insertCompanyLogo($idfile = 0)` - Inserta logo de empresa
- `insertFooter()` - Inserta pie de página con fecha
- `insertHeader($idempresa = null)` - Inserta encabezado con datos de empresa
- `insertInvoicePayMethod($invoice)` - Inserta forma de pago
- `insertInvoiceReceipts($invoice)` - Inserta tabla de recibos
- `renderQRimage(?string $qrImage, ?string $qrTitle, ?string $qrSubtitle, float $startX, float $startY, float $leftBlockWidth, float $rightBlockWidth): void` - Renderiza código QR
- `renderQRtext(?string $qrTitle, float $qrX, float $qrY, float $qrSize, bool $title = true): void` - Renderiza texto del QR

---

## Sistema de Email

### Clase BaseBlock

**Namespace:** `FacturaScripts\Core\Lib\Email`

**Propiedades Protegidas:**
- `$css: string` - Clase CSS
- `$footer: bool` - Indica si se renderiza en pie
- `$style: string` - Estilos inline
- `$verificode: string` - Código de verificación

**Métodos Abstractos:**
- `render(bool $footer = false): string` - Renderiza bloque como HTML

**Métodos Públicos:**
- `setVerificode(string $code): void` - Establece código de verificación

### Clase TextBlock

**Namespace:** `FacturaScripts\Core\Lib\Email`

Extiende: `BaseBlock`

**Propiedades Protegidas:**
- `$text: string` - Texto del bloque

**Constructor:**
- `__construct(string $text, string $css = '', string $style = '')`

**Métodos Públicos:**
- `render(bool $footer = false): string` - Renderiza como párrafo HTML

### Clase HtmlBlock

**Namespace:** `FacturaScripts\Core\Lib\Email`

Extiende: `BaseBlock`

**Propiedades Protegidas:**
- `$html: string` - HTML directo

**Constructor:**
- `__construct(string $html)`

**Métodos Públicos:**
- `render(bool $footer = false): string` - Devuelve HTML directamente

### Clase TableBlock

**Namespace:** `FacturaScripts\Core\Lib\Email`

Extiende: `BaseBlock`

**Propiedades Protegidas:**
- `$header: array` - Encabezados de tabla
- `$rows: array` - Filas de datos

**Constructor:**
- `__construct(array $header, array $rows, string $css = '', string $style = '')`

**Métodos Públicos:**
- `render(bool $footer = false): string` - Renderiza como tabla HTML

**Métodos Protegidos:**
- `renderHeaders(): string` - Renderiza encabezados
- `renderRows(): string` - Renderiza filas

### Clase ButtonBlock

**Namespace:** `FacturaScripts\Core\Lib\Email`

Extiende: `BaseBlock`

**Propiedades Protegidas:**
- `$label: string` - Etiqueta del botón
- `$link: string` - URL del botón

**Constructor:**
- `__construct(string $label, string $link, string $css = '', string $style = '')`

**Métodos Públicos:**
- `render(bool $footer = false): string` - Renderiza como botón HTML

**Métodos Protegidos:**
- `link(): string` - Genera URL con verificode

### Clase TitleBlock

**Namespace:** `FacturaScripts\Core\Lib\Email`

Extiende: `BaseBlock`

**Propiedades Protegidas:**
- `$text: string` - Texto del título
- `$type: string` - Tipo de etiqueta HTML (h1, h2, etc)

**Constructor:**
- `__construct(string $text, string $type = 'h2', string $css = '', string $style = '')`

**Métodos Públicos:**
- `render(bool $footer = false): string` - Renderiza como título HTML

### Clase BoxBlock

**Namespace:** `FacturaScripts\Core\Lib\Email`

Extiende: `BaseBlock`

**Propiedades Protegidas:**
- `$blocks: array` - Array de bloques anidados

**Constructor:**
- `__construct(array $blocks, string $css = '', string $style = '')`

**Métodos Públicos:**
- `render(bool $footer = false): string` - Renderiza contenedor con bloques anidados

### Clase SpaceBlock

**Namespace:** `FacturaScripts\Core\Lib\Email`

Extiende: `BaseBlock`

**Propiedades Protegidas:**
- `$height: float` - Altura en píxeles

**Constructor:**
- `__construct(float $height = 30)`

**Métodos Públicos:**
- `render(bool $footer = false): string` - Renderiza espacio vertical

### Clase NewMail

**Namespace:** `FacturaScripts\Core\Lib\Email`

**Constantes:**
- `ATTACHMENTS_TMP_PATH = 'MyFiles/Tmp/Email/'` - Ruta de archivos adjuntos temporales

**Propiedades Públicas:**
- `$empresa: Empresa` - Empresa por defecto
- `$fromEmail: string` - Email remitente
- `$fromName: string` - Nombre remitente
- `$fromNick: string` - Nick del remitente
- `$signature: string` - Firma de correo
- `$text: string` - Texto del cuerpo
- `$title: string` - Asunto del correo
- `$verificode: string` - Código de verificación generado

**Propiedades Protegidas:**
- `$footerBlocks: BaseBlock[]` - Bloques del pie de página
- `$html: string` - HTML generado
- `$lowsecure: bool` - Indica si se permite TLS bajo
- `$mail: PHPMailer` - Objeto PHPMailer
- `$mainBlocks: BaseBlock[]` - Bloques del cuerpo principal
- `$template: string` - Plantilla por defecto

**Métodos Públicos:**
- `__construct()` - Inicializa con configuracion de email
- `addMailer(string $key, string $name): void` - Añade transportista de correo personalizado
- `addAttachment(string $path, string $name): NewMail` - Añade archivo adjunto
- `addFooterBlock(BaseBlock $block): NewMail` - Añade bloque al pie
- `addMainBlock(BaseBlock $block): NewMail` - Añade bloque al cuerpo
- `bcc(string $email, string $name = ''): NewMail` - Añade email en copia oculta
- `body(string $body): NewMail` - Establece cuerpo de texto
- `canSendMail(): bool` - Verifica si se puede enviar correo
- `cc(string $email, string $name = ''): NewMail` - Añade email en copia
- `create(): NewMail` - Factoria estática
- `getAttachmentPath(?string $email, string $folder): string` - Obtiene ruta de archivos adjuntos
- `getAttachmentNames(): array` - Obtiene nombres de adjuntos
- `getAvailableMailboxes(): array` - Obtiene buzones disponibles
- `getBCCAddresses(): array` - Obtiene emails en copia oculta
- `getCCAddresses(): array` - Obtiene emails en copia
- `getMailer(): array` - Obtiene transportistas disponibles
- `getTemplate(): string` - Obtiene plantilla actual
- `getToAddresses(): array` - Obtiene destinatarios
- `replyTo(string $address, string $name = ''): NewMail` - Establece responder a
- `send(): bool` - Envía correo y registra en EmailSent
- `splitEmails(string $emails): array` - Divide string de emails
- `to(string $email, string $name = ''): NewMail` - Añade destinatario

**Métodos Estáticos Privados:**
- `buildHtml(): string` - Construye HTML a partir de bloques

### Clase MailNotifier

**Namespace:** `FacturaScripts\Core\Lib\Email`

**Métodos Públicos Estáticos:**
- `getText(string $text, array $params): string` - Reemplaza parámetros en texto
- `send(string $notificationName, string $email, string $name = '', array $params = [], array $attach = [], array $mainBlocks = [], array $footerBlocks = []): bool` - Envía notificación de email

**Métodos Protegidos Estáticos:**
- `replaceTextToBlock(DinNewMail &$newMail, array $params): void` - Reemplaza placeholders de bloques en texto

---

## Sistema de Importacion

### Clase CSVImport

**Namespace:** `FacturaScripts\Core\Lib\Import`

**Métodos Públicos Estáticos:**
- `getTableFilePath(string $table): string` - Obtiene ruta del archivo CSV para tabla
- `importFileSQL(string $table, string $filePath, bool $update = false): string` - Genera SQL INSERT desde archivo CSV
- `importTableSQL(string $table): string` - Genera SQL INSERT para tabla específica
- `updateTableSQL(string $table): string` - Genera SQL INSERT con UPDATE en duplicados

**Métodos Privados Estáticos:**
- `valueToSql(DataBase &$dataBase, string $value): string` - Convierte valor a formato SQL
- `insertOnDuplicateSql(string $sql, Csv $csv): string` - Añade lógica ON DUPLICATE según BD

**Uso Típico:**
```php
$sql = CSVImport::importFileSQL('clientes', '/ruta/archivo.csv');
$dataBase->exec($sql);
```

---

## Sistema de Contabilidad

### Clase AccountingBase

**Namespace:** `FacturaScripts\Core\Lib\Accounting`

**Propiedades Protegidas:**
- `$dataBase: DataBase` - Conexión a base de datos
- `$dateFrom: string` - Fecha inicio
- `$dateTo: string` - Fecha fin
- `$exercise: Ejercicio` - Ejercicio contable actual

**Métodos Abstractos:**
- `generate(string $dateFrom, string $dateTo, array $params = [])` - Genera proceso contable
- `getData()` - Obtiene datos del balance

**Métodos Públicos:**
- `__construct()` - Inicializa base de datos y ejercicio
- `setExercise($code)` - Carga ejercicio por código
- `setExerciseFromDate($idcompany, $date): bool` - Carga ejercicio desde fecha

**Métodos Protegidos:**
- `addToDate($date, $add): string` - Suma intervalo a fecha

### Clase AccountingClass

**Namespace:** `FacturaScripts\Core\Lib\Accounting`

Extiende: `AccountingAccounts`

**Propiedades Protegidas:**
- `$document: ModelClass` - Documento contable

**Métodos Públicos:**
- `generate($model)` - Inicializa proceso con modelo

**Métodos Protegidos:**
- `addBasicLine($accountEntry, $subaccount, $isDebit, $amount = null): bool` - Añade línea estándar
- `addLinesFromTotals($accountEntry, $totals, $isDebit, $counterpart, $accountError, $saveError): bool` - Añade grupo de líneas desde totales
- `addSurchargeLine($accountEntry, $subaccount, $counterpart, $isDebit, $values): bool` - Añade línea de recargo
- `addTaxLine($accountEntry, $subaccount, $counterpart, $isDebit, $values): bool` - Añade línea de impuesto
- `getBasicLine($accountEntry, $subaccount, $isDebit, $amount = null): Partida` - Obtiene línea estándar

### Clase InvoiceToAccounting

**Namespace:** `FacturaScripts\Core\Lib\Accounting`

Extiende: `AccountingClass`

**Propiedades Protegidas:**
- `$counterpart: Subcuenta` - Contrapartida contable
- `$document: FacturaCliente|FacturaProveedor` - Documento
- `$subtotals: array` - Subtotales por línea

**Métodos Públicos:**
- `generate($model)` - Genera asientos contables para factura

**Métodos Protegidos:**
- `addCustomerLine(Asiento $entry): bool` - Añade línea de cliente
- `addGoodsPurchaseLine(Asiento $entry): bool` - Añade línea de compra de bienes
- `addGoodsSalesLine(Asiento $entry): bool` - Añade línea de venta de bienes
- `addPurchaseIrpfLines(Asiento $entry): bool` - Añade línea de IRPF en compra
- `addPurchaseTaxLines(Asiento $entry): bool` - Añade líneas de IVA en compra
- `addPurchaseSuppliedLines(Asiento $entry): bool` - Añade línea de suplidos
- `addSalesIrpfLines(Asiento $entry): bool` - Añade línea de IRPF en venta
- `addSalesTaxLines(Asiento $entry): bool` - Añade líneas de IVA en venta
- `addSupplierLine(Asiento $entry): bool` - Añade línea de proveedor
- `purchaseAccountingEntry()` - Genera asiento de compra
- `salesAccountingEntry()` - Genera asiento de venta

### Clase AccountingCreation

**Namespace:** `FacturaScripts\Core\Lib\Accounting`

**Propiedades Privadas:**
- `$exercise: Ejercicio` - Ejercicio contable

**Métodos Públicos:**
- `__construct()` - Inicializa
- `createFromAccount($account, $code, $description = ''): Subcuenta` - Crea subcuenta desde cuenta
- `copyAccountToExercise($account, $codejercicio): Cuenta` - Copia cuenta a ejercicio
- `copySubAccountToExercise($subAccount, $codejercicio): Subcuenta` - Copia subcuenta a ejercicio
- `createSubjectAccount(&$subject, $account): Subcuenta` - Crea subcuenta de cliente/proveedor

**Métodos Protegidos:**
- `checkExercise($codejercicio): bool` - Verifica que ejercicio está abierto
- `getFreeSubjectSubaccount($subject, $account): string` - Obtiene código subcuenta libre para cliente/proveedor

### Clase AccountingClosingBase

**Namespace:** `FacturaScripts\Core\Lib\Accounting`

Extiende: `AccountingBase`

**Métodos Abstractos:**
- `getConcept(): string` - Obtiene concepto del asiento
- `getDate(): string` - Obtiene fecha del asiento
- `getOperation(): string` - Obtiene tipo de operación
- `getSQL(): string` - Obtiene SQL para datos

**Métodos Públicos:**
- `exec($exercise, $idjournal): bool` - Ejecuta proceso de cierre

**Métodos Protegidos:**
- `delete($exercise): bool` - Elimina asientos previos
- `initialChecks(): bool` - Verifica precondiciones

### Clase AccountingClosingClosing

**Namespace:** `FacturaScripts\Core\Lib\Accounting`

Extiende: `AccountingClosingBase`

**Métodos Públicos:**
- `exec($exercise, $idjournal): bool` - Ejecuta cierre de cuentas

**Métodos Protegidos:**
- `getConcept(): string` - Retorna concepto de cierre
- `getDate(): string` - Retorna fecha fin de ejercicio
- `getOperation(): string` - Retorna operación de cierre
- `getSQL(): string` - Obtiene SQL de balances de cuentas
- `setDataLine(&$line, $data): void` - Establece datos de línea para cierre

### Clase AccountingClosingOpening

**Namespace:** `FacturaScripts\Core\Lib\Accounting`

Extiende: `AccountingClosingBase`

**Propósito:** Abre balances de cuentas en ejercicio siguiente

**Métodos Principales:**
- `exec($exercise, $idjournal): bool` - Abre nuevas cuentas

### Clase AccountingClosingRegularization

**Namespace:** `FacturaScripts\Core\Lib\Accounting`

**Propósito:** Regulariza cuentas de gastos/ingresos

**Métodos Principales:**
- `exec($exercise, $idjournal): bool` - Ejecuta regularización

### Clase PaymentToAccounting

**Namespace:** `FacturaScripts\Core\Lib\Accounting`

**Propósito:** Genera asientos contables para pagos de documentos

### Clase AccountingAccounts

**Namespace:** `FacturaScripts\Core\Lib\Accounting`

**Métodos Protegidos:**
- `getAccount($special): Cuenta` - Obtiene cuenta especial
- `getIRPFPurchaseAccount($retention): Subcuenta` - Obtiene subcuenta de IRPF en compra
- `getIRPFSalesAccount($retention): Subcuenta` - Obtiene subcuenta de IRPF en venta
- `getSpecialSubAccount($special): Subcuenta` - Obtiene subcuenta especial
- `getSubAccount($code): Subcuenta` - Obtiene subcuenta por código

### Clase Ledger

**Namespace:** `FacturaScripts\Core\Lib\Accounting`

**Propósito:** Genera libro mayor

**Métodos Principales:**
- `generate(string $dateFrom, string $dateTo, array $params = [])`  - Genera libro mayor

### Clase AccountingPlanExport y AccountingPlanImport

**Namespace:** `FacturaScripts\Core\Lib\Accounting`

**Propósito:** Importar/Exportar planes contables

---

## Sistema Mod (Modificadores)

### Interfaz CalculatorModInterface

**Namespace:** `FacturaScripts\Core\Contract`

**Métodos Requeridos:**
- `apply(BusinessDocument &$doc, array &$lines): bool` - Aplica modificaciones iniciales al documento
- `calculate(BusinessDocument &$doc, array &$lines): bool` - Calcula totales del documento
- `calculateLine(BusinessDocument $doc, BusinessDocumentLine &$line): bool` - Calcula valores de línea
- `clear(BusinessDocument &$doc, array &$lines): bool` - Limpia cálculos previos
- `getSubtotals(array &$subtotals, BusinessDocument $doc, array $lines): bool` - Obtiene subtotales agrupados

### Clase CalculatorModSpain

**Namespace:** `FacturaScripts\Core\Mod`

Implementa: `CalculatorModInterface`

**Métodos Públicos:**
- `apply(BusinessDocument &$doc, array &$lines): bool` - Aplica reglas fiscales españolas
- `calculate(BusinessDocument &$doc, array &$lines): bool` - Valida coherencia fiscal global
- `calculateLine(BusinessDocument $doc, BusinessDocumentLine &$line): bool` - Aplica exenciones por línea
- `clear(BusinessDocument &$doc, array &$lines): bool` - Limpia datos
- `getSubtotals(array &$subtotals, BusinessDocument $doc, array $lines): bool` - Calcula subtotales con validaciones españolas

**Métodos Privados:**
- `applyUsedGoods(array &$subtotals, BusinessDocument $doc, BusinessDocumentLine $line, string $ivaKey, float $pvpTotal, float $totalCoste): bool` - Aplica régimen de bienes usados
- `checkLineConflicts(array $exenciones, bool $hasIva): bool` - Valida que no haya conflictos de exenciones
- `suggestGlobalExemption(BusinessDocument $doc, array $lines, bool $allLinesSaved, bool $allE3, bool $allE4, bool $allE2, bool $allE5): void` - Sugiere exención global
- `validateGlobalExemption(?string $globalEx, bool $allZeroIva, array $exenciones): bool` - Valida operación global
- `validateLineExemptions(BusinessDocument $doc, BusinessDocumentLine $line, ?string $subjectFiscalID, Contacto $addressShipping, ?string $globalEx): bool` - Valida exenciones por línea

**Características:**
- Valida operaciones intracomunitarias
- Soporta régimen de bienes usados
- Aplica exenciones de IVA españolas (E1-E6)
- Maneja inversión del sujeto pasivo
- Valida IRPF automático
- Calcula recargo de equivalencia

---

## Sistema de Workers (Cola de Trabajos)

### Clase WorkerClass

**Namespace:** `FacturaScripts\Core\Template`

**Propiedades:**
- Heredadas de clase base

**Métodos Abstractos:**
- `run(WorkEvent $event): bool` - Ejecuta trabajo

**Métodos Protegidos:**
- `done(): bool` - Marca trabajo como completado
- `failed(): bool` - Marca trabajo como fallido
- `retry(): bool` - Reintenta trabajo

### Clase TestWorker

**Namespace:** `FacturaScripts\Core\Worker`

Extiende: `WorkerClass`

**Métodos Públicos:**
- `run(WorkEvent $event): bool` - Almacena evento en caché para testing

**Uso:**
```php
$event = new WorkEvent();
$event->name = 'test-worker';
$event->value = 'test-value';

$worker = new TestWorker();
$worker->run($event);

// Recuperar valores de caché
$name = Cache::get('test-worker-name');
$value = Cache::get('test-worker-value');
```

### Clase PurchaseDocumentWorker

**Namespace:** `FacturaScripts\Core\Worker`

**Propósito:** Procesa documentos de compra en cola

**Métodos Principales:**
- `run(WorkEvent $event): bool` - Procesa documento de compra

### Clase CuentaWorker

**Namespace:** `FacturaScripts\Core\Worker`

**Propósito:** Procesa cuentas contables en cola

### Clase PartidaWorker

**Namespace:** `FacturaScripts\Core\Worker`

**Propósito:** Procesa partidas contables en cola

### Modelo WorkEvent

**Namespace:** `FacturaScripts\Core\Model`

**Propiedades:**
- `$id: string` - Identificador único
- `$name: string` - Nombre del evento
- `$value: mixed` - Valor asociado
- `$date: string` - Fecha del evento
- `$worker: string` - Clase worker que procesa

**Métodos:**
- `loadFromCode($code): bool` - Carga desde base de datos
- `save(): bool` - Persiste evento

### Sistema de Eventos (WorkEvent Listener)

Los plugins pueden crear eventos de trabajo con:
```php
$event = new WorkEvent();
$event->name = 'mi-evento';
$event->value = ['data' => 'valores'];
$event->save();

// El worker se ejecutará automáticamente en siguiente cron
```

### Ejecución de Workers

Los workers se ejecutan a través de:
1. **Cron API:** `/api/Cron` ejecuta workers pendientes
2. **CLI:** `php bin/console cron` (en instalaciones por comando)
3. **Dashboard:** Panel de control de trabajo

### Creación de Workers Personalizados

```php
namespace FacturaScripts\Dinamic\Worker;

use FacturaScripts\Core\Model\WorkEvent;
use FacturaScripts\Core\Template\WorkerClass;

class MiCustomWorker extends WorkerClass {
    public function run(WorkEvent $event): bool {
        // Procesar evento
        $data = json_decode($event->value, true);
        
        // Lógica del worker
        // ...
        
        return $this->done(); // o $this->failed()
    }
}
```

---

## Guías de Uso Práctico

### Exportar Datos a CSV desde Controlador

```php
use FacturaScripts\Core\Lib\Export\CSVExport;
use FacturaScripts\Dinamic\Model\FacturaCliente;

$export = new CSVExport();
$export->newDoc('Facturas', 0, 'ES');

$model = new FacturaCliente();
$where = [];
$order = ['fecha' => 'DESC'];
$columns = ['codigo', 'numero', 'fecha', 'total'];

$export->addListModelPage($model, $where, $order, 0, $columns, 'Listado Facturas');
$export->show($response);
```

### Exportar a PDF

```php
use FacturaScripts\Core\Lib\Export\PDFExport;

$export = new PDFExport();
$export->newDoc('Reporte', 0, 'ES');
$export->setCompany(1);

$model = new FacturaCliente();
if ($model->load($code)) {
    $export->addBusinessDocPage($model);
    $export->show($response);
}
```

### Enviar Email con Bloques

```php
use FacturaScripts\Core\Lib\Email\NewMail;
use FacturaScripts\Core\Lib\Email\TextBlock;
use FacturaScripts\Core\Lib\Email\ButtonBlock;
use FacturaScripts\Core\Lib\Email\TitleBlock;

$mail = NewMail::create();
$mail->to('cliente@example.com', 'Cliente');
$mail->title = 'Factura disponible';

$mail->addMainBlock(new TitleBlock('Su factura'));
$mail->addMainBlock(new TextBlock('Adjunto encontrará su factura.'));
$mail->addMainBlock(new ButtonBlock('Descargar', 'https://ejemplo.com/descargar'));

$mail->send();
```

### Generar Asiento Contable desde Factura

```php
use FacturaScripts\Core\Lib\Accounting\InvoiceToAccounting;

$accounting = new InvoiceToAccounting();
$factura = new FacturaCliente();
if ($factura->load($code)) {
    $accounting->generate($factura);
}
```

### Importar Datos desde CSV

```php
use FacturaScripts\Core\Lib\Import\CSVImport;

$sql = CSVImport::importFileSQL('clientes', '/ruta/archivo.csv');
$dataBase = new DataBase();
$dataBase->exec($sql);
```

### Crear Worker Personalizado

```php
namespace FacturaScripts\Dinamic\Worker;

use FacturaScripts\Core\Model\WorkEvent;
use FacturaScripts\Core\Template\WorkerClass;
use FacturaScripts\Core\Tools;

class ProcesoFacturasWorker extends WorkerClass {
    public function run(WorkEvent $event): bool {
        $data = json_decode($event->value, true);
        
        $factura = new FacturaCliente();
        if ($factura->load($data['idfactura'])) {
            // Procesar factura
            Tools::log()->info('Procesando factura: ' . $factura->codigo);
            return $this->done();
        }
        
        return $this->failed();
    }
}
```

### Validar Exenciones en España

```php
use FacturaScripts\Core\Mod\CalculatorModSpain;

$mod = new CalculatorModSpain();
$doc = new FacturaCliente();
$lines = $doc->getLines();

if (!$mod->getSubtotals($subtotals, $doc, $lines)) {
    // Hay errores fiscales
    Tools::log()->warning('Errores en validación fiscal');
}
```

---

## Constantes y Enumeraciones Importantes

### RegimenIVA (Excepciones Españolas)
- `ES_TAX_EXCEPTION_E1` - Exención por naturaleza
- `ES_TAX_EXCEPTION_E2` - Exportación
- `ES_TAX_EXCEPTION_E3` - Servicios intracomunitarios
- `ES_TAX_EXCEPTION_E4` - Artículos 23-24 LIVA
- `ES_TAX_EXCEPTION_E5` - Entrega intracomunitaria
- `ES_TAX_EXCEPTION_E6` - Otras exenciones
- `ES_TAX_EXCEPTION_PASSIVE_SUBJECT` - Inversión sujeto pasivo
- `ES_TAX_EXCEPTION_ART_7` - No sujeto (art. 7)
- `ES_TAX_EXCEPTION_ART_14` - No sujeto (art. 14)
- `ES_TAX_EXCEPTION_LOCATION_RULES` - Reglas de localización

### InvoiceOperation
- `INTRA_COMMUNITY` - Operación intracomunitaria
- `EXPORT` - Exportación
- `DOMESTIC` - Operación doméstica

### ProductType
- `PRODUCT` - Producto tangible
- `SERVICE` - Servicio
- `SECOND_HAND` - Bien usado

---

## Nota Final

Este documento proporciona referencia exhaustiva de todos los subsistemas de librerías de FacturaScripts 2025. Cada sección contiene propiedades, métodos, constantes y ejemplos de uso. Los desarrolladores deben consultar el código fuente para comportamientos específicos no documentados aquí.

Actualizado para FacturaScripts 2025 - Todos los derechos reservados Carlos García Gómez.
