## Description:

Guides agents in creating lyrics and songs, editing music, cloning consented voices, separating stems, and exporting results through a third-party music API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[2253128](https://clawhub.ai/user/2253128)

### License/Terms of Use:

MIT

## Use Case:

Creators and developers use this skill to plan and run music-generation, lyric-writing, cover, voice, stem-separation, and export workflows for songs and media soundtracks. A user-supplied API key and paid third-party service are required.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid third-party requests require an API key and may incur charges.

Mitigation: Use your own key, verify the API host and costs before calling it, and keep credentials out of logs and shared commands.

Risk: Uploading or transforming recordings may expose copyrighted audio or personal voice data.

Mitigation: Only submit audio you have rights and consent to process, and avoid voice cloning for impersonation or deception.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/2253128/skills/ai-music-studio)
- [Getting started and API key setup](references/getting-started.md)
- [Music creation API](references/api-create.md)
- [Lyrics and style API](references/api-lyrics.md)
- [Voice and audio API](references/api-voice.md)
- [Export API](references/api-export.md)
- [Third-party API service](https://api.a7w.cn/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Code, Guidance]

**Output Format:** [Markdown instructions and commands; API responses may contain JSON task IDs and media links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Music files are generated or exported by the external API, not by the skill itself.]

## Skill Version(s):

1.0.1 (source: release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
