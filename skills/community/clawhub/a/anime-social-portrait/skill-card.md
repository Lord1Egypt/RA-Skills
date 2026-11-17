## Description:

Create anime-style social avatars, Moments covers, and Twitter/X headers from real user photos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shuminliu026](https://clawhub.ai/user/shuminliu026)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to turn uploaded personal photos into anime-style social media assets, including avatars, Moments covers, and Twitter/X headers. The agent selects a supported anime style, constructs a prompt, calls the Mew image process endpoint, checks the result, and suggests follow-up variations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a mew.design API key and uploaded personal photo, which are sent to mew.design for image processing.

Mitigation: Ask for the key only when needed, avoid storing or reusing it outside the current task context, and tell users not to provide photos or credentials they do not want processed by that third-party service.

Risk: Installing the wrong package could route sensitive photos or credentials through unintended instructions.

Mitigation: Confirm the exact ClawHub package URL before installation: https://clawhub.ai/shuminliu026/anime-social-portrait.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shuminliu026/skills/anime-social-portrait)
- [ClawHub install URL](https://clawhub.ai/shuminliu026/anime-social-portrait)
- [Supported styles](artifact/references/styles.md)
- [Mew image process endpoint](https://api.mew.design/open/api/image/process)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Chinese Markdown response with generated image link and concise follow-up guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include asset-specific aspect ratios for Moments covers and Twitter/X headers; requires user-provided API key and uploaded photo.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
