---
name: calendario-actividades-skool-f100k
description: "Toma una rutina semanal recurrente + eventos puntuales con fecha + un tema de marca, calcula la grilla real del mes y la renderiza con HTML→Chrome→PNG. Dos caminos: DESDE 0 (arma la rutina con la metodología F100K de anclas) o CLONAR el mes anterior y ajustar. Activar SIEMPRE que se pida \"arma el calendario de actividades de mi comunidad/Skool\", \"hazme el calendario mensual de la comunidad\", \"el calendario de sesiones del mes\", \"calendario de eventos de Skool\", \"diséñame el calendario de actividades como el de F100K\", \"calendario de la comunidad de [clienta]\", \"actualiza el calendario de actividades a [mes]\", o cualquier variación que combine una comunidad/Skool con el calendario VISUAL de sus sesiones/eventos del mes. NO confundir con calendario-semanal-f100k ni calendarizador-contenido-formula100k (esas son para CONTENIDO de redes), ni con calendarizador-historias/urgencias."
metadata: {"openclaw": {"emoji": "🦞"}}
---

## 🦞 Corriendo en OpenClaw

> Esta versión corre en un agente OpenClaw (servidor + Telegram), no en Claude Code.
> **Antes de seguir, lee la skill `f100k-puente`**: traduce herramientas y rutas.
> Lo específico de esta skill:
>
> - Arranca desde `plantillas/dinamicas-genericas.json` (o `blanco.json`). La config real de FÓRMULA 100K no viaja en este paquete. La config de su comunidad guárdala en `cerebro/calendario-actividades/<comunidad>.json` para clonarla el mes siguiente.
> - Render: la primera vez `npm install` dentro de la carpeta de la skill (solo `puppeteer-core`, no baja navegador). Corre desde la raíz del workspace con el Chromium del servidor: `CHROME_PATH=$(command -v chromium || command -v chromium-browser) node skills/calendario-actividades-skool-f100k/render.js cerebro/calendario-actividades/<comunidad>.json --out entregables/calendarios-actividades/<AAAA-MM>_<comunidad>.png`.
> - El tema `alquimista-f100k` es la marca de FÓRMULA 100K. Para la comunidad de la usuaria usa `minimalista-claro`, `oscuro-neon` o un fondo propio; el tema nuevo va en `cerebro/calendario-actividades/themes/<marca>/` y lo copias a `themes/` antes de renderizar (las actualizaciones borran la carpeta de la skill).
> - Fondo propio con Higgsfield: costo estimado y ✅ antes de generar. Si no está el plugin, entrega el prompt y usa un tema CSS.
> - Mira el PNG antes de mandarlo (fechas en su día, chips sin desbordar) y mándalo por Telegram como archivo junto al `.html` editable. Publicarlo en Skool lo hace ella.

---

# Skill: Calendario de Actividades de Skool · FÓRMULA 100K

Convierte la rutina de una comunidad Skool en el **calendario mensual visual** (PNG) que se publica dentro de la comunidad — el entregable de "Contenido Vivo": predictibilidad (rutina fija) + novedad (eventos del mes).

Produce la **imagen final lista para publicar**, no un plan en texto. El motor es HTML → Chrome headless → PNG (mismo patrón que `carrusel-render-formula100k`).

---

## CUÁNDO USAR

- "Arma / actualiza el calendario de actividades de mi comunidad (a [mes])"
- "El calendario mensual de sesiones / eventos de Skool"
- "Diséñame el calendario como el de FÓRMULA 100K"
- "El calendario de la comunidad de [clienta]"

**No** es para contenido de redes (eso es `calendarizador-contenido-formula100k` / `calendario-semanal-f100k`).

---

## CÓMO FUNCIONA (3 pasos)

1. **Config** — un JSON por comunidad con: `comunidad`, `tema`, `mes`, `anio`, `rutinaSemanal`, `horarios`, `eventos`, `catalogoTipos`. Ver `plantillas/`.
2. **Render** — `node render.js <config.json>` calcula la grilla real del mes y la dibuja sobre el fondo del tema.
3. **Output** — PNG + HTML editable en `entregables/calendarios-actividades/` (corre el render desde la raíz del workspace).

