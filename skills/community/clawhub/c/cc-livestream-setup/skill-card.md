## Description:

This skill should be used when the user needs to create or configure a CC live streaming room via API, including room creation, authentication setup, and credential management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elberren](https://clawhub.ai/user/elberren)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to create CC live streaming rooms, collect required CC account credentials, choose a room template, and return the room creation result.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive CC account credentials and API keys.

Mitigation: Request credentials only when needed, do not store or cache them, and avoid exposing API keys through command-line history or logs.

Risk: The helper script creates rooms with weak hard-coded publisher and assistant passwords.

Mitigation: Replace the default passwords with unique strong values before real use, and rotate any passwords that may have been exposed.

Risk: The security review notes that full request URLs and sensitive responses may be logged.

Mitigation: Remove or redact sensitive request and response logging before using the skill with production credentials.

## Reference(s):

- [CC Live API Documentation Reference](references/api_docs.md)
- [CC Live API Appendix](https://doc.bokecc.com/live/developer/live_api/Appendix_2.html)
- [ClawHub Skill Page](https://clawhub.ai/elberren/skills/cc-livestream-setup)
- [Publisher Profile](https://clawhub.ai/user/elberren)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration]

**Output Format:** [Conversational guidance with shell command usage and API result summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Collects CC userid, API key, room name, template type, and optional mobile view mode from the user.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
