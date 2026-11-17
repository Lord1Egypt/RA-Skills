## Description:

Generate videos using Flyworks (a.k.a HiFly) Digital Humans by creating talking photo videos from images, using public avatars with TTS, or cloning voices for custom audio.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linhui99](https://clawhub.ai/user/linhui99)

### License/Terms of Use:

MIT

## Use Case:

Developers, creators, and external agent users use this skill to generate avatar videos from text, audio, or portrait images with Flyworks/HiFly, including public avatars and cloned voices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Face images, voice samples, prompts, and generated media may be sent to Flyworks/HiFly infrastructure.

Mitigation: Use only media the user owns or has explicit permission to use, disclose the third-party upload, and avoid sensitive content unless account terms and privacy handling are approved.

Risk: Voice cloning can be used to imitate real people.

Mitigation: Require explicit consent for cloned voices and avoid generating content that misleads viewers about identity or authorization.

Risk: The shared demo token has watermark and duration limits and may have unclear quota or account impact.

Mitigation: Prefer a user-owned HIFLY_API_TOKEN in an isolated project environment after reviewing account, quota, and billing implications.

## Reference(s):

- [Authentication](artifact/references/authentication.md)
- [Avatars](artifact/references/avatars.md)
- [Video Generation](artifact/references/video-generation.md)
- [Voices](artifact/references/voices.md)
- [Flyworks](https://flyworks.ai)
- [HiFly](https://hifly.cc)
- [Flyworks/HiFly API Base URL](https://hfw-api.hifly.cc/api/v2/hifly)
- [ClawHub Skill Page](https://clawhub.ai/linhui99/skills/flyworks-avatar-video)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and CLI text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return task IDs, avatar or voice IDs, and video URLs after asynchronous polling.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
