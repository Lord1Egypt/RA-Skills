## Description:

Issue ClawPrint reverse-CAPTCHA challenges to verify that another user or agent is a real AI, not a human. Uses the ClawPrint API to generate speed or pattern challenges that only machines can solve within the time limit.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fusionlabssource](https://clawhub.ai/user/fusionlabssource)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to issue, present, verify, and validate ClawPrint challenges before continuing an AI-only workflow. It can support gating decisions, but the server security guidance says it should be treated as a non-authoritative capability signal rather than proof of identity or permission.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The verification result can be mistaken for proof of identity or authorization.

Mitigation: Use ClawPrint only as a non-authoritative capability signal and require a separate authenticated authorization decision before sensitive actions.

Risk: A reusable secret key is sent to a configurable remote server during validation.

Mitigation: Pin CLAWPRINT_SERVER_URL to a trusted HTTPS service you control, protect CLAWPRINT_SECRET_KEY, and rotate it if exposure is suspected.

Risk: The skill text suggests using challenges before sharing sensitive credentials.

Mitigation: Do not automatically release API keys, credentials, or protected resources based only on a passed challenge.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fusionlabssource/skills/clawprint-verify)
- [ClawPrint service endpoint](https://dependable-adventure-production-44e3.up.railway.app/)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, json]

**Output Format:** [Markdown guidance with inline bash commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, CLAWPRINT_SERVER_URL, CLAWPRINT_SITE_KEY, and CLAWPRINT_SECRET_KEY for validation.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
