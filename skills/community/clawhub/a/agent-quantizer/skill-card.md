## Description:

Agent Quantizer provides OpenClaw maintenance helpers for token usage reporting, context compression, prompt trimming, response caching, idle session cleanup, heartbeat checks, cron auditing, model routing guidance, and skill organization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tryxin](https://clawhub.ai/user/tryxin)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw developers and operators use this skill to inspect and reduce token consumption, manage cached tool results, compact long sessions, audit recurring tasks, and organize local skills in an OpenClaw environment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary reports that broad caching can expose sensitive data.

Mitigation: Use only in a backed-up, non-sensitive OpenClaw environment and avoid caching secrets, private prompts, or sensitive tool outputs.

Risk: The security summary reports direct state rewriting that can corrupt sessions.

Mitigation: Review changes before running destructive or rewrite actions, keep backups, and prefer dry-run or inspection commands before cleanup or compression.

Risk: The security guidance warns that crafted queries, prompt files, or command arguments may execute code until interpolation bugs are fixed.

Mitigation: Do not pass untrusted inputs, prompt files, or command arguments to the skill; inspect script arguments and file paths before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tryxin/skills/agent-quantizer)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, local file edits, JSON configuration, and terminal status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read and rewrite local OpenClaw state, cache data, prompt files, and skill directories when invoked.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter states 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
