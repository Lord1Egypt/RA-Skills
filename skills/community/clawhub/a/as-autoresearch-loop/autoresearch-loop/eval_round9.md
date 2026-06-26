# Autoresearch Loop — Round 9 Eval Set (DO NOT MODIFY)

Round 8 saturated at 100% with baseline 10%. These prompts target governance,
automation, operational emergencies, and the human/organizational dynamics
that determine whether the loop methodology survives contact with reality.

## Scoring Rubric
Each prompt scored PASS (1) or FAIL (0).
Score = (passes / 10) * 100

---

### P81: Multi-stakeholder conflict
**Prompt**: "My skill is used by both the sales team and the support team. Sales wants it optimized for persuasive upsell language. Support wants it optimized for empathetic de-escalation. These directly conflict — improving one hurts the other. How do I handle this with autoresearch?"
**PASS if**:
- Recognizes this as a fundamental ONE ARTIFACT / ONE METRIC violation — a single artifact serving conflicting goals cannot be optimized with a single metric
- Recommends forking: split into two artifacts (sales skill + support skill), each with its own eval set optimized for that stakeholder's needs, and run independent loops
- If forking isn't feasible (e.g., must remain one artifact), recommends the composite metric approach with stakeholder-agreed weights BEFORE the loop starts — but warns that compromise artifacts may underperform dedicated ones
- Does NOT say "just pick the more important stakeholder" without offering the fork alternative

### P82: Automated CI/CD loop
**Prompt**: "I want to run autoresearch automatically in a CI pipeline — every night, the system runs 5 experiments on my skill, logs results, and commits the best version. No human in the loop at all. Is this a good idea? What guardrails do I need?"
**PASS if**:
- Says this is valid and aligned with Karpathy's original design ("the human's job is to set it up, not run it"), but requires guardrails
- Essential guardrails: (a) hard stop conditions (max experiments per run, score regression threshold that halts the pipeline), (b) alerting on anomalies (suspicious large gains, consecutive errors), (c) periodic human review of results.tsv to catch drift, (d) never auto-deploy to production — the pipeline produces a candidate, a human approves the deploy
- Notes the eval must be fully deterministic for unattended runs — LLM-as-judge noise without human oversight creates phantom improvements
- Does NOT say "don't automate, always have a human" or "just let it run with no guardrails"

### P83: Emergency hotfix during active loop
**Prompt**: "I'm mid-loop on a production agent's system prompt (working on a sandboxed copy). A critical bug just hit production — the live version is broken and users are affected. I need to fix the live version NOW. But the loop says 'freeze the live version.' What do I do?"
**PASS if**:
- Says production safety trumps loop discipline — fix the live version immediately
- But: don't abandon the loop. After the hotfix: (a) apply the same fix to your sandboxed loop copy, (b) re-eval to get a new current score (the hotfix changed the artifact), (c) log it as an out-of-band experiment in results.tsv with a note explaining the emergency, (d) continue the loop from the updated state
- The key insight: the live production sandboxing rule protects against CASUAL changes, not genuine emergencies. Breaking the sandbox in an emergency is correct — but you must reconcile the loop state afterward
- Does NOT say "wait until the loop finishes" or "the sandbox rule is absolute"

### P84: Experiment dependency — idea requires a discarded prerequisite
**Prompt**: "I have an idea for experiment 15, but it only makes sense if experiment 12 had been kept — and experiment 12 was discarded. My idea builds on what experiment 12 tried. Can I re-apply experiment 12's change as a prerequisite and then add my new idea on top?"
**PASS if**:
- Says this violates ONE CHANGE AT A TIME — re-applying a discarded experiment plus a new change is bundling two changes
- Correct approach: re-run experiment 12 as its own fresh experiment first. If it was discarded because of negative score impact, it will likely discard again — in which case, the dependent idea isn't viable either. If conditions have changed (other experiments since then may have created a context where 12 now works), it might keep this time
- After 12 is resolved (kept or discarded), THEN propose experiment 15 as a separate experiment
- Does NOT say "just bundle them since 12 was already tested" — the artifact has changed since 12 was tested, invalidating that result

### P85: Loop fatigue — diminishing experiment creativity
**Prompt**: "I'm on session 6 of this campaign. My last 3 sessions have each started with a baseline of 20-30% on the new harder evals, but I keep running out of ideas by experiment 5 or 6. My experiments are getting repetitive — slight rewording, moving paragraphs around. How do I break out of this rut?"
**PASS if**:
- Validates this as a real and common problem — creative fatigue in long campaigns is expected, not a personal failure
- Recommends concrete rut-breakers: (a) take a break and return with fresh eyes — the loop continues across sessions, there's no rush, (b) have someone else run a session — fresh perspective generates different hypotheses, (c) study the cross-artifact learnings doc for patterns that worked on similar artifacts, (d) try a radical structural rewrite rather than incremental tweaks, (e) question whether the eval itself has become the bottleneck — maybe the artifact is actually good enough and the eval needs redesigning, not the artifact
- Connects to existing guidance (escalation rule, cross-artifact learning, good-enough decision) but synthesizes them as a fatigue response
- Does NOT just say "think harder" or repeat the escalation rule verbatim

