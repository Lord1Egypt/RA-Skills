---
name: distil-pii-redactor
description: Redact PII from text locally using a fine-tuned 1B SLM. Text never leaves your machine. Handles names, emails, phones, addresses, SSNs, credit cards, IBANs, and more.
version: 1.1.1
tools:
  - Bash
---

# PII Redaction Skill

## When to use

Use this skill when the user asks to **redact**, **anonymize**, **sanitize**, or **remove PII / personal data** from text.

## Privacy guarantee

**CRITICAL: NEVER include the user's raw input text in your own responses, context, or reasoning.** The entire point of this skill is that the frontier LLM (you) never sees the PII. You pass the text directly to the redaction script and only return the redacted output.

## Prerequisites

- Python 3
- `curl` (for model download)

The setup script handles everything else (model download + server startup).

## First-time setup

If the model server is not running yet, run:

```bash
bash scripts/setup.sh
```

This downloads the GGUF model (~5 GB) and starts the local inference server on port 8712.

## How to redact

Pass the user's text directly to the redaction script. **Do not echo or repeat the raw text yourself.**

```bash
python scripts/redact.py "text to redact"
```

For longer text, pipe it via stdin:

```bash
echo "text to redact" | python scripts/redact.py
```

Return the output to the user as-is.

### `--show-entities` flag (use sparingly)

Adding `--show-entities` outputs the full JSON including the original PII values. **Only use this when the user explicitly asks to see which entities were detected or needs the mapping for a downstream task.** In normal redaction workflows, omit this flag -- displaying the raw entity values defeats the purpose of PII redaction.

```bash
python scripts/redact.py --show-entities "text to redact"
```

## How to stop the server

```bash
bash scripts/stop.sh
```

## Output format

By default the script prints **only the redacted text** -- PII tokens replace the sensitive data and the original values are never shown:

```
Hi, my name is [PERSON] and I need help with my recent order #ORD-29481.

You can reach me at [EMAIL] or call me at [PHONE]. I'm a [AGE_YEARS:34]-year-old [MARITAL_STATUS] woman living at [ADDRESS]...
```

With `--show-entities`, the script returns full JSON including original PII values (see flag note above for when this is appropriate).

See `examples/` for full input/output samples.
