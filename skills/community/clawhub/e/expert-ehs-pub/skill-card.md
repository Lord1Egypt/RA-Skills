## Description:

安全环保与职业健康专家 routes pasted EHS table material across 12 local checking workflows and returns line-by-line conclusions with source row references when the supplied columns are sufficient.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

External users and EHS operators use this skill to paste compliance, inspection, maintenance, waste, emissions, or equipment tables and get deterministic local checks with missing-column feedback. It is intended to support review of provided records, not replace legal advice, regulator review, or field inspection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill checks supplied EHS tables and may be mistaken for legal, regulatory, or field-inspection approval.

Mitigation: Use the output as review support only; have qualified personnel validate findings against applicable regulations, source records, and field conditions.

Risk: The local trial counter may block use after five runs and display subscription messaging.

Mitigation: Confirm trial and subscription behavior before deploying the skill in a workflow that requires uninterrupted use.

Risk: Incomplete or mismatched table headers can prevent routing or leave some checks unexecuted.

Mitigation: Provide complete table headers with data rows and review any missing-column or unexecuted-check messages before relying on results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/expert-ehs-pub)

## Skill Output:

**Output Type(s):** [Analysis, Text, JSON, Shell commands, Guidance]

**Output Format:** [Plain text or JSON, depending on command flags]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local deterministic output may include matched sub-skill, row-level findings, missing input fields, unexecuted checks, and trial-limit messaging.]

## Skill Version(s):

1.0.10 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
