# Flashcard Forge

> Turn walls of text into decks you'll actually review.

A [Hermes Agent](https://hermes-agent.nousresearch.com/docs) / OpenClaw skill
that converts study material — PDF excerpts, lecture notes, articles, textbook
chapters — into **Anki-importable flashcards** using regex-based extraction and
sentence analysis.

## Why

Students spend hours manually making flashcards from reading material. Most of
that work is mechanical: find the definitions, extract the key facts, format
them as Q&A or cloze cards. Flashcard Forge automates the extraction so you can
focus on reviewing, not transcribing.

## What's Included

- **`SKILL.md`** — core skill: modes, quick-reference table, how-it-works.
- **`references/`**
  - `extraction-patterns.md` — catalog of regex patterns the extractor uses.
  - `anki-import.md` — step-by-step guide to importing CSV into Anki.
  - `study-strategies.md` — best practices for flashcard-based learning.
- **`scripts/flashcard_forge.py`** — the main script (stdlib only, no deps).
- **`scripts/sample_text.txt`** — example input demonstrating all pattern types.

## Quick Start

```bash
# Generate Q&A flashcards (default mode)
python3 scripts/flashcard_forge.py notes.txt -o deck.csv

# Generate cloze (fill-in-the-blank) cards
python3 scripts/flashcard_forge.py notes.txt --mode cloze -o cloze.csv

# Auto mode: both Q&A and cloze, deduplicated
python3 scripts/flashcard_forge.py notes.txt --mode auto -o deck.csv

# Cap output to 50 cards, filter short sentences
python3 scripts/flashcard_forge.py notes.txt --max-cards 50 --min-length 25

# JSON output for programmatic use
python3 scripts/flashcard_forge.py notes.txt --format json -o deck.json
```

Example CSV output:

```
Front;Back
"What is photosynthesis?";"The process by which plants convert light energy into chemical energy"
"Mitochondria";"The powerhouse of the cell, responsible for ATP production"
```

Example cloze output:

```
Text;Extra
"The powerhouse of the cell is the {{c1::mitochondria}}";""
"Photosynthesis occurs in the {{c1::chloroplasts}} of plant cells";""
```

## Modes

| Mode    | Card Type  | Best For                          |
| ------- | ---------- | --------------------------------- |
| `qa`    | Basic Q&A  | Definitions, explicit questions   |
| `cloze` | Cloze      | Fill-in-the-blank memorization    |
| `auto`  | Both       | General use (default)             |

## Anki Import

1. Open Anki → File → Import
2. Select the CSV file
3. Set type to **Basic** (for qa) or **Cloze** (for cloze)
4. Ensure field separator is semicolon (`;`)
5. Click Import

See `references/anki-import.md` for detailed instructions with screenshots.

## Installation (Hermes Agent)

Copy or symlink this directory into your skills folder:

```bash
cp -r flashcard-forge ~/.hermes/skills/
```

Hermes auto-discovers skills with a valid `SKILL.md`. See the
[skills docs](https://hermes-agent.nousresearch.com/docs) for details.

## Requirements

- Python 3.8+ (stdlib only — no pip install needed)

## License

MIT © Denis Voronin
