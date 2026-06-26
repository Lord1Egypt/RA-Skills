# Checkout dropoff recovery playbook

Load when `cart-recovery` needs depth. Use by section.

---

## 1. Instrumentation (align events to steps)

| Conceptual step | Example events (names vary) |
|-----------------|------------------------------|
| Contact / address | `checkout_contact_info_submitted`, `checkout_address_completed` |
| Shipping | `add_shipping_info`, `shipping_rate_selected` |
| Payment | `add_payment_info`, `payment_submit`, gateway errors |

**Exit rate** for step *i*: sessions that reached step *i* but not step *i+1*, divided by sessions that reached step *i*.

---

## 2. Compensation design guardrails

- **Shipping comp** after address exit: use **margins** and **AOV**; cap **per user** or **time-box** to prevent abuse.
- **BNPL / installments** after payment exit: explain **eligibility**, **fees (if any)**, and **refund flow**—avoid promising approval.
- **Urgency**: true **cart expiry**, **real inventory** if verified, **real promo end**—never fabricate.

---

## 3. Email 1 — [Urgency] (ethical patterns)

- Honest **stock** or **price change date** if real.  
- **Cart link** + one line on **why finish now** (event, shipping cutoff).  
- Optional: small **time-bound** shipping code **if policy allows**.

---

## 4. Email 2 — [Trust rebuild]

- **Security** (SSL, processor names), **returns**, **reviews**, **human support** channel.  
- If exit at address/shipping: **delivery map** or **duty/transparency** one-liner.  
- If exit at payment: **BNPL logos + 1-sentence how it works**.

---

## 5. Email 3 — [Ultimatum]

- **Final email** in this sequence; **deadline** for offer if any.  
- **Graceful out**: "Still stuck? Reply with one issue—we’ll help."  
- **Unsubscribe** visible; no harassment tone.

---

## 6. SMS or push (optional add-on)

- Mirror the **three themes** in shorter form; **opt-in** and **STOP** compliance.
