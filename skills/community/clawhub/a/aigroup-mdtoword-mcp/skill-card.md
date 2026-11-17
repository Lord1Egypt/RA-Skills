## Description:

Use `aigroup-mdtoword-mcp` to convert Markdown into `.docx`, including Markdown file conversion, generated Markdown conversion, table-to-Markdown preprocessing, formula handling, table handling, and page-layout requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackdark425](https://clawhub.ai/user/jackdark425)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and knowledge workers use this skill to convert existing or generated Markdown, including tables and formulas, into polished Word .docx documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill launches the external aigroup-mdtoword-mcp package through an unpinned npx command.

Mitigation: Pin an audited package version, use a locked or trusted package source, and run with limited file and network access before processing private documents.

## Reference(s):

- [Markdown to Word MCP Capabilities](references/capabilities.md)
- [AIGroup Markdown to Word MCP Repository](https://github.com/jackdark425/aigroup-mdtoword-mcp)
- [ClawHub Skill Page](https://clawhub.ai/jackdark425/skills/aigroup-mdtoword-mcp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with tool-routing instructions and generated .docx file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces or routes conversion work toward native .docx documents with optional styling, formulas, tables, headers, footers, page numbers, and local images.]

## Skill Version(s):

0.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