### Primera vez
```bash
cd <skill>/calendario-actividades-skool-f100k
npm install          # instala puppeteer-core (usa el Chromium del servidor vía CHROME_PATH, no descarga otro)
```

### Renderizar
```bash
node render.js plantillas/dinamicas-genericas.json         # usa mes/anio/tema del config
node render.js mi-comunidad.json --mes 7 --anio 2026       # sobrescribe mes/año
node render.js mi-comunidad.json --tema oscuro-neon        # cambia de tema
node render.js mi-comunidad.json --out /ruta/calendario.png --scale 2
```

---

## CARGA EL CALENDARIO DE DINÁMICAS — no te quedes corto

**Antes de armar cualquier rutina, lee `referencias/dinamicas-y-eventos.md`.** Tiene el catálogo canónico F100K: **6 categorías · 28 dinámicas**, el **ritmo de 7 días con copy listo**, el **arco mensual de 4 semanas** (Fundamentos → Ejecución → Optimización → Celebración+Reto), el **mapa de frecuencias** y las **reglas de oro**.

Un calendario pobre (2–3 chips sueltos) NO es el entregable. Un calendario vivo **mezcla categorías**: rituales (lunes de metas, viernes de wins, check-in), participación (hot seat, pregunta del día, encuestas), gamificación (reto relámpago, leaderboard, rachas), co-creación (votaciones, construyamos juntas, caso de estudio), reconocimiento (alumna del mes, muro de la fama, shout-outs) y eventos en vivo (Q&A, co-working, masterclass, ceremonia de cierre).

- **Rutina semanal** = el esqueleto que se repite (ritmo de 7 días). Llénala de verdad.
- **Eventos del mes** = el arco de 4 semanas (inicio de reto S1, masterclass S2, reto relámpago/co-creación S3, regalo + cierre de reto + alumna del mes S4).
- **Adapta el copy y los nombres al nicho** de la clienta (el hot seat es auditoría de perfil, revisión de rutina, auditoría de oferta…).

## LOS DOS CAMINOS

### A) DESDE 0 (comunidad sin calendario)
1. Pregunta: nombre de la comunidad, nicho, y cuánta energía/equipo tiene (cuántas sesiones EN VIVO por semana puede sostener — los rituales en post fijado cuestan poco y sí pueden ser diarios).
2. Parte de `plantillas/dinamicas-genericas.json` (config "cargado" con el ritmo de 7 días + arco mensual completo) y **recorta** según la energía real, en vez de partir de `blanco.json` y quedarte corto.
   - **Siempre** conserva las dos anclas: un **Q&A en vivo** a media semana y un cierre de **Wins** el viernes.
   - Reparte el resto del ritmo de 7 días (lunes de metas, recurso/mini-clase, hot-seat, reto relámpago sábado, domingo de planeación).
   - Lo "en vivo" es lo caro: empieza con **2–3 eventos vivos/semana**; los rituales async pueden ser más.
   - Eventos del mes según el arco: inicio de reto (S1), masterclass/invitado (S2), reto relámpago + co-creación (S3), regalo del mes + cierre de reto + alumna del mes (S4).
3. Elige tema y renderiza.

### B) CLONAR Y AJUSTAR (ya tiene calendario)
1. Parte del config del mes anterior (o de `plantillas/dinamicas-genericas.json`).
2. Cambia `mes`/`anio` y **rota lo dinámico** de este mes en `eventos`: nuevo reto y tema mensual, masterclass distinta, nueva dinámica de co-creación, presenciales, lanzamientos. No repitas el mismo mes calcado — el arco de 4 semanas se mantiene, el contenido cambia.
3. Re-renderiza. La rutina semanal se recalcula sola sobre las fechas del mes nuevo.

---

