## Description:

飞书知识管理工具：当用户发送外部文章链接时，获取内容、存入飞书文档，并将知识要点归纳到飞书知识库。

This skill is ready for commercial/non-commercial use.

## Publisher:

[subwukong](https://clawhub.ai/user/subwukong)

### License/Terms of Use:


## Use Case:

External users and teams with Feishu workspaces use this skill to save articles from supported link types into Feishu Docs and maintain categorized knowledge summaries in a Feishu knowledge base. It can also guide a daily organization task for duplicate removal and knowledge-base structure cleanup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad Feishu write access could store or modify documents outside the intended knowledge-base scope.

Mitigation: Use a narrowly permissioned Feishu account or designated folder and confirm scope before storing links.

Risk: External article links may contain sensitive, internal, or unsuitable content that should not be persisted.

Mitigation: Confirm before storing sensitive or internal links and review generated summaries before adding them to the knowledge base.

Risk: The daily cron task can repeatedly reorganize or remove documents without sufficient oversight.

Mitigation: Enable scheduled cleanup only with clear scope, audit logs, rollback or version history, and a documented removal process.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and structured workflow guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce instructions that call Feishu document tools, link-reading tools, and an optional OpenClaw cron command.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
