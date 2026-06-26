---
name: contextcrumb
description: Use when an agent needs to read, inspect, summarize, or load large local prose-heavy files cheaply before sending them into LLM context. Best for Markdown docs, notes, meeting transcripts, issue threads, logs with narrative text, research dumps, and other natural-language files where exact wording is less important than preserving useful context.
---

# ContextCrumb

## Purpose

Use ContextCrumb as a cheap first pass before reading large local text files into an LLM context window. It compresses by deleting lower-value words and punctuation while keeping the remaining text in original order.

ContextCrumb is for orientation and triage. Treat compressed output as shortened context, not authoritative source text.

## When To Use

Use it before reading large natural-language files:

- Documentation and Markdown
- Notes and research dumps
- Meeting transcripts
- Issue threads and long discussions
- Logs with lots of prose
- Long comments or narrative text

## When Not To Use

Do not rely on compressed output for exact syntax or exact wording:

- Source code
- Config files
- Diffs and patches
- JSON, YAML, TOML, XML, or schemas
- Commands that may need to be copied exactly
- Legal, compliance, policy, or contract text

For these files, read the raw source. If a file is too large, use ContextCrumb only to find likely relevant sections, then open the raw file around those sections before editing, quoting, or copying anything.

## Default Workflow

If `contextcrumb` is already installed, use golden mode by default:

```powershell
contextcrumb load <file>
```

If the CLI is not installed and this is a one-off read, run it from PyPI:

```powershell
uvx --from contextcrumb contextcrumb load <file>
```

If repeated local use is expected, install it once:

```powershell
python -m pip install contextcrumb
```

Then use:

```powershell
contextcrumb load <file>
```

Golden mode chooses an adaptive cutoff for each file and is the preferred default because it is conservative. If the output is still too large, use a fixed keep ratio only after checking the tradeoff:

```powershell
contextcrumb load <file> --target-keep-ratio 0.75
contextcrumb load <file> --target-keep-ratio 0.5
```

Avoid aggressive ratios for first-pass reading unless the user explicitly asks for heavy compression.

## Validation

Check compression savings without dumping the full output:

```powershell
contextcrumb inspect <file>
```

Check what was removed before trusting a compressed result:

```powershell
contextcrumb diff <file>
```

Use JSON only when another tool needs stats:

```powershell
contextcrumb load <file> --json
```

Read the `text` field as compressed context. Use `stats.token_keep_ratio`, `stats.word_keep`, and `stats.model_windows` to decide whether to retry with a different setting.

## Practical Rules

- Use `contextcrumb load <file>` as the default.
- Use `uvx --from contextcrumb contextcrumb load <file>` for no-install one-off use.
- Use installed CLI for repeated use.
- Use `inspect` and `diff` before trusting compressed text for important work.
- Never edit code, copy commands, or quote exact wording based only on compressed output.
