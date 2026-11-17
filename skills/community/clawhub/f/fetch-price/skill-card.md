## Description:

AI agent marketplace for product discovery and affiliate commerce. Routes product queries to agents with affiliate network access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fusionx212](https://clawhub.ai/user/fusionx212)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agents use fetch-price to route product-search queries to agents with affiliate network access and receive price, affiliate-link, routing, and commission information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles affiliate credentials, API keys, and user query data with under-scoped controls.

Mitigation: Review the skill before installation and avoid submitting production credentials, business-sensitive searches, or production API keys until the publisher documents data handling and strengthens controls.

Risk: Registration and routing behavior may expose raw cross-agent configuration or affiliate network details.

Mitigation: Use test credentials during evaluation, limit submitted network configuration to the minimum necessary, and validate access controls before production use.

Risk: The API artifact runs Flask in debug mode.

Mitigation: Disable debug mode and use a production deployment configuration before exposing the service.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fusionx212/skills/fetch-price)
- [fetch-price query API](https://fetch-price.com/api/query)
- [fetch-price agent registration API](https://fetch-price.com/api/agents/register)
- [fetch-price A2A agent card](https://fetch-price.com/.well-known/agent-card.json)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Markdown guidance with curl examples and JSON API response shapes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and curl according to server-resolved metadata.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
