# Customer prep — read notes, honor flags, leave notes

**Do this before you enter an order.** `sales_get_customer {"partner_id": <id>}`
returns everything below in one call. Find the id first with
`sales_search_customers {"search": "Booster"}`.

## 1. Read the internal notes (the "special actions for this customer")

The only place free-text special instructions live is the standard Odoo
**Internal Notes** field, `res.partner.comment`. There is **no** `sale_warn`
pop-up mechanism on this Odoo — the notes are the whole story.

`sales_get_customer` returns two fields, and you should read **both**:

- `internal_notes` — notes on the ordering contact (`partner_id`).
- `commercial_internal_notes` — notes on the parent **company** (the
  commercial partner). Notes are often attached at the company level.

Treat anything in there as a directive: "always navy not royal", "PO # must be
on the packing slip", "call before shipping", "split ship to each school", etc.
If a note conflicts with what you're about to do, follow the note or ask.

## 2. Honor the hard flags (or confirm will hard-refuse)

These are enforced at confirm time on the **commercial** (company) partner.
`sales_get_customer` returns each; set the matching order field up front:

| Flag (on customer) | You must set on the order | Symptom if missing |
| --- | --- | --- |
| `requires_po` | `customer_po` | `UserError`: "Customer … requires a PO number." |
| `required_department` | `sale_order_department` | `UserError`: "… requires a department …" |
| `requires_shipping_label_notes` | `shipping_label_notes` | `UserError`: "… requires shipping label notes …" |

Also surfaced:

- `approval_state` — should be `approved`. If it's `draft`/`review`, the
  customer account isn't fully set up; flag it (advisory, not a hard block).
- `chipply_store_customer` — a webstore customer. Waives the ship-date gate, and
  a **duplicate `customer_po`** across non-cancelled orders is rejected at
  confirm. Don't reuse a PO number for these.
- `tax_exempt`, `buying_group`, `sports_inc_customer` — classification that
  affects tax and fees downstream.

## 3. Know what auto-populates

On `sales_create_order` these copy from the customer automatically — you don't
set them, but verify they look right: `team_id`, `salesperson_id`
(`user_id`), `payment_term_id`, `pricelist_id`, fiscal position, and the
invoice/delivery addresses. `parent_customer` is the commercial partner.

## 4. Leave timestamped notes

When you learn something worth remembering about this customer, record it:

```bash
python3 scripts/odoo_mcp.py call sales_add_customer_note \
  '{"partner_id": 4213, "note": "Always wants navy (PMS 289), never royal. PO # must print on packing slip."}'
```

This **appends a timestamped entry to the customer's Internal Notes**
(`res.partner.comment`) — the same field you read in step 1, so your learnings
land where a rep (and your future self) will see them. It:

- **appends**, never overwrites — existing notes are preserved;
- **stamps** each entry with the date/time and an author label;
- **HTML-escapes** the text so it can't corrupt the field.

`sales_get_customer` surfaces the accumulated notes back under `internal_notes`
(and `commercial_internal_notes`), so the next order benefits automatically.
Keep entries short and factual.

## Quick recipe

```bash
# 1. find the customer
python3 scripts/odoo_mcp.py call sales_search_customers '{"search":"Riverside Booster"}'
# 2. read notes + flags
python3 scripts/odoo_mcp.py call sales_get_customer '{"partner_id": 4213}'
# 3. create the order, pre-filling anything the flags require
python3 scripts/odoo_mcp.py call sales_create_order \
  '{"partner_id": 4213, "customer_po": "RB-2026-014", "commitment_date": "2026-08-01"}'
```
