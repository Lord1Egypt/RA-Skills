# Stock Visibility Guide — Flash Sale Designer

How and when to show inventory levels to maximize urgency without eroding trust.

## Core Rule

**Never show a number you can't keep accurate in near-real-time.**
If your inventory system has a 10-minute sync delay, don't show "47 left" — show "Less than 50 remaining."

---

## Threshold-Based Visibility Rules

| Stock Remaining (% of Flash Allocation) | Display Rule |
|---|---|
| 100–70% | No stock count needed — show discount and timer |
| 70–50% | Optional: "Selling fast" badge |
| 50–30% | Show "Only [N] left" if system is real-time |
| 30–15% | Mandatory: "Only [N] left at this price" |
| 15–5% | "Almost gone — [N] units remaining" + badge |
| <5% | "Last [N] units" with high-urgency styling |
| 0% | "Sold out — join waitlist for next event" |

---

## Social Proof Counters

When early sales velocity is strong, shift from "X left" to "X sold" framing:

- `[N] units sold in the last hour`
- `[N] people bought this today`
- `[N] sold since the event started`

**Use "sold" framing when**: At least 20% of allocation has sold in the first hour.
**Stick to "remaining" framing when**: Sales are slow — showing a high remaining count undermines urgency.

---

## Cart Reservation Logic (If Supported)

If your platform supports cart holds:
- Reserve items in cart for 10–15 minutes maximum
- Display: "Held in your cart for [MM:SS] — complete checkout to secure your order"
- Release back to inventory if checkout isn't completed

This creates real scarcity that reinforces the countdown.

---

## Platform-Specific Notes

**Shopify**
- Use a real-time inventory app (e.g., Inventory Planner, or native Shopify inventory tracking)
- Liquid variable: `product.variants.first.inventory_quantity`
- Third-party urgency apps: Hurrify, Countdown Timer Bar, Sales Countdown Timer

**TikTok Shop**
- Stock visibility is handled natively by the platform during live events
- Manually announce stock levels verbally during live: "We're down to the last 50!"

**Amazon Lightning Deals**
- Amazon controls the percentage-claimed progress bar — you cannot customize it
- Focus on pre-event hype to drive initial velocity, which Amazon's algorithm amplifies

**WooCommerce**
- Enable "Stock management" per product in WooCommerce settings
- Use WooCommerce Countdown Timer or FOMO plugins for urgency display

---

## Messaging Tone by Stock Level

| Stock Level | Tone | Example Copy |
|---|---|---|
| 100–50% | Informational | "Sale ends at 5pm" |
| 50–30% | Mild urgency | "Selling faster than expected" |
| 30–15% | Direct urgency | "Only 42 units left at this price" |
| 15–5% | High urgency | "Almost gone — 12 units remaining" |
| <5% | Critical urgency | "Last 4 units. Checkout now or miss it." |
| 0% | Graceful close | "Sold out. Join the waitlist for the next event." |

---

## What Not to Do

- **Don't fake it**: Showing "3 left" when you have 300 is a dark pattern. Customers notice, complain on social media, and lose trust permanently.
- **Don't show stock too early**: "500 in stock" at the start of a flash sale kills urgency. Suppress stock display until the threshold triggers.
- **Don't update manually mid-event**: Manual inventory updates during a live sale are error-prone. Automate where possible.
- **Don't ignore the "sold out" state**: A blank product page after sellout is a missed conversion opportunity. Always redirect to a waitlist or related product.
