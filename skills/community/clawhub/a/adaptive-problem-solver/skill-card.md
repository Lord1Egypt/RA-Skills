## Description:

Detects rigid security, permission, skill, or complexity limits and generates multiple adaptive, user-tailored alternative solutions for problem-solving.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zs15600770520](https://clawhub.ai/user/zs15600770520)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to turn blocked or overly rigid task responses into practical alternative plans, such as step-by-step guidance, safer local simulations, simplified scripts, or multiple implementation paths. It is intended for workflows where the user still reviews risks and chooses whether to proceed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is designed to respond to safety or permission refusals by suggesting workaround paths, including host commands or privilege-related options.

Mitigation: Review each generated workaround against the applicable safety, permission, and operational policy before execution; prefer lower-risk guidance, simulations, or user-approved manual steps.

Risk: The artifact stores triggering prompt excerpts, solution history, and user preferences in local plaintext files.

Mitigation: Avoid using it with secrets or sensitive operational details unless logging, retention, and access controls are changed.

## Reference(s):

- [Adaptive Problem Solver on ClawHub](https://clawhub.ai/zs15600770520/skills/adaptive-problem-solver)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with structured options, decision guidance, and inline code or shell commands when applicable]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include ranked alternatives, risk labels, estimated effort, implementation steps, learning reports, and local user preference records.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
