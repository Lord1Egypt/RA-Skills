## Description:

Configures bindings for newly added OpenClaw agents, asks the user for the target Feishu group, prepares the binding change for review, restarts the gateway after confirmation, and installs the required skills into the new agent workspace.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ywewanhuang](https://clawhub.ai/user/ywewanhuang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to add Feishu group bindings for OpenClaw agents and bootstrap the expected companion skills in each new agent workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and modifies other skills and keeps a self-improving component running continuously.

Mitigation: Require explicit approval for each install and for persistent runtime, pin installed dependency versions or digests, and document how to stop or remove the always-running skill.

Risk: The skill changes OpenClaw bindings and restarts the gateway.

Mitigation: Review the complete binding configuration before applying it and restart the gateway only after explicit user confirmation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ywewanhuang/skills/config-new-agent)
- [Publisher profile](https://clawhub.ai/user/ywewanhuang)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces user-facing review prompts, binding configuration snippets, install commands, and a completion notification.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
