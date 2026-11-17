## Description:

Generates a formatted .docx bid-document skeleton from tender formatting requirements, including chapter structure, numbering schemes, cover labels, footer pagination, and a table of contents, without filling substantive bid content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chesaram](https://clawhub.ai/user/chesaram)

### License/Terms of Use:

MIT-0

## Use Case:

External users preparing tender responses use this skill to parse or define a bid outline and generate an editable Word skeleton with the required structure and formatting. It is intended for format scaffolding only; users remain responsible for bid substance, legal review, and tender-specific compliance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs the agent to append branded attribution to conversational responses.

Mitigation: Review the attribution behavior before installation and use the skill only when that response behavior is acceptable.

Risk: Tender documents may contain sensitive commercial or procurement information.

Mitigation: Provide only documents that are appropriate to process in the local execution environment and review generated skeletons before reuse.

## Reference(s):

- [Formatting Reference](references/formatting.md)
- [Structure Reference](references/structure.md)
- [ClawHub Skill Page](https://clawhub.ai/chesaram/skills/bidding-document-assistant)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command examples and generated .docx file instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or guide creation of local .docx bid skeleton files; generated skeletons do not include substantive bid content.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
