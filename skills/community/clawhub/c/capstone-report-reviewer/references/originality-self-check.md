# Originality Self-Check (similarity risks)

## Four high-risk passage types and fixes

| High-risk passage | Why it duplicates | Fix |
|----------|------------|------|
| Chip introductions ("The STM32F103 is a…") | Everyone paraphrases the same datasheet | Only parameters relevant to *this* design, plus selection rationale |
| Method descriptions | Template sentences | Your own diagrams + measured data do the talking |
| Literature review | Synthesis clichés recur | Every claim lands on a specific paper's specific finding |
| Principle explanations (sensor theory etc.) | Textbook prose | Rewrite in context: "in this design, it is used to…" |

## Three similarity reducers

1. **Bind every descriptive paragraph to your own measurement/screenshot** — "measured 3.28 V vs 3.30 V theoretical, 0.6% deviation" cannot be similar to anything
2. **Redraw schematics/flowcharts yourself** — never screenshot datasheets (avoids similarity and stays sharp)
3. **Interrogate sentence by sentence** — for each suspect sentence ask: "is this how *I* would say it?"

## Note on AI writing detection

Turnitin-style detectors flag statistical patterns (perplexity/burstiness), not truth. Your best protection is not evasion tools — it is process evidence: version history, drafts, prompts saved, and the ability to explain every sentence in a viva. Write your own prose; use AI for structure feedback only, and disclose it.
