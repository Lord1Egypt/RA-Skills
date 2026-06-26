# Email Sequence Templates — Funnel Revenue Engine

Ready-to-import sequences for Brevo (or any ESP).
The agent selects the sequence matching the active business model,
fills all `[PLACEHOLDERS]`, and saves the result to
`/workspace/funnel/active_funnels/[slug]/email_sequence.md`.

**Platform setup note:**
Brevo → Automation → Workflows → "Contact enters a list" trigger
→ Add emails with the delays below → activate.

---

## B2C SUBSCRIPTION — 7-Day Free Trial Sequence

**Trigger:** contact signs up for free trial
**Goal:** convert trial user to paid subscriber by day 7

---

### Email 1 — Immediate (Day 0) — Welcome + First Value

```
Subject: Welcome — here's what happens next

Hi [first_name],

You're in.

Here's what to expect this week:

[DAY 1]: [First piece of value — the thing that made them sign up]
[DAY 3]: [How it works / deeper explanation]
[DAY 5]: [Real result or case study]
[DAY 7]: An offer to continue.

To get started right now:
→ [ONBOARDING_LINK or first value delivery]

Any question — reply to this email. I read every one.

— [SENDER_NAME]

P.S. Your free trial ends in 7 days. No charge before then.
```

---

### Email 2 — Day 2 — How It Works

```
Subject: How [PRODUCT_NAME] actually works

Hi [first_name],

Quick breakdown of how this works:

[STEP_1 — ex: "Every Monday at 8am you receive the weekly signal"]
[STEP_2 — ex: "The signal includes: asset, entry, target, stop-loss"]
[STEP_3 — ex: "You execute in your broker in < 5 minutes"]

That's it.

No complicated strategy. No hours of chart reading.
[DIFFERENTIATOR — what makes it simple/unique]

Here's [example / sample / preview]:
→ [SAMPLE_LINK]

— [SENDER_NAME]
```

---

### Email 3 — Day 4 — Real Result

```
Subject: [SPECIFIC_RESULT — ex: "+€127 last week. Here's the trade."]

Hi [first_name],

Last week's result:
[RESULT_WITH_NUMBERS — ex: "+3.2% on BTC long. Entry: 81,400. Exit: 84,000."]

[1-2 sentences explaining what led to the signal]

This is what [PRODUCT_NAME] does every week.

[SCREENSHOT_DESCRIPTION or link to proof]

Your free trial ends in 3 days.
If you want to keep receiving these: [UPGRADE_LINK]

— [SENDER_NAME]
```

---

### Email 4 — Day 6 — Objection Handling

```
Subject: The most common question I get

Hi [first_name],

Before your trial ends tomorrow, I want to address the
thing most people are thinking:

"[MAIN_OBJECTION — ex: 'What if a signal loses?']"

[HONEST_ANSWER — ex: "It happens. Not every trade wins.
My win rate is 68% over 47 trades. The average winner
is +4.1%. The average loser is -1.8%.
Over 6 months, the math works."]

[OPTIONAL: link to full track record]

Tomorrow is the last day of your trial.
Continue for €[PRICE]/month: [UPGRADE_LINK]

— [SENDER_NAME]

P.S. [GUARANTEE reminder — ex: "7-day refund if you're not satisfied."]
```

---

### Email 5 — Day 7 — Last Day Offer

```
Subject: Your trial ends today

Hi [first_name],

Today is the last day of your free trial.

What you get if you continue:
✅ [BENEFIT_1]
✅ [BENEFIT_2]
✅ [BENEFIT_3]
✅ [GUARANTEE]

€[PRICE]/month. Cancel anytime.

→ [UPGRADE_LINK]

If you have any question before deciding, reply here.
I respond within 2 hours.

— [SENDER_NAME]
```

---

## B2B SAAS — 8-Touchpoint Sequence (50 days)

**Trigger:** prospect replies to cold email or requests demo
**Goal:** book a call and close within 14-21 days

---

### Email 1 — Day 0 — Signal-Based Outreach

```
Subject: [SIGNAL — ex: "saw your post on [topic]"]

Hi [first_name],

[SPECIFIC_SIGNAL — ex: "I read your post about [topic] on LinkedIn.
The point about [specific detail] is exactly what we see with
our clients in [sector]."]

We help [ICP_DESCRIPTION] to [RESULT_IN_ONE_LINE].

[SOCIAL_PROOF — ex: "We've done this for [N] companies including [name]."]

15 minutes this week to see if there's a fit?

[SENDER_NAME]
[COMPANY]
```

---

### Email 2 — Day 3 — New Value

```
Subject: [STAT or INSIGHT about their situation]

Hi [first_name],

Quick follow-up.

[SURPRISING_STAT about their sector or situation]

[1-2 sentences connecting this to their specific challenge]

How do you handle [SPECIFIC_PROBLEM] today?

[SENDER_NAME]
```

---

### Email 3 — Day 7 — Different Angle

