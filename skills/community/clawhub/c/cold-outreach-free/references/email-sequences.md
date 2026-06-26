# Email Sequences Reference

Full template library, subject line bank, personalization signals, and A/B testing guide.

---

## Email 1 Templates — 5 Variants

Each variant targets a different pain point or industry. Adapt the [brackets] to your ICP.

---

### Variant 1: Hiring Signal (B2B SaaS)

**Subject:** outbound question

Hi [First Name],

Noticed [Company] is hiring SDRs — usually means you're scaling outbound. Most teams at that stage hit a wall with sequencing: manual follow-ups fall through, replies don't get categorized, and the pipeline looks messier than it should.

We built three n8n workflows that automate the sourcing-to-reply pipeline — no paid APIs, runs on Gmail and Google Sheets.

Worth a look?

[Name]

---

### Variant 2: Founder/Head of Sales at Small Team

**Subject:** cold outreach question

Hi [First Name],

Running outbound for a [10–50 person] company usually means you're doing it yourself — which means leads fall through when things get busy.

I put together an outreach system (3 n8n workflows) that runs the sourcing, sequencing, and reply routing automatically. Free tools, no subscriptions. Takes 15 minutes to set up.

Relevant to what you're working on?

[Name]

---

### Variant 3: Agency Targeting Clients

**Subject:** outreach for [Company]

Hi [First Name],

[Company] does [service] — the clients you'd want are almost always reachable via cold email, but building the automation to do it consistently is the hard part.

We have a pre-built outreach system (Apollo → Gmail → reply handler) that agencies are using to run campaigns for clients. $19, one-time, imports into n8n in minutes.

Worth a quick look?

[Name]

---

### Variant 4: Funding Signal

**Subject:** congrats on the raise

Hi [First Name],

Congrats on the [seed/Series A] — growth stage usually means outbound becomes the priority fast.

Most teams at this stage spend 2–3 weeks wiring together Apollo, Gmail, and a sequencer before sending a single email. We compressed that into 3 n8n workflows you import and configure in 15 minutes.

Relevant to where you're at?

[Name]

---

### Variant 5: Tech Stack Signal (HubSpot/CRM users)

**Subject:** outbound stack question

Hi [First Name],

I see [Company] is on HubSpot — most sales teams using it for inbound are starting to add a cold outreach layer on top.

We built an outbound pipeline (lead sourcing → 3-touch sequence → reply handler) that runs on free tools and feeds cleanly into any CRM. No subscriptions, one-time setup.

Worth 10 minutes?

[Name]

---

## Email 2 Templates — 5 Variants (Follow-Up)

Sent Day 3 to non-responders. Always acknowledge you're following up — one phrase, not a paragraph.

---

### Variant 1: Proof-Based

**Subject:** re: outbound question

Following up briefly.

One of our users set this up in a Saturday afternoon and had their first sequence running by Monday morning — 40 leads, 3-touch sequence, fully automated. They closed one client within 3 weeks.

Worth a quick conversation?

[Name]

---

### Variant 2: Problem Reframe

**Subject:** re: [previous subject]

One more angle on this:

The problem isn't usually sending emails — it's that follow-ups break down. Someone replies, the sequence keeps firing. Someone unsubscribes, they get emailed again. The reply handler in this system solves that automatically.

If any of that sounds familiar, it's worth 15 minutes.

[Name]

---

### Variant 3: Question-Based

**Subject:** quick question

Different angle: how are you currently handling follow-ups when someone doesn't reply?

Most teams either drop the ball on touch 2 and 3, or manually track who to follow up with. Either way it's either lost pipeline or busywork.

That's the specific problem this solves.

[Name]

---

### Variant 4: Stat-Based

**Subject:** reply rate numbers

Cold email reply rates average 1–3% for generic sequences. Teams running personalized 3-touch sequences with proper timing and reply detection hit 5–15%.

The difference is mostly in the follow-up logic and knowing when to stop. That's what Workflows 2 and 3 handle.

Worth a look?

[Name]

---

### Variant 5: Story-Based

**Subject:** re: outreach question

Short version of why I built this:

Spent two weeks wiring Apollo → n8n → Gmail → Google Sheets from scratch. 15 hours. Lots of broken node connections. Now it's packaged as three importable JSON files.

$19 to skip the 15-hour weekend. Let me know if it's relevant.

[Name]

---

## Email 3 Templates — 3 Close Variants

