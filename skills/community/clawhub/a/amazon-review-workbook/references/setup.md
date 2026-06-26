# Setup

## What This Skill Needs

This skill is designed for a two-phase workflow:

1. Use scripts to collect Amazon reviews and fill factual columns.
2. Use the model directly in the chat to tag the collected rows.

Keyword expansion is now manual. The normal path is `intake -> coverage-check -> decide whether to run --keywords`.
The built-in presets are `generic`, `electronics`, and `dashcam`; default keyword reuse skips previously productive keywords and temporarily suppresses recent zero-result retries.
The tuned state file lives at `<output-dir>/keyword_tuning_state.json` by default and can be rebuilt from the SQLite cache plus old keyword JSON reports with `keyword-autotune`.

The scripts do not require any external LLM API.

They only need:

1. A Chrome session with Amazon login available on `localhost:9222`
2. Python packages for scraping and workbook writing
3. Optional DeepLX access if you want machine translation before tagging

## Python Packages

Install these packages in the environment that will run the skill:

```bash
pip install pandas openpyxl requests websocket-client
```

## Chrome Remote Debugging

The script reads Amazon review pages through an already logged-in Chrome profile.

### Windows

1. Close existing Chrome windows.
2. Launch Chrome with remote debugging and your normal profile:

```powershell
"$env:ProgramFiles\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="$env:LOCALAPPDATA\Google\Chrome\User Data"
```

If Chrome is installed under `Program Files (x86)`, adjust the path.

### macOS

```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 --user-data-dir="$HOME/Library/Application Support/Google/Chrome"
```

### Linux

```bash
google-chrome --remote-debugging-port=9222 --user-data-dir="$HOME/.config/google-chrome"
```

After Chrome starts, verify that Amazon is logged in inside that same browser session.

## DeepLX Translation

If you want to fill `评论中文版` automatically before tagging, configure:

- `DEEPLX_API_URL`
- optional `DEEPLX_API_KEY`

You can place them in either:

- the current shell environment
- a local `.env` file in the working directory
- a local `.env` file in the skill root

The repo includes `.env.example` as a template. Keep the real `.env` out of Git.

Examples:

```powershell
$env:DEEPLX_API_URL="https://your-deeplx-host/translate"
$env:DEEPLX_API_KEY="your-key"
```

```bash
export DEEPLX_API_URL="https://your-deeplx-host/translate"
export DEEPLX_API_KEY="your-key"
```

## Sanity Check

Run this before the first real scrape:

```bash
python scripts/amazon_review_workbook.py doctor --url "<amazon-url>"
```

Expected result:

- URL parses to a valid `asin`
- `chrome_debug_ready` is `true`
- `deeplx_env_ready` is `true` if you plan to use `translate`
- `deeplx_reachable` is `true` if DeepLX is actually reachable

If `deeplx_reachable` is `false`, the skill can still continue:

- `translate` will preserve the factual rows and print `translation_mode=model_fallback`
- the model should then fill `评论中文版` during the tagging phase
