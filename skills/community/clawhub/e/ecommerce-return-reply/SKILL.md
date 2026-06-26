---
name: ecommerce-return-reply
description: Generate standardized, policy-compliant customer service replies for buyer return, exchange, and refund inquiries in e-commerce scenarios. Use when drafting or composing responses to buyer messages about returns, exchanges, refunds, order cancellations, damaged goods, wrong items received, or any after-sales dispute. Covers major Chinese and cross-border e-commerce platforms (Taobao, JD, PDD, Douyin, Shopee, Lazada, Amazon).
---

# E-commerce Return & Exchange Reply Generator

Standardized prompt template for generating compliant, friendly after-sales responses.

## Workflow

1. Identify the buyer's issue category from the message.
2. Read the corresponding rule section in `references/platform-rules.md`.
3. Compose the reply following the output template below.

## Issue Categories

| Category | Trigger Keywords |
|---|---|
| Return (refund only) | 退货, 退款, 不想要了, doesn't fit, changed mind |
| Exchange | 换货, 换颜色, 换尺码, wrong size, wrong color |
| Damaged / Defective | 破损, 坏了, 质量问题, cracked, defective, broken on arrival |
| Wrong Item | 发错货, 收到不一样, wrong item, not what I ordered |
| Partial Refund | 补偿, 差价, partial refund, price difference |
| Cancellation | 取消订单, 不买了, cancel my order |

## Output Template

Every reply must contain these sections in order:

```
【问候】— 礼貌称呼买家，表达歉意/理解
【问题确认】— 简要复述买家问题（1句）
【解决方案】— 明确告知可操作的下一步（退货/换货/补偿等）
【操作指引】— 平台操作步骤（2-3步），引用平台规则条款
【时效说明】— 处理时效与物流预估
【温馨提示】— 退货注意事项（包装、配件、运费等）
【结尾】— 感谢与联系方式
```

## Tone & Style Rules

- Use 敬语 (您/亲) for Chinese; warm but professional for English
- Never blame the buyer
- Never promise outcomes outside platform policy
- Include specific timeframes (e.g., "48小时内", "within 2 business days")
- If the request falls outside policy, explain politely and offer the best alternative

## Policy Compliance

- Read `references/platform-rules.md` before composing any reply
- When in doubt, default to the stricter interpretation
- Always state the applicable rule clause (e.g., "根据《七天无理由退货》规则…")

## Platform Awareness

If the buyer's platform is unknown, ask. Rules differ significantly:

- Taobao/JD: 7-day no-reason return for most categories
- PDD: Shorter window, stricter conditions
- Cross-border (Shopee/Lazada/Amazon): Varies by marketplace and region
- Live-stream sales (Douyin): Special 15-day rule may apply

## Advanced: Custom Policy Override

If the merchant has custom return policies (e.g., extended warranty, free return shipping), include them as additional context in the prompt call. Custom policies supplement but never contradict platform rules.