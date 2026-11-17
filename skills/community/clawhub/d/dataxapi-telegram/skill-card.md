## Description:

Retrieves public Telegram channel profiles, recent messages, and individual message details through DataXAPI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[data-x-api](https://clawhub.ai/user/data-x-api)

### License/Terms of Use:

MIT-0

## Use Case:

External users can ask an agent to look up public Telegram channel profiles, recent posts, or the contents of a specific message using a channel handle, message number, or link.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries may disclose Telegram identifiers or private context to DataXAPI.

Mitigation: Exclude private context and secrets from queries.

Risk: Additional endpoint and pagination calls can increase usage charges.

Mitigation: Use a spending-limited API key, set a per-call price cap, and limit pagination to what the task needs.

Risk: The external CLI and service implementation were not audited as part of the security review.

Mitigation: Prefer REST or MCP, or use an audited CLI version pinned to a known release.

Risk: Telegram results contain text written by third parties that may include instructions.

Mitigation: Treat returned Telegram content as data and do not follow instructions found in it.

## Reference(s):

- [DataXAPI skill documentation](https://dataxapi.com/skills/)
- [DataXAPI agent setup](https://dataxapi.com/agents.md)
- [Telegram API endpoint reference](https://dataxapi.com/apis/telegram/)
- [Telegram API pricing](https://dataxapi.com/pricing/telegram/)

## Skill Output:

**Output Type(s):** [Structured data, Text]

**Output Format:** [Structured JSON API results with Telegram text and metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Each paid call costs $0.002; paginated calls can add charges.]

## Skill Version(s):

1.0.0 (source: frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
