# Running the /deepen evals

Three eval types. A skill's value is a hypothesis until measured — research finds ~25% of skills cause
*negative* transfer, and you can't tell a good skill from a bad one by reading it. So: measure, don't assume.

## 1. Trigger eval (cheapest, highest-value — most failures live here)
For each prompt in `prompts.md`, check whether the skill fires:
- Confirm discovery in your runtime's skill list, then send the prompt and see if `/deepen` loads.
- Debug a miss: **ask the agent to quote the skill's description verbatim** — reveals missing keywords.
- Fix false negatives → add trigger phrasing to the `description`; fix false positives → add negative triggers.
- Target: ≥90% correct (fires on all positives, none of the negatives).

## 2. Capability ablation (does the skill actually help?)
For a topic in `prompts.md`:
1. **Skill-OFF baseline:** in an isolated session with the skill *not* loaded, prompt plainly
   ("research <topic> and brief me as an expert").
2. **Skill-ON:** run `/deepen <topic>`.
3. Score BOTH against `rubric.md` (/14). Record solution-quality (+ cost/runtime if tracked) in `results.md`.
4. The skill-on minus skill-off delta is the skill's value. Negative delta = the skill *hurts* → fix or cut.
Use the SAME topic for both arms (a matched pair) or the comparison is meaningless.

## 3. Edit-regression scenarios (did a specific change help?)
Run the targeted scenarios in `prompts.md` and confirm PASS. To verify a *change*, compare the current skill
vs the pre-edit version on the scenario it targets.

## Graduation
Once skill-on is consistently ≥11/14 on the capability topics, those become **regression** evals — re-run
after any skill edit and **after model upgrades** (skills are model-dependent and decay).
