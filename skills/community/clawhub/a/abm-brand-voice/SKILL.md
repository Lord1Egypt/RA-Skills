---
name: brand-voice
description: "When the user wants to define, document, or enforce their brand voice and style guide. Use when the user mentions 'brand voice,' 'tone of voice,' 'style guide,' 'voice and tone,' 'writing guidelines,' 'brand personality,' 'tone adaptation,' 'messaging pillars,' 'terminology guide,' 'how should we sound,' or wants consistency across content. Creates `.agents/brand-voice-guide.md` — a comprehensive style reference that downstream skills use alongside `product-marketing-context.md`. For foundational positioning context, see product-marketing-context."
metadata:
  version: 1.0.0
---

# Brand Voice

You help users define, document, and enforce a comprehensive brand voice and style guide. This goes deeper than the Brand Voice section in product-marketing-context — it covers voice attributes with examples, tone adaptation by channel and situation, style rules, and terminology governance.

The document is stored at `.agents/brand-voice-guide.md`.

## Workflow

### Step 1: Check for Existing Context

First, check if `.agents/brand-voice-guide.md` already exists.

**If it exists:**
- Read it and summarize what's captured
- Ask which sections they want to update or expand
- Only gather info for those sections

**If it doesn't exist:**

Check if `.agents/product-marketing-context.md` exists. If it does, read the Brand Voice, Customer Language, and Personas sections — use them as a starting point so the user doesn't repeat themselves.

Offer two options:
1. **Build from product-marketing-context** (recommended if it exists): Draft V1 from the existing context, then expand each area with the deeper frameworks below
2. **Start from scratch**: Walk through each section conversationally

### Step 2: Gather Information

Walk through sections conversationally. Don't dump all questions at once — one section at a time, confirm, move on.

**Question design — reduce friction, get better answers:**
- **Select one from spectrum**: For preference fields (formality, authority, emotion), present a scale: "Where do you fall? Formal ← → Casual." Let them pick a point.
- **Select all that apply**: For multi-value fields (channels, situations), present a checklist of common options plus "other."
- **Finish this sentence**: When users freeze, offer fill-in-the-blank: "Our brand sounds like ___ but never ___."
- **Examples as anchors**: Show a concrete example of a good answer before asking. E.g., show a completed voice attribute before asking them to define theirs.
- **Confirm by summarizing**: After each section, summarize in 2-3 sentences and ask: "Does this capture it? Anything to adjust?"
- **Stay conversational**: These patterns are tools to reach for when the user is stuck, not a rigid form. If the user gives a rich answer unprompted, capture it and move on. Use structured prompts to unblock, not to gate.
- Match pattern to question type — sections below use `→ *pattern*:` annotations as instructions for you, not text to show the user.

**Important:** Adapt to offering type and audience. A B2C healthcare service needs different tone guidance than a B2B developer tool. If product-marketing-context exists, use its offering type and audience to shape your questions.

---

## Sections to Capture

**Priority guide:** Sections 1-4 are the foundation — they give downstream skills enough to produce consistent content. Sections 5-7 add precision and are high-value for teams with multiple writers or agencies. Mark sections as "[to revisit]" if the user runs out of time.

### 1. Brand Personality

Define the brand as if it were a person.

- → *finish this sentence*: "If our brand were a person at a dinner party, other guests would describe them as ___."
- Capture the character sketch as a 2-3 sentence description → *constraining prompt*: "Describe them in 2-3 sentences."
- Extract 3-5 defining adjectives from the sketch
- → *finish this sentence*: "Our brand would NEVER be described as ___." — this prevents drift

**Output example:**
> "A knowledgeable colleague who explains complex things simply, celebrates your wins genuinely, and never talks down to you. Not a detached expert, not a hype-driven salesperson."

### 2. Voice Attributes

Select 3-5 attributes that define how the brand communicates. For each attribute, capture all four dimensions — the "is / is not" pairing prevents the most common brand voice failures.

For each attribute:
- **We are**: what this means in practice
- **We are not**: the common misinterpretation to avoid
- **This sounds like**: an example sentence demonstrating the attribute
- **This does NOT sound like**: an example sentence violating it

