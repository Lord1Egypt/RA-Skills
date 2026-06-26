# ClawPurse Website — Internationalization (i18n)

Multi-language build system for [clawpurse.ai](https://clawpurse.ai).

## Supported Languages (8)

| Code | Language | Native Name | Extra Font |
|------|----------|-------------|------------|
| `en` | English | English | — |
| `ja` | Japanese | 日本語 | Noto Sans JP |
| `ko` | Korean | 한국어 | Noto Sans KR |
| `es` | Spanish | Español | — |
| `fr` | French | Français | — |
| `hi` | Hindi | हिन्दी | Noto Sans Devanagari |
| `zh` | Mandarin (Simplified) | 中文 | Noto Sans SC |
| `id` | Indonesian | Bahasa Indonesia | — |

## Architecture

```
clawpurse-i18n/
├── build.js           # Node.js build script
├── template.html      # Single HTML template with {{key}} placeholders
├── locales/
│   ├── en.json        # English (source of truth)
│   ├── ja.json        # Japanese
│   ├── ko.json        # Korean
│   ├── es.json        # Spanish
│   ├── fr.json        # French
│   ├── hi.json        # Hindi
│   ├── zh.json        # Mandarin
│   └── id.json        # Indonesian
└── dist/              # Built output (generated)
    ├── index.html     # English (root)
    ├── sitemap.xml    # Multi-language sitemap with hreflang
    ├── en/index.html
    ├── ja/index.html
    ├── ko/index.html
    ├── es/index.html
    ├── fr/index.html
    ├── hi/index.html
    ├── zh/index.html
    └── id/index.html
```

## How to Build

```bash
node build.js
```

No dependencies required — uses only Node.js built-in modules.

## How to Deploy (GitHub Pages)

Copy the contents of `dist/` to your `www/` folder:

```bash
# From your ClawPurse repo root
cp -r clawpurse-i18n/dist/* www/
git add www/
git commit -m "Add multi-language support"
git push
```

## URL Structure

| Language | URL |
|----------|-----|
| English (default) | `https://clawpurse.ai/` |
| Japanese | `https://clawpurse.ai/ja/` |
| Korean | `https://clawpurse.ai/ko/` |
| Spanish | `https://clawpurse.ai/es/` |
| French | `https://clawpurse.ai/fr/` |
| Hindi | `https://clawpurse.ai/hi/` |
| Mandarin | `https://clawpurse.ai/zh/` |
| Indonesian | `https://clawpurse.ai/id/` |

## SEO Features

- `<html lang="xx">` attribute per page
- `<link rel="canonical">` per language
- `hreflang` alternate links (all 8 languages + x-default)
- `sitemap.xml` with `xhtml:link` hreflang entries
- Locale-specific meta titles and descriptions
- Structured data (JSON-LD) per page

## Adding a New Language

1. Copy `locales/en.json` to `locales/<code>.json`
2. Translate all values (keep keys identical)
3. Update `meta.lang` to the ISO 639-1 code
4. If the language needs a special font, add it to `meta.fontImport`
5. Add the language to `LANG_NAMES` in `build.js`
6. Run `node build.js`

## Translation Notes

- **Brand names stay untranslated**: ClawPurse, NTMPI, Neutaro, Timpi, OpenClaw, Timpi Drip
- **Technical terms stay in English**: CLI, API, Docker, JWT, SQLite, AES-256, HTTP 402
- **Code snippets stay in English**: command examples, code blocks, headers/protocols
- The `fontImport` field in `meta` adds locale-specific Google Fonts (CJK, Devanagari)
- All 8 locales have been verified to have identical key structures (137 keys each)

## Translation Review Recommendations

These AI-generated translations should be reviewed by native speakers, especially for:
- **Japanese (ja)**: Technical blockchain terminology nuance
- **Korean (ko)**: Formal/informal register consistency
- **Mandarin (zh)**: Simplified Chinese character accuracy
- **Hindi (hi)**: Devanagari script rendering and technical term transliteration choices
