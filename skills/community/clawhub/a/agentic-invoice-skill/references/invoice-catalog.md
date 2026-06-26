# Near-Exhaustive Agentic Development Invoice Catalog

Each template is a drafting pattern. Replace placeholders with verified facts before sending.

## Common Placeholders

- `{provider_name}`
- `{provider_address}`
- `{provider_email}`
- `{client_name}`
- `{client_address}`
- `{billing_contact}`
- `{invoice_number}`
- `{issue_date}`
- `{due_date}`
- `{payment_terms}`
- `{currency}`
- `{contract_id}`
- `{sow_id}`
- `{project_name}`
- `{billing_period}`
- `{workflow}`
- `{line_items}`
- `{subtotal}`
- `{tax}`
- `{discount}`
- `{credit}`
- `{amount_paid}`
- `{amount_due}`
- `{payment_instructions}`
- `{notes}`

## Templates

### pro-forma-invoice
Use when: the buyer needs a payable-looking estimate for procurement before final signature.

Invoice Type: Pro Forma Invoice
Invoice Number: {invoice_number}
Issue Date: {issue_date}
Valid Until / Due Date: {due_date}
Provider: {provider_name}
Client: {client_name}
Project: {project_name}
Reference: {contract_id}

Description:
Pro forma invoice for planned agentic development services related to {workflow}. This document summarizes expected charges for approval and purchasing workflow and should be reconciled against the final agreement before payment if terms change.

Line Items:
{line_items}

Subtotal: {subtotal}
Tax: {tax}
Discount: {discount}
Total Estimated Amount: {amount_due}

Notes:
{notes}

### deposit-request-invoice
Use when: scope is approved and a deposit is needed to reserve kickoff.

Invoice Type: Deposit Request
Invoice Number: {invoice_number}
Issue Date: {issue_date}
Due Date: {due_date}
Payment Terms: {payment_terms}

Bill To:
{client_name}
{client_address}

Project:
{project_name} - {workflow}

Line Items:
{line_items}

Amount Due Now: {amount_due}

Payment Instructions:
{payment_instructions}

Notes:
Deposit applies to the approved agentic development scope and will be credited against total project fees unless otherwise stated in the governing agreement.

### pilot-deposit-invoice
Use when: billing the initial deposit for a fixed-scope agentic workflow pilot.

Invoice Type: Agentic Workflow Pilot Deposit
Invoice Number: {invoice_number}
Issue Date: {issue_date}
Due Date: {due_date}
Contract / SOW: {contract_id}

Line Items:
- Agentic workflow pilot deposit for {workflow}: {amount_due}

Total Due: {amount_due}

Notes:
Pilot scope includes workflow design, bounded prototype implementation, evaluation examples, approval-gate setup, logging recommendations, and handoff documentation as defined in the agreement.

### contract-deposit-invoice
Use when: an agreement has been signed and the contract-defined deposit is due.

Invoice Type: Contract Deposit
Invoice Number: {invoice_number}
Issue Date: {issue_date}
Due Date: {due_date}
Agreement Reference: {contract_id}

Line Items:
{line_items}

Subtotal: {subtotal}
Amount Due: {amount_due}

Notes:
This invoice corresponds to the deposit due at signing for {project_name}. Work begins after signature, required access, and payment conditions are satisfied.

### discovery-assessment-invoice
Use when: billing a standalone discovery, workflow map, or readiness assessment.

Invoice Type: Discovery and Workflow Assessment
Invoice Number: {invoice_number}
Billing Period: {billing_period}
Project: {project_name}

Line Items:
- Discovery workshop for {workflow}
- Current-state workflow map
- Automation and approval-gate recommendations
- Pilot scope, risks, and effort estimate

Subtotal: {subtotal}
Tax: {tax}
Amount Due: {amount_due}

### milestone-invoice
Use when: billing a defined milestone after completion or acceptance.

Invoice Type: Milestone Invoice
Invoice Number: {invoice_number}
Milestone: {milestone_name}
Agreement / SOW: {sow_id}
Issue Date: {issue_date}
Due Date: {due_date}

Line Items:
{line_items}

Subtotal: {subtotal}
Prior Payments / Credits: {credit}
Amount Due: {amount_due}

Notes:
This invoice is tied to milestone completion or acceptance according to the governing agreement.

### prototype-delivery-invoice
Use when: billing delivery of the first working prototype.

Invoice Type: Prototype Delivery Invoice
Invoice Number: {invoice_number}
Project: {project_name}
Workflow: {workflow}

Line Items:
- Prototype implementation for {workflow}
- Intake, routing, retrieval, draft output, and human approval path
- Initial run logs and review notes

Amount Due: {amount_due}

Notes:
Prototype is intended for review and evaluation under the agreed pilot scope.

### evaluation-work-invoice
Use when: billing evaluation cases, testing, red-team checks, and acceptance examples.

Invoice Type: Evaluation Work Invoice
Invoice Number: {invoice_number}
Project: {project_name}

Line Items:
- Evaluation set creation for {workflow}
- Prompt-injection and tool-permission checks
- Regression examples and acceptance review support

