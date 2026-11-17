## Description:

Provides guidance for using NVIDIA OpenShell sandboxes to run code, security scans, debugging sessions, and tests in isolated execution environments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sabatech-dev](https://clawhub.ai/user/sabatech-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security engineers, debugging agents, and QA agents use this skill to route code execution, security scans, bug reproduction, and test runs through named OpenShell sandboxes with resource and network restrictions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sandbox administration commands can affect named environments, including deletion or policy changes.

Mitigation: Confirm sandbox names before destructive operations and only loosen network policies when necessary for the task.

Risk: Files copied out of isolated sandboxes may contain untrusted or task-generated content.

Mitigation: Review copied files before using them on the host or in downstream workflows.

Risk: Users may misapply the guide without OpenShell operational familiarity.

Mitigation: Install only when users are comfortable with OpenShell sandbox administration and can validate sandbox status before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sabatech-dev/skills/alfred-openshell-sandbox)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes sandbox names, command examples, file transfer patterns, policy notes, resource limits, troubleshooting guidance, and architecture notes.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
