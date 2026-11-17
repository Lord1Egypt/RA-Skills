## Description:

Automates generation of standardized Chinese official documents per GB/T 9704, with 18 template types, formal wording support, preview commands, and Markdown export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cryptocxf](https://clawhub.ai/user/cryptocxf)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, business users, and document authors use this skill to draft Chinese official documents such as notices, requests, reports, letters, meeting minutes, and plans with standardized structure and formatting guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated official-document drafts may contain incorrect, incomplete, or inappropriate wording for the final business or government context.

Mitigation: Review each generated draft manually and verify facts, dates, recipients, approvals, and wording before official stamping or submission.

Risk: Classified or confidential content may be exposed if users process sensitive documents through the skill.

Mitigation: Do not use this skill for classified or confidential documents; use the organization's approved secure channels instead.

Risk: The export command can write Markdown output to a user-specified path.

Mitigation: Use export only with paths the user intends to write and review the destination before running the command.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cryptocxf/skills/doc-formatter)
- [Quick Start Guide](references/quick-start.md)
- [Official Document Format Standards](references/format-standards.md)
- [Standard Phrase Library](references/phrase-library.md)
- [Document Template Library](references/template-library.md)
- [npm Package](https://www.npmjs.com/package/doc-formatter)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown documents with formatting notes and command-oriented guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May export generated drafts to a user-specified Markdown file path.]

## Skill Version(s):

1.0.0 (source: package.json, .claude-plugin/plugin.json, ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
