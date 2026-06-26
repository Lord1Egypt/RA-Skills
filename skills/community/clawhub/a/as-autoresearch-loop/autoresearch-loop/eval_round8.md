# Autoresearch Loop — Round 8 Eval Set (DO NOT MODIFY)

Round 7 saturated at 100% with baseline 0%. These prompts target operational
maturity gaps: managing long-lived campaigns, non-LLM artifact patterns,
tradeoff decisions the keep/discard binary doesn't cover, and real-world
deployment feedback loops.

## Scoring Rubric
Each prompt scored PASS (1) or FAIL (0).
Score = (passes / 10) * 100

---

### P71: Eval file management across many rounds
**Prompt**: "I'm on Round 12 of a campaign. I have eval_round1.md through eval_round12.md, plus regression_suite.md, plus holdout_eval.md. My workspace is getting messy. Which eval files do I actually need to keep? Can I delete old ones?"
**PASS if**:
- Says you MUST keep: the current round's eval (active), regression_suite.md (persistent), holdout_eval.md (persistent/campaign-level)
- Old round evals (eval_round1–11) CAN be archived or deleted — they're historical record, not operationally needed. Their value was consumed when results.tsv logged the experiments against them
- Recommends: keep them archived (not deleted) if storage isn't an issue, since they document how the eval evolved and can inform future eval design
- Does NOT say "keep everything forever" or "delete everything except the current round"

