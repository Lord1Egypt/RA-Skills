## Description:

Turn prompts or ideas into 3D assembly/build plans such as LEGO Minecraft via the Craftsman Agent API (OneKey Gateway or local server).

This skill is ready for commercial/non-commercial use.

## Publisher:

[ai-hub-admin](https://clawhub.ai/user/ai-hub-admin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to call hosted Craftsman Agent endpoints that generate LEGO or Minecraft build plans from prompts and optional reference image URLs. It helps produce inventories, multi-angle assembly images, and step-by-step build guidance for client applications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary reports risky handling of shared credentials and user API keys.

Mitigation: Set DEEPNLP_ONEKEY_ROUTER_ACCESS intentionally, avoid sensitive prompts or reference URLs, and avoid relying on the built-in demo key.

Risk: The security guidance flags unpinned and broader-than-needed package installs.

Mitigation: Review dependencies before installation and prefer running the skill in an isolated environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ai-hub-admin/skills/craftsman-agent)
- [Publisher profile](https://clawhub.ai/user/ai-hub-admin)
- [Craftsman Agent OneKey Gateway endpoint](https://agent.deepnlp.org/agent)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON API responses and script command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Endpoint responses may include image URLs, part inventories, inventory image details, and ordered assembly step images.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
