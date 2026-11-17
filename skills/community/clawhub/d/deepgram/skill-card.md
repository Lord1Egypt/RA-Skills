## Description:

Command-line guidance for using the Deepgram CLI to transcribe local files, remote audio URLs, stdin streams, and live microphone input.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nerkn](https://clawhub.ai/user/nerkn)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to install and authenticate the Deepgram CLI, run speech-to-text transcription jobs, and capture transcript output for scripts, search, summarization, or subtitle workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audio files, remote audio, stdin streams, or microphone input may be sent to Deepgram for transcription.

Mitigation: Use the skill only with audio that is allowed under the user's Deepgram account settings and applicable data handling obligations.

Risk: Authentication uses a Deepgram API key stored locally by the CLI.

Mitigation: Use a revocable, least-privilege API key and rotate it if the local environment is shared or compromised.

Risk: The documented install command uses a global npm package.

Mitigation: Prefer a pinned or isolated installation when possible and install only if the Deepgram CLI package is trusted.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces CLI usage patterns for JSON, text, SRT, and VTT transcript output.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
