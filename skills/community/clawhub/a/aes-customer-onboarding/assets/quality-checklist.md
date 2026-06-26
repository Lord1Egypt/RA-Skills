# Customer Onboarding Quality Checklist

Use this checklist before launching any post-purchase onboarding sequence. Every item should be verified and checked off.

---

## Sequence Strategy (7 items)

- [ ] Sequence length matches product complexity (3-4 for simple, 6-8 for complex)
- [ ] All touchpoints tied to event triggers (delivery, activation) not fixed dates
- [ ] Content follows 70/20/10 ratio (education / social proof / commercial)
- [ ] No commercial messages appear before Day 14 post-delivery
- [ ] Review request placed at Day 10-14 post-delivery (not on delivery day)
- [ ] Cross-sell recommendations based on actual product purchased, not generic
- [ ] Sequence ends with clear transition to ongoing lifecycle marketing

## Content Quality (8 items)

- [ ] Every message has a single clear purpose and one primary CTA
- [ ] Subject lines under 40 characters for mobile optimization
- [ ] Preview text complements (not repeats) subject line
- [ ] Educational content is product-specific, not generic brand messaging
- [ ] Visual assets included: product photos, how-to images, or UGC
- [ ] Tone is consistent across all touchpoints and matches brand voice
- [ ] No grammar, spelling, or formatting errors in any message
- [ ] Plain text version exists for every HTML email

## Personalization (6 items)

- [ ] Customer first name personalized in greeting
- [ ] Product name and/or category referenced in relevant messages
- [ ] Estimated delivery date included in pre-delivery messages
- [ ] Content segmented by product type (if multiple product lines)
- [ ] Acquisition channel influences tone/content where applicable
- [ ] Dynamic content blocks render correctly for all segments

## Channel Configuration (7 items)

- [ ] Email platform automation flow built and tested end-to-end
- [ ] SMS messages comply with TCPA (timing, consent, opt-out)
- [ ] Push notifications configured with correct deep links
- [ ] In-package insert design finalized and sent to fulfillment
- [ ] Delivery webhook integrated and firing correctly
- [ ] Cross-channel frequency caps enforced (no more than 2 messages/day)
- [ ] Timezone detection working for send-time localization

## Timing and Triggers (6 items)

- [ ] Order confirmation fires immediately (under 60 seconds)
- [ ] Shipping notification triggers from actual carrier webhook
- [ ] Delivery confirmation pulls from carrier data, not estimated date
- [ ] Post-delivery messages use confirmed delivery date as Day 0
- [ ] Minimum 48-hour gap between educational emails enforced
- [ ] SMS quiet hours respected (9am-9pm customer local time)

## Suppression and Safety (7 items)

- [ ] Return/refund initiated → all onboarding messages suppressed
- [ ] Support ticket opened → marketing paused for 7 days
- [ ] Second purchase made → skip to loyalty track
- [ ] Unsubscribe from any channel → respected across all channels
- [ ] Spam complaint → suppress all non-transactional messages
- [ ] Customer already reviewed → suppress review request
- [ ] Deceased/closed account → full suppression

## Technical Setup (5 items)

- [ ] All dynamic variables (name, product, dates) render correctly
- [ ] Links in all messages point to correct destinations and are tracked
- [ ] UTM parameters added to all links for analytics attribution
- [ ] Mobile rendering tested across iOS Mail, Gmail, Outlook
- [ ] SMS short links resolve correctly and are branded

## Metrics and Tracking (6 items)

- [ ] Per-touchpoint metrics defined (open rate, CTR, conversion)
- [ ] Sequence-level KPIs established (repurchase rate, return rate, NPS)
- [ ] Control group set up for A/B comparison (10-15% holdout)
- [ ] Attribution model configured for cross-channel touchpoints
- [ ] Dashboard or report template built for weekly monitoring
- [ ] First A/B test planned and scheduled for Week 2 of launch

## Compliance and Legal (5 items)

- [ ] CAN-SPAM compliance: physical address, unsubscribe link in all emails
- [ ] TCPA compliance: SMS consent verified, opt-out in every message
- [ ] GDPR compliance: lawful basis for processing, easy data access/deletion (if applicable)
- [ ] CCPA compliance: privacy notice, opt-out of sale (if applicable)
- [ ] All claims in content are accurate and substantiated (no false promises)

---

**Total items: 57**
**Minimum passing score: 52/57 (91%)**
**Critical items (must pass): All Suppression and Safety items, all Compliance items**
