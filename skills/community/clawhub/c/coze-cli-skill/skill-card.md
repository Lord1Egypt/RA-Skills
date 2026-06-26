## Description: <br>
Interact with Coze CLI (@coze/cli) to create and deploy Coze projects, manage spaces and organizations, send messages to projects, generate images, audio, and video, and automate Coze workflows via terminal. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cengsin](https://clawhub.ai/user/cengsin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to operate Coze CLI workflows from an agent, including project creation, deployment, workspace setup, messaging, media generation, and configuration tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Deploy, delete, environment, and configuration commands can change live Coze projects or workspaces. <br>
Mitigation: Confirm the target organization, space, project, environment, and command intent before running deploy, delete, env, or config operations. <br>
Risk: Piped logs, uploaded files, prompts, and local file references may contain secrets, personal data, or proprietary content. <br>
Mitigation: Review and redact sensitive content before sending logs, uploading files, or passing local context to Coze CLI commands. <br>
Risk: The skill depends on installing and operating the external Coze CLI package with an OAuth-authenticated session. <br>
Mitigation: Install only from a trusted package source and use accounts with permissions appropriate to the requested Coze operation. <br>


## Reference(s): <br>
- [Coze CLI command reference](references/commands.md) <br>
- [Coze CLI official docs](https://docs.coze.cn/developer_guides/coze_cli) <br>
- [Coze CLI quickstart](https://docs.coze.cn/developer_guides/coze_cli_quickstart) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Text, JSON] <br>
**Output Format:** [Markdown with inline bash command examples and optional JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference OAuth-authenticated Coze organizations, spaces, projects, environment variables, uploaded files, and generated media outputs.] <br>

## Skill Version(s): <br>
0.1.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
