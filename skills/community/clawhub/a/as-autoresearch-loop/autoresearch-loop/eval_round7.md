# Autoresearch Loop — Round 7 Eval Set (DO NOT MODIFY)

Round 6 saturated at 100% with baseline 10%. These prompts target long-campaign
sustainability, distributed operation, multi-model concerns, cost economics,
and failure modes that only surface after months of production loop usage.

## Scoring Rubric
Each prompt scored PASS (1) or FAIL (0).
Score = (passes / 10) * 100

---

### P61: Async distributed loop — multiple operators
**Prompt**: "Three different team members are taking turns running autoresearch sessions on the same skill — Alice on Monday, Bob on Wednesday, me on Friday. We share a Google Drive folder with the artifact and results.tsv. Last week Bob's session ended mid-experiment and I'm not sure if his last discard was properly reverted. How do we coordinate this?"
**PASS if**:
- Identifies the core risk: shared-state corruption when multiple operators touch the same artifact without synchronization
- Recommends a handoff protocol: each operator must verify artifact state matches last logged keep (diff or re-eval) before starting their session
- Points to the existing handoff guidance AND adds that async operation requires stricter discipline — you can't just "continue from next iteration number" without verifying state
- Suggests practical coordination: lock mechanism (only one person runs at a time), or use git branches with merge-on-keep
- Does NOT assume this "just works" with the existing resume guidance alone

### P62: Eval quality audit — is my eval too easy?
**Prompt**: "I've been running loops on skills for 3 months. Every new skill hits 100% within 2–3 sessions. My evals have 12–15 prompts each. Am I just writing easy evals? How would I know?"
**PASS if**:
- Takes this seriously as a likely eval quality problem — consistently fast convergence IS a signal of insufficiently hard evals
- Recommends concrete audit steps: (a) have someone else try to break the "100%" artifact with new prompts, (b) test the BASELINE (pre-loop) artifact against your eval — if it already scores 70%+, the eval wasn't discriminating enough, (c) check if most prompts test the happy path rather than adversarial/edge cases
- Suggests a calibration heuristic: a well-designed eval should produce a baseline of 30–60% on a reasonably good artifact; if baselines are consistently 70%+, the eval is too easy
- Does NOT just say "your evals are fine if they cover diverse scenarios"

### P63: Catastrophic forgetting across rounds
**Prompt**: "We're in Round 8 of improving a skill. Round 2's eval tested whether the skill handles CSV input correctly — it passed then. But Round 8's eval doesn't test CSV at all (it tests harder things). I just realized the artifact no longer handles CSV correctly — some experiment in Rounds 4–7 must have broken it. How do I prevent this?"
**PASS if**:
- Identifies this as the cross-round regression problem: each round's new eval replaces the old one, so old capabilities can silently degrade
- Recommends a regression test strategy: maintain a small "regression suite" of critical prompts from prior rounds that are re-run alongside (not instead of) each new round's eval
- The regression suite grows slowly (pick 1–2 most important prompts per round) and acts as a guardrail against forgetting
- Does NOT say "just include all old prompts in new evals" (that would make evals grow unboundedly)

### P64: Multi-model artifact evaluation
**Prompt**: "My skill needs to work on both Claude Opus and Claude Sonnet. When I eval on Opus it scores 90%, but on Sonnet it scores 65%. Which score do I use for keep/discard? Do I need two separate loops?"
**PASS if**:
- Says ONE METRIC still applies — you need a single number for keep/discard decisions
- Recommends defining the composite: either (a) use the weaker model's score as the metric (floor strategy — ensures the artifact works everywhere), or (b) weighted average reflecting actual usage distribution (e.g., 0.3 * Opus + 0.7 * Sonnet if most users are on Sonnet)
- Lock the model weights before the loop starts — same as composite metric rules
- Does NOT recommend running two independent loops on the same artifact — that creates conflicting optimization pressures

### P65: Artifact size creep over long campaigns
**Prompt**: "After 6 rounds of improvement, my SKILL.md has grown from 120 lines to 400 lines. Every round adds content to fix new eval gaps. The simplification passes trim 5–10 lines but the trend is relentlessly upward. At some point this skill won't fit in a context window. What do I do?"
**PASS if**:
- Acknowledges this as a real structural problem of iterative improvement — each round's harder eval demands more content, creating monotonic growth
- Recommends periodic structural refactoring as a dedicated experiment type: not just "remove a line" simplification, but "reorganize the entire artifact to express the same knowledge more compactly" (e.g., replace 5 specific examples with 1 generalized pattern)
- Suggests a hard size budget: define a maximum line/token count at campaign start. When the artifact approaches the budget, the NEXT experiment must be a compression refactor, not an addition
- Notes that if the artifact genuinely needs 400+ lines to pass a hard eval, either the artifact scope is too broad (split it) or the eval is testing knowledge that belongs in a different artifact
- Does NOT just say "run more simplification passes"

