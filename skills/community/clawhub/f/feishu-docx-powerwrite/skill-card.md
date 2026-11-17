## Description:

High-quality Feishu/Lark Docx writing via OpenClaw for turning Markdown into well-formatted Feishu Docx content with headings, lists, nesting, and code blocks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiongjjlj](https://clawhub.ai/user/xiongjjlj)

### License/Terms of Use:


## Use Case:

Developers, operators, and Feishu/Lark users use this skill to generate, append, or replace Docx document content from Markdown while preserving readable document structure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can mutate Feishu/Lark Docx documents through user-provided Feishu access, including full-document replacement.

Mitigation: Review the target document before writes, prefer append mode for routine updates, and use replace mode only when full overwrite is intended and explicitly confirmed.

Risk: Misconfigured Feishu credentials or scopes can prevent writes or grant broader document access than intended.

Mitigation: Use the user's own Feishu app credentials, verify Docx/Drive scopes, and avoid hardcoding tokens or document links in the skill.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xiongjjlj/skills/feishu-docx-powerwrite)
- [Docx templates](references/templates.md)
- [Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with Feishu/Lark Docx writing guidance and setup shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May append to documents or replace full document content when explicitly confirmed.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
