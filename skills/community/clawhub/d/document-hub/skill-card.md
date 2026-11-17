## Description:

Document Hub helps agents generate standardized PRD documents for multiple product types using customizable Jinja2 Markdown templates, with optional Feishu document publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[woai36d](https://clawhub.ai/user/woai36d)

### License/Terms of Use:

MIT-0

## Use Case:

Product managers, developers, and product teams use this skill to draft consistent PRDs for general products, AI features, APIs, data products, and platform products. It is most useful when an agent needs to turn structured product information into Markdown requirements documents or prepare content for Feishu publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated PRDs can contain sensitive roadmap, customer, or product details, especially when publishing through the Feishu flow.

Mitigation: Review and redact generated PRDs before sharing or uploading them to Feishu.

Risk: File output can write to an unintended location or overwrite an existing document when paths are chosen carelessly.

Mitigation: Use trusted JSON inputs and explicit safe output filenames or directories, and check for existing files before writing.

Risk: The API PRD template includes default WebSocket query-token guidance that may be unsafe if copied directly into an implementation.

Mitigation: Replace query-token authentication examples with a stronger authentication pattern before implementation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/woai36d/skills/document-hub)
- [Skill documentation](artifact/SKILL.md)
- [Base PRD template](artifact/templates/prd/base.md)
- [AI feature PRD template](artifact/templates/prd/ai-feature-prd.md)
- [API PRD template](artifact/templates/prd/api-prd.md)
- [Data product PRD template](artifact/templates/prd/data-product-prd.md)
- [Platform PRD template](artifact/templates/prd/platform-prd.md)

## Skill Output:

**Output Type(s):** [Markdown, Text, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown documents with optional JSON status output and Python or shell snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated PRDs may be returned as text, written to user-specified files, or prepared for Feishu upload.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
