---
name: auto-free-banana
description: Generates images in Google Flow (labs.google/fx) through browser UI automation. Supports Nano Banana 2 and Nano Banana Pro with landscape/portrait aspect ratios. Use when the user requests Flow-based image generation.
version: 1.1.0
metadata:
  openclaw:
    homepage: https://github.com/JimLiu/baoyu-skills#auto-free-banana
    requires:
      anyBins:
        - bun
        - npx
---

# Google Flow UI Client

Generate images in Google Flow through Chrome CDP + browser UI automation.

Important constraints:
- Project creation is **UI-only**
- Prompt submission is **UI-only**
- Do **not** use or describe any API-based project creation path
- Images are considered complete once the base images are visible in the browser

## Script Directory

Resolve:
1. `{baseDir}` = directory containing this `SKILL.md`
2. Script path = `{baseDir}/scripts/main.ts`
3. `${BUN_X}` = `bun` if installed, else `npx -y bun`

## Consent Check (REQUIRED)

Before first use, verify user consent for reverse-engineered API usage.

**Consent file locations**:
- macOS: `~/Library/Application Support/baoyu-skills/flow-web/consent.json`
- Linux: `~/.local/share/baoyu-skills/flow-web/consent.json`
- Windows: `%APPDATA%\baoyu-skills\flow-web\consent.json`

**Flow**:
1. Check if consent file exists with `accepted: true` and `disclaimerVersion: "1.0"`
2. If valid consent exists → print warning with `acceptedAt` date, proceed
3. If no consent → show disclaimer, ask user via `AskUserQuestion`:
   - "Yes, I accept" → create consent file with ISO timestamp, proceed
   - "No, I decline" → output decline message, stop
4. Consent file format: `{"version":1,"accepted":true,"acceptedAt":"<ISO>","disclaimerVersion":"1.0"}`

---

## Preferences (EXTEND.md)

Check EXTEND.md existence (priority order):

```bash
test -f .baoyu-skills/auto-free-banana/EXTEND.md && echo "project"
test -f "${XDG_CONFIG_HOME:-$HOME/.config}/baoyu-skills/auto-free-banana/EXTEND.md" && echo "xdg"
test -f "$HOME/.baoyu-skills/auto-free-banana/EXTEND.md" && echo "user"
```

**EXTEND.md Supports**: Default model | Default aspect ratio | Custom data directory

## Execution Envelope (REQUIRED)

Before any pre-flight check or `main.ts` invocation, decide one shell environment and reuse it for **every** command in the run.

- Use the same `PATH`
- Use the same proxy variables
- Use the same CDP / Chrome profile variables

If you set any of these once, keep them identical for all later commands in the turn:
- `PATH`
- `FLOW_WEB_PROXY`
- `HTTPS_PROXY` / `HTTP_PROXY`
- `AGENT_BROWSER_CHROME_PROXY_SERVER`
- `FLOW_WEB_DEBUG_PORT` / `AGENT_BROWSER_CDP_PORT`
- `FLOW_WEB_COOKIE_PATH`
- `FLOW_WEB_CHROME_PROFILE_DIR`
- `AGENT_BROWSER_USER_DATA_DIR_WIN`
- `AGENT_BROWSER_CMD_EXE_WSL`

Never run pre-flight checks in one environment and `main.ts` in another.

Preferred proxy setup:
```bash
export FLOW_WEB_PROXY=http://host:port
export HTTPS_PROXY="$FLOW_WEB_PROXY"
export HTTP_PROXY="$FLOW_WEB_PROXY"
export AGENT_BROWSER_CHROME_PROXY_SERVER="$FLOW_WEB_PROXY"
```

## Usage

