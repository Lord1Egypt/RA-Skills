---
name: cin7-inventory
description: "Cin7 Core inventory management -- products, stock, orders, purchases, customers, and suppliers via bash scripts."
version: "2.0.0"
homepage: "https://clawhub.ai/Yashthesiya1/cin7-inventory"
user-invocable: true
metadata:
  openclaw:
    requires:
      env: [CIN7_ACCOUNT_ID, CIN7_APP_KEY]
      bins: [curl, bash]
---

# Cin7 Inventory Management

Manage Cin7 Core inventory via bash scripts. All commands run from the skill directory.

## Required Environment Variables

- `CIN7_ACCOUNT_ID` — your Cin7 Core account ID
- `CIN7_APP_KEY` — your Cin7 Core application key

## Products

### List/search products
```bash
bash scripts/get-products.sh
bash scripts/get-products.sh --search "widget" --page 2
```

### Get single product
```bash
bash scripts/get-product.sh --id "product-id"
```

## Stock

### Check stock levels
```bash
bash scripts/get-stock.sh
bash scripts/get-stock.sh --product-id "product-id"
bash scripts/get-stock.sh --page 2
```

### Adjust stock (damage, recount, write-off)
```bash
bash scripts/stock-adjustment.sh --data '{"Lines":[{"ProductID":"id","Location":"Main Warehouse","Quantity":5}]}'
```

### Transfer stock between locations
```bash
bash scripts/stock-transfer.sh --data '{"Lines":[{"ProductID":"id","From":"Warehouse A","To":"Warehouse B","Quantity":10}]}'
```

## Sales Orders

### List orders
```bash
bash scripts/list-orders.sh
bash scripts/list-orders.sh --status "COMPLETED" --page 1
```

### Get single order
```bash
bash scripts/get-order.sh --id "order-id"
```

### Create order
```bash
bash scripts/create-order.sh --data '{"Customer":"John Smith","Lines":[{"ProductID":"id","Quantity":2}]}'
```

### Update order
```bash
bash scripts/update-order.sh --id "order-id" --data '{"Status":"COMPLETED"}'
```

### Sales report by date range
```bash
bash scripts/sales-report.sh --from "2026-01-01" --to "2026-03-07"
```

## Purchase Orders

### List purchase orders
```bash
bash scripts/get-purchases.sh
bash scripts/get-purchases.sh --status "ORDERED" --page 1
```

### Create purchase order
```bash
bash scripts/create-purchase.sh --data '{"Supplier":"Acme Corp","Lines":[{"ProductID":"id","Quantity":100}]}'
```

## Customers & Suppliers

### List/search customers
```bash
bash scripts/get-customers.sh
bash scripts/get-customers.sh --search "John"
```

### List/search suppliers
```bash
bash scripts/get-suppliers.sh
bash scripts/get-suppliers.sh --search "Acme"
```
