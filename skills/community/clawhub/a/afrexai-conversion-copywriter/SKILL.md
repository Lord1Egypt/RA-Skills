# Conversion Copywriter — The Complete Persuasion System

Write copy that converts. Every headline, landing page, email, ad, and sales page — engineered for action using proven frameworks, psychology, and systematic testing.

---

## Phase 1: Copy Brief (Before You Write a Single Word)

Every copy project starts with a brief. Skip this and you're guessing.

```yaml
copy_brief:
  project: "[Landing page / Email sequence / Ad campaign / Sales page]"
  objective: "[Signups / Purchases / Demos / Downloads]"
  target_audience:
    who: "[Job title, demographic, situation]"
    awareness_level: "[Unaware / Problem-Aware / Solution-Aware / Product-Aware / Most-Aware]"
    primary_pain: "[Their #1 frustration in their own words]"
    desired_outcome: "[What they actually want — the transformation]"
    current_alternative: "[What they do now instead of your solution]"
    objections:
      - "[Top objection 1]"
      - "[Top objection 2]"
      - "[Top objection 3]"
  offer:
    product: "[What you're selling]"
    unique_mechanism: "[HOW it works differently — the thing that makes you believe]"
    primary_benefit: "[Single biggest outcome]"
    proof_points:
      - "[Stat, testimonial, case study, demo]"
    guarantee: "[Risk reversal — money-back, free trial, etc.]"
    cta: "[Exact action you want them to take]"
  voice:
    brand_personality: "[Authoritative / Friendly / Provocative / Empathetic]"
    tone_for_this_piece: "[Urgent / Educational / Conversational / Bold]"
    reading_level: "[Grade 5-8 for mass market, 8-12 for B2B]"
  constraints:
    word_count: "[Target length]"
    platform: "[Web / Email / Social / Print]"
    compliance: "[Any legal/regulatory requirements]"
```

### Audience Awareness Levels (Eugene Schwartz)

This determines EVERYTHING about your copy structure:

| Level | They Know | Your Copy Must | Open With |
|-------|-----------|----------------|-----------|
| **Unaware** | Nothing about the problem | Educate → Agitate → Solve | A story or pattern interrupt |
| **Problem-Aware** | They have a problem | Agitate → Present solution | Their pain in their words |
| **Solution-Aware** | Solutions exist | Differentiate your approach | Your unique mechanism |
| **Product-Aware** | Your product exists | Overcome objections + prove | Proof and social proof |
| **Most-Aware** | They're almost ready | Make the offer irresistible | The deal — price, bonus, urgency |

**Rule:** Never sell to Unaware audiences the way you'd sell to Most-Aware. Match the message to the mind.

---

## Phase 2: Research (The 80/20 of Great Copy)

Great copy is assembled, not written. 80% research, 20% writing.

### Voice-of-Customer (VoC) Mining

Search these sources for the exact language your audience uses:

1. **Amazon reviews** (of competing books/products) — 3-star reviews = balanced, honest language
2. **Reddit/forums** — search `[problem] site:reddit.com` for raw frustration
3. **G2/Capterra/Trustpilot** — competitor reviews, especially 2-3 star
4. **Support tickets / sales call transcripts** — goldmine for objection language
5. **Social comments** — competitor posts, industry influencers
6. **Survey responses** — if you have them

### What to Extract

For each source, capture:

```yaml
voc_nugget:
  source: "[Where you found it]"
  quote: "[Exact words they used]"
  category: "[pain / desire / objection / language]"
  power_level: "[1-5 — how emotionally charged]"
  usable_as: "[headline / bullet / testimonial / objection handler]"
```

**Goal:** Collect 30-50 nuggets before writing. The best headlines are stolen from customer mouths.

### Competitor Copy Audit

For each competitor:
- Screenshot their landing page / key emails
- Note: headline, subhead, CTA, proof elements, guarantee, pricing frame
- Rate: clarity (1-5), desire (1-5), urgency (1-5), differentiation (1-5)
- Identify gaps: what are they NOT saying that you could?

---

## Phase 3: Core Copywriting Frameworks

### Framework 1: AIDA (Attention → Interest → Desire → Action)

The classic. Works for landing pages, emails, ads, sales pages.

```
ATTENTION:  Stop the scroll. Bold claim, provocative question, or pattern interrupt.
INTEREST:   Elaborate on the problem. Make them nod: "that's exactly me."
DESIRE:     Show the transformation. Paint the after-state with specificity.
ACTION:     Clear, single CTA. Remove all friction.
```

