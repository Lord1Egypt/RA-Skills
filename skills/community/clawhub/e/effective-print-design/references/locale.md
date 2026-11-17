# Locale Conventions Reference

Locale-specific typography rules for Western languages. See SKILL.md for principles.

## Quotation Marks

Set correct quotation marks per language using the CSS `quotes` property:

```css
html[lang="de"] { quotes: "„" "\201C" "‚" "\2018"; }
html[lang="en"] { quotes: "\201C" "\201D" "\2018" "\2019"; }
q { quotes: auto; }  /* let browser pick from lang attribute */
```

| Locale | Primary | Unicode | Secondary | Unicode |
|--------|---------|---------|-----------|---------|
| en-US | "…" | U+201C / U+201D | '…' | U+2018 / U+2019 |
| en-GB | '…' | U+2018 / U+2019 | "…" | U+201C / U+201D |
| de-DE/AT | „…" | U+201E / U+201C | ‚…' | U+201A / U+2018 |
| de-CH | «…» | U+00AB / U+00BB | ‹…› | U+2039 / U+203A |
| fr-FR | « … » | U+00AB nbsp … nbsp U+00BB | "…" | U+201C / U+201D |
| es-ES | «…» | U+00AB / U+00BB | "…" | U+201C / U+201D |
| it-IT | «…» or "…" | varies | '…' | U+2018 / U+2019 |
| pt-PT | «…» | U+00AB / U+00BB | "…" | U+201C / U+201D |
| pt-BR | "…" | U+201C / U+201D | '…' | U+2018 / U+2019 |
| nl-NL | '…' (modern) | U+2018 / U+2019 | "…" | U+201C / U+201D |
| nl-BE | «…» | U+00AB / U+00BB | "…" | U+201C / U+201D |
| pl-PL | „…" | U+201E / U+201D | «…» | U+00AB / U+00BB |

German guillemets point **inward** (»text«). French guillemets require nbsp **inside** (« text »). Swiss guillemets follow French direction (outward) but without internal spacing.

**Thin space** (`&thinsp;`, U+2009) between nested quotation marks to prevent visual merging: "She said 'hello' " — insert thin space between ' and ".

## Dashes

| Locale | Parenthetical | Spacing | Range |
|--------|---------------|---------|-------|
| en-US | Em dash — (U+2014) | No spaces | En dash, no spaces |
| en-GB | En dash – (U+2013) | Spaced: word – word | En dash, no spaces |
| de-DE/AT/CH | En dash – (U+2013) | Spaced: Wort – Wort | En dash, no spaces |
| fr-FR | En dash – (U+2013) | Spaced: mot – mot | En dash, no spaces |
| es-ES | Em dash — (U+2014) | Space before, not inside | En dash, no spaces |
| it-IT | Em or En dash | Spaced | En dash, no spaces |
| pt-PT/BR | Em dash — (U+2014) | Spaced | En dash, no spaces |
| nl-NL | En or Em dash | Spaced | En dash, no spaces |
| pl-PL | Em dash — (U+2014) | Spaced | En dash, no spaces |

## Number Formatting

| Locale | Decimal | Thousands | Example | Currency position |
|--------|---------|-----------|---------|-------------------|
| en-US/GB | `.` | `,` | 1,234.56 | Before, no space: $1,234.56 |
| de-DE/AT | `,` | `.` | 1.234,56 | After, space: 1.234,56 € |
| de-CH | `.` | `'` | 1'234.56 | After, space: 1'234.56 CHF |
| fr-FR | `,` | ` ` (nnbsp) | 1 234,56 | After, nnbsp: 1 234,56 € |
| es-ES | `,` | `.` | 1.234,56 | After, space: 1.234,56 € |
| it-IT | `,` | `.` | 1.234,56 | After, space: 1.234,56 € |
| pt-PT | `,` | `.` | 1.234,56 | After, space: 1.234,56 € |
| pt-BR | `,` | `.` | 1.234,56 | Before, no space: R$1.234,56 |
| nl-NL | `,` | `.` | 1.234,56 | Before, space: € 1.234,56 |
| pl-PL | `,` | ` ` (nbsp) | 1 234,56 | After, space: 1 234,56 zł |

**Unit spacing:** Non-breaking space between number and unit: `10 kg`, `100 %`, `20 °C` (ISO 80000-1). Use narrow no-break space (U+202F) for tighter fit.

## French Punctuation Spacing

French is unique among Western languages — mandatory non-breaking space before high punctuation:

| Mark | Space before | Type |
|------|-------------|------|
| `:` (colon) | Yes | No-break space (U+00A0) |
| `;` `?` `!` | Yes | Narrow no-break space (U+202F) |
| `«` (opening) | Space after | No-break space (U+00A0) |
| `»` (closing) | Space before | No-break space (U+00A0) |

The colon takes a full nbsp; semicolon, question mark, and exclamation take a **narrow** nbsp (Imprimerie nationale rules). Handle via preprocessor or `lang="fr"` specific rules.

## Typographic Preprocessing

Automate character substitution at build time instead of manual Unicode input:

| Tool | Key features |
|------|-------------|
| SmartyPants / smartypants.js | Curly quotes, en/em dashes, ellipsis (English-centric) |
| richtypo.js | **Locale-aware** — per-language rule packages, widow prevention |
| Tipograph | **Locale-aware** — configurable presets per locale |
| Typeset | Hanging punctuation, optical alignment, ligatures, soft hyphens |
| typogr.js | Wraps elements in `<span>` for CSS styling (ampersands, caps, widows) |

**Common transformations:** `"` → "…", `'` → '…', `--` → –, `---` → —, `...` → …, widow prevention (nbsp between last two words). Locale-aware tools handle quote direction, dash style, and spacing rules per language automatically.
