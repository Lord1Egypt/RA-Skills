## Description:

AI image editing and beautification suite for portrait retouching, body reshaping, AI hair styling, AI clothes and cosplay changes, expression edits, photo restoration, upscaling, and artistic filters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beautypluscom](https://clawhub.ai/user/beautypluscom)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to submit still images to BeautyPlus for portrait retouching, outfit or hair changes, expression edits, photo restoration, and delivery of resulting image URLs or media back to the user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch arbitrary URLs and upload media to cloud storage.

Mitigation: Run it in an isolated environment with restricted network access, and prefer local image files or trusted public HTTPS URLs.

Risk: BP and messaging credentials are required for API and delivery workflows.

Mitigation: Protect credentials in environment or host-managed secret storage, and avoid placing tokens in command-line arguments or logs.

Risk: Server-provided billing links may be relayed to users.

Mitigation: Verify that billing links are BeautyPlus domains before sharing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/beautypluscom/skills/beautyplus-ai)
- [BeautyPlus Developers](https://beautyplus.com/developers/console)
- [BeautyPlus product overview](https://beautyplus.com/)
- [Skill workflow](artifact/SKILL.md)
- [Multi-platform delivery](artifact/docs/multi-platform.md)
- [Errors and polling](artifact/docs/errors-and-polling.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 plus BP_AK and BP_SK credentials; the current catalog is image-focused, with video workflows documented as reserved.]

## Skill Version(s):

1.0.4 (source: ClawHub release metadata; artifact frontmatter lists 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
