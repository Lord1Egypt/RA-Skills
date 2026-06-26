## Description: <br>
Automates video editing workflows for talk, vlog, and standup videos by extracting audio, transcribing speech, segmenting clips, generating subtitles and covers, composing selected clips, adding B-roll, overlays, end cards, BGM, and Remotion voiceover visuals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maxazure](https://clawhub.ai/user/maxazure) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, editors, and developers use this skill to turn local long-form or oral-presentation media into edited videos with transcripts, selected clips, subtitles, covers, B-roll, overlays, background music, and optional Remotion-generated visuals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes local videos and transcripts that may contain sensitive content. <br>
Mitigation: Keep sensitive footage in a dedicated project directory and avoid scanning broad folders. <br>
Risk: Generated media, indexes, and transcript edits may replace or affect existing project-local outputs. <br>
Mitigation: Back up important generated outputs and review transcript edits before confirming changes. <br>
Risk: The workflow may download models or fonts from external providers. <br>
Mitigation: Install only in environments where external downloads from the documented providers are acceptable. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/maxazure/auto-video-editor) <br>
- [README](README.md) <br>
- [Remotion Voiceover Integration Guide](REMOTION_VOICEOVER.md) <br>
- [Video Skill V2 Plan](docs/plans/2026-03-29-video-skill-v2.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces project-local media artifacts such as transcripts, indexes, cover images, subtitle files, clips, and rendered videos when the user runs the generated commands.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
