## Description:

Automatically improve agent guidance through iterative testing and scoring. Use when you want to optimize prompts, AGENTS.md entries, or skill definitions using a Karpathy-style training loop with OpenClaw cron.

This skill is ready for commercial/non-commercial use.

## Publisher:

[peterpcw](https://clawhub.ai/user/peterpcw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use Autoagent to iteratively improve prompts, AGENTS.md entries, and skill definitions by testing changes against user-approved scoring criteria in a sandbox.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring cron-based optimization can continue running and making sandbox changes after the initial setup.

Mitigation: Inspect the scheduled cron entry before enabling it, choose a bounded interval, and confirm how to stop and remove the job.

Risk: The skill writes guidance, fixtures, and score logs into a user-selected sandbox path.

Mitigation: Use a new dedicated sandbox with non-sensitive content and avoid broad absolute paths.

Risk: Iterations forward full guidance and test data to subagents for scoring.

Mitigation: Keep secrets and private data out of fixtures and guidance before starting the optimization loop.

## Reference(s):

- [OpenClaw Integration](references/openclaw-integration.md)
- [ClawHub Skill Page](https://clawhub.ai/peterpcw/skills/autoagent)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions with sandbox files, score logs, fixtures, and OpenClaw cron setup.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates recurring optimization iterations when the user approves setup.]

## Skill Version(s):

0.8.9 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
