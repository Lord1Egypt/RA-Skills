# Cursor Agent — Available Models

Source: `agent models` (as of 2026-03-07)

## Recommended Models

| ID | Name | Best for |
|---|---|---|
| `sonnet-4.6` | Claude 4.6 Sonnet | Primary coding model — fast, accurate, no reasoning overhead |
| `sonnet-4.6-thinking` | Claude 4.6 Sonnet (Thinking) | Tricky debugging, non-obvious bugs |
| `opus-4.6-thinking` | Claude 4.6 Opus (Thinking) | Architecture, design decisions, complex planning |
| `opus-4.6` | Claude 4.6 Opus | Deep analysis without thinking overhead |
| `auto` | Auto (Cursor picks) | Trivial tasks; current CLI default |

## Other Available Models

- `gpt-5.3-codex` / `gpt-5.3-codex-fast` / `-high` / `-xhigh` — OpenAI Codex variants
- `gpt-5.4-medium` / `-high` / `-xhigh` — GPT-5.4 series
- `gpt-5.2`, `gpt-5.1-*` — Older GPT series
- `gemini-3.1-pro`, `gemini-3-pro`, `gemini-3-flash` — Google Gemini
- `kimi-k2.5` — Kimi
- `composer-1.5`, `composer-1` — Cursor Composer models
- `grok` — xAI Grok

## Max Mode

Some models support Max Mode (higher limits). Toggle with `/max-mode on` in interactive mode.
Use sparingly — costs more against Cursor subscription quota.

## Usage Tip

`gpt-5.3-codex` variants are purpose-built for code generation. Try these if Sonnet struggles with a specific task (e.g. complex algorithmic problems).
