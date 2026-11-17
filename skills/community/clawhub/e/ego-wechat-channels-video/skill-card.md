## Description:

Prepare and save a WeChat Channels video draft through Ego Lite after checking login status; publishing remains a human step.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terryso](https://clawhub.ai/user/terryso)

### License/Terms of Use:

MIT-0

## Use Case:

External users can prepare a WeChat Channels video draft by supplying a local video and post details. The skill checks login status, guides the agent through upload and draft creation, and leaves QR login and final publishing to the human.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local upload helper may expose unpublished videos to unrelated web pages.

Mitigation: Use a version that restricts access to the intended origin, requires an unpredictable token, and shuts down automatically. Until then, avoid confidential videos and stop the helper immediately after transfer.

Risk: The optional originality step accepts an agreement without a separate approval check.

Mitigation: Leave originality disabled unless a person has reviewed and authorized the agreement.

## Reference(s):

- [Login guidance](references/login.md)
- [Input fields](references/inputs.md)
- [Project homepage](https://github.com/terryso/ego-skills/tree/main/skills/wechat-channels-video)
- [WeChat Channels](https://channels.weixin.qq.com)

## Skill Output:

**Output Type(s):** [Video draft, Text, Shell commands, Guidance]

**Output Format:** [WeChat Channels draft with JSON status and user guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Saves a draft; final publishing is left to the human.]

## Skill Version(s):

0.2.1 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
