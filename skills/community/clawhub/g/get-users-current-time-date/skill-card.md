## Description: <br>
Get Users Current Time / Date returns the user's current date and time in their configured timezone for agents that need local and UTC timestamps, UTC offset, DST status, and derived date/time fields through AgentPMT-hosted remote tool calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agents use this skill to get the user's current local time, UTC time, timezone, UTC offset, and DST status for reminders, scheduling, logs, reports, and time-aware responses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The remote call can fail when the user has not configured a timezone in AgentPMT account settings. <br>
Mitigation: Check for validation errors and ask the user to configure their timezone before retrying. <br>
Risk: The tool may consume 3 credits per call and requires separate AgentPMT MCP or REST setup. <br>
Mitigation: Use the setup guidance before invoking the tool and call it only when current user-local time is needed. <br>
Risk: Prompts or logs could expose account secrets or payment credentials during setup or invocation. <br>
Mitigation: Keep account secrets, payment credentials, wallet material, and authorization headers out of prompts and logs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/agentpmt/skills/get-users-current-time-date) <br>
- [Publisher profile](https://clawhub.ai/user/agentpmt) <br>
- [AgentPMT marketplace product](https://www.agentpmt.com/marketplace/user-timezone-datetime) <br>
- [AgentPMT account MCP/REST setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Configuration] <br>
**Output Format:** [Markdown with JSON examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The remote action returns JSON datetime fields and requires the user's configured AgentPMT timezone.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
