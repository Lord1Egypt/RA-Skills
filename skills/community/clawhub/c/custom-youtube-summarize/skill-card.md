## Description:

Extract transcript from a YouTube video using Python and summarize it.

This skill is ready for commercial/non-commercial use.

## Publisher:

[5eun](https://clawhub.ai/user/5eun)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to fetch available YouTube subtitles from a provided video URL and produce an LLM-generated summary of the transcript.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts YouTube for the requested video and sends the resulting transcript into the LLM for summarization.

Mitigation: Use it only for videos where that data flow is acceptable, and avoid private or sensitive video content.

Risk: The skill may fail or return an error when a URL is invalid, transcripts are disabled, or no supported Korean or English transcript is available.

Mitigation: Check that the video URL is a supported YouTube URL and that the video has an available transcript before relying on the output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/5eun/skills/custom-youtube-summarize)
- [Publisher profile](https://clawhub.ai/user/5eun)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with transcript text and a summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The script prints transcript delimiters and returns errors when a URL is invalid or no transcript is available.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
