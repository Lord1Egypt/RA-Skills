## Description: <br>
Real-time observability for OpenClaw agents with a local dashboard and optional encrypted cloud sync for costs, tokens, sessions, tool calls, memory, crons, and system health. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vivekchand](https://clawhub.ai/user/vivekchand) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to monitor OpenClaw agent activity, costs, token usage, tool calls, system health, and debugging signals through ClawMetry's local dashboard or optional cloud sync. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill observes sensitive agent telemetry, including transcripts, tool inputs and outputs, logs, memory files, usage data, and costs. <br>
Mitigation: Install only when the clawmetry binary is trusted and agent telemetry collection is acceptable for the workspace. <br>
Risk: Cloud sync can send encrypted telemetry to ClawMetry Cloud for remote access. <br>
Mitigation: Keep cloud sync disabled unless remote monitoring is needed, and enable it only after accepting the data handling posture. <br>
Risk: Cloud sync depends on the CLAWMETRY_API_KEY credential. <br>
Mitigation: Store the API key in the intended environment only and rotate or remove it when cloud sync is no longer required. <br>


## Reference(s): <br>
- [ClawMetry on ClawHub](https://clawhub.ai/vivekchand/clawmetry) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline commands and local API endpoint references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the clawmetry binary and CLAWMETRY_API_KEY for cloud sync.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
