## Description:

Doubao (Volcengine ARK) text-to-image, text-to-video, and image-to-video media generation with generated files saved locally and sent back to chat.

This skill is ready for commercial/non-commercial use.

## Publisher:

[systiger](https://clawhub.ai/user/systiger)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to generate images or videos through Doubao and Volcengine ARK from text prompts or an input image URL. It is useful when an agent needs to create media files, return generation status, and surface the resulting local files in chat.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, image URLs, and generated-media requests are sent to Volcengine ARK using the user's ARK_API_KEY.

Mitigation: Avoid secrets, private prompts, and private image links; use an appropriate ARK_API_KEY and review provider terms before use.

Risk: Generated files are written to ~/.openclaw/workspace/output/ and may include unwanted or sensitive generated media.

Mitigation: Review generated files before sharing or retaining them, and delete outputs that should not persist.

Risk: The documented dependency installation uses an unpinned requests package.

Mitigation: Prefer a pinned dependency setup for repeatable installations.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/systiger/skills/doubao-media)
- [Volcengine ARK Documentation](https://www.volcengine.com/docs/82379)
- [Doubao Model Pricing](https://console.volcengine.com/ark)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill may create JPEG images and MP4 videos under ~/.openclaw/workspace/output/ and print task status or local file paths.]

## Skill Version(s):

1.0.0 (source: frontmatter, manifest, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
