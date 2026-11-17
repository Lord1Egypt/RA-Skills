## Description:

Creates a draft task file in .specs/tasks/draft/ that preserves the original user intent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hahamumu08](https://clawhub.ai/user/hahamumu08)

### License/Terms of Use:

MIT-0

## Use Case:

Developers maintaining an SDD task workflow use this skill to convert a short user request into a uniquely named draft task Markdown file with a title, issue type, optional dependencies, and the original prompt preserved.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes persistent workflow files from user-supplied prompts, titles, and dependency names.

Mitigation: Review generated task files before downstream processing and treat stored prompt, title, and dependency content as untrusted input.

Risk: The skill evidence notes inconsistent placement rules between draft and todo task paths.

Mitigation: Confirm the intended task directory before use and prefer .specs/tasks/draft/ to match the stated goal and constraints.

Risk: The skill calls a folder-creation script that is not bundled in the artifact.

Mitigation: Verify the expected script exists in the installed environment or create the required .specs task directories manually before running the skill.

## Reference(s):

- [Add Task on ClawHub](https://clawhub.ai/hahamumu08/skills/add-task)

## Skill Output:

**Output Type(s):** [Markdown, Text, Shell commands, Guidance]

**Output Format:** [Markdown task file plus concise status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates a new task file under .specs/tasks/draft/ and should avoid modifying existing task files.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
