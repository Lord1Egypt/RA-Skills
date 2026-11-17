## Description:

Followup Swarm guides agents through a customer follow-up SOP for lead acquisition, customer management, visit route planning, and conversion funnel analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gaoshung1981888](https://clawhub.ai/user/gaoshung1981888)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external business users can use this skill to structure customer lead capture, CRM updates, follow-up records, route planning, and conversion reporting for sales workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may create persistent local CRM and task files containing customer information.

Mitigation: Confirm file-write behavior, storage location, retention, and deletion expectations before using the skill with real customer records.

Risk: The workflow may send customer, contact, or location data to named external workflow tools.

Mitigation: Use the skill only after confirming user consent, data-sharing boundaries, and privacy controls for the connected tools.

Risk: The artifact describes customer outreach and pricing-related workflows that require human approval.

Mitigation: Require a human reviewer to approve outbound communication and price or discount commitments before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gaoshung1981888/skills/followup-swarm)
- [Publisher profile](https://clawhub.ai/user/gaoshung1981888)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell command and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe CRM records, follow-up logs, route plans, and conversion reports.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
