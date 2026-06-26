## Description: <br>
Make phone calls, view received SMS, provision numbers, manage agents, and track billing through the AgentLine telephony API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sameersribot](https://clawhub.ai/user/sameersribot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent place and manage US phone calls, inspect inbound SMS, retrieve call transcripts, configure phone agents, provision numbers, and review AgentLine billing. <br>

### Deployment Geography for Use: <br>
United States <br>

## Known Risks and Mitigations: <br>
Risk: Paid telephony actions can create charges for phone numbers and per-minute calls. <br>
Mitigation: Confirm user intent before provisioning numbers or placing calls, and review AgentLine billing data when cost is relevant. <br>
Risk: The skill accesses private communications data, including inbound SMS, call transcripts, phone numbers, and billing details. <br>
Mitigation: Install only when the user trusts AgentLine with this data, protect AGENTLINE_API_KEY, and avoid sharing transcripts or message contents beyond the user's request. <br>
Risk: The artifact requires a long-running local event poller for inbound calls and SMS. <br>
Mitigation: Confirm that the user wants the poller running, launch it only with the intended API key, and make clear how to stop and remove the process. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sameersribot/agentline-telephone) <br>
- [AgentLine](https://agentline.cloud) <br>
- [AgentLine API Base URL](https://api.agentline.cloud) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and API request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local background polling commands and summaries of calls, SMS events, transcripts, agents, numbers, and billing data.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
