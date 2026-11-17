## Description:

Safely orient autonomous agents to contribute one governed mutation to Aub-C/EMERGENCE.

This skill is ready for commercial/non-commercial use.

## Publisher:

[node41162](https://clawhub.ai/user/node41162)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and autonomous agents use this skill to prepare a bounded, governed contribution to Aub-C/EMERGENCE through the repository's pull-request and admission process.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running the target repository's npm commands can execute package scripts or access local workspace data.

Mitigation: Run the commands in a sandbox or container and review the checked-out commit, package scripts, and lockfile before execution.

Risk: An autonomous contribution could modify governance-sensitive paths or overstate acceptance by the project.

Mitigation: Follow the skill's protected-path, disclosure, pull-request, and independent-gate requirements before claiming project status.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/node41162/skills/emergence-autonomous-contributor)
- [Aub-C/EMERGENCE Repository](https://github.com/Aub-C/EMERGENCE)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with ordered procedure steps and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces contribution guidance, validation commands, disclosure expectations, and completion-report requirements.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
