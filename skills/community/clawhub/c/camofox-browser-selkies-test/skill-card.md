## Description:

Use the Selkies test browser stack for desktop-stream/browser-in-desktop checks, Selkies-specific debugging, and viewport/mobile-context experiments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lotfinity](https://clawhub.ai/user/lotfinity)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when testing or debugging the local Selkies browser stack, including desktop-stream behavior, browser-in-desktop validation, websocket issues, and viewport or mobile-context experiments tied to the Selkies test image/container.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Confusing this Selkies test stack with the main camofox-browser service could send validation or debugging steps to the wrong browser target.

Mitigation: Confirm the task is for Selkies or the local services on 127.0.0.1:9378 and 127.0.0.1:3003 before applying the skill.

Risk: Suggested Docker image or container actions may affect the local Selkies test stack.

Mitigation: Confirm the expected container name and image reference before running any shell command proposed from this skill.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown text with optional inline commands and local service URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
