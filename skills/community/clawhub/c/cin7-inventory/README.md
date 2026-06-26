# Cin7 Inventory Skill

An OpenClaw skill for managing Cin7 Core inventory, orders, stock, purchases, customers, and suppliers via bash scripts.

**ClawHub:** [clawhub.ai/Yashthesiya1/cin7-inventory](https://clawhub.ai/Yashthesiya1/cin7-inventory)

## Install

```bash
npx clawhub install cin7-inventory
```

## Setup

Set these environment variables:

```
CIN7_ACCOUNT_ID=your_account_id
CIN7_APP_KEY=your_application_key
```

Or create a `.env` file in the skill directory.

## Scripts

| Script | Description |
|---|---|
| `get-products.sh` | List/search products |
| `get-product.sh` | Get single product by ID |
| `get-stock.sh` | Check stock levels |
| `stock-adjustment.sh` | Adjust stock (damage, recount, write-off) |
| `stock-transfer.sh` | Transfer stock between locations |
| `list-orders.sh` | List sales orders |
| `get-order.sh` | Get single order by ID |
| `create-order.sh` | Create a sales order |
| `update-order.sh` | Update a sales order |
| `sales-report.sh` | Sales summary by date range |
| `get-purchases.sh` | List purchase orders |
| `create-purchase.sh` | Create a purchase order |
| `get-customers.sh` | List/search customers |
| `get-suppliers.sh` | List/search suppliers |

## Requirements

- `bash`
- `curl`
- Cin7 Core account with API access

## API Reference

- Base URL: `https://inventory.dearsystems.com/ExternalApi/v2`
- Auth: `api-auth-accountid` + `api-auth-applicationkey` headers
- [Cin7 Core API Docs](https://help.core.cin7.com/)
