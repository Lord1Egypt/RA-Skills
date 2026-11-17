## Description:

Task tracking for async/multi-step work. Use dex to create, track, and complete tasks that span multiple sessions or require coordination (e.g., coding agent dispatches, PR reviews, background jobs). Tasks stored as JSON files in .dex/tasks/.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gricha](https://clawhub.ai/user/gricha)

### License/Terms of Use:


## Use Case:

Developers and coding agents use this skill to create, inspect, update, complete, and delete local task records for asynchronous or multi-step work that needs follow-up across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task descriptions and context may include sensitive project details in local .dex/tasks JSON files.

Mitigation: Avoid storing secrets in task text, and review or delete .dex/tasks files when task records contain confidential details.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, shell commands, text, configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local JSON task files under .dex/tasks/ when the documented dex commands are used.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
