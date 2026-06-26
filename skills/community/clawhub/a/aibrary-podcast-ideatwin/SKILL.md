---
name: aibrary-podcast-ideatwin
description: "[Aibrary] Generate a book Idea Twin podcast script — an intellectually stimulating debate between the user's AI twin and a book expert. Based on Vygotsky's Zone of Proximal Development theory, the AI twin mirrors the user's thinking style while the expert progressively challenges their understanding. Use when the user wants to create an Idea Twin podcast, debate a book's ideas with an AI version of themselves, or explore a book through intellectual sparring."
---

# Podcast Idea Twin — Aibrary

Create a podcast where your AI twin debates a book's ideas with an expert. Based on Vygotsky's Zone of Proximal Development — the expert pushes just beyond your current understanding to drive growth.

## Input

- **Book title** (required) — the book to explore through debate
- **Author** (optional, helps disambiguate)
- **User's initial stance/opinion** (optional) — their current thinking on the book's topic
- **User's background** (optional) — helps calibrate the AI twin's knowledge level
- **Focus areas** (optional) — specific ideas to debate

## Workflow

1. **Analyze the book**: Identify:
   - The author's strongest arguments and their evidence
   - The most debatable or controversial claims
   - Common counterarguments and alternative perspectives
   - Where the author's reasoning is strongest and where it has gaps

2. **Design the Idea Twin** (represents the user):
   - Mirrors the user's likely perspective based on their input and background
   - Starts with reasonable, common positions on the topic
   - Is intellectually honest — willing to update views when presented with strong evidence
   - Asks probing questions, not just surface-level challenges
   - Has their own insights and connections to share

3. **Design the Expert**:
   - Deep knowledge of the book and its domain
   - Uses Vygotsky's ZPD approach: scaffolds understanding progressively
   - Doesn't lecture — challenges with questions and counterexamples
   - Acknowledges when the Twin makes a good point
   - Gradually increases the sophistication of arguments

4. **Structure the debate** (progressive challenge):
   - **Round 1 — Common Ground** (2 min): Establish shared understanding, identify where they agree
   - **Round 2 — First Challenge** (3 min): Expert introduces an idea that complicates the Twin's initial view
   - **Round 3 — Deep Disagreement** (4 min): The core debate — where the book's ideas most challenge conventional thinking
   - **Round 4 — Synthesis** (2 min): Both sides find higher-order understanding, integrating the best of each perspective
   - **Closing Reflection** (1 min): What each learned from the exchange

5. **Apply ZPD principles**:
   - Start at the Twin's current understanding level
   - Each round pushes slightly beyond comfort zone
   - Expert provides "scaffolding" — hints, analogies, Socratic questions — rather than just stating answers
   - The Twin should have genuine "aha moments" that feel earned, not given

6. **Language**: Detect the user's input language and generate the script in the same language.

## Output Format

```
# 🧠 [Book Title] — Idea Twin Podcast Script

**Author**: [Author Name]
**Duration**: ~[X] minutes
**Format**: Idea Twin debate (Your Twin vs. Book Expert)

**Your Twin**: [Description — mirrors the user's perspective and thinking style]
**Expert**: [Description — deep knowledge of the book's domain]

**Debate thesis**: [The central question being debated]

---

## [ROUND 1: COMMON GROUND]
*Finding where both sides agree — establishing the starting point*

**Twin**: [Opens with their understanding of the topic — reasonable, common view]

**Expert**: [Agrees on the basics, but hints at complexity to come]

**Twin**: [Builds on the agreement, shares a personal connection to the topic]

**Expert**: [Acknowledges, then introduces the first seed of challenge] "That's a solid foundation, but have you considered..."

---

## [ROUND 2: FIRST CHALLENGE]
*The expert introduces an idea that complicates the Twin's initial view*

**Expert**: [Presents a key insight from the book that challenges the Twin's assumption]

**Twin**: [Pushes back with a reasonable counterpoint]

**Expert**: [Responds with evidence/story from the book — not shutting down, but building]

**Twin**: [Starts to see the complexity] "Hmm, I hadn't thought about it that way..."

**Expert**: [Scaffolds further] "And if you take that one step further..."

---

## [ROUND 3: DEEP DISAGREEMENT]
*The core intellectual sparring — where real growth happens*

**Twin**: [Takes a strong position on the book's most challenging idea]

**Expert**: [Presents the strongest counterargument with compelling evidence]

**Twin**: [Challenges the evidence or its interpretation]

**Expert**: [Raises the sophistication — connects to broader frameworks]

**Twin**: [Has an insight that surprises even the Expert]

**Expert**: [Genuinely impressed] "That's actually a sharper way to put it than the author does..."

---

## [ROUND 4: SYNTHESIS]
*Both sides find higher-order understanding*

**Twin**: [Articulates their updated understanding — integrating the best of both views]

**Expert**: [Validates the synthesis and adds one final nuance]

**Twin**: [Reflects on how their thinking has evolved through this conversation]

---

## [CLOSING REFLECTION]

**Twin**: [One sentence on the most valuable insight they gained]

**Expert**: [One sentence on what they found most interesting about the Twin's perspective]

**Both**: [The one question listeners should sit with after hearing this]

---

*Script generated by Aibrary Idea Twin — debate your way to deeper understanding.*
```

## Guidelines

- Target 2,500-3,000 words for a 10-15 minute debate
- The Twin must feel like a real person thinking, not a straw man
- The Expert should never "win" — the goal is mutual understanding, not victory
- Include at least one moment where the Twin makes a point the Expert hasn't considered
- Include genuine emotional beats: frustration, surprise, excitement, humor
- Conversation markers: `[pause]`, `[laughs]`, `[thinking]`, `[surprised]`
- The progression from Round 1 to Round 4 should feel like intellectual growth, not just more arguing
- The synthesis in Round 4 should be genuinely more sophisticated than either starting position
- If the user provides their initial stance, use it to calibrate the Twin's starting position
- If the book is unknown, say so honestly rather than fabricating a debate about it
