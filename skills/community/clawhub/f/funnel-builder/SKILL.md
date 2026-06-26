---
name: funnel-builder
description: >
  Builds complete multi-channel revenue funnels adapted to any business model.
  Combines proven frameworks from elite operators: Yomi Denzel's viral top-of-funnel
  and deadline conversion system, Antoine Blanco's C4 business method (niche → offer → content → book → close → deliver) and Growth
  Operator model, and Andrew Tate's affiliate army and ticket ladder strategy.
  The agent detects the right niche, builds the full funnel architecture,
  writes the offer, sequences the emails, and maps every reconversion channel.
  Use when launching a new offer, rebuilding a funnel that doesn't convert,
  detecting a profitable niche, or setting up multi-channel retargeting.
version: 1.0.0
author: Wesley Armando (Georges Andronescu)
license: MIT
metadata:
  openclaw:
    emoji: "🚀"
    security_level: L1
    always: false
    required_paths:
      read:
        - /workspace/funnel/config.json
        - /workspace/funnel/active/
        - /workspace/.learnings/LEARNINGS.md
      write:
        - /workspace/funnel/config.json
        - /workspace/funnel/active/
        - /workspace/.learnings/LEARNINGS.md
        - /workspace/AUDIT.md
    network_behavior:
      makes_requests: true
      request_targets:
        - https://www.reddit.com (public read — niche research, no auth)
        - https://x.com (public read — niche signals, no auth)
        - https://www.youtube.com (public read — niche validation, no auth)
        - https://api.telegram.org (Telegram Bot API — requires TELEGRAM_BOT_TOKEN)
      uses_agent_telegram: true
    requires.env:
      - TELEGRAM_BOT_TOKEN
      - TELEGRAM_CHAT_ID
    requires:
      skills:
        - acquisition-master
        - content-creator
      optional_skills:
        - wesley-web-operator
        - virtual-desktop
---

# Funnel Builder — Multi-Channel Conversion Architecture

> "The money is not in the product. It's in the system that sells it." — Operator principle

A funnel is not a page. A funnel is not an email sequence.
A funnel is the **complete system** that takes a stranger
and turns them into a paying customer — automatically,
on multiple channels, at every stage of their journey.

This skill builds that system.

---

## What the Agent Understands About Funnels

Before building anything, the agent internalizes these truths:

```
TRUTH 1 — Most people won't buy the first time.
  The average purchase requires 7-12 touchpoints.
  A single landing page is not a funnel. It's a hope.
  A funnel is what happens across all the touchpoints.

TRUTH 2 — The top of the funnel determines everything.
  Yomi Denzel filled his funnel with 320,000 people in 5 days.
  Not because his offer was better — because his top-of-funnel was massive.
  Funnel quality × Funnel volume = Revenue.
  You need both.

TRUTH 3 — Non-buyers are your biggest asset.
  80% of leads don't buy immediately.
  They're not lost — they're just not ready.
  The system that converts them later is where the real money lives.
  Yomi does this with his webinaire live 2-3x/year.
  Tate does this with his affiliate army.

TRUTH 4 — The ticket ladder multiplies LTV.
  Tate: Free content → $50/month → $8,000 one-time
  Yomi: Free formation → €1,497 paid formation
  Blanco: Free content → €497 program → €3,000+ high-ticket
  One customer who ascends the ladder = 20x the revenue of one sale.

TRUTH 5 — Multi-channel beats single-channel every time.
  One platform can ban you overnight.
  One email sequence can land in spam.
  The system must exist on 3+ channels simultaneously —
  so when one fails, two others keep running.
```

---

## PHASE 1 — NICHE DETECTION

Before building the funnel, the agent validates the niche.
A funnel for a bad niche is a fast way to waste time and money.

### The 4 Niche Criteria (Agent checks all 4)

```
CRITERION 1 — Pain is real and urgent
  → People are actively searching for a solution RIGHT NOW
  → Not a "nice to have" — a "need to fix"
  → Test: would someone pull out their card at 11pm to solve this?

CRITERION 2 — Market can pay
  → The ICP has money and is already spending it on solutions
  → Competitors exist and are profitable (good sign — validates market)
  → Price point is sustainable (avoid "I'll pay €9 max" markets)

CRITERION 3 — You have an edge
  → A unique angle, result, mechanism, or story
  → Not "I'm better" — "I'm different in a specific way"
  → The 1 thing nobody else in this niche is saying

CRITERION 4 — Scalable via content
  → The niche has a large content-consuming audience
  → YouTube / Twitter / Reddit / TikTok searches return active communities
  → Organic content can build the top of the funnel without paid ads
```

