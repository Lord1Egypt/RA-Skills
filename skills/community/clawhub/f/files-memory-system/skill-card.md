## Description: <br>
Files Memory System helps OpenClaw agents maintain group-isolated, private, and global memory directories, organize workspace projects and repositories, and route group-context file operations to the appropriate location. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wxwzl](https://clawhub.ai/user/wxwzl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to initialize and manage persistent memory across private chats, group chats, shared global context, and group-specific repositories or skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill persistently changes workspace-wide agent instructions through AGENTS.md registration. <br>
Mitigation: Review the exact AGENTS.md block before enabling the skill and remove or edit rules that do not match the workspace policy. <br>
Risk: Memory files may store private, group, or global context in plaintext and may be reloaded in later sessions. <br>
Mitigation: Do not store credentials or sensitive personal data in memory files; use environment variables or a secrets manager for secrets. <br>
Risk: Group, private, and global memory scopes can expose information more broadly than intended if users choose the wrong target. <br>
Mitigation: Define clear rules for what may be written to private, group, and global memory, and periodically review stored memory files. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/wxwzl/files-memory-system) <br>
- [User guide](references/USER_GUIDE.md) <br>
- [Architecture](references/architecture.md) <br>
- [Security practices](SECURITY.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and file path guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update workspace memory files, repository directories, and AGENTS.md registration when its bundled scripts are executed.] <br>

## Skill Version(s): <br>
1.16.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
