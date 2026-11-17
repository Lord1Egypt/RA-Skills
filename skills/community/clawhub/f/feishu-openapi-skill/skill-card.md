## Description:

Operate Feishu or Lark IM APIs through UXC with a curated OpenAPI schema, tenant-token bearer auth, and chat/message guardrails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jolestar](https://clawhub.ai/user/jolestar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to discover and execute Feishu or Lark IM operations through UXC for chat lookup, member lookup, message history reads, user lookup, message sends and replies, file uploads, and bot-visible inbound message intake.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutable remote schema URLs can change the tenant-authenticated actions exposed after review.

Mitigation: Prefer the bundled schema in references/feishu-im.openapi.json or a commit-pinned schema URL before installation.

Risk: Message sends, replies, uploads, contact lookups, and long-running subscriptions can affect tenant data or send content externally.

Mitigation: Limit Feishu or Lark app scopes to intended chats, users, files, and message actions, keep secrets in environment-backed credentials, verify auth bindings, and require explicit confirmation before these operations.

Risk: File uploads depend on local path inputs and multipart/form-data behavior.

Mitigation: Review file paths and upload intent before executing image or file upload commands.

## Reference(s):

- [Usage patterns](references/usage-patterns.md)
- [Curated OpenAPI schema](references/feishu-im.openapi.json)
- [Feishu Open Platform docs](https://open.feishu.cn/document/)
- [Lark Open Platform docs](https://open.larksuite.com/document/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires tenant-scoped Feishu or Lark credentials and local file paths for multipart uploads.]

## Skill Version(s):

1.0.1 (source: server release evidence, created 2026-03-19T12:11:00Z)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
