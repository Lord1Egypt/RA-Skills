## Description: <br>
Provides local file read, write, and list guidance with default work limited to the OpenClaw workspace. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[greaterpeter](https://clawhub.ai/user/greaterpeter) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill when they need an agent to inspect logs, generate Markdown reports, or save scripts and configuration files inside an OpenClaw workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent may propose unintended workspace file changes. <br>
Mitigation: Review proposed reads and writes before accepting them, and keep operations scoped to intended workspace-relative paths. <br>
Risk: Destructive edits could remove important configuration, source, or system-related files from the workspace. <br>
Mitigation: Avoid deletion or destructive rewrites unless explicitly intended, and verify the target path before applying changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/greaterpeter/filesystem-access-greaterpeter) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with possible code, shell command, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose workspace file reads, writes, and directory listings for user review.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
