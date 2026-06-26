# CLI Workflows

## Stateless tools first

Use these when you do not need a persistent browser session.

```bash
python3 {baseDir}/scripts/main.py scrape --url https://example.com --format markdown --json
python3 {baseDir}/scripts/main.py screenshot --url https://example.com --full-page --json
python3 {baseDir}/scripts/main.py pdf --url https://example.com --json
```

### When to use each

- `scrape`: extract page content, optionally with `--pdf` or `--screenshot`
- `screenshot`: one-shot visual capture
- `pdf`: one-shot PDF generation

## Named-session lifecycle

Use a named session when the workflow is interactive or multi-step.

```bash
python3 {baseDir}/scripts/main.py start-session --session my-job --stealth --json
python3 {baseDir}/scripts/main.py browser --session my-job -- open https://example.com
python3 {baseDir}/scripts/main.py browser --session my-job -- snapshot -i -c
python3 {baseDir}/scripts/main.py browser --session my-job -- click @e3
python3 {baseDir}/scripts/main.py browser --session my-job -- wait --load-state networkidle
python3 {baseDir}/scripts/main.py browser --session my-job -- snapshot -i -c
python3 {baseDir}/scripts/main.py stop-session --session my-job --json
```

## High-value patterns

### Login or form flow

1. `start-session --session <name> --stealth`
2. `browser --session <name> -- open <url>`
3. `browser --session <name> -- snapshot -i -c`
4. `browser --session <name> -- fill @eN "..."`
5. `browser --session <name> -- click @eN`
6. `browser --session <name> -- wait --load-state networkidle`
7. Re-snapshot before the next `@eN` action
8. `stop-session --session <name>`

### Debug current state

```bash
python3 {baseDir}/scripts/main.py sessions --json
python3 {baseDir}/scripts/main.py live --session my-job
python3 {baseDir}/scripts/main.py browser --session my-job -- get title
python3 {baseDir}/scripts/main.py browser --session my-job -- get url
python3 {baseDir}/scripts/main.py browser --session my-job -- snapshot -i -c
```

## Guardrails

- Use the same `--session` name on every step.
- Re-snapshot after navigation or DOM changes.
- Prefer `snapshot -i -c` over raw HTML for action planning.
- Use `--json` when the next step needs structured parsing.
