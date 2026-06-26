# DeckLingo for PPTX

Translate editable PowerPoint decks into your chosen language while keeping layout, terminology, and editability as stable as possible.

Available on ClawHub:

```bash
clawhub install decklingo-pptx
```

## English

DeckLingo for PPTX translates editable PowerPoint decks without flattening the slides. It supports English to Chinese, Chinese to English, glossary-aware terminology control, selective translation of notes/layouts/masters, and verification after translation.

## 中文

DeckLingo for PPTX 用来翻译可编辑的 PowerPoint，而不是把整套幻灯片打平成图片后再替换文字。它支持英文转中文、中文转英文、术语表控制、备注/版式/母版选择性翻译，以及翻译后的校验。

## 日本語

DeckLingo for PPTX は、スライドを画像化せずに編集可能な PowerPoint をそのまま翻訳するためのツールです。英語から中国語、中国語から英語、用語集による用語統一、ノート/レイアウト/マスターの選択翻訳、翻訳後の検証に対応しています。

## Why This Exists

Most PPT translation workflows flatten slides, damage layout, or ignore speaker notes and inherited template text. DeckLingo for PPTX works directly on editable PPTX text and is designed for agent workflows, skill marketplaces, and local automation.

## Highlights

- Editable PPTX translation instead of image-based replacement
- Source language and target language are both configurable
- Interaction/output language is configurable separately
- English to Chinese and Chinese to English are both first-class workflows
- Optional translation of notes, layouts, and slide masters
- Glossary support for stable terminology
- Skip-pattern support for URLs, file names, identifiers, and protected text
- Preflight scan script and post-translation verification
- Works as a self-contained skill package for Codex-style and OpenClaw-style runtimes

## Search-Friendly Use Cases

- Translate PowerPoint to Chinese
- Translate PPTX to English
- Localize presentation decks
- Translate speaker notes in PowerPoint
- Keep PowerPoint layout after translation
- Glossary-aware slide translation

## Quick Start

Install dependencies:

```bash
pip install -r requirements.txt
```

Scan a deck before translating:

```bash
python scripts/scan_pptx_text.py \
  --input "example.pptx" \
  --source-lang en \
  --include-notes
```

Translate English to Simplified Chinese:

```bash
python scripts/translate_pptx_text.py \
  --input "example.pptx" \
  --output "example.zh-CN.pptx" \
  --source-lang en \
  --target-lang zh-CN \
  --ui-lang zh \
  --include-notes \
  --report-file "translation-report.json"
```

Translate Chinese to English with a glossary:

```bash
python scripts/translate_pptx_text.py \
  --input "example.pptx" \
  --output "example.en.pptx" \
  --source-lang zh \
  --target-lang en \
  --ui-lang en \
  --include-notes \
  --glossary-file "assets/glossary.sample.json"
```

## Runtime Compatibility

- Codex-style skill runtimes
- OpenClaw-style local agent platforms
- Any local agent system that can read `SKILL.md` and execute Python scripts

Platform notes are in [references/platform-compatibility.md](./references/platform-compatibility.md).

## Real Example Prompts

- Translate this PowerPoint from English to Simplified Chinese and keep all speaker notes editable.
- Convert this Chinese lecture deck into fluent English, but keep file names, URLs, and numbers unchanged.
- Localize this PPTX into Japanese using my glossary and tell me if any source-language text remains in layouts or masters.

## When To Use It / When Not To Use It

- Use it when you need editable PPT translation with minimal layout drift.
- Use it when the deck includes speaker notes or inherited template text that also needs translation.
- Do not use it when all text is rasterized inside images.
- Do not use it when the goal is visual redesign rather than translation.

## Project Structure

- [SKILL.md](./SKILL.md): primary skill instructions
- [agents/openai.yaml](./agents/openai.yaml): marketplace-style metadata
- [scripts/scan_pptx_text.py](./scripts/scan_pptx_text.py): preflight scan
- [scripts/translate_pptx_text.py](./scripts/translate_pptx_text.py): translation entrypoint
- [assets/glossary.sample.json](./assets/glossary.sample.json): sample glossary
- [assets/skip_patterns.sample.txt](./assets/skip_patterns.sample.txt): sample protected-text rules

## Validation

Validated locally on:

- `4.  Microbial metabolism 2026.pptx`
- Workflow: `English -> zh-CN`
- Result: scan succeeded, translation succeeded, output deck written, verification passed

## OpenClaw / ClawHub Notes

- Discovery depends on name, description, tags, and usage signals, not only exact keyword matches.
- This repository uses search-friendly copy so users can find it with natural tasks like "translate PowerPoint to Chinese".
- For publishing, use:

```bash
clawhub publish ./DeckLingo-for-PPTX --slug decklingo-pptx --name "DeckLingo for PPTX" --version 1.0.0 --changelog "Initial public release" --tags latest,pptx,powerpoint,translation,localization,slides,english-to-chinese,chinese-to-english,glossary,openclaw,codex
```

## Marketplace Copy

Multi-language listing copy is available in [references/market-listing.md](./references/market-listing.md).

## Changelog

See [references/changelog.md](./references/changelog.md).

## Author

Yang Yiheng  
yangyiheng00711@gmail.com
