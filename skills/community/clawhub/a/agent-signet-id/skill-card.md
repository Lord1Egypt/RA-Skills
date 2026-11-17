## Description:

Register with Signet to receive a trust score and API key. Look up agent trust scores, report transactions, and manage agent configuration. Use when you need to establish trust identity, verify another agent's trustworthiness, or interact with the Signet trust scoring platform.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deepcapt](https://clawhub.ai/user/deepcapt)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to register with Signet, retrieve trust scores, report transaction outcomes, rotate API keys, and manage agent scoring configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses an external Signet API and may send agent configuration, transaction metadata, or scoring data.

Mitigation: Install only when Signet integration is intended and review what data is sent before making API calls.

Risk: SIGNET_API_KEY grants authenticated access to Signet operations.

Mitigation: Keep SIGNET_API_KEY secret, store it as an environment variable, and avoid logging or sharing it outside api.agentsignet.com.

Risk: Transaction metadata could expose sensitive operational context if overfilled.

Mitigation: Do not include credentials, API keys, PII, file contents, sensitive prompts, or internal system details in metadata.

## Reference(s):

- [Agent Signet ID on ClawHub](https://clawhub.ai/deepcapt/skills/agent-signet-id)
- [Agent Signet for Agents](https://agentsignet.com/for-agents)
- [Agent Signet](https://agentsignet.com)
- [Signet API OpenAPI Specification](https://agentsignet.com/.well-known/skills/signet-api/)

## Skill Output:

**Output Type(s):** [guidance, API calls, shell commands, configuration]

**Output Format:** [Markdown with JSON and HTTP request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SIGNET_API_KEY for authenticated Signet API operations.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
