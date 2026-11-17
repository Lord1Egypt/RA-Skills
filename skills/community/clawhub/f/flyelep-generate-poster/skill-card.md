## Description:

Generates e-commerce product hero images, detail posters, and white-background product images through the Flyelep API, using asynchronous or synchronous requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flyelepai](https://clawhub.ai/user/flyelepai)

### License/Terms of Use:

MIT-0

## Use Case:

External e-commerce sellers and operators use this skill to request product hero images, detail-page posters, or white-background product images from Flyelep. They provide the product brief and API key, and may supply reference images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reference images may be sent to an external Flyelep upload service, and the security review notes incomplete reference resolution.

Mitigation: Check the upload destination and confirm each image is intended to be sent; review unresolved local-path references before relying on the skill.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/flyelepai/skills/flyelep-generate-poster)

## Skill Output:

**Output Type(s):** [Images, API Calls, JSON]

**Output Format:** [Generated image URLs and JSON task responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-provided Flyelep API key; reference images may be uploaded for use in generation.]

## Skill Version(s):

1.0.3 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
