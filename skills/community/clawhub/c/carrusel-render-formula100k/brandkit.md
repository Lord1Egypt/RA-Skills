# Brandkit Visual — FÓRMULA 100K

> Esta es la **fuente de verdad** del estilo visual de los carruseles. Cualquier cambio aquí se aplica a todos los renders futuros.

> ⚠️ **ESTILO PREDETERMINADO (desde jul-2026): EDITORIAL OSCURO.**
> El estilo **scrapbook** crema pasó a ser ALTERNATIVO — usarlo SOLO si el usuario lo pide explícitamente ("hazlo en scrapbook / estilo diario / crema"). Por defecto, todo carrusel se renderiza en **Editorial Oscuro**. Ver más abajo el bloque "ESTILO ALTERNATIVO — Scrapbook".

---

# ═══════════════════════════════════════
# ESTILO PREDETERMINADO — EDITORIAL OSCURO
# ═══════════════════════════════════════

**Estilo:** Editorial / magazine premium tech · cinematográfico
**Sensación:** portada de revista, creadora tech aspiracional, oscuro elegante, prueba real
**Por qué funciona:** contraste altísimo (blanco sobre casi-negro) frena el scroll; la foto real full-bleed + serif itálica se lee premium y confiable; las capturas reales dan autoridad.

**Referencia canónica:** `references/editorial-oscuro-motor.js` (carrusel "Mi stack de IA"): es el motor exacto reproducible del look.

---

## PALETA — EDITORIAL OSCURO

### Base oscura
| Rol | Hex | Uso |
|---|---|---|
| Negro base | `#050509` | Fondo base de slides |
| Carbón | `#0b0b10` / `#0c0c12` | Fondo de cajas/ventanas, variación |
| Tinta ventana | `#16161d` | Barra de ventana Mac (chrome) |
| Borde ventana | `#24242e` | Bordes sutiles |

### Texto
| Rol | Hex | Uso |
|---|---|---|
| Blanco | `#FFFFFF` | Titulares principales |
| Off-white cálido | `#f4f1ea` / `#f3efe7` | Cuerpo, descripciones |
| Crema tenue | `#efe7d8` / `#e9e2d4` | Subtítulos serif |

### Acentos
| Color | Hex | Uso |
|---|---|---|
| Dorado | `#F0B24A` | Palabras clave, comillas, borde de caja CTA |
| Verde prueba | texto `#7fe3ad` · borde `rgba(127,227,173,.4)` · fondo `rgba(62,207,142,.12)` | Badge "CAPTURA REAL" |
| Morado | 💜 `#B06CFF` | Acento en CTA (corazón / énfasis) |
| Dots Mac | `#ff5f57` `#febc2e` `#28c840` | Semáforo de ventana |

**NUNCA** usar fondos crema, colores planos pastel, washi tape, post-its ni stickers-decoración en este estilo.

---

## TIPOGRAFÍA — EDITORIAL OSCURO (sin fuentes externas, 100% offline)

La firma del estilo = **mezclar SANS pesada con SERIF itálica dentro del mismo titular.**

### Sans pesada — `-apple-system, 'Helvetica Neue', Helvetica, Arial`
- **Uso:** líneas fuertes del titular, nombres, CTA principal
- **Peso:** 800
- **Letter-spacing:** negativo, −2px a −5px (cuanto más grande, más negativo)
- **Tamaños:** 78–128px titulares

### Serif editorial — `Georgia, 'Times New Roman', serif`
- **Uso:** líneas conectoras del titular ("con las que creo"), subtítulos, descripciones, rol de app entre paréntesis, el número "#N"
- **Estilos:** `italic 500` (conector), `italic 800` (línea destacada serif), `400` (cuerpo/número)
- **Tamaños:** número 62px · descripción 44px/1.35 · subtítulo 44–58px · línea serif de titular 84–128px

### Etiquetas
- **Eyebrow** (arriba-izq): sans 700, 23px, `letter-spacing:5px`, UPPERCASE, `rgba(255,255,255,.72)`, text-shadow suave
- **Handle** (arriba-der): sans 600, 23px, `rgba(255,255,255,.72)`
- **Badge CAPTURA REAL:** sans 700, 20px, letter-spacing 2px, verde, pill con borde

Todo texto sobre foto lleva `text-shadow: 0 3px 18px rgba(0,0,0,.8)` para legibilidad.

---

## FONDOS Y OVERLAYS — EDITORIAL OSCURO

**Foto:** SIEMPRE foto REAL del usuario (carpetas `MI ADN VISUAL` / `MIS SELFIES`, ver `references/fotos-reales.md`). Cinematográfica, fondo con contexto (ciudad, estudio). Nunca stock.

- **Portada / CTA (foto nítida full-bleed):**
  ```
  background-image de la foto, background-position ~50% 32%
  overlay: linear-gradient(180deg, rgba(5,5,9,.64) 0%, rgba(5,5,9,.42) 30%, rgba(5,5,9,.55) 62%, rgba(5,5,9,.93) 100%)
  ```
- **Slides interiores (misma foto desenfocada como textura):**
  ```
  background-position:50% 20%; filter:blur(22px) saturate(.7) brightness(.7); transform:scale(1.1)
  overlay: linear-gradient(180deg, rgba(4,4,7,.82) 0%, rgba(4,4,7,.72) 45%, rgba(4,4,7,.9) 100%)
  ```

---

## ESTRUCTURA DE SLIDES — EDITORIAL OSCURO

**Formato fijo:** 1080×1350px. Todos los slides `color:#fff`.