### Niche Detection Process

```
STEP 1 — Scan with agent-shark-mindset
  → What signals are trending in the target domain?
  → What problems are people publicly complaining about?
  → What are the top reddit threads, Twitter discussions, YouTube comments?

STEP 2 — Check competitors
  → Who is already selling to this ICP?
  → What price points are working?
  → What's missing in their offer? (your positioning angle)

STEP 3 — Validate with the 3 questions
  Q1: "Would someone pay €97/month to solve this?" → Yes/No
  Q2: "Can I reach 1,000 of these people organically?" → Yes/No
  Q3: "Does this ICP already spend money on similar things?" → Yes/No
  If all 3 = Yes → valid niche → proceed to funnel build
  If any = No → adjust niche or ICP before building
```

---

## PHASE 2 — OFFER ARCHITECTURE

The offer is the engine. Everything else is the vehicle.
A bad offer with great marketing still fails.
A great offer with mediocre marketing can still win.

### The Grand Slam Offer Framework (Hormozi)

The agent builds every offer with these 5 components:

```
1. DREAM OUTCOME
   What the customer actually wants (not what you sell)
   → "€5,000/month from my laptop" not "access to trading signals"
   → "3 B2B clients in 30 days" not "outreach automation"
   Frame the outcome, not the mechanism.

2. PERCEIVED LIKELIHOOD OF ACHIEVEMENT
   Why will it work for THEM specifically?
   → Social proof: "312 people already did this"
   → Specificity: "Works for [specific profile] in [specific context]"
   → Guarantee: removes the risk of trying

3. TIME TO RESULT
   How fast do they get the outcome?
   → "In the first 7 days" beats "over time"
   → First win must come fast — it builds commitment
   → Show the quick win in the funnel (free value that works immediately)

4. EFFORT & SACRIFICE
   What do they NOT have to do?
   → "Without quitting your job"
   → "Without cold calling"
   → "Without needing a technical background"
   Remove the obstacles they fear.

5. PRICE ANCHORING
   Position price against the cost of the problem — not the cost of alternatives
   → "The problem costs you €800/month. This costs €97/month."
   → Never compare to competitors. Compare to the pain.
```

### The Ticket Ladder — 3 Levels Minimum

```
LEVEL 1 — FREE ENTRY (top of funnel)
  Goal: maximum volume, zero friction
  Format: lead magnet / free signal / free mini-formation / free tool
  What it does: proves value before asking for money
  Yomi model: free YouTube formation (hours of real value)
  Tate model: free content clips (viral, affiliates distribute)
  Blanco model: free organic content (daily posting, zero ads)

LEVEL 2 — CORE OFFER (main conversion)
  Goal: first paying customer, recurring if possible
  Format: subscription / course / community / service
  Price range: €47-497/month or €297-1,997 one-time
  Conversion mechanism: deadline / webinar / free trial expiry

LEVEL 3 — HIGH TICKET (LTV maximizer)
  Goal: 10x the revenue per customer
  Format: mentoring / done-for-you / mastermind / war room
  Price range: €1,000-10,000+
  Access: by application or invitation only (creates perceived exclusivity)
  Rule: never promote this before the customer has had a win at Level 2
```

---

## PHASE 3 — THE YOMI FUNNEL MODEL

Yomi's system is a free formation that leads to a paid one, with a 3-day deadline. Those who don't buy within the deadline are converted later via live webinars 2-3 times per year with a 50% promotional offer.

The agent applies this model:

