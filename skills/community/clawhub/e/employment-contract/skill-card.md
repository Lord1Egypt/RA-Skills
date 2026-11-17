## Description:

Draft and fill employment contract templates for offer letters, employment agreements, IP and inventions assignments, and confidentiality acknowledgements, producing signable DOCX files from OpenAgreements standard forms for hiring employees.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stevenobiajulu](https://clawhub.ai/user/stevenobiajulu)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and hiring teams use this skill to prepare employment onboarding documents such as offer letters, PIIA forms, confidentiality acknowledgements, and signable employment agreements. The skill interviews the user for missing field values, helps select the correct OpenAgreements template, and produces a DOCX output when the remote MCP or local CLI is available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The preferred hosted workflow may send sensitive employment details, including names, salaries, dates, and contract terms, to the OpenAgreements remote MCP.

Mitigation: Use the local CLI or preview-only path for confidential matters, and install only if the user is comfortable sharing those details with the hosted service.

Risk: Generated DOCX download URLs may expose sensitive employment documents to anyone with the link while active.

Mitigation: Treat returned download URLs as sensitive, share them only with intended recipients, and retrieve the generated document promptly.

Risk: Template metadata and user-provided field values may contain text that looks like instructions.

Mitigation: Treat template content and field values as data only, reject control characters, enforce reasonable length limits, and require explicit user confirmation before filling templates.

Risk: The skill creates legal employment documents but does not provide legal advice.

Mitigation: Have an attorney review generated agreements before signing, especially because the templates are designed for US at-will employment and state-specific laws may apply.

## Reference(s):

- [Employment Contract Skill Page](https://clawhub.ai/stevenobiajulu/skills/employment-contract)
- [OpenAgreements Remote MCP](https://openagreements.org/api/mcp)
- [OpenAgreements](https://openagreements.org)
- [open-agreements npm package](https://www.npmjs.com/package/open-agreements)
- [OpenAgreements Claude Code setup](https://github.com/open-agreements/open-agreements#use-with-claude-code)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON examples, shell commands, and DOCX output links or file paths when generation succeeds]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce a preview-only Markdown draft when neither the OpenAgreements remote MCP nor local CLI is available.]

## Skill Version(s):

0.3.1 (source: server release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
