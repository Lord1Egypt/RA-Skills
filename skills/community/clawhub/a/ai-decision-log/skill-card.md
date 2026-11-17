## Description:

Records AI-assisted decisions in a local JSONL ledger and reports model usage and gaps in human review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and governance teams use this skill to keep a local record of AI-assisted decisions, their models, evidence references, reviewers and timestamps, then identify decisions lacking human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Decision text, model details and reviewer names are stored in a local ledger and may be sensitive.

Mitigation: Choose the ledger path deliberately, restrict access and avoid recording sensitive details unless local storage is acceptable.

Risk: Documented CLI options and declared schema do not fully match the script's behavior.

Mitigation: Check the script's --help output before use and validate the ledger and report in your workflow.

## Reference(s):

- [ai-decision-log on ClawHub](https://clawhub.ai/zhaoxinghua09-cell/skills/ai-decision-log)
- [LGD theory (linked from the skill README; not verified as source provenance)](https://github.com/zhaoxinghua09-cell/lgd-theory)

## Skill Output:

**Output Type(s):** [Text, JSON, Files]

**Output Format:** [Local JSONL decision ledger; plain-text listings and summaries or a JSON report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Records decision, model, evidence hash, reviewer and timestamp; reports highlight unreviewed decisions.]

## Skill Version(s):

1.0.5 (source: ClawHub release; SKILL.md declares 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
