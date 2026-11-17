# SENDER — Auditoría STEP 1

Reconocimiento previo a construir. Sin diseño todavía.
Fecha: 2026-09-30 · Alcance: inventario de activos, contenido y estado real del proyecto.

---

## 1. Dónde estaban realmente los activos

El repo `cristianoleamiranda-dotcom/sender`, rama `main`, contiene **un solo archivo**:
`docs/proyecto/FLUJO-TRABAJO-IMMERSIVE.md`. Es decir: **`main` no es la fuente de verdad
de los activos**, aunque el propio documento de flujo lo declare así.

Los activos están en la rama **`arena/impeccable`** del mismo repo: **137 archivos**, 13 MB,
con `src/content/catalog.ts`, `src/content/site.ts` y las 10 fotografías originales.
Esta es la rama que manda.

| Rama de `sender` | Archivos | Qué contiene |
|---|---|---|
| `main` | 1 | Solo el documento de flujo |
| **`arena/impeccable`** | **137** | **Proyecto real**: fotos, video, catálogo, textos bilingües, QA |
| `arena/01a0ab93-sender` | 34 | React/Vite; `public/assets/{catalog,projects}/` **vacías** |
| `gh-pages` | 4 | `index.html` + video + frame 1 + `.nojekyll` |
| `cristianoleamiranda-dotcom-patch-1` | 2 | — |

> Nota de método: el conteo inicial de `arena/impeccable` pareció ser 2 porque `FETCH_HEAD` se
> sobrescribe en cada `git fetch` encadenado. Resuelto con `git rev-parse FETCH_HEAD` + `git archive`
> inmediato. No es un problema del repo.

---

## 2. Inventario de activos reales

**Todo lo listado existe. Nada es stock, nada es generado.** 9,7 MB rescatados al workspace.

### Fotografía — 10 originales

| Archivo | Dimensiones | Rol | Descripción |
|---|---|---|---|
| `hero.jpg` | 1200×1600 | ENTRY | Torre atirantada con balizamiento rojo, niebla y mar |
| `hero-wide.jpg` | 1792×1008 | ENTRY | Baliza costera, mar, cielo crepuscular |
| `about.jpg` | 1200×1600 | PROCESS | Técnico en banco de laboratorio con instrumental |
| `cap-broadcast.jpg` | 1600×1200 | SENDER | Sala de racks de radiodifusión, azul profundo |
| `cap-transmission.jpg` | 1200×1600 | ENGINEERING | Aislador / trampa de RF en campo, cielo de tormenta |
| `cap-antennas.jpg` | 1200×1600 | PROJECTS | Torre reticulada con arreglo de Yagis, montaña |
| `cap-rf.jpg` | 1200×1600 | PRODUCTS | Componentes RF: toroides, capacitores, semiconductores |
| `cap-critical.jpg` | 1792×1008 | TRANSMISSION | Estación costera con monopolo entre niebla marina |
| `proj-am.jpg` | 1200×1600 | PRODUCTS | Gabinete de transmisor con instrumentos analógicos |
| `proj-stl.jpg` | 1728×1152 | PROJECTS | Yagi en azotea sobre Santiago y la cordillera, atardecer |

### Video — 1 pieza

- `sender-hero.mp4` — 4,82 MB, 1376×768. Torre de telecomunicaciones en la cordillera al
  atardecer; dos técnicos con chaleco reflectante y una camioneta blanca en la base.
- `sender-hero-frame1.png` (2,5 MB) — frame 1 real, del que ya se derivaron 3 pósters WebP
  (640/960/1280).

### Lectura visual del material

Las diez fotos comparten un registro coherente y no negociado: **infraestructura real en
crepúsculo o noche, con niebla, mar o montaña**. Luz fría, azul-gris, con acentos cálidos
puntuales (balizamiento, ventana, skyline). Es un archivo fotográfico **cinematográfico y
sobrio**, no publicitario.

**Hallazgo que condiciona el DNA:** el video del hero tiene un **atardecer andino con naranja
dominante y muy saturado**. La paleta autorizada no incluye naranja. Hay que decidir el
tratamiento (ver §7, decisión B).

---

## 3. Inventario de contenido — verificado y auditado

El contenido no hay que inventarlo: **ya está escrito, es bilingüe y está auditado contra
`sender.cl`**. Es el activo más valioso del proyecto.

### Datos de empresa (`company.ts`)

