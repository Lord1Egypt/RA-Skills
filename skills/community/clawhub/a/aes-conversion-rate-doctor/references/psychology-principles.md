# Conversion Psychology Principles Reference

Ten core psychology principles that govern ecommerce conversion behavior. Each entry includes the principle definition, its ecommerce application, common violations observed in the wild, and a standardized fix pattern.

Use this reference when mapping findings to underlying behavioral mechanisms. Every diagnosis should cite at least one principle by name.

---

## 1. Hick's Law

**Definition:** The time required to make a decision increases logarithmically with the number of choices available. More options lead to longer decision times and higher likelihood of decision avoidance.

**Ecommerce Application:** Every additional choice, field, or step in a conversion flow increases the probability of abandonment. This applies to product variant selection, checkout form fields, payment method presentation, and navigation options on product pages.

**Common Violations:**
- Checkout flows that require account creation before showing guest checkout
- Product pages displaying 15+ variant options without intelligent defaults or filtering
- Payment step showing 8+ payment methods in an unorganized list
- Shipping option presentation with 5+ choices lacking a recommended default
- Modal dialogs that interrupt flow with secondary decisions (newsletter signup, add warranty, etc.)

**Fix Pattern:** Reduce visible choices to 3-5 at each decision point. Use smart defaults to pre-select the most common option. Implement progressive disclosure — show advanced options only when requested. Remove or defer non-essential decisions to post-purchase. Pre-select the most popular shipping and payment options.

---

## 2. Social Proof

**Definition:** People look to the actions and opinions of others to determine correct behavior, especially under uncertainty. The effect strengthens when the "others" are perceived as similar to the decision-maker.

**Ecommerce Application:** Reviews, ratings, purchase counts, "bestseller" badges, and real-time activity indicators reduce purchase uncertainty. Social proof is most effective when placed near the point of decision (adjacent to CTA buttons) and when it includes specific, relatable details.

**Common Violations:**
- Review scores hidden below the fold or behind a tab click
- Displaying review count without the average rating (or vice versa)
- No social proof visible on mobile without scrolling
- Generic testimonials without specificity ("Great product!" provides weak proof)
- Review sections that prominently display negative reviews without context
- Missing social proof at the checkout stage where buyer's remorse peaks

**Fix Pattern:** Display star rating and review count within the above-the-fold product area on all devices. Include 1-2 specific review excerpts near the CTA. Add "X people bought this today/week" counters when volumes support it. Show trust badges and review platform logos (Trustpilot, Google Reviews) at checkout. Ensure the most helpful positive reviews surface first.

---

## 3. Loss Aversion

**Definition:** People feel the pain of losing something approximately twice as strongly as the pleasure of gaining something of equivalent value. Unexpected losses trigger disproportionate negative reactions.

**Ecommerce Application:** Unexpected costs revealed late in the funnel (shipping, taxes, fees) feel like losses and are the leading cause of checkout abandonment. Conversely, framing benefits as "what you'll miss" rather than "what you'll get" increases action.

**Common Violations:**
- Shipping costs revealed only at the payment step
- Service fees or handling charges appearing for the first time in the order summary
- Cart showing a lower subtotal than the final order total without clear explanation
- Removing discount codes or promotional pricing between cart and checkout
- "Limited time" offers with no visible expiration creating suspicion rather than urgency

**Fix Pattern:** Show all costs as early as possible — ideally on the product page or cart. Display a "free shipping at $X" threshold bar. If shipping costs must vary, show an estimate on the product page ("Shipping from $X.XX"). Never add costs between cart review and payment without clear explanation. Frame discounts as "You save $X" to make the gain tangible.

---

## 4. Anchoring

**Definition:** People rely disproportionately on the first piece of information they encounter (the "anchor") when making subsequent judgments. Initial reference points shape perception of value.

**Ecommerce Application:** Price perception is heavily influenced by the first number a shopper sees. MSRP or "compare at" prices, strikethrough pricing, bundle "total value" displays, and per-unit cost breakdowns all serve as anchors that make the actual price feel like a deal.

**Common Violations:**
- Displaying the sale price without showing the original price
- Missing "compare at" or MSRP reference on discounted items
- Bundle pages that show only the bundle price without itemizing individual product values
- Subscription pricing without showing per-unit cost savings vs. one-time purchase
- Price displayed in isolation without context (no competitor comparison, no value framing)

**Fix Pattern:** Always show the reference price alongside the sale price using strikethrough formatting. Display "You save $X (Y%)" calculations. For bundles, itemize individual product values and show total value above the bundle price. For subscriptions, show per-unit cost with comparison to single-purchase pricing. Place the anchor (higher number) visually before the actual price.

---

## 5. Cognitive Load

**Definition:** Working memory has limited capacity. When processing demands exceed capacity, decision quality degrades and people default to the easiest action — which in ecommerce is leaving.

**Ecommerce Application:** Every piece of information, every form field, every visual element on a page consumes cognitive resources. Checkout flows with excessive fields, product pages with dense unformatted text, and cluttered layouts all increase cognitive load beyond what shoppers are willing to invest.

**Common Violations:**
- Checkout forms requesting information not required for the transaction (birthday, company name, fax number)
- Product descriptions as unbroken paragraphs exceeding 200 words
- More than 3 calls-to-action visible simultaneously on a product page
- Inconsistent visual hierarchy where it is unclear what to read or click first
- Requiring users to re-enter information they have already provided
- Error messages that do not specify which field has the problem

**Fix Pattern:** Minimize form fields to only what is essential (name, email, shipping address, payment). Use progressive disclosure — hide optional fields behind "Add" links. Format product descriptions with bullet points, headers, and scannable structure. Establish clear visual hierarchy with one primary CTA. Use inline validation to prevent errors rather than correcting them after submission. Auto-fill where possible (city/state from zip code).

