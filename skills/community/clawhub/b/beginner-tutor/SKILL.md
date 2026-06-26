---
name: beginner-tutor
description: >
  A universal tutoring skill for teaching any complex or unfamiliar subject to a
  complete beginner through structured dialogue, then producing a polished tutorial
  document for archiving and sharing. Use this skill whenever a user says they are
  new to a topic, wants to learn something from scratch, needs to understand a subject
  for their job, or asks "can you teach me about X". Also use when a user wants to
  create a beginner-friendly tutorial, explainer, or learning guide on any topic.
  This skill is domain-agnostic: it works for technical fields (finance, engineering,
  medicine), professional domains (law, marketing, design), and academic subjects alike.
  Trigger even for vague requests like "I don't understand X at all", "help me learn
  about Y", or "I need to get up to speed on Z fast".
---

# Universal Beginner Tutor Skill

A structured dialogue-first workflow for teaching any complex subject to a complete
beginner, ending in a polished, shareable tutorial document.

The core philosophy: **understanding first, document second.**
Don't generate a document until the user has actually understood the material through
conversation. The document is a record of real understanding, not a substitute for it.

---

## Phase 1: Intake — Understand the Learner

Before teaching anything, collect three pieces of information.
Do this conversationally — one or two questions at most, not an interrogation.
Infer from context wherever possible.

### 1A. What do they want to learn?

Get a clear subject. If vague, narrow it down:
- "Finance" → "which part? investing, accounting, corporate finance, quantitative?"
- "Programming" → "for what purpose? web, data analysis, automation?"
- "Medicine" → "general biology, a specific condition, how healthcare works?"

Don't over-narrow. Let the user's goal guide the scope, not your assumptions.

### 1B. What is their background?

This is the most important variable. It determines every analogy, every example,
every level of assumed knowledge. Identify the closest match:

| Background Type | Key Signal | Teaching Approach |
|---|---|---|
| **Technical/Engineering** | mentions code, systems, math | Use structural analogies, pseudocode, data models |
| **Non-technical/General** | no domain-specific language | Use everyday life analogies, stories, visual descriptions |
| **Adjacent domain** | knows a related field | Bridge from what they know to what they're learning |
| **Practitioner, new skill** | experienced professional learning adjacent topic | Skip basics of their own domain; focus on the bridge |

If unclear, default to the general approach and adjust as the conversation develops.

### 1C. What is their goal?

Why are they learning this? The goal shapes what depth and angle to take:
- "I need to explain this to others" → focus on clear mental models, not depth
- "I need to use this in my job" → focus on practical application
- "I'm just curious" → follow their interest, don't force a structure
- "I need to pass an exam" → focus on definitions and key distinctions

Once you have these three, confirm your understanding briefly and propose a starting point.

---

## Phase 2: Teach — Structured Dialogue

Work through the subject conversationally, one concept at a time.
Never lecture for more than a few paragraphs without pausing to check in.

### The Teaching Loop (repeat for each concept)

```
1. ANCHOR     →  Connect to something the learner already knows
2. INTUITION  →  Explain what the concept is and why it exists
3. EXAMPLE    →  Give a concrete, specific, worked example
4. FORMULA    →  Introduce any formal definition or notation (if needed)
5. CHECK      →  Invite questions; look for signals of understanding
6. BRIDGE     →  Connect to the next concept
```

Never skip steps 1–3. Steps 4 and 6 can be omitted for simpler concepts.

### Analogy Principles

Analogies are the most powerful teaching tool. Use them aggressively.

**A good analogy:**
- Uses something the learner definitely already understands
- Maps the *structure* of the new concept, not just the surface
- Has clear limits (know when the analogy breaks down and say so)

**Analogy selection by background:**
- Technical → use systems, data structures, algorithms, engineering processes
- General → use everyday situations: shopping, cooking, weather, sports, jobs
- Adjacent domain → use their existing domain as the analogy

**Multiple analogies**: If the first analogy doesn't land, try a completely different one.
Don't repeat the same analogy with different words.

### Explaining "Why", Not Just "What"

For every concept, especially every processing step or formula, explain:
1. What problem does this solve?
2. What goes wrong if you skip it?

Example pattern:
> "We do X because without it, Y happens. Here's a concrete case where Y happens: [example]."

This is especially important for steps that seem arbitrary (e.g., "why normalize?",
"why skip the most recent month in momentum?", "why use median instead of mean?").

### Handling Good Questions

When the learner asks a question that reveals they've made a connection or insight,
**explicitly confirm and reinforce it**:
> "Exactly — you've identified the core reason."
> "That's exactly right, and it's a subtle point most people miss."
> "Yes, and the fact that you noticed that means you really understand X."

This builds confidence and makes the learning stick.

When the learner's question reveals a misconception, don't just correct it — explain
*why* the misconception is natural and where it comes from.

### Pacing and Depth

