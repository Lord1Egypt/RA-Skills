---
name: generador-artifact-educativo-formula100k
description: "Use when the user asks to create an educational artifact, miniapp, interactive resource, or visual guide for a concept of her own course or community, or of FÓRMULA 100K. Triggers on phrases like \"crea un artifact\", \"miniapp educativa\", \"recurso para mis alumnas\", \"artifact del tab X\", \"guía interactiva\", \"construye un artifact sobre [tema]\", \"armemos un artifact de [concepto]\". Generates a single self-contained HTML file (Guía / Flashcards / Examen) with React + Tailwind + Babel via CDN that works by double-clicking — no server, no build, no Claude subscription needed. Saves it to entregables/artifacts/ and sends it by Telegram."
metadata: {"openclaw": {"emoji": "🦞"}}
---

## 🦞 Corriendo en OpenClaw

> Esta versión corre en un agente OpenClaw (servidor + Telegram), no en Claude Code.
> **Antes de seguir, lee la skill `f100k-puente`**: traduce herramientas y rutas.
> Lo específico de esta skill:
>
> - Sirve para recursos de SU curso o comunidad (o de un tema de FÓRMULA 100K que esté estudiando). El material fuente te lo manda por Telegram como archivo o texto; los artifacts de FÓRMULA 100K que menciona la skill no vienen en este paquete, así que solo cruza referencias con los que existan en `entregables/artifacts/`.
> - `.docx` sin `textutil` (es de Mac): usa `pandoc -t plain` o `python-docx` si están; si no, pídele el texto en `.txt` o pegado.
> - Guarda en `entregables/artifacts/f100k-{tema}.html` (o con el prefijo de su marca si lo prefiere). Revisa el HTML con el navegador del agente a 390 px y 1280 px (las tres vistas cargan y las flashcards giran) y mándalo por Telegram como documento: funciona con doble clic, sin servidor.
> - Para elegir paleta sin repetir, lista los artifacts que ya hay en `entregables/artifacts/`; `paletas.md` trae las usadas en FÓRMULA 100K, no las de ella.
> - En el header y el footer del template cambia `@TUHANDLE` por su handle (sale de `USER.md`); nunca dejes el de otra persona.

---

# Generador de Artifacts Educativos · FÓRMULA 100K

Genera artifacts educativos con un mismo sistema reconocible. Cada artifact es una miniapp HTML standalone con 3 vistas (Guía / Flashcards / Examen) que ayuda a las alumnas a entender un concepto de su curso, su comunidad o del manual de FÓRMULA 100K.

## Cuándo usar esta skill

Se activa cuando el usuario pide:
- "Crea un artifact sobre [tema]"
- "Armemos una miniapp para el tab [X]"
- "Recurso interactivo para mis alumnas sobre [concepto]"
- "Guía visual de [tema]"
- "Artifact del módulo [X]"

## Contexto crítico antes de empezar

**Usuario:** creador/a de contenido con comunidad propia. Audiencia: emprendedoras hispanas, creadoras de contenido.

**Restricción técnica:** Los artifacts deben funcionar SIN suscripción paga de Claude. Por eso son HTML standalone, no artifacts de claude.ai.

**Carpeta destino:** `entregables/artifacts/`

**Naming convention:** `f100k-{tema-en-kebab-case}.html` (ej: `f100k-lead-magnet.html`)

## Archivos de soporte de esta skill

- `template.html` — Estructura base completa lista para personalizar
- `patrones-visuales.md` — Librería de componentes visuales reutilizables (mockups, accordion, decision matrix, etc.)
- `paletas.md` — Paletas usadas y disponibles para diferenciar cada artifact

## Paso a paso

### Paso 1: Recibir y leer el material fuente

El usuario proporcionará un archivo (.txt, .docx, link) con el contenido educativo. Si es .docx, conviértelo con:
```bash
pandoc -t plain "ruta/al/archivo.docx"   # o python-docx; si no hay ninguno, pide el texto en .txt
```

