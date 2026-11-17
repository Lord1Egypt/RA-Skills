## Description:

Guides OpenClaw agents in managing Facebook Fanpages through Graph API workflows for posting, comment replies, Messenger auto-replies, setup, and insights.

This skill is ready for commercial/non-commercial use.

## Publisher:

[trustydev212](https://clawhub.ai/user/trustydev212)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and social media operators use this skill to configure Facebook Page credentials and guide an agent through Fanpage posting, comment replies, Messenger responses, and Page insights workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Facebook Page token can grant broad authority over posts, comments, Messenger, and Page data.

Mitigation: Protect the token like a password, avoid committing OpenClaw configuration files, and rotate or revoke the token if it is exposed.

Risk: Agent actions may publish posts, delete or hide content, reply to comments, or send Messenger messages with weak guardrails.

Mitigation: Require human approval before any publishing, deletion, comment reply, or Messenger send action.

Risk: The connection script prints partial access-token material to the console.

Mitigation: Remove or edit the token-printing line before use in shared terminals, logs, or automated environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/trustydev212/skills/facebook-fanpage-manager)
- [Setup guide](artifact/references/setup-guide.md)
- [Facebook Graph API reference](artifact/references/api-reference.md)
- [OpenClaw Viet Nam community](https://zalo.me/g/lajsqc334jqc5fezevvo)
- [Meta Graph API Explorer](https://developers.facebook.com/tools/explorer/)
- [Meta Access Token Debugger](https://developers.facebook.com/tools/debug/accesstoken/)
- [Meta Graph API documentation](https://developers.facebook.com/docs/graph-api/)
- [Meta Messenger Platform documentation](https://developers.facebook.com/docs/messenger-platform/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration snippets and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FACEBOOK_PAGE_ID, FACEBOOK_ACCESS_TOKEN, and curl for connection checks and API examples.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