## MODELO DE DATOS (config)

| Campo | Qué es |
|---|---|
| `comunidad` | Nombre que sale en el sidebar |
| `mesLabel` | Etiqueta corta grande del sidebar (ej. `"MAY."`); opcional |
| `tema` | Carpeta en `themes/` (`alquimista-f100k` \| `minimalista-claro` \| `oscuro-neon`) |
| `mes` / `anio` | Mes (1–12) y año a renderizar |
| `logo` | Ruta local a PNG/SVG del logo (opcional; si no, usa iniciales) |
| `catalogoTipos` | Mapa `tipo → {bg, fg}` = color de cada chip de sesión |
| `rutinaSemanal` | Llaves `0`–`6` (0=Domingo … 6=Sábado) → lista de sesiones fijas de ese día |
| `horarios` | Llaves `0`–`6` → texto de horarios (sidebar "Recuerda los horarios") |
| `eventos` | Fechas puntuales: `{fecha:"AAAA-MM-DD", titulo, icono, fechaLabel?, atento?}` |

- Sesión: `{ "sesion": "Q&A en vivo", "tipo": "qa", "icono": "💬" }` — el color viene de `catalogoTipos[tipo]`.
- Evento con `fechaLabel` y `atento:true` (default) sale como **píldora** en la grilla **y** en "Estáte atento a". Con `atento:false` solo sale como píldora en su día.

---

## TEMAS (plantillas visuales)

Cada tema vive en `themes/<nombre>/` con `theme.json` (CSS vars + tipografía) y un `fondo.jpg` opcional:

- **`alquimista-f100k`** — el flagship (fondo de laboratorio alquimista, azul profundo). Es la marca de FÓRMULA 100K: para otra comunidad usa otro tema o genera su fondo.
- **`minimalista-claro`** — fondo claro, sin imagen, 100% CSS. Marca sobria.
- **`oscuro-neon`** — morado/neón, sin imagen, 100% CSS.

### Fondo a demanda (marca propia de una clienta)
Genera un fondo nuevo con Higgsfield (`generate_image`, `nano_banana_pro`, `aspect_ratio:"16:9"`) describiendo el nicho de la clienta. **Reglas del prompt:** centro despejado/oscuro para que la grilla se lea, detalle en los bordes, vignette, y **sin texto/números/UI**. Luego:
```bash
mkdir -p themes/<marca>/ && cp themes/alquimista-f100k/theme.json themes/<marca>/theme.json
# descarga la imagen como themes/<marca>/fondo.jpg, ajusta colores en theme.json
```
Si llega en PNG, conviértela a JPEG con Pillow para que pese menos, o déjala como `fondo.png` y cambia `"fondo"` en `theme.json`.

---

## VERIFICACIÓN

Siempre **abre el PNG generado y revísalo** antes de entregar: que las fechas caigan en el día correcto, que los chips no se desborden, que el centro del fondo no tape el texto. Si el mes empieza en un día que deja muchas celdas vacías, está bien — así es el calendario real.

---

## ARCHIVOS

```
calendario-actividades-skool-f100k/
├── SKILL.md            # esta guía
├── template.html       # grilla + sidebar + chips sobre el fondo (vanilla JS)
├── render.js           # config → grilla del mes → PNG (puppeteer-core)
├── package.json
├── referencias/
│   └── dinamicas-y-eventos.md   # ⭐ catálogo F100K: 28 dinámicas + ritmo 7 días + arco mensual (LÉELO antes de armar)
├── themes/
│   ├── alquimista-f100k/{theme.json, fondo.jpg}
│   ├── minimalista-claro/theme.json
│   └── oscuro-neon/theme.json
└── plantillas/
    ├── (la config real de FÓRMULA 100K no viaja en este paquete)
    ├── dinamicas-genericas.json # ⭐ plantilla ROBUSTA: ritmo 7 días + arco de 4 semanas, lista para clonar/recortar
    └── blanco.json              # starter mínimo para DESDE 0
```
