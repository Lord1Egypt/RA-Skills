---
name: consumer-rights
slug: consumer-rights
description: "Generate complaint letters, 12315 filings, and escalation paths for consumer disputes in China."
---

# Consumer Rights

Use this skill when the user has a consumer dispute in China and needs structured escalation documents — complaint letters, 12315 filing, evidence checklist, and risk assessment.

## Good triggers

- "I got scammed on Pinduoduo, help me file a complaint."
- "Write a 12315 complaint for defective electronics."
- "Merchant won't refund — what are my rights?"
- "Food safety issue, how do I escalate?"
- "Generate consumer-rights documents for a false advertising case."

## Workflow

1. **Parse user scenario.** Identify dispute type: quality defect, false advertising, refund denial, food safety, counterfeit, delivery damage.

2. **Extract key fields.** Platform, merchant name, amount paid, date of purchase, description of issue, existing evidence (screenshots, receipts, chat logs, tracking numbers).

3. **Map applicable laws.** Based on dispute type, cite relevant provisions:
   - Quality defect → 消费者权益保护法 §24
   - False advertising → 广告法 §4/§56
   - Food safety → 食品安全法 §148
   - E-commerce → 电子商务法 §20/§38

4. **Assess win rate.** Evaluate strength of evidence and amount in dispute:
   - Strong (clear receipts, screenshots, merchant admission) → 80-100%
   - Moderate (receipts exist, screenshots partial) → 50-80%
   - Weak (no receipt, incomplete chat records) → 10-50%

5. **Generate three escalation documents:**
   - **Merchant negotiation letter** — polite, cites facts and law, requests resolution within 3 days
   - **Platform complaint** — formal submission to platform (PDD/Taobao/JD/Douyin) using their dispute-filing template
   - **12315 complaint application** — ready-to-file structured PDF/Markdown with all required fields: product, merchant, amount, cause, demand

6. **Evidence checklist.** Prioritize by usefulness:
   - [ ] Order page screenshot
   - [ ] Payment receipt
   - [ ] Chat logs with merchant
   - [ ] Product photos/video showing defect
   - [ ] Unboxing video (if applicable)
   - [ ] Third-party appraisal or report (for high-value items)

7. **Escalation path map.** Lay out step-by-step:
   - Step 1: Merchant negotiation (3 days)
   - Step 2: Platform complaint (3-7 days)
   - Step 3: 12315 hotline (12315.cn / WeChat mini program) (7-15 days)
   - Step 4: Market Supervision Bureau (行政投诉)
   - Step 5: Small Claims Court (小额诉讼, amounts < 50K RMB)

8. **Litigation risk assessment.** Cost-benefit analysis:
   - Legal costs (filing fees, possibly lawyer)
   - Time commitment (2-6 months for court)
   - Likely outcome vs settlement offers

9. **Package and output.** Deliver a single bundled report containing all documents, checklist, escalation path, and risk note formatted for immediate use.

## Sample prompt

```
consumer-rights complain --description "在拼多多买的手机标称512GB实际128GB，商家不承认，花费1899元"
```
