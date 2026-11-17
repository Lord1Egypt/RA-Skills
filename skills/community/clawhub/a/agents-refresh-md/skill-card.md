## Description:

Helps agents periodically reload markdown context files, distill recent memory logs into MEMORY.md, and maintain HEARTBEAT.md or cron refresh tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kentaroid-bot](https://clawhub.ai/user/kentaroid-bot)

### License/Terms of Use:


## Use Case:

Developers and external ClawHub users use this skill to maintain long-running agent context by scheduling markdown-only refreshes and summarizing recent memory logs into project memory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring refresh jobs may repeatedly read identity, user, and memory files and summarize them into persistent MEMORY.md.

Mitigation: Enable the skill only in workspaces where persistent memory maintenance is intended, and review the scheduled jobs and HEARTBEAT.md entries before allowing them to run.

Risk: Scheduled refresh tasks may remain active without clear stop or rollback controls.

Mitigation: Record created cron job names or IDs, keep HEARTBEAT.md changes reviewable, and remove or disable the jobs when ongoing refreshes are no longer needed.

Risk: Memory distillation may introduce incorrect or unwanted summaries into MEMORY.md.

Mitigation: Review MEMORY.md updates before relying on them, and preserve source logs so incorrect summaries can be corrected.

## Reference(s):

- [Agents Refresh MD ClawHub Skill Page](https://clawhub.ai/kentaroid-bot/skills/agents-refresh-md)
- [examples.md](references/examples.md)
- [OpenClaw Skills Documentation](https://docs.openclaw.ai/skills)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with inline cron JSON and shell-style tool commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update MEMORY.md and HEARTBEAT.md when run by an agent with appropriate workspace permissions.]

## Skill Version(s):

1.1.2 (source: server release metadata and manifest.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
