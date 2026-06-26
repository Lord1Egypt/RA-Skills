# Autoresearch Loop — Round 4 Eval Set (DO NOT MODIFY)

Round 3 saturated at 100%. These prompts target deeper, structural failure modes
that emerge at scale or in production use of the loop.

## Scoring Rubric
Each prompt scored PASS (1) or FAIL (0).
Score = (passes / 10) * 100

---

### P31: Non-deterministic metric
**Prompt**: "My metric is LLM-judged quality score. I run the same artifact twice and get 73% and 79%. That's a 6-point swing just from randomness. How do I run the loop reliably?"
**PASS if**:
- Acknowledges this is a real problem (LLM judges have variance)
- Gives a concrete solution: run eval N times and average (e.g., 3 runs), use the average as the score
- Suggests that the keep/discard threshold should account for noise (e.g., require improvement > variance margin)
- Does NOT just say "use a deterministic metric instead" without acknowledging that's not always possible

### P32: Eval overfitting / Goodhart's Law in practice
**Prompt**: "I've been iterating the same skill for 40 experiments across 4 sessions. The eval score is now 98%. But when I use the skill in real conversations, it doesn't feel noticeably better than it was at 75%. What's happening?"
**PASS if**:
- Names the phenomenon: eval overfitting / Goodhart's Law (the eval has become the target, not the proxy)
- Explains the mechanism: after 40 experiments targeting specific prompts, the artifact has been tuned to pass THOSE prompts, not to be generally better
- Gives a concrete fix: retire the current eval set, design a completely fresh one with new prompts, run the baseline again — the "real" score will likely be lower than 98%
- Does NOT just say "keep improving"

### P33: Loop vs one-shot
**Prompt**: "I need to write a one-time client proposal for a new engagement. Should I use the autoresearch loop to improve it?"
**PASS if**:
- Says NO — the loop is for artifacts that will be reused and improved over time
- Explains the core mismatch: a one-time document has no future eval set, no reuse value, no iteration benefit
- Suggests: just write a good proposal directly, possibly using other skills
- Does NOT say "you could set up an eval set for it" — that would cost more than just writing it well

### P34: Artifact with dependencies
**Prompt**: "My email triage agent uses two skills: one for language detection and one for routing logic. The routing is performing badly. Which artifact do I run the loop on?"
**PASS if**:
- Says: isolate which artifact is causing the failure before starting the loop
- Gives concrete guidance: run the routing skill in isolation with its own eval set first; if it passes, the bug may be in the language detection output feeding into it
- Warns against: running the loop on the routing skill while the language detection output is broken — you'll be optimizing against incorrect inputs
- Essentially applies ONE ARTIFACT but extends it to dependency debugging

### P35: Handoff documentation
**Prompt**: "I've been running the loop on a system prompt for a client. My colleague Roger needs to take over from experiment 12. What do I give him?"
**PASS if**:
- Lists the minimum handoff package: results.tsv, current best artifact version, the fixed eval set + rubric, and a brief note on what's been tried and what directions look promising
- Mentions that Roger should NOT re-run the baseline — he continues from experiment 13
- Is concrete enough that Roger could actually pick up and continue without asking questions
- Does NOT just say "share the files"

### P36: Metric drift
**Prompt**: "I started the loop 3 months ago with a 'checklist compliance score' metric. Since then, the checklist itself has been updated — 2 items removed, 3 new ones added. My old results.tsv shows scores from the old checklist. Can I just keep going?"
**PASS if**:
- Says NO — the metric has fundamentally changed; old scores are not comparable to new ones
- Treats this like a mid-loop eval change (same principle as EVAL IS IMMUTABLE)
- Recommends: start a fresh session. The old results.tsv becomes historical record only. New baseline against the updated checklist = iteration 0
- Acknowledges: any "improvement" measured against the old metric is now meaningless for comparison

### P37: Diminishing returns decision
**Prompt**: "I'm at 87% after 8 experiments. Each experiment takes about 30 minutes of my time. The last 3 all discarded. Should I keep going or spend that time elsewhere?"
**PASS if**:
- Applies a cost/benefit frame, not just "never stop"
- Acknowledges: 3 discards is not a plateau, but 30 min/experiment is a real cost
- Gives a principled recommendation: try 2–3 more targeted experiments (highest-signal ideas first); if they all discard, consider stopping for this session and returning with fresh ideas or a new eval set
- Does NOT robotically say "keep going indefinitely" — recognizes the human's time has value

### P38: Lost backup / version recovery failure
**Prompt**: "I forgot to save a versioned backup after my last keep. I ran a discard experiment and now I've lost track of what the current best version is. What do I do?"
**PASS if**:
- Gives concrete recovery options: check git history if tracked; look at the results.tsv to understand what the last kept state was, then reconstruct; if the file was overwritten and there's no backup, you may need to re-implement the last kept changes from the description in results.tsv
- Reinforces: this is why you always save a versioned copy immediately after every KEEP, before running the next experiment
- Is practical, not just "you should have backed up"

### P39: Warm-up / exploration phase
**Prompt**: "I just started the loop on a brand new system prompt I've never tested before. My baseline is 45%. I have no idea what's wrong. Where do I even begin?"
**PASS if**:
- Recommends starting with a diagnostic pass: read all the failing prompts carefully before proposing any change — understanding WHY things fail is more valuable than trying random fixes
- Suggests the first 2–3 experiments should be exploratory (remove a section entirely, test a radically different structure) to understand the problem space before optimizing
- Does NOT just say "start with the prioritized experiment list" — at 45% with no history, you need to understand the failure modes first

### P40: When the loop has converged
**Prompt**: "I'm at 94%, I've run 22 experiments, the last 8 have all discarded, and I've tried incremental changes, radical restructuring, and combining near-misses. I genuinely feel done. What do I tell the client?"
**PASS if**:
- Validates that this is a legitimate stopping point (not just "keep going")
- Tells them to produce the Research Summary (the end-of-session output from the skill)
- Gives guidance on framing for the client: 94% on a well-designed eval, 22 experiments, demonstrable log of what was tried — that's rigorous, professional, deliverable work
- Recommends: archive results.tsv + best artifact + eval set together as the deliverable package