```
YOMI CONVERSION SYSTEM:

STEP 1 — Massive top-of-funnel content
  Platform: YouTube primary + Instagram + TikTok
  Content: genuine, high-value, long-form
  Rule: give away what others charge for — it builds massive trust
  Volume: consistency beats virality (daily or 3x/week minimum)

STEP 2 — Free formation (lead magnet at scale)
  Not a checklist. Not a PDF. A real mini-formation.
  3-5 hours of content that actually solves a real problem.
  Capture email at the beginning — gate the next lesson
  This is the traffic-to-lead conversion mechanism.

STEP 3 — Paid offer with hard deadline
  After the free formation → present the full paid offer
  Deadline: 72 hours maximum
  Urgency: real (price increase, bonuses removed, cohort closes)
  Conversion rate target: 2-5% of free formation subscribers

STEP 4 — The reconversion system (where most funnels fail)
  Everyone who didn't buy in 72 hours goes into:
  → Nurture sequence (weekly email value, no pitch for 30 days)
  → Live webinar 2x/year (replay available for 48h only)
  → Webinar offer: 50% discount + urgency + new testimonials
  → This alone can double total revenue from the same traffic
```

---

## PHASE 4 — ANTOINE BLANCO'S C4 METHOD

The C4 is not a sales script. It's a complete business operating system.
6 steps, executed in strict order. Skip one → the system breaks.

```
C1 — CHOISIR SA NICHE
  3 primary markets: Santé / Argent / Relations
  Sub-niche: specific enough that one person reads it and thinks "this is for me"
  Validation: urgent pain + market can pay + competition exists + your angle

C2 — CRÉER SON OFFRE (Grand Slam Hormozi)
  Promise + mechanism + timeline + guarantee + price anchored to the PROBLEM cost

C3 — CRÉER DU CONTENU
  1 post/day, organic first, zero ad spend to start
  Formula: hook (result/claim) + value (real info) + CTA (DM/link)
  Never pitch in content. Educate → they come to you.

C4 — BOOKER DES APPELS
  Content → link in bio → landing page → application form → booking calendar
  Tools 2026:
  → systeme.io     : all-in-one (funnel + email + booking + member area) — FREE up to 2K contacts
  → Calendly       : simple booking, automatic reminders, free plan
  → iClosed        : AI qualification for high-ticket (€2K+ offers), filters non-buyers
  Application form filters tire-kickers BEFORE they reach your calendar.

C5 — CLOSER LES APPELS (20-30 min max)
  Open → Discovery → Solution → Close
  "Based on what you told me, [offer] gets you [result]. €[price]. Ready to start today?"
  Option: delegate to a closer (15-25% commission) via iClosed marketplace

C6 — DÉLIVRER LES RÉSULTATS
  systeme.io member area: course hosting (unlimited video, free)
  Skool/Discord: community (reduces support, creates organic proof)
  Onboarding sequence: 7 emails, automatic, starts immediately after purchase
  Happy client = testimonial = next funnel's proof
```

**The C4 Tool Stack (2026):**
```
systeme.io    → everything (funnel + email + booking + course) — start here
Calendly      → booking fallback or standalone
iClosed       → high-ticket qualification (€2K+)
Stripe        → payment processing
CapCut        → short-form video (free)
SubMagic      → automated subtitles for clips
Make / N8N    → cross-tool automation
Micro-entreprise → guichet-entreprises.fr (free, 10 min) — register before first payment
```

Full detail → see `references/masters_frameworks.md` → ANTOINE BLANCO section.

### Blanco's Growth Operator Model

Applied when building funnels for creators or other businesses:

```
MATCH → Identify the right creator/business to work with
  Criteria:
  → Audience exists but revenue is under-monetized
  → Creator has credibility but no system
  → Problem their audience has = solution you can build

BUILD → Build the complete monetization system
  → Identify the offer (what does the audience actually want to buy?)
  → Build the funnel (landing page + email sequence + payment)
  → Automate via Make / N8N (no manual intervention after setup)

CLOSE → Sell the system to the creator
  → Package as "I handle everything, you take % of revenue"
  → Or: "Here's the system, implement it" (consulting model)

SCALE → Systematize what works
  → What converted? Double it.
  → What didn't? Kill it in 2 weeks.
  → Replicate to next creator/business
```

---

## PHASE 4B — AGENT-NATIVE AUTONOMOUS FUNNEL

The frameworks above (Yomi, Blanco C4, Tate) were designed for humans.
A human closes on the phone. A human builds trust in person.
An agent can't do that — but an agent can do something else:
**run a complete sales system with zero human intervention, 24/7.**

This phase replaces every step that normally requires a human
with an automated mechanism that produces the same result.

