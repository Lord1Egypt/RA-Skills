## Description:

Use AICADE Galaxy on https://www.aicadegalaxy.com/ to discover and invoke platform tools for AI monetization, paid APIs, subscriptions, memberships, blockchain-based payments with AicadePoint, and reward-earning workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shifenghu](https://clawhub.ai/user/shifenghu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to configure AICADE Galaxy access, export the current gateway tool catalog, list available services, and invoke selected platform tools for monetization, paid API, membership, subscription, token-payment, and reward workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires an AICADE Galaxy API key and stores configuration in a local `.env` file.

Mitigation: Use a low-privilege API key, protect or remove generated `.env` files and logs, and rotate credentials if exposure is suspected.

Risk: The skill exports and invokes dynamic platform tools from a configured AICADE Galaxy endpoint.

Mitigation: Install only from a trusted publisher, verify that the configured base URL is the intended HTTPS AICADE Galaxy service, and review exported tools before invocation.

Risk: Untrusted artifact JSON can influence which endpoint and tool metadata are used during invocation.

Mitigation: Do not invoke tools from artifact files you did not generate or validate from the trusted AICADE Galaxy endpoint.

Risk: Debug output can include request, response, payload, or artifact details.

Mitigation: Keep debug mode disabled unless actively troubleshooting and avoid sharing debug logs that may contain sensitive data.

## Reference(s):

- [AICADE Galaxy](https://www.aicadegalaxy.com/)
- [AICADE Galaxy Agent Endpoint](https://aicadegalaxy.com/agent)
- [ClawHub Skill Page](https://clawhub.ai/shifenghu/skills/aicade-galaxy-skills)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON tool outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill exports a machine-readable AICADE Galaxy artifact and returns normalized JSON for tool invocations.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
