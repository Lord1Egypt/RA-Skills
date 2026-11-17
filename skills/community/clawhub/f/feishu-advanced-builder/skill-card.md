## Description:

Feishu Advanced Builder helps agents create native Feishu whiteboard diagrams, manipulate Bitable data, and convert complex Markdown into Feishu Docx block structures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mydreamhorse](https://clawhub.ai/user/mydreamhorse)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to generate Feishu whiteboard diagrams from Mermaid or PlantUML, create Bitable spreadsheets from Markdown tables, and write structured Markdown content into Feishu Docx blocks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses Feishu app credentials with document, whiteboard, and Bitable write access.

Mitigation: Use a least-privilege Feishu app, store credentials only in trusted local environment variables, and test on non-sensitive Feishu documents first.

Risk: The FEISHU_BASE_URL environment variable can redirect API traffic away from the default Feishu endpoint.

Mitigation: Leave FEISHU_BASE_URL unset unless the endpoint is fully trusted and controlled.

Risk: Token-printing commands can expose tenant access tokens in terminal logs or shared execution traces.

Mitigation: Avoid running token-printing commands in logged environments and rotate Feishu credentials if tokens are exposed.

Risk: Helper scripts can remotely create or update Feishu documents, whiteboards, and tables.

Mitigation: Review target document IDs, table IDs, generated diagram code, and Markdown content before execution.

## Reference(s):

- [Feishu Board API Notes](references/feishu-board-api.md)
- [Feishu Open API](https://open.feishu.cn/open-apis)
- [ClawHub Skill Page](https://clawhub.ai/mydreamhorse/skills/feishu-advanced-builder)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Feishu API command guidance and helper-script outputs for document, whiteboard, and Bitable write workflows.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
