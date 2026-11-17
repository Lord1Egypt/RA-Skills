## Description:

Self-evolution system for OpenClaw agents that enables continuous learning through mistake tracking, experience distillation, skill improvement queues, and automated daily and weekly evolution cycles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhanghengyi1986-afk](https://clawhub.ai/user/zhanghengyi1986-afk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add persistent self-improvement loops to OpenClaw agents, including real-time lesson capture, daily consolidation, weekly review, and queued skill or code improvements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled evolution runs can modify code, skills, and memory without clear user approval.

Mitigation: Change cron prompts to review-only by default and require explicit approval before code or skill changes are applied.

Risk: Persistent memory files may retain secrets or sensitive personal data if agents record them during normal work.

Mitigation: Exclude secrets and sensitive personal data from memory files and restrict writable paths before enabling the workflow.

## Reference(s):

- [Agent Self-Evolve ClawHub page](https://clawhub.ai/zhanghengyi1986-afk/skills/agent-self-evolve)
- [Daily Evolution Cron Prompt](references/daily-evolution-prompt.md)
- [Weekly Deep Evolution Cron Prompt](references/weekly-evolution-prompt.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands, cron prompt templates, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates persistent memory files and may queue or apply code and skill changes during scheduled evolution cycles.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
