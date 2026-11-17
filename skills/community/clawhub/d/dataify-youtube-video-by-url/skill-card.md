## Description:

Download or collect a YouTube video media file from a known video URL. Do not use for metadata, comments, transcripts, channel profiles, or keyword-based video discovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dataify-server](https://clawhub.ai/user/dataify-server)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to submit Dataify Builder jobs for YouTube video file collection from known YouTube video URLs and receive the final collected result after asynchronous task monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports unsafe credential-handling ambiguity and an unaudited external Python module path that can receive the user's API token.

Mitigation: Configure DATAIFY_API_TOKEN locally, do not paste tokens into chat, rotate any token previously shared in conversation, and install or run the package only when the Dataify service and local skill package environment are trusted.

Risk: Running the script may submit paid or quota-consuming Dataify jobs and retrieve results automatically.

Mitigation: Confirm the requested URL scope before execution, preserve task IDs for resume flows, and use explicit no-wait behavior when only task submission is intended.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dataify-server/skills/dataify-youtube-video-by-url)
- [Dataify Builder endpoint](https://scraperapi.dataify.com/builder?platform=1)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance and shell commands, with JSON task summaries and collected results when the Dataify task succeeds.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May submit quota-consuming Dataify jobs, monitor asynchronous task status, and retrieve final results unless no-wait behavior is requested.]

## Skill Version(s):

1.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
