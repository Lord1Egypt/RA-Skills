## Description:

Autonomous agent health, optimization, and cleanup for OpenClaw agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[robshabbir](https://clawhub.ai/user/robshabbir)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to monitor OpenClaw agent sessions, clean up stale background work, check process and context health, and record periodic retrospectives.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically terminate agent sessions or background processes using broad stale-state criteria.

Mitigation: Use it in tightly scoped environments, prefer dry-run behavior, and require explicit confirmation before terminating sessions or processes.

Risk: Cleanup behavior may remove background work or operational artifacts that are still useful.

Mitigation: Restrict cleanup to tagged resources and review targets before deletion or termination.

Risk: The skill can write retrospective notes to persistent memory.

Mitigation: Disable persistent memory writes unless the operator explicitly opts in.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/robshabbir/skills/agent-self-care)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown status report with shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or perform cleanup actions for stale agent sessions, background processes, cron artifacts, logs, and persistent memory notes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
