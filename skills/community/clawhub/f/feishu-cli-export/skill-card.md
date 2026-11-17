## Description:

Exports Feishu or Lark cloud documents and wiki pages to local Markdown files, with documented options for PDF and Word export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[giswilson](https://clawhub.ai/user/giswilson)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and document owners use this skill to export Feishu/Lark documents or wiki pages into local Markdown, PDF, or Word files for review, processing, archiving, or migration workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires Feishu document access and can write exported documents, images, and assets to local paths.

Mitigation: Grant only the Feishu scopes needed for the export task and treat generated files and cached tokens as sensitive.

Risk: The security evidence flags a documented local-file upload/import workflow that is outside the main export purpose.

Mitigation: Avoid local-file import or upload actions unless that capability is explicitly intended and confirmed before execution.

Risk: Exported tables or directory nodes may be incomplete or placeholder-like according to the artifact documentation.

Mitigation: Review exported content, especially tables and wiki directory nodes, before relying on it for downstream processing.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/giswilson/skills/feishu-cli-export)
- [Publisher Profile](https://clawhub.ai/user/giswilson)

## Skill Output:

**Output Type(s):** [text, markdown, files, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and generated local document files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create exported Markdown, PDF, Word, image, and asset files on the local filesystem.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