**Template:**
```
[HEADLINE — the promise or the pain, 6-12 words]

[SUBHEAD — elaborate on headline, add specificity or curiosity]

You know the feeling. [Describe their current painful situation in 2-3 sentences.
Use their language. Make it vivid.]

[2-3 sentences expanding the problem — what it costs them (time, money,
reputation, stress)]

Here's the thing: [Introduce your unique mechanism — HOW your solution
works differently]

[3-5 bullet points of specific benefits, each starting with a verb]

[Social proof block — testimonial, stat, or case study]

[CTA button: Verb + Benefit, e.g., "Start Saving 10 Hours/Week"]

[Risk reversal: guarantee, free trial, no-commitment language]
```

### Framework 2: PAS (Problem → Agitate → Solution)

Best for pain-driven products. Short-form emails, ads, social posts.

```
PROBLEM:    State it plainly. One sentence.
AGITATE:    Twist the knife. What happens if they DON'T solve it? Emotional cost.
SOLUTION:   Your product as the relief. Specific. Credible.
```

**Template:**
```
[PROBLEM — 1 sentence, their exact words]

And it's getting worse. [Agitate — 2-3 sentences on cascading consequences.
Future-pace the pain. "If you don't fix this, in 6 months you'll be..."]

[SOLUTION — Introduce product. 1-2 sentences. HOW it solves it specifically.]

[Proof — one compelling data point or testimonial]

[CTA]
```

### Framework 3: BAB (Before → After → Bridge)

Best for aspirational products, coaching, lifestyle. Social posts, emails.

```
BEFORE:  Their current frustrating reality (specific, vivid)
AFTER:   Their desired future state (specific, vivid, emotional)
BRIDGE:  Your product/service is the bridge between the two
```

### Framework 4: 4Ps (Promise → Picture → Proof → Push)

Best for sales pages and long-form.

```
PROMISE:  Bold, specific claim (your headline)
PICTURE:  Vivid description of life after using your product
PROOF:    Evidence — testimonials, data, case studies, demos
PUSH:     Urgency + CTA — why act now?
```

### Framework 5: PASTOR (Problem → Amplify → Story → Transformation → Offer → Response)

Best for long-form sales pages, webinar scripts, video sales letters.

```
P — PROBLEM:        Identify the pain (in their words)
A — AMPLIFY:        What happens if they ignore it? Emotional + financial cost
S — STORY:          Tell a story (yours, a client's) of facing the same problem
T — TRANSFORMATION: Show the before/after. Specific results.
O — OFFER:          Present your solution. What they get. Stack the value.
R — RESPONSE:       CTA. Tell them exactly what to do. Remove all risk.
```

### Framework Selection Guide

| Situation | Best Framework | Why |
|-----------|---------------|-----|
| Landing page (SaaS) | AIDA or 4Ps | Structured, covers all bases |
| Cold email | PAS | Short, punchy, pain-focused |
| Social media post | BAB | Quick, aspirational |
| Long sales page | PASTOR | Deep narrative, high-ticket |
| Ad (Facebook/Google) | PAS or AIDA | Compressed, attention-first |
| Welcome email | BAB | Sets the vision |
| Re-engagement email | PAS | Reminds them of unresolved pain |

---

## Phase 4: Headline Mastery

The headline does 80% of the work. If the headline fails, nothing else matters.

### The 7 Headline Types (With Templates)

**1. Benefit-Driven**
```
Get [Desired Outcome] Without [Pain Point]
[Number] [People Like Them] Already [Achieved Result]
The Fastest Way to [Outcome] — Even If [Objection]
```

**2. Curiosity-Gap**
```
Why [Common Approach] Is Killing Your [Goal] (And What to Do Instead)
The [Adjective] [Thing] That [Surprising Result]
What [Authority] Knows About [Topic] That You Don't
```

**3. How-To**
```
How to [Achieve Goal] in [Timeframe] (Step-by-Step)
How [Specific Person] Went From [Before] to [After] in [Time]
How to [Goal] Without [Sacrifice]
```

**4. Listicle**
```
[Number] Ways to [Benefit] (That Actually Work)
[Number] Mistakes That Are Costing You [Loss]
[Number] [Things] Every [Audience] Should Know
```

