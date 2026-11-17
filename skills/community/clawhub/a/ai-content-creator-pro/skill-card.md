## Description:

Multi-platform content creation buyout: pay 9.90 once, use forever. Generates 3-5 platform-adapted versions for Xiaohongshu, Douyin, Kuaishou, WeChat, and more. Unlimited access after one payment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jinyu12166](https://clawhub.ai/user/jinyu12166)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators and marketers use this agent skill to generate multiple Chinese social-platform content drafts and adapt them for Xiaohongshu, Douyin, Kuaishou, WeChat, Zhihu, Twitter, and similar channels. First-time use follows a local paid buyout workflow; later runs use the local buyout credential before the agent delivers text in conversation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The activation script is currently broken, which may prevent the paid workflow from completing.

Mitigation: Review and test service.py before installation or release, and require the publisher to fix the syntax error before relying on the skill.

Risk: The workflow writes order and buyout credential files under the user's OpenClaw home directory.

Mitigation: Install only when comfortable with local paid-access files, avoid sensitive input in the question argument, and store only minimally necessary credential data with restrictive permissions.

Risk: Payment receipt validation is weak according to the authoritative security scan.

Mitigation: Harden receipt validation before commercial reliance and independently review payment status handling.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jinyu12166/skills/ai-content-creator-pro)
- [Publisher profile](https://clawhub.ai/user/jinyu12166)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates at least three complete content plans from a user question after payment or local buyout verification.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
