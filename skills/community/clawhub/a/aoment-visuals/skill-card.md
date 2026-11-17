## Description:

AI image and video generation service - supports text-to-image, image-to-image, and video generation. Automatic API key registration supported for limited-time free access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[regalzzz](https://clawhub.ai/user/regalzzz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent users use this skill to register an Aoment agent API key, generate images or videos from prompts and reference images, and check generation quota.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends prompts, reference images, nicknames, API keys, and generated-media downloads through Aoment.

Mitigation: Use only approved non-sensitive inputs, avoid sensitive internal reference-image URLs, and prefer credential handling that does not place real API keys directly in shell commands.

Risk: The artifact describes remote package updates, and the security evidence warns against automatic replacement from the latest ZIP without review.

Mitigation: Pin the reviewed release and manually review and integrity-check any replacement package before use.

Risk: Reference-image URLs can be fetched and uploaded to Aoment during image-to-image or video generation.

Mitigation: Pass only trusted public or approved reference images, and avoid internal or credential-bearing URLs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/regalzzz/skills/aoment-visuals)
- [Aoment Service](https://www.aoment.com)
- [Aoment Visuals Skill Package](https://www.aoment.com/downloads/aoment-visuals-skill.zip)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [JSON responses and Markdown instructions with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns generated image or video URLs, quota information, or structured error messages.]

## Skill Version(s):

1.0.5 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
