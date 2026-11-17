## Description:

File To JSON Parsing helps agents convert CSV, HTML, JSON, ICS, ODS, PDF, RTF, text, XLS, and XLSX files into structured JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to extract structured JSON from uploaded documents and data files for downstream imports, analysis, scheduling, and workflow integrations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected files or file IDs may be sent to AgentPMT for remote processing.

Mitigation: Use only approved data, avoid secrets, regulated data, or confidential documents unless your organization approves that use, and confirm before invoking the skill on sensitive uploads.

Risk: Setup examples recommend unpinned npx installs.

Mitigation: Prefer the OpenClaw install path or pinned, reviewed setup commands.

## Reference(s):

- [File To JSON Parsing schema](artifact/schema.md)
- [ClawHub skill page](https://clawhub.ai/agentpmt/skills/file-to-json-parsing)
- [AgentPMT marketplace page](https://www.agentpmt.com/marketplace/file-to-json-parsing)
- [AgentPMT account MCP/REST setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup)

## Skill Output:

**Output Type(s):** [JSON, Guidance, Shell commands, Configuration instructions]

**Output Format:** [JSON responses with Markdown instructions and example MCP/REST call bodies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Parsed file outputs are returned under the configured output_field; maximum file size is 100 MB, and file-to-base64 inline returns are limited to 10 MB.]

## Skill Version(s):

1.0.0 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