**5. Question**
```
Are You Making These [Number] [Topic] Mistakes?
What If You Could [Dream Outcome] in Just [Timeframe]?
Is [Common Practice] Actually Hurting Your [Goal]?
```

**6. Command**
```
Stop [Bad Behavior] and Start [Good Behavior]
Forget Everything You Know About [Topic]
Stop Losing [Value] — [Solution] in [Time]
```

**7. Proof-Led**
```
How We Generated [Specific Number] in [Time] With [Method]
[Real Name] Went From [Before] to [After] — Here's How
[Number]% of [Audience] Saw [Result] Within [Time]
```

### Headline Quality Checklist (Score 0-10)

| Criteria | 0-1 | 5 | 9-10 |
|----------|-----|---|------|
| **Specificity** | Vague promise | Some detail | Exact numbers/outcomes |
| **Relevance** | Generic | Somewhat targeted | Speaks to their exact situation |
| **Curiosity** | No reason to read on | Mild interest | Can't NOT click |
| **Clarity** | Confusing | Understandable | Instantly clear what you get |
| **Emotional Pull** | Flat | Some feeling | Hits a nerve (pain or desire) |

**Rule:** Write 25+ headlines. Pick the top 3. Test them. The first headline you write is almost never the best.

---

## Phase 5: Persuasion Psychology (The Science Behind Conversion)

### 12 Cognitive Triggers

Use these ethically. Manipulation destroys trust. Persuasion serves both parties.

| Trigger | How It Works | Copy Example |
|---------|-------------|--------------|
| **Social Proof** | We follow the crowd | "Join 14,000+ teams using..." |
| **Scarcity** | Limited = valuable | "Only 12 spots left this quarter" |
| **Urgency** | Time pressure | "Price increases Friday at midnight" |
| **Authority** | Experts = credible | "Recommended by [known name/brand]" |
| **Reciprocity** | Give first, ask second | Free tool/guide before the ask |
| **Commitment** | Small yes → big yes | "Start with our free plan" |
| **Loss Aversion** | Losing > gaining | "You're leaving $X/month on the table" |
| **Anchoring** | First number frames all | "Normally $5,000 — yours for $497" |
| **Contrast** | Side-by-side comparison | "Hiring costs $80K/yr. This costs $49/mo" |
| **Curiosity Gap** | Open loop = must close | "The strategy most agencies won't tell you" |
| **Identity** | We buy who we want to be | "Built for founders who ship" |
| **Specificity** | Specific = believable | "37% increase" beats "significant increase" |

### The Objection Destruction Framework

For every copy piece, address the top 3-5 objections. Use this structure:

```
OBJECTION:    "[What they're thinking]"
ACKNOWLEDGE:  "You might be wondering..." or "Fair question."
REFRAME:      "[Why this objection doesn't apply / is actually a benefit]"
PROVE:        "[Testimonial, stat, or guarantee that neutralizes it]"
```

**Common objection patterns:**

| Objection Type | Example | Best Response |
|---------------|---------|---------------|
| Price | "Too expensive" | Anchor against alternative cost (hiring, time, lost revenue) |
| Time | "I'm too busy" | Show time savings with specific numbers |
| Trust | "How do I know it works?" | Case study + guarantee + specific results |
| Relevance | "Not for my situation" | Use their industry/role in examples |
| Complexity | "Seems complicated" | "3 steps" / "works in 10 minutes" |
| Risk | "What if it doesn't work?" | Guarantee: "30-day money-back, no questions" |

---

## Phase 6: Copy Types — Complete Templates

### Landing Page (Above the Fold)

```
[NAVIGATION — minimal. Logo + 1 CTA button in nav]

[HEADLINE — 6-12 words. Primary benefit or pain resolution]

[SUBHEADLINE — 15-25 words. Elaborate on headline.
 Add specificity, curiosity, or credibility]

[HERO IMAGE/VIDEO — show the product in use or the outcome]

[PRIMARY CTA BUTTON — Verb + Benefit. High contrast color]
[Friction reducer underneath: "Free trial" / "No credit card" / "2-minute setup"]

[SOCIAL PROOF BAR — logos, "Trusted by X companies", star ratings]
```

### Landing Page (Full Structure)

