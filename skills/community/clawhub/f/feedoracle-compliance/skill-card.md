## Description:

MiCA compliance evidence and stablecoin risk scoring for regulated tokenized markets. 27 MCP tools with ES256K-signed responses. Use when the user explicitly asks about stablecoin compliance, MiCA regulatory status, or needs verifiable evidence for audit workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[feedoracle](https://clawhub.ai/user/feedoracle)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agents, and compliance teams use this skill when a user explicitly requests stablecoin MiCA status, issuer due diligence, peg and reserve risk data, or verifiable evidence for audit workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User questions, token symbols, agent registration details, or audit decisions can be sent to feedoracle.io when the corresponding tool is invoked.

Mitigation: Invoke the skill only for explicit compliance, MiCA, stablecoin, evidence, KYA, audit, or report requests; avoid PII and unrelated conversation context.

Risk: KYA registration and audit logging are retention-oriented workflows.

Mitigation: Use KYA registration and audit logging only when the user intends the remote service to retain that profile or decision record.

Risk: Installer examples using latest package tags can change over time.

Mitigation: Prefer a pinned installer version when available for production or audited deployments.

## Reference(s):

- [FeedOracle Homepage](https://feedoracle.io)
- [FeedOracle MCP Server](https://feedoracle.io/mcp/)
- [FeedOracle API Docs](https://feedoracle.io/docs)
- [FeedOracle MCP Repository](https://github.com/feedoracle/feedoracle-mcp)
- [FeedOracle Trust Policy](https://github.com/feedoracle/feedoracle-mcp/blob/main/docs/TRUST_POLICY.md)
- [FeedOracle JWKS](https://feedoracle.io/.well-known/jwks.json)
- [ClawHub Skill Page](https://clawhub.ai/feedoracle/skills/feedoracle-compliance)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, markdown, API calls]

**Output Format:** [Markdown with inline shell commands, JSON configuration examples, and API-backed compliance evidence summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses may include signed evidence identifiers, ES256K signatures, pack IDs, JWKS URLs, audit trail identifiers, or generated report references when requested by the user.]

## Skill Version(s):

1.2.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
