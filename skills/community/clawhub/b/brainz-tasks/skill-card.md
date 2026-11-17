## Description:

Manage Todoist tasks using the `todoist` CLI. Add, list, and complete tasks from the command line.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xejrax](https://clawhub.ai/user/xejrax)

### License/Terms of Use:


## Use Case:

Developers and task-management users use this skill to list, create, and complete tasks from an agent workflow through the Todoist command line interface.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to expose task titles, due dates, identifiers, and completion actions to a task service.

Mitigation: Use only if that data exposure is acceptable, and prefer a narrowly scoped Todoist token.

Risk: The install metadata covers Todoist only, while the artifact also claims Microsoft To-Do and Microsoft Graph token support.

Mitigation: Avoid providing a broad Microsoft Graph token unless the publisher documents that integration and scope requirements.

Risk: The dependency installation example does not pin a reviewed package version.

Mitigation: Install the dependency in an isolated environment with a reviewed pinned version where possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xejrax/skills/brainz-tasks)
- [Publisher profile](https://clawhub.ai/user/xejrax)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes task-service credential setup guidance and command examples for listing, adding, and completing tasks.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
