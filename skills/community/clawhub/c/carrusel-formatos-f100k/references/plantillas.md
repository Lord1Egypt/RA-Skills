# Plantillas propias · formato del JSON

Todas se diseñan a 1080×1350 y se exportan al doble (2160×2700, como las otras skills de carrusel). Se arman con:

```bash
node skills/carrusel-formatos-f100k/build.js /ruta/spec.json [carpeta-salida]
```

`build.js` inyecta el JSON en la plantilla, abre la página, espera fuentes + imágenes +
autofit, imprime avisos (`⚠ no-cabe`, `⚠ letra-chica`, `⚠ fuente`, `⚠ imagen`) y exporta con
el `export.js` de `carrusel-render-formula100k` → `slide-01.png`, `slide-02.png`…
`--sin-png` solo revisa.

**Marcado de texto** (cualquier campo de texto):
`**negrita**` · `*itálica*` · `==resaltador==` · `__subrayado rojo__` · `\n` salto de línea.

**Fotos**: ruta (absoluta o relativa al spec) · `{ "src": "...", "foco": "50% 20%" }` · `{ "color": "#333" }`.

Campos comunes: `"plantilla"`, `"handle"` (firma), y `"slides": [...]`.
Ejemplos completos que ya renderizan: `ejemplos/split.json`, `ejemplos/papel.json`, `ejemplos/datos.json`, `ejemplos/garabato.json`.

---

## split.html · F01, F02, F05

Campos del spec: `estilo` (`fino` | `titular`, por defecto `fino`; se puede poner por slide), `acento` (color del texto de abajo en `titular`), `etiqueta` (texto arriba en la cuadrícula, ej. "10/10 hábitos"), `swipe` (true → chip "desliza ›").

| `tipo` de slide | Campos | Ficha |
|---|---|---|
| `partida` | `arriba: {foto, texto, pos}`, `abajo: {foto, texto, pos}`, `estilo` | F01 (`fino`), F02 (`titular`) |
| `habito` | `titulo`, `fotos: [arribaIzq, arribaDer, abajoIzq]`, `bloque: {normal, italica, negrita}` | F05 |
| `portada` / `pregunta` | `foto`, `titulo`, `sub`, `alinear: "izquierda"` | portada o cierre de F05/F10 |

`pos` (solo `fino`): `arriba` | `abajo` | centro por defecto. Úsalo para no tapar la cara.

## papel.html · F04, F06, F07, F08

Campos del spec: `variante` (`libreta` | `espiral` | `agenda`; se puede poner por slide), `fondo` (foto de fondo opcional: apaga el papel CSS) + `caja: {x, y, w, h}` (dónde va el texto sobre esa foto).

Cada slide: `variante`, `alinear: "centro"`, `bloques: [...]`.

| Bloque | Campos |
|---|---|
| `titulo` · `texto` · `nota` · `grande` | `texto` |
| `lista` (viñetas) · `check` (✓) | `items: []` |
| `chuleta` (nodo + filas unidas con líneas, F07) | `centro`, `filas: [["dato","qué hace"], ...]` |
| `imagen` (sticker, F06) | `src` |
| `espacio` | — |

Tinta: libreta negra · espiral azul bolígrafo · agenda gris oscuro (Patrick Hand).

**Renglones (espiral y agenda):** después del autofit la plantilla mide el interlineado del texto chico, ajusta
todos los bloques a múltiplos de ese paso, corre cada bloque hasta que su línea base cae en la rejilla y dibuja
el papel con ese paso. Deja un renglón en blanco entre bloques. Si al ajustar deja de caber, avisa `⚠ no-cabe`.
La libreta no tiene renglones. Con `fondo` (foto) no se dibujan.

## datos.html · F17, F18, F19

| `tipo` de slide | Campos | Ficha |
|---|---|---|
| `tier` | `titulo`, `filas: [{nivel: "S", etiqueta, items: [{nombre, img}]}]` | F17 |
| `cifras` | `titulo`, `sub`, `nota`, `fondo` (opcional), `items: [{nombre, valor, unidad}]` | F18 |
| `mapa` | `centro` (usa `|` para dos niveles: "Hazme un|videíto"), `ramas: [{texto, nota}]` (8-14) | F19 |
| `cierre` | `texto`, `sub` | último slide de cualquiera |

`cifras` sin `fondo` dibuja barras proporcionales. Con `fondo` (imagen IA de objetos apilados, SIN texto) las barras se vuelven invisibles y quedan solo cifras y nombres encima: ordena los objetos de la imagen igual que `items`.

## garabato.html · F13

Foto a sangre + letra manuscrita + trazos que SEÑALAN algo de la foto. Todas las coordenadas en px sobre 1080×1350:
**mira la foto recortada a 4:5 antes de ponerlas** (ImageOps.fit a 1080×1350 con una rejilla ayuda).

Campos del spec: `color` (trazo y letra, por defecto `#FFD60A`), `grosor` (7).

| Campo de slide | Qué es |
|---|---|
| `foto` | ruta o `{src, foco}` |
| `cara` | `{x, y, w, h}` de la cara: si una nota la tapa, avisa `⚠ no-cabe` |
| `notas` | `[{texto, x, y, w, h, px, rot, alinear, flecha: {desde: [x,y], hasta: [x,y], curva}}]` |
| `circulos` | `[{x, y, rx, ry, rot}]` imperfectos, dos vueltas |
| `subrayados` | `[{x, y, w, doble}]` |
| `contorno` | `{x, y, w, h}` óvalo suelto alrededor de la silueta (no es un recorte exacto) |
| `velo` | `"arriba"` / `"abajo"`: degradado negro para cielos muy claros |
| `swipe` | `true` → flecha «→» arriba a la derecha |

## HTML libre · estilos de la guía maestra (S17–S28) y fichas G

Para lo que no tiene plantilla propia (checklist con casillas, chat, nota del celular, periódico, recibo, terminal,
bento, barra de progreso, pieles tipográficas), Claude escribe el HTML siguiendo el **prompt del estilo** en
`references/estilos-guia-maestra.md` y el **visual de la ficha** en `references/prompts-por-plataforma.md`.

Contrato (build.js lo revisa):
- cada slide es un `<section class="slide">` de exactamente **1080×1350**;
- fuentes de Google Fonts con `<link>`; nunca `-apple-system` (en Chrome headless cae a Times);
- nada de texto fuera del slide; la decoración que sangra a propósito va dentro de un elemento con `data-sangra`;
- imágenes con ruta absoluta `file://` o relativa al HTML.

```bash
node skills/carrusel-formatos-f100k/build.js <carpeta>/carrusel.html
```
Avisa `⚠ no-cabe` (texto que se sale o se corta, slide de otro tamaño), `⚠ fuente` (familia que no cargó con
su peso real, o `-apple-system`), `⚠ imagen`.
