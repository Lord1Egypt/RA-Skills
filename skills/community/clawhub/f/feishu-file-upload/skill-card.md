## Description:

Uploads local files to Feishu Drive and sends them as file messages to group chats, users, or email recipients using configured Feishu app credentials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucezhu888](https://clawhub.ai/user/brucezhu888)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to send local documents, archives, and other files through a Feishu bot to group chats or individual recipients. It is intended for file-sharing workflows where the agent has an explicit file path, recipient, and configured Feishu app credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send any accessible local file to an arbitrary Feishu recipient.

Mitigation: Require explicit confirmation of the file path and recipient, restrict who can invoke the skill, and avoid sensitive directories.

Risk: The skill uses stored Feishu app credentials to request a tenant access token from Feishu.

Mitigation: Use a dedicated least-privilege Feishu app with only the required permissions and rotate credentials if they are exposed.

Risk: The bundled documentation's credential-handling disclosure is inaccurate.

Mitigation: Correct the disclosure before release so users understand that app credentials are sent over HTTPS to Feishu's auth endpoint.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/brucezhu888/skills/feishu-file-upload)
- [Feishu tenant access token API endpoint](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal)
- [Feishu file upload API endpoint](https://open.feishu.cn/open-apis/im/v1/files)
- [Feishu message API endpoint](https://open.feishu.cn/open-apis/im/v1/messages)

## Skill Output:

**Output Type(s):** [Shell commands, Code, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash commands and command-line output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local file path, Feishu app credentials, Python 3, the requests library, and a Feishu recipient identifier or OPENCLAW_CHAT_ID.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact frontmatter is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
