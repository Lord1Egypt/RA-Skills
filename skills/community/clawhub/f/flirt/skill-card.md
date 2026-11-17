## Description:

Automates scheduled romantic text and cloned-voice messages to Feishu and QQ, with configurable timing, probability, message library rotation, and Noiz TTS voice generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[william1hall](https://clawhub.ai/user/william1hall)

### License/Terms of Use:

MIT-0

## Use Case:

External users and automation builders use this skill to configure scheduled relationship-style messages, generate voice audio from a reference sample, and send the resulting text or audio through Feishu and QQ.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automated outbound messages can reach unintended recipients or continue after the user expects them to stop.

Mitigation: Review intended recipients before installation and add a simple disable path before enabling the scheduled job.

Risk: Voice cloning can misuse a person's voice sample.

Mitigation: Use only reference audio from people who have consented to voice cloning.

Risk: Plaintext Feishu credentials and broad file permissions can expose messaging access.

Mitigation: Do not store live secrets in the script, restrict file permissions, and avoid running the skill as root.

Risk: Unpinned TTS dependencies can change behavior across installs.

Mitigation: Pin the TTS dependency before deployment.

## Reference(s):

- [Skill release page](https://clawhub.ai/william1hall/skills/flirt)
- [Publisher profile](https://clawhub.ai/user/william1hall)
- [Noiz TTS skill repository](https://github.com/noizai/skills)
- [Example flirt message library](references/flirt_library.txt)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup instructions and operational shell commands; runtime behavior may create audio files, logs, and scheduled outbound messages.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
