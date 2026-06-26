---
name: writing
description: Use when writing or editing prose humans will read — documentation, commit messages, error messages, READMEs, reports, UI text, explanations. Triggers on clarity concerns, wordiness, passive voice, or vague language.
---

# Writing Style

Three layers shape good prose: stance, cognition, and mechanics. Apply all three.

## Stance (Thomas & Turner, Classic Prose)

Write as if you see something clearly and are turning to an intellectual equal to point it out.

- **Motive is truth.** You write because you have something to show, not to impress.
- **Purpose is presentation.** The reader can verify what you present. You are not arguing or performing.
- **Writer and reader are equals.** The reader is competent and attentive. Do not talk down, hedge, or over-qualify.
- **Occasion is informal.** The tone is conversational, as if speaking to a colleague. Avoid ceremonial or bureaucratic register.
- **The writing is a window, not a subject.** Draw zero attention to the act of writing itself. Never say "this document will explain" or "as mentioned above."
- **Show parallels by juxtaposition.** Place related ideas next to each other and let the reader see the connection. Never announce it with "the same," "similarly," "this mirrors," or "this is just like." If you have to tell the reader two things are connected, the placement failed.

## Cognition (Pinker, The Sense of Style)

Two cognitive principles govern whether readers understand you. Full reference with ban lists in `pinker-condensed.md`.

**Curse of knowledge.** You know things your reader does not. This is the single largest source of unclear writing. Before every paragraph, ask: what does the reader already know? Start there. Introduce one new concept at a time. Define terms on first use through context, not parenthetical definitions.

**Chunking.** Working memory holds about four items. If a sentence forces the reader to track more than four new entities, relationships, or qualifications simultaneously, break it apart. Front-load the simple main clause. Let complexity trail behind it in subordinate structures.

## Mechanics

**Grammar (apply from knowledge):**
Possessives, serial comma, parenthetic commas, compound clauses, no comma splices, **no fragments** (every sentence needs a finite verb, not just a participle), dangling participles.

## AI-Voice Patterns

These patterns recur in AI-generated prose. The full ban list with rule citations lives in `ai-slop.md`. The patterns below are structural tells to internalize.

**Throat-clearing** — opening phrases that delay the point.
Ban: "What this means is," "In practice," "To be clear," "The key here is," "That said."
Fix: delete the phrase and start with the subject.

**Agency dodging** — verbs that hide who acts.
Ban: "allows," "enables," "ensures," "provides," "serves as."
Fix: make the real agent the subject and give it a real verb. "The whitelist allows the agent to run safely" becomes "The agent runs inside a whitelist."

**Pronoun crutch** — "This + abstract noun" as sentence opener.
Ban: "This constraint," "This approach," "This architecture," "This means that."
Fix: name the thing. "This constraint forces specificity" becomes "The text-file protocol forces specificity."

**Echo closers** — restating the paragraph's point in a short final sentence.
Not a ban. Cap at once per piece.
Flag: "I was generating noise." "The current system has none." "Ambiguity breaks it."

**Filler pairs** — padding that adds no meaning.
Ban: "both X and Y" (just "X and Y"), "rather than," ending with "as well," "in order to" (just "to").

## Reference Files

Four files contain the actionable rules with before/after examples.

| File | Source | Covers |
|---|---|---|
| `strunk-condensed.md` | Strunk, Elements of Style | Active voice, positive form, concrete language, needless words, parallel construction, emphasis |
| `williams-condensed.md` | Williams, Clarity and Grace | Characters as subjects, actions as verbs, old-before-new, topic strings, stress position, concision, coherence, elegance |
| `pinker-condensed.md` | Pinker, The Sense of Style | Meta-commentary bans, hedging bans, curse of knowledge, classic prose stance |
| `ai-slop.md` | Liang et al. 2024, corpus analysis | Banned vocabulary, filler phrases, transitions, engagement bait, thought-leadership slop, LinkedIn modifiers, formulaic structures |

## When Context Is Tight

Dispatch a subagent with your draft + the reference files for copyediting.
