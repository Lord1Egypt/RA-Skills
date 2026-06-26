# Email Best Practices — Framework

Loaded when the conversation involves designing, evaluating, or troubleshooting email content. This is what a senior email marketer brings to the table that a generic agent doesn't.

## Subject lines

### What works (account-calibrated)

Read `~/.activecampaign-skill/state.json` for `baselines.avg_subject_line_length` and `baselines.top_performing_subjects`. Recommend in-line with what's worked for THIS account, not industry generics.

If state.json isn't available, defaults:
- 30-50 characters performs best on most accounts
- Questions outperform statements for most B2B (your account may differ — check history)
- Personalization tokens (`{{first_name}}`) lift opens 14-26% on average but lose effect with overuse
- Numbers in subject lines outperform alphabetical content for "list" emails ("5 reasons" > "Five reasons")
- Emoji impact varies wildly by audience — check `history.jsonl` for past results

### What doesn't work

- ALL CAPS (spam-trigger; deliverability hit)
- Multiple exclamation points (same)
- "Free" / "Act now" / "Limited time" / "Click here" / "$$$$" — spam-trigger words
- Subject lines that don't match the email body content (kills trust + click rate)
- Length over 60 characters (truncated on mobile — most opens are mobile)

### Personalization beyond first name

- Most-recent-product-viewed (requires ecommerce data in AC)
- Last-conversion context ("Loved the Widget Pro? See the Mark II")
- Tier/plan ("As a Pro customer, you get early access") — use custom field values
- Geography (timezone, weather, local events) — but only if you have actual data

## Preheader text

The preheader is the line of text after the subject that previews in the inbox.

- 40-90 characters
- Should NOT repeat the subject line — extend it
- Don't waste it with "View this email in your browser" (default fallback)
- Set explicitly via the `preview_text` parameter when creating campaigns

## Body content

### Length

- Newsletter: 200-500 words
- Welcome email: 100-200 words
- Re-engagement: 50-150 words (low ask, easy out)
- Sales follow-up: 50-100 words (one ask, no fluff)
- Long-form announcement: 300-800 words MAX, with TL;DR at top

### Structure that works

1. Greeting (personalized)
2. Hook (one sentence — answers "why am I reading this?")
3. Body (the substance, with one core idea)
4. Clear single CTA (one button, not multiple)
5. Sign-off (real human name, real email reply-to)

Multiple CTAs in one email reduce action by 30-40% on average. One email = one ask.

### Mobile-first rendering

