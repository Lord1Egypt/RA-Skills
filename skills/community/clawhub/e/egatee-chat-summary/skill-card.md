## Description: <br>
Pulls recent 1-7 day IM chat history for a bound Egatee account and returns grouped conversation summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ahoyoshi](https://clawhub.ai/user/ahoyoshi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to retrieve recent authorized IM chat history from Egatee and inspect grouped peer summaries for review, reporting, or follow-up. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill retrieves private IM chat history for the account bound to the Egatee API key. <br>
Mitigation: Install and run it only when authorized to access that account's conversations, and treat generated summaries as private chat data. <br>
Risk: Credential handling is review-worthy because the skill depends on EGATEE_CHAT_API_KEY and can optionally use custom endpoints or an auth token. <br>
Mitigation: Use a least-privileged Egatee API key, avoid UAT or custom base URLs unless the endpoint is trusted, and do not set EGATEE_AUTH_TOKEN unless required. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ahoyoshi/egatee-chat-summary) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Markdown, Analysis] <br>
**Output Format:** [JSON object containing meta and peer_summaries; artifact also contains a helper for readable Markdown summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EGATEE_CHAT_API_KEY and supports day range, page size, maximum pages, timeout, and optional Egatee endpoint settings.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
