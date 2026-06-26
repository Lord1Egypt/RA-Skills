## Description: <br>
CodeBuddy Code CLI installation, configuration, and usage guide for Tencent's AI-powered terminal programming assistant. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pmwalkercao](https://clawhub.ai/user/pmwalkercao) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers use this skill to install, configure, and operate Tencent CodeBuddy CLI, including interactive sessions, one-off prompts, slash commands, account login, updates, and troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing and authenticating with the Tencent CodeBuddy npm package and login flow may expose a development workspace to third-party CLI behavior. <br>
Mitigation: Install only when the package and login flow are trusted, and use the CLI in development workspaces. <br>
Risk: Permission-bypass flags can allow unintended file changes, deletion, or data loss. <br>
Mitigation: Avoid permission-bypass flags outside disposable sandboxes and review proposed file operations before use. <br>
Risk: Command and memory files may capture sensitive project details if secrets are included. <br>
Mitigation: Do not place secrets in CodeBuddy prompts, custom command files, or memory files. <br>


## Reference(s): <br>
- [CodeBuddy CLI for OpenClaw on ClawHub](https://clawhub.ai/pmwalkercao/codebuddy-cli) <br>
- [Publisher profile: pmwalkercao](https://clawhub.ai/user/pmwalkercao) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes CLI commands, usage tables, examples, login options, update steps, and security notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
