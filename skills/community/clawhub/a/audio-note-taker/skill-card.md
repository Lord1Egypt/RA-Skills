## Description:

Audio Note Taker transcribes audio files with the OpenAI Whisper API and writes structured notes as Markdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[utopiabenben](https://clawhub.ai/user/utopiabenben)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers can use this skill to turn meeting, lecture, interview, or personal audio into a Markdown note file with a full transcript. Review outputs before relying on advertised speaker detection, summarization, or action-item extraction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected audio is sent to OpenAI-compatible transcription services and the transcript is saved on disk.

Mitigation: Use only approved audio, follow consent and data-handling requirements, and protect or delete generated transcript files as appropriate.

Risk: The release overstates speaker detection, summarization, and action-item extraction compared with the implemented behavior.

Mitigation: Treat those features as unavailable in this version and manually review generated notes before operational use.

Risk: The installer uses an unpinned openai package.

Mitigation: Install in an isolated environment and pin a vetted openai package version when deploying.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/utopiabenben/skills/audio-note-taker)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Markdown note file with transcript text and command-line status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OPENAI_API_KEY and sends selected audio to an OpenAI-compatible transcription service.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
