## Description:

Poll Feishu groups for new messages, download message resources, read Feishu docs/wiki/sheets/bitables, compile message-source markdown, judge which chat segments are worth preserving, and ingest valuable materials into the Research KB through a prepare/apply workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[myd2002](https://clawhub.ai/user/myd2002)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and research knowledge-base maintainers use this skill to ingest Feishu group messages, attachments, and cloud documents into a Research KB while preserving source-item status and provenance for backend persistence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task-controlled inputs can redirect credentials or repository writes.

Mitigation: Run only with trusted payloads, bind GITEA_BOT_TOKEN to an administrator-configured Gitea origin, and reject payload-selected repository URLs.

Risk: Local files may be archived too broadly during apply.

Mitigation: Restrict archived source paths to the prepare workspace and review apply contexts before execution.

Risk: Feishu and Gitea credentials can expose sensitive workspace or repository data.

Mitigation: Use least-privilege Feishu and Gitea credentials and protect Feishu token cache permissions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/myd2002/skills/feishu-ingest)
- [Feishu Open Platform API](https://open.feishu.cn/open-apis)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance and JSON task envelopes for prepare/apply workflows]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces inputItems and sourceItems status records; apply can create or update Research KB Markdown pages, catalog entries, indexes, and archived source files.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
