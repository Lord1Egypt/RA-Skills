## Description:

Create a verbatim transcript for a YouTube URL using Google Gemini, with speaker labels and paragraph breaks but no time codes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[odrobnik](https://clawhub.ai/user/odrobnik)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to generate clean transcript documents from YouTube URLs through Google Gemini. It is intended for cases where a readable transcript without timestamps is needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends the YouTube URL or video reference to Google Gemini using the configured Gemini API key.

Mitigation: Install and run it only when that external processing is acceptable for the video and account being used.

Risk: Transcript files are written locally and may contain sensitive or copyrighted content from the source video.

Mitigation: Review generated files before sharing them and store them only in approved workspace or temporary locations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/odrobnik/skills/gemini-yt-video-transcript)
- [Google AI Studio API keys](https://aistudio.google.com/apikey)

## Skill Output:

**Output Type(s):** [Text, Files, Shell commands]

**Output Format:** [Plain text transcript file with the video title followed by speaker-labeled transcript lines]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GEMINI_API_KEY and python3; default output is written under the workspace out folder, while custom output paths are constrained to workspace or temporary directories.]

## Skill Version(s):

1.0.4 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
