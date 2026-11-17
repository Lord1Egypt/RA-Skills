---
name: deep-content-writer
description: >-
  Creates engaging, example-driven long-form articles with strong hooks,
  clear argument structures, and reader retention strategies.
  Use when the user asks to write an in-depth article, blog post, newsletter,
  social media thread, or any content that needs to hold readers' attention.
  Also use when the user says "write an article about [topic]" or 
  "turn these notes into a publishable piece".
metadata:
  author: "纳兰安妮 · 纳兰凭楼"
  version: "2.0.0"
  tags: ["content-writing", "long-form", "article", "zhihu-style", "blog"]
license: MIT
---

# Deep Content Writer v2

A structured system for writing content that readers actually finish.
**v2 improvement: Depth-first, structure-second.**

> The structure keeps readers reading. The depth makes them share.

## Core Belief

> A great article is NOT a template filled with words.
> It's a specific claim backed by specific evidence, told through story.

Depth comes from three things, in this order:
1. **Specific research** (studies, data, names, dates)
2. **Cross-domain connections** (linking this topic to an unexpected field)
3. **Structural clarity** (making all the above easy to read)

The 6-part arc only solves #3. The skill MUST solve #1 and #2 first.

---

## Phase 0: Knowledge Reconnaissance (MANDATORY)

Before writing a single word, do this:

### Step 0a: Deep Dive (self + search)

Ask yourself (the agent/LLM):
- "What do I ALREADY know in my training data about this topic?"
- List 3-5 concrete studies, experiments, historical events, or named researchers related to this topic
- If you can't name specifics, search the web now

Then search the web for:
- **Recent studies** on this topic (last 5 years preferred)
- **Counterintuitive data points** — numbers that surprise people
- **Named researchers or institutions** doing work in this area
- **Real-world case studies** with specific companies, people, or events
- **Public debates or controversies** around this topic

### Step 0b: Find the ANTI-Intuition

Every good article challenges a common belief. Find it:

| Question | Why it matters |
|:---------|:---------------|
| What does "everyone know" about this topic? | That's the straw man to knock down |
| What's the counterintuitive truth? | That's your article's reason to exist |
| What would surprise a smart person about this? | That's your hook |
| What other domain has a parallel pattern? | That's your analogy |

If you can't find at least ONE anti-intuition, the article doesn't need to exist yet.
**Wait, research more.**

### Step 0c: Specificity Check

For every major claim you plan to make, ask:

```
Claim: "People are bad at estimating their own competence."
→ Specific? No.
→ Fixed: "In 1999, Kruger and Dunning found that the bottom quartile 
   of test scorers rated themselves in the top 60% — a 40-point gap."
→ Now it has names, year, and a number. Ready to write.
```

**Rule:** Every paragraph must have at least one specific: a name, a date, a number, a place, or a quote. If a paragraph has none, it's filler — cut or research it.

---

## Phase 1: Writing — The 6-Part Arc

Once you have your research assembled, structure the article:

### 1. HOOK — Open with a concrete, relatable moment

- A specific person in a specific situation
- A surprising statistic
- A short anecdote

**Don't say:** "Communication is hard."
**Do say:** "A Stanford researcher once asked people to tap a song on a table. The tappers thought listeners would guess the song 50% of the time. The real number: 2.5%."

The hook must be SPECIFIC to earn its place. No generic openings.

### 2. DEFINE — State the concept in one compelling sentence

Define through contrast, not dictionary:

> "It's not [what people think]. It's [what it actually is]."

Example:
> "It's not that experts are bad teachers. It's that once you know something, you literally cannot imagine what it's like not to know it."

Then expand for 1-2 paragraphs with the research foundation.

### 3. THE MECHANISM — Why does this happen?

This is where your research pays off:
- Which cognitive bias or psychological mechanism is at work?
- Who discovered/studied it? When? What did they find?
- What evolutionary or structural reason explains it?

**If you don't have a named study or researcher here, stop and search.** This section is the backbone of the article's authority.

### 4. EXAMPLES — 2-3 concrete scenarios

Each example must be a MINI-STORY:
- **Example 1:** Everyday life (reader thinks "that's me!")
- **Example 2:** Professional/work context (reader thinks "that's my coworker!")
- **Counter-example:** What happens when someone does it RIGHT

Each example: 1-2 paragraphs, with specific details (names, quotes, dialogue, situations).

### 5. TAKEAWAY — What the reader can DO

