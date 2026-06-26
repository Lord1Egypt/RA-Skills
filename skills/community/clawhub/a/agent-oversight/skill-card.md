## Description: <br>
Comprehensive AI agent oversight and management skill. Monitors sub-agents, manages file edit coordination, logs failures, kills hung sessions, and maintains oversight records. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1477009639zw-blip](https://clawhub.ai/user/1477009639zw-blip) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to inspect local OpenClaw agent sessions and surface basic oversight status during multi-agent work. It is intended to support coordination and review, not to replace manual confirmation for disruptive actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release security summary says the skill overstates coordination, failure logging, and automatic hung-session cleanup behavior. <br>
Mitigation: Review the implementation before installing and do not rely on it for real coordination, failure logging, or session cleanup unless those behaviors are implemented with explicit confirmation and clear limits. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/1477009639zw-blip/agent-oversight) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text command output and Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and invokes the local openclaw CLI when listing sessions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
