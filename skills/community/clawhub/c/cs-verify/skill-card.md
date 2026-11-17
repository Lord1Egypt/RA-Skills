## Description:

Verify factual claims against live data sources and return structured verdicts with confidence scores.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cutthemustard](https://clawhub.ai/user/cutthemustard)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to check factual claims against a third-party verification API and interpret structured verdicts, confidence scores, freshness, and current truth values.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Claim text is sent to a third-party HTTPS service.

Mitigation: Submit only claims that are acceptable to share externally, and avoid secrets, personal data, confidential business facts, and regulated information unless the provider's privacy and retention terms are acceptable.

Risk: The artifact advertises an unpinned global MCP install.

Mitigation: Review the npm package before use, pin a version, prefer a local install, and avoid elevated privileges.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cutthemustard/skills/cs-verify)
- [Service Homepage](https://636865636b73756d.com)
- [Agent Card](https://636865636b73756d.com/.well-known/agent.json)
- [Service Metadata](https://636865636b73756d.com/.well-known/agent-service.json)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API calls, JSON]

**Output Format:** [Markdown guidance with bash examples and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [API responses are documented as verdicts with confidence scores, current truth values, freshness indicators, source counts, cache flags, request IDs, service URLs, and referral IDs.]

## Skill Version(s):

1.0.0 (source: artifact frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
