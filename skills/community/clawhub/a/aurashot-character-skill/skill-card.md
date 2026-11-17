## Description:

Character-consistent AI image generation for agents that creates ID photos, new character scenes, and image edits from a face reference while preserving identity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[whbzju](https://clawhub.ai/user/whbzju)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to create and manage roleplay or design characters, generate identity baselines from face references, produce new outfit or scene images, and edit existing character images through AuraShot.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends face photos, target images, clothing or scene references, prompts, and an AuraShot API key to the image-generation service.

Mitigation: Use it only with images and prompts the user is comfortable uploading, get consent for real-person photos, and review AuraShot's handling of submitted data before deployment.

Risk: The skill reads API keys from environment variables or a local .aurashot.env file.

Mitigation: Protect .aurashot.env, keep it out of version control, and rotate the key if it is exposed.

Risk: Custom base URLs or proxy settings can change where images, prompts, and credentials are sent.

Mitigation: Use the default AuraShot endpoint unless a trusted operator explicitly approves the destination and proxy configuration.

Risk: Generated avatars and downloaded gallery images may contain sensitive personal data.

Mitigation: Store avatar folders in access-controlled locations and delete local character assets when they are no longer needed.

## Reference(s):

- [AuraShot API Reference](references/api.md)
- [AuraShot Homepage](https://www.aurashot.art)
- [AuraShot API Documentation](https://www.aurashot.art/studio?tab=docs)
- [ClawHub Skill Page](https://clawhub.ai/whbzju/skills/aurashot-character-skill)
- [Publisher Profile](https://clawhub.ai/user/whbzju)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code, JSON, Files]

**Output Format:** [Markdown guidance with shell commands; CLI responses are JSON and generated images may be downloaded to local files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3 and an AuraShot API key; image inputs may be local files or public HTTPS URLs.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
