## Description: <br>
Create Ticket helps an agent request a private Discord support channel for unresolved user issues that require manual help or privacy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charles-lpd](https://clawhub.ai/user/charles-lpd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Support agents use this skill to open a private Discord ticket channel when automated repair cannot resolve a user issue, when a complex technical error needs human intervention, or when sensitive screenshots and transaction details should be handled privately. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Private Discord ticket channels may expose sensitive support details to unintended viewers if channel permissions or retention are misconfigured. <br>
Mitigation: Before installing, confirm the Discord bot can create channels only in the intended support area, users are told before a ticket is opened, and there is a clear process for who can access, retain, and delete private ticket channels. <br>


## Reference(s): <br>
- [Create Ticket on ClawHub](https://clawhub.ai/charles-lpd/create-ticket) <br>
- [Publisher profile: charles-lpd](https://clawhub.ai/user/charles-lpd) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Guidance, API Calls] <br>
**Output Format:** [JSON string containing a private-channel creation action, payload, and user-facing message] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires username and Discord user ID; issue defaults to General Support when not provided.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
