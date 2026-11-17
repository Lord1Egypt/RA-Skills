## Description:

Feishu Integration helps agents work with the Feishu Open Platform for document, wiki, file, Markdown import, message parsing, OCR, group welcome, token management, and Feishu API workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moxunjinmu](https://clawhub.ai/user/moxunjinmu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to automate Feishu document, wiki, file, import, messaging, OCR, and group welcome workflows through documented commands and API wrappers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release ships a plaintext Feishu app secret and bearer-token handling needs review before use.

Mitigation: Rotate the exposed secret, replace config/feishu.env with a template, restrict Feishu app scopes, and store cached tokens in private 0600 files or a secret store.

Risk: The skill can perform authenticated Feishu API calls and run cron-based welcome automation with tenant privileges.

Mitigation: Validate request destinations, review scheduled automation, update vulnerable dependencies, and test with least-privilege tenant scopes before installation.

## Reference(s):

- [Feishu API Reference](references/api-reference.md)
- [Token Management](references/token-management.md)
- [Import Workflow](references/import-workflow.md)
- [Message Parsing](references/message-parsing.md)
- [Feishu Open Platform Documentation](https://open.feishu.cn/document/)
- [ClawHub Skill Page](https://clawhub.ai/moxunjinmu/skills/feishu-integration)
- [ClawHub Publisher Profile](https://clawhub.ai/user/moxunjinmu)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, API calls, guidance]

**Output Format:** [Markdown guidance with shell commands, code snippets, JSON/API examples, and configuration values.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use Feishu tenant credentials and call Feishu Open Platform APIs when configured; review security guidance before using real tenant privileges.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
