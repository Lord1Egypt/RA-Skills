## Description: <br>
FlowConcierge turns a business website or knowledge base into a VAPI phone receptionist that can connect a Twilio number and log call outcomes to HubSpot with optional SMS follow-ups. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[windseeker1111](https://clawhub.ai/user/windseeker1111) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Business operators and developers use this skill to create and manage an AI phone receptionist from a website URL or markdown knowledge base. The skill supports setup of a VAPI assistant, Twilio phone connectivity, and webhook-based HubSpot call logging with optional SMS follow-up. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup flow can make paid Twilio changes when credentials are provided. <br>
Mitigation: Use test or limited-scope accounts first, confirm Twilio costs before setup, and prefer connecting an existing number when appropriate. <br>
Risk: The webhook can update HubSpot and send SMS follow-ups after call events. <br>
Mitigation: Secure the webhook before exposing it publicly and keep SMS follow-ups disabled until consent processes are in place. <br>
Risk: The skill requires access to VAPI, Twilio, and HubSpot accounts. <br>
Mitigation: Install only when granting that account access is acceptable, and use scoped or limited credentials where the services support them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/windseeker1111/flowconcierge) <br>
- [VAPI](https://vapi.ai) <br>
- [Twilio](https://twilio.com) <br>
- [HubSpot](https://hubspot.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, API calls] <br>
**Output Format:** [Markdown guidance with inline shell commands and command-line output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates external VAPI, Twilio, and HubSpot resources when run with valid service credentials.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
