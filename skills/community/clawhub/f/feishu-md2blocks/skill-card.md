## Description:

Insert rich Markdown content (including tables) into Feishu documents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deadblue22](https://clawhub.ai/user/deadblue22)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to convert Markdown into Feishu document blocks and insert formatted content such as tables, code blocks, and nested lists at a chosen position in an existing document.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The --replace mode can delete existing Feishu document blocks.

Mitigation: Prefer append or --after for normal edits, and use --replace only after confirming the doc_token and preserving a backup or document version history.

Risk: The skill uses configured Feishu app credentials and sends provided Markdown to Feishu APIs.

Mitigation: Install and run it only when those credentials and the Markdown content are appropriate for Feishu processing.

Risk: Large or media-heavy Markdown may not insert as expected because images need separate upload steps, inserts are capped at 1000 blocks, and document edits are rate limited.

Mitigation: Split large documents, handle image upload separately, and pace edits within the documented Feishu rate limit.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/deadblue22/skills/feishu-md2blocks)
- [Feishu tenant access token API](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal)
- [Feishu Markdown block convert API](https://open.feishu.cn/open-apis/docx/v1/documents/blocks/convert)
- [Feishu document descendant block API](https://open.feishu.cn/open-apis/docx/v1/documents/{doc_token}/blocks/{parent_id}/descendant)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and Python script usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Feishu app credentials from the local OpenClaw configuration and sends provided Markdown to Feishu APIs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
