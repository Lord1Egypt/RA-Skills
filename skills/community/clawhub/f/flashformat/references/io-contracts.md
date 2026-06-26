# IO Contracts

## Shared contract (all 5 scripts)

| Item | Contract |
| --- | --- |
| Input channels | `--input` or `--input-file` or `stdin` |
| Input priority | `--input` > `--input-file` > `stdin` |
| Output channels | `stdout` by default, or `--output-file` |
| Default output mode | Plain converted text |
| Structured output mode | `--json` |
| JSON success payload | `{"ok": true, "tool": "...", "output": "..."}` |
| JSON failure payload | `{"ok": false, "tool": "...", "error": "..."}` |
| Failure exit code | Non-zero |
| Plain-mode error stream | `stderr` |

## Tool-level details

### 1) yaml-to-json

- Script: `scripts/yaml_to_json.py`
- Source mapping:
  `backend/src/flashformat/converters/yaml_to_json.py`
  `backend/src/flashformat/api_v2.py::_run_yaml_to_json`
- Input format: YAML text
- Output format: JSON text
- Options:
  `--indent` (default `2`, clamped to `0..8`)
  `--compact` (force compact JSON)
- Special behavior:
  If `--indent 0`, script emits compact JSON (same intent as API route).
- Common failure:
  `YAML parse error: ...`

### 2) json-to-yaml

- Script: `scripts/json_to_yaml.py`
- Source mapping:
  `backend/src/flashformat/converters/json_to_yaml.py`
  `backend/src/flashformat/api_v2.py::_run_json_to_yaml`
- Input format: JSON text
- Output format: YAML text
- Options:
  `--sort-keys`
  `--compact` (sets wide line width and sorted keys behavior)
- Common failure:
  `JSON parse error: ...`

### 3) markdown-to-text

- Script: `scripts/markdown_to_text.py`
- Source mapping:
  `backend/src/flashformat/converters/text_ops.py::markdown_to_text`
- Input format: Markdown text
- Output format: Plain text
- Options:
  no tool-specific options
- Behavior highlights:
  strip heading/list markers, keep links as `text (url)`, collapse 3+ blank lines to 2.

### 4) json-minify

- Script: `scripts/json_minify.py`
- Source mapping:
  `backend/src/flashformat/converters/text_ops.py::json_minify`
  `backend/src/flashformat/api_v2.py::_run_json_minify`
- Input format: JSON text
- Output format: one-line compact JSON
- Options:
  no tool-specific options
- Common failure:
  `JSON parse error: ...`

### 5) yaml-auto-fix

- Script: `scripts/yaml_auto_fix.py`
- Source mapping:
  `backend/src/flashformat/converters/text_ops.py::yaml_auto_fix`
  `backend/src/flashformat/api_v2.py::_run_yaml_auto_fix`
- Input format: YAML text
- Output format: fixed YAML text
- Options:
  `--indent-step` (default `2`, clamped to `2..8`)
  `--fix-tabs` / `--no-fix-tabs` (default on)
  `--fix-odd-indent` / `--no-fix-odd-indent` (default on)
  `--trim-trailing-spaces` / `--no-trim-trailing-spaces` (default on)
  `--target-line-ending {lf,crlf}` (default `lf`)
- Validation behavior:
  parse fixed text with `yaml.safe_load_all`; fail if still invalid.
- Common failure:
  `YAML is still invalid after auto-fix: ...`
