# Manual test plan for the Fabric CLI skill

## Trigger tests

Use `evals/trigger_queries_train.json` for description iteration and `evals/trigger_queries_validation.json` for held-out checking. Run each query several times in the target agent client and record whether `SKILL.md` was loaded.

Pass criteria:

- Should-trigger queries load the skill in most runs.
- Should-not-trigger near misses do not load the skill in most runs.
- Microsoft Fabric, Daniel Miessler Fabric, Python Fabric SSH, Fabric.js, and textile/fashion prompts should be the main negative focus.

## Functional tests

Run the cases in `evals/evals.json` in a clean context. For each case, capture commands attempted, whether the skill was loaded, assertion results, redaction behaviour, and token/time cost if available. Compare with a baseline run without the skill or with the previous skill version.

## Human review checklist

- Did the agent choose Fabric.so rather than the wrong Fabric?
- Did it avoid undocumented syntax unless live help supported it?
- Did it avoid running the installer without consent?
- Did it handle task IDs safely?
- Did it use stdin for long generated notes?
- Did it report workspace and limitations clearly?
- Did it avoid persisting unnecessary or sensitive memory?
