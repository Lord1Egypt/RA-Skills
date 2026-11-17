## Description:

Auto-Talk-TTS speaks assistant responses aloud using edge-tts and can install node-edge-tts if needed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stefanochiodino](https://clawhub.ai/user/stefanochiodino)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to have an agent speak generated responses aloud through Microsoft Edge neural TTS while the text conversation continues without waiting for audio playback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill attempts to speak every assistant response aloud and can make that behavior automatic and persistent.

Mitigation: Use only when automatic speech is intended, and keep the behavior opt-in, locally scoped, and easy to disable.

Risk: Assistant response text may be sent to an external TTS provider.

Mitigation: Avoid using the skill for sensitive chats, credentials, private code, or shared spaces unless external TTS use is acceptable.

Risk: The security guidance calls for review of dependency installation and missing executable packaging before installation.

Mitigation: Review the package before installing, require the expected executable to be present, and prefer pinned local dependencies over automatic global installation.

## Reference(s):

- [Auto-Talk-TTS ClawHub Skill Page](https://clawhub.ai/stefanochiodino/skills/auto-talk-tts)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May play generated speech asynchronously and may send assistant response text to an external TTS provider.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
