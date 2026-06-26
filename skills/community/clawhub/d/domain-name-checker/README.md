# 🌐 domain-name-checker

> Check domain availability and brainstorm names — right from your AI assistant.

**domain-name-checker** is an [OpenClaw](https://github.com/eagerbots/openclaw) agent skill that lets you check domain availability across 10+ TLDs, get smart name suggestions when .com is taken, and even brainstorm domain names from a plain-English description using an LLM.

No domain registrar account needed. No API key required for basic checks.

---

## Features

- ✅ **Multi-TLD sweep** — checks `.com .net .org .io .ai .co .app .dev .so .xyz` in parallel
- 🔍 **DNS + optional whois** cross-check for accuracy
- 💡 **Auto-suggests alternatives** when .com is taken (prefixes like `get-`, `use-`, suffixes like `-app`, `-hq`)
- 🧠 **LLM brainstorm mode** — describe your idea, get 10 candidate names checked automatically
- 🎨 **Rich terminal tables** — color-coded (green = available, red = taken, yellow = unknown)
- 🔗 **Namecheap registration links** for available domains

---

## Install via ClaWHub

```bash
clawhub install domain-name-checker
```

---

## Usage

### Via your AI assistant (OpenClaw)

Just ask naturally:

> "Is eagerbots available?"  
> "Check if openclaw.ai is taken"  
> "Find me a domain for a tool that checks eBay prices"  
> "Brainstorm domain names for my new dev tool"  
> "What domains are available for clawbay and openclaw?"

### Direct CLI usage

```bash
# Check a name across all TLDs
python scripts/check.py eagerbots

# Check a specific full domain
python scripts/check.py eagerbots.ai

# Check multiple names at once
python scripts/check.py eagerbots clawbay openclaw

# Brainstorm names from a description (requires OPENROUTER_API_KEY)
OPENROUTER_API_KEY=sk-... python scripts/check.py --brainstorm "a tool for checking eBay prices"
```

### With uv (recommended)

```bash
uv run scripts/check.py eagerbots
```

---

## Example output

```
╭─────────────────────────────────────────────────╮
│          eagerbots — TLD sweep                  │
├─────────────────────────┬──────────────┬────────┤
│ Domain                  │ Status       │ Reg    │
├─────────────────────────┼──────────────┼────────┤
│ eagerbots.com           │ ❌ Taken      │        │
│ eagerbots.net           │ ✅ Available  │ 🔗     │
│ eagerbots.io            │ ✅ Available  │ 🔗     │
│ eagerbots.ai            │ ✅ Available  │ 🔗     │
│ ...                     │ ...          │        │
╰─────────────────────────┴──────────────┴────────╯

.com is taken. Checking alternatives for eagerbots...

╭──────────────────────────────────────────────────╮
│          eagerbots — Alternatives                │
├──────────────────────────┬──────────────┬────────┤
│ geteagerbots.com         │ ✅ Available  │ 🔗     │
│ eagerbotsapp.com         │ ✅ Available  │ 🔗     │
│ ...                      │ ...          │        │
╰──────────────────────────┴──────────────┴────────╯
```

---

## Requirements

- Python 3.9+
- [`uv`](https://github.com/astral-sh/uv) (recommended) or `pip install rich httpx`
- `whois` CLI (optional, improves accuracy — usually pre-installed on macOS/Linux)
- `OPENROUTER_API_KEY` (optional, for brainstorm mode)

---

## How it works

1. **DNS check** via `socket.getaddrinfo()` — if domain resolves, it's taken. NXDOMAIN → likely available.
2. **Whois cross-check** (optional) — subprocess call to system `whois` if available.
3. **Parallel checks** — all TLDs checked concurrently with 3s timeout per domain.
4. **LLM brainstorm** — uses `anthropic/claude-haiku-4-5` via OpenRouter (cheap model) to generate name candidates.

---

## Accuracy note

DNS-based availability checks are a heuristic. A domain that resolves may be parked. A domain that doesn't resolve may still be registered but not pointed anywhere. Always verify on a registrar before purchasing.

---

## Built by [EagerBots](https://github.com/eagerbots)

domain-name-checker is part of the EagerBots OpenClaw skill ecosystem.

MIT License
