## Description:

Helps an agent reply to Feishu voice messages by using Feishu transcripts and generating audio replies through MiniMax T2A with Edge TTS fallback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[michelangelo-in-sistine](https://clawhub.ai/user/michelangelo-in-sistine)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Feishu automation users can use this skill to turn incoming Feishu voice content into transcript-driven voice replies. It is intended for workflows that need a generated audio response file and a Feishu message command using audio/opus content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reply text may be sent to MiniMax or Edge TTS providers for speech synthesis.

Mitigation: Avoid secrets or sensitive conversation content unless the selected provider and account terms meet the deployment's privacy requirements.

Risk: Generated audio is written to local media and temporary paths that may retain message content.

Mitigation: Restrict access to generated media paths and clear retained audio files according to local data-retention requirements.

Risk: The MiniMax path depends on provider credentials, network access, and ffmpeg for opus conversion.

Mitigation: Verify MINIMAX_API_KEY, ffmpeg availability, and Edge TTS fallback behavior before using the skill in a live Feishu workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/michelangelo-in-sistine/skills/feishu-minimax-t2a-voice)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell-command examples and generated audio file paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce .opus or .ogg audio files and falls back to text when speech synthesis fails.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
