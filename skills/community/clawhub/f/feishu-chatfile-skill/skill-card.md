## Description:

Helps an agent send local images and files to Feishu or Lark private chats and group chats using upload-then-send message workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shouldnotappearcalm](https://clawhub.ai/user/shouldnotappearcalm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to deliver generated images, reports, archives, and other local files into Feishu or Lark conversations when a chat recipient ID and app credentials are available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can upload selected local files or generated images to Feishu or Lark.

Mitigation: Require explicit approval before each send and restrict the file paths that the agent may upload.

Risk: The documented command examples pass app_secret as a command-line argument.

Mitigation: Prefer a secret store or environment-based handoff that avoids exposing the secret in process listings or shell history.

Risk: The Feishu or Lark app credentials may allow message delivery beyond the intended conversation if over-permissioned.

Mitigation: Use least-privilege app permissions and verify the recipient ID before sending.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shouldnotappearcalm/skills/feishu-chatfile-skill)
- [Feishu tenant token API](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal)
- [Feishu file upload API](https://open.feishu.cn/open-apis/im/v1/files)
- [Feishu message API](https://open.feishu.cn/open-apis/im/v1/messages)
- [Lark Open Platform](https://open.larksuite.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash and Python command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May result in selected local files or images being uploaded to Feishu or Lark through the configured app.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
