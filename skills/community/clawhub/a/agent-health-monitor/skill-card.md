## Description: <br>
Monitors agent health status and detects failures for fault-tolerant agent systems. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jpengcheng523-netizen](https://clawhub.ai/user/jpengcheng523-netizen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect OpenClaw agent and session health, identify failed or inactive agents, and monitor local CPU and memory pressure. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads OpenClaw session metadata and local system resource information. <br>
Mitigation: Run it only in environments where local session metadata and host resource status are appropriate for monitoring. <br>
Risk: The security review reports a suspicious hard-coded status check for another installed skill. <br>
Mitigation: Review the wrapper status behavior before installing and remove or disable that check if the referenced local skill is not trusted. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jpengcheng523-netizen/agent-health-monitor) <br>
- [Publisher profile](https://clawhub.ai/user/jpengcheng523-netizen) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON health reports and status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports timestamped health status, session counts, failed agents, wrapper status, and local resource usage.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
