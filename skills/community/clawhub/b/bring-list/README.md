# 🛒 bring-list — The Best Bring! Skill for OpenClaw

**Lightweight. Most features. Clean code. Privacy-first.**

The only Bring! skill that runs everywhere — just `curl` and `jq`, no Node.js, no Python, no pip, no npm. Works on any Linux, any container, any VPS out of the box.

## Why this is the best all-round Bring! skill

The strongest integration is not merely the one with the most commands. **bring-list** combines the full item lifecycle, secure onboarding, catalog-aware behavior, automation features, and a tiny auditable runtime in one package.

### 🏆 Most features
Other skills only do add + remove. **bring-list** does everything:
- ✅ Add items (with quantity/description like "low fat, 1L")
- ✅ Add multiple items in one go ("Milk, Bread, Cheese|Gouda, Butter|Irish")
- ✅ Preview every change with `--dry-run`
- ✅ Read batch items from stdin or a pipe
- ✅ Match Bring's catalog for reliable native item icons
- ✅ Check off items when you've bought them
- ✅ Uncheck items (move back to shopping list)
- ✅ Remove items completely
- ✅ Remove or check off multiple items at once
- ✅ View all your lists and items
- ✅ JSON output for automation

### 🪶 Lightweight
| | **bring-list** | Others |
|---|---|---|
| Needs | `curl` + `jq` | Node.js + npm, or Python + pip |
| Install time | Instant | Minutes of downloading packages |
| Works in containers | Always | Often breaks |

### 🧠 Built for AI agents
- **Step-by-step Agent Setup Guide** — your agent knows exactly how to help you set up
- **Private terminal setup** — passwords are entered only in your own terminal, never in chat and never stored on disk
- **Default list support** — say "put milk on the list" without naming the list every time
- **Partial name matching** — "einkauf" finds "Einkaufsliste"
- **Smart argument parsing** — the agent figures out what's an item and what's a list name
- **Safe previews** — validate the list and intended change without modifying anything
- **Catalog-aware adds** — optional `smart-add` maps display names to Bring's internal icon IDs

### 🔒 Clean & secure
- Bring! email and password are used only for the initial login and are never stored
- Password entry happens privately in the user's terminal, never in agent chat or command arguments
- The protected token cache and preference files are enforced as owner-only
- No malware, remote code, or third-party telemetry
- No third-party services — talks only to Bring!'s official API and public catalog
- Fully auditable: one bash script, no hidden runtime dependency chain

### ⚙️ Complete without becoming heavy
- Full lifecycle: view, add, batch-add, check off, restore, and permanently remove
- Catalog-aware IDs preserve native Bring! icons while localized names remain human-readable
- Dry-run works across every modifying command, not merely adds
- stdin, batch operations, partial list matching, default lists, and JSON output cover both chat agents and shell automation
- Automatic refresh-token handling avoids repeated password use

## Installation

```bash
clawhub install bring-list
```

## Quick Setup

Tell your agent: *"Set up the Bring shopping list skill"* — it will walk you through it.

Or manually:
```bash
scripts/bring.sh setup
```

You need a [Bring!](https://getbring.com) account (free). If you signed up via Google/Apple, set a direct password first in the Bring! app (Settings → Account → Change Password).

## Just Talk Naturally

- *"Put milk and eggs on the shopping list"*
- *"What's on our list?"*
- *"Check off the butter, we got it"*
- *"Add bread, cheese, and yogurt to the list"*
- *"Remove the tomatoes"*
- *"Preview adding paprika with a native Bring icon"*

Your agent handles the rest.

## Configuration

`~/.config/bring/credentials.json`:
```json
{
  "default_list": "Einkaufsliste",
  "country": "DE",
  "locale": "de-DE"
}
```

- `default_list` — Skip typing the list name every time
- `country` — Item catalog language (default: `DE`). Use `AT`, `CH`, `US`, `FR`, etc.
- `locale` — Optional catalog override for `smart-add`; normally derived from `country`

## Advanced CLI usage

```bash
# Preview without changing the list
scripts/bring.sh add --dry-run "Milk" "1L"

# Use Bring's catalog/internal item ID so the native icon is preserved
scripts/bring.sh smart-add "Paprika" "2 Stück"

# Read one item per line; use item|specification when needed
printf '%s\n' "Milk|1L" "Bread" | scripts/bring.sh add-multi -
```

## Good to Know

- **Shared lists sync instantly** — your partner sees changes in real time
- **Lists must be created/deleted in the Bring! app** — API limitation, not ours
- **Special characters fully supported** — umlauts, quotes, emoji, all fine
- **Token auto-refreshes** — rerun setup only if the refresh token expires

## Privacy

No third-party services or telemetry — the skill talks only to Bring!'s own services: `api.getbring.com` for accounts/lists and `web.getbring.com` for public catalog matching/display names.

Run `scripts/bring.sh setup` in your own terminal. It reads the password with `read -s`, uses the email and password for that login, and stores neither. Optional list/country preferences live in `~/.config/bring/credentials.json`; the owner-only access/refresh token lives in `~/.cache/bring/token.json` and remains a secret.

Legacy `email` or `password` fields in `credentials.json` are removed automatically when the profile is loaded or setup is rerun.

## License

MIT-0
