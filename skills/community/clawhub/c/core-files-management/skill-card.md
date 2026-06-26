## Description: <br>
Core Files Management helps OpenClaw workspace agents manage and update core Markdown files, check organization, avoid duplication, and apply language rules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kofna3369](https://clawhub.ai/user/kofna3369) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw workspace agents use this skill to organize identity.md, soul.md, agents.md, user.md, memory.md, tools.md, and bootstrap.md while avoiding duplication and preserving language rules. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide edits to local OpenClaw workspace Markdown files, so incorrect approvals could overwrite useful workspace context. <br>
Mitigation: Review proposed changes before approving writes and confirm backups were created before modifying core files. <br>
Risk: Core workspace files may contain sensitive user or environment details if users store them there. <br>
Mitigation: Avoid storing passwords, tokens, private keys, or sensitive account details in these Markdown files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kofna3369/core-files-management) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with file-path tables and optional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local workspace file edits and backups for user review.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and skill body version table) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
