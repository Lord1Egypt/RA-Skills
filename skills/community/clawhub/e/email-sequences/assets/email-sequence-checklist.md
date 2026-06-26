# Email Sequence Quality Checklist

Use this checklist before delivering any Email Sequences output. Items marked REQUIRED must pass before delivery. Items marked RECOMMENDED represent best practices that significantly improve performance.

---

## Category 1 — Sequence Architecture (REQUIRED)

- [ ] Campaign type is clearly identified (abandoned cart / post-purchase / win-back / welcome / seasonal / loyalty)
- [ ] Number of emails and send timing for each is specified
- [ ] Behavioral trigger or schedule is defined for Email 1
- [ ] Exit condition (purchase, opt-out) is defined and applies to all emails in sequence
- [ ] Re-entry delay is specified after sequence completes without conversion
- [ ] Sequence fits within CTIA / CAN-SPAM guidance for campaign type

---

## Category 2 — Suppression Logic (REQUIRED)

- [ ] Purchase suppression is configured — sequence stops on conversion
- [ ] Opt-out suppression is configured — sequence stops and subscriber is added to permanent suppression list
- [ ] Hard bounce suppression is noted
- [ ] Frequency cap with other active sequences is defined
- [ ] Win-back sequences: does not target subscribers who purchased in last 30 days
- [ ] Abandoned cart: active-on-site suppression noted (don't trigger while user is browsing)

---

## Category 3 — Subject Line and Preview Text (REQUIRED)

- [ ] Every email has a subject line and preview text pair
- [ ] Subject lines are under 50 characters (mobile-optimized)
- [ ] Preview text is 85–100 characters and extends subject line with new information
- [ ] Preview text is not blank or a duplicate of the subject line
- [ ] No spam trigger words in subject lines (FREE, YOU WON, CLICK HERE, GUARANTEED)
- [ ] No ALL CAPS subject lines or excessive punctuation (max 1 exclamation point)

---

## Category 4 — Body Copy (REQUIRED)

- [ ] Each email has a clear hook in the first sentence
- [ ] Offer (if present) is specific — dollar amount, percentage, or free shipping (not vague "savings")
- [ ] Single CTA per email — one action verb, one destination
- [ ] Merge tag placeholders are noted: [FIRST_NAME], [PRODUCT_NAME], [ORDER_NUMBER], etc.
- [ ] No transactional message contains promotional content (discount codes, shop CTAs)
- [ ] Promotional emails reference consent path (express written consent)

---

## Category 5 — Segmentation (RECOMMENDED)

- [ ] Target segment is identified for the sequence
- [ ] Sequence is not addressed to "all subscribers" without qualification
- [ ] New vs. repeat customer variants are noted (or a single flow with conditional logic)
- [ ] VIP segment handling is addressed (separate flow or conditional block)
- [ ] Win-back: lapsed threshold is defined (90d / 180d / 365d based on category)
- [ ] Welcome: overlap with broadcast list cadence is addressed

---

## Category 6 — Discount and Offer Logic (RECOMMENDED)

- [ ] Discount escalation is logical: Email 1 no offer → Email 2 soft → Email 3 stronger (or no offer at all)
- [ ] Discount is not present in Email 1 of abandoned cart sequence
- [ ] Discount expiry is specific (not "limited time" — use exact date/time)
- [ ] Offer type matches product margin profile (high-AOV → free shipping preferred over % off)
- [ ] Unique coupon codes are used (not shared codes that can be shared publicly)

---

## Category 7 — Platform Configuration (RECOMMENDED)

- [ ] ESP platform is identified in output
- [ ] Trigger event name matches platform's actual metric name
- [ ] Flow exit event is specified using platform's terminology
- [ ] Smart Sending / quiet period configuration is noted
- [ ] A/B test setup instructions are included for key emails
- [ ] Send time optimization settings are addressed
- [ ] Transactional vs. promotional split is noted for platforms that require it (Mailchimp Transactional)

---

## Category 8 — A/B Test Coverage (RECOMMENDED)

- [ ] At least one email in the sequence has A/B subject line variants
- [ ] Variant uses a materially different hook angle (not just one word changed)
- [ ] Variable being tested is explicitly stated (urgency / curiosity / personalization / offer vs. no offer)
- [ ] Winner determination criteria is noted (open rate / click rate / revenue per recipient)
- [ ] Both variants meet the same compliance requirements

---

## Category 9 — Timing and Cadence (RECOMMENDED)

- [ ] Send times are within 8am–9pm recipient local time (per CAN-SPAM guidance)
- [ ] Abandoned cart Email 1 is not faster than 45–60 minutes post-trigger (to avoid "too fast" opt-outs)
- [ ] Win-back sequence does not exceed 2–3 emails per quarter per subscriber
- [ ] Post-purchase cross-sell delay is sufficient for delivery to have occurred
- [ ] Seasonal sequence includes last-chance email with explicit deadline

---

## Category 10 — Flags and Disclaimers (REQUIRED when applicable)

- [ ] Any compliance flags are noted (GDPR for EU subscribers, CASL for Canadian subscribers)
- [ ] Win-back sequences: CASL implied consent expiry (2-year limit) noted if Canadian subscribers involved
- [ ] "Not legal advice" disclaimer present for compliance-heavy outputs
- [ ] Platform-specific setup notes are accurate for current platform version
- [ ] Any assumed brand voice or segment definitions are flagged as assumptions

---

**Checklist score guide:**
- All REQUIRED items pass + 80%+ RECOMMENDED items pass → Deliver output
- Any REQUIRED item fails → Fix before delivering
- Less than 60% of RECOMMENDED items pass → Note gaps explicitly in output
