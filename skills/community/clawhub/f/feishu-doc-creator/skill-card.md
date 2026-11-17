## Description:

Creates Feishu documents including bitables, docs, spreadsheets, and slides, names them automatically, transfers ownership, and sends interactive-card links, with a weekly-report administration mode.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq654704712](https://clawhub.ai/user/qq654704712)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to let agents create Feishu documents through a bot application, return document links, and transfer ownership or collaboration permissions to the intended user or application.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses app-level Feishu credentials to create, transfer, and share documents rather than acting only through the requesting user's normal Feishu identity.

Mitigation: Use least-privileged Feishu app credentials dedicated to this skill and verify who can provide user_open_id, target_app_open_id, and admin_open_ids.

Risk: wen_admin mode can transfer ownership, add full-access administrators, and enable tenant-visible sharing for created documents.

Mitigation: Require preview or explicit approval before using wen_admin mode or enabling any tenant-wide sharing behavior.

Risk: Runtime dependencies are installed from Python package indexes during setup.

Mitigation: Install dependencies from a locked requirements set inside an isolated Python environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qq654704712/skills/feishu-doc-creator)
- [Feishu Open Platform - Create Bitable](https://open.feishu.cn/document/zh-cn/bitable-v1/app/create)
- [Feishu Open Platform - Create Docx Document](https://open.feishu.cn/document/zh-cn/docx-v1/document/create)
- [Feishu Open Platform - Transfer Document Owner](https://open.feishu.cn/document/zh-cn/drive-v1/permission/transfer_owner)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration instructions, API Calls]

**Output Format:** [JSON success or error objects, or plain text summaries, containing Feishu document names, types, tokens, and links.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill creates remote Feishu documents and can modify ownership, collaborators, and tenant-visible sharing settings depending on mode.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
