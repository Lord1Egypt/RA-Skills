# PayPal & Stripe Dispute Reference

> PayPal and Stripe disputes work differently from card network chargebacks.
> They operate their own dispute resolution systems first — with card chargebacks as a backstop.

---

## PayPal Disputes

### How PayPal disputes work
PayPal has its own internal dispute system (Resolution Center) that must be used before escalating to a card chargeback. The process has two stages:

**Stage 1 — Dispute:** You and the seller communicate. PayPal holds the payment while you try to resolve it directly.
**Stage 2 — Claim:** If no resolution within 20 days, you escalate to a PayPal Claim. PayPal reviews evidence from both sides and decides.

If PayPal rules against you, you may still be able to file a chargeback through your funding source (credit card or bank) — but PayPal will close your account if they determine you filed a chargeback while a PayPal dispute was ongoing.

### PayPal filing deadline
**180 days** from the transaction date — significantly longer than card networks.

### Where to file
paypal.com → Activity → find transaction → "Report a Problem"
Or: paypal.com/disputes

### PayPal dispute categories

| Category | Code | Use when |
|---|---|---|
| Item Not Received (INR) | INR | Paid but goods/services never delivered |
| Significantly Not as Described (SNAD) | SNAD | Item received is materially different from listing |
| Unauthorized Transaction | UAT | Transaction you didn't authorize |
| Billing Issue | BIL | Duplicate charge, incorrect amount |

### Evidence for PayPal

**INR:**
- Order confirmation
- Any tracking or shipping information
- Communication with seller showing non-delivery
- Proof delivery window has passed

**SNAD:**
- Original eBay/PayPal listing or seller's product description (screenshot)
- Photos clearly showing what you received vs. what was described
- Evidence you attempted return (seller's response or lack of response)
- Return tracking if you shipped the item back

**Unauthorized:**
- Statement that you did not authorize the transaction
- Note any account security events (unusual login, password change)

### PayPal dispute timeline

| Stage | Timeframe |
|---|---|
| Open dispute | Day 0 |
| Seller response window | 3 days (INR) or 10 days (SNAD) |
| Escalate to Claim | After seller response window, or after 20 days if no resolution |
| PayPal investigation | Up to 30 days after Claim opened |
| Resolution | 30–45 days total typical |

### PayPal-specific tips
- **Always open a PayPal dispute FIRST** — don't go straight to your card issuer. Doing so while a PayPal dispute is open can get your PayPal account limited.
- **For unauthorized charges:** Skip the dispute stage and go straight to "Report Unauthorized Activity" — this triggers PayPal's fraud team, not the general dispute process.
- **eBay purchases:** Use eBay's Money Back Guarantee first. If that fails, then PayPal dispute. Card chargeback is the last resort.
- **PayPal Credit:** Disputes on PayPal Credit go through Synchrony Bank (the issuer), not PayPal's Resolution Center.
- **Friends & Family payments:** PayPal explicitly does NOT cover F&F payments with buyer protection. If you were tricked into paying via F&F, your only option is to report it to PayPal as unauthorized and potentially to your bank.
- **After PayPal denies your claim:** You can still escalate to your funding source (credit card chargeback) if PayPal denies you AND you paid with a credit card. You have 60–120 days from the original transaction date depending on your card network.

---

## Stripe Disputes

### How Stripe disputes work
Stripe is a payment processor used by merchants — you don't have an account with Stripe directly. When you dispute a Stripe-processed charge, you file with **your bank or card issuer**, not with Stripe. Stripe then receives the chargeback and passes it to the merchant to respond.

**You never interact with Stripe directly as a consumer.**

### What "Stripe dispute" means in practice
When you see a charge from a company that uses Stripe (identifiable if the bank statement shows "Stripe" or the company's name followed by "via Stripe"):

1. File the dispute with **your card issuer** (Visa, Mastercard, Amex) using standard card network procedures
2. Stripe notifies the merchant automatically
3. The merchant has 5–7 days to respond through Stripe's dashboard
4. Your card issuer makes the final decision

### Evidence for Stripe-processed disputes
Same as the card network rules above — file as a standard Visa, Mastercard, or Amex dispute. The evidence requirements are determined by your card network, not Stripe.

### Stripe-specific context for your dispute letter
If you know the charge was processed through Stripe, you can add this line to your dispute letter:
*"This charge was processed through Stripe. I am requesting a standard [Visa/Mastercard] chargeback under reason code [X]."*

This isn't required but signals you understand the process.

### Common Stripe-powered merchants
Many subscription SaaS products, e-commerce stores, and marketplaces use Stripe. If you don't recognize a charge, look up the merchant name — their website will often have a Stripe checkout.

### Stripe dispute timeline
Same as the underlying card network (Visa or Mastercard). Stripe's internal timeline for notifying the merchant is 5–7 days from when your bank files the chargeback.

---

## Escalation path summary

| Platform | Step 1 | Step 2 | Step 3 |
|---|---|---|---|
| PayPal | PayPal dispute (Resolution Center) | PayPal Claim | Card chargeback (if paid by card and PayPal denies) |
| Stripe | File with your card issuer | Card network handles | No further escalation needed |
| Venmo | Venmo dispute (for unauthorized only) | Contact bank | Card chargeback (if funded by card) |
| Cash App | Cash App dispute | Contact bank | Very limited protection for P2P payments |

**Warning on P2P payments (Venmo, Cash App, Zelle):** These platforms have very limited buyer protection for authorized payments sent to the wrong person or to a scammer. The chargeback right depends on whether you funded the payment with a credit card — if you used a bank account, protection is minimal. Always flag this honestly to the user if they mention these platforms.
