## Description:

Detect and read the largest license plate from a local image using the TrafficEye REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eyedea-ai](https://clawhub.ai/user/eyedea-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and operations teams use this skill to extract license plate text and plate metadata from vehicle images through the TrafficEye API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Vehicle images and API credentials may be sent to a configurable endpoint.

Mitigation: Use the skill only with images approved for upload, pin TRAFFICEYE_API_URL to a trusted HTTPS host, and prevent untrusted configuration from changing the endpoint.

Risk: API keys can be exposed if query-string authentication is used.

Mitigation: Prefer header or bearer authentication and avoid query-string API keys.

## Reference(s):

- [TrafficEye](https://trafficeye.ai)
- [TrafficEye API](https://www.trafficeye.ai/api)
- [ClawHub Skill Page](https://clawhub.ai/eyedea-ai/skills/automatic-number-plate-recognition)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON plate-recognition output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns the selected largest plate payload, including recognized text, position, unreadable score, and source indexes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
