## Description: <br>
Execute AI coding CLI tools (Claude Code / Gemini CLI / qodercli) on behalf of Workers. Use when a Worker sends a coding-request: message, asking Manager to run coding operations in their workspace. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MontyCN](https://clawhub.ai/user/MontyCN) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let a Manager coordinate coding work by detecting approved local AI coding CLIs, configuring delegation mode, executing Worker-provided prompts in the Worker workspace, and returning success or failure guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Worker messages can trigger powerful local AI coding CLI tools in auto-approval mode. <br>
Mitigation: Enable the skill only for trusted Workers, restrict who can send coding requests, and require human review before accepting code changes. <br>
Risk: Prompts and generated logs may expose sensitive workspace details or credentials. <br>
Mitigation: Use contained workspaces, avoid placing secrets in prompts, and review generated coding-cli logs before sharing or retaining them. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Markdown] <br>
**Output Format:** [Markdown instructions with inline bash commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces CLI execution logs in the workspace and task messages for Worker and admin follow-up.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
