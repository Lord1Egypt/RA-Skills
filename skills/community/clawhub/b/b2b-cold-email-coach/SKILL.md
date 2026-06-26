---
name: b2b-cold-email-coach
description: Coach B2B founders, SDRs, agencies, and freelancers on writing cold email that gets opened, replied to, and converted to meetings — without burning domains or hitting spam. Diagnoses why open rates are low, why no one replies, why deliverability is broken. Knows the 2026 deliverability landscape: Google/Yahoo bulk-sender rules, DMARC/DKIM/SPF, domain warming, Smartlead/Instantly playbooks, the offer-message-targeting framework. Adapts advice for cold outbound to SMB, mid-market, and enterprise. Use when asked to write cold email, structure a sequence, fix low reply rates, set up a domain for cold sending, audit deliverability, build a target list, or migrate from Apollo/Outreach. Triggers on "cold email", "cold outreach", "cold outbound", "smartlead", "instantly", "apollo", "deliverability", "spam folder", "open rate", "reply rate", "sales sequence", "sdr playbook", "outbound prospecting".
metadata:
  tags: ["cold-email", "outbound", "b2b", "sales", "sdr", "lead-gen", "deliverability", "outreach"]
---

# B2B Cold Email Coach

Coach a sender on the actual mechanics of cold email that works in 2026 — past the dead playbooks ("personalize with their company news!"), past the spam-filter cliffs, into the version where reply rates are 4–8% and meetings book themselves.

## Usage

**Basic invocation:**
> Why are my open rates 30%?
> Rewrite this cold email: [paste]
> Set up domains for cold sending
> Build a 4-step sequence
> Diagnose: 0 replies in 800 sends

**With context:**
> Selling AI dev tools to SaaS engineering teams. $79/seat/mo. SDR sending 200 emails/day from main domain.
> Boutique branding agency. Cold email to founders of $5M-$50M brands. 1.5% reply rate.
> Founder-led outbound, B2B SaaS, $1k MRR, want to scale outbound to $5k.
> Was on Apollo, deliverability tanked, considering moving to Smartlead.

The coach diagnoses the four levers (offer, message, targeting, infrastructure) and rebuilds the system.

## The Four Levers

Cold email failures usually trace to one of four issues. Diagnose in order:

### 1. Targeting (most often broken)

If your offer doesn't fit the recipient, no copy can save it. Audit:

- **ICP definition:** specific role, specific company size, specific industry, specific stack/maturity stage. Generic ICP = generic results.
- **Pain triggers:** companies actively experiencing the pain (just funded? hiring this role? changed leadership?). Triggers > demographics.
- **Buyer vs decision maker:** are you emailing the person who actually buys, or the person who hears the pitch and forwards?
- **List quality:** scraped lists have 30% bad data; verified lists (NeverBounce, ZeroBounce) have <5%.

Symptoms of bad targeting:

- Replies are "not the right person"
- Replies are "not for us"
- 0% open rate suggests bad emails (target unreachable) more than bad subject lines

### 2. Offer (often unclear)

Your email is selling the meeting, not the product. The offer should be:

- **Specific:** "I help [ICP] do [specific outcome] in [timeframe]"
- **Differentiated:** what's unique about your approach
- **Risk-reversed:** "free [thing]," "no commitment," "pilot for 30 days"
- **Quantified:** "increased X by Y for company Z"

Bad offer signals: "see if we're a fit," "thoughts?", "interested in saving money?"

### 3. Message (the copy)

When targeting and offer are right, message becomes pure execution. See "Cold email anatomy" below.

### 4. Infrastructure (subtle but critical)

In 2026, one wrong setup ruins everything else:

- **From-domain:** never your main domain. Use look-alike (yourdomain.io if main is yourdomain.com).
- **Mailbox setup:** SPF, DKIM, DMARC must be configured. DMARC at `p=none` minimum, ideally `p=quarantine`.
- **Domain warming:** new domain needs 4–6 weeks of warming before high-volume cold.
- **Volume per mailbox:** max 30 cold emails/day per mailbox in 2026. Higher = spam.
- **Multiple mailboxes:** to scale, you need 5+ mailboxes across 2+ domains.
- **Tools:** Smartlead, Instantly, Lemlist, Apollo (declining), Reply.io.

