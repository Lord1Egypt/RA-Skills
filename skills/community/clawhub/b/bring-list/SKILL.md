---
name: bring-list
description: "Manage Bring! shopping lists (Einkaufsliste / grocery list) — add, catalog-match, preview, remove, check off items, batch/stdin ops, and default lists. Use when a user wants to set up Bring! or manage shopping-list items. Setup passwords are entered only in the user's own terminal and are never accepted in chat or stored on disk."
metadata:
  openclaw:
    emoji: "🛒"
    requires:
      bins:
        - curl
        - jq
---

# Bring! Shopping Lists

Manage Bring! shopping lists via the unofficial REST API. Requires `curl` and `jq`.

## Why this is the best all-round Bring! skill

- **Complete item lifecycle:** view, add, batch-add, check off, restore, permanently remove, and perform multi-item operations.
- **Private onboarding:** neither the Bring! email nor password is stored; password entry happens only in the user's terminal, never in agent chat or command arguments.
- **Catalog-aware without npm:** `smart-add` preserves native Bring! icons, while normal output and follow-up commands translate internal catalog IDs back to localized names.
- **Safe and automation-ready:** every modifying command supports `--dry-run`; batch input also works through stdin, and read commands support JSON.
- **Small auditable runtime:** one Bash script, only `curl` and `jq`, no package-manager install, hidden dependency chain, third-party service, or telemetry.
- **Agent-friendly defaults:** guided first setup, automatic token refresh, default lists, and partial case-insensitive list matching.

## Security & data handling

Be upfront with the user about what this skill accesses and stores:

- **Network:** talks only to Bring!'s official services: `api.getbring.com` for account/list operations and `web.getbring.com` for public catalog matching/display names. No third-party services or telemetry.
- **Files written locally:**
  - `~/.config/bring/credentials.json` — optional default-list and country preferences; no login credentials.
  - `~/.cache/bring/token.json` — cached access/refresh token. This remains a secret and is stored owner-only.
- **Password handling:** the password is entered only in the user's own terminal for `scripts/bring.sh setup`, used for that login, and never written to disk or accepted in chat. If the refresh token eventually expires, the user runs setup again.
- **Destructive actions:** `remove` / `remove-multi` permanently delete items, and every change syncs instantly to everyone on a shared list. Confirm with the user before removing items, especially on shared lists.

## Agent Setup Guide

When a user asks you to set up or use Bring for the first time, follow these steps. **Never request, receive, or write a Bring! password in chat.**

### Step 1: Check if already configured
Run `scripts/bring.sh lists` first. If it works, setup is already done — skip to usage.

### Step 2: Private terminal setup
Bring! requires an email + password. If the user doesn't have an account yet, they can create one for free at getbring.com or in the Bring! app.

**If they signed up via Google/Apple:** They need to set a direct password first in the Bring! app (Settings → Account → Change Password) before the API works.

Tell the user to run this in **their own terminal**:
```bash
scripts/bring.sh setup
```
The script reads the email and password without echoing the password, uses both for one login, stores neither, caches only a protected refresh token, then asks for a default list. The password must not be pasted into this conversation.

After it completes, ask the user to return here; then run the normal list commands.

### Step 3: Show existing lists
```bash
scripts/bring.sh lists
```
This shows all the user's Bring! lists. The user may have multiple lists, e.g.:
- Einkaufsliste (main grocery list)
- Drogerie (drugstore items)
- Baumarkt (hardware store)
- A shared list with a partner/family

**If the user has NO lists:** Tell them to create one in the Bring! app first. The API does not support creating or deleting lists — this must be done in the app. Once they've created a list, continue with setup.

**Ask the user which list should be the default.** This lets them skip typing the list name every time.

If they have only ONE list: set it as default automatically and inform them.
If they have MULTIPLE lists: show the list names and ask which one to use as default. Explain they can still target other lists by name (e.g., "Put nails on the Baumarkt list").

### Step 4: Confirm setup
Show the user their current list content to confirm everything works:
```bash
scripts/bring.sh show
```
Tell them: "All set! You can now say things like 'Put milk on the list' or 'What's on the shopping list?'"

### Important: Lists can only be managed in the app
The Bring! API does not support creating or deleting lists. If the user asks to create a new list or delete one, tell them:
"Lists can only be created and deleted in the Bring! app. Once you've made the change there, I can immediately work with the new list."

