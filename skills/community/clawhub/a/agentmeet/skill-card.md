## Description: <br>
Agent-to-agent meeting coordination over email. Read Google Calendar, generate available slots, send protocol-formatted emails. Recipients click a time slot to reply - no server, no account, pure p2p over email. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lmanchu](https://clawhub.ai/user/lmanchu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use AgentMeet to coordinate meetings over email by reading calendar availability, generating candidate slots, sending protocol-formatted invites, parsing replies, and creating calendar events. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may require Gmail and Google Calendar access, which can expose email and calendar data or permit unwanted messages and events. <br>
Mitigation: Grant the smallest possible Google permissions and require review of each outgoing email, parsed reply, and calendar event before sending or creating anything. <br>
Risk: Install and source boundaries are unclear in the release evidence. <br>
Mitigation: Verify the actual AgentMeet source code and dependencies at the referenced path before installing or running the skill. <br>


## Reference(s): <br>
- [AgentMeet ClawHub release](https://clawhub.ai/lmanchu/agentmeet) <br>
- [AgentMeet project homepage](https://github.com/agentmeet/agentmeet) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell and TypeScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce protocol-formatted email payloads, mailto links, available slot data, and calendar event guidance.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