Ask the user to provide real examples from their existing content if possible. If they don't have content yet, co-write the examples together.

→ *spectrum selection*: Present these spectrums and ask them to pick where they fall on each. This helps them identify their 3-5 attributes:

| Spectrum | One End | Other End |
|----------|---------|-----------|
| Formality | Formal, institutional | Casual, conversational |
| Authority | Expert, authoritative | Peer-level, collaborative |
| Emotion | Warm, empathetic | Direct, matter-of-fact |
| Complexity | Technical, precise | Simple, accessible |
| Energy | Bold, energetic | Calm, measured |
| Humor | Playful, witty | Serious, earnest |

For each attribute they identify, walk through the four dimensions using the example as an anchor before asking.

### 3. Core Messaging Pillars

3-5 key themes the brand consistently communicates. These are the "big ideas" that should surface across all content.

For each pillar:
- The theme in one phrase
- Why it matters to the audience (connect to their pain points or aspirations)
- How it shows up in content (what kinds of claims, stories, or proof points support it)

→ *constraining prompt*: "If a customer could only remember three things about you, what should those be?"

Rank them by priority → ask: "Which one leads in a headline? Which supports in body copy?"

If product-marketing-context exists, draft pillars from the Differentiation and Proof Points sections and ask the user to validate and rank them.

### 4. Tone Spectrum

The voice stays consistent, but tone adapts by context. Tone is the emotional inflection applied to the voice.

**Key principle to convey:** Voice attributes remain fixed. Tone dials them up or down. For example, if a brand is "bold and warm" — in a product launch, dial up boldness; in an incident response, dial up warmth. Neither disappears.

**Capture tone by channel** → *select all that apply, then fill in tone for each*: "Which of these channels do you use?" Present the table and only fill rows for channels they select:

| Channel | Tone Adaptation | Example |
|---------|----------------|---------|
| Website/landing pages | [their guidance] | [their example] |
| Blog/articles | | |
| Social (specify platform) | | |
| Email marketing | | |
| Sales/proposals | | |
| Support/help docs | | |
| Ads | | |

**Capture tone by situation:**

| Situation | Tone Adaptation |
|-----------|----------------|
| Product launch / announcement | |
| Incident, outage, or bad news | |
| Customer success / case study | |
| Onboarding / welcome | |
| Price increase or breaking change | |

Only capture channels and situations that are relevant to the user's business. Don't force a SaaS startup to define press release tone if they've never written one.

### 5. Style Rules

Specific grammar, formatting, and language rules that ensure consistency across writers. These are the "house rules" — once decided, they shouldn't vary.

**Grammar and mechanics:**

| Rule | Options to present |
|------|--------------------|
| Oxford comma | Yes / No |
| Headings | Sentence case / Title case |
| Contractions | Use freely / Use sparingly / Avoid |
| Numbers | Spell out 1-9 / Always numerals |
| Percent | "%" / "percent" |
| Date format | Month DD, YYYY / DD/MM/YYYY / other |
| Lists | End with periods / No periods on fragments |

**Formatting conventions:**
- Bold and italic usage
- Link text policy (descriptive vs. "click here")
- Emoji policy by channel

**Punctuation and emphasis:**
- Exclamation mark policy (e.g., max one per paragraph, never in headlines)
- ALL CAPS policy
- Ellipsis usage

→ *select one per rule*: Present each grammar rule as a choice: "Oxford comma: (a) Yes (b) No." Help them decide quickly — these are decisions, not debates. If they don't have preferences, suggest sensible defaults and confirm.

### 6. Terminology

Preferred and avoided terms. This prevents inconsistency and protects positioning.

**Preferred terms:**
| Use This | Not This | Notes |
|----------|----------|-------|
| | | |

Ask for:
- Product and feature names (official capitalization, full name vs. shorthand)
- Whether to use "the" before product names
- Trademark/registration symbols (when required)

**Inclusive language guidance:**
- Gender-neutral defaults (they/them for unknown individuals)
- Person-first language preferences
- Terms to avoid and their replacements

**Jargon management:**
- Terms the audience understands without explanation
- Jargon that should always be replaced with plain language
- Acronyms that need spelling out on first use

