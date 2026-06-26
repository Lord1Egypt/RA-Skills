# Python Plan Runner

Use the Python runtime only when you need custom Playwright logic that would be awkward through pure CLI steps.

## Command

```bash
python3 {baseDir}/scripts/main.py run-python-plan \
  --plan-file /absolute/path/to/plan.json \
  --url https://example.com
```

Optional runtime inputs:

- `--session <name>`: override the human-readable session label used in output
- `--site <key>`: cookie lookup key override
- `--cookies-file <path>`: explicit cookie JSON path
- `--use-proxy`: create the Steel session with proxy support
- `--solve-captcha`: create the Steel session with CAPTCHA solving enabled
- `STEEL_BROWSER_PYTHON_BIN`: alternate interpreter if the current Python lacks `steel` or `playwright`

## Plan schema

```json
{
  "url": "https://example.com",
  "session_name": "demo-plan",
  "session_id": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d",
  "use_proxy": false,
  "solve_captcha": false,
  "steps": [
    {"action": "wait_for_load_state", "state": "networkidle"},
    {"action": "extract_text", "selector": "body", "max_chars": 4000}
  ]
}
```

If `session_id` is omitted, the runner generates a valid UUID automatically.

## Supported actions

### Navigation and waits

- `goto`
  - fields: `url`, optional `wait_until`, optional `timeout`
- `wait_for_load_state`
  - fields: optional `state`, optional `timeout`
- `wait_for_selector`
  - fields: `selector`, optional `state`, optional `timeout`
- `wait_for_text`
  - fields: `text`, optional `timeout`

### Interaction

- `click`
  - fields: `selector`, optional `timeout`
- `fill`
  - fields: `selector`, `value`, optional `timeout`
- `type`
  - fields: `selector`, `value`, optional `delay_ms`, optional `timeout`
- `press`
  - fields: `key`, optional `selector`
- `select`
  - fields: `selector`, `value` or `values`
- `hover`
  - fields: `selector`, optional `timeout`
- `scroll`
  - fields: optional `x`, optional `y`

### Extraction and debug

- `eval`
  - fields: `script`
- `extract_text`
  - fields: optional `selector`, optional `max_chars`, optional `timeout`
- `extract_html`
  - fields: optional `selector`, optional `max_chars`, optional `timeout`
- `get_title`
  - no extra fields
- `get_url`
  - no extra fields
- `screenshot`
  - fields: `output`, optional `selector`, optional `full_page`

## Output

The runner prints a JSON object with:

- `runtime`
- `session_name`
- `session_id`
- final `url`
- per-step `results`

## Example

See `references/example-plan.json` for a minimal working plan.
