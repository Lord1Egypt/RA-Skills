## Description:

Helps agents diagnose successful prompt-driven cron or agentTurn jobs that produce zero results by separating upstream sampling failures from downstream classification issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[can4hou6joeng4](https://clawhub.ai/user/can4hou6joeng4)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to investigate Discord, Obsidian, OpenClaw, cron, and agentTurn reports that ran successfully but produced empty daily review or sampling results. It guides the agent to distinguish declared prompt criteria from fixed retrieval behavior, identify missing source evidence, and propose minimal repairs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is tied to a real Discord, Obsidian, and OpenClaw environment, including concrete local paths and IDs.

Mitigation: Sanitize paths, job IDs, user IDs, guild IDs, channel names, and dates before reuse; replace them with placeholders or environment-specific configuration.

Risk: Broad local searches can expose unrelated private workspace or source content.

Mitigation: Search the exact job, run, and output files first; ask for approval before expanding to broad directories, and summarize only evidence relevant to the reported zero-output task.

Risk: A successful cron status can be mistaken for proof that sampling coverage was correct.

Mitigation: Separate run success from retrieval correctness, and require scan counts, scanned channel or thread IDs, matched message IDs, and time-window audit data before treating an empty result as reliable.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/can4hou6joeng4/skills/debug-prompt-driven-cron-agent-zero-output)
- [Discord daily sampling contract](references/discord-daily-sampling-contract.md)
- [Prompt agentTurn cron evidence boundaries](references/prompt-agentturn-cron-evidence-boundaries.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration, code]

**Output Format:** [Markdown diagnostic guidance with checklists and small JSON or JavaScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces investigative recommendations and verification steps; it does not directly retrieve Discord data or modify cron jobs.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