### P86: Eval difficulty imbalance
**Prompt**: "My eval has 10 prompts but I've noticed 3 of them are trivially easy (the baseline artifact passes them) and 2 are so hard that no version of the artifact has ever passed them. That means my real discrimination range is only 5 prompts — 30% of my score is locked as a pass, 20% is locked as a fail. Is this a problem?"
**PASS if**:
- Says YES, this is a significant eval design problem — effective discrimination range is only 50% of the eval (5 prompts out of 10), which means one prompt flip = 10% instead of the theoretical 10%
- The trivially easy prompts waste eval budget — they pass on every version and never discriminate. The impossibly hard prompts are either testing beyond the artifact's possible scope or are poorly calibrated
- Recommends for the NEXT round: replace trivially easy prompts with harder versions, and either make the impossible prompts achievable (relax criteria) or remove them if they test something outside scope
- For the CURRENT round: continue as-is (EVAL IS IMMUTABLE) but note the imbalance — your effective eval is 5 prompts, so apply the statistical fragility rules (require 2+ prompt improvements before keeping)
- Does NOT say "just ignore it" or "redesign the eval mid-loop"

### P87: Metric ceiling before artifact ceiling
**Prompt**: "I hit 100% on my eval — all 15 prompts pass. But when I use the artifact in the real world, it clearly has gaps. The eval just doesn't test the scenarios where it fails. I've already done my simplification pass and the 100% holds. Now what?"
**PASS if**:
- Says the eval has been outgrown — the artifact has improved past what the eval can measure
- This is exactly when to start a new round: design a harder eval that covers the real-world gaps. Use the actual failure scenarios as the new eval prompts (post-deployment feedback loop)
- Check the holdout eval: if it also shows 100%, consider designing a new holdout too
- Does NOT say "you're done, ship it" without addressing the known real-world gaps — 100% on an outgrown eval is not convergence, it's a signal to level up the eval
- Does NOT say "keep running experiments on the current eval" — that's pointless at 100%

### P88: Model version regression
**Prompt**: "My skill was optimized to work with Claude Sonnet 3.5. A new model version (Sonnet 4) just came out and my company is switching to it. When I run my eval on the same skill with Sonnet 4, the score dropped from 92% to 71%. The skill didn't change — the model did. What do I do?"
**PASS if**:
- Identifies this as a form of environment change (analogous to input distribution drift, but the model is the environment)
- Recommends: (a) this is a new loop context — treat it as a fresh campaign start against the new model, (b) run a proper baseline (the 71% IS the baseline for Sonnet 4), (c) the old results.tsv from the Sonnet 3.5 campaign is historical — archive it, start a fresh log, (d) many old experiments may re-apply (the improvements likely still help), so check the cross-artifact learnings and prior results for warm-start ideas
- If multi-model support is needed, references the multi-model evaluation guidance (floor strategy or weighted average)
- Does NOT say "just keep using the old model" or "the skill is broken, start from scratch"

### P89: Shared artifact sabotage — unauthorized changes
**Prompt**: "Someone on my team edited the SKILL.md directly without going through the loop — they added a whole new section because a customer asked for it. Now my results.tsv doesn't reflect the current artifact state. The loop is contaminated. How do I recover?"
**PASS if**:
- Identifies this as a state contamination problem — the artifact and the log are out of sync
- Recommends: (a) diff the current artifact against the last logged keep's backup to see exactly what was added, (b) decide whether to keep or revert the unauthorized change: run the eval on the current (modified) artifact — if score improved or held, the change may be worth keeping; if score dropped, revert to the last backup, (c) log the event in results.tsv as an out-of-band change with a note, (d) establish a governance rule: all artifact changes go through the loop, or at minimum get logged
- Connects to async multi-operator guidance: this is the same corruption risk, just caused by someone bypassing the process entirely
- Does NOT say "start over from scratch" or "just ignore it and continue"

### P90: Campaign documentation for organizational learning
**Prompt**: "We've been running autoresearch on various artifacts for 6 months across 4 team members. We have results.tsv files everywhere, cross-artifact learnings scattered in docs, holdout evals, regression suites. If I left the company tomorrow, nobody could make sense of this. What should our campaign documentation look like?"
**PASS if**:
- Takes the knowledge management concern seriously — autoresearch generates valuable institutional knowledge that must be organized
- Recommends a campaign-level documentation structure: (a) per-artifact folder with: current best artifact, results.tsv, active eval set, regression suite, holdout eval; (b) a campaign index/README listing all artifacts under active improvement, their current status (active/retired/shipped), last session date, current best score; (c) the cross-artifact learnings doc as a shared team resource; (d) a brief runbook: "how to pick up any artifact's loop" referencing the handoff protocol
- Notes that results.tsv IS the primary documentation for individual loops — but cross-loop and cross-artifact coordination needs something above it
- Does NOT just say "keep good notes" without giving concrete structure
