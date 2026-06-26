## Description: <br>
Build or customize an owner-only proactive companion system with a cyber-girlfriend persona, Markdown private-life context, lightweight relationship memory, and OpenClaw presence cron delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kasanuowa](https://clawhub.ai/user/kasanuowa) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to configure an owner-only proactive companion that maintains persona, daily schedule, and relationship-memory files, wires OpenClaw delivery cron jobs, and validates setup or upgrades. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent proactive messaging may send content on a schedule to the wrong route or at undesired times. <br>
Mitigation: Preview cron payloads and delivery channel, account, target, quiet hours, and pacing before enabling; keep a documented pause or removal path. <br>
Risk: The skill requires sensitive delivery credentials or OAuth-backed runtime access. <br>
Mitigation: Keep secrets in local configuration or environment variables, never in published defaults, and confirm the sender account before use. <br>
Risk: Setup can read local owner context such as USER.md, session history, config files, and companion state. <br>
Mitigation: Confirm the exact files to be read or written and import only stable identity fields needed for the owner-only companion. <br>
Risk: Configurable healthcheck, jobs-list, and state-commit commands can execute local shell commands. <br>
Mitigation: Review configured commands before installation and run validation in preview or dry-run mode where available. <br>
Risk: Daily schedule and presence writing may use public web search. <br>
Mitigation: Enable web search only after confirming that public-web lookup is acceptable for the companion's configured context. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/kasanuowa/cyber-girlfriend) <br>
- [Standard Init / Upgrade Flow](references/standard-init-upgrade-flow.md) <br>
- [Configuration](references/configuration.md) <br>
- [Turn Contract](references/contract-schema.md) <br>
- [First-Time Setup Guide](references/first-time-setup.md) <br>
- [Presence Integration](references/presence-integration.md) <br>
- [Private Life Layer](references/private-life-layer.md) <br>
- [Required Events And Cron](references/required-events-and-cron.md) <br>
- [Script Contract Migration](references/script-contract-v2-migration.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with JSON configuration examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local setup or upgrade guidance for OpenClaw-based proactive companion delivery.] <br>

## Skill Version(s): <br>
2.1.9 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