```
Subject: [CASE_STUDY_TEASER — ex: "how [similar company] did X"]

Hi [first_name],

[BRIEF_CASE_STUDY — ex: "A company similar to yours was facing
[PAIN]. In 8 weeks they [RESULT]. Here's what changed: [brief]."]

Worth a 15-minute call to explore if the same applies to you?

[SENDER_NAME]
```

---

### Email 4 — Day 12 — Direct Question

```
Subject: quick question

Hi [first_name],

Is [MAIN_PAIN] a priority for you right now?

[SENDER_NAME]
```

---

### Email 5 — Day 18 — Free Resource

```
Subject: [RESOURCE_NAME] — for you

Hi [first_name],

I put together [RESOURCE — ex: "a 5-step checklist for [topic]"].
No strings attached.

→ [RESOURCE_LINK]

Hope it's useful.

[SENDER_NAME]
```

---

### Email 6 — Day 25 — Breakup

```
Subject: closing the loop

Hi [first_name],

I'm going to stop reaching out after this.

If [MAIN_PROBLEM] becomes a priority, I'm here.

If the timing is just off, I understand completely.

Either way — [RESOURCE] is yours to keep.

[SENDER_NAME]
```

---

## TRADING SIGNALS — Free Signal to VIP

**Trigger:** subscriber receives first free signal
**Goal:** convert to VIP paid subscriber

---

### Email 1 — Immediate — First Free Signal

```
Subject: Your first signal is ready

Hi [first_name],

Here's this week's signal:

Asset:     [ASSET]
Direction: [LONG/SHORT]
Entry:     [PRICE]
Target:    [TARGET]  (+[X]%)
Stop:      [STOP]    (-[X]%)

[1-2 sentences: why this trade / what the setup is]

Track record: [LINK_TO_RESULTS]

Next signal: [DAY], [TIME].

— [SENDER_NAME]

P.S. VIP subscribers get [ADDITIONAL_BENEFIT — ex: "3 signals/week
+ real-time alerts"]. More info: [VIP_LINK]
```

---

### Email 2 — Day 3 — Result Update

```
Subject: Signal update: [+X% / still open / closed]

Hi [first_name],

Update on last [DAY]'s signal:

[STATUS — ex: "Target hit: +3.2% ✅" or "Still open — holding"]

[BRIEF_ANALYSIS — 2-3 sentences about what happened]

Next free signal: [DAY].

VIP members already got [ADDITIONAL_SIGNAL] this week.
Join here: [VIP_LINK] — €[PRICE]/month.

— [SENDER_NAME]
```

---

## CONTENT / NEWSLETTER — Lead Magnet to Paid

**Trigger:** subscriber downloads lead magnet
**Goal:** convert to paid subscriber or product buyer

---

### Email 1 — Immediate — Deliver the Lead Magnet

```
Subject: Here's your [LEAD_MAGNET_NAME]

Hi [first_name],

Your [LEAD_MAGNET_NAME] is here:
→ [DOWNLOAD_LINK]

Quick preview of what's inside:
- [KEY_POINT_1]
- [KEY_POINT_2]
- [KEY_POINT_3]

Tomorrow I'll share [NEXT_VALUE — ex: "the most common mistake
people make when applying this"].

— [SENDER_NAME]
```

---

### Email 2 — Day 2 — Deeper Value

```
Subject: [INSIGHT related to lead magnet topic]

Hi [first_name],

[VALUABLE_INSIGHT — 3-4 sentences, something they wouldn't find easily]

[LINK_TO_RELATED_CONTENT if relevant]

Reply and tell me: what's your biggest challenge with [topic]?
I read every response.

— [SENDER_NAME]
```

---

### Email 3 — Day 4 — Best Content Example

```
Subject: [example of what they'll get as a subscriber]

Hi [first_name],

Here's a sample of what [PUBLICATION_NAME] subscribers
receive every [FREQUENCY]:

[ACTUAL_SAMPLE_CONTENT — 150-300 words of your best stuff]

If this is valuable to you, the full [FREQUENCY] edition is
[PRICE]/month: [SUBSCRIPTION_LINK]

— [SENDER_NAME]
```

---

### Email 4 — Day 6 — Social Proof

```
Subject: "[SUBSCRIBER_QUOTE]"

Hi [first_name],

[SUBSCRIBER_NAME], a [ICP_DESCRIPTION], told me last week:

"[TESTIMONIAL — specific, with result]"

[1 sentence connecting their result to what you offer]

[SUBSCRIPTION_LINK] — €[PRICE]/month.
[GUARANTEE]

— [SENDER_NAME]
```

---

### Email 5 — Day 7 — Offer

```
Subject: last day — [OFFER_OR_CONTEXT]

Hi [first_name],

[DIRECT_OFFER]:

[PRODUCT_NAME] — €[PRICE]/month
✅ [BENEFIT_1]
✅ [BENEFIT_2]
✅ [BENEFIT_3]
[GUARANTEE]

→ [SUBSCRIPTION_LINK]

If it's not for you — no problem.
You keep the [LEAD_MAGNET] either way.

— [SENDER_NAME]
```
