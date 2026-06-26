---
name: agentic-invoice-skill
description: >-
  Generate branded invoice and billing-document PDFs for agentic development services, including deposits, milestones, retainers, change orders, pass-through expenses, credits, receipts, refunds, and closeout billing. Use when the user wants structured billing documents from verified contract, SOW, milestone, and payment facts.
version: 1.0.10
metadata:
  openclaw:
    skillKey: agentic-invoice-skill
    homepage: https://github.com/CompleteTech-LLC/agentic-invoice-skill
    requires:
      bins:
        - python3
    install:
      - kind: uv
        package: reportlab==4.5.1
      - kind: uv
        package: pyyaml==6.0.3
      - kind: uv
        package: pypdfium2==5.8.0
      - kind: uv
        package: pillow==12.2.0
---

# Agentic Invoice Skill

## At a Glance

| What it creates | Best for | Output |
|---|---|---|
| Invoices and billing documents | Deposits, milestones, retainers, support, change orders, credits, receipts, refunds, and closeout | Branded PDF, Markdown, optional PNG preview |

This skill turns verified billing events, line items, contract references, credits, payment terms, and approval facts into clean CompleteTech-style invoice artifacts. It is local-only: it creates documents and does not issue invoices, collect payment, or call accounting systems.

## Included Billing Documents

| Category | Documents |
|---|---|
| Engagement start | Pro forma, deposit, pilot, discovery, and contract-deposit invoices. |
| Delivery milestones | Milestone, prototype, evaluation-work, handoff, final-balance, and time-and-materials invoices. |
| Ongoing services | Retainer, recurring support, overage, expansion, training, advisory, and pass-through invoices. |
| Adjustments | Credit memos, refund memos, corrected invoices, void notices, installment requests, and paid-in-full receipts. |

## Purpose

| Use | Scope |
|---|---|
| Billing artifact generation | Create practical invoice documents for agentic development services from verified billing facts. |
| Lifecycle coverage | Upfront deposits, scoped pilots, discovery, implementation, evaluation, change orders, retainers, support, expenses, credits, late fees, refunds, and closeout. |
| Operating boundary | Produce invoice documents only; payment collection, tax decisions, ledger posting, and collections stay with the accounting system or reviewer. |

## System Boundary

| Boundary | Use |
|---|---|
| This skill | Billing document drafting and invoice-event selection. |
| `agentic-proposal-skill` | Pricing rationale or commercial scope before approval. |
| `agentic-contract-skill` | Agreement terms and payment obligations. |
| `agentic-delivery-skill` | Milestone evidence, delivery records, and acceptance context. |
| `agentic-email-skill` | The message that accompanies an invoice. |
| Accounting system or reviewer | Final tax, payment, ledger, and collection decisions. |

## Core Workflow

| Step | Action |
|---|---|
| 1 | Identify the invoice event: estimate, deposit, milestone, retainer, time and materials, change order, expense, final invoice, credit, late fee, refund, or renewal. |
| 2 | Gather the required billing facts. |
| 3 | Use `references/invoice-positioning.md` for service language and risk boundaries. |
| 4 | Use `references/use-case-decision-table.md` to choose the right invoice type. |
| 5 | Use `references/invoice-lifecycle.md` for end-to-end billing flow and gates. |
| 6 | Use `references/invoice-catalog.md` for the near-exhaustive invoice template library. |
| 7 | Draft clearly and conservatively; do not invent tax, banking, contract, or accounting facts. |

| Required Fact | Examples |
|---|---|
| Parties | Provider, client, billing contact, and legal entity names. |
| Invoice details | Invoice number, issue date, due date, terms, currency, project name, billing period, and notes. |
| Commercial reference | Contract, SOW, purchase order, milestone, or delivery evidence. |
| Amounts | Line items, taxes, discounts, credits, previous payments, and amount due. |
| Payment handling | Payment instructions, accounting review status, and collection constraints. |

## Invoice Selection Guide

Choose by the actual commercial trigger first.

| Trigger Group | Use These Templates |
|---|---|
| Pre-approval and deposits | `pro-forma-invoice`, `deposit-request-invoice`, `pilot-deposit-invoice`, `discovery-assessment-invoice`, `contract-deposit-invoice` |
| Delivery and closeout | `milestone-invoice`, `prototype-delivery-invoice`, `evaluation-work-invoice`, `handoff-invoice`, `final-balance-invoice`, `holdback-release-invoice` |
| Ongoing work | `time-and-materials-invoice`, `monthly-retainer-invoice`, `recurring-support-invoice`, `retainer-renewal-invoice` |
| Scope changes | `change-order-invoice`, `rush-fee-invoice`, `integration-add-on-invoice`, `expansion-workflow-invoice`, `training-invoice`, `advisory-invoice` |
| Pass-through and expenses | `usage-pass-through-invoice`, `expense-reimbursement-invoice`, `support-overage-invoice` |
| Collections and payment status | `late-fee-invoice`, `installment-invoice`, `partial-payment-receipt-invoice`, `paid-in-full-receipt` |
| Adjustments | `prepayment-credit-invoice`, `discount-adjustment-invoice`, `corrected-invoice`, `termination-invoice`, `refund-memo`, `credit-memo`, `tax-only-invoice`, `voided-invoice-notice` |

