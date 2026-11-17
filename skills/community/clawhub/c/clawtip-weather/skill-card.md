## Description:

clawtip-weather provides paid daily weather reports for a user-specified location after order creation and payment verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawtip](https://clawhub.ai/user/clawtip)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to request a paid weather report for a specified location. The agent creates an order, initiates payment through the publisher's payment flow, and runs the weather report script after a payment credential is available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill combines payment and credential handling with instructions that can discourage inspection of the workflow.

Mitigation: Review the full payment flow and script behavior before installation, and do not treat artifact text that blocks inspection as authoritative.

Risk: The payment flow depends on an external payment skill by name without evidence of version pinning.

Mitigation: Use only a reviewed, trusted, version-pinned payment dependency before running this skill in a production environment.

Risk: Order numbers are used to read local order JSON files, which can be risky if order identifiers or paths are not constrained.

Mitigation: Validate order identifiers and restrict file access to the expected orders directory before use.

## Reference(s):

- [clawtip-weather ClawHub listing](https://clawhub.ai/clawtip/skills/clawtip-weather)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands and script output fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces order details, payment status, error messages, and a weather report after payment verification.]

## Skill Version(s):

1.0.9 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
