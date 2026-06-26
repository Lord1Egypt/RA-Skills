## Description: <br>
Place and manage AI-driven phone calls, access transcripts, recordings, call status, and configure inbound call agents via the Bland AI API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xrichyrich](https://clawhub.ai/user/0xrichyrich) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents with Bland AI accounts use this skill to place outbound AI calls, inspect call status, retrieve transcripts and recordings, manage inbound numbers, and configure inbound call agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place real calls that may incur cost and require legal authorization or consent. <br>
Mitigation: Confirm the recipient, purpose, consent requirements, and account balance before running call commands. <br>
Risk: The skill can expose call metadata, transcripts, and temporary recording URLs. <br>
Mitigation: Treat call outputs as sensitive data and share or store them only according to the user's data handling requirements. <br>
Risk: The skill includes account-changing commands such as stopping active calls, configuring inbound agents, and buying numbers. <br>
Mitigation: Run stop-all, setup-inbound, and buy-number only after explicit confirmation of the intended account impact. <br>
Risk: The skill depends on a Bland AI API key with access to live account resources. <br>
Mitigation: Set BLAND_API_KEY explicitly for the intended account and avoid broad or shared credentials when possible. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/0xrichyrich/bland) <br>
- [Bland API Base](https://api.bland.ai/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, API calls, Configuration] <br>
**Output Format:** [Terminal text with JSON-formatted API responses where available] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BLAND_API_KEY and network access to the Bland AI API; some commands can create billing events or expose call data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