| Dato | Valor |
|---|---|
| Nombre | Sender |
| Claim | *Tecnología que transmite* / *Technology that transmits* |
| Antigüedad | +20 años |
| Ciudad | Santiago, Chile |
| Teléfono | +56 9 8386 4148 |
| Correo | sender@sender.cl |
| Correo comercial | bis.ltda@gmail.com |
| Dirección | Blanco Viel 1108, 2º piso, San Miguel, Santiago, Chile |
| Dominio | https://www.sender.cl |
| Áreas | RF Engineering · Broadcasting · Transmission · Telecomunicaciones · Automatización |

### Catálogo — 16 productos en 7 categorías

| Categoría | Slug | Productos |
|---|---|---|
| Transmisores AM | `transmisores-am` | 2 |
| Transmisores FM | `transmisores-fm` | 1 |
| STL / Enlaces | `stl-enlaces` | 3 |
| Procesamiento de Audio | `procesamiento-de-audio` | 1 |
| Automatización | `automatizacion` | 2 |
| RF y Componentes | `rf-y-componentes` | 4 |
| Soluciones Especiales | `soluciones-especiales` | 3 |

Cada producto trae `slug`, nombre bilingüe, resumen, **grupos de especificaciones
(`specs`), características, aplicaciones, variantes, alt text bilingüe y `sourceUrl`**
a su ficha publicada en `sender.cl`.

### Proyectos documentados — 6

| # | Proyecto | Lugar | Fuente |
|---|---|---|---|
| 01 | Transmisor Sender en Radio Colosal | Ambato, Ecuador | **Radio World** (enlace verificable) |
| 02 | Torre autosoportada 60 m, desmontaje | Playa Ancha, Valparaíso | — |
| 03 | Comunicaciones HF de largo alcance | Isla de Pascua | — |
| 04 | Antena MF para NAVTEX 490/518 kHz | Entornos marítimos | — |
| 05 | Antenas HF de alto rendimiento | Chile e internacional | — |
| 06 | Enlaces estudio–planta AM/FM | Radiodifusión profesional | — |

### Bandas de operación — 6

AM 490–1700 kHz · FM 87.5–108 MHz · HF 2–30 MHz · VHF 134–174 MHz · UHF (enlaces) ·
NAVTEX 490/518 kHz

### La regla de contenido que el proyecto ya se impuso

Los archivos fuente lo declaran explícitamente y hay que **mantenerla**:

> «No se inventan clientes, no se asignan años, no se agregan cifras de proyectos
> completados. **Lo que no está documentado, no está.** Sin cifras de ventas, sin clientes
> sin nombre, sin certificaciones, sin premios, sin fechas de hitos.»

El modelo `Project` **no tiene campo `year`** a propósito: la interfaz simplemente no lo
muestra. Esto coincide exactamente con la prohibición del brief de inventar información.

---

## 4. Verificación cruzada contra el sitio vivo

`sender.cl` responde HTTP 200 (110.640 B, WordPress 7.1.2). Confirmado:

- Los mismos 16 productos y los mismos datos de contacto. **El contenido del repo es fiel.**
- **Deficiencias reales del sitio actual**, todas oportunidades del rediseño:
  - `<title>` = `sender.cl`. Sin meta description. Sin Open Graph.
  - **No es bilingüe**: todo en español. El repo ya tiene ES/EN completo.
  - Sobre WordPress con un tema comercial; sin jerarquía tipográfica propia.

---

## 5. Estado técnico heredado (lo que existe y funciona)

El proyecto en `arena/impeccable` es **React + Vite + TypeScript + react-router**, y ya tiene
trabajo de calidad hecho y medido que no conviene tirar a la basura sin saberlo:

| Activo heredado | Valor |
|---|---|
| QA automatizado | `qa/qa.mjs` recorre **27 rutas** con contraste WCAG AA por página |
| Perfil móvil real | `qa/dispositivo-s24.mjs` — 360×780, DPR 3 |
| Revisión de rutas profundas | `qa/pages-base.mjs` para GitHub Pages con base `/sender/` |
| Optimizador de assets | `scripts/optimize-assets.py` — 4,69 MB → 1,08 MB en WebP |
| Exportador WordPress | `tools/export-wordpress.mjs` |
| i18n | `src/i18n/LanguageContext.tsx` + `resolve.ts` (árbol de pares `{es, en}`) |
| SEO | `src/seo/jsonLd.ts`, `useDocumentMeta.ts`, sitemap y robots |
| Motion respetuoso | `useReducedMotion`, `useLenis`, `useCinematicHero` |

