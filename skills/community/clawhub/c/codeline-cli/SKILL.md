---
name: codeline
description: "Manage codeline via CLI - tools, products, orders, users, coupons. Use when user mentions 'codeline', 'products', 'orders', 'coupons', 'school platform', or wants to interact with the Codeline API."
category: e-commerce
---

# codeline-cli

## Setup

If `codeline-cli` is not installed, install it from GitHub:
```bash
npx api2cli install Melvynx/codeline-cli
```

If `codeline-cli` is not found, install and build it:
```bash
bun --version || curl -fsSL https://bun.sh/install | bash
npx api2cli bundle codeline
npx api2cli link codeline
```

`api2cli link` adds `~/.local/bin` to PATH automatically. The CLI is available in the next command.

Always use `--json` flag when calling commands programmatically.

## Authentication

```bash
codeline-cli auth set "your-token"
codeline-cli auth test
```

## Resources

### tools

| Command | Description |
|---------|-------------|
| `codeline-cli tools list --json` | List all available tools |
| `codeline-cli tools run --tool list_products --json` | Run tool by name |
| `codeline-cli tools run --tool get_user --params '{"email":"test@example.com"}' --json` | Run tool with JSON parameters |
| `codeline-cli tools run --tool list_orders --params '{"limit":10}' --fields id,status --json` | Run tool with custom field output |

### products

| Command | Description |
|---------|-------------|
| `codeline-cli products list --json` | List all products |
| `codeline-cli products list --fields id,name,price --json` | List with specific columns |
| `codeline-cli products get --id abc123 --json` | Get product by ID |

### orders

| Command | Description |
|---------|-------------|
| `codeline-cli orders list --json` | List all orders |
| `codeline-cli orders list --limit 10 --json` | List orders with max results |
| `codeline-cli orders list --fields id,status,total --json` | List with custom columns |
| `codeline-cli orders get --id abc123 --json` | Get order by ID |

### users

| Command | Description |
|---------|-------------|
| `codeline-cli users list --json` | List all users |
| `codeline-cli users list --fields id,email,name --json` | List users with columns |
| `codeline-cli users get --id abc123 --json` | Get user by ID |
| `codeline-cli users get --id "test@example.com" --json` | Get user by email address |

### coupons

| Command | Description |
|---------|-------------|
| `codeline-cli coupons list --json` | List all coupons |
| `codeline-cli coupons list --fields code,discount,type --json` | List with specific columns |
| `codeline-cli coupons create --code SAVE20 --discount 20 --json` | Create percentage discount (20%) |
| `codeline-cli coupons create --code FLAT10 --discount 10 --type fixed --json` | Create fixed amount coupon |
| `codeline-cli coupons create --code LAUNCH --discount 50 --max-uses 100 --json` | Create with usage limit |
| `codeline-cli coupons create --code SPECIAL --discount 15 --expires-at "2026-12-31" --json` | Create with expiration |
| `codeline-cli coupons create --code PRODUCT5 --discount 5 --product-id xyz789 --json` | Create for specific product |

## Global Flags

All commands support: `--json`, `--format <text|json|csv|yaml>`, `--verbose`, `--no-color`, `--no-header`
