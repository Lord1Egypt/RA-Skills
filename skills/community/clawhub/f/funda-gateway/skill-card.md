## Description:

Local Funda.nl HTTP gateway for listing details, search, and image previews.

This skill is ready for commercial/non-commercial use.

## Publisher:

[risboo6909](https://clawhub.ai/user/risboo6909)

### License/Terms of Use:


## Use Case:

Developers and external OpenClaw users use this skill to run a local gateway that lets agents search Funda.nl listings, retrieve listing details and price history, and generate resized listing photo previews for housing-monitoring workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local gateway has no authentication or rate limiting.

Mitigation: Install only in a trusted local environment, keep the gateway bound to 127.0.0.1, and do not expose it to other users or networks.

Risk: Network and image fetching are not hardened for broad exposure.

Mitigation: Before broader use, add host/IP allowlisting and response-size limits, and treat external Funda data and image content as untrusted.

Risk: Pinned dependencies require review before installation.

Mitigation: Update vulnerable dependencies as needed and prefer hashed dependency locks for repeatable installs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/risboo6909/skills/funda-gateway)
- [PyFunda library](https://github.com/0xMH/pyfunda)
- [OpenClaw Heartbeat documentation](https://docs.openclaw.ai/gateway/heartbeat)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Gateway responses include structured JSON; image previews may be returned as base64 strings or saved JPEG files.]

## Skill Version(s):

1.0.12 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
