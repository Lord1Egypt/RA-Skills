# Error Message Copy Guide — Checkout Recovery

Checkout error messages are the last conversation you have with a buyer before they leave. Good error copy turns a soft failure into a recovered sale. Bad error copy turns a fixable issue into permanent churn.

---

## Principles of Effective Error Message Copy

1. **Tell buyers what happened** (not just that something failed)
2. **Tell buyers what to do next** (give a specific, actionable next step)
3. **Maintain trust** (avoid accusatory language; it's never the buyer's fault)
4. **Be specific where possible** (card-specific errors vs. generic "payment failed")
5. **Offer an alternative payment path** (if they can't use the current method, show them another)

---

## Error Types and Rewrite Templates

### Card Declined (Bank Declined)

**❌ Weak:**
> Payment failed. Please try again.

**❌ Also weak:**
> Error: CARD_DECLINED

**✅ Strong:**
> We couldn't process your card. This sometimes happens when banks flag online purchases. Try a different card, or complete your order with PayPal — it only takes a moment.

**✅ Alternative for mobile:**
> Card not accepted. Try using Apple Pay or enter a different card to complete your order.

---

### Insufficient Funds

**❌ Weak:**
> Transaction declined.

**✅ Strong:**
> It looks like your card may have a balance issue. You can split this order across two cards, or try PayPal or Klarna to pay later in installments.

*Note: Don't use the phrase "insufficient funds" — it's embarrassing for the buyer and kills trust.*

---

### Address Verification Failed (AVS Mismatch)

**❌ Weak:**
> Your payment was not processed.

**✅ Strong:**
> We had trouble verifying your billing address. Make sure the address matches what's on file with your bank, then try again. Or use PayPal to skip this step — PayPal handles address verification automatically.

---

### Network Timeout / Technical Error

**❌ Weak:**
> Something went wrong. Please try again later.

**✅ Strong:**
> We hit a brief connection issue and your order wasn't placed. Your card has not been charged. Click below to try again — it usually works on the second attempt.

*Key: explicitly reassure that the card was NOT charged. This is the primary anxiety when a buyer sees a payment error.*

---

### Card Number Invalid / Entry Error

**❌ Weak:**
> Invalid card details.

**✅ Strong:**
> Double-check your card number — we couldn't validate it. If you're sure it's correct, try a different payment method below.

---

### 3D Secure / Authentication Failed

**❌ Weak:**
> Authentication failed.

**✅ Strong:**
> Your bank asked us to verify your identity, but we couldn't complete it. This sometimes happens when your banking app times out. Try opening your bank's app and approving the request, or use a different payment method.

---

### Card Expired

**❌ Weak:**
> Card expired.

**✅ Strong:**
> That card has expired. Enter your updated card details, or use PayPal or Apple Pay to check out instantly.

---

## Recovery Nudge Copy Within Checkout Flow

After a payment failure, display an alternative payment option nudge immediately:

**Inline nudge template:**
> Having trouble with your card? Try [PayPal / Apple Pay / Klarna] instead.
> [Button: Pay with PayPal] [Button: Pay with Apple Pay]

This keeps the buyer in the checkout flow instead of forcing them back to the cart.

---

## Abandoned Checkout Recovery Email Templates

### Email 1 — Soft Reminder (Send at 1 hour)

**Subject options:**
- "You left something behind, [First Name]"
- "Still thinking about [Product Name]?"
- "Your [Product Name] is waiting for you"

**Body template:**
> Hi [First Name],
>
> You were so close! Your [Product Name] is still in your cart — we've saved your order so you can pick up right where you left off.
>
> [Product image] | [Product Name] | [Price]
>
> [Button: Complete My Order]
>
> Your cart is saved for [24/48] hours. If you have any questions, reply to this email or reach us at [support email].
>
> [Store Name]

---

### Email 2 — Social Proof (Send at 24 hours)

**Subject options:**
- "[X] people love [Product Name] — here's what they say"
- "Here's what customers are saying about [Product Name]"

**Body template:**
> Hi [First Name],
>
> Still deciding? Here's what customers are saying about [Product Name]:
>
> ⭐⭐⭐⭐⭐ "[Customer review quote — specific and authentic]" — [Customer name/initials]
>
> ⭐⭐⭐⭐⭐ "[Another customer review quote]" — [Customer name/initials]
>
> [Button: Complete My Order]
>
> [Store Name]

---

### Email 3 — Final Nudge (Send at 72 hours)

**Subject options:**
- "Last chance — your cart expires soon"
- "[First Name], your [Product Name] is about to go"

**Body template:**
> Hi [First Name],
>
> Your cart is about to expire. If you've been waiting for the right moment — this is it.
>
> [If including discount]: Use code COMEBACK10 for 10% off your order, valid until [date/time].
>
> [Product image] | [Product Name] | [Price / Discounted Price]
>
> [Button: Complete My Order]
>
> After [date], your cart will clear and we can't guarantee availability.
>
> [Store Name]

*Only include a discount code on the 3rd email — not the 1st or 2nd. Sending discounts in the first email trains buyers to abandon intentionally.*

---

## SMS Recovery Templates

### SMS 1 (Send at 30 minutes after abandonment if SMS opt-in)
> [Store Name]: You left [Product Name] in your cart. Complete your order here: [short link] Reply STOP to unsubscribe.

### SMS 2 (Send at 24 hours)
> [Store Name]: Still interested in [Product Name]? [X] customers bought it this week. Order yours: [short link] Reply STOP to unsubscribe.

---

## Push Notification Templates

### Push 1 (Send at 1 hour)
> **You left something in your cart** 🛒
> [Product Name] is waiting for you. Tap to complete your order.

### Push 2 (Send at 24 hours)
> **Your cart is about to expire**
> [Product Name] — finish your order before it's gone.

---

## What to Avoid

| Avoid | Why |
|---|---|
| "Your card was rejected" | "Rejected" feels accusatory — use "couldn't process" instead |
| Raw error codes (e.g., "Error 4012") | Meaningless to buyers; creates anxiety |
| "Please try again later" | Vague and off-putting; buyers leave |
| Discount in email 1 | Trains buyers to abandon for discounts |
| Generic "you left something" with no product reference | 40% lower recovery rate than product-specific messages |
| Fake urgency ("only 1 left!" when it's not true) | Destroys trust permanently if detected |
