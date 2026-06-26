---
name: flashformat-local-converters
description: Provide five repository-local format conversion scripts (yaml-to-json, json-to-yaml, markdown-to-text, json-minify, yaml-auto-fix) for offline CLI and pipeline usage without running FlashFormat API. Use when users ask for local format conversion, batch processing, or CI-friendly text normalization.
---

# FlashFormat Local Converters

## Overview

Run local format conversion directly from Python scripts under `skills/flashformat-local-converters/scripts/`.
Avoid calling `/api/v2/*`; execute conversion in local shell, CI, or offline pipelines.

## Quick Start

1. Install runtime dependency:
   `python -m pip install PyYAML`
2. Run any converter script with one input channel:
   `--input` or `--input-file` or `stdin`
3. Choose output mode:
   plain text (default) or `--json`
4. Optionally write result to file:
   `--output-file <path>`

## Script Map

- `scripts/yaml_to_json.py`: Convert YAML to JSON, support `--indent` and `--compact`
- `scripts/json_to_yaml.py`: Convert JSON to YAML, support `--sort-keys` and `--compact`
- `scripts/markdown_to_text.py`: Strip Markdown syntax into readable text
- `scripts/json_minify.py`: Minify JSON to one-line payload
- `scripts/yaml_auto_fix.py`: Apply conservative YAML whitespace/indent fixes with validation

## Unified CLI Contract

- Input priority: `--input` > `--input-file` > `stdin`
- Output target: `stdout` by default, or `--output-file`
- JSON mode payloads:
  `{"ok": true, "tool": "...", "output": "..."}`
  `{"ok": false, "tool": "...", "error": "..."}`
- Plain mode failures write error text to `stderr` and return non-zero exit code

## Usage Examples

- YAML to JSON:
  `python skills/flashformat-local-converters/scripts/yaml_to_json.py --input-file in.yaml --output-file out.json`
- JSON to YAML (sorted keys):
  `python skills/flashformat-local-converters/scripts/json_to_yaml.py --input '{"b":2,"a":1}' --sort-keys`
- Markdown to text (stdin pipeline):
  `cat draft.md | python skills/flashformat-local-converters/scripts/markdown_to_text.py`
- JSON minify with structured output:
  `python skills/flashformat-local-converters/scripts/json_minify.py --input-file data.json --json`
- YAML auto-fix:
  `python skills/flashformat-local-converters/scripts/yaml_auto_fix.py --input-file broken.yaml --indent-step 2 --fix-tabs --fix-odd-indent`

## References

Read `references/io-contracts.md` when exact options, error messages, and backend logic mapping are needed.
