## Description:

Build and query a FAQ knowledge base from markdown files for business operations Q&A.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imbing](https://clawhub.ai/user/imbing)

### License/Terms of Use:

MIT

## Use Case:

Employees, support teams, and business operations agents use this skill to create, manage, search, and export FAQ knowledge bases for Feishu or similar business Q&A workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: FAQ entries are stored locally in ~/.faq-bot unless FAQ_BOT_DIR is set.

Mitigation: Set FAQ_BOT_DIR to an approved local path and review storage handling before installing or running the skill.

Risk: Imported markdown content can be reused in automated answers.

Mitigation: Import only FAQ files whose content has been reviewed and is appropriate for automated responses.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/imbing/skills/bo-faq-bot)
- [Publisher profile](https://clawhub.ai/user/imbing)
- [README](artifact/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The FAQ search command returns matched questions, answers, confidence scores, tags, and the top answer as JSON.]

## Skill Version(s):

0.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