```
WHAT NEEDS A HUMAN         AGENT REPLACEMENT
───────────────────────────────────────────────────────────────
Discovery call             Qualification form (auto-scores leads)
Building rapport           Email sequence with personal story + proof
Handling objections live   Objection-specific emails triggered by behavior
Creating urgency           Real deadline engine (evergreen or fixed window)
Closing the sale           Automated offer page + payment link
Negotiating price          Price tiers + downsell path (automated)
Following up               Behavioral trigger sequences (opens, clicks, time)
Webinar presentation       Evergreen automated webinar (pre-recorded)
```

---

### THE 4 CONVERSION MECHANISMS (no human required)

The agent uses one or more of these to close without a call.

```
MECHANISM 1 — THE DEADLINE ENGINE
  The most powerful autonomous conversion tool.
  Works for: digital products, subscriptions, courses

  Evergreen deadline (recommended for agents):
  → Each subscriber gets their own 72-hour countdown
  → Countdown starts when they join the email list
  → At expiry: price increases by €X or bonus disappears
  → Tool: systeme.io (built-in deadline feature)
  → Rule: ALWAYS real — fake countdowns destroy trust permanently

  Fixed launch window:
  → Offer opens for 5-7 days, then closes
  → Creates mass urgency across all subscribers simultaneously
  → Agent announces via email + Telegram + social content
  → Replay: non-buyers get a 48h "last chance" sequence after close

MECHANISM 2 — BEHAVIORAL TRIGGER SEQUENCES
  The agent tracks what each lead does and responds accordingly.
  No human needed — the system reacts to behavior automatically.

  Triggers the agent monitors:
  → Opened email but didn't click      → "Did you see this?" follow-up
  → Clicked offer page but didn't buy  → Objection-handling sequence
  → Bought Level 1 but not Level 2     → Upsell sequence (day 7 post-purchase)
  → No opens in 14 days                → Re-engagement sequence
  → Abandoned cart                     → Cart recovery sequence (3 emails, 48h)

  Setup in systeme.io:
  → Automation → "If contact clicks [link]" → tag → enter sequence
  → Each behavior gets its own response path
  → The funnel becomes intelligent — adapts to each person

MECHANISM 3 — THE PROOF ENGINE
  What a human does on a sales call: builds trust by talking.
  What the agent does: surfaces proof at the right moment automatically.

  Proof types ranked by conversion power:
  1. Video testimonial with specific result ("I made €X in Y days")
  2. Screenshot of result (trade, revenue, transformation)
  3. Written testimonial with before/after
  4. Number of customers ("312 people already...")
  5. Case study email (the agent writes one per week from real data)

  Automation:
  → Email 4 in every sequence = proof email (best testimonial you have)
  → Triggered re-engagement email = new proof they haven't seen yet
  → Landing page = proof visible above the fold, before the offer
  → Post-purchase sequence = ask for proof from new buyers (email day 14)

MECHANISM 4 — THE EVERGREEN AUTOMATED WEBINAR
  The Yomi live webinar reconverted 15-25% of non-buyers.
  An agent can't do a live webinar — but it can run one that appears live.

  How it works:
  → Record a 45-60 min "presentation" once
  → Upload to systeme.io or EverWebinar
  → Set it to run every hour or on-demand
  → It looks live — has chat, has Q&A (pre-scripted answers)
  → At minute 40: present the offer with a countdown timer
  → After "webinar": 48h replay available, then it closes

  The agent drives non-buyers to this webinar via:
  → Email at day 30 post non-purchase
  → Retargeting content ("I'm doing a live session on [topic]")
  → Direct Telegram message to cold subscribers
```

---

### THE AUTONOMOUS FUNNEL ARCHITECTURE

For a digital product or service with zero human involvement:

```
STAGE 1 — ATTRACT (automated by content-creator + acquisition-master)
  Agent publishes 1 piece of content/day on 3+ platforms
  Every post points to the same entry point (link in bio / landing page)
  Content style: result → insight → CTA ("Get [free thing] at link")

STAGE 2 — CAPTURE (systeme.io landing page)
  Single page. Single offer. Single CTA.
  Free entry: lead magnet / free training / free signal / free tool
  Email captured → enters nurture sequence automatically
  Application form (optional) → pre-qualifies before offer

STAGE 3 — NURTURE (automated email sequence, 7-21 days)
  Day 0:  Welcome + immediate value delivery (the free thing)
  Day 1:  Story — why this works / personal proof
  Day 2:  The mechanism — how it works (educate, don't pitch)
  Day 3:  Proof email — best testimonial or result screenshot
  Day 4:  Objection email — address the #1 reason people don't buy
  Day 5:  Case study — someone like them who got the result
  Day 6:  Soft offer — "when you're ready, here's how to get started"
  Day 7:  Hard offer — deadline activated, bonus expires in 72h
  Day 10: Last chance — 24h remaining on the deadline

  After day 10 (non-buyers):
  → Enter long-term nurture (1 email/week, pure value, no pitch)
  → Triggered back into offer sequence on new proof or webinar event

STAGE 4 — CONVERT (automated offer page)
  No call needed. The page does the work.
  Elements that close without a human:
  → Headline: their exact desired outcome
  → Video: 3-5 min explaining the mechanism + proof
  → What's included (specific, not vague)
  → Social proof: 3-5 testimonials with specific results
  → Price: anchored against the cost of the problem
  → Guarantee: removes risk completely
  → Deadline: visible countdown timer
  → FAQ: handles the 5 most common objections in writing
  → Payment: 2 clicks maximum (systeme.io → Stripe)

STAGE 5 — ASCEND (automated upsell path)
  Immediately after purchase → one-click upsell offer
  "You just got [X]. Would you also like [Y] for €Z more?"
  One click — no new checkout form needed
  Conversion rate: 15-30% of buyers take the upsell

  30 days after purchase → next level offer
  Only offered if they completed onboarding (tracking via systeme.io)
  "You've been using [product] for 30 days. Here's what comes next."

STAGE 6 — RECONVERT (evergreen automated webinar)
  Day 30 post non-purchase: "I'm hosting a session on [topic]"
  Redirects to evergreen automated webinar
  Webinar presents offer + countdown = 15-25% additional conversion
  Runs automatically, any time of day, without the agent present
```

---

### WHEN TO USE WHICH CLOSE TYPE

```
PRODUCT PRICE    HUMAN CLOSE?    AGENT MECHANISM
─────────────────────────────────────────────────────────
< €97            Never           Pure automation (mechanisms 1-4)
€97-297          Rarely          Automation + optional chat support
€297-997         Optional        Automation first, human on objection only
€997-2,000       Recommended     Automated funnel pre-qualifies → human closes
€2,000+          Required        Human close mandatory (Blanco C5 applies)

Rule: The higher the price, the more human trust is required.
      The agent automates everything up to the price threshold.
      Above €997 → automation pre-qualifies, human closes.
```

---

---

## PHASE 5 — ANDREW TATE'S MULTI-CHANNEL STRATEGY

The marketing principles — extracted from what actually worked:

### The Affiliate Army Model

Tate built a program where followers could earn 50% commission by spreading his content. Instead of one channel, there were suddenly thousands — creating viral reach that no ad budget could replicate.

Applied to the agent's funnel:

```
AFFILIATE PROGRAM — embed in every funnel

Structure:
  → Every paying customer gets an affiliate link
  → Commission: 20-40% on referred sales (adjust per margin)
  → Simple: one link, tracked automatically via systeme.io (built-in) or Gumroad

Why it works:
  → Customers who refer become super-advocates
  → Word-of-mouth has higher conversion than any ad
  → Marketing costs go to people who actually produce sales
  → Virality becomes structural, not accidental

Implementation:
  → Email 3 of onboarding sequence: "You can earn X% by sharing"
  → Make it easy: pre-written social posts they can copy
  → Show the leaderboard: top affiliates get recognition
  → Monthly payout = creates recurring motivation
```

### The AIDA Funnel Architecture

Tate's approach fuses the AIDA principle with marketing funnels — Attention, Interest, Desire, Action — directing all social media traffic to a conversion funnel rather than a traditional website.