Lee el material completo y extrae:
- **Frameworks principales** (ej: las 5 fases, los 4 niveles, los 3 pilares)
- **Conceptos clave** que el alumno debe memorizar
- **Ejemplos concretos** y casos reales
- **Decisiones críticas** o patrones de error común
- **Referencias cruzadas** con otros tabs del manual F100K

### Paso 2: Decidir paleta de colores única

Lee `paletas.md` para ver qué paletas ya están en uso y elegir una que NO se haya usado. Cada artifact debe tener identidad visual única para que las alumnas los distingan rápidamente.

### Paso 3: Estructurar la Guía (3 a 5 sub-tabs)

Decide cuántos sub-tabs según la complejidad del tema:
- **3 sub-tabs**: temas simples con un framework central
- **4 sub-tabs**: temas con múltiples dimensiones (lo más común)
- **5 sub-tabs**: temas muy complejos con guía paso a paso al final

Cada sub-tab debe tener un patrón visual distinto. Los patrones disponibles están en `patrones-visuales.md`:
- Accordion expandible (para listas de fases/condiciones)
- Decision matrix (para "cuál elegir según X")
- Tabla comparativa (para múltiples opciones)
- Flujo visual con flechas (para procesos secuenciales)
- Cards con previews (para estilos visuales)
- Numbered steps con badges circulares (para procesos)
- Mockups visuales (para conceptos visuales)

### Paso 4: Crear las 8 flashcards

Reglas:
- Cada flashcard tiene un TAG categorizador (ej: FUNDAMENTOS, MECÁNICA, APLICACIÓN)
- Front: pregunta clara y específica
- Back: respuesta con saltos de línea (`\n`) para legibilidad
- Distribución temática: 2 fundamentos + 2 mecánica + 2 aplicación + 2 casos límite
- Las respuestas deben ser memorizables, no enciclopédicas (3-5 líneas máximo)

### Paso 5: Crear los 5 casos prácticos del examen

Reglas estrictas:
- **NO preguntas teóricas** — situaciones reales que una alumna podría enfrentar
- 4 opciones (A, B, C, D)
- 1 opción correcta + 3 distractores plausibles (errores comunes reales)
- Campo `why` con explicación educativa que refuerce el concepto
- Los casos deben cubrir las decisiones más frecuentes del tema

Estructura típica de un caso:
> "Una alumna tiene [contexto específico con números]. Hace [acción]. ¿Qué [decisión/diagnóstico]?"

### Paso 6: Generar el HTML

Usa `template.html` como base. Personaliza:
1. `<title>` y branding del header
2. Gradiente del header (paleta única elegida)
3. Datos de las constantes (PHASES/CARDS/EXAM/etc.)
4. Sub-tabs de la Guía y sus componentes
5. Color de acento en botones, progress bars y hover states
6. Markdown export con la estructura del nuevo contenido

**Reglas de código:**
- Mantener la estructura React + Babel + Tailwind por CDN
- Mantener CSS de flip cards intacto
- Mantener la clase `.no-print` para botones del header/nav/footer
- Usar `useState` y `useMemo` (no useEffect a menos que sea necesario)

### Paso 7: REVISIÓN OBLIGATORIA de español neutro

**Antes de guardar el archivo**, escanea TODO el contenido en busca de voseo argentino. Esta es la regla más importante de la skill — El usuario ya lo corrigió una vez.

PROHIBIDO (voseo argentino):
- (voseo) vos, sos, tenés, sabés, podés, debés, querés, vivís
- (voseo) aplicás, encuestás, conocés, entendés, decís
- (voseo) Pintá, Mostrá, Ofrecé, Creá, Documentá, Usá, Traducí, Convertí
- Extraé, Anotá, Aislá, Dejá, Seguí, Volvé, repasá, Buscá
- (voseo) Identificá, Eliminá, Listá, Capturá, andá, mirá, hacé, llevá
- (voseo) "en vos", "a vos", "para vos", "te conviene a vos"

