## Description:

Create and configure OpenClaw agents, including workspace files, openclaw.json entries, Telegram routing, cron prompts, and gateway restart guidance for Arch's multi-agent system.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arch1904](https://clawhub.ai/user/arch1904)

### License/Terms of Use:


## Use Case:

Developers and operators maintaining Arch's OpenClaw setup use this skill to scaffold new agents, update agent configuration, set up Telegram routing, and prepare scheduled jobs with safer prompt patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide edits to ~/.openclaw configuration, gateway restarts, cron jobs, and Telegram messaging.

Mitigation: Use only in an intended OpenClaw environment and require explicit review of every file change and cron payload before execution.

Risk: Under-scoped shell-evaluated cron prompts can run unintended shell syntax or arbitrary commands.

Mitigation: Reject untrusted agent IDs or prompt text containing shell syntax, and avoid scheduled prompts that run arbitrary commands.

Risk: Persistent scheduled agents and Telegram routing changes can continue operating after setup.

Mitigation: Confirm schedules, recipients, and routing bindings before enabling cron jobs or restarting the gateway.

## Reference(s):

- [OpenClaw Agent Creator ClawHub Listing](https://clawhub.ai/arch1904/skills/claw-agent-creator-archit)
- [OpenClaw Agent Config Schema](references/config-schema.md)
- [Telegram Routing](references/telegram-routing.md)
- [Cron Job Prompt Patterns](references/prompt-patterns.md)
- [Bugs and Pitfalls](references/bugs-and-pitfalls.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON snippets and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose persistent OpenClaw config, cron job, and Telegram routing changes that require human review before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
