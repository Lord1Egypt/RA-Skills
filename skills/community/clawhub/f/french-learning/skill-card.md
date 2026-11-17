## Description:

French Learning automates French vocabulary processing by formatting sheet data with translations and examples, generating ElevenLabs audio, and uploading MP3 batches to Google Drive.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clairproqc-star](https://clawhub.ai/user/clairproqc-star)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and language-learning content creators use this skill to turn French vocabulary rows in Google Sheets into translated practice materials and batched French example-sentence audio.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses Google and AI service credentials to read, clear, rewrite, and upload cloud data.

Mitigation: Use dedicated or tightly scoped credentials, confirm the fixed Sheet and Drive IDs before running, and keep backups or confirmation steps for cloud writes.

Risk: Vocabulary and example sentence content may be sent to Gemini and ElevenLabs during translation and audio generation.

Mitigation: Avoid sensitive source sheets and review generated translations, examples, and audio before using them in learning materials.

Risk: Temporary files and fixed paths can expose or overwrite intermediate output if the runtime is shared.

Mitigation: Run in an isolated workspace and add temp-file handling or path validation before processing sensitive data.

## Reference(s):

- [French Learning configuration](references/config.md)
- [ClawHub skill page](https://clawhub.ai/clairproqc-star/skills/french-learning)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration instructions]

**Output Format:** [Google Sheet rows and MP3 audio files, with JSON status messages from scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Gemini, ElevenLabs, Google Sheets, and Google Drive CLI credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
