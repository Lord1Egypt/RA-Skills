## Description:

Compare models with A/B testing for selection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nidalghetf](https://clawhub.ai/user/nidalghetf)

### License/Terms of Use:


## Use Case:

Developers and model evaluators use this skill to compare two model candidates against user-defined test prompts and review the reported status, details, winner, and confidence score.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted test prompts may be stored in logs.

Mitigation: Review logging behavior before installation and redact prompt contents in environments where prompts may contain sensitive data.

Risk: The dependency setup is weak or malformed.

Mitigation: Fix package metadata, remove or pin unused dependencies, and add a lockfile before relying on the skill in production workflows.

Risk: The documented A/B testing behavior may not be implemented fully enough for real model evaluation.

Mitigation: Validate the comparison logic, winner selection, and confidence calculation against expected evaluation criteria before using results for model selection.

## Reference(s):


## Skill Output:

**Output Type(s):** [JSON, Analysis]

**Output Format:** [JSON object with status, details, winner, and confidence fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires model_a, model_b, and test_prompts inputs.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
