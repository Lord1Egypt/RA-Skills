## Description:

Daily Review Manager records and organizes daily reflection text or voice input into Markdown, with reminders and weekly or monthly summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hongyegege](https://clawhub.ai/user/hongyegege)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to capture personal or work daily reviews, preserve the original tone, and turn entries into structured Markdown journals, weekly reports, and monthly reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive personal or work reflections may be captured from text or voice and saved to a workspace Markdown file.

Mitigation: Use explicit confirmation before transcription or saving, keep storage local unless cloud storage is intentionally authorized, and review generated entries before retaining or sharing them.

Risk: Loose trigger phrases and voice or messaging integrations may process unintended messages.

Mitigation: Require user confirmation for voice or message ingestion and limit enabled integrations to trusted channels.

Risk: Voice transcription dependencies may introduce privacy or supply-chain exposure.

Mitigation: Pin transcription dependencies in an isolated environment and install only after reviewing ffmpeg, python3, and Whisper usage.

## Reference(s):

- [Review template](artifact/references/review_template.md)
- [ClawHub skill page](https://clawhub.ai/hongyegege/skills/daily-review-manager)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown files and concise agent guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May append structured daily review entries to a workspace Markdown file and may require ffmpeg, python3, and a Whisper transcription dependency for voice input.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
