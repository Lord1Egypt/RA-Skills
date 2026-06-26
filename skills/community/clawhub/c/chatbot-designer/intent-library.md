# Intent Library — Ecommerce Chatbot

## Order Status Intent

**Trigger keywords:** "where is my order", "track", "tracking", "shipping status", "hasn't arrived", "order status", "when will it arrive", "delivery"

**Required data:** Order number OR email address

**Success response template:**
> "I found your order! Order #[number] shipped on [date] via [carrier]. Your tracking number is [tracking] — click here to see live updates: [link]. Estimated delivery: [date]. Is there anything else I can help with?"

**Delayed order response:**
> "Your order #[number] is currently showing a delay with [carrier]. The new estimated delivery is [date]. I've flagged this on your account. If it doesn't arrive by [date+1], come back and I can file a claim on your behalf."

**Not found response:**
> "I couldn't find an order with that information. Can you double-check the order number? It's usually in your confirmation email and starts with #. If you still can't find it, let me connect you with our team."

---

## Return Request Intent

**Trigger keywords:** "return", "refund", "exchange", "send back", "doesn't fit", "changed my mind", "not what I expected"

**Required data:** Order number, reason for return

**Eligible return response:**
> "I can process this return for you. Your order is within our [30-day] return window. I'll send a prepaid return label to [email] — please allow 5–10 minutes for it to arrive. Once we receive your return, your refund will be processed within [X] business days."

**Ineligible return response (outside window):**
> "This order was delivered on [date] — our [30-day] return window closed on [date]. I'm not able to process this automatically, but I'll connect you with our team who can review your situation."

**Exchange response:**
> "For an exchange, I'll need to process a return and place a new order. Would you like me to start the return process? You can then place a new order with the correct [size/color/item], and I can apply a discount code for the inconvenience."

---

## Shipping Delay Intent

**Trigger keywords:** "late", "delayed", "hasn't shipped", "still processing", "stuck", "where", "overdue"

**Response template:**
> "I'm sorry to hear your order is running late. Let me check on this. [Look up order status] Your order is currently [status]. [If in transit:] It looks like there's been a carrier delay — the new estimated delivery is [date]. [If not yet shipped:] It's still being prepared for shipment. I'll flag this as high priority for our fulfillment team."

---

## Wrong Item Received Intent

**Trigger keywords:** "wrong item", "wrong product", "not what I ordered", "incorrect", "different item"

**Response template:**
> "I'm really sorry about that — receiving the wrong item is frustrating. I'd like to make this right. Can you share: (1) your order number, and (2) what you received vs. what you ordered? I'll initiate a replacement shipment and arrange return of the incorrect item at no cost to you."

---

## Product Question Intent (Pre-Purchase)

**Trigger keywords:** "compatible", "does it work with", "what size", "fit", "material", "dimensions", "specifications"

**Response template:**
> "Great question! [Answer from FAQ database]. [If not found:] I don't have that specific detail on hand — let me connect you with someone who can confirm before you order."

**Compatibility check template:**
> "The [product] is [compatible/not compatible] with [device/model]. [Add specific detail.] Does that help, or would you like to check something else?"

---

## Cancellation Request Intent

**Trigger keywords:** "cancel", "don't want it", "change my mind", "cancel order"

**Pre-shipment response:**
> "I can cancel this order since it hasn't shipped yet. Confirming cancellation of order #[number] — your refund of $[amount] will appear within 3–5 business days. Is there anything I can help you find instead?"

**Post-shipment response:**
> "Unfortunately, order #[number] has already shipped, so I'm not able to cancel it at this stage. Once you receive it, I can process a return with a free prepaid label. Would you like me to set that up in advance?"

---

## Promo Code Issue Intent

**Trigger keywords:** "code doesn't work", "discount not applying", "coupon", "promo", "won't accept"

**Response template:**
> "Let me check on that code. [Validate code status] [If valid but not applying:] This code applies to [eligible products/categories] — it looks like your cart may have [ineligible item]. Try removing [item] and re-entering the code. [If expired:] This code expired on [date]. Would you like me to check if there's a current offer I can apply? [If not found:] I couldn't find this code in our system. Can you double-check the spelling? Promo codes are case-sensitive."

---

## Escalation Handoff Script Templates

**Warm handoff (frustration detected):**
> "I can see this has been really frustrating, and I want to make sure you get the best help possible. I'm connecting you now with [Name/Team] — they specialize in situations like yours. I've shared our entire conversation so you won't need to repeat anything. They'll reply to you at [email] within [timeframe]."

**After-hours escalation:**
> "Our team is currently offline, but I've created a priority ticket for you (#[ticket number]). You'll receive a reply at [email] by [specific time] tomorrow. In the meantime, here's what I've noted about your issue: [summary]."

**High-value customer escalation:**
> "You're one of our valued customers, and I want to make sure this is handled by our senior support team. I'm flagging this as priority and someone will be in touch within [1–2 hours] during business hours."
