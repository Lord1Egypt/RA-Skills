# Fword Usage Reference

## Scripts

All scripts are in the `scripts/` directory of the skill.

### Setup

```bash
bash scripts/setup.sh
```

Installs Pandoc (if missing) and Python dependencies (pypandoc, anthropic, openai, python-docx, rich).

### Word → LaTeX

```bash
# Default provider (Anthropic Claude)
python scripts/convert.py document.docx

# Use Qwen (Alibaba Bailian)
python scripts/convert.py document.docx -p qwen

# Use Kimi with a specific model
python scripts/convert.py document.docx -p kimi --model moonshot-v1-32k

# Use DeepSeek
python scripts/convert.py document.docx -p deepseek

# Any OpenAI-compatible API
python scripts/convert.py document.docx -p openai --base-url http://localhost:8080/v1 --api-key your-key

# Specify output
python scripts/convert.py document.docx output.tex

# Pandoc only, no AI (no API key needed)
python scripts/convert.py document.docx --raw

# Keep Pandoc's raw output for debugging
python scripts/convert.py document.docx --keep-intermediate
```

### LaTeX → Word

```bash
# Back-convert (auto-detects original styles from .fword/ workspace)
python scripts/back.py document.tex

# Specify output
python scripts/back.py document.tex final.docx

# Use a custom Word template
python scripts/back.py document.tex --reference-doc template.docx
```

## Supported Providers

| Provider | Env Variable | Default Model |
|----------|-------------|---------------|
| Anthropic (Claude) | `ANTHROPIC_API_KEY` | `claude-sonnet-4-20250514` |
| OpenAI | `OPENAI_API_KEY` | `gpt-4o` |
| Qwen (Alibaba) | `DASHSCOPE_API_KEY` | `qwen-plus` |
| Kimi (Moonshot) | `MOONSHOT_API_KEY` | `moonshot-v1-8k` |
| MiniMax | `MINIMAX_API_KEY` | `MiniMax-Text-01` |
| DeepSeek | `DEEPSEEK_API_KEY` | `deepseek-chat` |
| Zhipu (GLM) | `ZHIPU_API_KEY` | `glm-4-plus` |

Any OpenAI-compatible API can also be used via `--base-url`.

## Round-trip Workflow

```
1. fword convert  →  creates .fword/ workspace + .tex output
2. edit .tex      →  by hand, with AI, or both
3. fword back     →  recovers original Word styles from workspace
```

## Workspace (.fword/)

Created automatically during `convert.py`. Contains:

- `reference.docx` — copy of the original Word document (used as style template)
- `manifest.json` — conversion history and document metadata

The workspace enables high-fidelity back-conversion by preserving the original document's styles, fonts, headers, footers, and page layout.

## Environment Variables

Set the appropriate variable for your chosen provider:

- `ANTHROPIC_API_KEY` — Anthropic (Claude)
- `OPENAI_API_KEY` — OpenAI
- `DASHSCOPE_API_KEY` — Qwen (Alibaba Bailian)
- `MOONSHOT_API_KEY` — Kimi (Moonshot)
- `MINIMAX_API_KEY` — MiniMax
- `DEEPSEEK_API_KEY` — DeepSeek
- `ZHIPU_API_KEY` — Zhipu (GLM)

Use `--raw` flag if no API key is available.