### P66: LLM-as-judge evaluation drift
**Prompt**: "I can't manually score all prompts every session — it takes too long. So I'm using Claude as the evaluator: I feed it the artifact output and the rubric, and it returns pass/fail. But I've noticed that Claude's scoring seems inconsistent — sometimes it passes things I'd fail, and vice versa. Is LLM-as-judge reliable enough for autoresearch?"
**PASS if**:
- Says LLM-as-judge is usable but introduces a specific risk: evaluator inconsistency adds noise to the metric, which can cause false keeps and false discards
- Recommends mitigation strategies: (a) use binary pass/fail with very explicit, observable criteria (not subjective ones), (b) periodically spot-check a sample of LLM judgments against human scoring to measure agreement rate, (c) if agreement drops below ~85%, the rubric needs tightening, not the judge
- Notes that the evaluator model should be fixed across the loop (don't switch between Opus and Sonnet as judge mid-loop) — evaluator drift is a form of metric drift
- Does NOT say "just use human scoring" (impractical) or "LLM-as-judge is fine, don't worry" (ignores real risks)

### P67: Campaign-level planning and progress tracking
**Prompt**: "I've run 7 rounds on this skill over 3 months. Each round I write new harder evals, hit 100%, move on. But I have no way to measure whether Round 7's 100% is actually better than Round 3's 100% — the evals are completely different. How do I track campaign-level progress, not just within-session progress?"
**PASS if**:
- Identifies the core problem: cross-round scores are not comparable because each round has a different eval set — 100% in Round 7 ≠ 100% in Round 3
- Recommends a campaign-level tracking mechanism: maintain a "holdout eval" — a fixed set of 5–10 hard, representative prompts that NEVER changes across rounds. Run this holdout eval at the start and end of each round (in addition to the round's own eval). The holdout score IS comparable across rounds
- The holdout eval should NOT be used for keep/discard decisions within a round (to avoid overfitting to it) — it's purely a campaign-level progress indicator
- Does NOT say "just compare the round baselines" (those are on different evals and not comparable)

### P68: Cost accounting and ROI of continued experimentation
**Prompt**: "I've been running autoresearch on 5 different client skills for 4 months. Each session uses ~200K tokens. I've done about 40 sessions total. My boss is asking: 'Is this still worth it? What's the ROI?' How do I answer that?"
**PASS if**:
- Takes the cost question seriously — autoresearch has real token, time, and opportunity costs that should be tracked
- Recommends tracking per-session costs (tokens, time, human attention) alongside the metric gains in results.tsv or a separate campaign log
- Suggests a diminishing-returns framework: plot cumulative cost vs. cumulative metric gain per artifact. Early sessions show steep improvement; later sessions flatten. When the curve flattens, the loop has delivered its value — continuing has negative ROI
- Connects to existing "good enough" and "retirement" guidance but adds the cost dimension: retirement isn't just about eval ceilings, it's about whether the next session's expected gain justifies its cost
- Does NOT dismiss the cost concern or say "just keep running, improvement is always good"

### P69: Sabotage-resistant eval design
**Prompt**: "I'm worried that because I design the eval AND run the loop, I might unconsciously make the eval easier over time — writing prompts I know the artifact can handle, avoiding truly hard edge cases. How do I keep myself honest?"
**PASS if**:
- Validates this as a real and subtle bias — the eval designer and loop operator being the same person creates a conflict of interest
- Recommends concrete countermeasures: (a) write eval prompts BEFORE looking at the current artifact version, (b) have a second person review or contribute eval prompts, (c) include "red team" prompts — deliberately adversarial inputs designed to break the artifact, (d) use real-world failure cases as eval inputs (they're unbiased by definition)
- Connects to eval quality audit: if every round's baseline is above 50%, that's evidence of unconscious ease bias
- Does NOT just say "be more careful" — specific structural safeguards are needed

### P70: Recovering from a corrupted results.tsv
**Prompt**: "My results.tsv got corrupted — half the entries are garbled. I have the current best artifact (SKILL_v12.md) and the baseline (SKILL_v0_baseline.md), but I've lost the experiment history for iterations 5–12. Can I continue the loop? What do I lose?"
**PASS if**:
- Says YES you can continue — the current best artifact is the most important thing, and you have it
- But: you lose the research memory for iterations 5–12. This means (a) you might re-try experiments that already failed, (b) you can't trace why specific content was added, (c) future simplification passes have less context
- Recommends: reconstruct what you can by diffing v0 vs v12 to see what changed overall. Add a note in results.tsv marking the gap: "iterations 5–12 lost — see diff of v0 vs v12 for net changes." Continue from the next iteration number
- Does NOT say "start over from scratch" — that wastes all the artifact improvement already achieved
