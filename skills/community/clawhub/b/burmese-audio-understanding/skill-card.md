## Description:

High-accuracy Burmese audio transcription using Gemini 3.1 Flash Preview.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thelapyae](https://clawhub.ai/user/thelapyae)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to transcribe Burmese voice notes or speech recordings into Burmese text with their own Google Gemini API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected audio files are sent to Google Gemini for transcription.

Mitigation: Use the skill only for recordings whose transfer to Google Gemini is acceptable under the user's API terms and data-handling requirements.

Risk: Remote file deletion occurs after successful transcription and may not run on failure paths.

Mitigation: Avoid highly sensitive recordings until cleanup is moved into a finally block and failure-path deletion is verified.

Risk: Dependency ranges may resolve to newer SDK versions with changed behavior.

Mitigation: Pin and review dependency versions before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thelapyae/skills/burmese-audio-understanding)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration]

**Output Format:** [Plain text transcription with setup and execution guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GEMINI_API_KEY and a local audio file path; the script uploads the selected audio file to Google Gemini and prints only the transcription.]

## Skill Version(s):

1.2.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
