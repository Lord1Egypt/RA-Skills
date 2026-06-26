## Description: <br>
Register Cliento booking pages via URL, check availability, and execute actual service bookings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[patello](https://clawhub.ai/user/patello) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and personal agents use this skill to register Cliento booking pages, check salon or barbershop availability, reserve slots, and confirm service bookings after user approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can finalize real service bookings and handles user contact details. <br>
Mitigation: Review the service, provider, time, price, and contact details, then require explicit user confirmation before final booking. <br>
Risk: Calendar access and saved USER.md contact details may expose personal information. <br>
Mitigation: Decline calendar access unless conflict checking is needed, and save contact details only after explicit user consent. <br>
Risk: The skill relies on undocumented Cliento endpoints that may change or fail. <br>
Mitigation: Use the bundled Python helper, inspect responses, and stop before confirmation when API results are missing or unexpected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/patello/cliento-booker) <br>
- [patello publisher profile](https://clawhub.ai/user/patello) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON or text responses from the Python helper.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses python3, can maintain .cliento/stores.json, and may consult USER.md for contact details only when needed.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
