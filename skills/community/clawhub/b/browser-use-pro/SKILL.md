---
name: browser-use
description: "AI-powered browser automation for complex multi-step web workflows. Uses Browser-Use framework when OpenClaw's built-in browser tool can't handle login flows, anti-bot sites, or 5+ step sequences."
---

# Browser-Use — AI Browser Automation

## Security & Privacy

- **No credential logging**: Passwords are handled via Browser-Use's `sensitive_data` parameter — the LLM never sees real credentials, only placeholder tokens.
- **User-initiated Chrome connection**: CDP mode (connecting to real Chrome) is opt-in and requires the user to manually launch Chrome with debug flag. The skill never silently connects to running browsers.
- **All packages are open-source**: Dependencies are `browser-use` (38k+ ⭐ on GitHub), `playwright` (by Microsoft), and `langchain-openai` — all widely audited open-source tools.
- **Local execution only**: Scripts run locally on the user's machine. No data is sent to any server except the configured LLM API for step-by-step reasoning.
- **Domain restriction available**: Use `allowed_domains` parameter to restrict which websites the agent can visit.
- **No telemetry**: This skill does not collect, store, or transmit any usage data.

## When to Use Browser-Use vs Built-in Tool

| Scenario | Built-in tool | Browser-Use |
|----------|:-:|:-:|
| Screenshot / click one button | ✅ Free & fast | ❌ Overkill |
| 5+ step workflow (login→navigate→fill→submit) | ❌ Breaks easily | ✅ |
| Anti-bot sites (real Chrome needed) | ❌ | ✅ |
| Batch repetitive operations | ❌ | ✅ |

**Cost**: Browser-Use calls an external LLM per step (costs money + slower). Use built-in tool for simple actions.

## Execution Flow

### 1. Check Environment
```bash
test -d ~/browser-use-env && echo "Installed" || echo "Need install"
```

### 2. First-Time Setup (once only)
```bash
python3 -m venv ~/browser-use-env
source ~/browser-use-env/bin/activate
pip install browser-use playwright langchain-openai
playwright install chromium
```

### 3. Choose Mode
- **Mode A — Built-in Chromium**: For simple automation or when detection doesn't matter. Runs immediately.
- **Mode B — Real Chrome CDP**: For anti-bot sites or when user's login session is needed. Requires user action.

Mode B setup — prompt user:
> Please quit Chrome completely (Mac: Cmd+Q), then tell me "done"

After user confirms:
```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 &
```
Verify: `curl -s http://127.0.0.1:9222/json/version`

### 4. Write Script and Run
Write script to user's workspace, then:
```bash
source ~/browser-use-env/bin/activate
python3 script_path.py
```

### 5. Report Results
Return results to user. On failure, follow the troubleshooting tree below.

## Script Template

```python
import asyncio
from browser_use import Agent, ChatOpenAI, Browser

async def main():
    # LLM — any OpenAI-compatible API
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        api_key="<YOUR_API_KEY>",  # From env var or user config
        base_url="https://api.openai.com/v1",
    )

    # Mode A: Built-in Chromium
    browser = Browser(headless=False, user_data_dir="~/.browser-use/task-profile")
    # Mode B: Real Chrome (user must launch with --remote-debugging-port=9222)
    # browser = Browser(cdp_url="http://127.0.0.1:9222")

    agent = Agent(
        task="Detailed step-by-step task description (see guide below)",
        llm=llm, browser=browser,
        use_vision=True, max_steps=25,
    )
    result = await agent.run()
    print(result)

asyncio.run(main())
```

## Task Writing Guide

### ✅ Good: Specific steps
```python
task = """
1. Open https://www.reddit.com/login
2. Enter username: x_user
3. Enter password: x_pass
4. Click login button
5. If CAPTCHA appears, wait 30s for user to complete
6. Navigate to https://www.reddit.com/r/xxx/submit
7. Enter title: xxx
8. Enter body: xxx
9. Click submit
"""
```

### ❌ Bad: Vague
```python
task = "Post something on Reddit"
```

### Tips
- **Keyboard fallback**: Add "If button can't be clicked, use Tab+Enter"
- **Error recovery**: Add "If page fails to load, refresh and retry"
- **Sensitive data**: Use placeholders + `sensitive_data` parameter

## Credential Security

```python
agent = Agent(
    task="Login with x_user and x_pass",
    sensitive_data={"x_user": "real@email.com", "x_pass": "S3cret!"},
    use_vision=False,  # Disable screenshots when handling passwords
    llm=llm, browser=browser,
)
```

## Key Parameters

| Parameter | Purpose | Recommended |
|-----------|---------|-------------|
| `use_vision` | AI sees screenshots | True normally, False with passwords |
| `max_steps` | Max actions | 20-30 |
| `max_failures` | Max retries | 3 (default) |
| `flash_mode` | Skip reasoning | True for simple tasks |
| `extend_system_message` | Custom instructions | Add specific guidance |
| `allowed_domains` | Restrict URLs | Use for security |
| `fallback_llm` | Backup LLM | When primary is unstable |

## Troubleshooting

```
Detected as automation?
  └→ Switch to Mode B (real Chrome)

CAPTCHA / human verification?
  └→ Prompt user to complete manually, add wait time in task

LLM timeout?
  └→ Set fallback_llm or use faster model

Action succeeded but no effect (e.g. post not published)?
  └→ 1. Check if platform anti-spam blocked it (common with new accounts)
     2. Add explicit confirmation steps to task

Website UI changed, can't find elements?
  └→ Browser-Use auto-adapts, but add fallback paths in task
```

## LLM Compatibility

| LLM | Works | Notes |
|-----|:---:|-------|
| GPT-4o / 4o-mini | ✅ | Best choice, recommended |
| Claude | ✅ | Works well |
| Gemini | ❌ | Structured output incompatible |
