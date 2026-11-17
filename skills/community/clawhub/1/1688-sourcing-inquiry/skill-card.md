## Description:

1688 Sourcing Inquiry helps an agent turn vague procurement needs into structured 1688 sourcing inquiries so the platform can match suppliers and quotation options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1688aiinfra](https://clawhub.ai/user/1688aiinfra)

### License/Terms of Use:

MIT-0

## Use Case:

External procurement users and agents use this skill when a buyer has a product name, quantity, and requirements but has not selected a specific product or supplier. The skill submits a 1688 sourcing inquiry after required fields are collected.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a 1688 access key and handles OAuth credential material.

Mitigation: Install only after reviewing the skill, provide credentials only in trusted environments, and rotate the access key if it may have been exposed.

Risk: Command usage is reported to the 1688 gateway.

Mitigation: Use the skill only when this telemetry behavior is acceptable for the deployment context.

Risk: Credential status or configuration output could appear in shared logs or transcripts.

Mitigation: Avoid running configure status commands in shared logs or transcripts.

## Reference(s):

- [1688 Sourcing Inquiry on ClawHub](https://clawhub.ai/1688aiinfra/skills/1688-sourcing-inquiry)
- [AK configuration guide](references/capabilities/configure.md)
- [Procurement capability guide](references/capabilities/procurement.md)
- [Common error handling](references/common/error-handling.md)
- [Skill usage telemetry notes](references/skill埋点说明.md)
- [1688 skills gateway](https://skills-gateway.1688.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration instructions, Guidance]

**Output Format:** [JSON containing success, markdown, and data fields; agents should present the markdown field to users]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and a configured ACCESS_KEY for authenticated 1688 gateway calls.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
