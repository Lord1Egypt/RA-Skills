## Description:

Issues ClawPrint reverse-CAPTCHA challenges through the ClawPrint API to verify that another user or agent is likely an AI rather than a human.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fusionlabssource](https://clawhub.ai/user/fusionlabssource)

### License/Terms of Use:


## Use Case:

Developers, agent operators, and external users use this skill to issue and validate ClawPrint reverse-CAPTCHA challenges before continuing gated AI-only workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may be used as the sole basis for sharing API keys, credentials, private data, or privileged access.

Mitigation: Use ClawPrint only as an auxiliary automation signal and require separate authorization checks before releasing sensitive resources.

Risk: The validation flow sends CLAWPRINT_SECRET_KEY to a runtime-configured ClawPrint server.

Mitigation: Configure only trusted HTTPS ClawPrint servers you control, protect CLAWPRINT_SECRET_KEY as sensitive, and avoid untrusted CLAWPRINT_SERVER_URL values.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/fusionlabssource/skills/captcha-ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, CLAWPRINT_SERVER_URL, CLAWPRINT_SITE_KEY, and CLAWPRINT_SECRET_KEY for server-side validation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
