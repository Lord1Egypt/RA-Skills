## Description: <br>
Automatically compress large contexts and clean up expired sessions, sub-agents, and temporary files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liujc007](https://clawhub.ai/user/liujc007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to reduce oversized agent contexts, archive stale sessions, and manage idle sub-agents while preserving important task history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may compress, archive, delete, or replace session-related state and terminate idle sub-agents with broad automatic authority. <br>
Mitigation: Run it in dry-run or archive-only mode by default, require explicit approval before deletion, context replacement, or sub-agent termination, and keep cleanup logs with a recovery path for archived sessions. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and cleanup reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces summaries, cleanup actions, archive notes, and token-savings reports.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
