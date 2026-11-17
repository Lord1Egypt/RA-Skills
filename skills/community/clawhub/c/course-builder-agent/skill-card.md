## Description:

Course Builder Agent turns text or existing course content into slide-based course videos with narration, subtitles, optional digital-human handling, and FFmpeg video assembly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freeman88-tch](https://clawhub.ai/user/freeman88-tch)

### License/Terms of Use:

MIT-0

## Use Case:

External education content creators and developers use this skill to convert Markdown, text, or existing course content into Chinese slide videos with synthesized narration and subtitles. The optional digital-human flow is intended for environments where the required third-party tooling and consent controls are available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install command can alter the host Python environment and uses unpinned dependencies.

Mitigation: Install and test the skill in an isolated virtual environment or container, and review or pin dependencies before use.

Risk: The skill advertises digital-human and photo handling without clear privacy terms or consent controls in the evidence.

Mitigation: Avoid personal photos or sensitive media unless the publisher provides clear third-party privacy terms, consent controls, and data-handling expectations.

Risk: Some advertised digital-human or subtitle embedding behavior may not work as described.

Mitigation: Run a representative test workflow before relying on generated videos, and manually review final media for completeness and correctness.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/freeman88-tch/skills/course-builder-agent)
- [Skill definition](artifact/SKILL.md)
- [Skill manifest](artifact/claw.json)
- [Build script](artifact/scripts/build.py)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration, Guidance]

**Output Format:** [MP4 video, PNG slide images, MP3 audio, SRT subtitles, and Markdown or shell guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local ffmpeg, edge-tts, Pillow, and optional VideoCraft Pro or digital-human tooling; generated media depends on local environment and user-provided inputs.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
