## Description:

Creates HeyGen AI avatar videos with controlled avatars, voices, scripts, backgrounds, captions, assets, and status workflows using HeyGen's v3 API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[michaelwang11394](https://clawhub.ai/user/michaelwang11394)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content production teams use this skill to select HeyGen avatars and voices, draft scripts, generate avatar or photo-avatar videos, manage backgrounds, captions, templates, and assets, and poll or receive completion events.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may use a HeyGen API key and send selected scripts, photos, images, video, or audio to HeyGen.

Mitigation: Install only where that data sharing is acceptable, scope access to the required HeyGen account, and keep HEYGEN_API_KEY out of prompts, logs, and generated artifacts.

Risk: Examples can upload local or fetched media content.

Mitigation: Require explicit confirmation before uploads and restrict upload inputs to a known media folder.

Risk: Webhook examples may be unsafe if copied directly into production.

Mitigation: Add strong signature verification on the raw request body, replay protection, and rate limits before production use.

Risk: The skill includes deletion and account-video management workflows.

Mitigation: Require confirmation before delete operations and verify the target video ID belongs to the intended project.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/michaelwang11394/skills/avatar-video)
- [HeyGen Create an Avatar Video API](https://docs.heygen.com/reference/create-an-avatar-video)
- [Skill Definition](SKILL.md)
- [Video Generation](references/video-generation.md)
- [Avatars](references/avatars.md)
- [Voices](references/voices.md)
- [Video Status](references/video-status.md)
- [Assets](references/assets.md)
- [Webhooks](references/webhooks.md)
- [Quota](references/quota.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with JSON payloads and curl, TypeScript, and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce HeyGen API request bodies, polling workflows, webhook handling guidance, and environment-variable setup guidance.]

## Skill Version(s):

2.23.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
