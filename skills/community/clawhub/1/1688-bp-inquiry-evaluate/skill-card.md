## Description:

Generates 1688 shop staff and customer-service inquiry reception quality evaluations and improvement reports from authenticated CLI-fetched data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1688aiinfra](https://clawhub.ai/user/1688aiinfra)

### License/Terms of Use:

MIT-0

## Use Case:

External 1688 merchants and operations teams use this skill to review team-level and individual salesperson inquiry handling, conversion indicators, and improvement suggestions using real CLI-fetched account data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles an ALI_1688_AK access key for authenticated report queries.

Mitigation: Install it only in environments where that AK is intended for this 1688 shopkeeper configuration, and avoid exposing production AKs in chat, shell history, or process logs.

Risk: Reports can include buyer conversation details and salesperson or inquiry links.

Mitigation: Share generated reports only with recipients authorized to view the underlying 1688 inquiry and salesperson data.

Risk: The security review advises confirming the OpenClaw gateway URL is trusted before use.

Mitigation: Verify the deployment gateway endpoint and local OpenClaw configuration before enabling the skill.

## Reference(s):

- [Configure Capability Guide](references/capabilities/configure.md)
- [Business Inquiry Evaluation Summary Guide](references/capabilities/bp_inquiry_evaluate_summary.md)
- [Business Inquiry Evaluation Sales Detail Guide](references/capabilities/bp_inquiry_evaluate_sales_detail.md)
- [1688 Team Service Evaluation](https://air.1688.com/app/bp-boot/a2a-team-newton/index.html)
- [ClawHub Skill Page](https://clawhub.ai/1688aiinfra/skills/1688-bp-inquiry-evaluate)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance]

**Output Format:** [Markdown reports and JSON CLI responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return an open-tab action for date ranges beyond the supported query window.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
