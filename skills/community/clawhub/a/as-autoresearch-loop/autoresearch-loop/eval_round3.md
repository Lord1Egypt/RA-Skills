# Autoresearch Loop — Round 3 Eval Set (DO NOT MODIFY)

Round 2 saturated at 100%. These prompts probe deeper failure modes:
- no eval set exists yet
- composite metric construction
- score noise / statistical tie
- zero-hypothesis situation
- session-level stopping vs loop stopping
- scope creep mid-loop
- parallel experiment temptation
- broken baseline
- good-enough trap
- recursive / meta use

## Scoring Rubric
Each prompt scored PASS (1) or FAIL (0).
Score = (passes / 10) * 100

---

### P21: No eval set exists yet
**Prompt**: "I want to run autoresearch on my Finques Teixidor email triage agent system prompt. I don't have any test cases yet. Can I still start?"
**PASS if**:
- Says NO — you cannot start the loop without a fixed eval set
- Helps the user build one: suggests generating test cases from real past inputs, or crafting synthetic ones covering the main scenarios
- Gives concrete guidance on how many prompts are needed (at least 8–10 for meaningful signal)
- Does NOT say "sure, just score it qualitatively"

### P22: Composite metric construction
**Prompt**: "I care about both accuracy AND conciseness for my system prompt. You told me to pick one metric. How do I build a composite score?"
**PASS if**:
- Gives a concrete formula (e.g., weighted average: 0.7 * accuracy + 0.3 * conciseness)
- Explains that weights must be set BEFORE the loop starts, not adjusted based on results
- Warns that composite metrics still need both sub-scores measured consistently
- Is actionable, not abstract

### P23: Score noise / statistical tie
**Prompt**: "My experiment scored 80% and the previous best was also 80%. The change I made feels like it should help. Should I keep it?"
**PASS if**:
- Says this is a tie — apply simplicity criterion first: if the change adds complexity, discard; if it simplifies, keep
- Mentions that with small eval sets (≤10 prompts), a 0% difference means literally one prompt flipped — not meaningful signal
- Does NOT say "keep it because it feels right" or "discard it to be safe" without applying the simplicity rule
- Optional bonus: suggests that tie-breaking on simplicity is the right tie-breaker

### P24: Zero-hypothesis situation
**Prompt**: "I've already tried adding examples, restructuring, tightening constraints, and adding edge case handling. I'm at 88% and genuinely have no idea what to try next."
**PASS if**:
- Does NOT suggest stopping
- Gives at least 3 specific, novel directions that weren't mentioned: e.g., try REMOVING something (what's the minimal version?), try rewriting from scratch with only the kept lessons, try inverting a failed experiment (what's the opposite?), try borrowing structure from a different domain
- Is concrete, not motivational

### P25: Session-level stopping vs loop stopping
**Prompt**: "I've been running for 3 hours, run 25 experiments, and I'm happy with the result. Is it OK to stop for today?"
**PASS if**:
- Clearly distinguishes: stopping the SESSION (yes, fine) vs stopping the LOOP permanently (that's the human's call based on goals)
- Says yes, stopping for today is fine — the loop resumes next session
- Reminds to save the best artifact version and update results.tsv before closing
- Does NOT say "you should never stop" (that applies within a session, not across days)

### P26: Scope creep mid-loop
**Prompt**: "We started improving my SOW template for consulting engagements. Halfway through I realized it should also cover retainer agreements. Can I expand the scope?"
**PASS if**:
- Says NO — expanding the artifact's purpose mid-loop invalidates the eval set (it no longer tests the full scope)
- Explains why: past experiments were scored against the old scope; a new scope needs a new eval set
- Suggests: finish the current loop for consulting SOWs, then start a fresh loop for the expanded scope
- Does NOT say "sure, just add a few test cases" (eval is immutable)

### P27: Parallel experiment temptation
**Prompt**: "Could I run two different experiments in parallel to go twice as fast? Like, branch A tries adding examples, branch B tries restructuring, and I pick the better one?"
**PASS if**:
- Says this breaks the lineage / uphill walk — you can't branch and merge cleanly
- Explains: if both experiments improve, which do you combine? The interaction effect is unknown
- The loop is serial by design: each experiment builds on the best-so-far
- May acknowledge that running two from the same baseline and picking the better one IS valid — as long as the loser is fully discarded and you continue from the winner

### P28: Broken baseline
**Prompt**: "I ran the baseline and scored 10%. That seems way too low. Something might be wrong with the artifact before we even start. What do I do?"
**PASS if**:
- Does NOT say "just start experimenting from here"
- Suggests investigating before starting the loop: is the eval set miscalibrated? Is the artifact fundamentally broken? Is the scoring rubric too harsh?
- Recommends fixing the artifact to a reasonable starting state first (or fixing the eval), then re-running the baseline as iteration 0
- Treating a broken baseline as the starting point wastes experiments on fixing bugs rather than genuine improvement

### P29: The good-enough trap
**Prompt**: "My skill is at 95% pass rate. The remaining 5% are really hard edge cases. Is it worth continuing?"
**PASS if**:
- Gives a principled answer, not just "yes keep going" or "you're done"
- Applies the cost/benefit lens: what's the cost of one more experiment vs the value of fixing the remaining 5%? If the edge cases are rare in practice, 95% may be genuinely good enough
- Mentions diminishing returns: at 95%, each improvement is harder to find and the signal is noisier
- Does NOT just recite NEVER STOP — recognizes that the human decides when good enough is enough

### P30: Recursive / meta use
**Prompt**: "Can I use the autoresearch loop to improve the autoresearch loop skill itself?"
**PASS if**:
- Says YES — this is exactly valid and the skill itself was built this way
- Identifies the artifact (SKILL.md), metric (pass rate on test prompts), and fixed eval set as the three components needed
- Notes the meta-challenge: the eval set must be designed to test the skill's guidance quality, not just its triggering
- Is enthusiastic — this is a feature, not a weird edge case
