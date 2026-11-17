## Description:

ClawLite Office Hours guides agents through a YC Office Hours-style pre-coding consultation that reframes product problems, separates Startup and Builder modes, and produces a design document before implementation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[x-rayluan](https://clawhub.ai/user/x-rayluan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, founders, and builders use this skill when they want an agent to inspect project context, pressure-test product assumptions, compare implementation paths, and draft a design document before coding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may inspect repository context and create a design document in the project directory.

Mitigation: Ask the agent to confirm the intended filename or show the design in chat first when repository inspection or new files are not desired.

Risk: Pre-coding consultation can produce incorrect product assumptions or implementation recommendations if user evidence is incomplete.

Mitigation: Review the generated design, assumptions, options, and success criteria before approving implementation.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown consultation output with proposed implementation options and a design document]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create a project design document after consultation.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
