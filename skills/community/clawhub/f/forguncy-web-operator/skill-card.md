## Description:

Provides functionality to interact with SpreadJS tables in web applications built by Forguncy (aka 活字格), specifically for extracting table data and column headers by dynamically identifying the table's fgcname attribute.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kadbbz](https://clawhub.ai/user/kadbbz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to read table names, table data, and column headers from authenticated Forguncy web pages that expose SpreadJS list views.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can bulk-read table contents from an authenticated Forguncy page.

Mitigation: Use it only for tables the user is authorized to access, avoid exporting more rows or columns than needed, and review extracted data before sharing it elsewhere.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kadbbz/skills/forguncy-web-operator)
- [Artifact Skill Definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, code, guidance]

**Output Format:** [Markdown with JavaScript snippets and short procedural guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The JavaScript snippets can return table identifiers, CSV table data, or column-header arrays when evaluated in an authorized Forguncy browser context.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
