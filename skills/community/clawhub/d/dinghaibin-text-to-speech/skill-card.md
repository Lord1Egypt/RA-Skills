## Description:

Convert text to speech audio files. Use when user needs to create audio from text, generate voiceovers, create podcasts, or convert articles to audio.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content creators use this skill to convert supplied text into speech audio files for voiceovers, podcasts, articles, and multilingual audio workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted text may be sent to an external text-to-speech provider.

Mitigation: Review the text before conversion and avoid confidential, regulated, personal, or secret content unless an acceptable backend and data-handling path are verified.

Risk: The skill writes audio files to user-selected output paths.

Mitigation: Keep output paths inside a trusted working directory and review generated files before sharing or publishing them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dinghaibin/skills/dinghaibin-text-to-speech)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Guidance]

**Output Format:** [Markdown with inline shell commands and generated audio files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write MP3 output files to a user-specified path; macOS fallback may write AIFF output.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
