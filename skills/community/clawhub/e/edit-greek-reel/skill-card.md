## Description:

Edit a raw talking-head video into a polished short-form reel with Greek karaoke subtitles, silence trimming, Manrope Bold subtitles, zoom effects, SFX, and image overlays.

This skill is ready for commercial/non-commercial use.

## Publisher:

[artemisln](https://clawhub.ai/user/artemisln)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators and video editors use this skill in Claude Code to transform raw Greek talking-head footage into vertical Instagram/TikTok reels with subtitles, tight cuts, zooms, image overlays, and sound effects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing required Python packages can introduce dependency and environment risk.

Mitigation: Install dependencies in a dedicated virtual environment and review or pin openai-whisper, Pillow, and cairosvg before use.

Risk: Input audio, generated transcripts, and processed videos may contain sensitive personal or business content.

Mitigation: Run the skill only on videos whose audio and generated transcript can be stored in the video directory, and remove temporary files when no longer needed.

Risk: Greek transcription and brand-name recognition can be incorrect, which may burn misleading subtitles into the final video.

Mitigation: Proofread the transcript before rendering subtitles and ask the user about uncertain words or use the manual text option for exact wording.

## Reference(s):

- [Greek Reel Video Editor Skill Page](https://clawhub.ai/artemisln/skills/edit-greek-reel)
- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code)
- [Manrope Font](https://fonts.google.com/specimen/Manrope)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration, Files]

**Output Format:** [Markdown guidance with inline shell and Python code blocks; media files are produced when the generated workflow is executed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces an edited MP4, transcript JSON, and temporary media-processing files in or near the input video directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
