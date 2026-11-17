## Description:

Configure, repair, and validate OpenClaw scheduled outbound delivery to Feishu.

This skill is ready for commercial/non-commercial use.

## Publisher:

[timyao61-max](https://clawhub.ai/user/timyao61-max)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to create, repair, and validate OpenClaw cron jobs that need to send proactive, user-visible Feishu messages for reminders, recurring reports, and morning summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The smoke-test helper can generate unsafe shell commands from crafted input.

Mitigation: Review the helper script before use, use trusted values, avoid copying output produced from untrusted input into a shell, and prefer fixed or safely quoted command values for Feishu cron setup.

Risk: Examples contain placeholder recipient, account, schedule, and Chinese message text values that may not match a target workspace.

Mitigation: Replace the example text, recipient placeholders, account IDs, and schedule details with values appropriate to the workspace before running generated commands.

## Reference(s):

- [Validated Feishu cron delivery pattern](references/validated-pattern.md)
- [Feishu Cron Delivery on ClawHub](https://clawhub.ai/timyao61-max/skills/feishu-cron-delivery)
- [timyao61-max publisher profile](https://clawhub.ai/user/timyao61-max)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes Feishu routing patterns, repair checks, validation steps, and an optional smoke-test command generator.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
