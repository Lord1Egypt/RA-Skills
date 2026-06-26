---
name: "decklingo-pptx"
description: "Translate editable PowerPoint decks into Chinese, English, Japanese, and other target languages while preserving layout, glossary consistency, and editability. Use for PPTX localization, English-to-Chinese slides, Chinese-to-English decks, speaker note translation, and glossary-aware presentation workflows."
license: "MIT"
metadata: {"short-description":"Translate editable PPTX decks with glossary-aware verification.","openclaw":{"homepage":"https://github.com/Neabigmo/DeckLingo-for-PPTX","emoji":"🌐","requires":{"anyBins":["python","python3"],"bins":[],"env":[],"config":[]},"install":[{"id":"download-source","kind":"download","label":"Open GitHub repository","url":"https://github.com/Neabigmo/DeckLingo-for-PPTX","os":["darwin","linux","win32"]}]}}
---

# DeckLingo for PPTX

Use this skill for translation tasks on existing `.pptx` decks when the output must stay editable and visually close to the source.

It is designed to stay tool-agnostic so the same skill package can be used in Codex-style environments, OpenClaw-style environments, and other agent runtimes that can execute local scripts and read `SKILL.md`.

Install on ClawHub:

```bash
clawhub install decklingo-pptx
```

Best search phrases for this skill:

- translate powerpoint to chinese
- translate pptx to english
- localize presentation deck
- translate speaker notes in powerpoint
- glossary aware ppt translation

## What This Skill Covers

- User-selectable translation target language
- User-selectable source language, including English to Chinese workflows
- User-selectable working/output language for the skill itself
- Translation of editable text in slides, speaker notes, layouts, and slide masters
- Terminology control through glossary files
- Verification that requested source-language text no longer remains in editable text objects
- Scan-only and dry-run workflows before writing output

## Real Example Prompts

- Translate this PowerPoint from English to Simplified Chinese and keep all speaker notes editable.
- Convert this Chinese lecture deck into fluent English, but keep file names, URLs, and numbers unchanged.
- Localize this PPTX into Japanese using my glossary and tell me if any source-language text remains in layouts or masters.

## When To Use It

- Use it when the source deck must remain editable after translation.
- Use it when you need slides, notes, layouts, or masters translated selectively.
- Use it when repeated terminology should stay stable with a glossary.

## When Not To Use It

- Do not use it when the deck text is baked into screenshots or flattened images.
- Do not use it when the user wants a full visual redesign rather than translation.
- Do not use it as a generic document translator for PDFs, DOCX, or websites.

## Defaults

- `source language`: `auto`
- `target language`: infer from the request; if not clear, use the most obvious requested language
- `english -> chinese` is a first-class workflow, not a fallback case
- `working/output language`: use the user's current language by default
- `translation scope`: slides on, notes on, layouts off, masters off unless the user requests a full inherited-text cleanup

Keep these separate:

- **Target language**: the language written into the deck
- **Working language**: the language used in logs, summaries, and user-facing notes

## Workflow

1. Determine:
   - input PPTX path
   - output PPTX path
   - source language
   - target language
   - working language
   - whether notes/layouts/masters should be translated
2. Run the scan script first when the deck is unfamiliar or large.
3. Prefer XML-level translation so the deck remains editable and layout drift stays low.
4. Translate paragraph-sized text instead of isolated run fragments whenever possible.
5. Preserve numbers, dates, URLs, filenames, code snippets, and product names unless translation is clearly needed.
6. Re-scan the result and report:
   - output file path
   - paragraph counts
   - glossary usage
   - any remaining source-language text in editable objects

## Scripts

Use the bundled scripts:

```bash
python .trae/skills/decklingo-pptx/scripts/scan_pptx_text.py \
  --input "path/to/input.pptx" \
  --source-lang zh \
  --include-notes \
  --include-layouts \
  --include-masters
```

```bash
python .trae/skills/decklingo-pptx/scripts/translate_pptx_text.py \
  --input "path/to/input.pptx" \
  --output "path/to/output.pptx" \
  --source-lang auto \
  --target-lang en \
  --ui-lang zh \
  --include-notes \
  --glossary-file ".trae/skills/decklingo-pptx/assets/glossary.sample.json" \
  --report-file "translation-report.json"
```

## Common Options

- `--source-lang`: source language code, default `auto`
- `--target-lang`: target language code such as `en`, `ja`, `fr`, `de`, `zh-CN`
- `--ui-lang`: language for logs and summaries, usually `zh` or `en`
- `--include-notes`: include speaker notes
- `--include-layouts`: include slide layouts
- `--include-masters`: include slide masters
- `--glossary-file`: JSON glossary mapping source terms to preferred translations
- `--skip-pattern-file`: regex patterns to protect text like URLs, file names, code identifiers, or custom labels
- `--report-file`: write a machine-readable JSON report
- `--dry-run`: inspect and translate in memory without writing a new deck
- `--backup-suffix`: backup suffix used when translating in place, default `.bak`

## When To Load References

- Read [references/glossary-schema.md](./references/glossary-schema.md) when you need to create or edit a glossary file.
- Read [references/translation-modes.md](./references/translation-modes.md) when choosing whether to include notes, layouts, or masters.
- Read [references/platform-compatibility.md](./references/platform-compatibility.md) when packaging the skill for Codex, OpenClaw, or another agent runtime.

## Notes

- Reuse or patch a better project-local translator if the repository already contains one.
- If network translation is required, verify connectivity first.
- If the user asks for design cleanup after translation, pair this skill with a slide-layout skill rather than rebuilding the deck here.
- Treat third-party skills and scripts as untrusted code and review them before enabling.
- Minimal runtime requirements: Python 3.10+, `lxml`, `deep-translator`, ZIP read/write access.
- Changelog: see [references/changelog.md](./references/changelog.md).
