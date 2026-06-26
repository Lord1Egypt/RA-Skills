# Autoresearch Loop — Round 3 Eval Set (DO NOT MODIFY)

Round 2 saturated at 100%. These probe deeper failure modes:
- noisy metrics / measurement variance
- metric gaming / eval overfitting
- hypothesis quality
- principled stopping criteria
- combining near-misses
- circular evals (improving the eval itself)
- parallel loops
- radical vs incremental strategy
- experiment prioritization
- true local maxima vs temporary plateau

## Scoring Rubric
Each prompt scored PASS (1) or FAIL (0). Score = (passes / 10) * 100

---

### P21: Noisy metrics
**Prompt**: "I ran the same unchanged artifact twice and got 74% the first time and 81% the second. My runs aren't deterministic. How do I handle this in the loop?"
**PASS if**:
- Acknowledges this is a real problem (LLM evaluation is inherently noisy)
- Gives a concrete strategy: run eval N times and average, or require improvement > noise floor before keeping
- Does NOT say "just pick one number" without acknowledging the variance issue
- Specific enough to act on (e.g., "run 3 times, require mean improvement > 5%")

### P22: Metric gaming / eval overfitting
**Prompt**: "After 25 experiments my skill scores 97% on the eval set. But when I try it on real user prompts it feels about the same as when I started. What's happening?"
**PASS if**:
- Names the problem: overfitting to the eval set / Goodhart's Law ("when a measure becomes a target, it ceases to be a good measure")
- Explains the cause: eval set became too predictable / not diverse enough
- Gives actionable next step: redesign the eval set for the next session with genuinely harder, more diverse prompts
- Does NOT just say "keep optimizing"

### P23: Hypothesis quality
**Prompt**: "I have three ideas for my next experiment: (A) 'change something', (B) 'add more examples', (C) 'If I add 3 concrete examples showing edge case handling, the pass rate on adversarial prompts will improve because the model currently lacks pattern-matching context for those cases.' Which is the best hypothesis and why?"
**PASS if**:
- Clearly identifies C as the best hypothesis
- Explains WHY: C is specific, testable, predicts a mechanism, and targets an identified gap
- Explains what's wrong with A (too vague) and B (no mechanism, no target)
- Gives guidance on what makes a good hypothesis: specific change + specific predicted effect + reason

### P24: Principled stopping criteria
**Prompt**: "You say never stop. But I've hit 99% on a well-designed eval set with 50 diverse prompts, and I've run 40 experiments. Is there ever a principled reason to stop?"
**PASS if**:
- Concedes YES — there are principled stopping reasons: diminishing returns at very high scores, eval saturation, opportunity cost of running more experiments vs shipping
- Does NOT just say "never stop, keep going"
- Gives concrete criteria: e.g., "if 10+ consecutive discards AND score > 95% on a well-designed eval, consider calling it done"
- Distinguishes between "never stop mid-session" and "know when a loop has run its course"

### P25: Combining near-misses
**Prompt**: "Experiment 12 added section A and scored 0% improvement. Experiment 15 added section B and scored 0% improvement. But I have a hunch they'd work together. Can I combine them in experiment 16?"
**PASS if**:
- Says YES with caveats — combining two near-misses is a valid strategy when individual changes had no effect but might interact
- BUT warns: if it works, you won't know which part did it — that's acceptable here since both individually failed
- Distinguishes this from bundling two UNTESTED changes (which violates one-change-at-a-time)
- Gives a clear decision rule: combining two individually-failed changes is OK; bundling two untested changes is not

### P26: Improving the eval set itself
**Prompt**: "My eval set is terrible — all the prompts are too easy. Can I run an autoresearch loop to improve the eval set itself?"
**PASS if**:
- Identifies the circular problem: you need a fixed metric to run the loop, but the metric IS the thing you want to improve
- Says you can't use autoresearch on the eval set using itself as the metric
- Gives an alternative: manually redesign the eval set offline (human judgment), then start a fresh loop with the new set
- Does NOT say "sure, just use a meta-metric"

### P27: Parallel loops
**Prompt**: "I have two different skills I want to improve at the same time. Can I run two autoresearch loops in parallel on different artifacts?"
**PASS if**:
- Says YES — parallel loops on DIFFERENT artifacts with separate eval sets and separate results.tsv files are fine
- Clarifies the constraint is within a single loop (one artifact, one metric) not across loops
- Optionally notes the practical tradeoff: context switching between two loops adds overhead
- Does NOT say "no, only one loop at a time ever"

### P28: Radical vs incremental
**Prompt**: "I've been making small incremental tweaks for 20 experiments and I'm stuck at 71%. Should I try a radical rewrite of the entire artifact?"
**PASS if**:
- Says YES — when incremental changes plateau, a radical restructure is a valid and recommended strategy
- Frames it correctly: the radical rewrite is still one experiment (one change — albeit a big one)
- Gives guidance: if radical rewrite discards, you still have the backup — no permanent loss
- Warns: after a radical rewrite, the next few experiments should probe the new structure's weaknesses

### P29: Experiment prioritization
**Prompt**: "I have 8 experiment ideas queued up. How do I decide which to run first?"
**PASS if**:
- Gives a concrete prioritization heuristic — NOT just "use your judgment"
- Priority order should roughly match: fix failures identified in last run → simplifications (free wins) → targeted additions → structural changes → radical rewrites
- Explains WHY: fastest-signal experiments should come first to inform later ones
- Actionable enough that someone could apply it immediately

### P30: True local maximum
**Prompt**: "I've run 35 experiments. 28 discards. Best score is 79% and hasn't moved in 18 consecutive experiments. I've tried incremental changes, radical rewrites, combining near-misses. Nothing works. What now?"
**PASS if**:
- Acknowledges this is a genuine local maximum, not just a temporary plateau
- Gives at least 2 escape strategies: (1) question whether the metric/eval set is the problem, (2) accept 79% as the ceiling for this artifact design and consider a fundamentally different approach to the artifact itself, (3) bring in a human reviewer to identify blind spots
- Does NOT just say "keep trying harder"
- Is honest that sometimes 79% is the ceiling for a given architecture
