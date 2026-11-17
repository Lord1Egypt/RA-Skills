## Description:

Automated video editing skill for talk/vlog/standup videos, including cutting, sentence-level splitting, clip merging, audio extraction, transcription, subtitles, cover generation, B-roll replacement, overlays, background music, and Remotion voiceover video generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maxazure](https://clawhub.ai/user/maxazure)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, developers, and agent users use this skill to turn talk, vlog, standup, podcast, or voiceover media into edited videos with transcripts, selected clips, subtitles, covers, B-roll, overlays, and final render commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read and index local project media and write generated media, transcripts, and index files.

Mitigation: Run it in a project-scoped workspace and review generated files before sharing or committing them.

Risk: The workflow may install external dependencies and download speech models or fonts.

Mitigation: Use pinned dependencies and lockfiles where possible, and approve model or font downloads before first use.

Risk: Troubleshooting guidance includes sudo and PPA package installation commands.

Mitigation: Avoid privileged package commands unless the source and system impact are trusted.

Risk: Cover generation may involve remote font use or Chrome sandbox changes.

Mitigation: Prefer local fonts and keep browser sandboxing enabled unless the environment has been reviewed.

Risk: One generated techcard cover style may include unwanted OpenClaw branding.

Mitigation: Review generated covers before publication and adjust the style or assets when branding is inappropriate.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/maxazure/skills/auto-video-editor)
- [README](artifact/README.md)
- [Remotion Voiceover Integration Guide](artifact/REMOTION_VOICEOVER.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON configuration examples and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces or edits local media workflow files such as transcripts, render_config.json, timeline JSON, thumbnails, and rendered video outputs through helper scripts.]

## Skill Version(s):

2.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
