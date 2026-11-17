## Description:

Creates and registers an OpenClaw agent by collecting setup details, generating workspace files, configuring optional channel bindings, and preparing review-mode self-improvement workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dao24dao](https://clawhub.ai/user/dao24dao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to create a new agent workspace, register the agent through the OpenClaw CLI, optionally bind messaging channels, and set up review-mode learning and evolution support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install mutable remote skills through npx-based commands.

Mitigation: Pin and verify remote skill installs before use, and review installed content before enabling the created agent.

Risk: Messaging channel setup can involve bot tokens, app secrets, access tokens, service-account files, or QR pairing.

Mitigation: Use least-privilege credentials, store secrets securely, and avoid pasting long-lived credentials into chat.

Risk: Generated agents keep long-term memory, learning logs, and review-mode evolution artifacts.

Mitigation: Review the generated workspace before operation, keep evolution in review mode, and avoid storing sensitive personal or business data in memory files.

Risk: The workspace generator can overwrite an existing workspace if the user confirms the prompt.

Mitigation: Inspect the target workspace path and keep a backup before approving overwrite behavior.

## Reference(s):

- [Workspace templates](artifact/references/workspace-templates.md)
- [Channel parameters](artifact/references/channel-params.md)
- [OpenClaw agents CLI documentation](https://docs.openclaw.ai/cli/agents)
- [OpenClaw channels documentation](https://docs.openclaw.ai/channels)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated workspace files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces OpenClaw workspace files, registration and channel-binding commands, and a post-creation checklist.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
