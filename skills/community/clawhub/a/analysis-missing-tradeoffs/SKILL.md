---
name: analysis-missing-tradeoffs
description: Analysis presents a single option without comparing alternatives or articulating the costs of the chosen approach.
emoji: ⚖️
metadata:
  clawdis:
    os: [macos, linux, windows]
---

# analysis-missing-tradeoffs

An analysis that skips comparison reads as advocacy, not analysis. The reader can't tell whether you considered and rejected alternatives or simply didn't see them, so they can't trust the recommendation.

## Symptoms

- Analysis proposes one approach and frames it as obviously correct.
- Costs and limitations of the chosen approach are not discussed.
- No mention of alternatives that a knowledgeable reader would have considered.
- Conclusion reads "we should do X" with no "rather than Y because Z".

## What to do

- Enumerate at least two viable options. If only one is viable, say why the others were eliminated.
- For each option, list what you gain and what you give up. Costs include complexity, risk, cost of reversal, team unfamiliarity — not just performance numbers.
- State the decision criteria up front: what matters most here (latency? cost? time to ship? blast radius?). Apply the criteria consistently across options.
- Show your work. The reader should be able to change one assumption and see which option wins.
- When the right answer is genuinely obvious, still name the alternatives and dismiss them briefly. Obvious-to-you is not obvious-to-everyone.
