## Description:

Dynamic Model Selector recommends a GitHub Copilot model for a task based on query complexity, cost, and task type.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mpelissari](https://clawhub.ai/user/mpelissari)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to route GitHub Copilot tasks to a recommended model by balancing task complexity, coding needs, and cost sensitivity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Model and cost recommendations may be stale or inconsistent with current GitHub Copilot options.

Mitigation: Verify recommendations against current GitHub Copilot model availability and pricing before relying on them for paid usage decisions.

## Reference(s):

- [Dynamic Model Selector on ClawHub](https://clawhub.ai/mpelissari/skills/dynamic-model-selector)
- [Available GitHub Copilot Models - Detailed Specs](references/models.md)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown guidance with optional shell command invocation and plain-text recommendation output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommendations are advisory and should be checked against current GitHub Copilot model availability and pricing.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
