## Description:

抖音视频快速转文字 helps an agent extract audio from Douyin links or local video files and transcribe Chinese speech with a local Whisper workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[btboy773](https://clawhub.ai/user/btboy773)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to convert Douyin share links or local video files into Chinese transcript text. It is suited for local transcription workflows where users can install Python, ffmpeg, openai-whisper, and the Douyin MCP dependency.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security review flags command-injection risk when processing untrusted links or filenames.

Mitigation: Use trusted inputs in an isolated environment until the script is updated to pass structured subprocess arguments instead of shell commands.

Risk: The server security review flags misleading privacy and offline claims because Douyin/MCP parsing and media download steps can make external requests.

Mitigation: Review network behavior before processing sensitive media, and do not rely on offline or privacy claims for Douyin-link workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/btboy773/skills/douyin-transcribe-fast)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and transcript text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write transcript .txt files under the configured local output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
