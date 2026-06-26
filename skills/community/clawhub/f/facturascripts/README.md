# FacturaScripts 2025 - Skill Completo

Skill de referencia exhaustiva para **FacturaScripts 2025.81**, el ERP open-source en PHP para gestion empresarial. Este skill permite a cualquier LLM generar codigo correcto para FacturaScripts sin necesidad de consultar documentacion externa.

Desarrollado por **Jose Conti** - [plugins.joseconti.com](https://plugins.joseconti.com)

---

## Para que sirve este skill

Este skill cubre la totalidad de FacturaScripts 2025 y permite:

- Crear plugins completos para FacturaScripts (modelos, controladores, vistas, traducciones, assets).
- Conectar sistemas externos con la API REST de FacturaScripts.
- Crear un MCP Server (Model Context Protocol) con herramientas para interactuar con FacturaScripts desde un LLM.
- Depurar y modificar codigo existente de plugins.
- Entender la arquitectura interna del ERP para tomar decisiones de desarrollo informadas.
- Trabajar con la contabilidad, facturacion, stock, compras, ventas y CRM del sistema.

---

## Que contiene

El skill se compone de un archivo principal `SKILL.md` que actua como punto de entrada y 12 archivos de referencia detallados en `references/`. En total, mas de **21,500 lineas de documentacion tecnica** (676 KB) generadas directamente desde el codigo fuente de FacturaScripts CORE-2025.81.

### Estructura de archivos

```
facturascripts-skill/
  SKILL.md                          Punto de entrada del skill (181 lineas)
  README.md                         Este archivo
  .gitignore                        Exclusiones de Git
  references/
    architecture.md                 Arquitectura del nucleo (2,374 lineas)
    models.md                       Todos los modelos de dominio (1,135 lineas)
    controllers.md                  Controladores y sistema extendido (1,721 lineas)
    controllers-advanced.md         Patrones avanzados de controladores (713 lineas)
    views-widgets.md                Vistas XML, widgets y plantillas Twig (2,787 lineas)
    api.md                          API REST completa y guia MCP Server (2,811 lineas)
    database.md                     Base de datos, esquemas y migraciones (2,649 lineas)
    plugins.md                      Desarrollo de plugins paso a paso (2,089 lineas)
    libraries.md                    Exportacion, PDF, email, contabilidad (944 lineas)
    security.md                     Seguridad, usuarios, roles, permisos (1,840 lineas)
    translations.md                 Traducciones e internacionalizacion (1,181 lineas)
    quick-reference.md              Consulta rapida de clases y metodos (454 lineas)
```

---

## Que documenta cada referencia

### architecture.md - Arquitectura del nucleo

Documentacion exhaustiva de los 26 componentes principales del core de FacturaScripts:

- **Punto de entrada** (index.php): flujo completo de ejecucion paso a paso.
- **Kernel**: sistema de rutas, matching de URLs, timers, bloqueos, ciclo de vida completo.
- **Request**: encapsulacion de datos HTTP (GET, POST, headers, cookies, files), deteccion de navegador y SO.
- **Response**: respuestas HTTP con interfaz fluent (json, pdf, file, download, view, redirect), gestion de cookies.
- **Session**: manejo de sesion, usuario autenticado, permisos, deteccion de IP.
- **Plugins**: instalacion, activacion, desactivacion, eliminacion, deploy, gestion de dependencias.
- **Cache**: cache basada en archivos con TTL, patron remember para lazy-loading.
- **Logger**: logging multicanal con niveles (debug, info, notice, warning, error, critical), persistencia a BD.
- **Tools**: mas de 40 funciones utilitarias (fechas, numeros, bytes, carpetas, slugs, ASCII, config).
- **Html (Twig)**: motor de plantillas con funciones personalizadas (asset, cache, config, trans, money, number, date, bytes).
- **Http**: cliente cURL con soporte GET, POST, PUT, PATCH, DELETE, headers y bearer token.
- **Translator**: sistema de traducciones multiidioma con parametros y deploy.
- **Validator**: validadores para email, URL, fecha, alfanumerico, string.
- **DbQuery**: query builder fluent con llamadas magicas (whereNombre, whereCodcliente).
- **Where**: constructor de clausulas WHERE con todos los operadores.
- **WorkQueue**: cola de trabajos asincronos con wildcards.
- **NextCode**: generacion de codigos secuenciales con bloqueo.
- **Migrations**: sistema de migraciones del core y plugins.
- **DbUpdater**: actualizacion de estructura de BD desde XML.
- **Base/Controller**: clase base de controladores con seguridad y respuestas.
- **Base/DataBase**: abstraccion MySQL/PostgreSQL con transacciones.
- **Contratos e interfaces**: todas las interfaces del sistema.
- **Error handlers**: DefaultError, PageNotFound, AccessDenied y otros.
- **DataSrc**: data sources precacheados (Agentes, Almacenes, Divisas, Empresas, Series).
- **Internal**: Plugin, Headers, SubRequest, PluginsDeploy.
- **CrashReport, DebugBar, Telemetry, UploadedFile**.

### models.md - Modelos de dominio

Documentacion de los 87+ modelos organizados por area funcional:

- **Clases base**: ModelCore, ModelClass (CRUD completo, busqueda, paginacion), JoinModel.
- **15 traits**: CompanyRelationTrait, CurrencyRelationTrait, EmailAndPhonesTrait, ExerciseRelationTrait, FiscalNumberTrait, GravatarTrait, IbanTrait, IntracomunitariaTrait, InvoiceLineTrait, InvoiceTrait, PaymentRelationTrait, ProductRelationTrait, SerieRelationTrait, TaxRelationTrait, AccEntryRelationTrait.
- **Maestros basicos**: Pais, Divisa, Almacen, Empresa, AgenciaTransporte.
- **Clientes y proveedores**: Cliente, Proveedor, Contacto, GrupoClientes.
- **Productos**: Producto, Variante, Stock, Familia, Fabricante, Atributo, AtributoValor, Tarifa, ProductoImagen, ProductoProveedor.
- **Documentos de venta**: PresupuestoCliente, PedidoCliente, AlbaranCliente, FacturaCliente y todas sus lineas.
- **Documentos de compra**: PresupuestoProveedor, PedidoProveedor, AlbaranProveedor, FacturaProveedor y todas sus lineas.
- **Pagos**: ReciboCliente, PagoCliente, ReciboProveedor, PagoProveedor.
- **Contabilidad**: Ejercicio, Cuenta, Subcuenta, CuentaEspecial, Asiento, Partida, Diario.
- **Impuestos**: Impuesto, ImpuestoZona, Retencion.
- **Configuracion**: Serie, FormaPago, Settings, CronJob.
- **Usuarios y permisos**: User, Role, RoleAccess, RoleUser.
- **API**: ApiKey, ApiAccess.
- **Paginas**: Page, PageOption, PageFilter.
- **Archivos**: AttachedFile, AttachedFileRelation.
- **Notificaciones**: LogMessage, WorkEvent, EmailNotification, EmailSent.
- **Transformacion**: DocTransformation.
- **Cuentas banco**: CuentaBanco, CuentaBancoCliente, CuentaBancoProveedor.
- **Modelos Join**: vistas virtuales con campos calculados.
- **Diagrama de relaciones** entre modelos.

Cada modelo incluye: tabla y clave primaria, todas las propiedades con tipos PHP, todos los metodos con firmas completas, relaciones con otros modelos y logica de negocio.

### controllers.md - Controladores

Documentacion de los 125+ controladores del core y el sistema extendido:

- **BaseController**: propiedades, metodos de respuesta, seguridad, permisos.
- **ListController**: listados con filtros, ordenacion, paginacion, createViews, loadData.
- **EditController**: formularios de edicion, execPreviousAction, execAfterAction.
- **PanelController**: formularios con pestanas (tabs), addView.
- **ReportController**: informes con filtros.
- **Sistema de vistas**: BaseView, ListView, EditView, EditListView, HtmlView.
- **9 tipos de filtros**: AutocompleteFilter, CheckFilter, DateFilter, NumberFilter, PeriodFilter, SelectFilter, SelectWhereFilter y mas.
- **AjaxForms**: formularios AJAX para documentos comerciales (ventas y compras).
- **Todos los controladores del core** organizados por funcionalidad: dashboard, clientes, proveedores, productos, ventas, compras, contabilidad, informes, administracion.
- **Ejemplos completos** de como crear controladores List y Edit.

### controllers-advanced.md - Patrones avanzados

- Patrones de diseno comunes en controladores.
- Filtros avanzados y personalizados.
- Validacion y permisos.
- Traits y mixins disponibles.
- Casos de uso reales.
- Mejores practicas de seguridad y rendimiento.

### views-widgets.md - Vistas y widgets

- **Sistema de vistas XML**: estructura completa de archivos XMLView (columns, rows, modals, groups).
- **26 tipos de widgets** documentados con propiedades, comportamiento y ejemplos: WidgetText, WidgetTextarea, WidgetNumber, WidgetMoney, WidgetPercentage, WidgetDate, WidgetDatetime, WidgetTime, WidgetCheckbox, WidgetSelect, WidgetAutocomplete, WidgetDatalist, WidgetRadio, WidgetPassword, WidgetFile, WidgetLibrary, WidgetLink, WidgetColor, WidgetJson, WidgetBytes, WidgetSeconds, WidgetStars, WidgetVariante, WidgetSubcuenta y otros.
- **Plantillas Twig**: estructura Master, macros, variables, funciones personalizadas, como extender desde plugins.
- **133 XMLViews del core** organizadas por area funcional.
- **Guia paso a paso** para crear vistas personalizadas con modales y filas de estado.

### api.md - API REST

- **Arquitectura de la API**: flujo de peticiones, ApiController, autenticacion, codigos de error.
- **Recursos automaticos**: CRUD automatico por modelo, endpoints GET/POST/PUT/DELETE.
- **9 operadores de filtro**: =, gt, gte, lt, lte, neq, like, null, notnull.
- **Gestion de API Keys**: modelo ApiKey, ApiAccess, permisos granulares por recurso y metodo HTTP.
- **Recursos personalizados**: como crear endpoints API propios en un plugin.
- **Ejemplos practicos**: listar clientes, crear facturas, actualizar stock, buscar productos.
- **Uso desde codigo externo**: ejemplos en cURL, PHP, JavaScript/fetch y Python requests.
- **Guia para crear un MCP Server**: implementacion completa en TypeScript con herramientas basadas en la API.

### database.md - Base de datos

- **Abstraccion DataBase**: conexion, consultas, estructura, transacciones.
- **Motores soportados**: MySQL y PostgreSQL con sus diferencias.
- **DbQuery (Query Builder)**: todos los metodos fluent (select, where, join, groupBy, orderBy, limit, agregaciones).
- **Where**: todos los operadores y combinaciones AND/OR.
- **DbUpdater**: creacion y actualizacion de tablas desde XML.
- **Migraciones**: sistema del core y plugins.
- **Esquema completo de la base de datos**: todas las tablas con columnas, tipos, restricciones e indices.
- **Formato XML de tablas**: como definir tablas nuevas.
- **Ejemplos practicos** de consultas comunes.

### plugins.md - Desarrollo de plugins

Guia completa para crear plugins de principio a fin:

- **Estructura de directorios** y archivos requeridos.
- **facturascripts.ini**: formato completo con todos los campos.
- **Init.php**: metodos init(), update(), uninstall().
- **Ciclo de vida**: instalacion, activacion, actualizacion, desactivacion, eliminacion.
- **Sistema Mod (hooks)**: todas las interfaces de modificadores para extender el core.
- **Crear modelos**: definir tabla XML y clase Model.
- **Crear controladores**: List, Edit, Panel con getPageData completo.
- **Crear vistas**: XMLView y plantillas Twig personalizadas.
- **Workers**: cola de trabajos, registro y ejecucion.
- **Migraciones**: automaticas por XML y manuales.
- **Traducciones**: archivos JSON multiidioma.
- **Assets**: inclusion de CSS y JavaScript.
- **Ejemplo completo**: plugin funcional paso a paso con todos los componentes.

### libraries.md - Librerias

- **Exportacion**: ExportBase, CSVExport, XLSExport, PDFExport, MAILExport, AsientoExport.
- **PDF**: PDFCore, PDFDocument con headers, footers, QR, tablas de impuestos.
- **Email**: arquitectura de bloques (Text, Html, Table, Button, Title, Box, Space), NewMail, MailNotifier, SMTP.
- **Importacion**: CSVImport con soporte MySQL y PostgreSQL.
- **Contabilidad**: InvoiceToAccounting, AccountingCreation, AccountingClosing, Ledger.
- **Sistema Mod**: CalculatorModInterface con implementacion espanola completa.
- **Workers**: WorkerClass, TestWorker, PurchaseDocumentWorker, CuentaWorker, PartidaWorker.

### security.md - Seguridad

- **Modelo User**: propiedades, hash de password, verificacion, autenticacion en dos factores (TOTP).
- **Sistema de Roles**: Role, RoleAccess, RoleUser.
- **Permisos por pagina**: allowdelete, allowupdate, allowinsert, allowdetail, allowexport, allowimport, onlyownerdata.
- **Sesion y autenticacion**: login, logout, cookies, proteccion contra fuerza bruta.
- **Proteccion CSRF**: MultiRequestProtection, generacion y validacion de tokens.
- **Seguridad API**: API Keys, acceso por recurso, metodo HTTP.
- **Validacion de datos**: todos los validadores con sus reglas.
- **Implementar seguridad en plugins**: ejemplos de verificacion de permisos, prevencion XSS y SQL injection.

### translations.md - Traducciones

- **Clase Translator**: metodos completos para traduccion.
- **Formato de archivos**: estructura JSON, convenciones de claves.
- **25 idiomas soportados**: espanol, ingles, aleman, frances, italiano, catalan, euskera, gallego, valenciano y variantes latinoamericanas.
- **Uso en PHP y Twig**: Tools::trans(), filtro trans().
- **Parametros**: sintaxis %nombre%.
- **Traducciones en plugins**: estructura, carga automatica, sobrescritura.
- **Datos por pais**: sistema CSV con provincias, ciudades, divisas.

### quick-reference.md - Consulta rapida

Tabla de referencia compacta con las clases, metodos y patrones mas utilizados para consultas rapidas durante el desarrollo.

---

## Como usar este skill

### En Claude Code o Cowork

Coloca la carpeta `facturascripts-skill` en la ruta de skills de tu proyecto o sesion. Claude cargara el `SKILL.md` automaticamente cuando detecte que la tarea esta relacionada con FacturaScripts y consultara las referencias especificas segun lo que necesite.

### Como referencia de desarrollo

Puedes consultar los archivos de `references/` directamente como documentacion tecnica. Estan organizados por area funcional y cada uno tiene tabla de contenidos para facilitar la navegacion.

---

## Sobre FacturaScripts

FacturaScripts es un ERP open-source desarrollado en PHP que cubre:

- Facturacion (presupuestos, pedidos, albaranes, facturas).
- Contabilidad (plan contable, asientos, balances, cierres).
- Gestion de stock (multialmacen, movimientos, inventario).
- Compras y ventas (documentos completos con lineas, impuestos, descuentos).
- CRM (clientes, proveedores, contactos, grupos).
- Gestion de usuarios y permisos basada en roles.
- API REST completa para integraciones externas.
- Sistema de plugins extensible.

Mas informacion en [facturascripts.com](https://facturascripts.com).

---

## Version

- **FacturaScripts Core**: 2025.81
- **Skill version**: 1.0.0
- **Fecha de creacion**: Abril 2026

---

## Autor

**Jose Conti**
- Web: [plugins.joseconti.com](https://plugins.joseconti.com)
- Email: j.conti@joseconti.com

---

## Licencia

Este skill es documentacion tecnica generada a partir del codigo fuente de FacturaScripts, que se distribuye bajo licencia LGPL v3. Consulta el archivo COPYING del proyecto original para mas detalles.
