## Description:

Creates a daily spoken quotation using a selected voice, combines it with optional cover or avatar video media, and sends the resulting media to the configured recipient.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daaab](https://clawhub.ai/user/daaab)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to automate a daily inspirational voice quote workflow, including quote selection, voice generation, media formatting, and delivery through a configured messaging channel.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses cloned-voice media and personal photo or avatar material.

Mitigation: Run it only with explicit consent for the voice and image material, and limit access to the workspace and generated media.

Risk: The workflow depends on ElevenLabs, LINE, optional HeyGen or Gemini credentials, and public media URLs.

Mitigation: Use narrowly scoped tokens, avoid printing secrets, rotate credentials when exposed, and prefer short-lived signed URLs with unguessable names.

Risk: Scheduled sends can deliver media to the wrong recipient or at the wrong cadence if configuration is incorrect.

Mitigation: Confirm recipient IDs, hosting URLs, and cron configuration with a test run before enabling recurring execution.

Risk: The required sag executable is identified as an unpinned dependency.

Mitigation: Pin or verify the dependency source before installation and review updates before use.

## Reference(s):

- [Daily Voice Quote ClawHub listing](https://clawhub.ai/daaab/skills/daily-voice-quote)
- [Publisher profile](https://clawhub.ai/user/daaab)
- [Holiday and special-date reference](references/holidays.md)
- [Quotation reference pool](references/quotes.md)
- [ElevenLabs voice setup](https://try.elevenlabs.io/clawhub)
- [HeyGen avatar video setup](https://www.heygen.com/?sid=rewardful&via=clawhub)
- [Google AI Studio for optional image generation](https://aistudio.google.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces or guides creation of audio files, static video files, optional avatar video, captions, and messaging payloads.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
