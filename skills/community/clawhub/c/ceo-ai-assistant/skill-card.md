## Description:

A Chinese-language OpenClaw skill that configures a CEO decision assistant with delegated agents, Feishu notifications, scheduled briefings, persistent memory, and P0-P3 decision tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[james6548](https://clawhub.ai/user/james6548)

### License/Terms of Use:

MIT-0

## Use Case:

Chinese-speaking CEOs and executive operators use this skill to organize decision support, delegate monitoring work to specialized agents, and receive scheduled Feishu briefings for market, project, and operational follow-up.

### Deployment Geography for Use:

Global; optimized for China-based CEO workflows and Asia/Shanghai schedules.

## Known Risks and Mitigations:

Risk: Scheduled Feishu sharing may expose sensitive executive briefings or decisions beyond the intended audience.

Mitigation: Use least-privilege Feishu credentials, restrict recipients with allowlists, and review notification routing before enabling scheduled delivery.

Risk: Persistent memory and automatic knowledge-base updates may retain sensitive executive conversations without sufficient review, retention, deletion, or redaction controls.

Mitigation: Disable automatic knowledge-base updates until retention, deletion, redaction, and human review controls are explicitly approved.

Risk: Session-history access can broaden exposure of prior conversations used for sensitive executive work.

Mitigation: Disable or narrow session-log access and review what historical data the skill can read before deployment.

Risk: Installer or dependency changes could alter the behavior of a skill that handles executive workflows.

Mitigation: Pin the installer and dependencies, then review and scan the exact release before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/james6548/skills/ceo-ai-assistant)
- [Publisher profile](https://clawhub.ai/user/james6548)
- [ClawHub homepage](https://clawhub.ai)
- [Feishu Open Platform](https://open.feishu.cn/app)
- [CEO decision collaboration framework](artifact/CEO决策协作体系v2.8.md)
- [Installation guide](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, JSON configuration templates, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes scheduled briefing prompts, Feishu announcement delivery, and persistent memory update behavior when installed and configured.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata reports 2.8.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
