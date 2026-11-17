## Description:

Generates short-drama scripts from structured IP information for Douyin/Fanqie-style episodes with configurable episode count and duration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ghwyever](https://clawhub.ai/user/ghwyever)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content-production teams use this skill to turn structured novel or story IP data into short-drama episode scripts with scene lists and total duration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Supplied ip_info content is sent to the configured model endpoint.

Mitigation: Use a trusted HTTPS API_BASE and avoid submitting confidential manuscripts or business data unless the provider is approved for that data.

Risk: API credentials are required for model access.

Mitigation: Use a scoped API key with usage limits and rotate it according to the provider's credential policy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ghwyever/skills/02-script-generator)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [JSON object containing scenes and total_duration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires configured API_KEY, API_BASE, and MODEL_NAME; sends supplied ip_info to the configured model endpoint.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
