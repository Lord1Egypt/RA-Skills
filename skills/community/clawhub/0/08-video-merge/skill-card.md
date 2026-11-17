## Description:

Locally merges video clips, dubbing audio, SRT subtitles, and background music into a 9:16 vertical short video ready for publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ghwyever](https://clawhub.ai/user/ghwyever)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and automation developers use this skill to combine video, audio, and optional subtitles into a vertical short-video output for publishing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may report a completed video merge without creating a real merged output.

Mitigation: Treat final_video_url as untrusted until the referenced file exists, opens successfully, and contains the expected video, audio, and subtitle content.

## Reference(s):


## Skill Output:

**Output Type(s):** [text]

**Output Format:** [JSON object with final_video_url and status message]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports a local output path; evidence security review says no merged media is actually produced.]

## Skill Version(s):

1.0.3 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
