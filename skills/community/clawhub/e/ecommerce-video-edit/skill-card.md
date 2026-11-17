## Description:

Turns existing product footage into short-form ecommerce video ads with FFmpeg, including vertical edits, captions, calls to action, and hook variants.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vargai](https://clawhub.ai/user/vargai)

### License/Terms of Use:

MIT-0

## Use Case:

Ecommerce marketers and video editors use this skill to turn existing product or creator footage into vertical ads for TikTok, Reels, and Meta, then make hook variants for testing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The hosted processing option may share footage or media URLs with Varg.

Mitigation: Use the hosted option only after understanding and accepting that sharing; process sensitive footage locally with FFmpeg.

Risk: Installation instructions use unpinned packages.

Mitigation: Review package sources and pin versions before installing.

Risk: Security analysis is incomplete because some references did not resolve.

Mitigation: Review the full source and unresolved references before deployment.

## Reference(s):

- [Project homepage (declared in Clawdis metadata)](https://github.com/vargHQ/skills/tree/main/ecommerce-video-edit)
- [Varg ecommerce video editing guide](https://varg.ai/how-to/skills/ecommerce-video-edit)

## Skill Output:

**Output Type(s):** [Video files, Image files, Shell commands, Guidance]

**Output Format:** [MP4 video files, a JPEG cover frame, and Markdown guidance with inline Bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One 9:16 MP4 per hook, an optional 4:5 feed cut, and a cover frame.]

## Skill Version(s):

1.0.6 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
