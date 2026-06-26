# Cohere Translator Skill

State-of-the-art neural machine translation using Cohere's **Command A Translate** model
(`cohere/command-a-translate-08-2025`, 111B parameters, 23 languages).

> **🔑 Requires a Cohere API key.** The model is free for trial keys as of 2026-05-17
> (1,000 calls/month, 20 req/min). Get a key at: https://dashboard.cohere.com/api-keys

## ⚠️ CRITICAL: Always Use File Mode to Save Tokens

**When translating file content, use `--file`/`-f` mode.** This bypasses the agent
entirely — the script reads the file directly and translates it. Your agent never
loads the file content into its context window.

```bash
# ❌ WASTES TOKENS: Agent reads file → passes text as CLI argument
python3 translate.py "$(cat document.txt)" --to ja

# ✅ ZERO AGENT TOKENS: Script reads file directly, agent only issues the command
python3 translate.py -f document.txt --to ja -o output.txt
```

**This is not optional advice — it is the correct way to use this skill.**
Every byte of text you pass through the agent as a CLI argument doubles your token
cost for no benefit. File mode eliminates this entirely.

This applies equally when using the skill from an agent (OpenClaw, Claude Code, etc.)
or directly from the command line.

## Quick Start

```bash
# 1. Set your Cohere API key (get one at https://dashboard.cohere.com/api-keys)
export COHERE_API_KEY="your-key-here"

# 2. Translate a file (RECOMMENDED — zero agent tokens)
python3 skills/cohere-translator/scripts/translate.py -f input.txt --to ja -o output.txt

# 3. Quick one-liner (text on command line — small texts only)
python3 skills/cohere-translator/scripts/translate.py "Hello" --to ja
# → こんにちは
```

## Usage Modes

### File Mode (RECOMMENDED)

```bash
# File → file
python3 translate.py -f document.txt --to ja -o translated.txt

# File → stdout
python3 translate.py -f document.txt --to en

# Stdin → stdout
cat document.txt | python3 translate.py -f - --to ja

# Stdin → file
cat document.txt | python3 translate.py -f - --to ja -o output.txt

# Large files auto-chunked (6,000+ chars automatically split)
python3 translate.py -f large_document.txt --to ja -o output.txt
# Output: 📄 12000 chars → 16 chunks ... ✓ 16/16
```

### Text Mode (small texts only)

```bash
python3 translate.py "Hello world" --to ja    # EN→JA
python3 translate.py "こんにちは" --to en     # JA→EN
python3 translate.py "Bonjour" --to es        # FR→ES
```

## Supported Language Codes

```
en: English     ja: Japanese     zh: Chinese     ko: Korean
fr: French      de: German       es: Spanish     it: Italian
pt: Portuguese  ar: Arabic       ru: Russian     pl: Polish
tr: Turkish     vi: Vietnamese   nl: Dutch       cs: Czech
id: Indonesian  uk: Ukrainian    ro: Romanian    el: Greek
hi: Hindi       he: Hebrew       fa: Persian
```

## Options

```
-f, --file PATH       Input file (or '-' for stdin). PREFERRED MODE.
-o, --output PATH     Output file (default: stdout)
-t, --to CODE         Target language (default: en)
--temperature FLOAT   Temperature 0.1-1.0 (default: 0.3)
--max-tokens INT      Max output tokens per chunk (default: 4000)
--system-prompt STR   System message for constraints
--api-key KEY         Cohere API key (or set COHERE_API_KEY env var)
--json                Output full JSON with token counts
-q, --quiet           Suppress progress messages
--list-languages      List supported language codes
```

## System Prompt Examples

```bash
# Operational constraints work well
python3 translate.py -f doc.txt --to ja \
  --system-prompt "Output ONLY the translation. Keep numbers and URLs unchanged."
```

**Note**: System prompts work for operational constraints but have limited effect on
translation tone/style. The model's DPO training makes translation behavior largely hardwired.

## API Key

This skill requires a Cohere API key. Get a free trial key at:
https://dashboard.cohere.com/api-keys

Trial keys provide: 1,000 calls/month, 20 req/min, completely free.

```bash
export COHERE_API_KEY="your-key-here"
```

## How the Agent Should Use This Skill

```
[TASK] Translate /workspace/document.txt to Japanese.

# Correct:
python3 skills/cohere-translator/scripts/translate.py -f /workspace/document.txt --to ja -o /workspace/document_ja.txt

# The agent never reads document.txt. ZERO context tokens wasted on file content.
# After completion, the agent may read document_ja.txt to verify the result.
```

## Known Limitations

- **Japanese slang** (2ch-style, ギャル語) may cause API errors
- **System messages cannot change formality** reliably
- **8K input token limit** — auto-chunked for files (see translate_file())
- **Idioms translate literally** rather than finding cultural equivalents
- **Business keigo→European** loses some formality density

## Quality Matrix

| Direction | Casual | Business | Technical | Idioms |
|---|---|---|---|---|
| **JA↔KO** | ★★★★★ | ★★★★★ | ★★★★★ | ★★★ |
| **JA↔ZH** | ★★★★★ | ★★★★ | ★★★★★ | ★★★ |
| **EN→any** | ★★★★★ | ★★★★★ | ★★★★★ | ★★★★ |
| **Any→EN** | ★★★★★ | ★★★★★ | ★★★★★ | ★★★★ |
| **ZH↔KO** | ★★★★★ | — | ★★★★★ | — |
| **FR↔DE** | ★★★★★ | ★★★★★ | ★★★★★ | — |

Full research: `skills/cohere-translator/RESEARCH.md`
