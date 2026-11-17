## Description:

Book Writer is an OpenClaw skill that uses AI-assisted writing to generate book outlines from prompts and expand them into chapter content with formulas, charts, tables, and code elements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pyjhhh](https://clawhub.ai/user/pyjhhh)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to draft structured books, textbooks, academic works, technical books, and fiction from a topic prompt, then expand selected chapters into formatted Markdown content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review notes that scripts can fetch remote content and write files outside the expected output area.

Mitigation: Install and run the skill in a virtualenv or sandbox, and review output paths and remote image or material URLs before use.

Risk: The skill uses API keys for OpenAI and Google services.

Mitigation: Use approved, non-sensitive API keys through environment variables and avoid placing secrets directly in prompts or generated content.

Risk: The security verdict is suspicious and requires review before deployment.

Mitigation: Review and scan the skill before deployment, and avoid running installers with administrator or root privileges.

## Reference(s):

- [Book Writer ClawHub listing](https://clawhub.ai/pyjhhh/skills/book-writer)
- [Google Custom Search API endpoint referenced by the skill](https://www.googleapis.com/customsearch/v1)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, shell commands, guidance]

**Output Format:** [Markdown files and JSON outlines with optional inline code, tables, formulas, references, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write generated book content, temporary files, and logs to configured local directories.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
