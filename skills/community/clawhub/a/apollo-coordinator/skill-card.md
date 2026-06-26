## Description: <br>
Coordinates complex tasks by splitting them across multiple helper agents and summarizing the results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nic-yuan](https://clawhub.ai/user/nic-yuan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to coordinate Hub-and-Spoke task decomposition, parallel subagent work, timeout handling, conflict surfacing, and final result synthesis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The included status-check script reads local OpenClaw workflow and task metadata and writes a coordinator state file. <br>
Mitigation: Run it only in the intended OpenClaw workspace and review workflow or task status files first if they may contain sensitive information. <br>
Risk: Parallel helper-agent outputs can conflict, time out, or contain incorrect guidance. <br>
Mitigation: Keep the coordinator responsible for surfacing conflicts, marking timeouts, and requiring human review before acting on the final synthesis. <br>


## Reference(s): <br>
- [Apollo Coordinator on ClawHub](https://clawhub.ai/nic-yuan/apollo-coordinator) <br>
- [nic-yuan publisher profile](https://clawhub.ai/user/nic-yuan) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown text with structured task and result sections; the included shell script prints a local coordination status report.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include task decomposition, per-task status, timeout notes, conflict notes, and local workspace coordination status.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
