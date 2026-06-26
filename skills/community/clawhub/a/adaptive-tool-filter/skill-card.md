## Description: <br>
Filters an agent's available tools based on task intent to reduce token use and prioritize relevant tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paibwhgs](https://clawhub.ai/user/paibwhgs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agent developers and operators use this skill as guidance for selecting smaller, intent-matched tool sets before or during conversations when many tools are available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad keyword matching can expose sensitive tools such as command execution, file editing, messaging, external document actions, or subagent spawning. <br>
Mitigation: Require explicit user intent before enabling sensitive tools and avoid relying on single broad keywords for access decisions. <br>
Risk: Intent-based filtering can hide tools needed later in a conversation or retain tools that are no longer relevant. <br>
Mitigation: Carry forward recently used context only while relevant and allow users or agents to request missing tools when the task changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/paibwhgs/adaptive-tool-filter) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, configuration] <br>
**Output Format:** [Markdown with inline code and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only guidance; no executable installer or hidden data access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
