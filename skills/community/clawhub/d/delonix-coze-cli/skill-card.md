## Description: <br>
Interact with Coze CLI (@coze/cli) to create and deploy Coze projects, manage spaces and organizations, send messages to projects, generate media, and automate Coze workflows through terminal commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chaoliuzhu](https://clawhub.ai/user/chaoliuzhu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to guide an agent through authenticated Coze CLI workflows, including project creation, deployment, messaging, environment configuration, media generation, and file upload. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill guides an agent through authenticated Coze CLI commands that can alter remote projects and workspace configuration. <br>
Mitigation: Use a least-privileged Coze account and non-production workspace where possible, and require explicit approval before deploy, delete, environment variable, domain, skill, upload, or file-sending commands. <br>
Risk: Message, upload, and log-analysis workflows can send local files or sensitive project data to Coze services. <br>
Mitigation: Review and redact files, logs, prompts, and command arguments before sending them through Coze CLI. <br>
Risk: The workflow depends on the external @coze/cli package and an OAuth-authenticated session. <br>
Mitigation: Verify the @coze/cli package source and version before installation, and keep OAuth credentials scoped to the intended organization and workspace. <br>


## Reference(s): <br>
- [Coze CLI command reference](references/commands.md) <br>
- [Coze CLI official documentation](https://docs.coze.cn/developer_guides/coze_cli) <br>
- [Coze CLI quickstart](https://docs.coze.cn/developer_guides/coze_cli_quickstart) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include text or JSON CLI output guidance when commands support --format json.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
