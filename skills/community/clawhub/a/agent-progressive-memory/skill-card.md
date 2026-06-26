## Description: <br>
Provides a progressive disclosure protocol for agents to read group, team, and project memory through an index-first workflow instead of loading all memory at once. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[biociao](https://clawhub.ai/user/biociao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to manage shared group memory in chat, team, and project collaboration contexts. It guides agents to map group names, read an index first, load only the most relevant memory files, and optionally maintain local memory state through hooks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent group memory can retain sensitive or stale workspace information. <br>
Mitigation: Install only in workspaces where persistent group memory is acceptable, and periodically inspect or prune memory files and memory/flush-state.json. <br>
Risk: Optional hooks can automatically write local memory state. <br>
Mitigation: Review the hook code before copying it into ~/.openclaw/hooks and enable precompact-remem only when automatic memory-state updates are desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/biociao/agent-progressive-memory) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown guidance with inline shell commands and local hook configuration details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes optional hooks that update local memory state files when installed.] <br>

## Skill Version(s): <br>
1.2.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
