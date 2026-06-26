---
name: allourthings
description: >
  Household and personal inventory management. Use this skill to add, find,
  update, search, or delete items in the user's AllOurThings vault — covering
  anything they own: appliances, electronics, tools, furniture, collectibles,
  warranties, receipts, manuals, and more. Also handles attachments such as
  photos, receipts, and warranty documents. Triggers on questions about
  possessions, household items, warranties, purchase history, or "what do I
  own".
homepage: https://allourthings.io
metadata:
  {
    "openclaw":
      {
        "emoji": "📦",
        "primaryEnv": "ALLOURTHINGS_DATA_DIR",
        "requires": { "env": ["ALLOURTHINGS_DATA_DIR"] },
        "install": [],
        "mcp":
          {
            "servers":
              {
                "allourthings":
                  {
                    "command": "npx",
                    "args": ["-y", "@allourthings/mcp-server"],
                    "env":
                      {
                        "ALLOURTHINGS_DATA_DIR": "${ALLOURTHINGS_DATA_DIR}",
                      },
                  },
              },
          },
      },
  }
---

# AllOurThings

Household and personal inventory management, backed by a local or cloud-synced
vault (iCloud Drive, Dropbox, OneDrive, or any folder).

## When to Use

✅ **USE this skill when the user asks about:**

- Their belongings, possessions, or household items
- Appliances, electronics, tools, furniture, vehicles, collectibles
- Warranties — "is my TV still under warranty?", "what warranties are expiring?"
- Purchase history — "when did I buy my washing machine?", "how much did I pay?"
- Finding something — "where did I put my drill?", "do I own a label maker?"
- Adding or cataloguing a new item
- Searching across their inventory — "list all Bosch appliances"
- Attaching or retrieving photos, receipts, manuals, or warranty documents

## When NOT to Use

❌ **DON'T use this skill when:**

- The user is asking about general product information or reviews (no inventory context)
- The question is about shopping or buying something new (unless checking existing inventory first)
- The vault is not configured — prompt the user to set `ALLOURTHINGS_DATA_DIR`

## Setup

The user must set `ALLOURTHINGS_DATA_DIR` to the path of their AllOurThings
vault folder.

```bash
# Example — iCloud Drive vault
export ALLOURTHINGS_DATA_DIR="$HOME/Library/Mobile Documents/com~apple~CloudDocs/Documents/allourthings-vault"

# Example — Dropbox
export ALLOURTHINGS_DATA_DIR="$HOME/Dropbox/AllOurThings"

# Example — local folder
export ALLOURTHINGS_DATA_DIR="$HOME/Documents/AllOurThings"
```

Add this to your shell profile (`~/.zshrc`, `~/.bashrc`) to make it permanent.

The vault is a plain folder of JSON files — create it anywhere you like, or
point it at an existing folder to start cataloguing immediately.

## Available Tools

| Tool | Description |
|------|-------------|
| `list_items` | List all items, optionally filtered by category, subcategory, or tags |
| `search_items` | Full-text search across all item fields |
| `get_item` | Retrieve a single item by ID or name |
| `add_item` | Add a new item to the vault |
| `update_item` | Update fields on an existing item |
| `delete_item` | Delete an item and all its attachments |
| `get_item_fields` | List all field names in use across the vault |
| `add_attachment` | Attach a photo, receipt, manual, or warranty document |
| `get_attachment` | Retrieve an attachment's raw bytes |
| `attach_from_url` | Download a file from a URL and attach it to an item |
| `delete_attachment` | Remove an attachment from an item |

## Example Interactions

**"What electronics do I own?"**
→ `list_items` with `category: "Electronics"`

**"Is my dishwasher still under warranty?"**
→ `search_items` for "dishwasher", check `warranty_expires`

**"I just bought a Dyson V15 vacuum for £499"**
→ `add_item` with name, brand, purchase price, and date

**"Show me everything I bought from Amazon last year"**
→ `search_items` for "Amazon" or `list_items` filtered by retailer

**"Attach the receipt for my MacBook"**
→ `add_attachment` with kind `receipt`

## CLI

AllOurThings also ships a standalone CLI (`@allourthings/cli`) for scripting
and automation outside of an AI session:

```bash
npx @allourthings/cli list
npx @allourthings/cli search "bosch"
npx @allourthings/cli add --name "Dyson V15" --category "Appliances"
```

Set `ALLOURTHINGS_DATA_DIR` or pass `--data-dir` to point at your vault.

## Notes

- Data is stored as plain JSON files — fully portable, no lock-in
- Works with any sync provider that exposes a local folder path (iCloud Drive, Dropbox, OneDrive, etc.)
- The MCP server and CLI share the same vault format — interchangeable
