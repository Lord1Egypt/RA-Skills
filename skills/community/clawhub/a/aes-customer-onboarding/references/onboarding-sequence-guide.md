# Onboarding Sequence Design Guide

## Core Principles of Post-Purchase Onboarding

### The Adoption Window

The period between delivery and Day 14 post-delivery is the critical adoption window. Research across ecommerce verticals shows that customers who engage with a product within the first 7 days are 3.2x more likely to make a second purchase within 60 days. The onboarding sequence exists to compress time-to-first-use and guide customers through initial adoption barriers.

### The Value-Before-Commerce Rule

Every post-purchase sequence must follow the 70/20/10 content ratio:
- **70% educational and helpful content**: Product tips, usage guides, care instructions, styling ideas, recipes, workout plans — whatever helps the customer get maximum value from their purchase
- **20% social proof and community**: Reviews from similar customers, user-generated content, community features, progress celebrations
- **10% commercial content**: Cross-sell recommendations, repurchase reminders, loyalty program enrollment

Violating this ratio — especially front-loading commercial content — signals to customers that your post-purchase communication is just another sales channel, leading to unsubscribes and brand erosion.

### Event-Based vs. Time-Based Triggers

**Event-based triggers** (recommended) fire messages based on real customer milestones:
- Order placed → immediate confirmation
- Order shipped → tracking + preparation content
- Order delivered → unboxing guide + setup instructions
- First product use detected (app, QR scan, account creation) → reinforcement
- Review submitted → thank you + community invitation
- Repurchase window reached → restock reminder

**Time-based triggers** (fallback) fire on fixed intervals from order date:
- Day 0: Confirmation
- Day 3: Brand story
- Day 7: Product tips (assumes delivery by Day 5)
- Day 14: Review request
- Day 28: Cross-sell

Event-based triggers consistently outperform time-based triggers by 35-45% in click-through rates because they match the customer's actual experience rather than an assumed timeline.

## Sequence Architecture by Product Type

### Simple Consumables (Food, Beauty, Supplements)

**Characteristics:** Low complexity, repeat purchase expected, short adoption cycle
**Sequence length:** 4-5 touchpoints over 21 days
**Primary goal:** Drive reorder before product runs out
**Content focus:** Usage tips, recipes/routines, consumption tracking

**Key timing insight:** Calculate the expected depletion date based on product size and recommended usage frequency. Place the reorder reminder 5-7 days before depletion so it arrives while the customer still has positive product experience (not after they've run out and potentially switched).

### Complex Single Products (Electronics, Equipment, Appliances)

**Characteristics:** High complexity, accessory/upgrade cross-sell, long adoption cycle
**Sequence length:** 7-9 touchpoints over 35 days
**Primary goal:** Ensure product activation and regular use
**Content focus:** Setup guides, feature discovery, troubleshooting, use cases

**Key timing insight:** The biggest dropout moment is between unboxing and first real use. If a customer doesn't activate/use the product within 48 hours of delivery, the probability of return increases by 4x. The Day 1-2 post-delivery touchpoints are the most critical in the entire sequence.

### Multi-Product Systems (Skincare Routines, Wardrobes, Kitchen Sets)

**Characteristics:** Medium-high complexity, products work together, requires habit formation
**Sequence length:** 6-8 touchpoints over 30 days
**Primary goal:** Establish routine usage of the full system
**Content focus:** Step-by-step routines, combination guides, progressive complexity

**Key timing insight:** Introduce products one at a time rather than overwhelming with the full routine. Day 1: Start with the simplest/most familiar product. Day 3-4: Add the second product. Day 7: Introduce the full routine. This progressive approach reduces overwhelm and builds confidence.

### Subscription First Shipments

**Characteristics:** High retention stakes, need to justify ongoing cost, habit formation critical
**Sequence length:** 8-10 touchpoints over the first billing cycle
**Primary goal:** Prevent cancellation before second shipment
**Content focus:** Value reinforcement, usage encouragement, community connection

**Key timing insight:** The highest cancellation risk is in the 48 hours before the second charge. Place a value-summary email 3-4 days before the next billing date showing what they've received, how much they've saved, and what's coming next. This preempts cancellation by reinforcing perceived value.

## Channel Selection Framework

### When to Use Email

- Rich educational content requiring images, formatting, and links
- Product guides and tutorials that customers may reference later
- Cross-sell recommendations with product images and descriptions
- Weekly or bi-weekly digests summarizing multiple topics
- Content the customer might want to save or forward

**Email best practices for onboarding:**
- Keep subject lines under 40 characters for mobile
- Use preview text strategically — it's your second headline
- Single-column layout, 600px max width
- One primary CTA per email (secondary CTAs below the fold only)
- Plain text version for every HTML email

### When to Use SMS

- Time-sensitive delivery updates (shipped, out for delivery, delivered)
- Quick single tips that don't require visual support
- Urgent CTAs (flash sale, almost out of stock)
- Re-engagement for customers who haven't opened emails
- Milestone celebrations (workout streak, usage milestone)

**SMS best practices for onboarding:**
- Maximum 160 characters for a single segment (no split messages)
- Always identify the brand in the first 3 words
- Include opt-out language per compliance requirements
- Respect quiet hours: 9am-9pm in the customer's local timezone
- Maximum 4 SMS messages in any 30-day onboarding sequence

### When to Use Push Notifications

- App-based products requiring in-app actions
- Gentle habit reminders (daily routine, workout schedule)
- Real-time engagement prompts (new content available, friend activity)
- Low-friction micro-actions (rate this, quick poll, streak reminder)

### When to Use In-Package Inserts

- First-use setup instructions (always — this is the highest-visibility touchpoint)
- QR codes linking to video tutorials or exclusive content
- Loyalty program enrollment cards
- Referral program introduction with shareable codes
- Care/maintenance quick-reference cards

## Timing Psychology

### The Reciprocity Window (Days 0-3 Post-Delivery)

Customers feel positive toward the brand immediately after receiving their order. This is the best time for:
- Asking for app downloads or account creation
- Requesting social follows
- Enrolling in loyalty programs
- Gathering product preferences for personalization

### The Education Window (Days 1-10 Post-Delivery)

Customers are most receptive to learning about their product during the first 10 days. Attention and engagement drop sharply after this period. Front-load your most important educational content here.

### The Validation Window (Days 10-21 Post-Delivery)

Customers seek validation that they made the right choice. This is the optimal time for:
- Sharing reviews from similar customers
- Showing before/after results or success stories
- Presenting usage statistics ("You've used X 12 times this week!")
- Requesting reviews (they now have informed opinions)

### The Commercial Window (Days 21-35 Post-Delivery)

Customers who have adopted the product are now open to expanding their relationship with the brand. This is when cross-sell, upsell, and repurchase messages perform best.

## Suppression and Safety Rules

### Mandatory Suppression Triggers

Always suppress remaining onboarding messages when:
- Customer initiates a return or exchange
- Customer contacts support with a complaint (hold for 7 days, then resume with care message)
- Customer has already made a second purchase (skip to loyalty/VIP track)
- Customer unsubscribes from any channel (respect across all channels)
- Customer marks any message as spam (suppress all non-transactional)

### Frequency Caps

- **Email:** Maximum 3 onboarding emails per week, with at least 48 hours between sends
- **SMS:** Maximum 1 per week for onboarding, never more than 4 in the full sequence
- **Push:** Maximum 1 per day, with a weekly cap of 5
- **Combined across channels:** Never more than 2 messages on the same day from any combination of channels
