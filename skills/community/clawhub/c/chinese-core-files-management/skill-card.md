## Description: <br>
OpenClaw workspace skill for managing core Markdown files, checking file organization, avoiding duplicate content, applying language rules, and summarizing workspace file structure. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kofna3369](https://clawhub.ai/user/kofna3369) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw agents use this skill to organize identity.md, soul.md, agents.md, user.md, memory.md, tools.md, and bootstrap.md files. It guides safe edits, backups, language rules, and file placement decisions for an OpenClaw workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide edits to sensitive local workspace files such as memory.md, user.md, agents.md, tools.md, and bootstrap.md. <br>
Mitigation: Review proposed edits before applying them and keep backups before changing core workspace files. <br>
Risk: Core Markdown files may contain personal context, operational details, or configuration information. <br>
Mitigation: Avoid storing secrets in these files and inspect content before sharing or publishing workspace files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kofna3369/chinese-core-files-management) <br>
- [Publisher profile](https://clawhub.ai/user/kofna3369) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and file templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose edits or backups for sensitive OpenClaw workspace Markdown files.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence; artifact body lists 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
