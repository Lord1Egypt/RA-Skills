## Description:

AI Animation Studio helps an agent turn stories into storyboarded, styled animation workflows with image/video generation prompts, voiceover, burned-in subtitles, BGM selection, and final video assembly steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[systiger](https://clawhub.ai/user/systiger)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and developers use this skill to plan and automate short animated videos from story input, including scene breakdowns, style prompts, cloud image/video generation, voiceover, subtitles, BGM, and video composition. It is most useful when an agent is helping produce social-video or story-animation assets with local media tooling and configured cloud services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Story text, prompts, and generated media may be sent to Volcengine/Doubao or edge-tts services.

Mitigation: Avoid private stories, proprietary prompts, and sensitive media unless the deployment has approved those services and their data handling terms.

Risk: The workflow runs local ffmpeg processing on downloaded or generated media.

Mitigation: Run in a constrained workspace with reviewed inputs and a maintained ffmpeg installation.

Risk: Generated files can be written or overwritten in configured output locations.

Mitigation: Use a dedicated output directory and review paths before running full animation workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/systiger/skills/ai-animation-choose)
- [Publisher profile](https://clawhub.ai/user/systiger)
- [Artifact skill documentation](artifact/SKILL.md)
- [BGM library](artifact/BGM_LIBRARY.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python code, JSON scene data, shell commands, and generated media file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may reference local media paths and cloud-generated image or video URLs before final media files are assembled.]

## Skill Version(s):

2.2.0 (source: server release metadata and artifact documentation, released 2026-03-29)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