Subtotal: {subtotal}
Tax: {tax}
Amount Due: {amount_due}

### handoff-invoice
Use when: billing documentation, administrator handoff, or final walkthrough deliverables.

Invoice Type: Documentation and Handoff Invoice
Invoice Number: {invoice_number}
Project: {project_name}

Line Items:
- Handoff documentation
- Administrator walkthrough
- Configuration notes
- Known limitations and monitoring recommendations

Amount Due: {amount_due}

### final-balance-invoice
Use when: billing remaining project balance after deposits, credits, and prior payments.

Invoice Type: Final Balance Invoice
Invoice Number: {invoice_number}
Agreement Reference: {contract_id}
Project: {project_name}

Contract Total: {contract_total}
Previously Invoiced / Paid: {amount_paid}
Credits: {credit}
Final Balance Due: {amount_due}

Line Items:
{line_items}

Notes:
This invoice represents the remaining balance for the completed scope unless open defects or holdbacks are documented separately.

### time-and-materials-invoice
Use when: billing hourly work, advisory time, or development time at agreed rates.

Invoice Type: Time and Materials Invoice
Invoice Number: {invoice_number}
Billing Period: {billing_period}

Line Items:
{line_items}

Subtotal: {subtotal}
Expenses: {expenses}
Tax: {tax}
Amount Due: {amount_due}

Notes:
Line items should include date or period, role, work description, hours, rate, and extended amount.

### monthly-retainer-invoice
Use when: billing a monthly support, monitoring, maintenance, or improvement retainer.

Invoice Type: Monthly Retainer Invoice
Invoice Number: {invoice_number}
Billing Period: {billing_period}
Project: {project_name}

Line Items:
- Monthly support retainer for {workflow}
- Included support scope: {included_scope}
- Included hours or capacity: {included_hours}

Amount Due: {amount_due}

### recurring-support-invoice
Use when: billing recurring agentic operations support on a subscription-like cadence.

Invoice Type: Recurring Support Invoice
Invoice Number: {invoice_number}
Service Period: {billing_period}

Line Items:
- Agentic workflow monitoring and support
- Issue triage and minor configuration adjustments
- Monthly review notes

Amount Due: {amount_due}

### change-order-invoice
Use when: billing approved scope added after original agreement.

Invoice Type: Change Order Invoice
Invoice Number: {invoice_number}
Change Order Reference: {change_order_id}
Project: {project_name}

Line Items:
{line_items}

Amount Due: {amount_due}

Notes:
This invoice covers approved work outside the original scope.

### rush-fee-invoice
Use when: an approved rush timeline or expedited work premium applies.

Invoice Type: Rush Fee Invoice
Invoice Number: {invoice_number}
Approval Reference: {approval_reference}

Line Items:
- Rush scheduling premium for {workflow}: {amount_due}

Notes:
Rush fees should be billed only when approved in writing or covered by the agreement.

### integration-add-on-invoice
Use when: billing added integration with a tool, API, data source, CRM, ticketing system, or document repository.

Invoice Type: Integration Add-On Invoice
Invoice Number: {invoice_number}
Integration: {system}

Line Items:
- Integration design for {system}
- Connector or API configuration
- Testing and documentation

Amount Due: {amount_due}

### usage-pass-through-invoice
Use when: billing approved third-party API, model, hosting, storage, or software charges.

Invoice Type: Usage Pass-Through Invoice
Invoice Number: {invoice_number}
Billing Period: {billing_period}

Line Items:
{line_items}

Subtotal Pass-Through Charges: {subtotal}
Markup, if agreed: {markup}
Tax: {tax}
Amount Due: {amount_due}

Notes:
Attach usage export, vendor invoice, or billing report when available.

### expense-reimbursement-invoice
Use when: billing reimbursable travel, shipping, printing, procurement, or other approved expenses.

Invoice Type: Expense Reimbursement Invoice
Invoice Number: {invoice_number}
Expense Period: {billing_period}

Line Items:
{line_items}

Total Expenses: {amount_due}

Notes:
Attach receipts or approval references where available.

### support-overage-invoice
Use when: support hours exceed included retainer, warranty, or support period allowances.

Invoice Type: Support Overage Invoice
Invoice Number: {invoice_number}
Billing Period: {billing_period}

Included Support: {included_hours}
Overage Work:
{line_items}

Amount Due: {amount_due}

### late-fee-invoice
Use when: billing a late fee allowed by agreement and calculated from supplied terms.

Invoice Type: Late Fee Invoice
Invoice Number: {invoice_number}
Original Invoice: {original_invoice_number}
Original Due Date: {original_due_date}

Late Fee Calculation:
{line_items}

Amount Due: {amount_due}

Notes:
Apply late fees only if allowed by the governing agreement and applicable law.

### installment-invoice
Use when: billing one payment in an approved payment plan.

Invoice Type: Installment Invoice
Invoice Number: {invoice_number}
Installment: {installment_number} of {installment_count}

Total Plan Amount: {contract_total}
Prior Payments: {amount_paid}
This Installment Due: {amount_due}
Remaining After Payment: {remaining_balance}

