# Documentación de Referencia - FacturaScripts 2025

## Bienvenida

Esta carpeta contiene una documentación exhaustiva y detallada del sistema de vistas, widgets, y arquitectura de FacturaScripts 2025, completamente en español.

## Archivos de Documentación

### 1. **views-widgets.md** (84 KB - 2,787 líneas)
**Documentación más completa y detallada del proyecto**

Contiene:
- Sistema completo de XMLViews (estructura, elementos, atributos)
- Catálogo exhaustivo de 26 widgets con ejemplos
- Documentación de plantillas Twig
- Lista completa de 133 XMLViews del core
- Guías paso a paso para crear vistas personalizadas
- Apéndices con referencias rápidas, jerarquía de clases, casos de uso, etc.

**Secciones principales:**
- Sistema de Vistas XML (estructura, columnas, grupos, rows, modales)
- Catálogo completo de widgets (WidgetText, WidgetMoney, WidgetSelect, etc.)
- Plantillas Twig (Master, Macros, Variables disponibles)
- Las 133 XMLViews del core organizadas por área
- Guía de creación de vistas personalizadas con ejemplos completos

### 2. **INDICE.md** (7.2 KB - 282 líneas)
**Referencia rápida y acceso directo**

Contiene:
- Widgets agrupados por tipo de dato
- XMLViews más usados agrupados por funcionalidad
- Estructura típica de XMLView con ejemplo mínimo
- Atributos comunes más utilizados
- Listado de las 26 clases de widget principales
- Códigos de color Bootstrap
- Métodos útiles en controladores

**Propósito:** Consulta rápida cuando necesitas encontrar algo específico en segundos.

### 3. **architecture.md** (60 KB)
Análisis completo de la arquitectura de FacturaScripts incluyendo MVC, patrones de diseño, flujo de datos, base de datos.

### 4. **plugins.md** (54 KB)
Guía completa para crear y desarrollar plugins de FacturaScripts.

### 5. **api.md** (70 KB)
Documentación de las APIs internas de FacturaScripts.

### 6. **controllers.md** y **controllers-advanced.md**
Documentación detallada de controladores y técnicas avanzadas.

### 7. **models.md** (35 KB)
Guía sobre la creación y uso de modelos en FacturaScripts.

### 8. **quick-reference.md** (13 KB)
Referencia rápida para desarrolladores con comandos y patrones comunes.

---

## Cómo Usar Esta Documentación

### Si Necesitas...

**Entender el sistema de vistas y crear un listado o formulario:**
→ Ver `views-widgets.md` sección 5 "Como Crear Vistas Personalizadas"

**Encontrar rápidamente un widget específico:**
→ Ver `INDICE.md` sección "Acceso Rápido a Widgets por Tipo de Dato"

**Saber qué atributos tiene un widget:**
→ Ver `views-widgets.md` sección 2 "Catálogo Completo de Widgets"

**Ver ejemplo completo de un XMLView (ListXxx.xml):**
→ Ver `views-widgets.md` sección 1.8 "Ejemplo Completo de ListXxx.xml"

**Ver ejemplo completo de un formulario (EditXxx.xml):**
→ Ver `views-widgets.md` sección 1.9 "Ejemplo Completo de EditXxx.xml"

**Entender como funcionan los filas de estado (status rows):**
→ Ver `views-widgets.md` sección 1.6.1 "Row Type: Status"

**Crear un plugin desde cero:**
→ Ver `plugins.md`

**Entender la arquitectura general:**
→ Ver `architecture.md`

**Referencia rápida de todo:**
→ Ver `INDICE.md` o `quick-reference.md`

---

## Características Principales de Esta Documentación

### Exhaustividad
- 26 widgets documentados completamente
- 133 XMLViews listados y categorizados
- Más de 14,000 líneas de documentación total
- Todos los atributos de cada elemento documentados

### Ejemplos Prácticos
- Ejemplos de XMLView para listados
- Ejemplos de XMLView para formularios
- Ejemplo completo integrado de Cliente VIP
- Patrones para crear modales
- Patrones para filas de estado

### Organización
- Tabla de contenidos clickeable
- Índices rápidos
- Agrupación lógica por funcionalidad
- Referencias cruzadas
- Apéndices especializados

### En Español
- 100% documentación en español
- Convenciones en español para FacturaScripts
- Ejemplos adaptados al contexto hispano

---

## Versión y Actualización

- **Versión:** FacturaScripts 2025.001
- **Fecha de generación:** 12 de abril de 2026
- **Idioma:** Español
- **Cobertura:** Core de FacturaScripts 2025

---

## Estructura de Directorios Referenciados

```
facturascripts-core/
├── facturascripts/Core/
│   ├── XMLView/              (133 archivos XML)
│   │   ├── ListProducto.xml
│   │   ├── EditProducto.xml
│   │   └── ...
│   ├── Lib/Widget/           (36 archivos PHP)
│   │   ├── WidgetText.php
│   │   ├── WidgetMoney.php
│   │   └── ...
│   ├── View/                 (plantillas Twig)
│   │   ├── Master/
│   │   ├── Macro/
│   │   └── ...
│   ├── Controller/
│   └── Model/
```

---

## Notas Importantes

1. **XMLViews:** Los archivos XML en `/Core/XMLView/` definen completamente cómo se visualizan y editan los datos en la UI.

2. **Widgets:** Hay 26 clases de widget principales, cada una especializada en un tipo de dato.

3. **Herencia:** Todos los widgets heredan de `BaseWidget`, que proporciona funcionalidad base común.

4. **Traducción:** Las etiquetas en XML se traducen automáticamente según patrones como `column-{name}`.

5. **Flexibilidad:** El sistema XML es muy flexible, permitiendo:
   - Ocultar/mostrar columnas dinámicamente
   - Cambiar el orden de campos
   - Cambiar ancho de columnas
   - Agregar campos personalizados

6. **Bootstrap:** Usa Bootstrap 5 para estilos y responsive design.

7. **FontAwesome:** Los íconos usan FontAwesome 6+.

---

## Documentos Generados Desde

Esta documentación se generó leyendo y analizando:

- **36 archivos PHP** de widgets en `/Core/Lib/Widget/`
- **133 archivos XML** de vistas en `/Core/XMLView/`
- **62 archivos** de plantillas y configuración en `/Core/View/`
- Arquitectura general del framework FacturaScripts

---

## Consejos para Developers

1. **Comienza con ejemplos:** Copia un XMLView existente similar a lo que quieres crear.

2. **Usa los widgets correctos:** Elige el widget adecuado para cada tipo de dato.

3. **Estructura tu XML:** Usa grupos para organizar campos en formularios grandes.

4. **Orden de campos:** Usa números múltiplos de 10 (100, 110, 120...) para orden.

5. **Traducciones:** Mantén las claves de traducción en archivos .json separados.

6. **Reutiliza:** El sistema está pensado para maximizar reutilización de código.

7. **Respeta convenciones:** Sigue las convenciones de nombres del framework.

---

## Contacto y Contribuciones

Para más información sobre FacturaScripts, visita:
https://www.facturascripts.com

---

**Documentación generada con dedicación para facilitar el desarrollo en FacturaScripts 2025.**
