## Description:

Evaluates dataset submissions by scoring content consistency and structured data quality, then computing a final miner score.

This skill is ready for commercial/non-commercial use.

## Publisher:

[levey](https://clawhub.ai/user/levey)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and dataset evaluators use this skill to grade miner submissions by comparing cleaned text samples with structured JSON against a dataset schema.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Subjective similarity and value-accuracy judgments can produce inconsistent or misleading scores.

Mitigation: Use deterministic similarity metrics where possible, base judgments only on provided inputs, and review final scores for judgment quality.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, json, guidance]

**Output Format:** [JSON score object with concise evaluative rationale when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scores are expected to remain deterministic, reproducible, and bounded from 0 to 100.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