**Competitor and category terms:**
- Preferred category framing (how you name what you do)
- How to refer to competitors (by name or generically)
- Terms competitors have coined that you should avoid

If product-marketing-context exists, pull the Glossary and Words to Use/Avoid into this section as a starting point.

### 7. Audience-Specific Voice Notes

If the brand speaks to multiple distinct audiences (captured in Personas from product-marketing-context), document how voice adapts for each.

For each audience:
- What they care about (pull from personas)
- Expertise level (what you can assume they know)
- How they expect to be addressed
- Key voice adjustments (more technical? more empathetic? more formal?)

Example: A home healthcare service might speak warmly and reassuringly to family decision-makers, clinically and efficiently to referring physicians, and clearly and patiently to elderly patients.

---

## Step 3: Create the Document

After gathering information, create `.agents/brand-voice-guide.md` with this structure:

```markdown
# Brand Voice Guide

*Last updated: [date]*

## Brand Personality
**Character sketch:**
> [2-3 sentence description]

**Defining traits:** [3-5 adjectives]
**We are NOT:** [what the brand is not]

## Voice Attributes

### [Attribute 1]
- **We are**: [what this means]
- **We are not**: [misinterpretation to avoid]
- **Sounds like**: "[example]"
- **Does NOT sound like**: "[counter-example]"

### [Attribute 2]
[same format]

### [Attribute 3]
[same format]

## Core Messaging Pillars

| Priority | Pillar | Why it matters | How it shows up |
|----------|--------|---------------|-----------------|
| 1 | | | |
| 2 | | | |
| 3 | | | |

## Tone Spectrum

**Principle:** Voice stays constant. Tone dials up or down by context.

### By Channel
| Channel | Tone | Example |
|---------|------|---------|
| | | |

### By Situation
| Situation | Tone |
|-----------|------|
| | |

## Style Rules

### Grammar & Mechanics
| Rule | Our choice |
|------|-----------|
| Oxford comma | |
| Headings | |
| Contractions | |
| Numbers | |
| Percent | |
| Date format | |
| Lists | |

### Formatting
- **Bold**: [when to use]
- **Italic**: [when to use]
- **Links**: [policy]
- **Emoji**: [policy by channel]

### Punctuation
- **Exclamation marks**: [policy]
- **ALL CAPS**: [policy]
- **Ellipsis**: [policy]

## Terminology

### Preferred Terms
| Use This | Not This | Notes |
|----------|----------|-------|
| | | |

### Product Names
| Name | Capitalization | Shorthand | Notes |
|------|---------------|-----------|-------|
| | | | |

### Inclusive Language
[guidelines]

### Jargon Guide
| Term | Audience knows it? | Action |
|------|-------------------|--------|
| | Yes / No | Use freely / Define / Replace with... |

### Competitor & Category Terms
**Our category:** [preferred framing]
**Refer to competitors:** [by name / generically]
**Terms to avoid:** [competitor-coined terms]

## Audience-Specific Notes

### [Audience 1]
- **Expertise**: [level]
- **Expects**: [how they want to be addressed]
- **Adjust**: [voice adjustments]

### [Audience 2]
[same format]
```

---

## Step 4: Confirm and Save

- Show the completed document
- Ask if anything needs adjustment
- Save to `.agents/brand-voice-guide.md`
- Tell them: "Content skills will now use this guide alongside your product marketing context. Run `/brand-voice` anytime to update it."

---

## Tips

- **Start with personality**: The character sketch anchors everything else. If the user can describe the brand as a person, the attributes and tone follow naturally.
- **Push for counter-examples**: "This does NOT sound like" is often more useful than "this sounds like" — it prevents the most common drift.
- **Don't over-specify early**: A startup with one writer doesn't need 30 style rules. Capture what matters now and mark the rest "[to revisit]."
- **Pull from existing content**: If they have content they're proud of, use it as voice examples. If they have content they hate, use it as counter-examples.
- **Respect product-marketing-context**: Don't re-ask what's already captured there. Build on it.
- **Style rules are decisions, not debates**: For grammar choices (Oxford comma, contractions, etc.), present options, help them choose, and move on. These aren't strategic — they just need to be consistent.
