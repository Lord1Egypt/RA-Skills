# Autoresearch Loop — Round 5 Eval Set (DO NOT MODIFY)

Round 4 saturated at 100%. These prompts target production-scale and adversarial
failure modes that emerge after weeks of real-world loop usage.

## Scoring Rubric
Each prompt scored PASS (1) or FAIL (0).
Score = (passes / 10) * 100

---

### P41: Live production artifact
**Prompt**: "My Laia agent system prompt is currently live and serving real tenant queries for Finques Teixidor. I want to run the autoresearch loop on it to improve it. What should I watch out for?"
**PASS if**:
- Warns that iterating a live artifact risks deploying regressions to real users mid-loop
- Recommends working on a copy/branch, not the live version, until a candidate is ready to deploy
- Suggests: freeze the live version, run the loop on the copy, then do a deliberate controlled deploy of the winning version
- Does NOT just say "go ahead, the loop will catch regressions via the metric"

### P42: Human overrides the metric
**Prompt**: "The experiment scored 71% which is lower than the current best of 75%. But I really like how it reads — it feels much clearer. Should I keep it anyway?"
**PASS if**:
- Acknowledges this is a real tension (metric says discard, human intuition says keep)
- Gives a principled answer: the metric is the agreed arbiter — overriding it mid-loop breaks the entire comparison system
- Suggests the right path: discard per the metric, but note the "reads clearer" observation as a hypothesis for a future experiment that specifically targets readability as the metric
- Does NOT say "trust your gut, keep it"

### P43: Statistical significance with tiny eval sets
**Prompt**: "My eval set has 6 prompts. My experiment went from 4/6 (67%) to 5/6 (83%). That's a +16% jump. Should I trust that result?"
**PASS if**:
- Flags the statistical fragility: with 6 prompts, one prompt flip = 17 percentage points — the result is noisy
- Recommends expanding the eval set before trusting single-prompt swings as meaningful signal
- Gives a practical threshold: with <10 prompts, require 2+ prompt improvements before keeping, not just 1
- Does NOT just say "83% > 67%, keep it"

### P44: Version file explosion
**Prompt**: "I've been running the loop for 6 weeks and I now have 47 versioned backup files (SKILL_v1.md through SKILL_v47.md). How do I manage this?"
**PASS if**:
- Acknowledges this is a real maintenance burden
- Gives practical cleanup guidance: you only need the current best version + the baseline; intermediate versions can be archived or deleted once results.tsv documents what each one contained
- Suggests: if using git, the file history handles versioning automatically — no need for numbered copies at all
- Does NOT just say "keep all of them"

### P45: Warm-starting from a related artifact
**Prompt**: "I have a working system prompt for a Barcelona property management agent. Now I need to build one for a Madrid property management agent. Should I start the loop from scratch or start from the Barcelona prompt?"
**PASS if**:
- Says start from the Barcelona prompt — it's a better baseline than nothing, inheriting solved problems
- But: requires running a proper baseline (iteration 0) on the NEW artifact with a Madrid-specific eval set — don't assume the Barcelona score carries over
- Warns: the warm start means early experiments may show quick gains (fixing Barcelona-specific content) before the real Madrid-specific work begins
- Does NOT say "just copy it, they're the same"

### P46: Catastrophic experiment
**Prompt**: "My last experiment completely broke the artifact — I accidentally deleted a critical section and now the eval crashes with errors on every prompt. I scored it as 0%. What's the correct procedure?"
**PASS if**:
- Says: log it as `error` or `0.0 / crash` in results.tsv
- Immediately revert to the last backup (SKILL_vN.md)
- Investigate: was it a typo/accident (fix and re-run same experiment) or a fundamentally bad idea (discard and move on)?
- Does NOT say "just fix it in place and re-run without logging the failure"

### P47: Conflicting instructions from an experiment
**Prompt**: "After my last kept experiment, I noticed the artifact now tells the model to 'always respond in bullet points' in one section and 'always respond in prose' in a different section. The score improved but the artifact is internally contradictory. What do I do?"
**PASS if**:
- Treats internal contradictions as a bug that overrides the metric signal
- Recommends: revert to previous version — a higher score achieved through a broken artifact is not a genuine improvement
- Notes: fix the contradiction as its own targeted experiment and re-run
- Does NOT say "the metric improved so keep it"

### P48: Moving target — real-world inputs keep changing
**Prompt**: "I'm improving a workflow that processes client emails. But the client's communication style keeps changing and my eval set (built 2 months ago) no longer represents what we actually receive today. What do I do?"
**PASS if**:
- Names the problem: the eval set has drifted from the real-world distribution — it's no longer a valid proxy
- Recommends: pause the current loop, rebuild the eval set from recent real inputs, start a fresh session with the new eval (new baseline, new results.tsv)
- Distinguishes from metric drift (where the scoring criteria changed) — here the inputs themselves changed
- Does NOT say "just add a few new prompts mid-loop" (EVAL IS IMMUTABLE)

### P49: Multi-round eval evolution strategy
**Prompt**: "You've been designing progressively harder eval sets each round. What's the actual strategy for making each round's eval harder without just adding random prompts?"
**PASS if**:
- Explains the principle: each new eval set should target the *gaps* revealed by the previous round — look at what passed easily and what the skill never got tested on
- Gives the concrete method: (1) review all prompts that passed instantly in round N, (2) ask "what harder version of this question could be asked?", (3) find scenarios the skill currently handles correctly but could break under edge conditions, (4) add one-step-removed failure modes
- This is meta-guidance about the loop process itself, not just running it
- Is concrete enough to actually follow

### P50: When to retire vs keep improving
**Prompt**: "The autoresearch loop skill has now been through 4 rounds of improvement. At what point do I stop running improvement loops on it and just use it?"
**PASS if**:
- Gives a principled answer: retire from active improvement when (a) it handles all real-world use cases reliably and (b) new eval prompts are getting hard to design because there are no obvious gap scenarios left
- Distinguishes: the loop doesn't run continuously forever — it runs when there's a known problem or a new use case to handle. Maintain, don't obsessively optimize.
- Notes: retire the loop, keep the artifact. Resume a loop session only when real-world usage reveals new failure modes worth addressing
- Does NOT just say "keep going forever" or "you're done now"
