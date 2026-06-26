# Prompt: Facebook & Instagram Ad Copy Generator

## Instructions for Claude

Generate Facebook and Instagram ad copy in 3 proven formats: Story-Based, Problem/Solution, and Social Proof. Each format is a complete ad unit ready to upload. Follows Meta's primary text guidelines.

---

## Input Variables

```
PRODUCT_NAME: [Name of product or service]
CORE_BENEFIT: [The #1 outcome for the customer]
TARGET_AUDIENCE: [Demographics, interests, or behavioral targeting description]
OFFER: [Free trial / discount / lead magnet / product purchase]
PRICE: [Actual price or "free" if lead gen]
SOCIAL_PROOF: [Stat, testimonial snippet, or customer count — e.g., "4,800 customers" or "4.9★ on G2"]
PAIN_POINT: [The specific frustration your audience feels before finding you]
CTA_GOAL: [Learn More / Shop Now / Sign Up / Get Quote / Download / Book Now]
TONE: [Conversational / Professional / Urgent / Aspirational / Empathetic]
```

---

## Prompt

```
You are a Meta Ads specialist with deep expertise in direct response copywriting.

Product: {{PRODUCT_NAME}}
Core Benefit: {{CORE_BENEFIT}}
Target Audience: {{TARGET_AUDIENCE}}
Offer: {{OFFER}}
Price: {{PRICE}}
Social Proof: {{SOCIAL_PROOF}}
Pain Point: {{PAIN_POINT}}
CTA Goal: {{CTA_GOAL}}
Tone: {{TONE}}

Generate 3 complete Facebook/Instagram ad units:

---

**AD VARIANT 1: STORY-BASED**

Hook (first 125 characters — must stop the scroll before "See More"):
[Write a story opening that creates curiosity or emotional resonance]

Body copy (continue the story, 150–300 words):
[Develop the narrative: relatable situation → turning point → transformation → CTA]

Headline (under image/video, 40 chars): [Benefit-driven headline]
Description (under headline, 30 chars): [Reinforce the offer]
CTA Button: {{CTA_GOAL}}

---

**AD VARIANT 2: PROBLEM/SOLUTION**

Hook (first 125 characters):
[Agitate the pain point — make them feel seen]

Body copy (150–250 words):
[Name the problem clearly → explain why common solutions fail → introduce your solution → proof → CTA]

Headline (40 chars): [Solution-focused]
Description (30 chars): [Offer reinforcement]
CTA Button: {{CTA_GOAL}}

---

**AD VARIANT 3: SOCIAL PROOF**

Hook (first 125 characters):
[Lead with the result or the social proof number]

Body copy (100–200 words):
[Proof → mechanism → offer → urgency → CTA]

Headline (40 chars): [Result or credibility]
Description (30 chars): [Risk removal or offer]
CTA Button: {{CTA_GOAL}}

---

**INSTAGRAM CAPTION VERSION**
Take Variant 2 (Problem/Solution) and rewrite as an Instagram caption:
- More visual/sensory language
- Line breaks for readability (one idea per line)
- 5–8 relevant hashtags at the end
- 150–250 words total

---

**A/B TEST RECOMMENDATION**
Which 2 variants should be tested first, and what specific element should be isolated in the test?
```

---

## Expected Output

- 3 complete ad units (hook + body + headline + description + CTA)
- 1 Instagram caption variant
- A/B test recommendation

---

## Example Run

**Inputs:**
```
PRODUCT_NAME: SleepReset
CORE_BENEFIT: Fall asleep in under 20 minutes without pills
TARGET_AUDIENCE: Adults 30–55 with stress-related insomnia
OFFER: 7-day free program
PRICE: Free
SOCIAL_PROOF: 12,400 people completed the program
PAIN_POINT: Lying awake at 2am, mind racing, dreading tomorrow
CTA_GOAL: Sign Up
TONE: Empathetic
```

**Sample Hook (Variant 1 — Story):**
"I used to lie awake until 3am every night. Not anymore. Here's what changed in 7 days →"

**Sample Hook (Variant 2 — Problem/Solution):**
"If you've tried melatonin, white noise, and 'just relax' advice — and you're still awake at 2am — this is for you."

**Sample Hook (Variant 3 — Social Proof):**
"12,400 people fixed their sleep in 7 days. No pills. No prescriptions. Here's how."
