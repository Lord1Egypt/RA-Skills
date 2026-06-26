# cohere-translator

> **🔑 Requires a Cohere API key.** The `cohere/command-a-translate-08-2025` model
> is **free** for trial keys as of 2026-05-17 (1,000 calls/month, 20 req/min).
> Get a key at: https://dashboard.cohere.com/api-keys

High-quality neural machine translation for 23 languages, powered by Cohere's
**Command A Translate** (`cohere/command-a-translate-08-2025`) — a 111B-parameter model
that outperforms GPT-5, DeepL, and Google Translate on standard benchmarks.

## Why This Skill?

- **Free tier**: Cohere trial keys give you 1,000 translations/month at zero cost
- **SOTA quality**: Built on difficulty-filtered DPO training — beats general-purpose LLMs at translation
- **23 languages**: Japanese, English, Chinese, Korean, French, German, Spanish, and 16 more
- **Cross-language direct**: Translate ZH↔KO, FR↔DE without needing English as a pivot
- **Production-consistent**: Identical output at low temperature — safe for automated pipelines
- **Full LLM capabilities**: Handles complex grammar, mixed content, code, and markdown

## Installation

```bash
# Clone or copy the skill into your OpenClaw workspace
cp -r cohere-translator ~/.openclaw/workspace/skills/

# No Python dependencies needed — uses only stdlib + curl
```

## Setup

1. Get a **free Cohere API key** at https://dashboard.cohere.com/api-keys
   - Trial keys: 1,000 calls/month, 20 req/min, completely free
   - Production keys: contact Cohere sales for higher limits

2. Set the environment variable:
   ```bash
   export COHERE_API_KEY="your-key-here"
   ```

## Usage

### ⚡ File Mode (Recommended — Zero Agent Tokens)

When used from an AI agent (OpenClaw, Claude Code, etc.), file mode eliminates all
context-window waste. The script reads the file directly — the agent never touches the content.

```bash
# Translate a file → file
python3 translate.py -f document.txt --to ja -o translated.txt

# Translate stdin → file
cat document.txt | python3 translate.py -f - --to ja -o output.txt

# Translate file → stdout
python3 translate.py -f document.txt --to en

# Large files auto-chunked (6,000+ chars automatically split with rate-limit pacing)
python3 translate.py -f large_document.txt --to ja -o output.txt
```

### Text Mode (Quick one-liners)

```bash
python3 translate.py "Hello, how are you?" --to ja  # → こんにちは
python3 translate.py "おはようございます" --to en      # → Good morning
python3 translate.py "Bonjour le monde" --to es       # → ¡Hola mundo!
python3 translate.py "你好，今天天气真好" --to ko     # Cross-language, no EN pivot
```

### Advanced Options

```bash
# Adjust temperature (default: 0.3 — lower = more consistent)
python3 translate.py "..." --to ja --temperature 0.1

# Cap output length (default: 4000 tokens, model max: 8000)
python3 translate.py "..." --to en --max-tokens 500

# Get JSON output with token counts
python3 translate.py "Hello" --to ja --json
# {"text": "こんにちは", "tokens_in": 15, "tokens_out": 5, "finish_reason": "COMPLETE"}

# System prompt for constraints
python3 translate.py "..." --to ja \
  --system-prompt "Output ONLY the translation. Keep numbers and URLs unchanged."

# List supported languages
python3 translate.py --list-languages
```

### Python API

```python
from translate import translate

result = translate("Hello world", target_lang="ja", temperature=0.3)
print(result["text"])        # こんにちは世界
print(result["tokens_in"])   # 15
print(result["tokens_out"])  # 5
```

## Supported Languages

| Code | Language | Code | Language | Code | Language |
|---|---|---|---|---|---|
| `en` | English | `ja` | Japanese | `zh` | Chinese |
| `ko` | Korean | `fr` | French | `de` | German |
| `es` | Spanish | `it` | Italian | `pt` | Portuguese |
| `ar` | Arabic | `ru` | Russian | `pl` | Polish |
| `tr` | Turkish | `vi` | Vietnamese | `nl` | Dutch |
| `cs` | Czech | `id` | Indonesian | `uk` | Ukrainian |
| `ro` | Romanian | `el` | Greek | `hi` | Hindi |
| `he` | Hebrew | `fa` | Persian | | |

## How It Works

The script sends a chat completion request to Cohere's API:

```
POST https://api.cohere.ai/v2/chat
Authorization: Bearer $COHERE_API_KEY
{
  "model": "command-a-translate-08-2025",
  "messages": [{"role": "user", "content": "Translate everything that follows into Japanese:\n\n{text}"}],
  "temperature": 0.3
}
```

The model is a 111B-parameter LLM based on Command A, fine-tuned with Direct Preference
Optimization and a novel **difficulty filtering** technique that focuses training on the
hardest translation examples.

## Quality Benchmarks

Based on empirical testing across 50+ test cases and 5 language pairs:

| Language Pair | Casual | Business | Technical | Idioms |
|---|---|---|---|---|
| JA↔KO | ★★★★★ | ★★★★★ | ★★★★★ | ★★★ |
| JA↔ZH | ★★★★★ | ★★★★ | ★★★★★ | ★★★ |
| EN→any | ★★★★★ | ★★★★★ | ★★★★★ | ★★★★ |
| Any→EN | ★★★★★ | ★★★★★ | ★★★★★ | ★★★★ |
| ZH↔KO | ★★★★★ | — | ★★★★★ | — |
| FR↔DE | ★★★★★ | ★★★★★ | ★★★★★ | — |

## Limitations

- **Japanese slang** (2ch/ギャル語) causes API errors — stick to standard Japanese
- **System prompts can't control tone** — the model's translation style is hardwired
- **8K token input limit** — split long documents into chunks (~15 words each)
- **Idioms translate literally** — "塞翁失马" becomes the literal story, not "a blessing in disguise"
- **Keigo→European** loses formality density — `拝啓 貴社ますますご清栄` becomes generic business greeting

## Comparison

| | Cohere Command A Translate | Google Translate | DeepL |
|---|---|---|---|
| Languages | 23 | 130+ | 30+ |
| Free tier | 1,000 calls/month | Unlimited (web) | 500K chars/month |
| Quality (JA↔EN) | SOTA | Good | Very good |
| Cross-language | Excellent | Via EN pivot | Via EN pivot |
| API | REST (Cohere v2) | REST | REST |
| Context | 8K tokens | ~few sentences | ~few sentences |
| Consistency | Perfect (temp=0.3) | Deterministic | Deterministic |
| Non-translation tasks | Full LLM | ❌ | ❌ |

## Files

```
cohere-translator/
├── SKILL.md              # OpenClaw skill definition
├── README.md             # This file — public documentation
├── RESEARCH.md           # Full research: 50+ tests, parameters, edge cases
└── scripts/
    └── translate.py      # Main translation script (stdlib only, no pip install needed)
```

## License

MIT — use freely in any project. Attribution appreciated.

The underlying model (`command-a-translate-08-2025`) is available under
[CC-BY-NC](https://cohere.com/cohere-labs-cc-by-nc-license) for research use
and via Cohere API for commercial use.
