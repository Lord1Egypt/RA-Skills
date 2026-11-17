## Description:

Creates a single English-then-Arabic digital-human spokesperson video from supplied copy, with voiceover, subtitles, and AI-content labels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arronjack](https://clawhub.ai/user/arronjack)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, educators, and marketing teams use this skill to turn English copy, optionally paired with Arabic copy, into a bilingual presenter video for English- and Arabic-speaking audiences.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud lip-sync services may receive avatar images and voice audio.

Mitigation: Use local SadTalker or the fallback for sensitive media; use cloud services only when sharing those assets is acceptable.

Risk: HeyGen requires publicly accessible image and audio URLs.

Mitigation: Review public hosting and access before supplying media URLs.

Risk: Local rendering requires ffmpeg and may involve large third-party dependencies.

Mitigation: Review the installation and resource requirements before running the local pipeline.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/arronjack/skills/digital-human-spokesperson)
- [Bilingual digital-human pipeline](references/pipeline.md)
- [SadTalker local lip-sync engine](https://github.com/vinthony/SadTalker)

## Skill Output:

**Output Type(s):** [Video files, Text guidance, Shell commands]

**Output Format:** [MP4 video and a brief text summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [English segment followed by Arabic, with subtitles and AI-content labels by default; fallback video does not provide precise lip-sync.]

## Skill Version(s):

1.1.0 (source: skill frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
