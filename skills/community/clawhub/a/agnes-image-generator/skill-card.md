## Description:

Generates and edits images from text prompts or reference images using the Agnes Image 2.1 Flash API and returns direct image URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lg0219](https://clawhub.ai/user/lg0219)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to generate images from prompts or edit supplied reference images in OpenClaw workflows, with configurable image sizes and URL output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reference images or local files passed to image-to-image generation may be uploaded to Agnes.

Mitigation: Use only non-sensitive images that you are authorized to upload, and verify the exact file path before running image-to-image commands.

Risk: Generated output links may be public or accessible outside the local environment.

Mitigation: Avoid sensitive prompts or images and treat returned image URLs as shareable unless access controls are confirmed.

Risk: The Agnes API key can be exposed if hard-coded into source files or committed with the skill.

Mitigation: Store the API key in an environment variable or secret store and do not commit credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lg0219/skills/agnes-image-generator)

## Skill Output:

**Output Type(s):** [JSON, Image URLs]

**Output Format:** [JSON object with a success flag, an image URL on success, and an error message on failure.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an Agnes API key and returns cloud-hosted image URLs.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact/skill.yaml lists 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
