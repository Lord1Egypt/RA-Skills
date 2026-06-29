# Voice Attributes

How to define, document, and validate the 3-5 voice attributes that anchor TONE.md. Voice is the brand's fixed personality — it does **not** change across channels. Tone modulates per situation; voice does not.

---

## Table of contents

- [The "X but never Y" pattern](#the-x-but-never-y-pattern)
- [Attribute documentation template](#attribute-documentation-template)
- [NN/g 4 dimensions](#nng-4-dimensions)
- [Jung's 12 archetypes](#jungs-12-archetypes)
- [BrandSort / message architecture](#brandsort--message-architecture)
- [Brand-as-person exercise](#brand-as-person-exercise)
- [Frameworks compared](#frameworks-compared)

---

## The "X but never Y" pattern

The single most useful documentation device in the discipline. Slack's published voice:

> _"Confident (never cocky), Witty (but never silly), Conversational (but always appropriate and respectful), Intelligent (but not arrogant), Friendly (but not ingratiating), Helpful (never overbearing), Clear, concise and human."_

Why it works: every attribute carries its own anti-attribute. Writers learn what to do AND what to avoid in the same memorable phrase. Without the "never Y" half, "confident" reads as a synonym for "cocky" to half the team.

For each attribute, produce **three** "we are X but we are not Y" statements during the BrandSort exercise. The triplet forces specificity — by the third statement, generic phrasing collapses and concrete language emerges.

**Bad** (generic, won't survive use):

- "We are friendly."
- "We are professional."

**Good** (specific, falsifiable):

- "Confident, never cocky."
- "Plainspoken, not patronising."
- "Warm, but never saccharine."

---

## Attribute documentation template

Each attribute in TONE.md follows this exact structure (downstream skills parse on it):

```
### N. <Attribute name>

**Definition:** <one line — what this attribute means in practice>

**Sounds like:** "<one example sentence in the voice>"

**Does not sound like:** "<one anti-example — generic, off-brand, or category default>"

**Do:**
- <concrete behaviour 1>
- <concrete behaviour 2>
- <concrete behaviour 3>

**Don't:**
- <concrete behaviour 1>
- <concrete behaviour 2>
- <concrete behaviour 3>

**Anti-example from past content:** "<actual past sentence that violated this attribute>"
```

**Why anti-examples from past content matter:** abstract anti-examples ("don't be too formal") fail to bite. Anti-examples sourced from the brand's own historical copy bite because writers recognise them — "oh, I wrote that exact sentence last quarter." This is where the guide stops being theatre and starts shaping behaviour.

---

## Worked attribute example

Drawn from a B2B SaaS context — adapt for the brand at hand.

```
### 1. Plainspoken

**Definition:** We say what we mean in the fewest credible words.

**Sounds like:** "Your invoice failed. Update your card to keep your subscription."

**Does not sound like:** "Unfortunately, we were unable to process the transaction at this time."

**Do:**
- Use active voice — name who does what.
- Lead with the most important fact.
- Use one idea per sentence.

**Don't:**
- Hedge ("perhaps", "potentially").
- Use insurance-language passives ("an error has occurred").
- Stack qualifiers ("we are currently unable to potentially process...").

**Anti-example from past content:** "It has come to our attention that, in some cases, certain customers may have experienced..."
```

---

## NN/g 4 dimensions

Nielsen Norman Group's measurement layer for voice. Four spectra, each a 3-point scale (or 5-point if you want finer granularity):

| Dimension | One end | Other end | Default for most brands |
| --- | --- | --- | --- |
| Funny ↔ Serious | Funny | Serious | Lean serious; reserve funny for moments of relief |
| Formal ↔ Casual | Formal | Casual | Most modern brands lean casual |
| Respectful ↔ Irreverent | Respectful | Irreverent | Respectful unless the brand is Outlaw archetype |
| Enthusiastic ↔ Matter-of-fact | Enthusiastic | Matter-of-fact | Matter-of-fact for B2B trust; enthusiastic for D2C |

**Use case:** plot the brand on all four dimensions. Plot 3-5 competitors on the same chart. Look for clustering — if you're at the same coordinates as two competitors, your voice is not differentiating. Move at least one dimension.

**Anti-pattern:** clustering near the midpoint on all four dimensions. Per Quasa.io's diagnosis: _"teams defaulting to mid-range scores (4-7), result in bland, forgettable voices."_ If three dimensions are at midpoint, the brand has no voice.

**Empirically grounded:** NN/g research shows tone of voice measurably affects perceived friendliness, trustworthiness, and desirability. On average, **52% of the variability in desirability scores is explained by trustworthiness** — meaning trust-building tone dimensions (matter-of-fact, plainspoken, respectful) pay more than charm.

---

## Jung's 12 archetypes

Strategic personality alignment with audience psychology. Each archetype maps to a core motivation — pick the one whose audience your buyer most resembles.

| Archetype | Core motivation | Example brands |
| --- | --- | --- |
| **Innocent** | Safety, simplicity, optimism | Coca-Cola, Dove |
| **Sage** | Truth, knowledge, mastery | Stripe (docs), Harvard, BBC |
| **Explorer** | Freedom, discovery, autonomy | Patagonia, Jeep, REI |
| **Outlaw / Rebel** | Disruption, freedom, revolution | Harley-Davidson, Liquid Death, Oatly |
| **Magician** | Vision, transformation | Apple, Disney, Tesla |
| **Hero** | Mastery, courage, achievement | Nike, FedEx, Patagonia (also) |
| **Lover** | Intimacy, beauty, pleasure | Chanel, Godiva, Häagen-Dazs |
| **Jester** | Joy, play, mischief | Old Spice, Mailchimp, Duolingo (TikTok) |
| **Everyman** | Belonging, realism, equality | IKEA, Target, Budweiser |
| **Caregiver** | Service, compassion, protection | Johnson & Johnson, Volvo, charity: water |
| **Ruler** | Control, leadership, prosperity | Rolex, Mercedes-Benz, Microsoft (enterprise) |
| **Creator** | Self-expression, craft, innovation | Lego, Apple (also), Adobe |

**Use caveats:**

1. Most brands lead with one archetype and borrow from one adjacent (e.g. Apple = Magician primary, Creator secondary).
2. Archetype is a positioning shortcut, not a voice solution. Two "Hero" brands can sound completely different (Nike vs FedEx). Don't stop at the archetype label — derive concrete voice attributes from it.
3. Brands that lean too hard on archetype end up in cosplay. The archetype should inform decisions, not become a costume.

---

## BrandSort / message architecture

Margot Bloomstein's exercise (_Content Strategy at Work_, Morgan Kaufmann, 2012) for surfacing brand attributes through a card-sort:

1. Use a deck of ~100 brand-attribute adjective cards (or generate a list).
2. Sort each card into one of three piles: **who we are now**, **who we'd like to be**, **who we are not**.
3. Narrow the "who we'd like to be" pile to ~9 cards.
4. Group those 9 into three clusters of three; pick the strongest from each cluster.
5. The top 3 are the message architecture and the seed for voice attributes.

**Run with a cross-functional group of 6-10 people**: leadership, marketing, sales, customer success, product writing, support, HR. The disagreements between groups are diagnostic — surface them explicitly rather than averaging them out.

**Reconcile** by running BrandSort three times:

1. Once with leadership
2. Once with the writing team
3. Once with sales / customer success (who hear how customers actually talk)

Differences between the three runs reveal where the brand's self-image diverges from its operational reality. Force a decision in the room rather than letting it persist as ambiguity in the guide.

---

## Brand-as-person exercise

A forcing function for concreteness. If the brand were a person at a dinner party:

- Job, age range, hobbies?
- What do they read?
- Who do they admire?
- How do they introduce themselves?
- What do they refuse to talk about?
- What do they wear?

For B2B brands, substitute "ideal colleague" or "celebrity spokesperson" — Slack explicitly aims to be _"an ideal colleague"_. This frames voice as a relationship the brand has with the reader, not an abstract personality.

**Output:** one paragraph describing this person. Then check: does the brand actually sound like this person in its current content? If not, that gap is what TONE.md is for.

---

## Frameworks compared

| Framework | What it gives you | Where it falls short |
| --- | --- | --- |
| **NN/g 4 dimensions** | Measurable axes; comparable profiles; falsifiable decisions | Misses culture and lexicon; can produce average outputs if everyone clusters near midpoint |
| **Mailchimp voice/tone** | Cleanest articulation of voice/tone distinction; mature documentation pattern | Specific to a SaaS context; not a discovery method |
| **Jung's 12 archetypes** | Strategic personality alignment; audience psychology link | Often used too literally; archetypes become cosplay |
| **"We are / We are not"** | Forces specificity; produces usable do/don't pairs | Easy to write trivially ("we are friendly but not unfriendly") if not facilitated |
| **Voice attributes with do/don't tables** | The operational atom of any modern guide | Without examples, becomes abstract |
| **Tone spectrums** (Builtvisible / Adobe Spectrum) | Channel-by-channel modulation made visible | Maintenance burden if too many spectrums |
| **Margot Bloomstein's BrandSort** | Stakeholder alignment; prioritised attributes; basis for content audit | Outputs are inputs; still need lexicon, examples, modulation matrix |
| **GV Brand Sprint (3 Circles)** | Speed; useful for early-stage startups | Lightweight; not a substitute for the full method |

**No single framework is sufficient.** Combine: BrandSort for stakeholder alignment, NN/g 4 dimensions for differentiation, "X but never Y" for documentation, archetype as positioning shortcut. Each addresses a different stage of the work.
