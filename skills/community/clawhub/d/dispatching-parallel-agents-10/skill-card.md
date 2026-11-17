## Description:

Use when facing 2+ independent tasks that can be worked on without shared state or sequential dependencies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivansslo](https://clawhub.ai/user/ivansslo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to split independent failures, subsystems, or tasks into focused parallel subagent investigations and then review and integrate the returned results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Parallel subagents may receive prompts that expose sensitive files or broad code context.

Mitigation: Review generated subagent prompts and limit each prompt to the files and context needed for its independent task.

Risk: Independent agent changes may conflict or introduce inconsistent fixes when integrated.

Mitigation: Review each returned summary, check for overlapping edits, and run the full test suite before accepting combined changes.

## Reference(s):

- [Server-resolved GitHub source](https://github.com/ivansslo/Supwrs/tree/main/skills/dispatching-parallel-agents)
- [ClawHub skill page](https://clawhub.ai/ivansslo/skills/dispatching-parallel-agents-10)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands]

**Output Format:** [Markdown guidance with example subagent prompts and command-oriented instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces coordination guidance; does not execute code by itself.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
