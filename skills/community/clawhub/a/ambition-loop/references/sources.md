# Sources and credits

This skill is an independent implementation. It turns the ideas in the essay below into an executable agent workflow. All wording here is our own, apart from short quotations marked as such.

## Primary source
- **Felix Rieseberg**, "How to be more ambitious: A tutorial for humans with models", published 13 October 2026.
  https://felixrieseberg.com/how-to-be-more-ambitious-a-tutorial-for-humans-with-models/
  - Ideas taken: ambition as Speed / Altitude / Depth / Range; the QBR ladder; "keep our apps crash-free"; using expert instruments rather than expert vocabulary; unreasonable targets presented as reasonable (10 s → 200 ms); challenging assumptions against raw data; producing new knowledge validated on unseen data; an outside judge instead of self-grading; noun-to-verb reframing (credited there to Tom Kelley and Jonathan Littman, *The Art of Innovation*); assembling a crew that includes adversaries, without role-play; the self-efficacy argument.
  - The four-question "deeper, not bigger" prompt that Step 3 adapts comes from that essay.
  - Short quotations used: "the goal beyond the goal"; "deeper version of this task, not a bigger one"; "Don't ask the model to write like a short seller, ask it to do what a short seller does".
- Chinese translation (Liangziwei / QbitAI, WeChat): https://mp.weixin.qq.com/s/DSkimaN8KLtSRI0UFNFaPA

## Research cited by the essay (see self-efficacy.md)
- Edwin Locke and Gary Latham, goal-setting theory: a review of roughly 35 years of research finding that specific, difficult goals outperform "do your best".
- Albert Bandura, self-efficacy (the psychological construct the essay names).
- Patrick Collison's "Fast" list (https://patrickcollison.com/fast).
- W. Timothy Gallwey, *The Inner Game of Tennis*.
- Anecdotes in the essay: George Dantzig's "homework" problems; Roger Bannister and the four-minute mile.

## What this skill adds beyond the essay
The essay is written for the human who prompts. This skill makes the agent do that work itself and then carry it through. It adds a fit check that decides when *not* to escalate, explicit approval gates, a mandatory setup step (data, environment, judge, baseline), a persistence rule (no lowering the target, at least two distinct approaches, honest reporting), per-claim external verification, and a final gap report against both the literal ask and the ambitious target.

## Related prior work (not copied)
Many skills based on the same essay appeared in October 2026, for example DannyMac180/skills `be-ambitious`, wanderingspirit03/ambition-skill, robonuggets/be-ambitious, and ClawHub `@abhione/ambition`. None of their text was copied here.

## Sibling version
This folder is the English counterpart of `ambition-loop-zh` (Simplified Chinese). Both keep the same workflow, gates and step numbers. When you change one, update the other.
