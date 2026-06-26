# feynman-technique-explainer

An AI agent skill that explains any concept using the Feynman Technique, the learning method developed by Nobel Prize-winning physicist Richard Feynman, empirically validated to improve comprehension and knowledge retention over passive study methods.

---

## What it does

Given any concept, the agent produces a structured four-part breakdown:

1. **Plain explanation** — no jargon from the concept's own field allowed
2. **Analogy** — maps the concept onto everyday life, with an explicit note on where the analogy fails
3. **Concrete example** — a specific, real-world instance of the concept in action
4. **Comprehension quiz** — three questions designed to test understanding, not recall

After the user attempts the quiz, the agent evaluates answers and fills in any gaps.

---

## Installation

Add to your agent's skill list on [ClawHub](https://clawhub.ai) by searching `feynman-technique-explainer`, or place the `SKILL.md` file in your agent's skills directory.

No API keys, environment variables, or external dependencies required. The skill runs entirely on the agent's reasoning.

---

## Usage

Trigger phrases that activate this skill:

- "Explain X to me"
- "Help me understand X"
- "Break down X in simple terms"
- "ELI5: X"
- "I keep forgetting how X works"
- "Teach me X from scratch"

Works on any subject, science, technology, economics, philosophy, history, medicine, and more.

---

## What makes this different from a normal explanation

- **Jargon ban enforced.** The agent cannot use the concept's own vocabulary in the explanation. This forces genuine simplification rather than rewording.
- **Analogy limits named.** Every analogy is followed by a statement of where it breaks down, preventing oversimplification.
- **Quiz tests transfer, not recall.** Questions require applying the concept to new situations, not reciting the explanation back.

---

## Limitations

- Best suited for single, well-defined concepts. Very broad topics (e.g., "explain science") will prompt a clarifying question.
- Not a replacement for deep technical study, designed to build foundational understanding and identify knowledge gaps.
- For frontier or genuinely contested topics, the agent will flag uncertainty rather than fabricate an explanation.

---

## License

MIT