| Selection Rule | Guidance |
|---|---|
| Several templates fit | Choose the invoice closest to the actual billing trigger. |
| Delivery happened before acceptance | If the contract bills on milestone acceptance, use `milestone-invoice`, not `prototype-delivery-invoice`. |
| Facts are incomplete | Keep missing values as `TBD` and do not invent payment, tax, PO, or banking details. |

## Quality Rules

| Rule | Requirement |
|---|---|
| Amounts and terms | Use exact client-provided amounts and terms. |
| Line items | Keep line items specific enough for approval but not cluttered. |
| References | Tie invoices to contract, SOW, change order, or accepted milestone references when available. |
| Separation | Separate professional services, third-party pass-throughs, expenses, taxes, credits, and late fees. |
| Unknowns | Mark drafts as drafts if payment details or tax handling are unknown. |
| Advice boundary | Do not include legal, tax, or accounting advice unless the user specifically asks for explanatory notes. |
| Fabrication guardrail | Never fabricate bank accounts, tax IDs, purchase order numbers, tax rates, or compliance status. |

## Resource Guide

| Resource | Role |
|---|---|
| `references/invoice-positioning.md` | Agentic development service wording, line-item language, and invoice boundaries. |
| `references/use-case-decision-table.md` | Invoice-type selection for a specific billing event. |
| `references/invoice-lifecycle.md` | End-to-end invoicing workflows, approval gates, and follow-up steps. |
| `references/invoice-catalog.md` | Near-exhaustive invoice template library. |
| `references/template-index.json` | Machine-readable template metadata used by the renderer. |
| `scripts/render_invoice.py` | Lists invoice templates or renders a draft with placeholders. |

## Runtime Permissions

| Area | Runtime behavior |
|---|---|
| Execution | Runs local Python entry points: `scripts/render_invoice.py` and `scripts/render_pdf.py`. |
| Reads | Bundled templates, references, examples, `assets/logo.png`, and user-provided Markdown or invoice variables. |
| Writes | Only user-selected `--out`, `--png`, `--markdown-out`, or default `output/` artifact paths. |
| Network | Not required and not used for invoice drafting or document rendering. |

| Not Included | Boundary |
|---|---|
| Payment operations | Does not collect payment, issue payment links, post to ledgers, or call accounting systems. |
| Credentials | Does not read banking credentials, accounting credentials, API keys, or CRM tokens. |
| System changes | Does not create persistence, escalate privileges, run background services, or perform destructive file operations. |

## Renderer

Use the local renderer for repeatable invoice drafts, template discovery, and branded artifacts:

```bash
python3 scripts/render_invoice.py --list
python3 scripts/render_invoice.py --stage milestone --list
python3 scripts/render_invoice.py --template pilot-deposit-invoice --var client_name=Acme --var invoice_number=INV-1001 --var amount_due=6000
```

| Need | Command Pattern |
|---|---|
| List all templates | `python3 scripts/render_invoice.py --list` |
| List a stage | `python3 scripts/render_invoice.py --stage milestone --list` |
| Render a template | `python3 scripts/render_invoice.py --template pilot-deposit-invoice --var key=value` |
| Production polish | Replace every placeholder with verified invoice, contract, tax, payment, and client facts. |

## Rendering to a Branded PDF

Artifacts from this skill are delivered as branded CompleteTech LLC **PDF** documents. The renderer can emit PDF, Markdown, and optional PNG preview in one local command:

```bash
pip install -r requirements.txt
python3 scripts/render_invoice.py --template milestone-invoice \
  --out artifact.pdf --png artifact.png \
  --title "Invoice INV-2026-0461" --doc-type "MILESTONE INVOICE" \
  --meta "INVOICE NO.=INV-2026-0461" --meta "DUE=2026-06-23" --no-cover \
  --var client_name="Client Name" --var workflow="support triage"
```

| Output Need | Use |
|---|---|
| Branded PDF | `--out artifact.pdf` |
| PNG preview | `--png artifact.png` |
| Markdown source | `--markdown-out artifact.md` |
| Markdown only | `--no-pdf` |
| Single-document invoice | `--no-cover` |
| Existing billing Markdown to PDF | `python3 scripts/render_pdf.py --markdown invoice.md --out invoice.pdf --logo assets/logo.png --title "Invoice INV-2026-0461" --doc-type "MILESTONE INVOICE"` |

| Rendering Support | Details |
|---|---|
| Markdown subset | `#`, `##`, `###`, paragraphs, `-` bullets, tables, `>` callouts, `**bold**`, and `[PAGE_BREAK]`. |
| Required package | `reportlab==4.5.1` for PDF rendering. |
| Optional preview packages | `pypdfium2==5.8.0` and `pillow==12.2.0` for `--png`. |
| Example output | See `assets/examples/` for rendered Markdown, PDF, and PNG artifacts. |

## Network Boundary

This skill is local-only. It does not include outbound network helpers, callbacks, or any helper that posts invoice run metadata to an external service.
