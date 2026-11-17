## Description:

Detect flood events by comparing water levels to thresholds.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wu-uk](https://clawhub.ai/user/wu-uk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and analysts use this skill to identify flood days, aggregate water-level observations to daily maxima, and classify flood severity against established thresholds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Incorrect threshold sources or mismatched units can misclassify flood conditions.

Mitigation: Review threshold sources and confirm water-level and threshold units before relying on generated flood classifications.

Risk: Missing water-level observations can hide daily peaks or produce incomplete flood counts.

Mitigation: Check data availability, inspect missing values, and treat results as incomplete when daily maxima cannot be computed reliably.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown guidance with Python code examples and CSV or JSON output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on externally supplied water-level data and flood-stage thresholds.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
