## Description:

Enable and configure Agent Synthesizer for OpenClaw to improve autonomy and execution throughput.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rylena](https://clawhub.ai/user/rylena)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use this skill to install, configure, troubleshoot, or optimize Agent Synthesizer by following the referenced project README.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill delegates installation and command execution to a mutable external GitHub README without explicit safety boundaries.

Mitigation: Treat the README as reference material only, show exact commands before execution, and reject instructions that request secrets, persistence, privilege escalation, unrelated file access, or destructive changes.

Risk: Setup behavior can change when the external README changes.

Mitigation: Pin or vendor reviewed setup steps for release use and repeat review when the upstream setup instructions change.

## Reference(s):

- [Agent Synthesizer on ClawHub](https://clawhub.ai/rylena/skills/agent-synthesizer)
- [Agent Synthesizer repository](https://github.com/rylena/agent-synth)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and setup status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes the current setup step, expected success signal, and next step.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
