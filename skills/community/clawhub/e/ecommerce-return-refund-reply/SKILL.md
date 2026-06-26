---
name: ecommerce-return-refund-reply
description: Generate standardized, policy-compliant customer service replies for e-commerce return, exchange, and refund inquiries. Use when a buyer asks about returning an item, exchanging a product, requesting a refund, checking return eligibility, or any after-sales consultation. Covers scenarios like damaged goods, wrong items, size issues, quality complaints, change-of-mind returns, and refund status checks.
---

# E-commerce Return & Refund Reply Generator

Produce a single, ready-to-send reply to a buyer's return/exchange/refund inquiry.

## Input Required

Before generating, confirm these variables (ask the user if missing):

| Variable | Example |
|---|---|
| `buyer_question` | "我收到的衣服有个洞，想退货" |
| `issue_type` | damaged / wrong_item / size_issue / quality / change_of_mind / refund_status |
| `order_status` | unreceived / received |
| `return_window` | e.g. 7 days, 15 days (per platform rule) |
| `platform` | taobao / jd / pdd / douyin / other |

## Workflow

1. **Classify** the inquiry into one `issue_type`.
2. **Select template** from [references/reply-templates.md](references/reply-templates.md) by `issue_type`.
3. **Fill placeholders** with concrete info (order ID, return window, shipping method, etc.).
4. **Apply tone rules** below.
5. **Output** the final reply — one message only, no meta-commentary.

## Tone & Style Rules

- **Friendly & empathetic** — acknowledge the buyer's frustration before offering solutions.
- **Concise** — under 200 words; no walls of text.
- **Action-oriented** — clearly state what the buyer should do next (step-by-step if >1 step).
- **Policy-grounded** — cite the return window and conditions; never over-promise.
- **No legal jargon** — use plain language a typical buyer understands.
- **Closing** — always end with an open invitation: "如有其他问题，随时联系我们 😊"

## Policy Guardrails

- Do **not** offer refunds that exceed the order amount.
- Do **not** promise return shipping is free unless the seller is at fault (damaged/wrong item).
- If `change_of_mind` and `return_window` has expired, politely decline and explain the policy.
- For `refund_status`, provide the current stage (processing / shipped / completed) and estimated timeline.

## Output Format

```
【应答内容】
<the reply text, ready to copy-paste>

【内部备注】
Issue type: <issue_type>
Template used: <template_name>
Policy checked: ✅
```