- 60-70% of opens are mobile
- Buttons should be ≥44px tall (Apple's minimum touch target)
- Text size ≥14px body, ≥18px headings
- Single column layout
- No tables for layout (use CSS, fall back gracefully)
- Dark mode: test inverted colors, especially logos

### Accessibility

- Alt text on every image (also helps deliverability — clients that block images by default)
- Real text, not images of text
- Sufficient color contrast (WCAG AA minimum: 4.5:1 for body)
- Logical heading order (h1 → h2 → h3)
- Don't rely on color alone to convey meaning

## CTAs

### What works

- Action-first verbs ("Get the report" > "Click here")
- First-person framing ("Send me my report" > "Get your report") — counterintuitive but tests well
- Specific over generic ("Book a 15-min demo" > "Learn more")
- Single prominent button, not buried link

### Button design

- Bright, brand-aligned color (high contrast against background)
- Border-radius 4-8px (not rounded pill, not sharp rectangle)
- Generous padding (16px vertical, 32px horizontal minimum)
- Centered or left-aligned, not right
- Standalone (white space around it)

## Send time

### Use account baselines, not generic advice

Read `state.json` for `baselines.best_send_window_utc` and `baselines.best_send_dow`. These are computed from THIS account's last 90 days.

If state.json isn't available:
- Tuesday/Wednesday/Thursday outperform Monday and Friday on most B2B accounts
- 9-11am local time and 1-3pm local time are typical peaks
- Sunday evening (6-9pm) is rising for B2C
- Avoid sending Friday after 2pm (lowest engagement window)
- Account for recipient timezone if list spans regions (consider AC's timezone-aware send)

### When to break the pattern

- Time-sensitive content (event reminder) — send 24-48h before
- Transactional-feeling content (receipt, password) — immediate
- Re-engagement of dormants — try an unconventional time; they're not opening normal sends anyway
- Holiday windows — adjust by 1-2 days; office holidays vary

## Frequency

### The right cadence varies by audience

- B2B SaaS prospect: 1-2 / week MAX
- B2B SaaS customer: 1-3 / month for product news, ad-hoc for events
- B2C ecommerce: 2-4 / week is common; engaged segments tolerate more
- News/content: daily can work IF subscribers chose it
- Onboarding: 4-7 emails over first 30 days, then drop to maintenance

### Watch for fatigue signals

- Open rate decay over time (15%+ drop in 90 days = fatigue)
- Unsubscribe rate climbing (>0.5% per send is concerning)
- Engagement concentration in top 20% (long tail not engaging)

If you see fatigue, the answer is segment more (send to engaged subset only) or send less (drop frequency by 30-50%) or both. Sending more rarely fixes fatigue.

## Spam trigger checklist (pre-send)

Before any send, verify:

- [ ] No spam-trigger words in subject (free!!!, act now, $$$, "you've won")
- [ ] No ALL CAPS in subject or first line
- [ ] No more than 1 exclamation in subject
- [ ] Image-to-text ratio < 40% (more text than image)
- [ ] Physical address in footer (CAN-SPAM)
- [ ] Working unsubscribe link (one-click, no login required)
- [ ] Reply-to is a real monitored mailbox
- [ ] From-name is consistent with prior sends (sender reputation)
- [ ] Preheader is set (not default fallback)
- [ ] All merge tags resolve (test send with empty fields)
- [ ] All links work (no 404s, no missing UTM params)

## Deliverability hygiene

### Domain reputation signals

- SPF, DKIM, DMARC all aligned — verify with external tools (MXToolbox, Google Postmaster Tools)
- BIMI record (optional, but helps Gmail logo display)
- Sending domain matches reply-to domain
- Subdomain isolation (use `mail.yourco.com` for marketing, not the root)

### List hygiene

- Remove hard bounces immediately (AC does this automatically)
- Remove soft bounces after 3-5 consecutive bounces
- Remove never-engaged contacts after 6 months (run `scripts/audit_list_health.py`)
- Honor unsubscribes within 10 days (CAN-SPAM)
- Use double opt-in for new subscribers (better long-term deliverability)

### When deliverability drops

Common causes in priority order:
1. Sudden volume increase without warm-up → throttle, slow ramp
2. New sending domain not warmed up → start at 100/day, double daily
3. Engagement rate dropping → tighten audience to engaged subset only
4. List quality eroding → remove dormants, drop bought lists
5. Authentication failure → re-verify SPF/DKIM/DMARC

**Note:** Domain-level deliverability data (inbox placement, sender reputation scores) is not available via the AC API. Use Google Postmaster Tools, MXToolbox, or your ESP's deliverability dashboard in the AC UI for this data.

`scripts/audit_list_health.py` catches problems 3, 4, and 5 using bounce logs and engagement proxies.

## What this skill won't do

- Generate copy that sounds like the user without samples (always ask for past examples first)
- Promise specific deliverability rates (too many variables outside the platform)
- Recommend buying lists (don't, ever — kills sender reputation)
- Recommend dark patterns (pre-checked opt-ins, hidden unsubscribes) — not just unethical, illegal under GDPR

## Related files

- `recipes/welcome-series.md` — template-driven welcome flow
- `recipes/list-health-audit.md` — full list diagnostics
- `frameworks/segmentation-theory.md` — who to send to
- `scripts/audit_list_health.py` — runs the list health audit
