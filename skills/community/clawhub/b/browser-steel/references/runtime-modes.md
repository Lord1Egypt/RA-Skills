# Runtime Modes

## Goal

Choose the lightest runtime that can complete the task reliably.

## What counts as `CLI`

`CLI` means the Steel terminal commands themselves.

Examples:

```bash
steel scrape https://example.com
steel screenshot https://example.com --full-page
steel browser start --session demo
steel browser open https://example.com --session demo
steel browser snapshot -i --session demo
```

Inside this skill, `scripts/main.py` uses those commands as the default execution path unless the user explicitly chooses the Python runtime.

## Modes

### `auto`

Default mode.

1. Use installed `steel` if present.
2. Otherwise use `npx --yes @steel-dev/cli`.
3. Do not fall through to Python implicitly; choose Python only when the workflow needs custom Playwright logic.

### `cli`

CLI-only mode.

- Prefer installed `steel`.
- Fall back to `npx --yes @steel-dev/cli`.
- Fail if neither path exists.

### `node`

Force the Node-distributed CLI path.

- Use `npx --yes @steel-dev/cli` even if `steel` is installed.
- Use this when you want behavior closer to the upstream CLI package or when testing community-install assumptions.

### `python`

Use `run-python-plan`.

- Requires `STEEL_API_KEY`.
- Requires Python packages `steel` and `playwright`.
- If the current interpreter lacks those packages, set `STEEL_BROWSER_PYTHON_BIN` to a compatible interpreter.

## Env loading

The wrapper loads env vars in this order:

1. Current process env
2. `--env-file <path>` if provided
3. `STEEL_BROWSER_ENV_FILE` if provided
4. `.env` in the current working directory
5. `.env` inside the skill directory

Loaded values only fill missing keys; they do not overwrite already-exported env vars.

## Privacy rules

- Do not hardcode workspace-specific `.env` paths in the published skill.
- Do not ship personal cookies, browser profiles, or account-specific namespaces.
- Use `STEEL_BROWSER_COOKIES_FILE` or `--cookies-file` only at runtime.
- Keep profile names and credential namespaces task-specific, not user-specific.
