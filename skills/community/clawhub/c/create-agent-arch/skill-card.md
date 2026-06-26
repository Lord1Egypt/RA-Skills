## Description: <br>
Guides an agent through creating and registering an OpenClaw Agent by collecting setup details, generating workspace files, running OpenClaw CLI commands, optionally binding channels, and producing a follow-up checklist. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dao24dao](https://clawhub.ai/user/dao24dao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to bootstrap a new OpenClaw agent workspace, register it with the OpenClaw CLI, optionally bind messaging channels, and install evolution-related skills that operate in review mode. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes persistent setup changes to a local OpenClaw installation and generated workspace. <br>
Mitigation: Review the workspace path and all OpenClaw, npx, and git commands before execution, and avoid overwriting existing workspaces unless intentionally approved. <br>
Risk: Channel binding can require bot tokens, app secrets, QR login, or other sensitive credentials. <br>
Mitigation: Use least-privilege bot credentials, avoid long-lived secrets in chat, and skip channel binding unless it is needed for the deployment. <br>
Risk: Installed self-improvement and evolution skills can propose future changes to the created agent. <br>
Mitigation: Keep review mode enabled and inspect installed skills and evolution proposals before approving any changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dao24dao/create-agent-arch) <br>
- [OpenClaw agent CLI documentation](https://docs.openclaw.ai/cli/agents) <br>
- [OpenClaw channel documentation](https://docs.openclaw.ai/channels) <br>
- [Workspace templates](references/workspace-templates.md) <br>
- [Channel parameter templates](references/channel-params.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command blocks and generated workspace file content.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create persistent local OpenClaw workspace files and instruct execution of OpenClaw, npx, git, and channel-binding commands.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
