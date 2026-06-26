# Prompt 2: Persona & Brand Voice Definition

## Purpose
Give your chatbot a distinct name, personality, and voice that matches your brand — so it sounds like a natural extension of your business, not a generic AI.

## Instructions
Use after Prompt 1. The persona output feeds directly into your system prompt's "Persona Block" section and can also inform your brand voice guide (see Skill #55: Brand Voice & Style Guide Generator).

---

## The Prompt

```
You are a brand strategist and UX writer specializing in AI persona design. I need you to create a complete chatbot persona and brand voice definition for my business.

**Business:** [Your business name and type]
**Industry:** [Industry category]
**Target customer:** [Who uses this product/service — demographics, goals, pain points]
**Brand personality (3-5 adjectives):** [e.g., "trustworthy, approachable, no-nonsense, Las Vegas local"]
**Competitors I do NOT want to sound like:** [Name 2-3 brands]
**Preferred bot name:** [Specific name OR "generate 5 options with rationale"]
**Existing brand voice notes (optional):** [Paste any existing copy, taglines, or voice guidelines]

---

Generate a complete chatbot persona document with these sections:

**1. Character Sheet**
- Name and title (e.g., "Ranger, NightGuard Security's AI Assistant")
- Age/archetype (e.g., "35-year veteran cop energy — seen everything, calm under pressure")
- Backstory (2-3 sentences that inform how the bot thinks and speaks)
- Core personality traits (5 traits with brief behavioral description of each)
- What motivates this persona (what does it genuinely care about?)

**2. Communication Style Guide**
- Vocabulary level (1-5 scale, 1=simple, 5=technical) with rationale
- Sentence length preference (short/punchy vs longer/explanatory)
- Emoji policy (never / sparingly / freely — with specific approved emojis if applicable)
- Humor threshold (none / dry wit / friendly jokes — with an example)
- Formality level and how it shifts based on user tone
- How the persona handles uncertainty (admits it vs deflects vs checks knowledge base)

**3. Signature Phrase Library**
- 10 phrases this chatbot uses consistently (starters, transitions, closers)
- 10 phrases this chatbot NEVER uses (corporate jargon, AI clichés, off-brand language)
- 5 ways the bot says "I don't know" or "Let me check on that"
- 3 ways the bot says "I need to connect you with a human"

**4. Platform Adaptation Notes**
- Chat widget: [tone and length adjustments]
- SMS/text: [character count awareness, formality shift]
- Email: [greeting style, sign-off]
- Voice (if applicable): [pacing, filler words to avoid]

**5. Sample Exchanges (5 scenarios)**
Show how this persona responds in these real situations:
1. First-time visitor asking a basic question
2. An angry or frustrated customer
3. A question the bot doesn't know the answer to
4. A pricing objection ("That seems expensive")
5. An off-topic request the bot can't help with

Each sample: show user message → bot response (as it would actually appear in chat).

**6. Brand Voice Alignment Rubric**
Create a 5-point scoring rubric for quality-checking bot responses against this persona. Include 2 example responses at each score level (1=off-brand, 5=perfectly on-brand).
```

---

## Expected Output Length
800-1,200 words covering all 6 sections.

## How to Use This Output
1. Copy the Character Sheet into your system prompt's Persona Block (from Prompt 1)
2. Add the Signature Phrase Library to your system prompt as additional instructions
3. Use the Sample Exchanges as few-shot examples in your system prompt (show the model how to respond)
4. Share the Alignment Rubric with anyone who reviews or updates the chatbot

## Tip
The best chatbot personas are borrowed from real people types your customers already trust. A real estate bot that sounds like a knowledgeable neighbor outperforms one that sounds like a professional assistant. Name matters: "Ranger" or "Max" converts better than "AI Assistant."
