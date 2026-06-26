# Agentic Development Invoice Lifecycle

## End-to-End Billing Flow

1. Estimate or pro forma
   - Use before contract signature, procurement approval, or vendor setup.
   - Do not request payment unless the user intends the document to be payable.

2. Deposit or kickoff invoice
   - Use after the client approves scope or signs the agreement.
   - Tie to contract ID, SOW, or pilot name.

3. Discovery or assessment invoice
   - Use for a standalone workflow assessment or first phase.
   - Include deliverables such as workflow map, risks, pilot recommendation, and effort estimate.

4. Milestone invoice
   - Use when the contract bills on completion or acceptance of specific milestones.
   - Include milestone name, acceptance criteria, and prior payments if relevant.

5. Change-order invoice
   - Use for added workflow, integration, deployment target, data source, rush work, or support outside scope.
   - Reference the change-order approval.

6. Recurring support or retainer invoice
   - Use for monthly monitoring, support, maintenance, admin help, or improvement backlog.
   - Include billing period and included hours or scope.

7. Pass-through or expense invoice
   - Use for authorized third-party usage, hosting, model/API charges, travel, or procurement.
   - Keep these separate from professional services where possible.

8. Final invoice
   - Use after delivery, acceptance, or closeout.
   - Include total contract value, deposits/credits, amount previously paid, and balance due.

9. Post-sale adjustments
   - Use credit memo, refund memo, corrected invoice, late-fee invoice, or installment invoice as the actual event requires.

## Approval Gates Before Issuing

Check:

- Is there a signed agreement, accepted quote, purchase order, or written approval?
- Is the invoice number unique?
- Are dates, terms, and currency present?
- Are client billing contact and provider payment instructions verified?
- Are tax rates supplied by the user or accounting system?
- Are expenses or pass-through charges authorized and documented?
- Are credits and previous payments deducted correctly?
- Does the invoice match the commercial trigger?

## Follow-Up Flow

1. Send invoice with concise context.
2. If unpaid near due date, send a reminder with invoice number and amount.
3. If overdue, send an overdue notice and ask whether billing details need correction.
4. If still unpaid, escalate according to the agreement and client relationship.
5. Apply late fees only if allowed by agreement and supplied by the user.

## Status Labels

Use labels consistently:

- Draft
- Sent
- Due
- Paid
- Partially paid
- Overdue
- Void
- Corrected
- Credited
- Refunded
