## Description: <br>
Universal flow tracer with cross-platform date support, latency calculation, and token estimation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zven0312](https://clawhub.ai/user/zven0312) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to inspect recent local OpenClaw/MCP tool-call logs, calculate step latency, estimate payload size, and prepare trace tables or Mermaid sequence diagrams for workflow review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Trace output can reveal recent tool names, timestamps, and approximate input sizes from the local workflow. <br>
Mitigation: Install only in workspaces where local log inspection is acceptable, and review generated trace output before sharing it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zven0312/flow-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [JSON trace data and Markdown trace summaries with Mermaid sequence diagrams] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads the last 15 matching entries from local claw_execution.log and estimates token counts from payload character size.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter and changelog mention 1.3.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
