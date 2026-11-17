## Description:

Security audit framework for AI agent skills, MCP servers, and packages that uses the agent's LLM for analysis and a shared trust database for findings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[starbuck100](https://clawhub.ai/user/starbuck100)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to check package, skill, and MCP server safety before installation or use. It supports registry lookups, integrity checks, trust score calculation, manual audits, peer review, and structured audit report upload.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically influence install and use decisions for packages, skills, and MCP servers.

Mitigation: Review the reported findings and require explicit user confirmation before proceeding when the registry is unavailable, reports are missing, or the result is not clearly trusted.

Risk: Auto-upload workflows can send source-derived audit reports to a third-party registry.

Mitigation: Do not run uploads on private, proprietary, or secret-bearing code unless the report has been inspected and sanitized first.

Risk: Registry endpoints and API credentials affect audit integrity and reporter identity.

Mitigation: Keep ECAP_REGISTRY_URL unset or pinned to a trusted registry, treat example bearer tokens as compromised, and keep ECAP_API_KEY out of shared reports and logs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/starbuck100/skills/ecap-security-auditor)
- [Trust Registry](https://skillaudit-api.vercel.app)
- [Trust Registry API documentation](https://skillaudit-api.vercel.app/docs)
- [SKILL.md](artifact/SKILL.md)
- [README.md](artifact/README.md)
- [FERRET-SCAN-ANALYSIS.md](artifact/FERRET-SCAN-ANALYSIS.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON audit reports and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May query a third-party registry API, compare SHA-256 hashes, and prepare report payloads for upload.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
