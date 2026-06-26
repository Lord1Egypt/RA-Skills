---
name: brand-voice
description: Generate marketing copy, landing pages, email sequences, and social media posts with consistent brand voice. Use when asked to "write copy", "draft a landing page", "email sequence", "tagline", "headline", "social post", "marketing content", or "A/B test variants". Supports multiple brands with per-brand reference files.
---

# Brand Voice

Marketing copy generation with framework-driven consistency. User-first, transformation-focused, always with a clear CTA.

## Instructions

### Step 1: Identify the Brand
Determine which brand this is for, then load its reference file from `references/`.

Each brand file should contain: identity, tagline, ICP (ideal customer profile), customer psychology, tone, key messages, and anti-patterns.

See `references/cyberdyne-systems.md` for an example brand file.

### Step 2: Pick the Right Framework

Match the copy framework to what you're writing:

| Content Type | Framework | When to Use |
|-------------|-----------|-------------|
| Landing page hero | **PAS** (Problem → Agitate → Solve) | When the audience feels the pain already |
| Email sequence | **AIDA** (Attention → Interest → Desire → Action) | Nurturing cold leads to conversion |
| Social posts | **Hook → Value → CTA** | Short-form engagement |
| Feature announcement | **FABE** (Feature → Advantage → Benefit → Evidence) | When you have proof/numbers |
| Comparison/competitive | **BAB** (Before → After → Bridge) | Showing transformation |
| Testimonial page | **Social proof cascade** | When you have customer stories |

### Step 3: Apply Copy Principles
1. **User-first voice:** "You can..." not "Acme allows..."
2. **Specificity sells:** "200 attendees" beats "large events"
3. **Transformation > features:** What does their life look like after?
4. **Social proof:** Real humans, real results
5. **Clear next step:** Every piece has one CTA
6. **Hook first:** Reason to care in the first second

### Step 4: Customer Psychology
Always ask before writing:
- "Who is this actually for?" — no "generic user"
- "What's the transformation?" — features → life after
- "What's the hook?" — find it before writing

### Step 5: Deliver with Variants
Every deliverable includes:
1. **Headline** (2-3 A/B variants)
2. **Subheadline** (supports the hook)
3. **Body copy** (transformation-focused)
4. **CTA** (single, clear action)
5. **Hypothesis** — why this version should work

### Step 6: Platform Adaptation
Adapt the same message for different platforms:

| Platform | Constraints | Style |
|----------|------------|-------|
| Landing page | No length limit | Full narrative, multiple sections |
| Email | Subject line < 50 chars | Personal, conversational, one CTA |
| X/Twitter | 280 chars | Punchy, hook-first, link in bio |
| LinkedIn | 3000 chars | Professional, story-led, insight-driven |
| Discord | No markdown tables | Bold + bullets, casual tone |

## "This / Not That" — Universal Rules

| ✅ This | ❌ Not That |
|---------|-----------|
| "You'll have a site live in 10 minutes" | "Our platform enables rapid deployment" |
| "200 parents signed up in one weekend" | "Our solution drives high adoption rates" |
| Specific numbers and names | Vague superlatives ("best", "powerful", "revolutionary") |
| Customer language | Product language |
| One CTA per piece | Multiple competing CTAs |
| Earned confidence | Hype or desperation |

## Adding New Brands

Create a new file in `references/` following this structure:

```markdown
# [Brand Name] Brand Guide

## Identity
- **Domain:** example.com
- **Tagline:** "Your tagline here"
- **ICP:** Who is the ideal customer?
- **Market:** Geographic or demographic focus

## Customer Psychology
- **Primary driver:** What motivates the purchase?
- **Fear:** What are they afraid of?
- **Aspiration:** What do they want to become?

## Voice & Tone
- **Personality:** [e.g., confident but approachable]
- **Register:** [e.g., casual professional]
- **Unique phrases:** [brand-specific language]

## Key Messages
1. [Primary value prop]
2. [Secondary value prop]
3. [Social proof angle]

## Anti-Patterns (Never Do This)
- [Brand-specific mistakes to avoid]
```

## Gotchas
- **Generic copy is worse than no copy** — If you can swap in any competitor's name and it still works, the copy is too generic. Rewrite with product-specific details.
- **Framework mismatch kills conversion** — PAS on a feature announcement feels manipulative. FABE on a cold email feels robotic. Match the framework to the content type.
- **Don't mix brand voices** — Each brand has its own personality. Writing Brand A copy in Brand B's voice confuses both audiences.
- **CTA competition** — Two CTAs on one page split attention and reduce conversion. Pick the one that matters most.
- **Load the brand reference every time** — Don't rely on memory. Brand details drift. Read the file.
