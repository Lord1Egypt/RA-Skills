## Description:

Create a traceable, screening-level freedom-to-operate report from a supplied risk-point Word document and user-approved PatSnap search expressions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

Patent analysts, IP teams, product counsel, and R&D owners use this skill to turn a risk-point Word document and reviewed PatSnap search expressions into a structured FTO screening package with candidate retrieval, claim comparison, triage, and report outputs. The output supports screening and follow-up planning, not a legal clearance opinion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses PatSnap API configuration and may handle private credentials.

Mitigation: Keep the PatSnap base URL pinned to an approved PatSnap host, prefer environment or secure credential storage, and do not use untrusted API configuration files.

Risk: Generated JSON and reports may include confidential product details or local input paths.

Mitigation: Inspect generated JSON and reports before sharing, and transmit confidential source materials to external services only with user authorization.

Risk: The server security verdict is suspicious because credential-handling and privacy issues require review before installation.

Mitigation: Install only when the API configuration and generated outputs can be controlled and reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuanzhian-patsnap/skills/create-fto-screening-report-ip)
- [PatSnap Data-Access Policy](references/api_call_policy.md)
- [PatSnap Open Platform API Reference for FTO Screening](references/api_reference.md)
- [Claim Chart JSON Schema](references/claim_chart_schema.md)
- [Generic FTO Screening Report Requirements](references/report_requirements.md)
- [PatSnap Developer Center](https://open.patsnap.com/devportal)
- [PatSnap MCP marketplace](https://open.patsnap.com/marketplace/mcp-servers)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, JSON, HTML, DOCX]

**Output Format:** [Structured JSON evidence, HTML and DOCX reports, Markdown guidance, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated reports and evidence packages are run-specific and should stay outside the skill package.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
