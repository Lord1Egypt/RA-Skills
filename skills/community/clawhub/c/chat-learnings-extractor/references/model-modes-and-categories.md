# Configuration, Model Modes, and Output Format

Detail split out of `SKILL.md` to keep it within the 100-line budget.
# Model Modes and Extraction Categories

Detail split out of `SKILL.md` to keep it within the 100-line budget.

### Using OpenAI-compatible API (e.g., OpenAI, Anthropic Bedrock, etc.)

```bash
export OPENAI_API_KEY=sk-...
export OPENAI_BASE_URL=https://api.openai.com/v1  # optional, defaults to OpenAI
python3 scripts/extract.py --dir /path/to/exports --model gpt-4o-mini
```


---

## Configuration

### Using Ollama (Local)

**Prerequisites:** Ollama running at `http://127.0.0.1:11434` (default)

```bash
# Use default model (gemma4:26b)
python3 scripts/extract.py --dir /path/to/exports

# Use a different local model
python3 scripts/extract.py --dir /path/to/exports --model llama2

# Custom Ollama endpoint
export OLLAMA_BASE_URL=http://ollama.example.com:11434
python3 scripts/extract.py --dir /path/to/exports
```

**Environment Variables:**
- `OLLAMA_BASE_URL` — Ollama API endpoint (default: `http://127.0.0.1:11434`)

### Using OpenAI-compatible API

Any API supporting the OpenAI `/chat/completions` endpoint (OpenAI, Bedrock, LM Studio, etc.)

```bash
export OPENAI_API_KEY=sk-...
export OPENAI_BASE_URL=https://api.openai.com/v1  # optional
python3 scripts/extract.py --dir /path/to/exports --model gpt-4o-mini
```

**Environment Variables:**
- `OPENAI_API_KEY` — API key (required to enable this mode; if set, OpenAI mode is used instead of Ollama)
- `OPENAI_BASE_URL` — API base URL (default: `https://api.openai.com/v1`)

**Model auto-selection:**
- If `OPENAI_API_KEY` is set → defaults to `gpt-4o-mini`
- If `OPENAI_API_KEY` is not set → defaults to `gemma4:26b` (Ollama)


---

## Output Format

Results are appended to `memory/semantic/learnings-from-exports.md` with this structure:

```markdown

---

## Chat Title (YYYY-MM-DD)

### Lessons Learned

- [bullet points]

### Decisions Made

- [bullet points]

### Patterns Noticed

- [bullet points]

### Dead Ends

- [bullet points]
```

Each category is optional — if a conversation doesn't have notable insights for a category, it will show "None".
