## Description:

Run one controlled daily project loop for a single active project. Use on: scheduled daily runs, planner-initiated project steps, resuming a project after cleanup, user requests for active project advancement. Triggered when a project needs to advance by one meaningful step per day.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunbinnju-star](https://clawhub.ai/user/sunbinnju-star)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, project operators, and agent workflows use this skill to advance one active project by one meaningful daily step, select the current bottleneck, dispatch focused work, and record structured writeback for the next loop.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Incorrect or incomplete project state can cause the loop to choose the wrong bottleneck or write inaccurate project updates.

Mitigation: Confirm the active project card, latest weekly review, recent daily logs, and open questions are current before running the skill; stop with safe_to_proceed=false when required state is missing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sunbinnju-star/skills/daily-loop-runner)

## Skill Output:

**Output Type(s):** [text, configuration, guidance]

**Output Format:** [Structured JSON-compatible object]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes the daily objective, selected agent, task input, expected output, execution summary, findings, decisions, next action, project card updates, writeback payload, and safe-to-proceed status.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
