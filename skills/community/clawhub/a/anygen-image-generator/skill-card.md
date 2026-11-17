## Description:

Generates images, illustrations, and visual assets through the AnyGen CLI and service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[logictortoise](https://clawhub.ai/user/logictortoise)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to create posters, banners, social media graphics, product mockups, logo concepts, thumbnails, covers, icons, and other generated visual assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Image prompts and reference assets may be sent to AnyGen's external service.

Mitigation: Use the skill only with content approved for that service and avoid sensitive material unless policy permits it.

Risk: Authentication examples include an API-key command pattern.

Mitigation: Prefer browser login, a secret manager, or environment variables over pasting API keys into commands.

Risk: The skill relies on external CLI and workflow installation.

Mitigation: Review the @anygen/cli package and anygen-workflow-generate skill source and version before allowing automatic installation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/logictortoise/skills/anygen-image-generator)
- [AnyGen Service](https://www.anygen.io)
- [ClawHub Publisher Profile](https://clawhub.ai/user/logictortoise)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Generated image files with Markdown guidance and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the AnyGen CLI and ANYGEN_API_KEY; prompts and reference assets may be sent to the AnyGen service.]

## Skill Version(s):

3.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
