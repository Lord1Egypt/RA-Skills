## Description:

Generate images, videos, icons, audio, and more using Freepik's AI API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cohnen](https://clawhub.ai/user/cohnen)

### License/Terms of Use:

MIT

## Use Case:

Developers and external users use this skill to have an OpenClaw agent call Freepik's API for image generation, video generation, image editing, icon creation, audio generation, stock search, and related AI utilities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad curl permission could expose the Freepik API key if command matching is not strict.

Mitigation: Review before installation, prefer the ClawHub package or a pinned reviewed commit, and use a restricted or low-quota Freepik API key until the curl allowlist is tightened.

Risk: Prompts or private media URLs sent through the skill may be sensitive.

Mitigation: Avoid sending sensitive prompts or private media URLs unless the user has approved that use.

Risk: Generated media may remain in local session folders.

Mitigation: Periodically clean ~/.freepik/sessions when generated files no longer need to be retained.

## Reference(s):

- [Freepik API Docs](https://docs.freepik.com)
- [Freepik Developers Dashboard](https://www.freepik.com/developers/dashboard)
- [Freepik OpenClaw Skill Homepage](https://github.com/SqaaSSL/freepik-openclaw-skill)
- [Freepik API Models Reference](models-reference.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown with inline bash commands, API request examples, result URLs, and local generated media files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FREEPIK_API_KEY and may save generated media under ~/.freepik/sessions.]

## Skill Version(s):

1.0.5 (source: frontmatter, _meta.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