Symptoms of broken infrastructure:

- Open rates < 30% (deliverability is your problem, not subject lines)
- Replies say "found this in spam"
- Sudden drop in opens after a "successful" week (domain reputation tanked)

## Cold Email Anatomy (the only template you need)

```
Subject: [Specific, low-key]

Hi [first name],

[Opening: 1 sentence that proves you're targeting them specifically — a pain
trigger, observation, or relevant connection]

[Body: 1-2 sentences that connect their context to your offer]

[CTA: 1 specific question with a clear yes/no, or a low-friction next step]

[Sign-off]
[Name]
[Company URL]
```

**Length:** 50–80 words for first email. Longer = lower reply.

**Subject line rules:**

- 4–8 words
- Lowercase or sentence case (NOT Title Case)
- No spam words ("free," "discount," "limited time")
- Specific is better than clever
- Examples: "quick question on [topic]", "saw you're hiring [role]", "for [company]"

## Sequence Design

A single email rarely works. Multi-touch sequences are standard.

**Standard 5-touch sequence:**

```
Touch 1 (Day 0): Cold intro, primary value prop
Touch 2 (Day 3): Different angle (case study, specific result)
Touch 3 (Day 7): Different format (loom video, P.S. with tip, audit offer)
Touch 4 (Day 14): "Bumping this up" — short, casual
Touch 5 (Day 21): Break-up email ("I'll stop following up unless I hear back")
```

**Sequence rules:**

- Each touch must add value, not just "checking in"
- Vary the angle (problem-focused, outcome-focused, social proof, low-effort offer)
- Reference prior emails sparingly ("following up on the email about X")
- Stop after 5 touches max — beyond that, you're harassing

**Reply rate by touch (typical):**

- Touch 1: 2–4%
- Touch 2: +1–2% (cumulative)
- Touch 3: +1–2%
- Touch 4: +0.5–1%
- Touch 5: +0.5–1%
- Total: 5–9% reply across full sequence

## Personalization (the Right Kind)

**Wrong personalization:** "I noticed your company [boilerplate fact from website]."

**Right personalization:** specific to their role, situation, or trigger.

**Personalization tiers:**

1. **List-level** (everyone gets it): same email; ICP fit
2. **Segment-level** (small variations): "For SaaS founders" vs "For agency owners"
3. **First-line custom:** unique opener per email (Snipping & Smartwriter automate this); requires domain + LLM cost
4. **Manual research:** 100% manual; for executive ICP only

**Effort vs value:**

- Mass with no personalization: 1–2% reply
- Segment-level: 2–4% reply
- First-line: 3–6% reply
- Manual research (premium): 8–15% reply

Match effort to deal size. $5k deal: segment-level. $50k+: manual.

## Domain Strategy and Warming

The 2026 reality: your main domain is sacred. Cold sending = lookalike domains.

**Buy 2–4 lookalike domains:**

- yourbrand.io
- get.yourbrand
- yourbrandhq.com
- tryyourbrand.com

**Each domain:**

- Set up SPF, DKIM, DMARC properly
- Custom MX records pointing to a clean ESP (Google Workspace or Microsoft 365)
- Buy "warmup" service (Smartlead, Instantly, Warmbox) for 4–6 weeks
- Send 5 → 10 → 20 → 30 emails/day during warmup, gradually increasing

**Warmup metrics to track:**

- Inbox placement % (should be >85% before going to cold)
- Spam folder % (<10%)
- Reply opens to seeded warmup messages

## Deliverability Diagnostics

If open rates are low, the issue is almost always deliverability, not subject lines.

**Check (in order):**

