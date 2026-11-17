## Description:

Automatically prompts OpenClaw agents to send personalized daily greetings to their bound channels using startup or scheduled triggers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shz2050](https://clawhub.ai/user/shz2050)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users use this skill to have bound agents send scheduled, persona-aware greetings with relevant status updates to channels such as Discord, Feishu, or Telegram.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic channel messaging can expose inferred context or status details in sensitive channels.

Mitigation: Limit the skill to approved agents and channels, and remove sensitive context or status details from the configured trigger message.

Risk: BOOT.md and cron triggers can cause greetings to run without an explicit daily user action.

Mitigation: Disable BOOT.md and cron until scheduled greetings are explicitly needed, then review the trigger schedule before enabling.

Risk: The uninstall command removes the configured skill directory and can be unsafe if SKILL_DIR is overridden.

Mitigation: Do not run uninstall with an overridden SKILL_DIR, and inspect the resolved path before removal.

## Reference(s):

- [Daily Greeting ClawHub release page](https://clawhub.ai/shz2050/skills/daily-greeting)
- [README](artifact/README.md)
- [Installation Guide](artifact/guide.md)
- [Chinese README](artifact/docs/README_zh.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions, bash command output, JSON configuration, and runtime channel messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runtime behavior depends on OpenClaw bindings, weekday scheduling, duplicate-run state, and the configured trigger message.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
