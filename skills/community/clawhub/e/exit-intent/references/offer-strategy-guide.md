# Exit-Intent Offer Strategy — Reference Guide

## Offer Segmentation Framework

The most effective exit-intent strategies don't use a single offer for all visitors. Instead, they segment by three dimensions and serve the offer most likely to convert without over-discounting.

### Dimension 1: Cart Context

**Has items in cart (cart page abandoner)**
These visitors showed the highest purchase intent. They selected products, navigated to the cart, and are about to leave. The friction is usually shipping cost, total price shock, or comparison shopping.

Best offers:
- Free shipping (if not already offered)
- Free shipping upgrade (standard → express)
- Small percentage discount (5-10%)
- "Your items are selling fast" social proof (no discount needed)
- Payment plan / BNPL reminder

**Has items in cart (product page abandoner)**
They added to cart earlier but are now browsing other products and preparing to leave. They may be comparison shopping or losing interest.

Best offers:
- Bundle discount ("Add [complementary product] and save 15%")
- Cart reminder with product images
- Limited-time free shipping threshold ("Add $X more for free shipping")

**No cart (browsing abandoner)**
Never showed purchase intent. Discounting is wasteful. Focus on list building.

Best offers:
- Email signup for future discount
- "Get notified when this drops in price" alert signup
- Quiz or style guide (engagement, not transaction)
- Content download (guide, lookbook)

### Dimension 2: Cart Value

| Cart Value | Margin Headroom | Recommended Offer Type |
|---|---|---|
| Above 2× AOV | High (can afford discount) | Percentage discount (10-15%) or gift with purchase |
| 1-2× AOV | Medium | Free shipping or small fixed discount ($5-10) |
| Below AOV | Low (protect margins) | Free shipping threshold or email capture |
| Empty | None | Email/SMS list signup only |

### Dimension 3: Visitor Type

**New visitor (first session)**
- No brand relationship yet
- Higher discount tolerance (acquisition cost justifies it)
- Welcome offer: 10-15% off first order
- Always capture email even if they don't convert immediately

**Returning visitor (2+ sessions, no purchase)**
- Familiar with brand but hasn't committed
- May be comparison shopping
- Targeted offer: free shipping or time-limited discount
- Show social proof (reviews, user-generated content)

**Previous purchaser**
- Already converted — DO NOT show generic discount
- Exception: loyalty program enrollment or referral offer
- Best to exclude from exit popups entirely
- Use post-purchase email flows instead

## Offer Value Calibration

### The Incrementality Test

Not every popup conversion is incremental. Many visitors who click a popup discount would have purchased anyway (they were just moving the mouse to navigate within the site). To measure true incrementality:

1. Run a control group (10-20% of qualifying traffic) that never sees a popup
2. Compare conversion rate: popup group vs. control
3. Calculate: `Incremental Revenue = (Popup Group CR - Control CR) × Popup Impressions × AOV`
4. Compare against: `Discount Cost = Popup Conversions × Average Discount Given`
5. True ROI = Incremental Revenue - Discount Cost

### Offer Escalation Strategy

If you have enough traffic, consider an escalation approach:
1. First visit: No discount, just social proof ("Join 50,000 happy customers")
2. Second visit (if they return): Free shipping offer
3. Third visit: 10% discount
4. Fourth visit: 15% discount with urgency ("Offer expires in 24 hours")

This prevents first-visit discount anchoring while progressively converting harder-to-close visitors.

### Margin Protection Rules

Before setting any discount level, calculate:
- `Max Discount = (Gross Margin % - Target Net Margin %) / (1 - Target Net Margin %)`
- Example: 65% gross margin, want 30% net → Max discount = (0.65 - 0.30) / (1 - 0.30) = 50%. But in practice, stay well under this.
- Rule of thumb: Exit popup discounts should be ≤ 1/3 of your gross margin to remain profitable
- Always calculate dollar impact: "10% off $85 AOV = $8.50 per order × estimated conversion volume"

## Offer Format Best Practices

### Percentage vs. Dollar-Off vs. Free Shipping

| Format | Best When | Example |
|---|---|---|
| Percentage off | AOV > $75, consistent margin | "15% off your order" |
| Dollar off | Low AOV, makes the discount feel bigger | "$5 off orders over $30" |
| Free shipping | Shipping is a known friction point | "Free shipping on this order" |
| Free gift | High-margin brand, want to avoid discount perception | "Free sample set with your order" |
| BOGO/Bundle | Inventory clearance, AOV lift goal | "Buy 2, get 1 free" |

### Code vs. Auto-Apply

- **Auto-apply** (code added to cart automatically when CTA clicked): Higher conversion, 20-30% more usage than code copy
- **Code display** ("Use code EXIT15 at checkout"): Lower conversion but creates urgency if code has expiry
- **Recommendation:** Auto-apply whenever your platform supports it. Removes friction entirely.

### Urgency Mechanisms

Real urgency only — never fake:
- ✅ "This code expires when you close this page" (if technically true)
- ✅ "Only 3 left in stock" (if real inventory data)
- ✅ "Price increases tomorrow" (if real scheduled price change)
- ❌ Fake countdown timers that reset on page refresh
- ❌ "Only X left!" when inventory is unlimited
- ❌ "Offer expires in 5 minutes" with arbitrary deadline

Fake urgency erodes trust and may violate consumer protection laws (FTC, ASA, EU Consumer Rights Directive).
