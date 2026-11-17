# Catálogo de estilos

Cada estilo es un **bloque que se copia entero** en los dos prompts de cuadro. Nunca se resume
a «retro collage style»: el modelo necesita la paleta, la textura y el tratamiento dichos.

**Regla de un video:** si un reel lleva varios clips, todos van con el MISMO estilo. Mezclar
estilos en un reel se ve como un banco de imágenes.

## Cómo elegir (por el tono de la frase que acompaña)

| La frase es… | Estilo | Por qué |
|---|---|---|
| Una idea, un sistema, algo que «se abre», tu método | `miniatura-3d-suave` | amable, premium, se lee como producto |
| Un villano, algo que se come, amenaza, crítica | `collage-retro` | el recorte de periódico hace de denuncia |
| Plata, números, anuncios, pérdidas | `editorial-oscuro` | el objeto brillando sobre negro pesa |
| Algo íntimo, un proceso creativo, «así lo pensé» | `lapiz-vivo` | el trazo sigue siendo tuyo |
| Historia, oficio, algo antiguo o con peso moral | `grabado-tenebrista` | el claroscuro le da gravedad |
| Juego, humor, algo que se arma pieza por pieza | `plastilina` | el stop-motion da risa sin chiste |
| Marca F100K, láminas de clase, la comunidad | `noche-dorada` | es la identidad del DESIGN.md |

Ofrece **3** candidatos con una línea de por qué, y recomienda uno.

---

## `miniatura-3d-suave`
*El del cofre de ideas del reel.*

```
Soft cinematic 3D miniature render, like a premium toy product shot. Rounded, slightly glossy
matte-plastic objects with gentle bevels and subtle subsurface glow. Background: a smooth
off-white seamless studio backdrop fading to pale lilac. Soft diffused key light from above,
very soft contact shadows, gentle reflections on the floor. Pastel light accents in peach,
lavender and sky blue; one saturated accent color on the hero object. Shallow depth of field,
everything in crisp focus on the main subject. Clean, uncluttered, calm.
```

## `collage-retro`
*El default de la skill original; el del banco con tentáculos.*

```
Retro paper-collage poster, physically assembled from cut paper. Grayscale or duotone vintage
photographic cutouts combined with flat saturated color shapes. Background: cream paper with
visible grain, plus one bold flat color field in mustard yellow, teal, olive green, burnt
orange or deep red. Retro newsprint halftone dot overlays on some shapes. Every cutout has
torn, hand-cut rough edges and a soft printed drop shadow. Flat, poster-like lighting with no
dramatic shadows. One or two saturated accent colors punch through the muted photographic
palette. A few thin hand-drawn doodle lines, used sparingly.
```

## `editorial-oscuro`
*El de la tarjeta de $1,000 del reel.*

```
Dark premium editorial product render. Deep near-black background with a subtle vignette.
The hero object is glossy and saturated (electric cobalt blue) with a thin bright rim light
and a faint inner glow, floating slightly above a dark reflective surface. Secondary objects
are desaturated and partly out of focus. Crisp specular highlights, rich contrast, a thin haze
in the air catching the light. Minimal, expensive, tense.
```

## `lapiz-vivo`
*El más barato de hacer creíble: el dibujo no se «mejora», se anima.*

```
Hand-drawn graphite pencil illustration on warm white sketchbook paper, loose single-weight
lines with visible pencil pressure variation, light cross-hatching only where the sketch has
it, no color except [UN SOLO ACENTO: por ejemplo, a single gold marker highlight]. Visible
paper tooth and faint eraser smudges. Flat, even scanner-like lighting. The drawing keeps the
exact wobbly, imperfect character of the original sketch — do not clean it up into vector art.
```
Movimiento que le va: *line boil* (el trazo tiembla a 12 fps), las cosas se dibujan solas,
stop-motion de papel. Pídelo así en el prompt de movimiento: `hand-drawn line boil at 12 fps`.

## `grabado-tenebrista`
*Emparentado con el corto del oidor: tinta y claroscuro.*

```
Antique copperplate engraving translated into a chiaroscuro painting. Fine parallel and
cross-hatched ink lines define every form. Background falls into deep warm black. A single hard
raking light from the upper left carves the subject out of the darkness in bone white and
aged ochre; everything else sinks into shadow. Palette limited to black, bone, ochre and one
accent of oxblood red. Aged paper texture visible in the midtones.
```

## `plastilina`

```
Handmade claymation stop-motion scene. Every object is sculpted from matte modeling clay with
visible thumbprints, slightly uneven surfaces and soft rounded edges. Miniature set on a
tabletop with a simple painted backdrop. Warm soft practical lighting like a small studio
lamp, gentle soft shadows. Saturated but friendly palette. Tiny imperfections make it feel
physically handmade.
```
Movimiento que le va: `stop-motion at 12 fps, slightly jittery, objects squash and stretch`.

## `noche-dorada`
*F100K. Colores del DESIGN.md: negro `#050509`, crema `#f4f1ea`, UN dorado `#F0B24A`.*

```
Minimal luxury graphic scene. Background: deep ink black (#050509) with a very soft warm
radial glow behind the subject. Objects are rendered in matte cream (#f4f1ea) with fine gold
(#F0B24A) edges and one gold highlight on the hero element only. Thin elegant gold line work,
subtle film grain, calm cinematic lighting, generous negative space. No other colors.
```
Gold solo en UN elemento. Si todo brilla dorado, deja de ser la firma.

---

## Texto dentro de la imagen

- Solo el texto que **está escrito en el boceto**, copiado letra por letra. No se agrega texto.
- Máximo 3 palabras. Si hay más, el texto vive en el header del reel, no en el clip.
- En el prompt de movimiento, siempre: `the text stays static and locked`. Seedance deforma las
  letras cuando se mueven.
- Si la IA escribe mal el texto, se regenera el cuadro. **Nunca** se entrega con errores.
