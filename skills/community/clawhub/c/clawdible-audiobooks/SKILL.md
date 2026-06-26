---
name: clawdible
description: Search, browse, and manage Audible audiobooks. Use when the user wants to search for audiobooks on Audible, view their library, get book details, purchase a title, or manage their wishlist. Triggers on phrases like "find audiobook", "buy audiobook", "what's in my Audible library", "search Audible for", "add to wishlist". Requires one-time auth setup.
---

# Clawdible

Manage Audible via the `audible` Python library (unofficial API). Works across platforms — macOS, Linux, Windows.

## Dependencies

Both scripts auto-install dependencies on first run via pip:
- `audible` — unofficial Audible API client
- `httpx` — HTTP client

No manual pip install needed.

## Locating the scripts

Resolve the skill directory at runtime:

```bash
SKILL_DIR=$(python3 -c "
import subprocess, json
skills = subprocess.check_output(['openclaw', 'skills', '--json'], text=True)
for s in json.loads(skills):
    if s['name'] == 'clawdible':
        print(s['path']); break
" 2>/dev/null || find ~/.openclaw -name 'audible_cli.py' -path '*/clawdible/*' 2>/dev/null | head -1 | xargs dirname)

SCRIPT="python3 $SKILL_DIR/audible_cli.py"
AUTH="python3 $SKILL_DIR/audible_auth.py"
```

Or use the path OpenClaw provides when loading this skill (available as the skill's directory).

## Setup (one-time)

Auth stored at `~/.config/audible/auth.json` (chmod 600).

**Step 1** — generate login URL:
```bash
python3 audible_auth.py --locale us
```
Send URL to user. They open it on any device and sign into Amazon.

**Step 2** — after login, Amazon redirects to `https://www.amazon.com/ap/maplanding...`. User pastes that URL:
```bash
python3 audible_auth.py --callback '<redirect URL>'
```

**Verify:**
```bash
python3 audible_cli.py status
```

**Locale options:** `us`, `au`, `uk`, `de`, `ca`, `fr`, `in`, `it`, `jp`, `es`
Auth file's `locale_code` is auto-detected; override with `--locale` if needed.

## Commands

All commands accept `--locale LOCALE` and `--json`.

```bash
# Auth status
python3 audible_cli.py status
python3 audible_cli.py status --locale us

# Search catalogue
python3 audible_cli.py search "Project Hail Mary"
python3 audible_cli.py search "Andy Weir" --limit 5 --locale us

# View library
python3 audible_cli.py library
python3 audible_cli.py library --limit 50

# Get book details
python3 audible_cli.py info B08G9PRS1K

# Purchase (requires explicit --confirm — always verify with user first)
python3 audible_cli.py buy B08G9PRS1K --confirm

# Wishlist
python3 audible_cli.py wishlist
python3 audible_cli.py wishlist add B08G9PRS1K
```

## Workflow

**Typical search-and-buy:**
1. `search` — find title, note the ASIN
2. `info <asin>` — confirm correct edition/narrator
3. Confirm purchase with user verbally
4. `buy <asin> --confirm` — execute purchase

**Never run `buy` without explicit user confirmation.**

## Marketplace

- Auto-detects locale from auth file
- Override with `--locale` when needed (e.g. user's account is US but located in AU)
- Fallback purchase URL on API failure: `https://www.audible.com/pd/<asin>` (adjust domain per locale)

## Error Handling

| Error | Cause | Fix |
|---|---|---|
| No auth file | Not set up | Run `audible_auth.py` |
| 401/403 | Token expired | Re-run `audible_auth.py` |
| 404 | Wrong ASIN or locale | Try different `--locale` |
| 429 | Rate limited | Wait and retry |
| Buy fails | API blocked | Send manual URL to user |
| InvalidValue on auth | Code expired | Start auth flow again |

## Notes

- `audible` library is unofficial — Amazon may change their API without notice
- Auth tokens auto-refresh via device private key; re-auth only needed if device is deregistered
- Auth file is chmod 600 (owner-only read/write)
