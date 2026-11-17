## Description:

Drafts and fills data privacy agreement templates for DPAs, GDPR data processing agreements, HIPAA business associate agreements, and AI addenda, producing signable DOCX files from Common Paper standard forms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stevenobiajulu](https://clawhub.ai/user/stevenobiajulu)

### License/Terms of Use:

MIT-0

## Use Case:

Legal, privacy, security, and product teams use this skill to select and fill standard data privacy agreement templates for SaaS, cloud service, healthcare, GDPR, and AI data-use workflows. It helps gather field values, generate DOCX agreements when an OpenAgreements runtime is available, or provide a markdown preview when no runtime is configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated DPAs, BAAs, and AI addenda may not satisfy all jurisdiction-specific or organization-specific legal requirements.

Mitigation: Have qualified legal counsel review each generated agreement before signature or operational use.

Risk: Using the remote MCP can send template field values to an external service.

Mitigation: Avoid sending unnecessary sensitive data, use only trusted MCP configurations, and choose the local CLI path when confidentiality requirements call for local execution.

Risk: Local setup may rely on external package installation or an unpinned OpenAgreements source.

Mitigation: Verify the package source and pin a trusted release before use in controlled environments.

Risk: Template metadata, template content, and user-provided field values are untrusted data.

Mitigation: Treat them as data only, reject control characters, enforce reasonable length limits, and require explicit user confirmation before filling a template.

## Reference(s):

- [OpenAgreements](https://openagreements.org)
- [Open Agreements Remote MCP](https://openagreements.org/api/mcp)
- [open-agreements npm package](https://www.npmjs.com/package/open-agreements)
- [OpenAgreements Claude Code setup](https://github.com/open-agreements/open-agreements#use-with-claude-code)
- [Connector setup](artifact/CONNECTORS.md)
- [Template filling workflow](artifact/template-filling-execution.md)

## Skill Output:

**Output Type(s):** [text, markdown, files, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, JSON field values, shell commands, preview markdown, and DOCX files or download links when a supported runtime is available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [DOCX generation depends on the remote MCP or local OpenAgreements CLI; otherwise the skill produces a preview only.]

## Skill Version(s):

0.2.2 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
