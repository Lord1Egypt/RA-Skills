## Description:

DigenAI image and video generation for OpenClaw, supporting text-to-image, image-to-video, and text-to-video requests through DigenAI APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eeoeofl](https://clawhub.ai/user/eeoeofl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to call DigenAI services for image generation, video generation, media upload, job polling, and batch image workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence reports exposed bot and master credentials plus unsafe API-key distribution code.

Mitigation: Do not install in sensitive environments until the publisher removes and rotates exposed credentials and separates key provisioning from the generation client.

Risk: The release evidence reports unsafe secret delivery and storage behavior.

Mitigation: Use isolated test credentials, avoid sharing generated keys publicly, and review any persisted key files before deployment.

Risk: The release evidence reports disabled TLS verification and automatic TinyURL shortening.

Mitigation: Require TLS verification and make URL shortening opt-in with clear disclosure before production use.

## Reference(s):

- [DigenAI API Reference](references/api.md)
- [DigenAI API key portal](https://claw.digen.ai)
- [DigenAI video API base](https://api.cowork.digen.ai)
- [DigenAI image API base](https://api.digen.ai)
- [ClawHub skill page](https://clawhub.ai/eeoeofl/skills/digen-ai-free)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell examples; Python helpers return dictionaries and JSON files containing generated media URLs, status values, errors, and task metadata.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated media is returned as URLs; video status polling can include shortened video URLs.]

## Skill Version(s):

1.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
