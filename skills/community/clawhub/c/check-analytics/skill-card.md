## Description:

Audit existing Google Analytics implementation. Checks for common issues, missing configurations, and optimization opportunities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeftekhari](https://clawhub.ai/user/jeftekhari)

### License/Terms of Use:


## Use Case:

Developers and site maintainers use this skill to audit analytics implementations, identify tracking and configuration issues, and receive prioritized recommendations for improving measurement accuracy, privacy posture, and maintainability.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires reading project files to locate analytics code and identifiers.

Mitigation: Review the files accessed during the audit and keep reported measurement IDs partially redacted.

Risk: Analytics recommendations can affect measurement accuracy, consent behavior, or reporting quality if applied without review.

Mitigation: Have a qualified maintainer review the generated audit findings and proposed next steps before changing production analytics code.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown audit report with summary, current implementation, prioritized issues, event coverage table, and next steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Measurement IDs should be partially redacted in reports.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