Sent Day 7. Final touch. Close the loop, leave the door open.

---

### Variant 1: The Clean Close

**Subject:** last note

Last email on this — didn't want to leave it hanging.

If the timing's off or it's just not relevant, no problem. If you want to revisit later, just reply "later" and I'll reach out in 90 days.

[Name]

---

### Variant 2: The Soft CTA Close

**Subject:** re: [previous subject]

Last note from me.

If you ever do want to add an automated outreach layer without building from scratch, the system is at [link]. It'll be there.

Hope the outbound is going well.

[Name]

---

### Variant 3: The Permission Close

**Subject:** closing the loop

I'll stop here — three emails is enough.

One last thing: if timing changes and outbound becomes a priority, reply any time. Happy to pick this back up.

[Name]

---

## Subject Line Bank — 20 Tested Lines

Organized by format. Use lowercase. Keep it 2–4 words. Avoid spam triggers (FREE, URGENT, !!!).

### Question format
1. `outbound question`
2. `quick question`
3. `cold outreach question`
4. `outreach stack question`
5. `how are you doing follow-ups?`

### Intrigue / observation format
6. `noticed something`
7. `saw you're hiring`
8. `re: your outbound`
9. `congrats on the raise`
10. `saw your post`

### Name-drop / referral-style
11. `[Mutual name] suggested I reach out` *(only if true)*
12. `[Company] → [Your Company]`
13. `from [Your Company]`

### Internal-looking
14. `quick note`
15. `last note`
16. `following up`
17. `re: [previous subject]`
18. `closing the loop`
19. `one more thing`
20. `outbound`

**Rules:**
- Never use all-caps
- Never use exclamation marks in subject lines
- Never use "opportunity," "partnership," or "synergy"
- Test two at a time: split first 20 leads 10/10, measure opens, scale the winner

---

## Personalization Signal List — 10 Triggers

For every email, identify one signal. Write the opening line to connect it to the problem you solve.

| Signal | Example opening line |
|--------|---------------------|
| LinkedIn post in last 30 days | "Your post on [topic] caught my eye — you clearly think about [problem] a lot." |
| Hiring for outbound/SDR role | "Noticed [Company] is hiring SDRs — usually means outbound is becoming a priority." |
| Recent funding | "Congrats on the [round] — growth stage usually brings outbound to the front of the queue." |
| New product launch | "Saw [Company] just launched [product] — new launches usually need a pipeline to match." |
| Company in the news | "Saw [Company] in [publication] — interesting timing to reach out." |
| Tech stack match | "I see you're on [tool] — most teams using it for [use case] eventually add [adjacent thing]." |
| Podcast/speaking appearance | "Heard you on [podcast] — your take on [topic] is exactly the problem we're solving." |
| Job change (new role) | "Congrats on the new role at [Company] — first 90 days in a new sales seat usually means building the pipeline from scratch." |
| Company blog post | "Read your post on [topic] — the [specific point] you made maps directly to what we're building." |
| Competitor is a customer | "We work with [similar company] — thought the context might be useful." *(verify this is true)* |

**Rule:** The personalization must logically connect to your offer. If you remove the opening line and the email still makes sense, it's decorative personalization. Make it structural.

---

## A/B Testing Guide

Test one variable at a time. Keep everything else identical.

### What to test (in priority order)

1. **Subject line** — biggest impact on opens. Test two variants on 20 leads each.
2. **Email 1 opening line** — biggest impact on replies. Test different personalization angles.
3. **CTA phrasing** — "Worth a look?" vs "15 minutes this week?" vs "Relevant?"
4. **Email length** — 5 sentences vs 7 sentences
5. **Send timing** — Tuesday 9 AM vs Thursday 2 PM

### How to interpret results

- **Open rate difference < 5%:** not meaningful. Run more sends before concluding.
- **Open rate difference > 10%:** meaningful. Scale the winner.
- **Reply rate difference > 2%:** meaningful. Understand *why* before scaling.

### Sample size minimums

- Subject line test: 20 per variant (40 total) minimum before reading results
- Copy test: 30 per variant (60 total) minimum
- Never kill a variant based on fewer than 15 sends

### What not to test

- Don't test two things at once. You won't know which change caused the result.
- Don't test on your best leads first. Use median-quality leads for testing, best leads for your proven winner.
- Don't run A/B tests longer than 2 weeks — market conditions shift.
