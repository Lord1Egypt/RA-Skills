## Description:

DreamAct animates face images with expressions, lip movements, and head poses derived from a driving video using the DreamAct API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hy-1990](https://clawhub.ai/user/hy-1990)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to configure DreamAct API access and generate face-animation videos from supplied face images and a driving video.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Face images, driving videos, job metadata, and generated outputs are sent to DreamAct/NewportAI infrastructure.

Mitigation: Avoid submitting sensitive or regulated media unless the provider's privacy and data handling terms meet the user's requirements.

Risk: The DREAMACT_API_KEY is stored in OpenClaw configuration for future use.

Mitigation: Protect the API key, limit access to the local configuration, and rotate the key if it may have been exposed.

Risk: Generated face-animation media can be misused or misrepresented.

Mitigation: Use the skill only with appropriate rights and consent for the source media and clearly label generated outputs where context requires it.

## Reference(s):

- [DreamAct API Reference](https://api.newportai.com/api-reference/dreamact)
- [DreamAPI Get Started](https://api.newportai.com/api-reference/get-started)
- [Dreamface AI Tools](https://tools.dreamfaceapp.com/home)
- [DreamAct Skill Page](https://clawhub.ai/hy-1990/skills/dreamact)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, API calls]

**Output Format:** [Markdown with inline shell commands and API endpoint references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DREAMACT_API_KEY; accepts a driving video URL, one or more face image URLs, and an optional seed.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
