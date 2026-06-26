# Cart Recovery Program Audit Checklist

## A. Checkout Friction Analysis (8 items)
- [ ] Checkout funnel drop-off rates measured at each stage (cart, shipping, payment, review)
- [ ] Mobile vs. desktop abandonment rates compared (mobile is typically 10-15% higher)
- [ ] Shipping costs visible before checkout begins (or free shipping threshold clearly displayed)
- [ ] Guest checkout available (no forced account creation)
- [ ] Payment options include at least 3 methods (credit card, PayPal, digital wallet)
- [ ] Checkout loads in under 3 seconds on mobile
- [ ] Form fields minimized (only essential information collected)
- [ ] Progress indicator shows checkout steps remaining

## B. Data Collection & Tracking (7 items)
- [ ] Cart abandonment events tracked with timestamp, products, cart value, and user ID
- [ ] Email capture happens before the checkout page (pop-up, account creation, or newsletter)
- [ ] Abandonment stage recorded (which checkout step they left from)
- [ ] Device type and traffic source captured for each abandonment
- [ ] Customer type flagged (new visitor, returning visitor, previous purchaser)
- [ ] Cart contents and product categories logged for segmentation
- [ ] Real-time conversion tracking connected to suppress recovered customers immediately

## C. Recovery Sequence Setup (9 items)
- [ ] Minimum 3-touch sequence configured across at least 2 channels
- [ ] First touch sends within 60 minutes of abandonment
- [ ] Each touch has a distinct purpose (reminder, social proof, incentive, urgency)
- [ ] Timing between touches appropriate (not more than 1 message per 6 hours)
- [ ] Sequence completes within 5-7 days total
- [ ] Dynamic product content populates from actual cart contents
- [ ] Product images, names, and prices render correctly in all email clients
- [ ] Deep links take the customer directly to their saved cart (not homepage)
- [ ] Sequence stops immediately when customer completes purchase

## D. Segmentation & Personalization (7 items)
- [ ] New vs. returning customers receive different sequences
- [ ] Cart value tiers trigger different incentive levels
- [ ] High-value carts (top 20% by value) receive enhanced sequence (more touches, higher priority)
- [ ] Product category influences message copy and imagery
- [ ] Repeat abandoners (3+ in 30 days) excluded or handled separately
- [ ] Recently purchased customers excluded from discount offers
- [ ] Subject lines include product name or category for relevance

## E. Incentive Strategy (8 items)
- [ ] First touch contains NO discount (reminder only)
- [ ] Incentives escalate through the sequence (free shipping → % off → $ off)
- [ ] Maximum discount cap set per cart value tier
- [ ] Discount codes are unique and single-use (not shareable)
- [ ] Discount codes expire within 24-48 hours of generation
- [ ] Already-discounted products excluded from additional discounts (or capped)
- [ ] Minimum order value set for discount codes to protect margins
- [ ] Discount stacking rules defined (can/cannot combine with other promotions)

## F. Email Quality (8 items)
- [ ] Subject lines are under 50 characters and include product reference
- [ ] A/B test variants prepared for subject lines on highest-volume touches
- [ ] Preview text is customized (not auto-generated from body content)
- [ ] Email renders correctly on top 5 email clients (Gmail, Apple Mail, Outlook, Yahoo, mobile)
- [ ] CTA buttons are prominent, contrasting color, at least 44x44px on mobile
- [ ] Unsubscribe link is visible and functional
- [ ] Sender name is recognizable brand name (not "noreply@")
- [ ] Reply-to address is monitored (customers reply to cart recovery emails)

## G. SMS & Push Compliance (6 items)
- [ ] SMS only sent to contacts with explicit SMS marketing consent
- [ ] SMS includes brand identification and STOP opt-out instructions
- [ ] SMS respects quiet hours (no messages 9pm-9am recipient local time)
- [ ] Push notifications only sent to users who have opted in
- [ ] Maximum 1 SMS and 1 push notification per abandonment sequence
- [ ] SMS deep links tested and working on both iOS and Android

## H. Measurement & Optimization (9 items)
- [ ] Recovery rate tracked (recovered carts / total abandoned carts)
- [ ] Revenue recovered tracked by channel (email, SMS, push)
- [ ] Per-touch metrics monitored (open rate, click rate, conversion rate)
- [ ] Incrementality holdout test running (10% of abandoners receive no recovery messages)
- [ ] Unsubscribe rate monitored per touch (early warning for too-aggressive sequencing)
- [ ] Spam complaint rate tracked (should be under 0.1%)
- [ ] Revenue per email sent calculated (total recovery revenue / total emails sent)
- [ ] Discount cost tracked (total discounts given / total revenue recovered)
- [ ] A/B tests running with sufficient sample size (minimum 1,000 per variant per test)

## I. Ongoing Maintenance (5 items)
- [ ] Product catalog changes reflected in email templates (discontinued products handled)
- [ ] Seasonal messaging variations prepared (holiday, sale events, etc.)
- [ ] Suppression lists cleaned monthly (bounced emails, invalid numbers removed)
- [ ] Recovery sequence performance reviewed weekly during first month, monthly ongoing
- [ ] Discount codes audited for leakage (check coupon-sharing sites monthly)

---

**Total Items: 67**

**Scoring Guide:**
- 60-67 items completed: Comprehensive — recovery program is well-built and actively optimized
- 50-59 items completed: Solid — core recovery working, optimization opportunities remain
- 35-49 items completed: Gaps — recovery likely underperforming due to missing components
- Below 35: Foundation needed — significant setup required before expecting meaningful recovery rates
