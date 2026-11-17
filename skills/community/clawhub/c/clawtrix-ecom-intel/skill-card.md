## Description:

Surfaces up to three ClawHub skill recommendations for e-commerce agents based on platform, workflows, scale, integrations, installed skills, and risk posture.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nicope](https://clawhub.ai/user/nicope)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and e-commerce operations teams use this skill to audit an agent's context and choose ClawHub skills for store onboarding, fulfillment, inventory, support, returns, payments, and peak-season readiness.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow reads local agent context and writes a recommendation report that could capture sensitive operational details.

Mitigation: Confirm that reading SOUL.md and saving the report is acceptable, and avoid including raw credentials, customer data, or unnecessary operational details in the generated report.

Risk: E-commerce agents may operate near payment systems, customer PII, and inventory write access.

Mitigation: Run a security audit before installing recommended skills and review each candidate for platform fit, volume constraints, and data access before deployment.

Risk: Search-based recommendations can be mismatched to the store platform, existing installed skills, or current operational needs.

Mitigation: Manually review the top recommendations against the agent mission, installed skills, store platform, and order volume before installing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nicope/skills/clawtrix-ecom-intel)
- [Publisher profile](https://clawhub.ai/user/nicope)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown recommendation report with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Limits recommendations to the top three candidates.]

## Skill Version(s):

0.1.1 (source: server release metadata, created 2026-04-02)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