### Handling shared lists
Bring! lists are often shared between family members or partners. Changes made by the agent sync instantly to all devices sharing that list. Inform the user:
- "Any items I add will show up immediately on all phones that share this list."
- This is usually desired (e.g., partner sees the updated grocery list), but worth mentioning.

## Setup (manual / reference)

For non-interactive login, provide `BRING_EMAIL` + `BRING_PASSWORD` as temporary environment variables. Optional preferences live in `~/.config/bring/credentials.json`:

```json
{"default_list": "Einkaufsliste", "country": "DE", "locale": "de-DE"}
```

Interactive setup (TTY required): `scripts/bring.sh setup`. It never writes the email or password to disk. Existing legacy `email` and `password` profile fields are removed automatically.

## Commands

All commands accept a list name (partial match) or UUID. If `default_list` is configured, the list argument can be omitted.

```bash
# List all shopping lists
scripts/bring.sh lists

# Show items on a list (or default list)
scripts/bring.sh show
scripts/bring.sh show "Einkaufsliste"

# Add item (with optional specification/quantity)
scripts/bring.sh add "Milch" "fettarm, 1L"
scripts/bring.sh add "Einkaufsliste" "Milch" "fettarm, 1L"

# Preview any modifying command without changing the list
scripts/bring.sh add --dry-run "Milch" "fettarm, 1L"

# Match Bring's public catalog and use its internal item ID for reliable icons
scripts/bring.sh smart-add "Paprika" "2 Stück"

# Add multiple items at once (use "item|spec" for specifications)
scripts/bring.sh add-multi "Brot" "Käse|Gouda" "Butter|irische"

# Add newline-separated items from stdin (same item|spec format)
printf '%s\n' "Milch|1L" "Brot" | scripts/bring.sh add-multi -

# Complete/check off item (moves to recently purchased)
scripts/bring.sh complete "Milch"

# Complete multiple items at once
scripts/bring.sh complete-multi "Milch" "Brot" "Käse"

# Move item back from recently to purchase list
scripts/bring.sh uncomplete "Milch"

# Remove item entirely
scripts/bring.sh remove "Milch"

# Remove multiple items at once
scripts/bring.sh remove-multi "Milch" "Brot" "Käse"
```

## Targeting specific lists

When the user has multiple lists, they can target a specific one by name:
- "Put nails on the **Baumarkt** list" → `scripts/bring.sh add "Baumarkt" "Nails"`
- "What's on the **Drogerie** list?" → `scripts/bring.sh show "Drogerie"`

List names support partial case-insensitive matching, so "einkauf" matches "Einkaufsliste".

If no list is specified, the `default_list` from the config is used.

## JSON Output

Append `--json` to `lists` and `show` for raw JSON:

```bash
scripts/bring.sh lists --json
scripts/bring.sh show --json
scripts/bring.sh show "Einkaufsliste" --json
```

## Notes

- Specifications are the small description text under an item (e.g., quantity, brand)
- `complete` moves items to "recently purchased" (like checking off in the app)
- `remove` deletes items entirely from the list
- Token is cached at `~/.cache/bring/token.json` and auto-refreshed
- Changes sync instantly to all devices sharing the list
- Item names with special characters (quotes, umlauts, emoji) are fully supported
- Bring! requires a direct account password — Google/Apple SSO logins don't work with the API
- `country` in credentials.json controls the item catalog language (default: `DE`)
- `locale` optionally overrides the catalog locale used by `smart-add` (for example `de-DE`); otherwise it is derived from `country`
- `smart-add` keeps ordinary `add` unchanged: use it when matching Bring's catalog/icon matters, and use `add` for custom item names
- Human-readable `show` output translates catalog IDs back to localized display names; `show --json` remains the untouched API response
- `--dry-run` is accepted by every modifying command; it may perform read-only validation but never submits a list change
- `add-multi -` reads one item per line from stdin; append `|specification` when needed
- When showing items to the user, consider only showing the "TO BUY" section unless they specifically ask for recently completed items — the recently list can be very long
- If `remove` fails with "not found", suggest the user check the exact item name with `show`
- **Creating/deleting lists is not supported by the Bring! API** — users must manage lists in the Bring! app
