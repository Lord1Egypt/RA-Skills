## Description:

Merges multiple Feishu weekly report documents by preserving the original Markdown content, grouping it under Part1-Part5 sections in source order, and creating a new Feishu cloud document.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ganguagua](https://clawhub.ai/user/ganguagua)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and operations teams use this skill to combine multiple Feishu weekly reports into one structured document while retaining each contributor's original text and formatting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Potentially sensitive Feishu report contents are written to predictable plaintext files in /tmp.

Mitigation: Use a private per-run temporary directory or in-memory processing, and remove only files created by the skill.

Risk: The skill can create a new Feishu document from fetched report contents.

Mitigation: Require explicit weekly-report merge intent and confirm the destination and title before creating the document.

Risk: The merged output may reformat section structure in ways that are not fully disclosed to users.

Mitigation: Disclose that the merge normalizes Part1-Part5 section headers and inserts contributor sections before execution.

## Reference(s):

- [Chapter Parsing Reference](references/chapter_parsing.md)
- [ClawHub Skill Page](https://clawhub.ai/ganguagua/skills/feishu-weekly-report-merger)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, API Calls, Guidance]

**Output Format:** [Markdown content for a newly created Feishu document, with supporting shell commands and Feishu tool calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves source document order and Feishu Markdown formatting where the merge script supports it.]

## Skill Version(s):

1.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
