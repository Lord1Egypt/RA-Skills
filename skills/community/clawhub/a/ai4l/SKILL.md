---
name: er
description: AI4L Evidence Review Toolkit
licence: see LICENSE.md
---

Copyright (c) 2026 [Forever Healthy Foundation](https://forever-healthy.org)

# AI4L Evidence Review Toolkit

Version: 2026.03.19.1

This skill handles all Evidence Review workflows. 


## Key Files

* `AI4L.md` — The QA audit checklist for ERs


## General Rules

* Parse the user's input to determine which command to execute
* Note the start time (HH:MM:SS) when beginning any command, and report the time taken when done

* All generated results go in `./results/` as .md files
* All references to "ER.md" and "QA.md" files are relative to `./results/`

* Do not edit or modify any files outside `./results/` unless explicitly granted permission by the user on a case-by-case basis.

* Set [default_topic] to “Using Telmisartan to Improve Health and Longevity”


## Command: VERIFY

Trigger: "verify"

### Target Files

- `AI4L.md`
- `CLAUDE.md`
- `README.md`
- `PERSONA.md`
- `SKILL.md`
- `./docs/AI Models.md`
- `./examples/README.md`

### Process


* Verify all target file version numbers. Use the version stated at the start of AI4L.md in the alt text (not the badge) as a reference. Make sure that all targets are consistent with it, including the version number in the badges. SKILL.md does not have a badge, just a plain-text version number, so make sure that matches as well.

* Check the numbering of all items and the item count in AI4L.md

* Verify all target files for consistency and completeness

* If there are any inconsistencies, fix them.

* Report what was checked and what (if anything) was fixed.


## Command: CREATE

Trigger: "create"

### Topic Parsing

* Set [remainder] to the rest of the input after the command trigger word "create"

* If [remainder] is empty, set [topic] to the [default_topic]
* If [remainder] looks like "Using \<intervention> for/as/to \<goal>", set [topic] to [remainder]
* If [remainder] contains only an intervention and no goal, set [topic] to  "Using \<intervention> to Improve Health and Longevity"

* Notify the user that an ER will be created for [topic]

* Create an ER for [topic] that can pass a QA audit as described in "AI4L.md"

* Save the result as an .md file in `./results/` using the filename given in the result
* Report the filename and location when done.


## Command: SUBAUDIT (with sub-agent)

Trigger: "subaudit"

Audit an ER using a sub-agent

### Determine the Target

* If no further information is given, set [target] to the last evidence review generated; otherwise, take the remainder of the input as [target]

* If [target] = "all", audit all "ER.md" files that have not been audited yet using the instructions in "AI4L.md"

### Audit (Sub-agent)

Launch sub-agent, with Opus as its model, to audit the ER using the prompt given below. 
DO NOT pass any other instructions to the sub-agent besides the prompt.

> * State your model name and version number to the user
> * Audit the [target] file using the instructions in "AI4L.md"
> * Do NOT use any sub-agents for the task. Do things step-by-step.
> * Save the result in `./results/` using the name defined in the result
> * Do not modify any files outside `./results/`

### Report and Offer Fix

* Read the audit output and report the pass rate

* If not 100%, and the audit was done by the same AI model that generated the ER, ask the user if they want to fix it

* If yes, read the audit file, identify all failed items, and fix the ER based on the auditor's comments. DO NOT modify the QA file. Only the ER may be edited during the fix step.


## Command: AUDIT (no sub-agent)

Trigger: "audit"

Audit an ER without using a sub-agent

### Determine the Target

* If no further information is given, set [target] to the last evidence review generated; otherwise, take the remainder of the input as [target]

* If [target] = "all", audit all "ER.md" files that have not been audited yet using the instructions in "AI4L.md"

### Do the actual audit

* Audit the [target] file using the instructions in "AI4L.md"
* Do NOT use any sub-agents for the task. Do things step-by-step.

* Save the result in `./results/` using the name defined in the result
* Do not modify any files outside `./results/`

### Report and Offer Fix

* Read the audit output and report the pass rate

* If the pass rate is not 100%, and the audit was done by the same AI model that generated the ER, ask the user if they want to fix it

* If yes fix the ER based on the audit results. DO NOT modify the QA file. Only the ER may be edited during the fix step.


## Command: FULL

Trigger: "FULL"

Run the complete single-pass workflow: create an ER, audit it, and fix any issues.

### Process

1. **Create** — follow the CREATE command process (sub-agent creates the ER)
2. **Audit** — follow the AUDIT command process (fresh sub-agent audits it)
3. **Fix** — read the audit results, identify all failures, and fix the ER automatically

### Report

After saving the fixed ER, report the ER filename, the audit filename, the pass rate, and the time taken.


## Command: ITERATE

Trigger: "iterate"

Creates an ER, then loops audit/fix cycles up to 10 times until two consecutive audits show 100% pass rate.

### Process

1. **Parse topic** — same logic as the ER command

2. **Create ER** — launch sub-agent (same as ER command)

3. **Audit loop:**

Initialize: `iteration = 0`, `consecutive_passes = 0`, `max_iterations = 10`

Loop while `iteration < max_iterations` and `consecutive_passes < 2`:

  a. **Audit** — launch a fresh sub-agent (same prompt as Audit command). Fresh context is
     critical — the auditor must have no knowledge of the ER creation or prior audits.

  b. **Extract pass rate** — read the audit file, extract from the summary table. If ambiguous, run a script to parse and calculate.

  c. **Evaluate** — if 100%, increment `consecutive_passes`; otherwise reset to 0.
     Report: "Iteration {n}: Pass rate = {rate}% ({consecutive_passes}/2 consecutive passes needed)"

  d. **Fix** (if needed) — if `consecutive_passes < 2`, read the audit file, identify all
     failed items, fix the ER. The fix step is done by the orchestrator (not a sub-agent)
     since it needs the context of both the ER and the audit. Increment `iteration`.

### Report

- **Success:** "Pipeline complete. The ER passed two consecutive audits with a 100% pass rate
  after {n} iteration(s)."
- **Limit reached:** "Pipeline stopped after 10 iterations. Best pass rate achieved: {rate}%.
  The latest ER and audit files are in ./results/ for manual review."

List all files generated in `./results/`.


## Command: COMPARE

Trigger: "COMPARE"

### Process

* If no further information is given, set [intervention] to the intervention of the latest "ER.md" in "./results/" (parse the filename to extract the intervention)
* Otherwise, take the remainder of the input as [intervention]

* Compare all [intervention] "ER.md" files by the quality of the content. Be detailed. Also, take into account the latest [intervention] "QA.md" for each of them.
 
* Present a clear recommendation of which ER is strongest and why.
