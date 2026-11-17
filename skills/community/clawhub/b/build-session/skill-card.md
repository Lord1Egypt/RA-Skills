## Description:

Facilitates focused autonomous sessions to build, create, or produce one concrete deliverable, then log and commit progress efficiently.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stevenartzt](https://clawhub.ai/user/stevenartzt)

### License/Terms of Use:


## Use Case:

Developers and autonomous-agent operators use this skill to structure scheduled or focused work sessions around one concrete deliverable, with lightweight logging and optional task-selection helpers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Autonomous commit and push guidance may publish unintended files or changes.

Mitigation: Require explicit approval before commits or pushes, review git status and staged diffs, and stage only intended files.

Risk: Running the skill in a worktree with unrelated changes or secrets can expose or mix unintended content into session output.

Mitigation: Use a clean worktree for build sessions and avoid repositories or workspaces that may contain secrets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/stevenartzt/skills/build-session)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes optional shell helpers for task selection and session logging.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
