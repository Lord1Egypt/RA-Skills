# Troubleshooting

## `steel: command not found`

- Run `python3 {baseDir}/scripts/main.py doctor`
- If `steel` is missing but `npx` exists, use runtime `auto` or `node`
- If neither `steel` nor `npx` exists, install the Steel CLI prerequisites first

## `Missing browser auth` or similar auth failure

- Confirm `STEEL_API_KEY` exists in the env or env file
- Re-run the doctor command to verify the key is visible to the wrapper
- For local/self-hosted mode, verify whether `--local` or `--api-url` is the intended path

## Session not reused

- Use the same `--session <name>` on every command
- Do not mix one session name in `start-session` with another in `browser` steps
- If state is stale, run `stop-session --all` and start fresh

## Python runtime import failure

- Install `steel` and `playwright` into the active interpreter
- Or set `STEEL_BROWSER_PYTHON_BIN` to a compatible interpreter
- Re-run the same `run-python-plan` command after fixing the interpreter path

## Cookie issues

- Pass cookies through `--cookies-file` or `STEEL_BROWSER_COOKIES_FILE`
- Keep cookies outside the published skill directory
- If the cookie file is a site-keyed JSON map, pass `--site` when hostname inference is ambiguous

## CAPTCHA or anti-bot friction

- Prefer `start-session --stealth`
- If CAPTCHA solving is needed in Python runtime, use `--solve-captcha`
- If the site still blocks, add proxy support explicitly instead of blind retries