### Portada (Slide 1)
- `eyebrow` arriba-izq (tema en UPPERCASE tracked) + `handle` arriba-der
- Bloque de titular a la izquierda (~top 300px), MEZCLANDO líneas: sans 800 + serif italic 500 + serif italic 800 + `sub` serif italic
- Opcional: fila de íconos (squircles) abajo, o dejar respirar la foto

### Slides de contenido (2…N-1)
- Fondo foto desenfocada + overlay app
- `#N` número serif centrado arriba
- Fila `head` centrada: ícono squircle (132px) + título sans 800 con rol serif debajo
- `desc` serif 44px centrada (máx ~3 líneas)
- Si hay prueba: `shot` = captura REAL enmarcada en ventana Mac (barra + 3 dots + cuerpo, border-radius 16px, sombra grande), + flecha SVG dibujada a mano apuntándola + badge `CAPTURA REAL` abajo-der
- Un solo punto por slide

### CTA (Slide final)
- Fondo foto nítida + overlay
- Titular grande sans 800 + subline serif italic con **palabra clave dorada** (la keyword del "Comenta X")
- Caja glass oscura: `background:rgba(10,8,4,.55); backdrop-filter:blur(4px); border:1px solid rgba(240,178,74,.4); border-radius:22px` con cierre que vende F100K (sans 600, incluir 💜)
- Handle visible

### Íconos de apps (cuando aplique)
- Squircle: `border-radius:24%`, fondo de color de marca, `box-shadow:0 12px 26px rgba(0,0,0,.55)`, SVG de marca dentro (ver `build.js` de la referencia para los SVG de Claude/v0/Supabase/Gemini/Higgsfield/Vercel).

---

## REGLAS DURAS — EDITORIAL OSCURO (no romper)
1. Formato 1080×1350px.
2. Fondo SIEMPRE oscuro con foto real (nítida en portada/CTA, desenfocada en interiores). Nunca crema ni color plano.
3. Mezcla obligatoria sans-pesada + serif-itálica en el titular de portada/CTA.
4. Toda captura de pantalla va enmarcada en ventana Mac + badge "CAPTURA REAL". Las capturas son REALES, nunca inventadas.
5. Acento dorado `#F0B24A` para la keyword del CTA.
6. Handle del usuario (`@tuhandle`) arriba-der (portada/CTA) o donde calce; eyebrow del tema arriba-izq.
7. Cero elementos scrapbook (washi, post-its, stickers-decoración, crema).

---

## IDENTIDAD (común a ambos estilos)
- **Handle Instagram:** el del usuario — pregúntaselo la primera vez y reúsalo (`@tuhandle` es solo placeholder)
- **Comunidad:** Fórmula 100K
- **CTA estándar:** "Comenta **[PALABRA]** y te envío/enseño…" → siempre cierra vendiendo F100K
- **Fotos reales:** `cerebro/fotos` (curadas) · `cerebro/fotos` (pool)

---
---

# ═══════════════════════════════════════
# ESTILO ALTERNATIVO — SCRAPBOOK (solo si el usuario lo pide)
# ═══════════════════════════════════════

**Estilo:** Scrapbook / collage / álbum personal · cuaderno de creadora
**Cuándo:** SOLO cuando el usuario diga explícitamente "scrapbook", "estilo diario", "crema", "collage".

## Paleta scrapbook
- Crema fondo `#F5EFE0` · Crema oscuro `#EDE4CE` · Tinta `#2B2218`
- Acentos: Terracota `#C17F5A` · Salvia `#8FAF8A`
- Temáticos: Rojo `#D85A4E` · Amarillo `#F4C75B` · Morado `#B68EC8` · Verde `#9BC289` · Azul `#7FA9C9` · Rosa `#E8A8B8`
- Post-its: amarillo `#FFE881` · rosa `#FFCAD4` · verde `#CCE3B5` · azul `#BFD8E8` · morado `#DCC8E8`

## Tipografía scrapbook (Google Fonts CDN)
```html
<link href="https://fonts.googleapis.com/css2?family=Caveat:wght@400;500;600;700&family=Poppins:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
```
- **Caveat** (handwritten): títulos 100-180px, notas 36-52px
- **Poppins** (sans): cuerpo 26-30px, tags 22-26px (800, spacing 2px), CTA 30-36px (800)

## Textura de fondo scrapbook
```css
background:
  #F5EFE0
  radial-gradient(circle at 20% 30%, rgba(193,127,90,0.04) 0%, transparent 40%),
  radial-gradient(circle at 80% 70%, rgba(143,175,138,0.04) 0%, transparent 40%),
  url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='200' height='200'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='2' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 0.2  0 0 0 0 0.15  0 0 0 0 0.1  0 0 0 0.08 0'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>");
```

## Decoración scrapbook
- **Washi tape** (1-2/slide, ±5°-12°, ~140×32px, colores translúcidos de acento)
- **Post-its** (1-2/slide, Caveat, sombra ofset, cinta arriba)
- **Stickers emoji** (3-5/slide, 70-140px, drop-shadow) según tono
- **Doodles** SVG (subrayados ondulados terracota bajo palabras clave)

## Reglas scrapbook
1. 1080×1350px · 2. Fondo crema con textura (nunca blanco) · 3. Min 1 tape + 2 stickers + 1 post-it/doodle por slide · 4. Asimetría (ver `references/composiciones.md`) · 5. Slide final con CTA + "guárdalo para después" + handle · 6. Handle abajo-izq · 7. Numeración abajo-der Caveat 28px

> El ejemplo scrapbook canónico está en `references/ejemplo-completo.html` (carrusel "Chisme Silicon Valley"). Las composiciones asimétricas en `references/composiciones.md` aplican al estilo scrapbook.
