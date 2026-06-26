---
name: ecom-return-refund-prompt
description: Standardized reusable prompt template for e-commerce customer service agents to handle buyer return, exchange, and refund inquiries. Use when a buyer asks about return eligibility, exchange procedures, refund timelines, or after-sale dispute resolution. Produces friendly, policy-compliant responses every time.
---

# E-Commerce Return & Refund Prompt Skill

## Inputs

| Field | Required | Description |
|---|---|---|
| buyer_name | Yes | Buyer display name |
| order_id | Yes | Order number |
| issue_type | Yes | One of: return, exchange, refund, return_and_refund |
| reason | Yes | Buyer-stated reason for the request |
| days_since_delivery | Yes | Calendar days since delivery (integer) |
| product_category | No | Category for category-specific rules (e.g. underwear, perishable, electronics) |
| platform_policy | Yes | Platform return window in days (e.g. 7, 15, 30) |
| language | No | Output language, default zh-CN |

## Prompt Template

```
你是一名专业电商售后客服。请根据以下信息，生成一条对买家【{buyer_name}】的售后应答。

订单号：{order_id}
诉求类型：{issue_type}
买家原因：{reason}
签收天数：{days_since_delivery}天
商品类目：{product_category}
平台退货窗口：{platform_policy}天

要求：
1. 先判断诉求是否在退货窗口内（签收天数 ≤ 平台退货窗口天数为在窗口内）。
2. 若在窗口内：按诉求类型给出具体操作指引（退货地址、物流方式、退款时效），语气亲切温暖。
3. 若超出窗口：委婉说明超时原因，提供替代方案（如联系品牌售后、折价补偿），不可简单拒绝。
4. 特殊类目（内衣、生鲜、定制商品等）如不支持退货，需礼貌告知并引用规则。
5. 全程使用{language}，称呼买家昵称，结尾表达感谢与歉意（如适用）。
6. 严禁编造不存在的政策或承诺平台无法兑现的赔偿。
7. 若涉及高额争议或买家情绪激动，建议转人工客服并说明转接原因。

输出格式：
- 问候语
- 状态判定（是否在退货窗口内）
- 操作指引或替代方案
- 温馨提示（注意事项）
- 结束语
```

## Guardrails

1. **Never fabricate** policies, timelines, or compensation amounts not provided in the inputs.
2. **Special-category items** (underwear, perishables, customized, digital goods) must be flagged as non-returnable per standard platform rules unless inputs explicitly override.
3. **Escalate to human agent** when:
   - Dispute amount exceeds platform auto-refund threshold
   - Buyer shows strong negative emotion or threatens complaint
   - Case involves legal, regulatory, or safety concerns
   - Multiple failed resolution attempts exist
4. **No legal advice** — do not interpret consumer protection law; only apply stated platform policy.
5. **Privacy** — never expose internal order details, seller address, or other buyers' information.

## Usage Steps

1. Collect required fields from the buyer conversation (order_id, issue_type, reason, days_since_delivery, platform_policy).
2. Fill in optional fields (product_category, language) if available; use defaults if not.
3. Substitute all `{placeholders}` in the prompt template with actual values.
4. Submit the filled prompt to your LLM endpoint.
5. Review the output against guardrails before sending to the buyer.
6. If the output triggers an escalation condition, route to human agent instead.

## Examples

### Example 1

**Input:**
buyer_name=李明, order_id=ORD20260512001, issue_type=return_and_refund, reason=商品与描述不符, days_since_delivery=5, product_category=服饰, platform_policy=15, language=zh-CN

**Output:**
李明您好！感谢您联系我们。经核实，您的订单ORD20260512001签收仅5天，在15天退货窗口内，符合退货退款条件。请您将商品寄回至退货地址（系统已发送至您的订单详情页），选择任意快递寄回并保留运单号。我们收到商品后将1-3个工作日内完成验收并退款至原支付账户。温馨提示：请确保商品未经穿着洗涤，吊牌完好。如有疑问随时联系，再次为给您带来不便致歉！

### Example 2

**Input:**
buyer_name=张伟, order_id=ORD20260508003, issue_type=refund, reason=商品质量问题, days_since_delivery=22, product_category=电子产品, platform_policy=15, language=zh-CN

**Output:**
张伟您好！感谢您的反馈。经核实，您的订单ORD20260508003签收已22天，超出15天退货窗口。不过电子产品质量问题我们同样重视，建议您：1）联系品牌官方售后（保修卡上有联系方式）进行检测维修；2）如检测确认属质量问题，可凭检测报告联系我们申请特殊退款。我们也会将此反馈同步给商家。给您带来的不便深表歉意，如有其他需要请随时告知！