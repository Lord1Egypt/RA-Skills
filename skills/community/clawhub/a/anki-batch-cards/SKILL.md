---
name: anki-batch-cards
description: Batch add word cards to Anki via AnkiConnect. Supports Spanish-Chinese vocabulary cards with automatic translation and example sentences. Use when the user wants to add multiple words to Anki at once, import vocabulary lists, or bulk-create flashcards.
---

# Anki Batch Cards

Batch-add vocabulary cards to Anki with translations and example sentences.

## Requirements

- Anki running with [AnkiConnect](https://foosoft.net/projects/anki-connect/) plugin (code `2055492159`)
- Python 3

## Quick Start

```bash
python3 scripts/batch_add.py words.txt --deck "综西单词::综西单词3" --model "西语"
```

## Input Formats

### 1. TSV (recommended)

Tab-separated: `word<TAB>meaning<TAB>example (optional)`

```tsv
despertarse	醒来	Me despierto a las siete.
acostarse	睡觉	Me acuesto tarde.
```

### 2. JSON

```json
[
  {"word": "despertarse", "meaning": "醒来", "example": "Me despierto a las siete.", "tags": ["西语", "动词"]},
  {"word": "acostarse", "meaning": "睡觉", "example": "Me acuesto tarde.", "example_cn": "我很晚睡觉。"}
]
```

### 3. Plain text

One word per line (agent looks up translations automatically).

## Options

| Flag | Short | Default | Description |
|------|-------|---------|-------------|
| `--deck` | `-d` | `Default` | Target Anki deck |
| `--model` | `-m` | `西语` | Note model in Anki |
| `--field-word` | | `单词` | Word field name |
| `--field-meaning` | | `简明释义` | Meaning field name |
| `--field-example` | | `例句1` | Example field name |
| `--tags` | `-t` | `auto-import` | Comma-separated tags |
| `--test` | | | Dry run: parse & show without adding |

## Agent Workflow

1. User provides a list of words/phrases
2. Agent looks up translations and example sentences
3. Agent creates a TSV or JSON file
4. Agent runs `batch_add.py` with the file and target deck
5. Agent reports results to user

### Batch add with agent translation

When the user gives only words, the agent provides the translation and examples inline and builds the TSV file, then runs the script.

### Decks and model discovery

List available decks:

```bash
python3 -c "import urllib.request, json; print(json.loads(urllib.request.urlopen(urllib.request.Request('http://127.0.0.1:8765', json.dumps({'action':'deckNames','version':6}).encode())).read())['result'])"
```

List model fields:

```bash
python3 -c "
import urllib.request, json
req = urllib.request.Request('http://127.0.0.1:8765', json.dumps({'action':'modelFieldNames','version':6,'params':{'modelName':'西语'}}).encode())
print(json.loads(urllib.request.urlopen(req).read())['result'])
"
```

### Common Spanish model (西语) field structure

| Field | Content |
|-------|---------|
| `单词` | Spanish word / phrase |
| `简明释义` | Chinese meaning |
| `发音` | Pronunciation (optional) |
| `额外释义` | Extra meanings / usage notes |
| `例句1` | Spanish example sentence |
| `例句2` | Chinese translation of example |
| `例句3` | Additional example |
