## Description: <br>
Command-line tool to manage contacts, tasks, notes, deals, events, and communications via the Follow Up Boss API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[danielfoch](https://clawhub.ai/user/danielfoch) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to run Follow Up Boss CRM commands from an agent workflow, including retrieving account data and managing people, tasks, notes, deals, events, communications, and webhooks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The CLI can create, update, complete, or delete CRM records and webhooks in Follow Up Boss. <br>
Mitigation: Review mutating commands and JSON payloads before running them against production CRM data. <br>
Risk: The skill requires a Follow Up Boss API key that can grant account access. <br>
Mitigation: Use a limited API key where available and keep FUB_API_KEY out of shared logs, transcripts, and committed files. <br>
Risk: Text and email commands log communications but do not send messages. <br>
Mitigation: Use Follow Up Boss sending features or approved integrations when an actual outbound message is required. <br>
Risk: Follow Up Boss API rate limits may reject excessive requests. <br>
Mitigation: Throttle repeated requests and retry only after the relevant rate-limit window. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/danielfoch/follow-up-boss) <br>
- [Follow Up Boss API base URL](https://api.followupboss.com/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, API calls, Text] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands require FUB_API_KEY and may print Follow Up Boss API responses as formatted JSON.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
