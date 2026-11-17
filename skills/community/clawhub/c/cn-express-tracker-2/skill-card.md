## Description:

中文快递查询 helps an agent look up logistics status, tracking history, carrier information, and detail links for major Chinese express delivery companies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huanyuai](https://clawhub.ai/user/huanyuai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when they need an agent to query Chinese package-delivery status from a tracking number, optionally with a carrier code, and return the carrier, current status, route history, and detail link.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shipment identifiers and any requested phone-number suffix may be submitted to kuaidi100.com for lookup.

Mitigation: Notify users before lookup, request only the minimum identifiers needed, and avoid retaining or sharing tracking details beyond the lookup task.

Risk: The package references a tracking script that is not included, so it may not work as written.

Mitigation: Verify the package contents before relying on execution; if the script is absent, treat the release as incomplete and request a corrected package.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huanyuai/skills/cn-express-tracker-2)
- [Publisher profile](https://clawhub.ai/user/huanyuai)
- [Kuaidi100 data source](https://www.kuaidi100.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown or plain text with optional inline shell commands and logistics results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include carrier name, tracking number, current status, route history, and a detail link.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