```
1. Hero (above fold) — headline, subhead, CTA, social proof bar
2. Problem Section — "You're dealing with..." (3 pain points)
3. Solution Section — "Here's how [Product] fixes this" (3 benefits with icons)
4. How It Works — 3 numbered steps (simple, visual)
5. Social Proof — 2-3 testimonials with photo, name, result
6. Features → Benefits — don't list features, translate to outcomes
7. Objection Handling — FAQ or "But what if..." section
8. Case Study — one detailed before/after story
9. Pricing — anchored, with most popular plan highlighted
10. Final CTA — repeat the primary CTA with urgency
11. Risk Reversal — guarantee badge/text
```

### Email Sequence (Welcome — 5 emails)

```yaml
email_1_welcome:
  timing: "Immediately after signup"
  subject: "Welcome to [Product] — here's your first win"
  goal: "Deliver quick value, set expectations"
  structure:
    - "Welcome + what they just got access to"
    - "ONE thing to do right now (their first quick win)"
    - "What to expect (email frequency, what's coming)"
    - "P.S. — Reply to this email with your biggest challenge with [topic]"

email_2_value:
  timing: "Day 2"
  subject: "[Specific useful tip or resource]"
  goal: "Prove expertise, build trust"
  structure:
    - "Teach one actionable thing (not product-related)"
    - "Show you understand their world"
    - "Soft CTA: 'Check out [feature] for more of this'"

email_3_story:
  timing: "Day 4"
  subject: "How [Name] went from [Before] to [After]"
  goal: "Social proof through narrative"
  structure:
    - "Tell a customer success story (BAB framework)"
    - "Specific numbers and timeline"
    - "CTA: 'Want results like this? Here's how to get started'"

email_4_objection:
  timing: "Day 6"
  subject: "The #1 question we get about [Product]"
  goal: "Handle the biggest objection"
  structure:
    - "Acknowledge the concern honestly"
    - "Reframe with data or logic"
    - "Prove with testimonial or guarantee"
    - "CTA: 'See for yourself — [start trial / book demo]'"

email_5_urgency:
  timing: "Day 8"
  subject: "Last chance: [Specific offer with deadline]"
  goal: "Convert fence-sitters"
  structure:
    - "Remind of the transformation (BAB)"
    - "Stack the value: everything they get"
    - "Add urgency: deadline, limited spots, price increase"
    - "Risk reversal: guarantee"
    - "Clear CTA"
```

### Cold Outreach Email

```
SUBJECT: [Specific result] for [their company/role]
(Never generic. Never "Quick question." Never salesy.)

[First line — specific observation about THEM. Not about you.]

[One sentence: the problem you solve, stated as an outcome.]

[One proof point: "[Similar company] saw [specific result] in [timeframe]."]

[CTA — low commitment: "Worth a 15-min call to see if this fits?"]

[Sign-off — name, title. No "Sent from my iPhone." No multi-paragraph signature.]
```

**Cold email rules:**
- Under 100 words total
- No attachments
- No "I hope this finds you well"
- No "I'd love to pick your brain"
- One CTA only
- Personalization in first line is mandatory

### Ad Copy (Facebook/Instagram)

```
PRIMARY TEXT (125 chars visible before "See More"):
[Hook — pattern interrupt or bold claim. Stop the scroll.]

[EXPANDED TEXT]:
[Problem — 1 sentence, their language]
[Agitate — what it costs them]
[Solution — what you offer, one sentence]
[Proof — one stat or testimonial, one line]
[CTA — "Click below to [specific outcome]"]

HEADLINE (40 chars): [Benefit, not feature]
DESCRIPTION (30 chars): [Supporting detail or urgency]
CTA BUTTON: [Learn More / Sign Up / Get Offer — match funnel stage]
```

### Google Ads

```
HEADLINE 1 (30 chars): [Primary keyword + benefit]
HEADLINE 2 (30 chars): [Differentiator or proof]
HEADLINE 3 (30 chars): [CTA or urgency]
DESCRIPTION 1 (90 chars): [Expand on benefit. Include keyword naturally. CTA.]
DESCRIPTION 2 (90 chars): [Proof point or second benefit. Risk reversal.]
```

### Product Description (Ecommerce)

```
[HEADLINE: Outcome-focused, not feature-focused]

[Opening paragraph: Who this is for + the #1 benefit they'll experience]

WHAT MAKES IT DIFFERENT:
• [Benefit 1 — tied to a specific feature]
• [Benefit 2 — tied to a specific feature]
• [Benefit 3 — tied to a specific feature]

[Technical specs / dimensions / materials — for the detail-seekers]

[Social proof: star rating, review quote, "X,000 sold"]

[CTA: "Add to Cart" / "Buy Now" with urgency element]
```

