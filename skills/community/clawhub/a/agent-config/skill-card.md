## Description: <br>
Intelligently modify agent core context files (AGENTS.md, SOUL.md, IDENTITY.md, USER.md, TOOLS.md, MEMORY.md, HEARTBEAT.md). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ThatGuySizemore](https://clawhub.ai/user/ThatGuySizemore) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to maintain OpenClaw agent context files, place behavior changes in the right file, avoid duplicated instructions, and preserve size and formatting constraints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can enable persistent changes to agent behavior and related logs beyond its clearly advertised core files. <br>
Mitigation: Require explicit approval before edits to AGENTS.md, SOUL.md, TOOLS.md, MEMORY.md, HEARTBEAT.md, BOOTSTRAP.md, daily memory files, or decision and failure logs. <br>
Risk: Persistent instructions or logs could retain sensitive or unwanted behavior changes. <br>
Mitigation: Periodically inspect changed context files and logs for sensitive data, unwanted persisted instructions, and unexpected scope expansion. <br>


## Reference(s): <br>
- [Change Protocol](references/change-protocol.md) <br>
- [Claude Instruction Patterns](references/claude-patterns.md) <br>
- [OpenClaw Workspace File Map](references/file-map.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose edits to persistent agent context files and related logs.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
