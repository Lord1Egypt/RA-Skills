## Description:

Chat Logger records direct Feishu and DingTalk messages into daily Markdown logs and returns summary reports for exact chat-log trigger phrases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bjmfjoy](https://clawhub.ai/user/bjmfjoy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators integrating OpenClaw with Feishu or DingTalk use this skill to keep per-user direct-message logs and generate daily or all-time chat summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores private direct messages in persistent logs.

Mitigation: Deploy only in controlled workspaces where users are informed that direct messages are logged and retention expectations are clear.

Risk: Global chat-log summaries can expose multiple users' messages without clear authorization controls.

Mitigation: Restrict summary commands to authorized administrators or add access checks before enabling the skill.

Risk: Path handling may allow writes outside the intended log directory.

Mitigation: Fix and review path normalization before deployment, then verify logs remain under the intended chat-log directory.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/bjmfjoy/skills/chat-logger)
- [ClawHub Publisher Profile](https://clawhub.ai/user/bjmfjoy)

## Skill Output:

**Output Type(s):** [text, markdown, files, guidance]

**Output Format:** [Markdown log files and plain-text or Markdown summary strings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores direct-message logs under a per-channel, per-user, per-day structure.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