### Sales Page (Long-Form — Complete Structure)

```
1. PRE-HEAD: "[Attention] For [specific audience] who want [outcome]"
2. HEADLINE: The big promise
3. SUBHEAD: Specificity + credibility layer
4. OPENING: Story or problem statement (PAS or PASTOR)
5. PROBLEM EXPANSION: 3-5 specific symptoms they recognize
6. FAILED ALTERNATIVES: What they've tried (and why it didn't work)
7. UNIQUE MECHANISM: Your "aha" — the thing that makes THIS solution different
8. BENEFIT STACK: 7-10 bullets, each Benefit → because Feature → so that Outcome
9. SOCIAL PROOF: 3-5 testimonials (diverse: different roles, industries, results)
10. OFFER STACK: Everything they get, with perceived value next to each
11. PRICE REVEAL: Anchored against alternatives. "Not $X. Not $Y. Just $Z."
12. BONUSES: 2-3 extras that increase perceived value
13. GUARANTEE: Bold, specific, generous. "Full refund within 60 days. Keep the bonuses."
14. URGENCY: Real deadline or real scarcity (never fake)
15. FINAL CTA: Repeat offer summary + button
16. P.S.: Restate the key benefit + the guarantee (many readers skip to P.S.)
```

---

## Phase 7: Bullet Point Mastery

Bullets do heavy lifting. Most copy lives or dies on bullet quality.

### The Bullet Formula

```
[POWER WORD] + [SPECIFIC BENEFIT] + [CURIOSITY/PROOF]
```

### 6 Bullet Types

**1. Benefit Bullet:**
```
✓ Save 10+ hours every week on reporting (so you can focus on strategy)
```

**2. Curiosity Bullet:**
```
✓ The counterintuitive pricing trick that increased our revenue 42% overnight
```

**3. Proof Bullet:**
```
✓ Used by 3,200+ agencies in 40 countries (including 4 Fortune 500 firms)
```

**4. Fear Bullet:**
```
✓ The hidden compliance gap that's exposing 73% of SaaS companies to lawsuits
```

**5. How-To Bullet:**
```
✓ How to write proposals that close in 48 hours (not 3 weeks)
```

**6. Specificity Bullet:**
```
✓ 14 pre-built email templates tested across 200K+ sends (avg. 34% open rate)
```

**Rule:** Mix bullet types. Never use more than 3 of the same type in a row.

---

## Phase 8: CTA Optimization

### CTA Formula

```
[ACTION VERB] + [SPECIFIC BENEFIT] + [TIME/EASE QUALIFIER]
```

**Examples:**
```
✓ "Start Saving 10 Hours/Week — Free for 14 Days"
✓ "Get Your Custom Growth Plan in 2 Minutes"
✓ "Download the 47-Point Checklist (Free)"
✗ "Submit" / "Click Here" / "Learn More" (weak, vague)
```

### CTA Placement Rules

| Location | Type | Purpose |
|----------|------|---------|
| Above fold | Primary button | Catch ready buyers |
| After problem section | Text link | Catch pain-motivated |
| After social proof | Primary button | Catch proof-seekers |
| After pricing | Primary button | Catch decision-makers |
| Bottom of page | Primary button + guarantee | Catch completionists |
| Sticky bar/footer | Persistent CTA | Catch scrollers |

### Friction Reducers (Place Near CTAs)

```
"No credit card required"
"Cancel anytime — no questions asked"
"Takes less than 2 minutes"
"Join 14,000+ [audience] who already [outcome]"
"100% money-back guarantee"
```

---

## Phase 9: Copy Scoring Rubric (0-100)

Score every piece before publishing:

| Dimension | Weight | 0-2 | 5 | 8-10 |
|-----------|--------|-----|---|------|
| **Clarity** | 20% | Confusing, jargon-heavy | Mostly clear | Crystal clear, grade-school readable |
| **Specificity** | 15% | Vague claims, no numbers | Some specifics | Exact numbers, names, timeframes |
| **Emotional Resonance** | 15% | Flat, corporate | Some feeling | Hits pain or desire viscerally |
| **Proof** | 15% | No evidence | One proof point | Multiple proof types stacked |
| **CTA Strength** | 10% | Weak/missing CTA | Generic CTA | Specific, benefit-driven, low friction |
| **Objection Handling** | 10% | Ignores doubts | Addresses 1-2 | Systematically neutralizes top 3+ |
| **Voice Consistency** | 10% | Tone shifts randomly | Mostly consistent | Natural, human, on-brand throughout |
| **Readability** | 5% | Dense paragraphs | OK formatting | Short paragraphs, bullets, visual hierarchy |

