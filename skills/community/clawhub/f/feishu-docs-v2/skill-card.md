## Description:

Feishu Docs helps agents read, create, update, delete, import, and list Feishu cloud documents through a Node.js CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[upupc](https://clawhub.ai/user/upupc)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to manage Feishu cloud documents from Claude Code or similar agent sessions, including reading documents, creating or importing content, listing folders, and updating or deleting files when authorized.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A configurable FEISHU_DOMAIN can expose Feishu app credentials and document data to an unintended server.

Mitigation: Keep FEISHU_DOMAIN fixed to the official Feishu/Lark API origin and install the skill only when the publisher and runtime environment are trusted.

Risk: Update, delete, and import commands can overwrite cloud document content, delete files, or upload sensitive local files.

Mitigation: Use a least-privilege Feishu app, confirm document and folder tokens before destructive commands, and import only files intended for Feishu.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/upupc/skills/feishu-docs-v2)
- [Feishu Docs homepage](https://github.com/upupc/feishu-docs)
- [Feishu Open Platform](https://open.feishu.cn)
- [Feishu app management](https://open.feishu.cn/app)
- [Lark/Feishu Node SDK](https://github.com/larksuite/node-sdk)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Files, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell commands; the CLI can emit JSON, Markdown, text, and local files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js plus FEISHU_APP_ID and FEISHU_APP_SECRET environment variables.]

## Skill Version(s):

0.1.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
