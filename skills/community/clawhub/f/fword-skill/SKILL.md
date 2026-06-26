---
name: fword
description: "AI-powered bidirectional Word ↔ LaTeX converter. Supports multiple AI providers (Anthropic, OpenAI, Qwen, Kimi, MiniMax, DeepSeek, Zhipu). Converts Word to clean LaTeX with AI refinement, and converts back preserving original styles."
---

# Fword — Word ↔ LaTeX Converter

You are an AI assistant equipped with the Fword skill for bidirectional Word ↔ LaTeX conversion.

## When to Activate

Activate this skill when the user:
- Wants to convert a `.docx` / Word file to LaTeX
- Wants to convert a `.tex` / LaTeX file back to Word
- Asks you to edit a Word document (convert to LaTeX first, edit, convert back)
- Mentions "fword" by name

## Setup

Before first use, ensure dependencies are installed:

```bash
bash {SKILL_DIR}/scripts/setup.sh
```

Check if setup is needed by testing: `python3 -c "import pypandoc, anthropic, openai, docx"`. If this fails, run setup.

## Supported AI Providers

| Provider | Env Variable | Default Model | Flag |
|----------|-------------|---------------|------|
| Anthropic (Claude) | `ANTHROPIC_API_KEY` | `claude-sonnet-4-20250514` | `-p anthropic` |
| OpenAI | `OPENAI_API_KEY` | `gpt-4o` | `-p openai` |
| Qwen (Alibaba) | `DASHSCOPE_API_KEY` | `qwen-plus` | `-p qwen` |
| Kimi (Moonshot) | `MOONSHOT_API_KEY` | `moonshot-v1-8k` | `-p kimi` |
| MiniMax | `MINIMAX_API_KEY` | `MiniMax-Text-01` | `-p minimax` |
| DeepSeek | `DEEPSEEK_API_KEY` | `deepseek-chat` | `-p deepseek` |
| Zhipu (GLM) | `ZHIPU_API_KEY` | `glm-4-plus` | `-p zhipu` |

Any OpenAI-compatible API can also be used via `--base-url`.

## Commands

### Word → LaTeX

```bash
cd {SKILL_DIR}/scripts && python3 convert.py /absolute/path/to/document.docx /absolute/path/to/output.tex
```

Options:
- `-p, --provider PROVIDER` — AI provider (default: anthropic)
- `--model MODEL` — AI model (default: provider's default)
- `--api-key KEY` — API key (or set provider's env var)
- `--base-url URL` — Custom API base URL
- `--raw` — Pandoc-only conversion, no AI refinement (no API key needed)
- `--keep-intermediate` — Save Pandoc's raw output as `.raw.tex`

Examples:
```bash
# Default (Anthropic Claude)
cd {SKILL_DIR}/scripts && python3 convert.py /path/to/doc.docx

# Use Qwen
cd {SKILL_DIR}/scripts && python3 convert.py /path/to/doc.docx -p qwen

# Use DeepSeek with specific model
cd {SKILL_DIR}/scripts && python3 convert.py /path/to/doc.docx -p deepseek --model deepseek-chat

# Pandoc only (no AI)
cd {SKILL_DIR}/scripts && python3 convert.py /path/to/doc.docx --raw
```

### LaTeX → Word

```bash
cd {SKILL_DIR}/scripts && python3 back.py /absolute/path/to/document.tex /absolute/path/to/output.docx
```

Options:
- `--reference-doc PATH` — Use a specific Word template for styles (overrides workspace)

## Workflow

### Standard conversion

1. Run `convert.py` on the `.docx` file — this creates a `.fword/` workspace and outputs `.tex`
2. The `.fword/` workspace stores the original document as a style reference
3. Edit the LaTeX as needed
4. Run `back.py` to convert back — it automatically finds the workspace and recovers styles

### AI-assisted editing workflow

When the user wants to edit a Word document with AI help:

1. Convert: `convert.py document.docx` → produces `document.tex`
2. Read the `.tex` file and make the requested edits directly in LaTeX
3. Convert back: `back.py document.tex` → produces `document.docx` with original styles

### Quick reference

| User wants... | Action |
|---|---|
| Convert Word to LaTeX | `convert.py input.docx` |
| Convert with Qwen | `convert.py input.docx -p qwen` |
| Convert with DeepSeek | `convert.py input.docx -p deepseek` |
| Convert without AI | `convert.py input.docx --raw` |
| Convert LaTeX to Word | `back.py input.tex` |
| Edit Word doc with AI | convert → edit .tex → back |

## Important Notes

- Always use **absolute paths** for input/output files
- Always `cd {SKILL_DIR}/scripts` before running scripts (they import each other)
- Set the appropriate **environment variable** for your chosen provider's API key
- If no API key is available, use `--raw` flag for Pandoc-only conversion
- The `.fword/` workspace is created next to the output file
- For large documents, AI refinement processes in chunks automatically
