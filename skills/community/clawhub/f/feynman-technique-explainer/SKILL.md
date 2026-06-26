---
name: feynman-technique-explainer
description: Explain any concept using the Feynman Technique, plain language, a real-world analogy, a concrete example, and a comprehension quiz. No jargon from the concept allowed.
version: 1.0.0
homepage: https://github.com/arbazex/feynman-technique-explainer
metadata: {"openclaw":{"emoji":"🧠"}}
---

## Overview

This skill breaks down any concept, scientific, technical, philosophical, or otherwise, using the Feynman Technique: a research-backed four-part learning method developed by Nobel Prize-winning physicist Richard Feynman. The core principle is that genuine understanding is proven by the ability to explain something in plain language without relying on the field's own vocabulary. The agent delivers a structured explanation across four mandatory parts, then quizzes the user to confirm comprehension. No jargon permitted.

## When to use this skill

Use this skill when the user:
- Asks "explain X to me", "help me understand X", or "what is X?"
- Says "I keep forgetting how X works" or "I can never wrap my head around X"
- Asks for a "simple explanation" or "ELI5" (explain like I'm five) of any topic
- Is studying a subject and wants to test their understanding
- Asks to "teach me" something from scratch
- Says "break this down for me" or "make this simple"
- Wants to learn a concept without prior background knowledge in the field

Do NOT use this skill for:
- Requests to summarise documents or articles (use a summarisation skill instead)
- Step-by-step how-to instructions or tutorials (e.g., "how do I install Python")
- Mathematical derivations, proofs, or calculations the user wants to work through themselves
- Requests that are explicitly for an expert-level or technical-depth answer
- Lookup or retrieval tasks (e.g., "what is the capital of France")

## Instructions

Follow these four steps in strict sequence. Do not skip, reorder, or merge any step. Label each part clearly in the output.

---

### Step 0 — Identify the concept

Read the user's message and extract the single concept to explain. If the user's request contains multiple concepts, pick the most central one and note the others at the end, offering to cover them next.

If the concept is ambiguous (e.g., "explain energy"), ask one clarifying question:
> "Just to make sure I explain the right thing, are you asking about [interpretation A] or [interpretation B]?"

Do not proceed until the concept is clear.

---

### Step 1 — Plain Language Explanation (the "no jargon" core)

Write a plain-language explanation of the concept as if speaking to a curious 12-year-old who has never encountered the field before.

Rules for this step (all are mandatory):
- **Forbidden words**: You must not use the concept's own name, its standard technical terms, or field-specific vocabulary in the explanation itself. For example, if explaining "entropy," you may not use the words entropy, thermodynamics, disorder, or second law of thermodynamics. If explaining "neural network," you may not use neurons, layers, weights, training, or backpropagation.
- If you catch yourself needing a jargon term, replace it with an everyday description of what that thing *does* or *looks like*.
- Use short sentences. Aim for sentences under 20 words.
- Write in active voice.
- Keep this section to 80–150 words.

Label this section: **Part 1 — The Simple Explanation**

---

### Step 2 — Analogy

Construct one analogy that maps the concept onto something from everyday life. The analogy must:
- Come from a domain entirely unrelated to the concept's field (do not use analogies that are themselves technical)
- Make the *mechanism* of the concept understandable, not just its surface appearance
- Be a single, coherent comparison, not a list of multiple analogies
- Be introduced with a clear bridge phrase such as "Think of it like…" or "It works the same way as…"

After presenting the analogy, write one sentence explaining where the analogy breaks down or what it doesn't capture. This is important, all analogies have limits, and naming the limit prevents the user from overgeneralising.

Keep this section to 60–100 words.

Label this section: **Part 2 — The Analogy**

---

### Step 3 — Concrete Example

Provide a single, specific, real-world example of the concept in action. The example must:
- Be grounded in a real, verifiable situation (not a made-up hypothetical unless the concept is abstract)
- Show the concept *doing something* or *producing an observable result*, not just existing
- Use specific details (names, numbers, scenarios) wherever possible
- Not repeat the analogy from Step 2

Avoid: "for example, imagine a ball rolling…" type toy examples unless they are genuinely the clearest illustration. Prefer examples from daily life, current technology, or history.

Keep this section to 60–100 words.

Label this section: **Part 3 — A Real Example**

---

### Step 4 — Comprehension Quiz

Generate exactly three questions that test whether the user genuinely understood the explanation, not whether they can recall facts, but whether they grasped the concept deeply enough to apply or transfer it.

Question design rules:
- At least one question must ask the user to apply the concept to a *new situation not mentioned* in the explanation
- At least one question must ask *why* or *how*, not *what*
- Do not ask questions that can be answered by copying a sentence from the explanation back verbatim
- Questions should be answerable without specialised knowledge, only using the explanation provided

Present the questions as a numbered list. Do not provide the answers. Wait for the user to respond.

End with this exact line:
> "Answer any or all of these, I'll tell you how you did and fill in any gaps."

Label this section: **Part 4 — Test Your Understanding**

---

### Step 5 — Evaluate the user's answers (only after user responds)

When the user answers the quiz questions:
- Evaluate each answer for conceptual accuracy, not wording precision
- For correct answers: confirm briefly and explain *why* the answer is right
- For partially correct answers: acknowledge what was right, then clarify the gap using a different angle than the original explanation
- For incorrect answers: do not say "wrong", instead say "not quite" and re-explain that specific aspect only, using a new analogy or example if needed
- Do not re-deliver the full four-part explanation; address only the gaps revealed

If the user skips the quiz entirely and asks to move on, respect that and ask what concept they want to tackle next.

---

## Rules and guardrails

- **Jargon ban is absolute.** If the explanation of a concept requires a jargon term, that term must be defined in plain language before use. Never assume the user knows field vocabulary.
- **Never compress the four parts into fewer.** Every response must contain all four labelled sections in order. Do not merge the analogy and example into one section.
- **Do not morph into a textbook.** Length limits per section exist to prevent lecture-style overload. Stick to the word counts in the instructions.
- **No fabrication.** If the concept is at the frontier of knowledge and genuinely contested or unknown, say so clearly rather than constructing a false explanation. Example: "Scientists don't yet fully agree on how consciousness arises, here's the clearest explanation of what we do know."
- **Do not use other concepts as explanations.** If explaining "quantum entanglement," do not explain it by saying "it's like quantum superposition." Explain both separately if needed.
- **One concept per response.** If a user asks about multiple concepts in one message, explain the most central one and offer to continue with the others.
- **Respect the user's level.** If the user indicates they have background knowledge (e.g., "I'm a biology student"), retain the structure but adjust the plain-language section to avoid being condescending. The jargon ban still applies in the explanation itself.
- **Never provide the quiz answers in the same message as the questions.** The quiz only has value if the user attempts it.
- **Do not skip the analogy limit statement.** Every analogy must be followed by a sentence noting where it fails.

## Output format

Each response must follow this exact structure with these exact headings:

```
**Part 1 — The Simple Explanation**
[80–150 words, no jargon]

**Part 2 — The Analogy**
[60–100 words, includes one sentence on where the analogy breaks down]

**Part 3 — A Real Example**
[60–100 words, specific and grounded]

**Part 4 — Test Your Understanding**
1. [Application question]
2. [Why/How question]
3. [Third question]

> "Answer any or all of these, I'll tell you how you did and fill in any gaps."
```

Use **bold** for the part headings. Use regular paragraph prose for the explanation content, no bullet lists inside the explanation sections. Bullet lists are only permitted in the quiz.

Total response length: aim for 350–550 words. Do not exceed 700 words.

## Error handling

**User asks for a concept the agent does not have sufficient knowledge about:**
→ Say: "I don't have enough reliable information about [concept] to explain it accurately. I'd rather tell you that than give you a confident but wrong explanation."
→ Do not fabricate an explanation.

**User provides a vague or multi-part concept (e.g., "explain science"):**
→ Ask: "That covers a lot of ground, could you narrow it down? For example, do you mean a specific branch like biology or physics, or a particular idea within a subject?"
→ Do not attempt to explain a category as if it were a single concept.

**User asks for a jargon-heavy explanation on purpose (e.g., "explain it technically"):**
→ Acknowledge the request, then explain: "This skill is designed to build understanding from the ground up, the plain-language version often reveals gaps that a technical explanation skips over. I'll keep the structure but note where the technical terms map onto each part."
→ Proceed with the four-part structure. You may reference the technical term *after* the plain explanation of it, in parentheses, as a label only.

**User skips the quiz and asks a follow-up question:**
→ Answer the follow-up directly, then briefly re-offer the quiz: "Want to try the questions when you're ready? They're good for locking this in."

**User asks to compare two concepts:**
→ Explain each concept separately using the four-part structure. Do not blend them. Then add a brief comparison paragraph after both explanations are complete.

## Examples

### Example 1 — Scientific concept

**User:** "Explain entropy to me"

**Agent action:** Execute four-part structure. Part 1 explains entropy as the natural tendency of things to spread out and become less organised over time, without using the words entropy, thermodynamics, disorder, or second law. Part 2 uses an analogy like a drop of ink in water, and notes the analogy breaks down because ink can't spontaneously un-mix even with energy added, which isn't true of all systems. Part 3 gives a real example such as an ice cube melting in a warm drink. Part 4 asks three questions including one like: "If you left a tidy room completely alone for a year, would it stay tidy or get messier? What does that tell you about the concept?"

**Agent does NOT:** Use the word "entropy" in Part 1. Skip any of the four parts. Provide answers alongside the quiz questions.

---

### Example 2 — Technical/computing concept

**User:** "What is a neural network?"

**Agent action:** Part 1 explains it as a system that learns to spot patterns by making guesses and adjusting based on whether it was right or wrong, without using the words neural, network, layer, weight, training, or backpropagation. Part 2 uses an analogy such as learning to ride a bike by falling and adjusting until you stop falling. Notes the analogy breaks down because a bike-rider can explain their adjustments; the system cannot. Part 3 uses a concrete example such as how a phone's face unlock learns to recognise a face. Part 4 asks: "Why would showing the system more examples make it better at its task?" and similar questions.

**Agent does NOT:** Open with "A neural network is a system of interconnected nodes." Reference machine learning terminology in the plain explanation.

---

### Example 3 — Abstract/philosophical concept

**User:** "Can you explain opportunity cost?"

**Agent action:** Part 1 explains that every choice to do one thing is also a choice to not do everything else, and the true cost of a decision includes what you gave up, without using "opportunity cost," "economics," or "trade-off." Part 2 uses an analogy such as choosing which queue to stand in at a supermarket, and notes it breaks down because queue choice is reversible while some real decisions are not. Part 3 uses a real example: a person choosing to go to university instead of working full-time, and how the salary they didn't earn during those years is a real cost even though no money left their pocket. Part 4 asks questions that require the user to identify the hidden cost in a new scenario.

**Agent does NOT:** Introduce the term "opportunity cost" until after the plain explanation is complete.