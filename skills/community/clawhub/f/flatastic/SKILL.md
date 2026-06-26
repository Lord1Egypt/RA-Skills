---
name: flatastic
description: Manage shared household chores, shopping lists, and expenses via Flatastic. Use when user asks about chores, WG tasks, shopping list, expenses, or Flatastic.
metadata:
  clawdbot:
    emoji: "🏠"
    requires:
      bins: ["flatastic"]
---

# Flatastic CLI

CLI for managing shared household in Flatastic (WG-App).

## Installation

```bash
cd ~/Projects/flatastic-cli
npm install
npm run build
npm link
```

After linking, `flatastic` is available globally.

## Setup

```bash
flatastic auth             # Login with email/password
flatastic refresh          # Refresh WG data from server
```

Token + user/WG info saved to `~/.config/flatastic/config.json`

## Commands

### Chores

```bash
flatastic chores           # List all chores with assignee, points, due dates
flatastic done <search>    # Mark chore as done (partial name match)
flatastic remind <search>  # Send reminder notification for a chore
flatastic stats            # Show chore statistics & leaderboard
flatastic history          # Show chore completion history
flatastic history -l 50    # Show last 50 entries
```

### Shopping List

```bash
flatastic shop             # Show pending items (shortcut)
flatastic shop -a          # Show all items (including bought)

flatastic shopping list    # Show pending items
flatastic shopping add "Milch"  # Add item to list
flatastic shopping done milch   # Mark item as bought
flatastic shopping delete milch # Remove item from list
flatastic shopping clear        # Clear all bought items
```

### Expenses / Finances

```bash
flatastic expenses         # Show recent expenses
flatastic expenses -l 20   # Show last 20 expenses
flatastic balances         # Show who owes whom
flatastic expense "Pizza" 24.50           # Add expense, split with all
flatastic expense "Taxi" 15 -s "David"    # Split only with David
```

### WG Info

```bash
flatastic wg               # Show WG info and flatmates with points
```

### Shouts (Messages/Bulletin Board)

```bash
flatastic shouts           # Show recent shouts
flatastic shout "Pizza ist da!"  # Post a new shout
```

## Usage Examples

**"Was steht heute an?"**
```bash
flatastic chores
```

**"Hake Staubsaugen ab"**
```bash
flatastic done staubsaugen
```

**"Erinner mal wegen Müll"**
```bash
flatastic remind müll
```

**"Wer hat die meisten Punkte?"**
```bash
flatastic stats
```

**"Was muss ich noch einkaufen?"**
```bash
flatastic shop
```

**"Setz Milch auf die Liste"**
```bash
flatastic shopping add "Milch"
```

**"Hab ich gekauft"**
```bash
flatastic shopping done milch
```

**"Wer schuldet wem Geld?"**
```bash
flatastic balances
```

**"Ich hab 24€ für Pizza bezahlt"**
```bash
flatastic expense "Pizza" 24
```

## API Endpoints Discovered

### Chores
- `GET /chores` — List all chores
- `GET /chores/next?id=&userId=&completedBy=` — Mark as done
- `GET /chores/remind?id=` — Send reminder
- `GET /chores/statistics` — Get point statistics
- `GET /chores/history` — Completion history
- `POST /chores` — Create new chore
- `POST /chores/update` — Update chore
- `DELETE /chores/id/:id` — Delete chore

### Shopping
- `GET /shoppinglist` — List all items
- `POST /shoppinglist` — Add item `{name: "..."}`
- `GET /shoppinglist/toggle_item?id=` — Toggle bought
- `DELETE /shoppinglist/item/:id` — Delete item
- `POST /shoppinglist/delete_bought_items` — Clear bought

### Expenses (Cashflow)
- `GET /cashflow?offset=&limit=` — List expenses
- `GET /cashflow/settlement` — Who owes whom
- `GET /cashflow/statistics` — Expense stats
- `POST /cashflow` — Add expense
- `DELETE /cashflow/id/:id` — Delete expense

### Shouts
- `GET /shouts` — List shouts
- `POST /shouts` — Post shout `{shout: "..."}`
- `DELETE /shouts/id/:id` — Delete shout

### WG
- `GET /wg` — WG info with flatmates

## Config File

`~/.config/flatastic/config.json`:
```json
{
  "token": "...",
  "user": { "id": "...", "firstName": "...", "chorePoints": "..." },
  "wg": {
    "name": "...",
    "flatmates": [{ "id": "...", "firstName": "..." }, ...]
  }
}
```

## Notes

- All commands support partial name matching (case-insensitive)
- Amounts in expenses are in Euros (e.g., "24.50" or "24,50")
- Reminders trigger push notifications to the assigned person