**Score interpretation:**
- **90-100:** Ship it. Strong conversion likely.
- **70-89:** Good. Test it, iterate on weak dimensions.
- **50-69:** Mediocre. Rewrite weakest 2-3 dimensions.
- **Below 50:** Start over with a fresh brief.

---

## Phase 10: A/B Testing Protocol

Never trust your instincts. Test everything.

### What to Test (Priority Order)

1. **Headlines** — highest leverage, test first always
2. **CTA text and color** — second highest impact
3. **Social proof placement** — where and what type
4. **Price framing** — anchoring, struck-through, monthly vs annual
5. **Page length** — short vs long (depends on awareness level)
6. **Images** — product screenshot vs lifestyle vs video thumbnail

### Testing Rules

- **One variable at a time** — never test headline AND CTA simultaneously
- **Minimum sample:** 100 conversions per variant before calling a winner
- **Statistical significance:** 95% confidence minimum
- **Run for full weeks** — don't stop mid-week (day-of-week effects)
- **Document everything:**

```yaml
ab_test:
  test_id: "[descriptive name]"
  hypothesis: "[Changing X will improve Y because Z]"
  variable: "[headline / CTA / image / etc.]"
  control: "[current version]"
  variant: "[new version]"
  metric: "[conversion rate / CTR / revenue per visitor]"
  start_date: "[YYYY-MM-DD]"
  end_date: "[YYYY-MM-DD]"
  sample_size: "[per variant]"
  result:
    control_rate: "[X%]"
    variant_rate: "[Y%]"
    confidence: "[Z%]"
    winner: "[control / variant]"
    lift: "[+/-X%]"
  learning: "[What this teaches us about our audience]"
```

---

## Phase 11: Platform-Specific Rules

### Web Copy
- Above-fold load time < 3s — heavy copy on slow pages never converts
- F-pattern reading: front-load important info on the left
- Mobile-first: 60%+ traffic is mobile — test on phone before desktop
- Max 3-4 lines per paragraph on desktop, 2-3 on mobile

### Email Copy
- Subject line < 50 chars (mobile truncation)
- Preview text is your second headline — write it intentionally
- One CTA per email (multiple links to same destination is fine)
- Plain text outperforms heavy HTML for B2B
- P.S. line gets read more than any paragraph — use it

### Social Copy
- First line must hook — everything after is "See More"
- Use line breaks aggressively (each line = new thought)
- Emojis: 1-2 max in professional contexts, more in consumer
- End with a question to boost comments (algorithm signal)

### Ad Copy
- Match ad copy to landing page headline (message match = higher Quality Score)
- Negative keywords save budget — review search terms weekly
- Dynamic keyword insertion: `{KeyWord:Default}` in headlines
- Retargeting ads: objection-handling copy, not awareness copy

---

## Phase 12: Copy Editing Checklist

Run every piece through this before publishing:

### Cut
- [ ] Remove every "very," "really," "actually," "just," "that" (unless needed for rhythm)
- [ ] Kill adverbs — if the verb needs an adverb, use a stronger verb
- [ ] Delete any sentence that doesn't earn its place (does it inform, persuade, or move forward?)
- [ ] Remove weasel words: "might," "could," "possibly," "somewhat"

### Strengthen
- [ ] Replace passive voice with active ("was improved by" → "improved")
- [ ] Convert features to benefits ("AI-powered" → "saves you 3 hours daily")
- [ ] Add numbers wherever possible ("fast results" → "results in 48 hours")
- [ ] Replace "we" with "you" (reader-centric, not company-centric)

### Format
- [ ] No paragraph longer than 4 lines on desktop
- [ ] Subheadings every 3-5 paragraphs (scannable)
- [ ] Bullets for any list of 3+ items
- [ ] Bold key phrases (not whole sentences)
- [ ] One idea per paragraph

### Proof
- [ ] Read it aloud — if you stumble, rewrite
- [ ] Hemingway App or equivalent: target grade 6-8
- [ ] Check: would a stranger understand this in 5 seconds?
- [ ] Show to someone outside your industry — do they get it?

---

## Phase 13: Swipe File Management

Build your own library of proven copy.