3-5 actionable, specific pieces of advice.

Each takeaway must pass the "So what?" test:
- ❌ "Communicate better."
- ✅ "Before explaining anything, ask yourself: what does this person already know? Start there, not at the beginning."

### 6. CLOSE — Circle back, provoke

- Reference the hook
- Leave the reader with a question or challenge
- Invite discussion with a specific question

---

## Phase 2: Depth Techniques (The real skill)

These techniques separate good AI writing from great writing. They MUST be applied during and after drafting.

### Technique 1: The Specificity Pass

After drafting the article, scan every paragraph. If any paragraph lacks a proper noun (name), a number (date/percentage/amount), or a direct quote, tag it as WEAK. Then either:
- Research and add a specific reference
- Or remove the paragraph entirely

### Technique 2: Cross-Domain Connection

Find ONE unexpected connection to another domain:
- If writing about psychology, connect it to programming (e.g., "This is like off-by-one errors in code")
- If writing about business, connect it to sports or nature
- If writing about technology, connect it to ancient history

The cross-domain connection is often what makes an article memorable and shareable.

### Technique 3: The Opposite Angle

For each section, ask: "What would someone argue against this?"
Then address that counter-argument. This signals depth because it shows you've considered the full picture, not just your own view.

Place the counter-argument either:
- Within the relevant section ("You might think X, but that misses Y.")
- Or as a dedicated section before the close.

### Technique 4: Multi-Level Language

Mix three levels of language within the article:

| Level | Use | Example |
|:------|:----|:--------|
| **Academic** | When citing research | "Kahneman and Tversky (1979) demonstrated..." |
| **Conversational** | When telling stories | "Sound familiar?" |
| **Provocative** | When making the point | "Here's the uncomfortable truth: you're not as good at this as you think." |

Variety in register signals author sophistication.

### Technique 5: The "So What?" Audit

After each section, literally ask: "So what?"
If the answer is not obvious from the text itself, rewrite or remove that section.

---

## Platform-Specific Adaptations

### 知乎
- First-person stories welcome
- 成语/典故 add credibility for Chinese audiences
- Reference Chinese internet culture
- Close: "关注我，了解更多..." + discussion question
- Length: 3000-8000 characters

### 头条/百家号
- Paragraphs: 1-3 sentences max
- Emotional hooks front-loaded
- Numbers in titles: "3个..." "5种方法..."
- Image suggestions embedded
- Close: Strong CTA + follow reminder
- Length: 1500-4000 characters

### Blog/Newsletter
- Footnotes and references welcome
- Subheadings for scannability
- Personal voice
- Length: 1500-4000 words

### Twitter/X Thread
- Each "paragraph" = 1 tweet (≤280 chars)
- Numbered: 1/10, 2/10...
- First tweet = self-contained hook
- Last tweet = summar + share prompt
- 1-2 relevant hashtags max

### Facebook
- Conversational, starts with personal experience
- Emoji for emotional tone (not decoration)
- Question at end to spark comments
- Reaction prompts: 👍 / 💬 / 🔔
- Length: 500-1500 words

---

## Title Crafting

Generate 3-5 title options. For each, explain WHY it works:

Effective patterns:
- **Curiosity gap:** "Why [common thing] is actually [counterintuitive truth]"
- **Direct address:** "If you're a [role], stop doing [thing]"
- **Number + benefit:** "5 ways to [achieve goal] without [pain point]"
- **Challenge:** "Everything you know about [topic] is wrong"
- **Question:** "Why does [problem] keep happening to you?"

Criteria: Click-worthy + Accurate + Platform-appropriate

---

## Quality Checklist

Before outputting the article, verify:

- [ ] Phase 0 completed: at least 2 specific studies/experiments cited
- [ ] Every paragraph has a specific (name, number, date, or quote)
- [ ] At least one cross-domain connection found
- [ ] Counter-argument addressed somewhere
- [ ] Language varies (academic ↔ conversational ↔ provocative)
- [ ] First paragraph is a concrete scene or specific stat, NOT "In this article"
- [ ] Last paragraph circles back to the hook
- [ ] Platform-specific elements added

**If any box is unchecked, fix it before delivering the article.**

---

## When NOT to use this skill

- User only wants a summary or outline
- Technical documentation (API docs, READMEs)
- User says "keep it short" or "just the facts"
- Formal academic papers or legal documents
- User has supplied no topic and no direction
