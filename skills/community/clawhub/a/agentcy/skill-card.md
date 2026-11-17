## Description:

Your OpenClaw team's marketing analyst - just tell your agent what you need to know about your clients' marketing and Agentcy delivers synthesized insights and recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twchase](https://clawhub.ai/user/twchase)

### License/Terms of Use:

MIT-0

## Use Case:

External marketing teams, agencies, and OpenClaw users use this skill to query client marketing performance, discover connected data sources, and request competitive or market research through Agentcy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Client marketing questions, domain context, and connected-source access are sent to Agentcy through the configured API key.

Mitigation: Use this skill only with data approved for Agentcy processing, and configure a least-privileged Agentcy API key.

Risk: The documented install command uses an unpinned installer version.

Mitigation: Prefer a pinned installer version when available and review the skill before deployment.

Risk: Freeform marketing queries may include secrets, PII, or confidential strategy.

Mitigation: Avoid submitting sensitive data unless it is approved for Agentcy processing.

## Reference(s):

- [Agentcy homepage](https://www.goagentcy.com)
- [Agentcy ClawHub skill page](https://clawhub.ai/twchase/skills/agentcy)
- [Agentcy publisher profile](https://clawhub.ai/user/twchase)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text synthesized marketing insights, research findings, source listings, and command guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AGENTCY_API_KEY, curl, and jq; calls Agentcy API endpoints over HTTPS.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
