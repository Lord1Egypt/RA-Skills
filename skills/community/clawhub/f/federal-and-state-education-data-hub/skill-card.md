## Description:

Federal And State Education Data Hub helps agents query World Bank education statistics by country or region, including enrollment, literacy, gender parity, completion, teacher-ratio, and SDG 4 indicators through AgentPMT-hosted remote tool calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and policy teams use this skill to request country or regional education indicators for policy analysis, benchmarking, equity reporting, trend review, and program impact evaluation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential, wallet, payment, or unrelated personal data could be exposed if supplied in prompts or tool inputs.

Mitigation: Keep inputs limited to the education-data query and use the AgentPMT setup skills for credential handling.

Risk: The remote data may be unavailable, delayed, or incomplete for some countries, regions, indicators, or years.

Mitigation: Check returned availability metadata, handle country-resolution errors, and verify unclear schemas or examples before production integrations.

## Reference(s):

- [Generated action schema](artifact/schema.md)
- [AgentPMT marketplace product](https://www.agentpmt.com/marketplace/education-statistics-literacy)
- [ClawHub skill page](https://clawhub.ai/agentpmt/skills/federal-and-state-education-data-hub)
- [AgentPMT overview](https://clawhub.ai/agentpmt/what-is-agentpmt)
- [AgentPMT account MCP/REST setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with JSON request examples and remote-tool response handling guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill defines one AgentPMT action, query_education_data; remote calls return JSON education data, metadata, optional regional comparisons, gender parity analysis, and SDG alignment.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
