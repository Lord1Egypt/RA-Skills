## Description: <br>
Creates and configures OpenClaw agents by guiding workspace setup, OpenClaw configuration, Telegram routing, cron job prompts, and gateway verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arch1904](https://clawhub.ai/user/arch1904) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw administrators use this skill to create or modify local OpenClaw agents, including workspace files, OpenClaw JSON configuration, Telegram group routing, cron jobs, and gateway restart checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide changes to local OpenClaw configuration and scheduled jobs. <br>
Mitigation: Review every configuration edit, cron schedule, shell substitution, and report command before restarting the gateway. <br>
Risk: Cron prompts and report commands may send unintended or sensitive output to Telegram destinations. <br>
Mitigation: Verify Telegram targets, avoid untrusted cron prompt input, and avoid report commands that expose secrets unless that output is explicitly intended. <br>
Risk: Editing OpenClaw files while the gateway is running can lose or corrupt job state. <br>
Mitigation: Stop the OpenClaw gateway before edits, keep backups, and restart only after reviewing the final configuration. <br>


## Reference(s): <br>
- [OpenClaw Agent Creator](https://clawhub.ai/arch1904/claw-agent-creator-archit) <br>
- [OpenClaw Agent Config Schema](references/config-schema.md) <br>
- [Telegram Routing - The 3-Layer System](references/telegram-routing.md) <br>
- [Cron Job Prompt Patterns](references/prompt-patterns.md) <br>
- [Bugs and Pitfalls](references/bugs-and-pitfalls.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with JSON examples and inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces human-reviewed setup steps for local OpenClaw files, Telegram routing, cron prompts, and gateway checks.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
