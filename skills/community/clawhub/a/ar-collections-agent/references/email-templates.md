# AR Collections Email Templates

Five-tier escalation ladder. Replace `{{}}` placeholders before sending. Requires approval before sending.

---

## Tier 1: Friendly Reminder (1–30 Days Past Due)

**Subject:** Friendly Reminder — Invoice {{INVOICE_ID}} Due {{DUE_DATE}}

Hi {{CUSTOMER_NAME}},

I hope you're doing well! This is a friendly reminder that invoice {{INVOICE_ID}} for **${{AMOUNT}}**, issued on {{INVOICE_DATE}}, was due on {{DUE_DATE}}.

If you've already sent payment, please disregard this message. Otherwise, you can pay via {{PAYMENT_METHOD/LINK}}.

Feel free to reach out with any questions.

Best,
{{SENDER_NAME}}
{{FIRM_NAME}}

---

## Tier 2: Second Notice (31–60 Days Past Due)

**Subject:** Second Notice — Invoice {{INVOICE_ID}} Now {{DAYS_PAST_DUE}} Days Overdue

Hi {{CUSTOMER_NAME}},

We wanted to follow up regarding invoice {{INVOICE_ID}} for **${{AMOUNT}}**, which was due on {{DUE_DATE}} and remains unpaid.

Please arrange payment at your earliest convenience using {{PAYMENT_METHOD/LINK}}.

If there's an issue with the invoice or you need to discuss payment arrangements, please reply to this email or call us at {{PHONE}}.

Thank you,
{{SENDER_NAME}}
{{FIRM_NAME}}

---

## Tier 3: Firm Request with Payment Plan Option (61–90 Days Past Due)

**Subject:** Urgent: Invoice {{INVOICE_ID}} — ${{AMOUNT}} Now {{DAYS_PAST_DUE}} Days Overdue

Dear {{CUSTOMER_NAME}},

Our records indicate that invoice {{INVOICE_ID}} for **${{AMOUNT}}** remains unpaid, now {{DAYS_PAST_DUE}} days past its due date of {{DUE_DATE}}.

We request immediate payment. If you are experiencing financial difficulties, we are open to discussing a structured payment plan. Please contact us within **5 business days** to avoid further action.

Payment can be made via: {{PAYMENT_METHOD/LINK}}

Please treat this as urgent.

Regards,
{{SENDER_NAME}}
{{FIRM_NAME}} | {{PHONE}}

---

## Tier 4: Final Notice — Escalation Warning (91–120 Days Past Due)

**Subject:** FINAL NOTICE — Invoice {{INVOICE_ID}} — ${{AMOUNT}} — Immediate Action Required

Dear {{CUSTOMER_NAME}},

Despite previous notices, invoice {{INVOICE_ID}} for **${{AMOUNT}}** remains outstanding — now {{DAYS_PAST_DUE}} days past due.

**This is our final notice before we escalate this matter.**

Unless full payment or a confirmed payment arrangement is received by **{{DEADLINE_DATE — 10 business days out}}**, we will be required to pursue further collection actions, which may include referral to a collections agency or legal action.

To resolve this immediately: {{PAYMENT_METHOD/LINK}} or call {{PHONE}}.

Sincerely,
{{SENDER_NAME}}
{{FIRM_NAME}}

---

## Tier 5: Collections/Legal Escalation Notice (120+ Days Past Due)

**Subject:** Collections Referral Notice — Invoice {{INVOICE_ID}} — ${{AMOUNT}}

Dear {{CUSTOMER_NAME}},

We regret to inform you that your account balance of **${{AMOUNT}}** (invoice {{INVOICE_ID}}, due {{DUE_DATE}}) has been referred for {{collections agency review / legal action}}.

This referral may affect your credit rating and result in additional fees and legal costs.

To stop this process, payment in full must be received by **{{DEADLINE_DATE}}** via {{PAYMENT_METHOD/LINK}}.

If you believe this notice was sent in error, contact us immediately at {{PHONE}} or {{EMAIL}}.

{{SENDER_NAME}}
{{FIRM_NAME}} | {{PHONE}}

---

## Usage Notes

- Always verify invoice details before sending
- CC Irfan on Tier 3+ drafts for review
- Log send date and tier in payment promise tracker
- Never send Tier 4 or 5 without explicit Irfan approval
- Attach original invoice PDF when possible (Tier 2+)
