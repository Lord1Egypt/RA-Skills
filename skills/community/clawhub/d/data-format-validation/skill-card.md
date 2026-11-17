## Description:

Data Format Validation helps agents validate JSON, email, UUID, IP address, MAC address, credit card, IBAN, phone, color, ISBN, Base64, URL, and regex inputs through AgentPMT-hosted remote tool calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to validate common input formats and receive structured validity details before ingesting, routing, or processing data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Validation inputs may be sent to AgentPMT and can include complete personal or financial values.

Mitigation: Keep inputs scoped to the minimum needed and avoid real payment cards, bank identifiers, customer records, secrets, private URLs, or sensitive JSON/Base64 unless AgentPMT processing and logging terms are approved.

Risk: Security evidence flags the release as suspicious because it is a remote validator with weak scoping and update guidance.

Mitigation: Use pinned, reviewed installation paths, confirm schemas through approved AgentPMT setup routes, and review or scan the skill before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/agentpmt/skills/data-format-validation)
- [AgentPMT Marketplace Page](https://www.agentpmt.com/marketplace/data-format-validation)
- [Data Format Validation Schema](artifact/schema.md)

## Skill Output:

**Output Type(s):** [guidance, configuration, API calls, JSON]

**Output Format:** [Markdown instructions with JSON request and response shapes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Remote validation actions return a validity boolean, message, and format-specific parsed details.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
