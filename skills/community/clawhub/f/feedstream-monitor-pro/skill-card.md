## Description:

Provides Chinese-language guidance and example workflows for monitoring security advisories, correlating products, tracking remediation status, and configuring alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

Proprietary

## Use Case:

Security teams use this skill for Chinese-language guidance and example workflows to review vulnerability advisories, compare them with product inventories, track response status, and prepare webhook alerts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The example code needs repairs before it can provide reliable monitoring and alerts.

Mitigation: Repair and test the examples before use; independently verify affected versions and scores before acting on results.

Risk: Webhook notifications include advisory descriptions and other advisory details.

Mitigation: Configure only webhook destinations you trust and review what advisory data the endpoint will receive.

Risk: Integrity results depend on a trusted baseline.

Mitigation: Preserve a trusted integrity baseline when using the integrity-checking guidance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/feedstream-monitor-pro)
- [NVD RSS feed example](https://nvd.nist.gov/feeds/xml/公告/misc/nvd-rss-analyzed.xml)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Code, Configuration, Analysis]

**Output Format:** [Chinese-language Markdown guidance with Python examples and JSON-oriented workflows]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Example code is provided for adaptation; repair and test it before relying on alerts or scores.]

## Skill Version(s):

1.0.1 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