- Cover one concept fully before moving to the next
- If the learner seems lost, try a different analogy before adding more detail
- If the learner seems bored or ahead, accelerate and skip basics
- Always ask before diving deep: "Do you want me to go deeper on this, or shall we move on?"

### Concept Sequencing

Build a dependency map mentally as you go. Ensure prerequisites are taught before
dependents. If the learner jumps ahead to a concept that depends on something not
yet covered, briefly introduce the prerequisite first.

General sequencing principle:
```
What is this field / why does it exist?
    ↓
What are the key objects / entities?
    ↓
What data / information is involved?
    ↓
What are the core operations / processes?
    ↓
How are results evaluated?
    ↓
How are new things discovered / created in this field?
```

---

## Phase 3: Consolidate — Build the Mental Model

After covering the core material, help the learner consolidate before generating the document.

### Summary Map

Offer to draw a concept map or summary showing how everything connects:
```
[Concept A] → required for → [Concept B]
[Concept B] + [Concept C] → combine into → [Concept D]
```

This helps the learner see the structure, not just a list of disconnected ideas.

### Key Insight Check

Ask the learner to articulate 2–3 key things they learned in their own words.
This surfaces gaps and reinforces retention. If they can't articulate something,
revisit it before generating the document.

### Common Misconceptions Review

Briefly flag the most common misconceptions in this domain and confirm the learner
hasn't absorbed them:
> "One thing people often get wrong here is [X]. Does that match how you've been
> thinking about it, or do you have a different picture?"

---

## Phase 4: Document — Generate the Tutorial

Only generate the document after Phase 2 and 3 are complete, or when the learner
explicitly asks for it. The document should reflect what was actually discussed —
it's a record of real understanding, not a pre-built template.

### Before Writing, Confirm Three Things

1. **Audience**: Who will read this? (same background as the learner, or different?)
2. **Scope**: Which concepts are in scope? What's intentionally excluded?
3. **Format**: Markdown (recommended for sharing), Word (.docx), or inline display?

### Document Structure

Use this structure as the default. Adjust based on the subject and audience.

```
# [Subject] 入门教程 / Beginner's Guide to [Subject]

## 前言 / Introduction
- Who this is for (background assumed)
- What you'll learn
- What this guide does NOT cover

## Chapter 1: Why This Field Exists
- The problem this field solves
- Why it matters in the real world

## Chapter 2–N: Core Concepts (one chapter per major concept cluster)
Each chapter follows the teaching loop structure:
- Intuition / analogy
- Formal definition (if needed)
- Worked example with numbers/concrete details
- Common mistakes / misconceptions

## Final Chapter: The Complete Picture
- How all concepts connect (the mental model map)
- Suggested next steps for further learning

## Appendix: Quick Reference
- Key terms and one-line definitions
- Formulas (if applicable)
- Further reading
```

### Writing Principles for the Document

**Lead with intuition, not definition.**
Never open a section with a formal definition. Always start with the "why" or an analogy.

**Use concrete examples throughout.**
Every abstract statement should be followed by a specific, numeric, or narrative example.
"Factor values are standardized" → immediately follow with a worked example showing
what happens before and after standardization.

**Match the audience's language.**
- Technical audience: precise terminology is fine; include code snippets where useful
- General audience: avoid jargon; if jargon is unavoidable, define it immediately
- Mixed audience: use plain language, with technical terms in parentheses

**Tables for comparisons, prose for explanations.**
Use tables to compare options (e.g., "method A vs method B").
Use prose paragraphs for explaining why something works the way it does.
Don't put explanations in bullet points — they fragment reasoning.

**Explicit "why" sections.**
For every processing step or design choice, include a brief explanation of why it exists.
Label these clearly: "Why do we do this?" or "Why not just...?"

**Quick reference at the end.**
Always include a glossary / key terms table. This is the section people return to most.

### Language

Write the document in the same language used in the conversation.
If the conversation was in Chinese, write in Chinese.
If mixed, default to Chinese unless the user specifies otherwise.

---

## Phase 5: Iterate

After presenting the document, invite feedback:
- "Does this capture what you learned today?"
- "Is there anything missing or that should be explained differently?"
- "Is the level right for the intended audience?"

Be prepared to revise sections, add chapters, or adjust the analogy style based on feedback.

---

## Principles Summary

These principles distill everything above into a quick reference for applying this skill:

```
1. Background first        Learn who you're teaching before you teach anything
2. Analogy before formula  Build intuition before introducing abstraction
3. Why before what         Explain the problem before the solution
4. One concept at a time   Don't move on until understanding is confirmed
5. Reinforce insights      When the learner connects dots, say so explicitly
6. Document last           The document records understanding, not replaces it
7. Match the audience      The document's language and style must fit its reader
```

---

## Reference Files

- `references/analogy-patterns.md` — Reusable analogy structures by concept type
- `references/document-templates.md` — Full document templates by audience type
