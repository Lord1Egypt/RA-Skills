## Description:

Helps agents use Feishu Open Platform APIs to find chats and members, send text messages, and upload images or files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jypjypjypjyp](https://clawhub.ai/user/jypjypjypjyp)

### License/Terms of Use:


## Use Case:

Employees, operators, and developers use this skill to send Feishu messages and resolve Feishu chat or member identifiers when coordinating work in a Feishu tenant.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Verbose DEBUG and full-response logging may expose sensitive Feishu API responses or organizational metadata.

Mitigation: Use lower log levels in tenant environments, redact API responses before logging, and avoid copying the example full-response logging pattern.

Risk: The skill handles Feishu chat/member lookup results and file uploads that may contain sensitive organizational data.

Mitigation: Limit Feishu app permissions to the minimum required scopes, confirm recipients and file paths before sending, and treat uploaded files and lookup results as sensitive.

## Reference(s):

- [Feishu API Documentation](https://open.feishu.cn/document/server-docs/api-call-guide/server-api-list)
- [ClawHub Skill Page](https://clawhub.ai/jypjypjypjyp/skills/feishu-messaging)
- [ClawHub Publisher Profile](https://clawhub.ai/user/jypjypjypjyp)

## Skill Output:

**Output Type(s):** [Guidance, Code, Configuration]

**Output Format:** [Markdown with Python code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Feishu app credentials, target recipient or chat identifiers, and appropriate Feishu API permissions.]

## Skill Version(s):

0.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
