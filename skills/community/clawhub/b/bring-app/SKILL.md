---
name: bring-shopping-list
description: Manage Bring! shopping lists via CLI — add, remove, complete, and list items. Use when the user wants to interact with Bring! grocery/shopping lists: add items, remove items, check items off, view list contents, or list available shopping lists. Also matches phrases like "bring list", "shopping list", "Einkaufsliste", "add to shopping list", "Bring! API".
---

# Bring! Shopping List Skill

Manage Bring! shopping lists using the `bring-api` Python package via a bundled CLI script.

## Setup (one-time)

1. Install the Python dependency:

   ```bash
   python3 -m pip install bring-api
   ```

2. Configure credentials — set env vars `BRING_EMAIL` and `BRING_PASSWORD`, or create `~/.openclaw/credentials/bring.json`:

   ```json
   {
     "email": "your@email.com",
     "password": "your_password"
   }
   ```

3. (Optional) Set a default list via env var `BRING_LIST` (matches list title, case-insensitive).

## Usage

All commands use the bundled script `scripts/bring.py`.

### List all shopping lists

```bash
python3 scripts/bring.py list
```

### Show items in a list

```bash
python3 scripts/bring.py items
python3 scripts/bring.py items --list "Einkauf"
```

### Add an item

```bash
python3 scripts/bring.py add "Milch"
python3 scripts/bring.py add "Milch" --spec "fettarm"
python3 scripts/bring.py add "Zitronen" --list "Party"
```

### Remove an item

```bash
python3 scripts/bring.py remove "Milch"
python3 scripts/bring.py remove "Milch" --list "Einkauf"
```

### Complete (check off) an item

```bash
python3 scripts/bring.py complete "Milch"
python3 scripts/bring.py complete "Milch" --list "Einkauf"
```

## Common Patterns

- When the user says "add X to shopping list", extract the item name and optional spec, then call `add`.
- When the user says "remove X from shopping list", call `remove`.
- When the user says "check off X" or "done with X", call `complete`.
- When the user says "show shopping list" or "what's on the list", call `items`.
- If the user has multiple lists, use `--list "Name"` to target the right one.
- If unsure which list, call `list` first and ask the user to confirm.

## Troubleshooting

- **Authentication failed**: Check email/password in `~/.bring.json` or env vars. Bring! uses the email from the app account settings.
- **List not found**: List names are case-insensitive but must match exactly. Use `list` to see available names.
- **Item not found**: Item matching is case-insensitive. If duplicates exist, the first match is used.
- **ModuleNotFoundError**: Run `python3 -m pip install bring-api`.

## API Reference

Based on [`miaucl/bring-api`](https://github.com/miaucl/bring-api) (unofficial Bring! API, MIT license).

The CLI wraps these core API methods:
- `load_lists()` → all shopping lists
- `get_list(listUuid)` → items in one list
- `batch_update_list(listUuid, item, ADD)` → add item
- `batch_update_list(listUuid, item, REMOVE)` → remove item
- `batch_update_list(listUuid, item, COMPLETE)` → check off item

## License

This skill uses the MIT-licensed `bring-api` package. Bring! trademarks belong to Bring! Labs AG. This is not affiliated with or endorsed by Bring! Labs AG.
