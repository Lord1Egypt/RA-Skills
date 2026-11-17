## Description:

Provides low-level Feishu cloud document block operations via REST API for batch cell updates, precise positioned inserts, block tree traversal, table manipulation, image replacement, and direct block-level control when built-in Feishu document actions are insufficient.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deadblue22](https://clawhub.ai/user/deadblue22)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to have an agent inspect and modify Feishu cloud document blocks directly when standard Feishu document actions do not cover the required table, image, traversal, insertion, or deletion operation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to use Feishu app credentials from local OpenClaw configuration and mint tenant access tokens.

Mitigation: Use scoped Feishu credentials or a limited pre-provided token where possible, and install only when the agent is permitted to access the targeted Feishu documents.

Risk: Direct block update and delete operations can alter or remove Feishu document content.

Mitigation: Review proposed write, replacement, and batch_delete requests before execution, especially index ranges and operations affecting many cells or blocks.

Risk: Batch document edits can exceed Feishu per-app or per-document rate limits.

Mitigation: Throttle write calls according to the documented 3 requests per second limits and avoid concurrent edits to the same document.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/deadblue22/skills/feishu-block-ops)
- [Feishu Tenant Access Token Endpoint](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal)
- [Feishu Docx Documents API Base](https://open.feishu.cn/open-apis/docx/v1/documents)
- [Feishu Batch Update Blocks Endpoint](https://open.feishu.cn/open-apis/docx/v1/documents/{doc}/blocks/batch_update)

## Skill Output:

**Output Type(s):** [text, markdown, code, API calls, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline Python snippets, REST API endpoints, request bodies, and operational cautions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include direct Feishu read, write, and delete API instructions, rate-limit timing, and block-operation gotchas.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