1. SPF, DKIM, DMARC — use mxtoolbox.com to verify
2. Domain age — <30 days = will be flagged
3. Volume ramp — sending 200/day from new domain = instant spam
4. Spam-trap hits — if your list has spam traps, your domain is on a blocklist
5. Content keywords — heavy formatting, links, attachments, "Free!" / "$$$"
6. Engagement metrics — Google/Yahoo penalize low-engagement domains
7. Recent complaints — even 0.3% spam complaints tank reputation

**Recovery from a blacklist:**

- Stop all cold sending immediately
- Remove domain from current cold flow
- Wait 30+ days
- Investigate root cause (list quality, volume, content)
- Restart with new lookalike domain; old one may not recover

## Tools (2026 Landscape)

| Tool | Cost | Best for |
|---|---|---|
| **Smartlead** | $39+/mo per mailbox | Most cold senders; best inbox placement |
| **Instantly** | $37+/mo per workspace | Slightly different UX, similar capability |
| **Lemlist** | $59+/mo | Personalization-heavy, smaller volume |
| **Reply.io** | $60+/mo | Multi-channel (email + LinkedIn) |
| **Apollo** | $49+/mo | Built-in data; deliverability declining |
| **Outreach.io / Salesloft** | enterprise | Inside-sales teams, mid-market+ |

**Recommendation by stage:**

- Founder-led outbound: Smartlead
- 2–10 SDRs: Smartlead or Instantly
- Mid-market sales team: Outreach or Salesloft
- Heavy personalization: Lemlist or custom + Smartlead

## List Building

Sources for B2B contact lists:

- **Apollo / ZoomInfo / Lusha:** built-in databases. Fresh ~70%, accuracy ~70–85%.
- **Sales Navigator + scraping:** more current; manual or via tools (PhantomBuster).
- **CrunchBase / PitchBook:** for funding-stage triggers.
- **Verified-list services:** UseArtemis, Wiza, etc.
- **Buy lists:** dangerous; usually old/spam-trap-laden. Avoid.

**Verification (mandatory):**

- Run every list through NeverBounce, ZeroBounce, or Bouncer
- Discard "risky" / "unknown" tier
- Aim for <3% bounce rate when sending

## Common Diagnoses

### "30% open rate, 0 replies"

- Open rate is being inflated by Apple Mail Privacy Protection (counts opens that don't happen)
- Real engaged opens are likely 10–15%
- Subject lines may be fine; deliverability hidden
- Body or offer is the problem

Fix: ignore Apple-MPP-inflated opens; track unique-replies and meetings booked instead; rewrite body using anatomy above; check deliverability.

### "0 replies in 800 sends"

- Deliverability dead (in spam)
- Targeting wildly wrong
- Offer doesn't resonate
- Domain blacklisted

Fix: check deliverability first (test from another inbox; check inbox placement); if deliverability is OK, audit targeting and offer.

### "Started strong, opens dropped over time"

Classic domain reputation collapse:
- Volume increased too fast
- Spam traps in list
- Low engagement (your list isn't replying or marking as not-spam)
- Content triggered filters

Fix: cool down 14–30 days; switch to fresh domain; smaller volume per mailbox; cleaner list.

### "Replies are negative ('not interested', 'unsubscribe', etc.)"

This is normal. ~30% of replies are negative. What matters is:
- Positive reply rate (1–3% of sends)
- Meeting book rate (40–60% of positive replies)
- Show-up rate (60–80% of meetings)
- Conversion-to-paying (5–15% of meetings)

If positives are 0%, see "0 replies" diagnosis above.

## Output Format

The coach returns:

1. **Funnel diagnosis** — where you're losing
2. **Targeting audit** — ICP fit and trigger quality
3. **Offer rewrite** — what value prop should be
4. **Email rewrite** — paste-ready, anatomy-correct
5. **Sequence plan** — 5 touches with day spacing
6. **Infrastructure plan** — domains, mailboxes, warmup
7. **List sourcing plan** — how to build pipeline
8. **30-day plan** — what to ship this month
