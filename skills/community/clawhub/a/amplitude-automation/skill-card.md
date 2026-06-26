## Description: <br>
Automate Amplitude tasks via Rube MCP (Composio): events, user activity, cohorts, user identification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sohamganatra](https://clawhub.ai/user/sohamganatra) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and analytics operators use this skill to guide an agent through Amplitude workflows, including sending events, retrieving user activity, identifying users, and managing cohorts through a connected Rube MCP Amplitude account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An agent using this skill can read or change analytics data through a connected Amplitude account. <br>
Mitigation: Install it only for intended Amplitude automation and verify the workspace, user IDs, cohort IDs, and payloads before execution. <br>
Risk: User activity and analytics payloads may expose sensitive product or user behavior data. <br>
Mitigation: Avoid retrieving or sharing raw user activity unless necessary, and revoke the Rube/Amplitude connection when it is no longer needed. <br>
Risk: Incorrect identifiers or timestamps can send events to the wrong user, cohort, or time period. <br>
Mitigation: Resolve Amplitude internal user IDs before activity lookups, confirm cohort IDs before membership updates, and use millisecond epoch timestamps for events. <br>


## Reference(s): <br>
- [Rube MCP endpoint](https://rube.app/mcp) <br>
- [ClawHub release page](https://clawhub.ai/sohamganatra/amplitude-automation) <br>
- [Publisher profile](https://clawhub.ai/user/sohamganatra) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with tool sequences, parameter notes, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Rube MCP and an active Amplitude connection before the agent can act on Amplitude data.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
