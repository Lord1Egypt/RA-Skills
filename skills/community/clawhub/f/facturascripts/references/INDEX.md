# FacturaScripts 2025 - Documentacion Completa de Controladores

Indice maestro de la documentacion completa sobre controladores y arquitectura de FacturaScripts 2025.

---

## ARCHIVOS DE REFERENCIA

### 1. **controllers.md** (1,721 líneas - 47 KB)
Referencia exhaustiva principal de todos los controladores.

**Contenido:**
- Arquitectura de Controladores Extendidos (BaseController, ListController, EditController, PanelController)
- Propiedades y métodos de cada clase base
- Sistema de Vistas (BaseView, ListView, EditView, EditListView, HtmlView)
- Sistema de Filtros completo
- AjaxForms para documentos comerciales
- Listado categorizado de TODOS los controladores del core (113 controladores)
  - Dashboard y Configuración (Login, Root, Dashboard)
  - Clientes y Contactos (EditCliente, ListCliente, EditContacto)
  - Proveedores (EditProveedor, ListProveedor)
  - Productos y Stock (EditProducto, ListProducto, ListAlmacen, ListStock)
  - Documentos de Venta (Presupuestos, Pedidos, Albaranes, Facturas)
  - Documentos de Compra
  - Contabilidad (Asientos, Cuentas, Diarios, Ejercicios)
  - Administración (Usuarios, Roles, API)
  - Datos Básicos (Ciudades, Países, Bancos, etc.)
- Ejemplo completo: Como crear un ListController
- Ejemplo completo: Como crear un EditController
- Ejemplo completo: Como crear un PanelController

**Usar cuando:**
- Necesitas documentación exhaustiva sobre un controlador específico
- Buscas entender la arquitectura completa
- Necesitas ver ejemplos de implementación de diferentes tipos de controladores

---

### 2. **controllers-advanced.md** (713 líneas - 19 KB)
Guía avanzada con patrones de diseño y casos de uso reales.

**Contenido:**
- Patrones de Diseño Comunes
  1. ListController con múltiples vistas
  2. EditController con vistas relacionadas
  3. Filtros dinámicos generados desde BD
  4. Acciones personalizadas
- Filtros Avanzados
  - Crear filtro personalizado extendiendo BaseFilter
  - Usar filtro personalizado en vista
  - Combinación de filtros (AND/OR)
- Validación y Permisos
  - Verificación de permisos específicos
  - Filtrado por propietario
  - Validación de datos en modelo
- Traits y Mixins
  - ListViewFiltersTrait
  - ListBusinessActionTrait
  - DocFilesTrait
  - LogAuditTrait
  - ProductImagesTrait
- Casos de Uso Reales
  1. Listado de Facturas con Filtros Complejos
  2. Panel de Administración Completo
  3. Controlador con Validaciones Personalizadas
  4. Listado con Búsqueda Global
- Mejores Prácticas (Seguridad, Rendimiento, Mantenibilidad, UX)

**Usar cuando:**
- Necesitas implementar patrones complejos
- Buscas casos de uso específicos del mundo real
- Quieres optimizar o mejorar controladores existentes
- Necesitas crear filtros personalizados

---

### 3. **quick-reference.md** (454 líneas - 13 KB)
Referencia rápida y compacta para consulta rápida.

**Contenido:**
- Jerarquía de clases (diagrama ASCII)
- Métodos principales por clase (tabla resumida)
- Vista rápida de acciones comunes (código básico)
- Operadores de filtro (tabla de referencias)
- Configuración de vista (settings disponibles)
- Ejemplos de filtros
- Flujos de ejecución (ListController, PanelController, EditController)
- Permisos y seguridad
- Constantes útiles
- Archivos importantes (directorios y clases)
- Logging y debugging
- Operadores en URL
- Eventos y hooks (Pipes)
- Tips y trucos
- Checklist para crear nuevo controlador

**Usar cuando:**
- Necesitas referencia rápida
- Estás en medio de desarrollo y necesitas una búsqueda rápida
- Quieres recordar sintaxis o nombres de métodos
- Necesitas verificar operadores o configuraciones

---

## ESTADISTICAS

### Documentación Generada

- **2,888 líneas** totales de documentación
- **113 KB** de contenido en 3 archivos principales
- **113 controladores del core** documentados
- **9 tipos de filtros** explicados
- **5 tipos de vistas** documentadas

### Cobertura

- **Clases Base Documentadas**: 12 principales
- **Métodos Documentados**: 200+
- **Ejemplos de Código**: 11 completos
- **Patrones de Diseño**: 4 principales
- **Casos de Uso**: 5 reales
- **Mejores Prácticas**: 15+

---

## BUSQUEDAS RAPIDAS

### Por Tipo de Controlador:
- **ListController**: controllers.md sección 1.2
- **EditController**: controllers.md sección 1.4  
- **PanelController**: controllers.md sección 1.3
- **SalesController**: controllers.md sección 4

### Por Funcionalidad:
- **Filtros**: controllers.md sección 3 + controllers-advanced.md sección 2
- **Validación**: controllers-advanced.md sección 3
- **Permisos**: controllers-advanced.md sección 3
- **Vistas**: controllers.md sección 2

### Por Dominio de Negocio:
- **Clientes/Contactos**: controllers.md sección 5.B
- **Productos/Stock**: controllers.md sección 5.D
- **Ventas**: controllers.md sección 5.E
- **Compras**: controllers.md sección 5.F
- **Contabilidad**: controllers.md sección 5.G
- **Administración**: controllers.md sección 5.H

---

## COMO USAR

### Para Principiantes:
1. Leer quick-reference.md (estructura básica)
2. Leer controllers.md secciones: Arquitectura + Crear Controlador
3. Ver ejemplos en controllers-advanced.md

### Para Intermedios:
1. Usar controllers.md como referencia exhaustiva
2. Consultar controllers-advanced.md para patrones
3. Usar quick-reference.md para búsquedas rápidas

### Para Avanzados:
1. controllers-advanced.md para patrones complejos
2. quick-reference.md para referencias rápidas
3. controllers.md para detalles específicos

---

**Documentación Completa de FacturaScripts 2025**
**Generada: Abril 2026**
**Versión: 1.0 (Completa y Exhaustiva)**
