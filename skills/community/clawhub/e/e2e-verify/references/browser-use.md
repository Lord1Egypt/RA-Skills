# Engine: browser-use (AI-driven ephemeral verification)

How to run `e2e-verify` Route A with [browser-use](https://github.com/browser-use/browser-use) — an open-source (MIT) Python library that gives an LLM agent a real headless Chromium: it opens pages, clicks, types, reads the DOM, takes screenshots, and reports what it found. Unlike Playwright (fixed scripts), browser-use **decides what to click** from natural-language intent — so it can explore flows a fixed test would miss.

Pick this engine when it's installed (`python -c "import browser_use"` succeeds), when the user names it ("run browser-use"), or when the run benefits from exploratory AI walking — the agent *finding* broken flows rather than re-running known paths. Works for any web frontend (Next.js/React/Vue/Svelte/vanilla) and for Tauri apps via their Vite dev server. Not for native mobile (`maestro-mobile-test`).

The discipline is identical to every other `e2e-verify` engine: safety gate first, ration by journey risk, quote what you observed, never report "passed" on something you didn't run. All paths below are relative to the `e2e-verify` skill root.

## Prerequisites

| Requirement | How to check | Install |
|---|---|---|
| Python 3.11+ | `python --version` | System Python (or `brew install python` / `apt install python3`) |
| uv (package manager) | `uv --version` | `pip install uv` — or `brew install uv` (macOS) |
| browser-use venv | `python -c "import browser_use"` | Run `scripts/browser-use/setup.sh` (handles everything) |
| Playwright Chromium | `playwright install chromium` | Installed automatically by `scripts/browser-use/setup.sh` |
| An LLM API key | Any provider env var | OpenAI, Gemini, DashScope, Anthropic, Groq, OpenRouter, or Ollama (local) |

### One-time setup script

The `scripts/browser-use/setup.sh` script creates a dedicated venv, installs browser-use + Playwright, and writes an activation helper:

```bash
bash skills/e2e-verify/scripts/browser-use/setup.sh
```

What it does:
1. Creates `~/AppData/Local/browser-use/` (Windows) or `~/.browser-use/` (macOS/Linux)
2. Creates a Python 3.13 venv inside it
3. Installs `browser-use`, `playwright`, and dependencies
4. Runs `playwright install chromium` (the browser binary)
5. Writes an `activate.sh` that sets the right PATH and loads API keys
6. Writes a `config.py` with your LLM endpoint and model

### ⚠️ The PYTHONPATH pitfall

If another application sets a global `PYTHONPATH` pointing at its own venv (some Windows apps export one system-wide; pyenv wrappers on macOS), it leaks into any new venv and breaks `pydantic_core`:

```
ModuleNotFoundError: No module named 'pydantic_core._pydantic_core'
```

**Fix:** the `activate.sh` script unsets `PYTHONPATH`. If you ever see this error in a new venv, run `unset PYTHONPATH` after activating.

## The LLM — any OpenAI-compatible endpoint (provider agnostic)

browser-use needs an LLM to drive the agent. The skill auto-detects your provider from standard environment variables — no hardcoded endpoints:

```bash
# Set ONE of these in your shell or .env — the skill does the rest
export OPENAI_API_KEY="sk-..."           # OpenAI
export GEMINI_API_KEY="AIza..."          # Google Gemini
export DASHSCOPE_API_KEY="sk-..."        # Alibaba DashScope / Qwen
export ANTHROPIC_API_KEY="sk-ant-..."    # Anthropic
export GROQ_API_KEY="gsk_..."            # Groq
export OPENROUTER_API_KEY="sk-or-..."    # OpenRouter (any model)
# Or use local Ollama (free, no key): https://ollama.com
```

To override auto-detection, set `BROWSER_USE_LLM_KEY`, `BROWSER_USE_LLM_BASE_URL`, and `BROWSER_USE_LLM_MODEL`.

The `config.py` in `scripts/browser-use/` handles detection:

```python
from browser_use.llm import ChatOpenAI
from config import API_KEY, BASE_URL, MODEL  # auto-detected

llm = ChatOpenAI(model=MODEL, api_key=API_KEY, base_url=BASE_URL)
```

**Tested against:** browser-use 0.13.x, Playwright 1.61.x. Compatible LLM providers include Qwen (DashScope), Gemini, GLM, OpenAI, Anthropic, Groq, and local Ollama — any OpenAI-compatible endpoint.

## The core workflow

1. **Start the dev server** the repo's own way (`npm run dev`, `npx next dev`, etc.). Confirm it responds before launching the agent.
2. **Write the verification script** using the template in `scripts/browser-use/verify_template.py`.
3. **Run it** against localhost.
4. **Read the agent's report** — it returns structured findings, not just pass/fail.

> **Cost awareness:** each run is an LLM agent loop — 5-15 steps of vision + DOM context. That's non-trivial token spend (often 10K-50K tokens per run depending on steps and page size). Budget accordingly for CI — prefer Ollama or a cheap model for smoke tests, reserve frontier models for exploratory runs.

### The verification script template

Every test is a Python script that:
1. Loads LLM credentials from `config.py`
2. Creates an `Agent` with a natural-language task
3. Runs it and prints the structured result

```python
import asyncio
from browser_use import Agent
from browser_use.llm import ChatOpenAI
from config import API_KEY, BASE_URL, MODEL

async def main():
    agent = Agent(
        task="Go to http://localhost:3000 and verify: 1) page loads, "
             "2) the login button is visible, 3) clicking it shows the login form. "
             "Report any errors.",
        llm=ChatOpenAI(model=MODEL, api_key=API_KEY, base_url=BASE_URL),
        headless=True,
    )
    result = await agent.run(max_steps=15)
    print(result.final_result())

asyncio.run(main())
```

## Writing good verification tasks

The agent follows natural-language intent. Be specific about what to check and what to report:

```python
# VAGUE — agent will explore but may miss edge cases
task = "Test the checkout flow."

# GOOD — specific steps, specific assertions, specific report format
task = """
Go to http://localhost:3000. Verify the product catalog:
1. Confirm at least 3 products are listed
2. Click "Add to Cart" on the first product
3. Navigate to the cart and verify the item appears
4. Verify the cart total is displayed
5. Report any console errors or broken images
"""
```

### Structured output (Pydantic schemas)

For assertions you can programmatically check:

```python
from pydantic import BaseModel

class CheckoutResult(BaseModel):
    order_placed: bool
    order_total: str
    items_in_cart: int
    errors_found: list[str]

agent = Agent(
    task="Complete a checkout flow...",
    llm=llm,
    output_model_schema=CheckoutResult,
)
result = await agent.run()
parsed = CheckoutResult.model_validate_json(result.final_result())
```

## Capabilities and limits

| What browser-use can do | What it cannot do |
|---|---|
| Navigate to any URL | Drive native mobile apps (use Maestro) |
| Click, type, scroll, screenshot | Interact with browser extension popups |
| Read DOM, extract structured data | Test extension options pages (auto-closed by design) |
| Assert on visible text and elements | Run as fast as a fixed Playwright script |
| Test localhost, staging, production | Test behind auth walls without credentials |
| Test mobile-responsive layouts (emulation) | Drive the real mobile Safari/Chrome engine |
| Self-heal when selectors drift | Guarantee it found every bug (it's an AI, not a fuzzer) |

### Mobile emulation

```python
from browser_use.browser import BrowserProfile

profile = BrowserProfile(
    user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 17_0...)",
    window_size={"width": 390, "height": 844},
    device_scale_factor=3,
)
agent = Agent(task="...", llm=llm, browser_profile=profile)
```

### Tauri apps

Point browser-use at the Vite dev server. The native shell (tray, menus, file dialogs) is out of reach, but the entire web frontend — where 95% of bugs live — is fully testable:

```python
task = "Go to http://localhost:1420 and verify the dashboard..."
```

## Running tests

### Headless (default, CI)

```python
agent = Agent(task="...", llm=llm, headless=True)
```

### Headed (debugging — watch the agent)

```python
agent = Agent(task="...", llm=llm, headless=False)
```

### Parallel agents (multiple flows at once)

```python
import asyncio
from browser_use import Agent
from browser_use.browser import BrowserProfile, BrowserSession
from browser_use.llm import ChatOpenAI
from config import API_KEY, BASE_URL, MODEL

async def main():
    llm = ChatOpenAI(model=MODEL, api_key=API_KEY, base_url=BASE_URL)
    browser_session = BrowserSession(browser_profile=BrowserProfile(keep_alive=True))
    await browser_session.start()

    agents = [
        Agent(task="Test login flow...", llm=llm, browser_session=browser_session),
        Agent(task="Test catalog...", llm=llm, browser_session=browser_session),
    ]
    await asyncio.gather(*[a.run() for a in agents])

    await browser_session.kill()
```

## Durable tests vs ephemeral checks

Same routing as `e2e-verify` (*"durable" = a test committed to the repo that runs in CI forever; "ephemeral" = a one-off run for immediate confidence in a change*):

| Signal | Route |
|---|---|
| "Does my change work?", pre-merge confidence | **Ephemeral** — run the agent once, read the report |
| "Add e2e tests", critical flow, regression risk | **Durable** — write a Python script that runs in CI |
| Feature just built | **Both** — smoke now, durable script as the deliverable |

For durable CI tests, commit the verification scripts under `tests/browser-use/` in the repo and run them in GitHub Actions:

```yaml
# .github/workflows/browser-use.yml
- name: Run browser-use E2E
  run: |
    source ~/.browser-use/activate.sh
    python tests/browser-use/login_flow.py
```

## Examples

### Example 1: post-feature smoke

**User:** "I just finished the login redesign — verify it works."

**Claude:** Confirms the dev server is running (`curl localhost:3000` returns 200). Writes a verification script: navigate to `/login` → verify email and password fields are visible → type test credentials → click Sign In → verify redirect to dashboard. Runs it headless, quotes the agent's observations per step. Reports: *"Walked login flow against localhost:3000 (seeded account): email field rendered (observed: placeholder 'name@company.com'), password field rendered, Sign In clicked → redirected to /dashboard (observed: 'Welcome' heading). Console: 1 warning (deprecated API, non-blocking). Not walked: OAuth providers, password reset."*

### Example 2: exploratory regression check

**User:** "Run browser-use against the new checkout flow before I merge."

**Claude:** Identifies the checkout routes from the diff. Writes a task: add item to cart → proceed to checkout → fill shipping → verify order summary totals → assert no console errors. Runs headless, reports findings: *"Walked checkout flow: cart→checkout→shipping→summary (observed: tax calculated correctly at $4.20, total $54.20). Finding: the 'Apply Discount' button is visible but non-functional on mobile viewport (390px) — clicking does nothing, no network request fired."*

## Proving red-capable

The deterministic red/green discipline from `e2e-verify` (Playwright) doesn't map cleanly to an AI agent — its responses are non-deterministic. Instead of asserting wrong text, use a reliable environmental red proof:

1. **Point the agent at a dead port** (e.g., `http://localhost:9999`) → verify it reports failure / connection refused. That's your red.
2. **Point it at the live server** → verify it reports success. That's your green.

This tests the harness (does the script correctly surface failures?) without depending on the agent's interpretation of a specific assertion.

## Anti-patterns

- ❌ Testing against production with real user data — always localhost or staging.
- ❌ Hardcoding API keys in test scripts — use `config.py` or env vars.
- ❌ Using `headless=False` in CI — it fails without a display.
- ❌ Writing vague tasks ("test the app") — the agent explores but misses edge cases. Be specific.
- ❌ Reporting "e2e passes" — the honest claim is "no issues found in the paths walked", paths listed.
- ❌ Shipping a test never seen red — break it, quote the red, revert, quote the green.
- ❌ Forgetting to start the dev server — a dead port produces "every flow is broken."
- ✅ Dev server running → specific task with steps → headless run → quote observations per flow → not-walked list always present.

## Troubleshooting

| Problem | Cause | Fix |
|---|---|---|
| `ModuleNotFoundError: pydantic_core` | PYTHONPATH leaking from another venv | `unset PYTHONPATH` after activating |
| Agent can't reach localhost | Server not running | Start `npm run dev` first, confirm `curl localhost:PORT` returns 200 |
| `401 Invalid API key` | Wrong endpoint for the key | Verify the endpoint URL matches the key's plan/region |
| Agent clicks wrong element | Ambiguous task description | Be more specific: "click the 'Sign In' button at the top right" |
| Agent too slow | Vision mode on a slow model | Set `use_vision=False` for DOM-only mode |
| Gemini: `frequency_penalty` error | Gemini's OpenAI-compat layer doesn't support it | Use a different provider (Qwen, OpenAI, Anthropic, or Ollama), or pass `frequency_penalty=0` |
| Tauri app: only tests frontend | Can't drive native shell | Accept the limit; 95% of bugs are in the web layer |
| Extension popup not testable | browser-use auto-closes `chrome-extension://` | Test extension effects on web pages, not the popup UI |

## Scripts

Reusable scripts ship with `e2e-verify` in `scripts/browser-use/`:

| Script | Purpose |
|---|---|
| `scripts/browser-use/setup.sh` | One-time venv creation + browser-use install |
| `scripts/browser-use/verify_template.py` | Copy-and-edit template for new verification flows |
| `scripts/browser-use/config.py` | LLM endpoint config (read from env vars) |

## Links

- browser-use repo: https://github.com/browser-use/browser-use
- browser-use docs: https://docs.browser-use.com
- Examples: https://github.com/browser-use/browser-use/tree/main/examples
- browser-harness (real-browser mode): https://github.com/browser-use/browser-harness