```yaml
swipe:
  source: "[URL or screenshot location]"
  brand: "[Company name]"
  type: "[landing page / email / ad / sales page]"
  what_works: "[Specific technique: headline formula, proof stacking, etc.]"
  steal_this: "[Exact pattern you can adapt]"
  date_saved: "[YYYY-MM-DD]"
  tags: ["headline", "social-proof", "urgency", "B2B"]
```

**Swipe file rules:**
- Save 2-3 pieces per week minimum
- Tag by technique, not by industry
- Review monthly — spot patterns in what attracts you
- Adapt structures, never copy verbatim

---

## Phase 14: Advanced Techniques

### The "So What?" Test
After every claim, ask "So what?" If you can't answer with a specific benefit to the reader, delete the claim.

```
"Our platform uses machine learning." → So what?
"It predicts which leads will close so you stop wasting time on dead-ends." ✓
```

### The "One Reader" Rule
Write to ONE specific person. Not "businesses." Not "marketers." One human with a name, a frustration, and a deadline. If you can't picture them reading your copy, it's too generic.

### The Contrast Principle
Always anchor your price/effort against something bigger:
```
"A single bad hire costs $50K. This costs $499/year."
"You'll spend 400 hours doing this manually. Or 4 hours with [Product]."
```

### Future Pacing
Describe their life AFTER using your product. Be specific. Engage senses.
```
"Imagine opening your laptop Monday morning to a dashboard showing every deal
moving forward automatically. No missed follow-ups. No spreadsheet chaos."
```

### The Bucket Brigade
Transition words that keep readers scrolling:
```
"Here's the thing:"
"But it gets better."
"Now here's where it gets interesting."
"Think about it:"
"The bottom line?"
"And the best part?"
```

### Power Words (Use in Headlines and Bullets)

| Category | Words |
|----------|-------|
| **Urgency** | Now, Today, Instant, Fast, Deadline, Limited, Final |
| **Exclusivity** | Secret, Insider, Private, Members-only, Invitation |
| **Proof** | Proven, Tested, Guaranteed, Verified, Data-backed |
| **Ease** | Simple, Easy, Effortless, Quick, Painless, Done-for-you |
| **Value** | Free, Bonus, Premium, Unlock, Access, Exclusive |
| **Emotion** | Crushing, Devastating, Skyrocket, Transform, Breakthrough |

---

## Phase 15: Natural Language Commands

```
"Write a landing page for [product]"     → Brief + AIDA landing page
"Write cold email for [audience]"        → Research + PAS cold email
"Score this copy"                        → Run 0-100 rubric with feedback
"Write 25 headlines for [topic]"         → Headline variations across all 7 types
"Write email sequence for [product]"     → 5-email welcome sequence
"Write ad copy for [platform]"           → Platform-specific ad copy
"Write sales page for [offer]"           → Long-form PASTOR sales page
"Handle objections for [product]"        → Objection destruction framework
"Audit this copy: [paste]"              → Editing checklist + scoring + rewrite
"Write bullets for [feature list]"       → 6-type bullet variations
"Write CTA options for [page]"           → 10+ CTA variations with scoring
"Compare frameworks for [situation]"     → Framework selection with rationale
```

---

## Edge Cases

### Regulated Industries (Finance, Health, Legal)
- No income claims without disclaimers
- "Results may vary" mandatory with testimonials
- Avoid superlatives ("best," "guaranteed results") — use "designed to" language
- Have compliance review BEFORE publishing, not after

### B2B vs B2C
- **B2B:** Longer consideration. More proof needed. ROI language. Multiple stakeholders.
- **B2C:** Shorter. More emotional. Aspirational. Single decision-maker.
- **B2B2C:** Write for the buyer (B2B) AND their customer (B2C) simultaneously.

### High-Ticket ($5K+)
- Longer copy works better (more objections to handle)
- Case studies mandatory — abstract claims won't close
- Personal touch: video, hand-signed, "from [Founder Name]"
- Risk reversal must be generous and specific

### Low-Ticket (<$50)
- Short copy often wins (less deliberation needed)
- Social proof: volume numbers ("10K+ customers")
- Impulse triggers: urgency, simplicity, instant access

### International / Non-English
- Research local idioms — direct translation kills conversion
- Cultural sensitivity: humor, urgency, authority vary by culture
- Currency, date format, measurement units — match the market
- Test separately — what works in US rarely works in Japan unchanged
