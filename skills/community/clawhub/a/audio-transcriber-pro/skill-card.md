## Description:

Audio Transcriber Pro transforms audio recordings into professional Markdown documentation with intelligent summaries using LLM integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bingze00000](https://clawhub.ai/user/bingze00000)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, knowledge workers, and teams use this skill to transcribe audio or video recordings into Markdown reports, meeting notes, action items, and summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Full transcript text may be sent to external AI tools when summary mode runs.

Mitigation: Use transcript-only or local processing for confidential audio, and enable LLM summary mode only when external processing is acceptable.

Risk: Dependency installation can add unpinned Python packages into the user's environment.

Mitigation: Review the installer first and prefer an isolated virtual environment before installing or running the transcription tooling.

## Reference(s):

- [Audio Transcriber Pro release page](https://clawhub.ai/bingze00000/skills/audio-transcriber-pro)
- [Transcription Tools Comparison](references/tools-comparison.md)
- [Claude CLI documentation](https://docs.anthropic.com/en/docs/claude-cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with terminal guidance and optional subtitle or structured data files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates timestamped transcript and summary files; summary mode may use Claude or GitHub Copilot CLI when available.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
