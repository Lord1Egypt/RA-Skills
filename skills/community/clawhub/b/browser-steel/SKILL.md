---
name: browser-steel
description: "Browser automation with Steel CLI as the default runtime, plus a Python Playwright fallback for custom flows. Use when the user asks to open a JS-heavy site, capture live page content, take screenshots/PDFs, fill forms, reuse a named browser session, or debug login/CAPTCHA/browser workflows. Trigger examples: 'Use Steel to log into this site and extract the table' or 'Take a real-browser screenshot of this dashboard'. Capabilities: (1) Steel CLI session workflows, (2) stateless scrape/screenshot/pdf commands, (3) Python Playwright plan execution, (4) runtime selection between auto/cli/node/python." 
learnable: true
metadata: {"openclaw":{"emoji":"🌐","requires":{"bins":["steel","python3"],"env":["STEEL_API_KEY"]},"primaryEnv":"STEEL_API_KEY"}}
---

# Browser Steel

Use Steel CLI first. Use the Python runtime only when the workflow needs selector-heavy custom logic that is awkward to express through raw CLI steps.

## What `CLI` means here

`CLI` means **Command Line Interface**.

In this skill, it specifically means the Steel terminal commands themselves, for example:

```bash
steel scrape https://example.com
steel browser start --session demo
steel browser open https://example.com --session demo
steel browser snapshot -i --session demo
```

The wrapper script does not replace Steel CLI. It packages it into a more publishable, agent-friendly entrypoint:

```bash
python3 {baseDir}/scripts/main.py scrape --url https://example.com
python3 {baseDir}/scripts/main.py start-session --session demo
python3 {baseDir}/scripts/main.py browser --session demo -- snapshot -i -c
```

So the relationship is:

- **Steel CLI** = the underlying browser command system
- **`scripts/main.py`** = the wrapper that calls Steel CLI by default
- **Python runtime** = a fallback path for custom Playwright logic when CLI steps are not enough

## First checks

1. Run the doctor command before the first real task in a new environment:
   ```bash
   python3 {baseDir}/scripts/main.py doctor
   ```
2. Prefer stateless commands for one-shot extraction or capture.
3. Prefer named sessions for multi-step interaction.
4. Keep the same `--session` value across every step in one workflow.
5. Never bake private cookies, profile names, or local paths into the skill itself.

## Runtime selection

- `auto`: prefer installed `steel`, otherwise fall back to `npx @steel-dev/cli`
- `cli`: same as `auto`, but fail if no CLI path is available
- `node`: force the Node-distributed CLI path through `npx @steel-dev/cli`
- `python`: use Steel SDK + Playwright through `run-python-plan`

Read `references/runtime-modes.md` only when runtime choice or env resolution matters.
Read `references/official-docs.md` when you need the authoritative Steel CLI or Playwright-Python upstream reference.

## Preferred commands

### Health check

```bash
python3 {baseDir}/scripts/main.py doctor
```

### Stateless commands

```bash
python3 {baseDir}/scripts/main.py scrape --url https://example.com --format markdown --json
python3 {baseDir}/scripts/main.py screenshot --url https://example.com --full-page --json
python3 {baseDir}/scripts/main.py pdf --url https://example.com --json
```

### Named-session workflow

```bash
python3 {baseDir}/scripts/main.py start-session --session demo --stealth --json
python3 {baseDir}/scripts/main.py browser --session demo -- open https://example.com
python3 {baseDir}/scripts/main.py browser --session demo -- snapshot -i -c
python3 {baseDir}/scripts/main.py browser --session demo -- fill @e2 "hello"
python3 {baseDir}/scripts/main.py browser --session demo -- click @e5
python3 {baseDir}/scripts/main.py browser --session demo -- wait --load-state networkidle
python3 {baseDir}/scripts/main.py stop-session --session demo --json
```

### Python Playwright plan

```bash
python3 {baseDir}/scripts/main.py run-python-plan \
  --plan-file {baseDir}/references/example-plan.json \
  --url https://example.com
```

Read `references/python-plan.md` only when the CLI path is insufficient.

## Guardrails

- Start with `scrape`, `screenshot`, or `pdf` when the task is stateless.
- For interactive workflows, follow `start-session -> browser commands -> stop-session`.
- After any navigation or meaningful DOM change, take a fresh `snapshot -i` before using another `@eN` ref.
- Keep secrets in env vars or an explicit `--env-file`, not in the skill files.
- Pass cookies only through `--cookies-file` or `STEEL_BROWSER_COOKIES_FILE`.
- Use the Python runtime only for tasks that genuinely benefit from custom Playwright logic.
- Record confirmed improvements in `maintenance.log`.

## References

- `references/official-docs.md` — upstream Steel CLI and Playwright-Python references
- `references/runtime-modes.md` — runtime choice, env loading, and privacy rules
- `references/cli-workflows.md` — reliable Steel CLI patterns
- `references/python-plan.md` — JSON plan schema and supported actions
- `references/troubleshooting.md` — install/auth/runtime recovery
