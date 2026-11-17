## Description:

Helps agents create narrated MP4 presentation videos from slide scripts by generating slide images, Edge TTS narration, and ffmpeg-composed video.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openclawzhangchong](https://clawhub.ai/user/openclawzhangchong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, and operations teams can use this skill to turn structured presentation scripts into narrated training, reporting, tutorial, or product-demo videos. It is most useful when an agent should produce concrete media artifacts through repeatable command-line steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: HTML-template mode can render hardcoded branded or sample slide content instead of the user's actual content.

Mitigation: Review and fix the HTML templates before using that mode, and inspect generated slides before publishing the video.

Risk: Normal use may install Playwright and Chromium and modify the active Python environment.

Mitigation: Run the skill in an isolated virtual environment or container and review dependency installation before execution.

Risk: Narration text is sent to Edge TTS during audio generation.

Mitigation: Avoid sensitive or confidential narration text unless use of that service is approved for the content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/openclawzhangchong/skills/free-mp4-pptzc)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Files]

**Output Format:** [Markdown guidance with inline shell commands and generated media files such as PNG slide images, MP3 narration, and MP4 video.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local Python scripts, Edge TTS for narration, ffmpeg for video assembly, and optional Playwright/Chromium for HTML-template slide rendering.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
