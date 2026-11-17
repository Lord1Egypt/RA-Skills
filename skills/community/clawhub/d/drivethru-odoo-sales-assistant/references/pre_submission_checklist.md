# Pre-submission checklist

> **This is the part we tune as we test.** The checks below are the v1 seed,
> derived from Odoo's real confirm gates. As BaconCo operators tell us what
> "ready to submit" really means, add/adjust checks **in two places**:
> this file (the human reference) and the MCP service's evaluator,
> `drivethru_mcp/services/sales_entry.py` → `_evaluate_checklist()` (what the
> tool actually computes). Keep them in sync.

## How to run it

```bash
python3 scripts/odoo_mcp.py call sales_run_preflight '{"order_id": 42}'
```

Read-only — it **mutates nothing**. It predicts every gate `action_confirm`
will enforce, plus advisory items. Each check has:

- `status` — `pass` | `fail` | `warn` | `na`
- `severity` — `blocking` (Odoo will refuse confirm) or `advisory`
- `detail` — plain-language explanation
- `source` — where the rule lives

The response rolls up: `ready_to_submit` (false while any blocking check is
`fail`), `blocking_failures`, `blocking_overridable` (blocking checks at `warn`,
which only a manager or `force_confirm` can pass), `advisory_flags`, and a
`summary`. **Run it right before every submit/confirm.**

## The checks (v1 seed)

| Check | Severity | What it verifies |
| --- | --- | --- |
| `customer_set` | blocking | The order has a customer. |
| `customer_notes_reviewed` | advisory | Surfaces the customer's internal notes — read them for special handling. |
| `customer_approved` | advisory | Customer account approval state is `approved`. |
| `ship_date` | blocking | `commitment_date` is set (waived for website / chipply-store customers). |
| `lines_have_products` | blocking | Every non-section line has a product. |
| `end_items_constructed` | advisory | No decorated line is still a raw blank — i.e. **Preview has been run**. |
| `no_unknown_deco_method` | blocking | No linked decoration has an `UNKNOWN` method. |
| `customization_lines` | blocking | Custom-text decorations have one customization line per unit. |
| `has_decorations` | advisory | Order has decorations (else Odoo asks to confirm a pass-through order). |
| `decorations_production_ready` | blocking (overridable) | All linked decorations have production files (DST/PNG); Embroidery exempt. |
| `proof_approvals` | advisory | Proofs approved when `require_proof_approvals` is on. |
| `no_mixed_dropship` | blocking | Lines are all dropship or all in-house. |
| `shipping_account` | blocking | Customer shipping account set when the carrier requires one. |
| `partner_requires_po` | blocking | Customer PO # entered when the customer requires it. |
| `partner_required_department` | blocking | Department set when the customer requires it. |
| `partner_shipping_label_notes` | blocking | Shipping label notes entered when the customer requires it. |
| `blank_costs_entered` | advisory | Every product line has a per-unit blank cost (else margin is wrong and quote-send is blocked). |

## How to read the result

1. **Any blocking `fail`?** Fix it before submitting — Odoo will refuse
   otherwise. The `detail` tells you exactly what's missing.
2. **Blocking `warn` (overridable)?** Usually `decorations_production_ready`.
   Either get the art production-ready (upload the DST/PNG) or, if the user
   accepts the risk, confirm with `force_confirm=true` (a manager-level
   override — production may be delayed).
3. **Advisory `fail`/`warn`?** Not blocking, but worth resolving: read the
   customer notes, enter blank costs, get proofs approved, run Preview.

## Where the real gates live (source of truth)

- `sales_module_addon/models/sale_order.py` → `action_confirm_preflight()` and
  `action_confirm()`.
- `res_partner_addon/models/sale_order.py` → the partner PO/department/label
  gates.
- Decoration readiness: `artwork_module_custom/models/decoration.py` →
  `decoration_production_ready`.

The checklist tool re-implements these read-only so you can see them *before*
clicking submit — but **Odoo re-checks every hard gate on the real confirm**, so
a green checklist predicts success, it doesn't bypass anything.

## Notes area for tuning (append as we test)

<!-- As operators refine the checklist, capture the agreed rules here with a
     date, then implement them in _evaluate_checklist(). e.g.:
     - 2026-07-14: Rush orders (event_date within 5 business days) must have a
       decoration request already in `approved` before submit. [status: proposed]
-->
