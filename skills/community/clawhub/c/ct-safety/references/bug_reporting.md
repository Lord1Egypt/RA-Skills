# Bug Reporting (ct-base §20.3)

Self-reporting adapter: `adapters/bug_report.py`. This skill **sends `report` only**.

## Two-stage confirmation (2026-08-21) — never send on your own

1. **Propose with preview.** Show the bilingual `confirm_prompt` **together with** the full report
   (`render_report_text`). State that it is sanitized and carries no input data, and invite a problem
   description. If the user adds one, re-render and re-show before asking for consent.
2. **On explicit consent only**, call `send_to_endpoint` (auto `action=report`, endpoint
   `https://ct-bugreport.coze.site/run`, token = the embedded ct-base §5 public credential).

If the user declines, **never re-propose in the same session**.

## When to propose

- **Strong signal, max 1 proposal per session:** unexpected non-zero exit / engine or compute error /
  user explicitly questions the result — **and** the same operation was retried at least once.
- **Weak signal (just repeated tuning) never triggers.**

## Sanitization is hard

The report carries only the 11-key whitelist:

`skill` / `version` / `error_type` / `error_code` / `engine_status` / `description` / `locale` /
`query_origin` / `session_hash` / `attempts` / `test`

Never raw data or subject records. `description` is the single free-text field for debugging and is
**user-reviewed** before sending — write the symptom / reproduction / expected vs actual / algorithm
or function used / error message. Values and study design are acceptable.

**Hard boundary:** no identifiable person, institution, or subject information.

An empty description omits the key. If the session made **no** cloud call, `save_local_report()`
writes a local Markdown file plus the author email — data never leaves the machine.

## Client-only scope

Governance actions (get / update / download / delete — pull pending, mark done, download all, clean
up) are reserved for the `ct-update` skill on the author side. **Never call them from this skill.**

## CLI

```bash
python adapters/bug_report.py --error-type <t> --description "<free text>" [--send]
```

Add `--send` only after the user has confirmed in stage ①.
