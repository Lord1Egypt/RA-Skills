## Description: <br>
Make real phone calls to businesses. Book reservations, cancel subscriptions, navigate IVR menus. Get transcripts and recordings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yanmellata](https://clawhub.ai/user/yanmellata) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to have an agent place real business phone calls, such as booking reservations, canceling subscriptions, or navigating IVR menus, then return the call outcome, summary, transcript, and recording URL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place real phone calls and affect reservations or subscriptions without requiring an explicit final confirmation. <br>
Mitigation: Require manual confirmation before every call, including the phone number, business identity, objective, and any permitted commitments. <br>
Risk: Calls may create recordings or transcripts and may expose sensitive personal, account, legal, medical, or payment information. <br>
Mitigation: Confirm recording and transcription acceptability before use, keep the API key private, and avoid sensitive calls unless the provider's privacy, retention, and consent terms have been reviewed. <br>


## Reference(s): <br>
- [AgentPhone ClawHub listing](https://clawhub.ai/yanmellata/agentphone) <br>
- [AgentPhone website](https://agentphone.app) <br>
- [AgentPhone API docs](https://agentphone.app/docs) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with API request examples and structured call-result fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AGENTPHONE_API_KEY and curl; calls return status, outcome, summary, transcript, recording URL, and duration when available.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
