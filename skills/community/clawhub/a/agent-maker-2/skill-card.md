## Description:

Create autonomous AI agents for OpenClaw with guided discovery that clarifies purpose, personality, skills, channels, automation, and security before generating a configured agent workspace.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anhnt224](https://clawhub.ai/user/anhnt224)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to design and create autonomous agents through a guided requirements flow, then generate the agent workspace, configuration guidance, and setup commands needed to activate the agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated agents may be persistent and active with broad access.

Mitigation: Review each generated agent before activation, set explicit tool allowlists, choose sandbox all for untrusted inputs, and avoid tier3 unless standing automation is required.

Risk: The creation script can overwrite files at a user-supplied workspace path.

Mitigation: Use a dedicated workspace under an expected OpenClaw directory and avoid existing or symlinked directories.

Risk: Channel tokens or other secrets may be needed for messaging integrations.

Mitigation: Handle tokens through a proper secret store rather than chat or generated files.

## Reference(s):

- [OpenClaw](https://openclaw.ai)
- [Agent Maker on ClawHub](https://clawhub.ai/anhnt224/skills/agent-maker-2)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with bash, JSON, and TypeScript command examples; generated workspace files are Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create OpenClaw agent workspace files, memory directories, skill directories, gateway configuration, heartbeat settings, and optional channel or cron setup instructions.]

## Skill Version(s):

1.0.0 (source: server release metadata, artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