Before running any generation command, complete the [Pre-flight Checks](#pre-flight-checks) below.

```bash
# Default generation: creates a NEW Flow project through the UI
${BUN_X} {baseDir}/scripts/main.ts --prompt "A cute cat"

# Specify model + portrait + 2 images
${BUN_X} {baseDir}/scripts/main.ts --prompt "A sunset" --model NANO_BANANA_PRO --aspect 9:16 --count 2

# Reuse an EXISTING Flow project only when you already have the project id
${BUN_X} {baseDir}/scripts/main.ts --project-id <project-id> --prompt "A sunset"

# Authentication only
${BUN_X} {baseDir}/scripts/main.ts --login

# Batch mode: multiple prompts in one project (5s interval)
${BUN_X} {baseDir}/scripts/main.ts --prompt "A cute cat" --prompt "A sunset" --prompt "A mountain landscape"
```

Batch mode rules:
- Use one command with repeated `--prompt`
- The first prompt creates a new project through the UI unless `--project-id` is supplied
- Later prompts reuse that same project
- Do not run multiple separate `main.ts` commands for a multi-prompt batch

---

## Pre-flight Checks

Run these checks **in order**. Each step must pass before moving to the next.

### Step 1: Runtime Prerequisites (BLOCKING)

Check the Bun runtime and Python:

```bash
command -v bun >/dev/null && echo "BUN" || command -v npx >/dev/null && echo "NPX_BUN" || echo "MISSING"
command -v python3 >/dev/null && echo "OK" || echo "MISSING"
```

If any required command is missing, stop.

If running under WSL, also verify the Windows bridge and Chrome path assumptions:

```bash
test -x /mnt/c/Windows/System32/cmd.exe && echo "OK" || echo "MISSING"
test -f "/mnt/c/Program Files/Google/Chrome/Application/chrome.exe" && echo "OK" || echo "MISSING"
```

If not running under WSL, ensure `FLOW_WEB_CHROME_PATH` is set before continuing.

### Step 2: Browser Profile Check (AUTO-RESOLVE)

Check if the Chrome debug user data directory exists. Default WSL-visible path:
- `/mnt/c/chrome-debug-openclaw`
- env override: `AGENT_BROWSER_USER_DATA_DIR_WIN`

```bash
test -d /mnt/c/chrome-debug-openclaw && echo "EXISTS" || echo "NEW"
```

- `EXISTS` → proceed
- `NEW` → proceed, but tell the user a fresh browser profile will be created

### Step 3: Network Connectivity Check (WARN + WAIT)

Test Google reachability using the **same environment** you will use for `main.ts`:

```bash
curl -sS --connect-timeout 5 -o /dev/null -w '%{http_code}' https://labs.google/fx/ 2>/dev/null || echo "FAIL"
```

- `200/301/302` → proceed
- `FAIL / timeout` → stop and fix proxy settings first

Do not continue into `main.ts` while shell networking and browser proxy settings disagree.

### Step 4: Login State Check (WARN + GUIDE)

Check if cached credentials exist:

Linux default cookie file:
- `~/.local/share/baoyu-skills/flow-web/cookies.json`

```bash
test -f ~/.local/share/baoyu-skills/flow-web/cookies.json && echo "EXISTS" || echo "NONE"
```

- `EXISTS` → proceed
- `NONE` → run:
  ```bash
  ${BUN_X} {baseDir}/scripts/main.ts --login --verbose
  ```
  Then wait for the user to finish Google login in the browser.

---

## Generation Rules

The skill supports exactly two generation entry modes:
- New project: omit `--project-id`; the script creates a project through the **Flow UI**
- Existing project: provide `--project-id`

Do not invent any third path.

Explicitly forbidden:
- API-based project creation
- Describing API project creation as a fallback
- Mixing one failed path with a different project-creation mechanism mid-run

If automatic UI project creation fails:
1. Inspect the Flow listing page in the browser
2. Fix the UI state only
3. Retry the same UI path
4. If needed, manually click `新建项目` in the browser, capture the resulting project id from the URL, then rerun `main.ts` with `--project-id <id>`

The fallback is still UI-only.

---

## Task Completion (IMPORTANT)

`main.ts` only automates the UI. It fills the prompt, clicks Create, then exits immediately. Actual image generation continues asynchronously in the browser.

**After `main.ts` exits with code 0:**

1. The script has successfully submitted all prompts. Images are now **generating in the browser**.
2. You MUST verify generation completion by **taking a browser screenshot** (via CDP or screenshot tool) and visually checking whether images have appeared on the page.
3. If the screenshot shows images are still loading (spinner, progress indicator, blank placeholders), **wait 10-15 seconds** and take another screenshot.
4. Repeat until all images are visible, or until 2 minutes have passed (then report a timeout).
5. Once the base images are confirmed visible, stop and report completion.
6. **Do NOT** download, fetch, curl, or render any URLs. Images are visible in the browser.

Important completion rule:
- If the images are visible **and** Flow still shows optional HD-enhancement / download / post-processing toasts, treat the task as complete anyway.

**If the script exits with a non-zero code**, report the error and stop.

---

## Options

| Option | Description |
|--------|-------------|
| `--prompt`, `-p` | Prompt text (repeat for batch mode) |
| `--model`, `-m` | Model ID (see Models table) |
| `--aspect`, `-a` | Aspect ratio: 16:9 (default), 9:16 |
| `--count` | Number of images: 1-4 (default: 2) |
| `--project-id` | Reuse existing project |
| `--verbose` | Enable debug logging |
| `--login` | Authenticate and save cookies, then exit |
| `--cookie-path` | Custom cookie file path |
| `--profile-dir` | Chrome profile directory |

## Models

| Model | Description |
|-------|-------------|
| `NARWHAL` | Nano Banana 2 (default, fast) |
| `NANO_BANANA_PRO` | Nano Banana Pro |

## Optional Verification Helper

If `/home/admin1/.openclaw/workspace/scripts/agent-browser-cdp.sh` exists, it is a convenient helper for screenshots and browser inspection after generation:

```bash
bash /home/admin1/.openclaw/workspace/scripts/agent-browser-cdp.sh --full screenshot /tmp/flow.png
bash /home/admin1/.openclaw/workspace/scripts/agent-browser-cdp.sh snapshot -c
```

This helper is optional. Generation must not depend on `agent-browser` being installed.

## Environment Variables

| Variable | Description |
|----------|-------------|
| `FLOW_WEB_PROXY` | Preferred proxy for shell/API requests |
| `HTTPS_PROXY` / `HTTP_PROXY` | Standard proxy env vars |
| `FLOW_WEB_DATA_DIR` | Data directory |
| `FLOW_WEB_COOKIE_PATH` | Cookie file path |
| `FLOW_WEB_CHROME_PROFILE_DIR` | Local Chrome user data dir when not on WSL |
| `FLOW_WEB_CHROME_PATH` | Chrome executable path for non-WSL environments |
| `FLOW_WEB_DEBUG_PORT` | Fixed Chrome debug port |
| `FLOW_WEB_CHROME_EXE_WIN` | Windows Chrome path override when running from WSL |
| `FLOW_WEB_CHROME_USER_DATA_DIR_WIN` | Windows Chrome user data dir override when running from WSL |
| `FLOW_WEB_CHROME_EXTRA_ARGS` | Extra Chrome args |
| `AGENT_BROWSER_CHROME_PROXY_SERVER` | Browser proxy used by host Chrome |
| `AGENT_BROWSER_USER_DATA_DIR_WIN` | Windows-side Chrome debug profile override |
| `AGENT_BROWSER_CMD_EXE_WSL` | WSL path to `cmd.exe` |
| `BAOYU_CHROME_PROFILE_DIR` | Shared Chrome profile override |
