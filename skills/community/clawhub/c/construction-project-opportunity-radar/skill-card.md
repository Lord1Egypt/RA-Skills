## Description:

Finds and prioritizes early-stage construction opportunities from proposed projects, procurement intentions, and expiring service contracts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dragonzu](https://clawhub.ai/user/dragonzu)

### License/Terms of Use:

MIT-0

## Use Case:

Construction sales and business-development teams use this skill to find and rank Chinese infrastructure and building-project leads before tenders, with recommended follow-up actions.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: API credentials are stored locally and used to access a third-party service.

Mitigation: Review local credential storage and access before installing; restrict access to the API key and avoid including it in reports.

Risk: Free-trial registration transmits a hash derived from the device MAC address.

Mitigation: Require informed consent before registration; use an existing API key if device-derived registration is not acceptable.

Risk: Generated reports can contain signed links that bypass login for recipients.

Mitigation: Treat reports and signed URLs as sensitive; review recipients and avoid public posting or casual forwarding.

Risk: Opportunity scans consume metered API credits.

Mitigation: Confirm estimated credit usage before scanning and limit the number of calls.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/dragonzu/skills/construction-project-opportunity-radar)
- [API quick reference](references/api-quick.md)
- [Opportunity-scanning workflow](references/workflow.md)
- [Report template](references/report-template.md)
- [Registration and credential setup](references/auto-register.md)
- [Vendor skill documentation](https://ai.zhiliaobiaoxun.com/docs/skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, HTML reports, Guidance]

**Output Format:** [Markdown opportunity list with optional shareable HTML report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Ranked leads include source links, timing, estimated value, and suggested follow-up actions.]

## Skill Version(s):

1.0.8 (source: skill frontmatter and server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
