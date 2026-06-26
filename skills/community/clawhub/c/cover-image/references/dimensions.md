# Cover Image Dimensions

## Type

| Value | Best For |
| --- | --- |
| `hero` | one main subject with a strong focal center |
| `conceptual` | abstract ideas, opinion pieces, trend analysis |
| `typography` | title-led designs with supporting visuals |
| `metaphor` | content that needs a visual metaphor |
| `scene` | narrative scenes, atmosphere, world-building |
| `minimal` | restrained, brand-like visuals with more whitespace |

## Palette

| Value | Visual Feel |
| --- | --- |
| `warm` | friendly, warm, lifestyle-oriented |
| `elegant` | restrained, refined, premium |
| `cool` | technical, rational, professional |
| `dark` | dark, cinematic, immersive |
| `earth` | natural, human, documentary-like |
| `vivid` | saturated, eye-catching, social-friendly |
| `pastel` | soft, light, healing |
| `mono` | monochrome or near-monochrome minimalism |

## Rendering

| Value | Recommended Mapping |
| --- | --- |
| `editorial` | `--style editorial` |
| `poster` | `--style poster` |
| `cinematic` | `--style cinematic` |
| `watercolor` | `--style watercolor` |
| `flat-vector` | `--style flat-illustration` |
| `ink-brush` | `--style ink-brush` |
| `chalk` | `--style chalk` |
| `manga` | `--style manga` |
| `anime` | `--style anime` |
| `photoreal` | `--style photoreal` |
| `3d-render` | `--style 3d-render` |
| `infographic` | `--style infographic` |

## Text

| Value | Meaning |
| --- | --- |
| `none` | pure visual cover with no image text dependency |
| `title-only` | reserve a clear title area |
| `title-subtitle` | reserve title and subtitle zones |
| `text-rich` | more information layers, but still image-first |

## Mood

| Value | Meaning |
| --- | --- |
| `subtle` | quiet, low-contrast, restrained |
| `balanced` | default; clear focus without excessive intensity |
| `bold` | high-contrast, high-impact, distribution-oriented |

## Aspect

Recommended defaults:

- `16:9` for general article covers and shareable hero images
- `2.35:1` for stronger banner or cinematic composition
- `1:1` for social covers
- `3:4` for portrait card covers

## Language

Recommendations:

- follow the user's language by default
- a purely visual cover may not need a language note
- if the image contains a title, subtitle, or labels, state the target language explicitly in the prompt
