# Cognitive Science Appendix

Cognition is **inspired by** cognitive science. It does not claim to implement these theories literally.

The value of this appendix is framing: it explains why the skill is organized this way and what each part borrows from.

| Inspiration | Useful idea | How Cognition uses it |
|---|---|---|
| Episodic memory research | Recent experience should be captured before it fades | Daily logs as append-only session memory |
| Semantic memory | Durable knowledge benefits from compact indexing + deeper reference stores | `MEMORY.md` + `memory/bank/*.md` |
| Prospective memory | Intentions need explicit triggers or they get dropped | `memory/FUTURE_INTENTS.md` |
| Procedural learning | Repeated successes should become reusable procedures | `memory/procedures/` + maturity states |
| Metacognition | Agents should track confidence and uncertainty | coarse confidence bands + `[NEEDS_REVIEW]` |
| Retrieval cueing / spreading activation | Linked context improves recall | optional cross-references overlay |
| Consolidation / replay | Off-session review can promote durable patterns | nightly staged consolidation |
| Reflective practice | Periodic review improves judgment and maintenance | weekly reflection reports |

## Translation layer

The skill translates theory into simple operational rules:
- write important things down
- keep durable memory compact
- separate raw logs from promoted knowledge
- stage changes before mutating durable files
- track uncertainty explicitly
- turn repeated wins into procedures

If you want the science, keep it here.
If you want the skill to work, focus on the operational rules in `SKILL.md`.
