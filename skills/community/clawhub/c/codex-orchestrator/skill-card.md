## Description:

Monitor, control, and orchestrate background Codex sessions. Use this skill to track progress, handle interruptions, and ensure task completion for long-running coding tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[microcarft](https://clawhub.ai/user/microcarft)

### License/Terms of Use:


## Use Case:

Developers and engineering teams use this skill to supervise long-running Codex coding sessions, monitor progress, respond to interactive prompts, recover stalled work, and summarize completed changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: High-impact autonomous execution and prompt approval can affect repositories without enough safeguards.

Mitigation: Use only for trusted, explicit long-running coding tasks in repositories where full-auto Codex changes are acceptable or sandboxed.

Risk: Untrusted prompt text passed into the shown shell command can influence autonomous coding behavior.

Mitigation: Do not pass untrusted prompt text into the command; review task text before launching a background Codex session.

Risk: Blindly answering interactive prompts can approve unwanted actions.

Mitigation: Inspect each interactive prompt before submitting input and avoid blind approvals.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/microcarft/skills/codex-orchestrator)
- [Artifact skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, markdown]

**Output Format:** [Markdown with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces operational procedures for launching, monitoring, intervening in, resuming, and reporting on Codex background sessions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
