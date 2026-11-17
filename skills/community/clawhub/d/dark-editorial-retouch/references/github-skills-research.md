# Skills de GitHub que se usaron como referencia

Busqueda hecha el 2026-10-23 con `gh search repos` + `gh api` (contenido real, no solo
descripciones). Estos repos aportaron estructura o criterios que estan aplicados en
`skills/dark-editorial-retouch/`.

## 1. `anthropics/skills` (183k ★)

Coleccion de skills oficiales de Anthropic, con el formato `SKILL.md` + frontmatter
(`name`, `description`, `license`). Es el estandar que sigue esta skill.

- `skills/canvas-design` — filosofia de diseño antes de ejecutar: definir una tesis
  visual y recien despues producir. **Aplicado:** la skill define "clave baja editorial"
  como tesis y deriva todas las perillas de ahi; el texto de la marca queda como unico
  acento grafico.
  https://github.com/anthropics/skills/blob/main/skills/canvas-design/SKILL.md
- `skills/brand-guidelines` — paleta y tipografia como contrato, con variantes por
  contexto. **Aplicado:** `assets/brand/` con 5 variantes de la insignia (knockout,
  lineas, color, monocromo oscuro, tamanos de avatar) y la regla de cuando usar cada una;
  la insignia a color nunca se recolorea (ver `references/logo-integration.md`).
  https://github.com/anthropics/skills/blob/main/skills/brand-guidelines/SKILL.md

## 2. `ComposioHQ/awesome-claude-skills` (77k ★)

Indice curado; de ahi salio el patron "skill = instrucciones + activos + script
ejecutable" y la skill `image-enhancer` (analizar calidad → upscale → sharpening →
reduccion de artefactos → optimizar por caso de uso). **Aplicado:** `analyze()` mide
entrada y salida (p01/p50/p99, clipping, cast) y el reporte JSON documenta la mejora.
https://github.com/ComposioHQ/awesome-claude-skills/blob/main/image-enhancer/SKILL.md

## 3. `remotion-dev/skills` (5.5k ★)

Skills de motion graphics programatico (`remotion-render`, `remotion-multimedia`,
`remotion-best-practices`). No se usan para editar fotos, pero aportaron el criterio de
"frame como unidad de diseño": composicion, jerarquia y continuidad entre tomas.
**Aplicado:** `references/motion-language.md` y la consistencia de serie (mismo preset,
misma posicion y tamano de marca).
https://github.com/remotion-dev/skills

## 4. `vercel-labs/skills` / `vercel-labs/agent-skills` (36k / 32k ★)

Distribucion de skills con CLI y estructura de carpetas; convencion de `references/`
como documentacion de apoyo que se carga solo cuando hace falta. **Aplicado:** la skill
mantiene `SKILL.md` corto y mueve el detalle tecnico a `references/`.
https://github.com/vercel-labs/skills

## 5. Referencias tecnicas de retoque (no skills, pero verificables)

- Dodge & burn no destructivo con capa gris 50% en Soft Light / dos capas de curvas, y
  la advertencia de que las herramientas nativas corren color:
  https://gdefoto.com/en/articles/dodge-and-burn-photoshop
- Separacion de frecuencias + dodge & burn como pareja (textura vs forma):
  https://fixanyphoto.com/guide/high-end-retouching-techniques/
- Halation: halo calido por estructura de emulsion y selectividad espacial (Kodak,
  Wikipedia *Film emulation*, guias de coloristas):
  https://en.wikipedia.org/wiki/Film_emulation · https://www.kodak.com/en/motion/page/glossary-of-motion-picture-terms/
- Rolloff de altas luces / hombro de la curva caracteristica:
  https://pixeltoolspost.com/blogs/resolve/film-emulation-explained
- Colocacion de marca en fotografia (5-20% del ancho, esquina, zona tranquila, espacio
  de resguardo, contraste):
  https://barnimages.com/blog/tips/adding-a-logo-to-social-media-graphics/

> Nota: no se copio codigo de terceros. Se tomaron criterios de estructura (formato de
> skill, separacion instrucciones/referencias) y conocimiento fotografico publico; toda
> la implementacion de `retouch.py` y `prepare_brand.py` es original y solo depende de
> numpy / scipy / Pillow / pillow-heif.
