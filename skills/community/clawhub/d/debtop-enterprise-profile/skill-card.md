## Description:

Summarizes an enterprise's publicly published debt-transfer and disposal notices, including disclosed amounts, related parties, timeline, and guarantees.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ninjaliang](https://clawhub.ai/user/ninjaliang)

### License/Terms of Use:

MIT-0

## Use Case:

External users provide an enterprise name to review its publicly disclosed debt notices, amounts, related parties, and guarantee details. The summary is not a credit report, risk rating, or investment recommendation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The guest-access helper stores short-lived access and refresh tokens and a device identifier in a local user cache.

Mitigation: Prefer a platform-managed MCP/OAuth connection when available; review local bash/Python helpers and restrict cache access to the user.

Risk: Guest credentials could be exposed to an untrusted service if an alternate endpoint is used.

Mitigation: Only connect to agent.debtop.com unless you control and trust the alternate service; do not forward guest credentials elsewhere.

Risk: Public notices may be incomplete or outdated and can be mistaken for a credit assessment.

Mitigation: Label the data as public-notice disclosures, provide the query time and original notice links, and avoid credit ratings or investment conclusions.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/ninjaliang/skills/debtop-enterprise-profile)
- [Guest access and prerequisites](artifact/references/guest-access.md)
- [Available tools and fields](artifact/references/tools-and-fields.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown summary with tables and links to source notices]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a query time and disclosed-data caveats; cites notice links as returned.]

## Skill Version(s):

1.0.9 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
