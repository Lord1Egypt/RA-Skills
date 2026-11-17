## Description:

Use a text model such as gpt-5.4 with the image_generation tool over an OpenAI-compatible /v1/responses endpoint, matching the CPA blog example.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shiftshen](https://clawhub.ai/user/shiftshen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to generate image files by calling an OpenAI-compatible Responses API with a text model and the image_generation tool. It is intended for environments where direct gpt-image-2 model calls are not exposed by the gateway.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credentials may be sent to an unintended or unencrypted endpoint if the base URL and API key are mismatched or fall back from local configuration.

Mitigation: Use only trusted HTTPS endpoints, set the matching base URL and API key explicitly, and avoid relying on fallback credentials from models.json.

Risk: Image prompts and generated output may contain sensitive information that leaves the local environment.

Mitigation: Do not include secrets or sensitive data in prompts unless the endpoint and output path are approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shiftshen/skills/cpa-gpt-image-2)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration, Guidance]

**Output Format:** [Image file output with Markdown and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes the first base64 image returned by the Responses API to a caller-provided output path.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