### P72: Artifact forking — when and how to split
**Prompt**: "My SKILL.md started as a 'customer communication' skill but over 6 rounds it now covers email responses, Slack messages, phone call scripts, and complaint escalation. It's 500 lines and the eval has to test 4 completely different scenarios. Should I split it? How?"
**PASS if**:
- Says YES, this is a clear case for splitting — 4 distinct scenarios with different evaluation criteria signals scope has grown beyond what one artifact should handle
- Gives concrete forking mechanics: (a) identify natural boundaries in the current artifact, (b) create 2–3 new artifacts from the sections, (c) create NEW eval sets for each fork (the old eval doesn't apply as-is), (d) run a fresh baseline (iteration 0) on each fork, (e) continue independent loops
- Notes that the existing results.tsv and campaign history stay with the "parent" artifact — the forks start fresh loops with their own results logs
- Does NOT say "just keep it as one artifact and manage the complexity"

### P73: n8n workflow eval — concrete execution testing
**Prompt**: "I want to run autoresearch on an n8n workflow that processes incoming emails and routes them to different departments. I understand the concept but I don't know what 'running the eval' means for a workflow. I can't just score prompts. What does my eval set look like?"
**PASS if**:
- Gives concrete workflow eval guidance: the eval set is a collection of sample inputs (test emails) with expected outputs (correct department routing)
- Each test case = one sample input + expected output + pass/fail rule (e.g., "email about billing → routed to Finance department" = pass, anything else = fail)
- The eval run = trace through the workflow node by node with each sample input, or actually execute the workflow in a test environment
- Suggests 10–20 sample emails covering: normal cases, edge cases (ambiguous department), error cases (malformed email), and boundary cases (email that could go to two departments)
- Does NOT just say "adapt the same pattern as skills" without concrete workflow-specific guidance

### P74: Partial improvement tradeoff
**Prompt**: "My experiment improved 3 previously-failing prompts but broke 1 previously-passing prompt. Net score went from 70% to 80%. The prompt that broke covers an important real-world scenario. Do I keep or discard?"
**PASS if**:
- Says KEEP per the metric — score strictly improved (70% → 80%), so the rule says keep
- BUT: flags the regression on the important prompt as a serious concern that needs immediate follow-up
- Recommends: keep this experiment, then make the NEXT experiment specifically target fixing the regressed prompt without losing the 3 new gains
- Notes that if the regressed prompt covers a critical scenario, you might also add it to the regression suite as a guardrail for future experiments
- Does NOT say "discard because one important thing broke" (that's overriding the metric) or "keep and ignore the regression" (that's reckless)

### P75: Hypothesis generation when truly stuck
**Prompt**: "I've been staring at this skill for an hour. I've tried fixing every failing prompt individually, restructured twice, done simplification passes, tried a radical rewrite. I'm at 78% and stuck — the same 2 prompts keep failing and nothing I do fixes them. What specific techniques can I use to generate new experiment ideas?"
**PASS if**:
- Gives concrete idea-generation techniques beyond what's already in the skill (not just "try the inverse" or "combine near-misses"):
  - Read the failing prompt outputs CHARACTER BY CHARACTER — what specifically is wrong? Is it missing info, wrong format, wrong tone, wrong reasoning?
  - Study artifacts that handle similar scenarios successfully — what do they do differently?
  - Ask: "What would a human expert add to this artifact if they read the failing output?"
  - Try approaching from the opposite direction: instead of adding content to fix the failure, remove content that might be CAUSING the failure (conflicting guidance, misleading examples)
  - Check if the failing prompts require knowledge the artifact fundamentally can't provide — if so, the eval may need adjustment next round
- Does NOT just restate the existing escalation rule or generic advice

### P76: Readability vs. performance tradeoff
**Prompt**: "My skill scores 95% but it's a mess — bullet points inside paragraphs, contradictory-sounding advice that's actually nuanced, 3 different sections that each mention the same rule slightly differently. It works but nobody can read it. Can I do a readability refactor even if it risks dropping the score?"
**PASS if**:
- Says YES — readability/maintainability is a legitimate experiment goal, treated like any other experiment
- Run it as a normal experiment: refactor for readability, re-eval, keep if score stays equal or improves, discard if it drops
- Notes that "0% change but much cleaner: keep the simpler version" from the simplicity criterion applies here — a score-neutral readability improvement IS a keep
- If the readability refactor drops the score, it's a discard — but note what specifically broke and try a more targeted cleanup that preserves the critical passages
- Does NOT say "readability doesn't matter, only the metric matters" or "just do it without re-evaluating"

### P77: Format migration mid-campaign
**Prompt**: "I've been improving a SKILL.md for 5 rounds. Now I want to convert it to a structured YAML format because the platform we're deploying to requires YAML. Do I continue the current loop or start fresh?"
**PASS if**:
- Says this is a format change, not a content change — treat it as a special experiment within the current loop
- Run it as one experiment: convert to YAML, re-eval with the SAME eval set and scoring criteria. If score holds, keep (you've migrated without loss). If score drops, either fix the conversion or discard
- Does NOT recommend starting a completely fresh loop — the eval set and scoring criteria haven't changed, only the artifact format
- Notes that the results.tsv history remains valid and continuous — a format migration is just another experiment in the log
- Does NOT say "formats don't matter" or "always start fresh on format changes"

### P78: Eval scoring bug discovered mid-loop
**Prompt**: "I'm on iteration 14 and I just realized I've been scoring Prompt 5 wrong — my pass criteria say 'must include a date' but I've been passing it even when no date is present. I've probably scored 8+ experiments wrong on this prompt. What do I do?"
**PASS if**:
- Says this is distinct from an ambiguous prompt — this is a genuine scoring error that has corrupted your results
- Recommends: (a) fix the scoring immediately — apply the correct criteria going forward, (b) do NOT retroactively re-score all past experiments (that's impractical and changes history), (c) note the bug in results.tsv ("scoring error on P5 discovered at iteration 14, corrected going forward"), (d) the current best artifact's score may be inflated — re-eval now with correct scoring to get a true current score, then continue from there
- Does NOT say "EVAL IS IMMUTABLE means you can't fix it" — immutability protects against changing WHAT you test, not against fixing HOW you score
- Does NOT say "restart the entire loop" — past experiments still have value even with one noisy prompt

### P79: Post-deployment monitoring loop
**Prompt**: "I ran 4 rounds of autoresearch, got the skill to 95%, shipped it to production. Two months later, users are reporting it handles new scenarios poorly that didn't exist when I built the eval. How do I connect production feedback back to the loop?"
**PASS if**:
- Says this is exactly when to resume a loop session — real-world failures are the highest-quality signal for new eval prompts
- Recommends: (a) collect the specific failure cases from production, (b) use them as the foundation for the next round's eval set (they're real, not synthetic), (c) check the regression suite and holdout eval — if those still pass, the failures are in uncovered territory, not regressions, (d) run a new round with the failure-informed eval
- Connects to artifact retirement: "Resume a loop session only when real-world usage reveals a new failure mode worth addressing"
- Does NOT say "the loop is done, just manually fix the issues" or "start a completely new campaign"

### P80: Bootstrapping a loop for a novel artifact type
**Prompt**: "I want to improve a Figma design system component library using autoresearch. There's no template for this in the skill. How do I define the artifact, metric, and eval for something that isn't code, a prompt, or a document?"
**PASS if**:
- Walks through the setup framework applied to a novel artifact type: (a) artifact = the design system file or component spec, (b) metric = needs creative definition — could be a checklist pass rate (accessibility, consistency, completeness), design review score, or component coverage percentage, (c) eval = a set of test scenarios ("render a data table with 3 columns", "create a form with validation states") scored against the checklist
- The key insight: the methodology is format-agnostic — artifact, metric, eval, loop. Any artifact type works IF you can define a measurable metric and a repeatable eval
- Recommends starting with a small eval (5–10 test scenarios) to validate the metric makes sense before committing to a full campaign
- Does NOT say "autoresearch only works for text artifacts" or refuse to help because there's no template
