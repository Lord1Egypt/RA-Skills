---
name: daftra-backup
description: Analyze Daftra CSV backups covering customers, suppliers, products, invoices (and line items), purchase orders, expenses, and projects. Use this skill to read, search, inventory, link records, or prepare data for migration to MCP or import files—while checking for duplicate numbers and unresolved relationships. This skill does not provide a live connection or the ability to modify the Daftra account.
---

# Daftra Backup Analysis

## Define Source and Scope

- Use user-provided files if specified; otherwise, use the reference backup located in `assets/source/`.
- Treat the backup as static historical data. Do not describe prices or balances as real-time, and do not consider it a complete snapshot of the entire Daftra account.
- Preserve the original assets; perform any cleaning or transformation in separate output files. Do not execute write operations on a live account based on these files.
- Respond in Arabic, but retain original column names and identifiers when explaining data matching.

## Pre-analysis Inspection

Run from the skill directory:

```bash
python3 scripts/inspect_backup.py
```

To inspect a new ZIP backup or CSV folder:

```bash
python3 scripts/inspect_backup.py /absolute/path/to/backup.zip
```

Consult `references/schema.md` to select tables and columns. Use `references/inventory.json` for counts and fingerprints of the provided backup, not to validate data from a new backup. The script performs read-only operations and outputs JSON; it does not establish connections or modify data. Import `read_table` from the script to read files consistently during analysis. ## Contents of the Attached Version

| File | Number of Records | Purpose |
|---|---:|---|
| Clients.csv | 64 | Client data, contract fields, and unit details |
| Client_contacts.csv | 72 | Client contacts |
| Suppliers.csv | 29 | Supplier data |
| Supplier_contacts.csv | 29 | Supplier contacts |
| Products.csv | 3256 | Products, services, prices, and inventory fields |
| Invoices.csv | 122 | Invoice headers and totals |
| Invoice_items.csv | 705 | Invoice line items and taxes |
| Purchase_orders.csv | 62 | Purchase order headers |
| Purchase_order_items.csv | 279 | Purchase order line items |
| Expenses.csv | 2241 | Expenses |
| Projects.csv | 23 | List of projects |

Total: 4,862 records across 11 tables; do not aggregate these as a count of unique transactions or individuals.

## Reading the CSV Without Corrupting Identifiers

- The attached files contain a BOM at the start of the first data record following the headers. Remove it from memory before parsing the CSV; using `utf-8-sig` alone does not remove the internal BOM and may corrupt the first quoted field.
- Use a CSV reader that supports quoted text and newlines within fields, rather than simple comma or line-based splitting.
- Treat codes, phone numbers, and barcodes as text strings—preserving leading zeros (e.g., `000011`) and alphanumeric codes (e.g., `AZ-CRM-0005`). - Treat text consisting solely of whitespace as empty in the staging copy. Do not automatically convert empty numeric values ​​to zero.
- Use `Decimal` for financial calculations and log non-convertible values ​​instead of silently discarding them.
- Retain the file reference and CSV record number for each result. The record number is not necessarily the actual line number.

## Link tables using established relationships

| From | To | Staging Result |
|---|---|---|
| Invoice_items.no | Invoices.InvoiceNo | 705 items have a matching number; 4 items have an unresolved parent due to duplicate invoice numbers |
| Invoices.ClientNo | Clients.ClientNumber | 122 of 122 matched |
| Client_contacts.ClientNumber | Clients.ClientNumber | 72 of 72 matched |
| Purchase_order_items.no | Purchase_orders.PurchaseOrderNo | 279 of 279 matched |
| Supplier_contacts.supplier_number | Suppliers.SupplierNumber | 29 of 29 matched |
| Purchase_orders.SupplierNo | Suppliers.SupplierNumber | 0 of 62 matched textually; relationship not supported |

- Verify parent key uniqueness before linking, and check row counts and totals both before and after linking.
- Invoice number `AZ-INV-2024-00177` appears in two headers. Do not automatically delete one, nor link the four items to both (which would double the quantities). Present both headers for review and use the `ID` to track each header after verifying its uniqueness; do not replace it with the item key `no` without justification.
- Do not handle supplier number discrepancies by stripping leading zeros or matching based on row number. - Use `SupplierBusinessName` for display purposes, sourced directly from the purchase order header. While a name match with `BusinessName`—accompanied by a confidence score and supporting evidence—may be suggested, do not treat it as a confirmed relationship without verification.
- There is no explicit product identifier in the line-item tables; the `item` field is a text description, not a guaranteed key linking to `Products.id` or `ProductCode`.
- There is no explicit project relationship in invoice, purchase order, or expense headers. Do not attribute these records to projects based solely on `StaffID` or names by default.
- `Expenses.Vendor` is not a validated vendor key; treat it as a text field unless proven otherwise.

## Task Execution by Domain

### Invoices and Sales

- Rely on invoice headers for totals and line items for details; do not conflate the two into a single aggregate figure.
- Display `SummaryTotal`, `SummaryPaid`, `SummaryUnpaid`, and `SummaryDeposit` as independent source fields. Validate their relationships and document any discrepancies; do not assume that deposits are automatically added to or deducted from paid amounts.
- Aggregate data by currency. While all `CurrencyCode` values ​​in the financial tables for this instance are EGP, verify this for each new instance.
- Review `subtotal_without_tax`, `tax1_amount`, `tax2_amount`, and `subtotal` alongside header-level discounts. Do not assume that every discrepancy indicates an error or that every tax value represents a percentage.
- Do not infer the meaning of `PaymentStatus` codes or assume that every invoice represents realized revenue without clear documentation and status definitions.

### Purchase Orders and Suppliers

- Present these amounts as "Purchase Orders," not as expenses or automatically realized payments. - Separate purchase orders from expenses; do not combine them