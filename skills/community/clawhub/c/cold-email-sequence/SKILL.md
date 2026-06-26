---
name: cold-email-sequence
description: Generate personalized cold email sequences with follow-ups. Supports multiple frameworks (AIDA, PAS, BAB), A/B variants, and merge-field personalization. Pairs with lead-gen-research for full outreach automation.
metadata:
  version: 1.0.0
  author: TKDigital
  category: Sales & Marketing
  tags: [cold email, outreach, sales, email sequence, B2B, prospecting]
---

# Cold Email Sequence Skill

Generate complete cold email campaigns — personalized sequences with follow-ups, A/B variants, and framework options.

## What It Does

1. **Sequence Generation** — Creates 3-5 email sequences with timed follow-ups
2. **Framework Selection** — AIDA, PAS, BAB, or custom frameworks per email
3. **Personalization** — Merge fields for prospect-specific details (name, company, trigger event, pain point)
4. **A/B Variants** — 2 subject line variants + 2 body variants per email
5. **Follow-Up Logic** — Timed follow-ups with value-add content, not just "bumping this"
6. **Deliverability Tips** — Spam-trigger warnings, length optimization, formatting guidance

## Usage

### Generate a Full Sequence
```
Create a 5-email cold outreach sequence:

Service: AI-powered content production for agencies
Target: Marketing agency owners (10-50 employees)
Price point: $2,000-5,000/month retainer
Unique value: 10x content output without hiring writers
Social proof: Helped 3 agencies scale from 15 to 50+ posts/week

Include:
- Email 1: Cold intro (trigger-based)
- Email 2: Value-add follow-up (case study)
- Email 3: Social proof (results)
- Email 4: Objection handler
- Email 5: Breakup email

Give me 2 subject line variants per email.
Timing: 0, 3, 7, 14, 21 days
```

### Quick Single Email
```
Write a cold email:
To: [Title] at [Company type]
Offering: [Your service]
Trigger: [Recent event — funding, hire, launch]
Tone: Direct, no fluff
Length: Under 100 words
```

### Personalize for Prospect List
```
I have these prospects from my research:
1. Sarah Chen, CMO at DataFlow (just raised Series B)
2. Mike Torres, VP Marketing at CloudScale (hiring 3 content writers)
3. Lisa Park, Founder at GrowthLab (competitor just launched similar product)

Write personalized Email 1 for each using the trigger events.
Service: AI content production
```

## Output Format

```
## Email [#] — [Purpose]
**Timing**: Day [X] after previous email
**Framework**: [AIDA/PAS/BAB]

### Subject Line A:
[Subject]

### Subject Line B:
[Subject]

### Body (Variant A):
Hi {{first_name}},

[Email body with merge fields]

[Signature]

### Body (Variant B):
[Alternative approach]

### Notes:
- Spam check: [Any flags]
- Optimal send time: [Recommendation]
- Expected reply rate: [Benchmark]
```

## Frameworks

### AIDA (Attention → Interest → Desire → Action)
Best for: First cold emails to warm prospects

### PAS (Problem → Agitate → Solve)
Best for: Pain-point heavy industries, urgent problems

### BAB (Before → After → Bridge)
Best for: Transformation-focused services, case study emails

### QVC (Question → Value → CTA)
Best for: Short follow-ups, LinkedIn messages

## Deliverability Guidelines

- Subject lines: 4-7 words, no ALL CAPS, no excessive punctuation
- Body: Under 150 words for cold emails, under 100 for follow-ups
- No images in first email
- Max 1 link (and not in email 1 if possible)
- Plain text format beats HTML for cold outreach
- Personalize first line — generic openers kill deliverability scores
- Avoid: "just following up", "touching base", "I hope this finds you well"

## References

- `references/frameworks-detailed.md` — Deep dive on each email framework
- `references/subject-line-formulas.md` — 25 proven subject line patterns
- `references/spam-triggers.md` — Words and patterns that trigger spam filters