### partial-payment-receipt-invoice
Use when: acknowledging partial payment while showing remaining balance.

Invoice Type: Partial Payment Receipt / Balance Invoice
Invoice Number: {invoice_number}
Original Invoice: {original_invoice_number}

Original Amount: {contract_total}
Amount Paid: {amount_paid}
Remaining Balance Due: {amount_due}

### prepayment-credit-invoice
Use when: client prepays and the balance should be tracked as credit.

Invoice Type: Prepayment Credit Invoice
Invoice Number: {invoice_number}

Prepayment Received: {amount_paid}
Applied To: {project_name}
Available Credit Balance: {credit}

Notes:
Credit should be applied to future invoices according to the accepted terms.

### discount-adjustment-invoice
Use when: applying a discount, courtesy reduction, or negotiated adjustment.

Invoice Type: Discount Adjustment Invoice
Invoice Number: {invoice_number}
Related Invoice: {original_invoice_number}

Original Amount: {contract_total}
Discount / Adjustment: {discount}
Adjusted Amount Due: {amount_due}

Reason:
{notes}

### corrected-invoice
Use when: replacing or correcting a prior invoice.

Invoice Type: Corrected Invoice
Invoice Number: {invoice_number}
Corrects Invoice: {original_invoice_number}

Correction Summary:
{notes}

Corrected Line Items:
{line_items}

Corrected Amount Due: {amount_due}

### termination-invoice
Use when: project ends early and earned work or approved expenses remain payable.

Invoice Type: Termination Invoice
Invoice Number: {invoice_number}
Project: {project_name}
Termination Date: {termination_date}

Earned Work:
{line_items}

Approved Expenses: {expenses}
Credits / Deposits Applied: {credit}
Amount Due: {amount_due}

### refund-memo
Use when: documenting an amount to be refunded to the client.

Document Type: Refund Memo
Memo Number: {invoice_number}
Related Invoice: {original_invoice_number}

Refund Amount: {amount_due}
Reason:
{notes}

Refund Method / Timing:
{payment_instructions}

### credit-memo
Use when: documenting credit to apply to future work.

Document Type: Credit Memo
Credit Memo Number: {invoice_number}
Related Invoice: {original_invoice_number}

Credit Amount: {credit}
Reason:
{notes}

Apply To:
Future approved agentic development services unless otherwise agreed.

### retainer-renewal-invoice
Use when: renewing support, monitoring, or advisory retainer after the initial term.

Invoice Type: Retainer Renewal Invoice
Invoice Number: {invoice_number}
Renewal Period: {billing_period}

Line Items:
- Retainer renewal for {workflow}
- Support, monitoring, and minor improvement backlog review

Amount Due: {amount_due}

### expansion-workflow-invoice
Use when: adding a second workflow after a successful pilot or handoff.

Invoice Type: Expansion Workflow Invoice
Invoice Number: {invoice_number}
New Workflow: {next_workflow}

Line Items:
- Discovery and scope for {next_workflow}
- Prototype implementation
- Evaluation and handoff

Amount Due: {amount_due}

### training-invoice
Use when: billing enablement, admin training, reviewer training, or user workshops.

Invoice Type: Training Invoice
Invoice Number: {invoice_number}
Training Date / Period: {billing_period}

Line Items:
- Training session for {workflow}
- Reviewer workflow walkthrough
- Administrator enablement materials

Amount Due: {amount_due}

### advisory-invoice
Use when: billing advisory review without implementation.

Invoice Type: Advisory Services Invoice
Invoice Number: {invoice_number}
Billing Period: {billing_period}

Line Items:
- Agentic workflow advisory review
- Architecture and risk-control recommendations
- Evaluation and implementation plan review

Amount Due: {amount_due}

### holdback-release-invoice
Use when: billing retained amount after acceptance conditions are met.

Invoice Type: Holdback Release Invoice
Invoice Number: {invoice_number}
Agreement Reference: {contract_id}

Holdback Amount: {amount_due}
Acceptance / Release Condition:
{notes}

Amount Due: {amount_due}

### tax-only-invoice
Use when: tax was omitted or must be separately invoiced based on verified accounting instructions.

Invoice Type: Tax Adjustment Invoice
Invoice Number: {invoice_number}
Related Invoice: {original_invoice_number}

Tax Basis: {subtotal}
Tax Amount: {tax}
Amount Due: {amount_due}

Notes:
Use only with verified tax treatment supplied by the user or accounting system.

### voided-invoice-notice
Use when: documenting that a previously issued invoice should not be paid.

Document Type: Voided Invoice Notice
Notice Number: {invoice_number}
Voided Invoice: {original_invoice_number}

Reason:
{notes}

Replacement Invoice, if any: {replacement_invoice_number}

### paid-in-full-receipt
Use when: confirming that an invoice or project balance has been paid in full.

Document Type: Paid-in-Full Receipt
Receipt Number: {invoice_number}
Related Invoice / Project: {project_name}

Amount Paid: {amount_paid}
Payment Date: {payment_date}
Remaining Balance: 0

Notes:
Thank you. This receipt confirms payment for the referenced agentic development invoice.
