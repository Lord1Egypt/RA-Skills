# Prompt: LinkedIn Ads Copy Generator

## Instructions for Claude

Generate LinkedIn advertising copy for three formats: Sponsored Content, Lead Gen Form, and InMail. LinkedIn's audience is professional — copy must be credible, specific, and business-outcome focused.

---

## Input Variables

```
PRODUCT_NAME: [Name of product or service]
CORE_BENEFIT: [The #1 business outcome — use metrics where possible]
TARGET_ROLE: [Job title(s) you're targeting, e.g., "VP of Sales, Sales Directors"]
TARGET_COMPANY_SIZE: [Company size range, e.g., "100–1,000 employees"]
TARGET_INDUSTRY: [Industry or industries]
OFFER: [What they get by clicking — demo, whitepaper, free audit, trial]
PAIN_POINT: [The professional challenge your audience faces]
SOCIAL_PROOF: [Customer logos, case study result, user count, award]
SENDER_NAME: [Name for InMail — your name or company name]
TONE: [Professional / Thought Leadership / Data-Driven / Direct]
```

---

## Prompt

```
You are a LinkedIn B2B advertising specialist. Write copy for a LinkedIn campaign targeting {{TARGET_ROLE}} at {{TARGET_COMPANY_SIZE}} companies in {{TARGET_INDUSTRY}}.

Product: {{PRODUCT_NAME}}
Core Benefit: {{CORE_BENEFIT}}
Offer: {{OFFER}}
Pain Point: {{PAIN_POINT}}
Social Proof: {{SOCIAL_PROOF}}
Tone: {{TONE}}

---

**FORMAT 1: SPONSORED CONTENT (Single Image or Document Ad)**

Intro text (max 150 characters — appears above the image):
[Professional hook that speaks to the pain point or outcome]

Headline (max 70 characters):
[Benefit or offer-focused headline]

Description (max 100 characters, shown on desktop):
[Reinforce the value, include a call to action]

Body copy for document/carousel caption (100–200 words):
[Explain the problem, tease the solution, build credibility with social proof, end with clear CTA]

---

**FORMAT 2: LEAD GEN FORM**

Form headline (max 60 characters):
[Make the value exchange clear — what they get]

Form description (max 160 characters):
[Why this is worth 30 seconds of their time]

Privacy policy note (max 160 characters):
[How you'll use their information — builds trust]

Thank-you message (max 300 characters):
[What happens next — set expectations, add value]

Custom questions (suggest 2–3 qualifying questions relevant to {{TARGET_ROLE}}):
[Questions that both qualify the lead and feel relevant to them]

---

**FORMAT 3: LINKEDIN INMAIL (Sponsored Messaging)**

Subject line (max 60 characters):
[Curiosity + relevance — must not feel like a mass blast]

Opening line (personalized-feeling, 1–2 sentences):
[Reference something specific to their role/industry — shows you know their world]

Body (150–250 words):
[Problem acknowledgment → credibility signal → offer → specific benefit → CTA]

CTA Button text (max 20 characters):
[Action-oriented, specific to the offer]

P.S. line (optional but high-converting):
[One additional reason to click or a risk reversal]

---

**CAMPAIGN STRATEGY NOTES**
- Recommended objective (Awareness / Lead Gen / Website Visits): [Recommendation with rationale]
- Best ad format for this offer: [Single Image / Document / Video / Carousel — with reason]
- Audience targeting tip: [1 specific LinkedIn targeting recommendation for this ICP]
- Bid strategy: [CPM for awareness / CPC for conversion — recommendation]
```

---

## Expected Output

- Sponsored Content (intro + headline + description + body)
- Lead Gen Form (all fields + 2–3 custom questions)
- InMail (subject + opening + body + CTA + P.S.)
- Campaign strategy notes

---

## Example Run

**Inputs:**
```
PRODUCT_NAME: Forecastly
CORE_BENEFIT: Reduce revenue forecast error by 60%
TARGET_ROLE: VP of Sales, Revenue Operations Directors
TARGET_COMPANY_SIZE: 200–2,000 employees
TARGET_INDUSTRY: B2B SaaS
OFFER: Free 30-minute pipeline accuracy audit
PAIN_POINT: Sales forecasts are off by 20–30% every quarter — board loses confidence
SOCIAL_PROOF: Used by 340 B2B SaaS teams, average forecast error reduced from 28% to 11%
SENDER_NAME: Alex Chen
TONE: Data-Driven
```

**Sample Sponsored Content Intro:**
"Your Q2 forecast is probably wrong by 20%. Here's how 340 SaaS teams fixed it."

**Sample InMail Subject:**
"Your Q2 forecast — quick question"

**Sample InMail Opening:**
"Running revenue forecasting at a SaaS company means owning the number in front of the board every quarter — and that number is almost always wrong by more than you'd like to admit."
