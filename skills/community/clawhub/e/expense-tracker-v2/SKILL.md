---
name: expense-tracker
description: Track expenses and income with multi-backend storage (local/Notion/Google Sheet/Supabase). Credentials are encrypted with AES-256-GCM. Use when user wants to record expenses, view transaction history, or check monthly spending statistics.
---

# Expense Tracker Skill

## Quick Start

### Initial Setup (First Time)

```bash
expense-tracker setup
```

This will:
1. Ask you to set a master password (for encrypting credentials)
2. Select storage backend and configure API keys

**Storage backends:**
1. **Local file** - No config needed
2. **Notion** - Requires API Key + Database ID
3. **Google Sheet** - Requires credentials path + Spreadsheet ID
4. **Supabase** - Requires URL + Anon Key

### Set Password (For Subsequent Uses)

```bash
expense-tracker pass <your-password>
```

Or enter interactively when prompted.

### Record Expense

```bash
expense-tracker add -50 "lunch" food
# Format: expense-tracker add <amount> <note> <category>
# Negative amount = expense
```

### Record Income

```bash
expense-tracker add 5000 "salary" salary
# Positive amount = income
```

### View Records

```bash
expense-tracker list              # Recent 10 records
expense-tracker list --month     # This month
expense-tracker list --category  # By category
```

### Statistics

```bash
expense-tracker stats             # This month
expense-tracker stats -m 2       # 2 months ago
```

## Security

Credentials are encrypted using **AES-256-GCM** with PBKDF2 key derivation.

- Config file: `~/.openclaw/expense-tracker/config.enc`
- Never stores plain text passwords or API keys

## Categories

- `food` - Food & Dining
- `transport` - Transportation
- `shopping` - Shopping
- `entertainment` - Entertainment
- `salary` - Salary
- `bonus` - Bonus
- `investment` - Investment
- `other` - Other

## Commands Reference

| Command | Description |
|---------|-------------|
| `setup` | Set password & configure backend (first time) |
| `pass <password>` | Set password for decryption |
| `add <amount> <note> <category>` | Add new record |
| `list` | View recent records |
| `list --month` | This month's records |
| `list --category` | Group by category |
| `stats` | Monthly summary |
| `stats -m <n>` | N months ago |

## Data Format

Each record:

```json
{
  "id": "uuid",
  "type": "expense|income",
  "amount": -50,
  "category": "food",
  "note": "lunch",
  "date": "2026-03-03",
  "created_at": "2026-03-03T20:23:00Z"
}
```