**Mediciones registradas del build heredado:** Lighthouse escritorio 99 / 100 / 100 / 100
(Perf / A11y / BP / SEO), móvil 78 / 100 / 100 / 100. CLS 0,013. 305 KiB.

### Bloqueo conocido

El token de GitHub está **expirado o revocado** (`401 Bad credentials`) y hay **3 commits sin
publicar** en `arena/01a0afb6-sender`, incluido el arreglo de rutas profundas. El sitio
publicado (`cristianoleamiranda-dotcom.github.io/sender/`) corre un build anterior y tiene ese
bug vivo. Ver §7, decisión C.

---

## 6. Riesgos y trampas detectadas

1. **El brief pide Next.js; el proyecto real es Vite.** Migrar significa abandonar el router,
   el QA de 27 rutas, el exportador de WordPress y el arreglo de `404.html` para Pages, todo
   ya verificado. Ver §7, decisión A.
2. **El repo está fragmentado en ~19 repositorios** del mismo proyecto (`sender-onair` 43 MB,
   `sender-site` 45 MB, `sender-atelier` 38,7 MB, `sender-design-ops` 106 MB…). Se eligió
   `arena/impeccable` porque es el único que contiene simultáneamente **fotos originales,
   video, catálogo y textos bilingües verificados**. Los demás son versiones anteriores o
   artefactos de proceso.
3. **Solo hay 10 fotos para 9 escenas.** No se pueden inventar imágenes. El diseño debe
   resolverse con **recorte, duotono, profundidad y movimiento** sobre las mismas piezas, no
   repitiendo fotos evidentemente.
4. **Algunas fotos ya están comprometidas a un producto o proyecto concreto** (`proj-am`,
   `proj-stl`, `cap-broadcast`). Usarlas como ambiente genérico debilita su rol documental.
5. **`DESIGN.md` de la raíz es del proyecto «Dala»** (negro, iris violeta, saffron). **No aplica
   a SENDER** y su paleta es justo la prohibida. No se reutiliza.

---

## 7. Decisiones que bloquean la construcción

### A · Stack
El brief pide Next.js + R3F + GSAP + Lenis. Lo heredado es Vite + React + Lenis.
- **Migrar a Next.js**: cumple el brief, permite SSG/SEO por idioma y `hreflang` reales.
  Coste: reconstruir router, QA y Pages.
- **Quedarse en Vite**: conserva QA, exportador y arreglo de rutas; SEO bilingüe se resuelve
  con rutas `/es` y `/en` + prerender.

### B · Tratamiento de color de foto y video reales
El atardecer del video del hero es naranja saturado; la paleta autorizada no tiene naranja.
- **Grade frío** (duotono hacia `#1E73BE` / `#0085B2`): unifica todo el archivo con el sistema.
  Mantiene el contenido intacto — no altera la identidad fáctica — pero modifica las fotos.
- **Respetar el color original**: máxima fidelidad documental, pero el naranja entra al sitio.

### C · Entrega a GitHub
No hay credenciales de escritura disponibles. No puedo crear la rama `immersive-redesign`
ni empujar los 12 commits por hito.
- **Construir en el workspace** y entregar el árbol completo + script que crea los 12 commits
  exactos, para que el push lo haga la persona.
- **O** facilitar un fine-grained PAT (solo `Contents: RW` + `PR: RW`, ≤ 7 días, según la
  propia política de `SEGURIDAD.md`).

### D · Alcance de la primera entrega
El brief exige aprobación visual del Hero **antes** de seguir.
- Entregar **DNA + Hero** y detenerse hasta la aprobación (lo que pide el brief), **o**
  construir el sitio completo y ajustar después.

---

## 8. Lo que NO se va a hacer

- No se sustituyen fotografías reales por stock ni por imágenes generadas.
- No se inventan clientes, fechas, cifras, certificaciones ni productos.
- No se usa ningún color fuera de `#FFFFFF` `#1E73BE` `#494949` `#0085B2`.
- No se copia ninguna web de referencia.
- No se mezclan idiomas en la interfaz.
- No se toca la rama de producción.
- No se usa el vocabulario prohibido (*innovative solutions*, *cutting-edge*, *revolutionary*,
  *next-generation*, *world-class*).
