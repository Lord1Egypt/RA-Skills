# Email Sequences — Output Template

Use this template for every Email Sequences deliverable. Fill in all sections. Write "N/A — [reason]" for non-applicable sections.

---

## Sequence Summary

| Field | Value |
|---|---|
| Campaign type | [abandoned cart / post-purchase / win-back / welcome / seasonal / loyalty] |
| Platform | [Klaviyo / Mailchimp / Omnisend / ActiveCampaign / other] |
| Trigger | [behavioral trigger or scheduled date] |
| Target segment | [new subscribers / repeat buyers / VIPs / lapsed 90d+ / all consented] |
| Offer (if any) | [discount code, amount, expiry] |
| Brand voice | [tone notes] |
| Emails in sequence | [N] |

---

## Sequence Overview Table

| Email | Timing | Angle | Offer |
|---|---|---|---|
| Email 1 | [Xh after trigger] | [angle description] | [none / offer description] |
| Email 2 | [Xh after trigger] | [angle description] | [none / offer description] |
| Email 3 | [Xh after trigger] | [angle description] | [none / offer description] |

**Exit conditions:** [e.g., "Purchase exits all emails. Opt-out exits all emails."]

---

## Email 1 of N

**Trigger / send time:** [behavioral trigger or delay]

**Subject line:** [subject line text — note character count]
**Preview text:** [preview text — aim for 85–100 characters]

**Body copy:**

---
[Full email body. Use [FIRST_NAME], [PRODUCT_NAME], [ORDER_NUMBER], [LINK] as merge tag placeholders.]
---

**CTA button text:** [single action verb phrase]
**CTA destination:** [page type — cart, product, checkout, account]

**A/B Subject Line Variant:**
- Variant A: [primary subject]
- Variant B: [alternative subject with different hook angle]
- Variable being tested: [urgency / curiosity / personalization / benefit-first]

---

## [Repeat Email block for each message in sequence]

---

## Suppression and Exit Logic

| Event | Action |
|---|---|
| Purchase | Exit sequence immediately — suppress all remaining emails |
| Opt-out | Exit sequence — add to suppression list permanently |
| Email open (optional) | [suppress next email / no action — note your choice] |
| Sequence completion without purchase | Re-entry delay: [X days] minimum |
| Frequency cap | [Do not send if subscriber received any flow/campaign in past X hours] |

---

## Platform Setup Notes

**[Platform name]:**
- Trigger configuration: [specific event or segment criteria]
- Flow exit event: [metric name in platform]
- Suppression list: [name or tag]
- A/B test setup: [split percentage recommendation]
- Send time optimization: [on/off — note recommendation]

---

## Notes and Flags

[List any compliance issues, segmentation assumptions, consent requirements, or recommendations not covered above.]