---

## 6. Trust Signals

**Definition:** In the absence of physical interaction, online shoppers rely on visible indicators of credibility, security, and reliability to reduce perceived risk of transaction.

**Ecommerce Application:** Trust signals include SSL indicators, payment provider logos, money-back guarantees, return policy visibility, security badges, BBB ratings, industry certifications, and professional design quality. Their absence or poor placement creates unconscious anxiety that suppresses conversion.

**Common Violations:**
- No visible security badge or SSL indicator near the payment form
- Return and refund policy buried in footer links, not visible during checkout
- Payment provider logos missing from the checkout page
- No guarantee or warranty information on the product page
- Contact information (phone, email, chat) hidden or absent
- Broken images, typos, or outdated copyright years signaling neglect

**Fix Pattern:** Place recognized security badges (Norton, McAfee, PCI compliance) adjacent to the payment form. Display return policy summary (not just a link) on the product page and at checkout. Show accepted payment method logos in the checkout header. Include a money-back guarantee badge near the CTA. Make contact options visible on every page. Maintain professional polish throughout — fix broken elements immediately.

---

## 7. Urgency and Scarcity

**Definition:** People assign greater value to opportunities that are limited in time or availability. Real constraints motivate faster action; manufactured constraints, once detected, destroy trust.

**Ecommerce Application:** Genuine stock counters, sale end dates, limited edition labels, and shipping cutoff times can accelerate purchase decisions. However, fake urgency (perpetual countdown timers, "Only 2 left!" on unlimited digital products) erodes credibility when shoppers notice.

**Common Violations:**
- Countdown timers that reset on page refresh (immediately destroys trust)
- "Only X left!" on products that are clearly not supply-constrained
- "Sale ends soon" without specifying when
- Aggressive urgency on first visit before any relationship is established
- Pop-ups with fake time pressure ("This offer expires in 10 minutes!")

**Fix Pattern:** Use urgency only when the constraint is genuine. Display actual stock levels when inventory is genuinely limited. Show specific sale end dates and times. Use shipping cutoff urgency ("Order within 3h 22m for delivery by Friday") which is always truthful. For scarcity, "Low stock" is more credible than exact numbers for items with fluctuating inventory. Never use timers that reset.

---

## 8. Reciprocity

**Definition:** People feel obligated to return favors. When given something of value, they are more inclined to reciprocate — in ecommerce, by making a purchase or providing information.

**Ecommerce Application:** Free value provided before asking for commitment increases conversion. This includes free shipping thresholds, sample or trial offers, educational content, size guides, detailed comparison tools, and transparent pricing. The key is that the value must be perceived as genuinely helpful, not manipulative.

**Fix Pattern:** Offer free shipping above a threshold displayed prominently. Provide sizing tools, comparison guides, or style quizzes before asking for purchase commitment. Include free samples with orders (and mention this on the product page). Offer free returns to reduce purchase risk. Display helpful content (care instructions, compatibility guides) that demonstrates expertise and builds goodwill.

**Common Violations:**
- Asking for email signup before providing any value
- Gating basic product information behind account creation
- Requiring payment information for a "free trial"
- Pop-ups requesting commitment (newsletter, account) on first page load before the visitor has received any value

---

## 9. Visual Hierarchy

**Definition:** People scan visual layouts in predictable patterns (F-pattern for text, Z-pattern for landing pages). Elements that are larger, higher-contrast, and positioned along scan paths receive disproportionate attention.

**Ecommerce Application:** The CTA button, price, product title, and primary image must fall along natural scan paths. If the add-to-cart button blends into the page, requires scrolling, or competes with equally prominent secondary actions, conversion suffers.

**Common Violations:**
- CTA button color that blends with the page background or other elements
- Multiple buttons of equal visual weight competing for attention (Add to Cart, Add to Wishlist, Compare, Share all the same size and color)
- Critical information (price, availability, shipping estimate) positioned outside natural scan paths
- Product images that are smaller than surrounding text content
- Key information below the fold on mobile with no visual cue to scroll

**Fix Pattern:** Make the primary CTA the most visually prominent element on the page — largest button, highest contrast color, positioned along the natural scan path. Reduce secondary actions to text links or ghost buttons. Place price and key decision information (rating, availability) adjacent to the CTA. Use whitespace to create visual breathing room around the primary action area. Ensure the first mobile viewport contains: image, title, price, rating, and CTA.

---

## 10. Fitts's Law

**Definition:** The time required to move to a target is a function of the distance to the target and the size of the target. Smaller and more distant targets are harder and slower to reach.

**Ecommerce Application:** CTA buttons, form fields, navigation links, and interactive elements must be large enough and positioned close enough to related content to support rapid, error-free interaction — especially on mobile where touch targets replace mouse cursors.

**Common Violations:**
- Add-to-cart button smaller than 44x44px on mobile (Apple's minimum recommended touch target)
- CTA button positioned far from the product information it relates to
- Closely spaced links in the footer causing mis-taps on mobile
- Checkout form fields that are too narrow for comfortable text entry on mobile
- Quantity selectors using tiny +/- buttons instead of a tap-friendly stepper or dropdown
- Close (X) buttons on modals that are too small to tap accurately

**Fix Pattern:** Size all primary CTA buttons at minimum 44x44px on mobile (48x48px preferred). Place the CTA immediately adjacent to the price and product summary. Maintain at least 8px spacing between adjacent tap targets on mobile. Use full-width buttons on mobile checkout forms. Make form fields at least 48px tall with adequate padding. For quantity adjustment, use a stepper with large tap zones or a dropdown instead of tiny buttons.
