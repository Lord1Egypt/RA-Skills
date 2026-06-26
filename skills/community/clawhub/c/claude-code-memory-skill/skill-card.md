## Description: <br>
Use when you want to set up, maintain, or review a Claude Code style layered memory workflow, including `CLAUDE.md` rules, session memory, durable memory, and promotion of stable learnings into instruction files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[indulgeback](https://clawhub.ai/user/indulgeback) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent maintainers use this skill to set up and review repo-local layered memory for coding agents, separating durable rules, active session state, and long-lived project context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Repo-local memory may retain secrets, credentials, health or financial details, or overly personal notes if users store them there. <br>
Mitigation: Review `.agent-memory/` content periodically, avoid saving sensitive details, and remove stale or overly personal notes. <br>
Risk: Stale durable memory can mislead future agent sessions when project files or policies have changed. <br>
Mitigation: Verify referenced files and current repository state before acting on memory, and update or delete stale memories when drift is found. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/indulgeback/claude-code-memory-skill) <br>
- [Layered Memory Architecture](references/architecture.md) <br>
- [Host Tool Mapping](references/host-tool-mapping.md) <br>
- [Example Durable Memory Index](examples/persistent-memory/MEMORY.md) <br>
- [Example Session Summary](examples/session-memory/summary.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration, shell commands] <br>
**Output Format:** [Markdown guidance with file layout examples and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or update repo-local memory files only when the user asks.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