```
ATTENTION — Stop the scroll
  → Controversial or surprising hook (not offensive — surprising)
  → A specific result with a real number
  → A counter-intuitive claim about the niche
  Channels: Twitter, TikTok, YouTube Shorts, LinkedIn

INTEREST — Make them want to know more
  → Expand the hook with one unexpected insight
  → Show proof (screenshot, chart, specific result)
  → Reference something they already believe but haven't heard stated
  Mechanism: content that earns the click to the funnel

DESIRE — Make them want the outcome
  → Paint the picture of their desired future state
  → Case study from someone identical to them
  → Remove the primary objection before they even ask
  Mechanism: landing page + free formation

ACTION — Remove all friction from the purchase
  → One CTA. One button. One decision.
  → No menu. No other options on the page.
  → Payment in 2 clicks maximum
  → Mobile optimized (50%+ of purchases happen on phone)
```

### Anti-Single-Point-of-Failure: The 5-Channel Rule

```
The agent NEVER builds a funnel that depends on one channel.
If one channel dies, the funnel keeps running.

CHANNEL 1 — Email list (owned, never rented)
  The primary asset. Build this first. Protect it above all.
  Import to multiple platforms for redundancy.

CHANNEL 2 — Telegram (direct, high open rate)
  For hot leads and paying customers.
  VIP channel = premium access = retention mechanism.

CHANNEL 3 — Short-form video (Twitter/X, TikTok, Reels)
  Top of funnel. Viral potential. Keeps new people entering.

CHANNEL 4 — Long-form content (YouTube, Substack, blog)
  SEO + authority building. Evergreen traffic.
  One great video can bring leads for 2 years.

CHANNEL 5 — Affiliate network (owned distribution)
  Every satisfied customer becomes a distribution node.
  Compounds over time without additional cost.
```

---

## PHASE 6 — THE RECONVERSION MACHINE

This is where most agents stop. This is where the money is.

### Reconversion Channels (for non-buyers)

```
CHANNEL 1 — Webinar live (Yomi model)
  Frequency: 2-3x per year
  Format: 60-90 min live + replay 48h
  Offer: 30-50% discount on core offer + new bonuses
  Target: everyone who watched the free formation but didn't buy
  Expected additional conversion: +15-25% of remaining leads

CHANNEL 2 — Retargeting email sequence
  Trigger: 30 days after non-purchase
  Sequence: 4 emails over 10 days
  Angle: different from original sequence
  Email 1: New result/testimonial since they last engaged
  Email 2: Direct question ("What stopped you?")
  Email 3: Case study from someone who hesitated like them
  Email 4: Final offer with a new angle (not same pitch)

CHANNEL 3 — New entry point (content loop)
  Non-buyer stays in content feed (Twitter, YouTube)
  New content creates new buying triggers
  → New result they see → reopens the desire
  → New objection handled → removes their blocker
  → Price drop announcement → creates urgency

CHANNEL 4 — Downsell (for price-sensitive leads)
  If they didn't buy the core offer → offer Level 1 at 1/3 price
  → Lower barrier to first transaction
  → Once they're a customer, upsell is 5x easier

CHANNEL 5 — Re-engagement campaign
  90 days of silence → send a "we miss you" with fresh value
  Subject: "[Name], what happened?" or "Still struggling with [X]?"
  Include: 1 new piece of free value + soft CTA
```

---

## PHASE 7 — FUNNEL BUILD CHECKLIST

The agent works through this checklist in order. Never skip steps.

