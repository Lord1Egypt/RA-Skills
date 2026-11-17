## Description:

Orchestrates cross-platform IM workflows across Feishu, DingTalk, and WeCom with their official CLIs for unified inbox triage, task sync, notification broadcast, platform-aware routing, and emergency communication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lm203688](https://clawhub.ai/user/lm203688)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to plan and execute coordinated enterprise messaging workflows across Feishu, DingTalk, and WeCom, including triage, task synchronization, broadcasts, routing, and incident communications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide installation and authentication of enterprise messaging CLIs.

Mitigation: Install in a controlled environment, verify and pin CLI packages before authentication, and use least-privileged platform accounts.

Risk: Workflow examples include DING, all-user, and multi-platform broadcasts that could notify too many recipients or send unintended content.

Mitigation: Require an explicit preview and user confirmation before DING, all-user, or multi-platform broadcast actions.

Risk: Repeated cross-platform notifications can create duplicate messages or exceed practical messaging limits.

Mitigation: Apply the artifact's safety rules: limit sending to 10 messages per minute per platform, 30 total messages per minute, and avoid duplicate notifications unless urgency requires them.

## Reference(s):

- [Cross-Platform IM CLI on ClawHub](https://clawhub.ai/lm203688/skills/cross-platform-im-cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include platform-specific routing guidance, prerequisite checks, and preview or confirmation steps before messaging actions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
