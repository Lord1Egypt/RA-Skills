## Description: <br>
Builtin Tools is a cross-platform Python standard-library toolkit that gives an agent fallback utilities for filesystem operations, content search, web search and fetch, runtime installation, persistent memory, scheduling, task management, and shell-command orchestration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangjiaocheng](https://clawhub.ai/user/wangjiaocheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill when an agent host lacks basic local tools and needs JSON-driven fallback scripts for files, search, web access, command execution, installation, memory, scheduling, or task tracking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can grant broad local-tool authority, including shell, file, network, install, memory, and automation actions. <br>
Mitigation: Install only for agents that intentionally need these privileges, and enforce explicit approval plus strict workspace, host, and path limits. <br>
Risk: Shell command mode, recursive deletion, arbitrary file writes, runtime downloads, browser opening, memory storage, and automation generation are privileged actions. <br>
Mitigation: Review requests before execution and restrict these operations to trusted inputs and controlled environments. <br>


## Reference(s): <br>
- [Builtin Tools Protocol](references/protocol.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/wangjiaocheng/builtin-tools) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON tool results, Markdown guidance, code snippets, shell commands, and configuration instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scripts accept JSON input and return JSON success or error objects with exit codes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
