# Channel Timing Reference Card

## Optimal Send Times by Channel

### Email Send Time Windows

| Day of Week | Best Window | Good Window | Avoid |
|-------------|-----------|-------------|-------|
| Monday | 10am-12pm | 2pm-4pm | Before 9am (inbox overload) |
| Tuesday | 10am-11am | 7pm-8pm | 12pm-2pm (lunch) |
| Wednesday | 9am-11am | 7pm-9pm | 3pm-5pm |
| Thursday | 10am-12pm | 7pm-8pm | After 9pm |
| Friday | 9am-10am | — | After 2pm (weekend mode) |
| Saturday | 10am-12pm | — | Before 10am, after 6pm |
| Sunday | 4pm-7pm | 10am-12pm | Before 10am |

**Notes:**
- All times are in the customer's local timezone
- Transactional emails (order confirmation, shipping) send immediately regardless of time
- Educational content performs best Tuesday-Thursday mid-morning
- Cross-sell and promotional content performs best Tuesday-Wednesday

### SMS Send Time Windows

| Message Type | Optimal Window | Acceptable Window | Hard Boundaries |
|-------------|---------------|-------------------|----------------|
| Delivery alert | Immediately on event | — | Never suppress (transactional) |
| Quick tip | 11am-1pm | 9am-3pm | Never before 9am or after 8pm |
| Review request | 10am-12pm Sat/Sun | 6pm-8pm weekdays | Never Monday morning |
| Reorder reminder | 10am-11am Tue-Thu | 2pm-4pm | Never Friday-Sunday |

**Compliance requirements:**
- TCPA: Only send between 8am-9pm local time (some states 8am-8pm)
- All SMS must include opt-out (Reply STOP to unsubscribe)
- Transactional SMS exempt from marketing time restrictions
- Maintain separate consent records for marketing vs. transactional SMS

### Push Notification Timing

| Notification Type | Optimal Time | Frequency Cap |
|------------------|-------------|---------------|
| Setup reminder | 7pm-8pm (evening, time to set up) | Once, then stop |
| Usage reminder | Matches established habit time | 1x daily max |
| Content alert | 12pm-1pm or 6pm-7pm | 3x weekly max |
| Achievement | Immediately on trigger | No cap (event-driven) |

## Channel Selection Matrix

### By Message Type

| Message Purpose | Primary Channel | Secondary Channel | Avoid |
|----------------|----------------|-------------------|-------|
| Order confirmation | Email | SMS (short version) | Push (not installed yet) |
| Shipping update | SMS | Email | Push |
| Delivery confirmation | SMS | Push | Email (too slow) |
| Setup/unboxing guide | Email + In-package insert | Push (if app) | SMS (too long) |
| Product education | Email | Push (app content link) | SMS |
| Quick tip | SMS | Push | Email (too heavy) |
| Check-in / survey | Email | SMS (1-question) | Push |
| Review request | Email | SMS (if high-value) | Push |
| Cross-sell | Email | — | SMS (too commercial) |
| Reorder reminder | Email | SMS (if consumable) | Push |

### By Customer Segment

| Segment | Email | SMS | Push | Insert |
|---------|-------|-----|------|--------|
| Gen Z (18-25) | Secondary | Primary | Primary (if app) | QR-code focused |
| Millennial (26-40) | Primary | Secondary | Secondary | Visual, scannable |
| Gen X (41-56) | Primary | Transactional only | Rarely | Detailed instructions |
| Boomer (57+) | Primary | Avoid for marketing | Avoid | Detailed, large print |

### By Product Price Point

| Price Range | Recommended Touches | Channel Mix |
|------------|-------------------|-------------|
| Under $30 | 3-4 touchpoints | Email only + insert |
| $30-$75 | 5-6 touchpoints | Email + SMS delivery alerts + insert |
| $75-$150 | 6-8 touchpoints | Email + SMS + insert + optional push |
| $150-$300 | 7-9 touchpoints | Full multi-channel + video content |
| $300+ | 8-10 touchpoints | Full multi-channel + personal outreach option |

## Frequency Management

### Maximum Frequency Caps

| Channel | Per Day | Per Week | Per 30-Day Sequence | Notes |
|---------|---------|----------|---------------------|-------|
| Email | 1 (exceptions: order day can have 2) | 3 | 10 | 48-hour gap between educational emails |
| SMS | 1 | 1 (marketing) | 4 | Transactional unlimited |
| Push | 2 | 5 | 15 | Only if app installed |
| All combined | 2 | 5 | 18 | Never email + SMS + push same day |

### Spacing Rules

- **Minimum 4 hours** between any two messages on the same day (except transactional)
- **Minimum 48 hours** between two emails with similar content themes
- **Minimum 72 hours** between two SMS marketing messages
- **No commercial messages** within 24 hours of a transactional message (don't piggyback)
- **Pause all marketing** for 7 days after a support ticket is opened

### Cross-Channel Orchestration

When the same information needs to go through multiple channels, stagger the delivery:

1. **SMS first** (if urgent/time-sensitive) — immediate
2. **Push second** (if app action needed) — 30 minutes after SMS
3. **Email third** (for detail and reference) — 2-4 hours after SMS

**De-duplication rules:**
- If customer opens email within 2 hours, suppress the follow-up SMS on same topic
- If customer completes CTA from any channel, suppress same-topic messages on other channels
- If customer clicks SMS link, mark email on same topic as "supplementary" (lower priority in inbox)

## Message Length Guidelines

| Channel | Ideal Length | Maximum Length | Format |
|---------|-------------|---------------|--------|
| Email subject | 25-40 chars | 60 chars | Question or benefit statement |
| Email preview text | 40-80 chars | 100 chars | Complement (don't repeat) subject |
| Email body | 150-250 words | 400 words | Scannable sections with one CTA |
| SMS | 80-120 chars | 160 chars (1 segment) | Brand name + value + CTA |
| Push title | 20-40 chars | 50 chars | Action-oriented |
| Push body | 40-80 chars | 100 chars | Single clear message |
| In-package headline | 5-8 words | 10 words | Imperative (Scan to start) |

## Timezone and Localization

### Timezone Handling

- Store customer timezone at order time (derived from shipping address)
- All marketing sends scheduled in customer's local timezone
- Transactional sends fire immediately regardless of timezone
- If timezone unknown, default to the timezone of the shipping address state/country
- For international orders, respect country-specific marketing hours regulations

### Language Considerations

- Match onboarding language to the storefront language used at purchase
- If multi-language support isn't available, default to English with simple, clear phrasing
- Avoid idioms, slang, and cultural references that don't translate
- Date formats: Use the customer's locale (MM/DD/YYYY for US, DD/MM/YYYY for EU/UK)
- Currency: Always show in the currency of original purchase
