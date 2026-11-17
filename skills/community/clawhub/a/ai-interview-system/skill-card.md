## Description:

Ai Interview provides a two-agent AI interview workflow with a Feishu group chat interview and a local web viewer for observing the conversation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeeban-g](https://clawhub.ai/user/jeeban-g)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to configure a simulated AI interview between a job-seeker agent and a recruiter agent, with Feishu group chat as the interaction channel and a local viewer for monitoring the exchange.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local web viewer can expose OpenClaw conversation logs.

Mitigation: Keep the viewer bound to localhost, do not expose port 8091 to a network, and restrict access to the intended agents.

Risk: The viewer includes an endpoint that can delete local conversation logs.

Mitigation: Remove or protect the clear endpoint before use in shared or sensitive environments.

Risk: Feishu app secrets are required for setup.

Mitigation: Store app secrets outside version control and maintain a rotation plan.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jeeban-g/skills/ai-interview-system)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes OpenClaw agent identity templates, Feishu configuration guidance, installation commands, and local viewer usage guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
