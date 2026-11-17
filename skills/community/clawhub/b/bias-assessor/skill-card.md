## Description:

Add bias/risk-of-bias assessment fields to an extraction table and populate them consistently.

This skill is ready for commercial/non-commercial use.

## Publisher:

[willoscar](https://clawhub.ai/user/willoscar)

### License/Terms of Use:

MIT-0

## Use Case:

External researchers and review teams use this skill after a systematic-review extraction table exists to add consistent risk-of-bias columns and ratings before synthesis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release presents as a narrow risk-of-bias table helper, but server security evidence reports bundled research-pipeline tooling that can route workflows, write many workspace files, run subprocesses, and auto-approve checkpoints.

Mitigation: Install only when the broader helper bundle is intended; constrain workspace and command scope, and review planned file changes before running.

Risk: Risk-of-bias ratings can be misleading when source papers lack enough methodological detail.

Mitigation: Use the documented low/unclear/high scale, prefer unclear when evidence is insufficient, and keep short auditable notes for each rating.

## Reference(s):

- [Bias Assessor skill page](https://clawhub.ai/willoscar/skills/bias-assessor)
- [Skill definition](artifact/SKILL.md)
- [Systematic review pipeline](artifact/pipelines/systematic-review.pipeline.md)

## Skill Output:

**Output Type(s):** [Files, Text, Guidance]

**Output Format:** [Updated CSV table with low/unclear/high ratings and short notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an existing papers/extraction_table.csv; artifact metadata indicates python3 or python may be required for bundled helpers.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
