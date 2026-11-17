## Description:

Feishu Doc Sync helps agents synchronize local documents to Feishu Docs and operate Feishu document tables, including delete-and-insert table updates, header-row creation, insert positioning, column-width handling, and three-phase diff sync.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deadblue22](https://clawhub.ai/user/deadblue22)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to read, write, append, insert, and incrementally synchronize Feishu document content while preserving table placement and formatting constraints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may lead an agent to read Feishu app credentials and create tenant tokens for direct authenticated API calls.

Mitigation: Keep authentication inside the approved Feishu document tool where possible and avoid exposing app secrets to general agent context.

Risk: The skill includes replace, delete, and insert workflows that can mutate Feishu documents.

Mitigation: Require explicit user approval for destructive or broad document changes and compare current document content before writing.

Risk: The skill recommends running git pull before reading local repository files.

Mitigation: Require explicit approval before mutating the local workspace and review incoming repository changes before syncing them to Feishu.

## Reference(s):

- [Feishu tenant access token API endpoint](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal)
- [Feishu Docx block children API endpoint](https://open.feishu.cn/open-apis/docx/v1/documents/{doc_token}/blocks/{doc_token}/children?document_revision_id=-1)
- [ClawHub skill page](https://clawhub.ai/deadblue22/skills/feishu-doc-sync)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with JSON action examples, bash commands, and YAML configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes Feishu document action patterns, table update workflows, synchronization heuristics, and permission notes.]

## Skill Version(s):

1.0.0 (source: evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