```
PRE-BUILD (before writing a single word)
  ☐ Niche validated (4 criteria passed)
  ☐ ICP defined (1 specific person, not a demographic)
  ☐ Offer built (Grand Slam structure complete)
  ☐ Ticket ladder defined (3 levels minimum)
  ☐ Competitors analyzed (what's missing in their offer)

TOP OF FUNNEL (attract)
  [If trading-signals model: include financial disclaimer on all pages — see funnel_config.json]
  ☐ Content strategy defined (platform + format + frequency)
  ☐ Hook library built (references/copywriting.md)
  ☐ Free entry point created (lead magnet / free formation / free trial)
  ☐ Affiliate program structure defined

CAPTURE (convert visitor to lead)
  ☐ Landing page built (templates/landing_page.md)
  ☐ Single CTA on page (no distractions)
  ☐ Email capture configured (systeme.io built-in, Brevo, or ConvertKit — agent uses wesley-web-operator)
  ☐ Thank you page with immediate value delivery
  ☐ Mobile tested

NURTURE (convert lead to buyer)
  ☐ Email sequence written (templates/email_sequence.md)
  ☐ 7-day free trial or free formation mapped
  ☐ Deadline mechanism set (72h or webinar date)
  ☐ Objection handling in emails 3 and 4
  ☐ Guarantee visible on every conversion page

CONVERT (buyer)
  ☐ Payment page set up — agent outputs config, deploy via systeme.io or Stripe (manual or via virtual-desktop)
  ☐ 2-click maximum from CTA to payment
  ☐ Upsell offered immediately after purchase
  ☐ Onboarding email with affiliate link (email 3)
  ☐ Member area set up (systeme.io) + Telegram VIP optional

RECONVERT (non-buyers)
  ☐ Webinar date set (2x/year minimum)
  ☐ Retargeting sequence written (4 emails, 10 days)
  ☐ Downsell page created
  ☐ 90-day re-engagement campaign planned

SCALE
  ☐ Affiliate program live (systeme.io built-in or Gumroad)
  ☐ A/B test defined for landing page headline
  ☐ Analytics configured (open rate, CTR, conversion per stage)
  ☐ Anomaly thresholds set (< 25% open = rewrite subject lines)
```

---

## PHASE 8 — FUNNEL DIAGNOSIS

When an existing funnel doesn't convert, the agent diagnoses before rebuilding.

### The 5 Funnel Failure Points

```
FAILURE POINT 1 — Wrong traffic (top of funnel)
  Symptom: high traffic, low opt-in rate (< 10%)
  Diagnosis: the content attracts the wrong ICP
  Fix: redefine ICP, change content angle

FAILURE POINT 2 — Weak lead magnet
  Symptom: low opt-in rate despite right traffic (< 15%)
  Diagnosis: the free offer doesn't feel valuable enough
  Fix: increase perceived value of lead magnet (more specific, faster result)

FAILURE POINT 3 — Email sequence not converting
  Symptom: good opt-in rate, < 1% purchase rate
  Diagnosis: sequence doesn't build desire or handle objections
  Fix: rewrite email 3 (proof) and email 4 (objection) first

FAILURE POINT 4 — Landing page friction
  Symptom: people click the CTA but don't complete purchase
  Diagnosis: too many steps, mobile broken, payment confusion
  Fix: reduce to 2-click purchase, test on mobile, add trust signals

FAILURE POINT 5 — No reconversion system
  Symptom: one-time revenue, no revenue growth over time
  Diagnosis: non-buyers are abandoned after sequence ends
  Fix: add webinar + retargeting sequence + downsell

Fixing failure points in order 1→5. Never fix 5 before 1.
```

---

## Workspace Structure

```
/workspace/funnel/
├── config.json               ← business model, ICP, offer, price
├── active/
│   └── [business-slug]/
│       ├── funnel_map.md     ← complete funnel architecture
│       ├── landing_page.html ← deploy to hosting
│       ├── email_sequence.md ← import into Brevo
│       ├── offer_doc.md      ← full offer copy
│       └── checklist.md      ← deployment progress
└── templates/                ← this skill's reference files
    ├── funnel_config.json  ← read-only reference (bundle file)
    ├── landing_page.md
    └── email_sequence.md
```

---

## Error Handling

```
ERROR: config.json missing
  Action: Ask principal for 4 inputs via Telegram:
    1. Business model
    2. ICP (1 sentence)
    3. Core offer (1 sentence)
    4. Price point
  Never build without config. A funnel without a defined ICP converts nobody.

ERROR: Niche validation fails (any of 4 criteria = No)
  Action: Do not build the funnel.
  Report to principal: "Niche [X] failed criterion [Y].
  Recommendation: [alternative niche or ICP adjustment]"
  Log: LEARNINGS.md → niche rejection with reason

ERROR: Funnel built but conversion < 0.5% after 100 leads
  Action: Run the 5-failure-point diagnosis automatically.
  Report the failure point found.
  Propose specific fix with rationale.
  Log: LEARNINGS.md → funnel diagnosis + fix applied

ERROR: Email sequence open rate < 25%
  Action: Rewrite subject lines using hooks from references/copywriting.md
  A/B test new vs old subject line
  Log: AUDIT.md → subject line test initiated
```
