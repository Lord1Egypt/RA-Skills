## Description:

Use when you have a written implementation plan to execute in a separate session with review checkpoints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lovemymobilewebsite-dotcom](https://clawhub.ai/user/lovemymobilewebsite-dotcom)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to execute an existing written implementation plan with critical review, task-by-task progress tracking, and verification checkpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A written plan can direct the agent to run unsafe commands or make broad destructive changes.

Mitigation: Review the plan before using the skill and avoid running it with untrusted plans.

Risk: Implementation can stall or drift when a plan has unclear steps, missing dependencies, or repeated verification failures.

Mitigation: Follow the skill's stop-and-ask guidance when blockers, unclear instructions, or repeated verification failures occur.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lovemymobilewebsite-dotcom/skills/executing-plans-2)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, code]

**Output Format:** [Markdown guidance with task updates, verification results, and implementation changes as needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce code edits or shell commands while executing the supplied plan; stops and asks for help when blockers or repeated verification failures occur.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
