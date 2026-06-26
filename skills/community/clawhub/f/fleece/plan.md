  # cli.py — Fleece Companion CLI Plan

## Purpose

A Typer-based CLI that exposes Fleece's credit card research tools as shell commands.
Primary consumers: AI agents (Claude Code, OpenAI Codex, future agentic tools) that need
to query live credit card data without running the Streamlit UI. Also usable by humans.

---

## Design Philosophy

**Agent-first, human-friendly.**

Agents need:
- Machine-readable output (JSON) they can parse without regex
- Deterministic exit codes (0 = success, 1 = tool error, 2 = config error)
- No interactive prompts — all inputs via args/flags
- Self-describing `--help` text so agents can discover commands without docs
- Stdin piping support for chaining commands

Humans need:
- Readable plain-text output by default
- Sensible defaults (no flags required for simple queries)
- Fast feedback on missing API key

---

## Command Structure

```
fleece <command> [args] [options]
```

### Commands

| Command | Args | Key Flags | Description |
|---|---|---|---|
| `card` | `name` | `--json` | Full card report (fees, offer, earnings, credits, benefits) |
| `rates` | `name` | `--category`, `--json` | Earning rates, optionally filtered by spend category |
| `partners` | `name` | `--json` | Transfer partners with ratios |
| `credits` | `name` | `--json` | Statement credits and perks |
| `news` | `name` | `--json` | Changes in the past month |
| `compare` | `card-a`, `card-b` | `--aspects`, `--json` | Side-by-side comparison |
| `wallet` | `cards...` | `--json` | Portfolio gap/overlap analysis (variadic: multiple cards) |
| `roi` | `name` | `--travel`, `--dining`, `--other`, `--json` | First-year ROI given monthly spend |
| `recommend` | `profile` | `--preferences`, `--json` | Card recommendations for a spending profile |

### Global Options (on every command)

| Flag | Default | Description |
|---|---|---|
| `--json / -j` | False | Emit JSON instead of plain text |
| `--api-key` | env | Override `BRAVE_API_KEY` (fallback to `.env`) |
| `--no-dotenv` | False | Skip loading `.env` file |

---

## Output Format

### Plain text (default — human)
Raw string result from the research tool, printed to stdout.

### JSON mode (`--json`)
```json
{
  "command": "card",
  "query": "Chase Sapphire Preferred",
  "result": "...",
  "ok": true,
  "error": null
}
```

Errors always emit JSON with `"ok": false` and `"error": "<message>"` to stderr,
regardless of `--json` flag, so agents can always parse failure.

---

## Exit Codes

| Code | Meaning |
|---|---|
| `0` | Success |
| `1` | Search/tool error (Brave API failure, timeout) |
| `2` | Configuration error (missing API key) |

---

## File Structure

```
fleece/
├── cli.py                  # NEW: Typer app, all commands
├── tools/
│   ├── brave_client.py     # existing
│   ├── credit_card_tools.py # existing — cli.py calls tool fns directly, not via LangChain
│   └── __init__.py
├── requirements.txt        # add: typer[all]
└── tests/
    └── test_cli.py         # NEW: CLI tests via typer.testing.CliRunner
```

### Key architectural decision
`cli.py` calls the underlying search functions in `tools/brave_client.py` **directly**,
bypassing the LangChain tool wrappers. This avoids pulling in the full LangChain agent
stack for a simple CLI query. The LangChain `@tool` decorators stay on
`credit_card_tools.py` for the Streamlit agent — the CLI is a thinner layer.

---

## Implementation Steps

### Step 1 — Add typer to requirements.txt
`typer[all]>=0.12.0` (includes `rich` for pretty output)

### Step 2 — Create cli.py skeleton
- `app = typer.Typer(name="fleece", help="Fleece credit card research CLI")`
- Shared `_get_wrapper(api_key, freshness)` helper that loads `.env`, resolves key, exits
  with code 2 if missing
- Shared `_emit(result, as_json, command, query)` helper that prints plain or JSON

### Step 3 — Implement simple single-arg commands
`card`, `rates`, `partners`, `credits`, `news` — each is ~10 lines:
1. Build wrapper via `_get_wrapper()`
2. Call `search_and_format(wrapper, query)`
3. Call `_emit(result, ...)`

### Step 4 — Implement multi-arg commands
- `compare` — takes two positional args, calls `search_and_format` twice, merges output
- `wallet` — variadic `cards: list[str]`, loops over each card
- `roi` — float flags `--travel`, `--dining`, `--other`; calls search + formats spend math
- `recommend` — takes `profile` positional + optional `--preferences`

### Step 5 — Add stdin support
If a command's primary arg is `-`, read from stdin:
```bash
echo "Chase Sapphire Preferred" | python cli.py card -
```
Useful for agent pipelines.

### Step 6 — Write tests/test_cli.py
Use `typer.testing.CliRunner` to invoke each command with a mocked `search_and_format`.
Test: success path, JSON output, missing API key (exit code 2), search error (exit code 1).

---

## Usage Examples

### Human
```bash
python cli.py card "Chase Sapphire Preferred"
python cli.py compare "Amex Gold" "Chase Sapphire Preferred"
python cli.py roi "Chase Sapphire Preferred" --travel 500 --dining 300 --other 1000
python cli.py wallet "Amex Platinum" "Chase Freedom Unlimited" "Bilt"
```

### Agent / piped
```bash
python cli.py card "Chase Sapphire Preferred" --json | jq '.result'
python cli.py recommend "high dining and travel spend" --preferences "no annual fee" --json
echo "Amex Gold" | python cli.py rates -
```

### Claude Code skill
A future `/card-research` skill could shell out to `cli.py` for live data,
rather than re-implementing the Brave search logic in a prompt.

---

## Out of Scope (for now)
- Auth / user accounts
- Persistent caching of search results
- Card database / local storage
- Streaming output