USAR (español neutro):
- tú, eres, tienes, sabes, puedes, debes, quieres, vives
- aplicas, encuestas, conoces, entiendes, dices
- Pinta, Muestra, Ofrece, Crea, Documenta, Usa, Traduce, Convierte
- Extrae, Anota, Aísla, Deja, Sigue, Vuelve, repasa, Busca
- Identifica, Elimina, Lista, Captura, anda, mira, haz, lleva
- "en ti", "a ti", "para ti", "te conviene a ti"

Si encuentras dudas, pasa el archivo por:
```bash
grep -n "vos\|sos\|tenés\|sabés\|podés\|debés\|aplicás\|Pintá\|Mostrá\|Ofrecé\|Creá\|Documentá\|Usá\|Traducí\|Convertí\|Extraé\|Anotá\|Aislá\|Dejá\|Seguí\|Volvé\|repasá\|Buscá\|Identificá\|Eliminá\|Listá\|Capturá\|en vos\|a vos\|para vos" /ruta/al/archivo.html   # detector de voseo
```

### Paso 8: Guardar y abrir

```bash
# Guardar en la carpeta correcta
# Ruta: entregables/artifacts/f100k-{tema}.html

# Abrir en navegador para validar visualmente
# ábrelo con el navegador del agente (390 px y 1280 px) y mándalo por Telegram como documento
```

### Paso 9: Reportar al usuario

Al terminar, reporta:
1. Confirmar que el archivo está en la carpeta correcta
2. Listar la tabla actualizada de todos los artifacts existentes
3. Resumir lo nuevo/diferente de este artifact (qué patrones visuales usaste, color elegido, conexiones con otros artifacts)
4. Ofrecer el siguiente tema lógico si aplica

## Conexiones cruzadas entre artifacts

Cuando el tema lo permita y esos artifacts existan en `entregables/artifacts/` (los de FÓRMULA 100K no vienen en el paquete de OpenClaw), haz referencia explícita a otros artifacts ya creados:

- **Artifact de Análisis de Negocio** define las 5 fases (0-4) — referenciar al hablar de progresión
- **Artifact de Avatar** define los 4 niveles de consciencia — referenciar al hablar de contenido por nivel
- **Artifact de Vehículo Único** define el método propio — referenciar al hablar de diferenciación
- **Artifact de Urgencia** define los 5 gatillos — referenciar al hablar de CTAs y conversión
- **Artifact de Plataformas** define las decisiones por fase — referenciar al hablar de monetización

Estas referencias mantienen coherencia conceptual del universo F100K.

## Reglas anti-error

- **NO inventar contenido** — si el material fuente no cubre algo, pide aclaración antes de fabricar
- **NO traducir directamente** — adaptar al lenguaje del usuario (directo, profesional, sin tecnicismos innecesarios)
- **NO usar emojis decorativos** — solo emojis con función (📋 Guía, 🎯 CTA, ⚠ Warning)
- **NO repetir paletas** — cada artifact tiene identidad visual propia
- **NO superar 1500 líneas** en el HTML — si el contenido es muy denso, dividir en sub-tabs
- **NO crear archivos extras** (jsx, scss, json) — todo va en un solo HTML
- **NO usar lucide-react ni librerías externas** — solo Tailwind y emojis Unicode

## Formato de output del proceso

Mientras trabajas, comunica brevemente:
1. "Leyendo el material fuente"
2. "Estructurando [N] sub-tabs: [lista corta]"
3. "Construyendo el artifact" (después de leer)
4. "Revisando español neutro" (después de generar)
5. Tabla final + resumen de novedades

## Notas importantes

- El template tiene CSS de flip cards probado en Safari y Chrome — no modificarlo
- Tailwind por CDN incluye TODAS las clases — no necesitas agregar configuración
- El markdown export es el "pasaporte" del artifact: permite que cualquier IA lo procese para responder preguntas. Mantenerlo completo y bien estructurado.
- Si el tema requiere algo nuevo (ej: mockups visuales, interactividad especial), documenta el patrón en `patrones-visuales.md` para que se reutilice en futuros artifacts.
