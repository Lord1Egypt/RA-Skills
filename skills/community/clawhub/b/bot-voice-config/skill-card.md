## Description:

Bot Voice Config Clean configures and binds Volcengine TTS voices for OpenClaw bots, including voice lookup, default voice selection, bot-specific binding, test audio generation, and optional Feishu delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaqzsd](https://clawhub.ai/user/kaqzsd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw bot operators use this skill to select, bind, test, and persist text-to-speech voice settings for bots that use Volcengine TTS and Feishu voice-message delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Volcengine and Feishu credentials.

Mitigation: Use least-privilege credentials, prefer environment variables, avoid storing real secrets in JSON configuration, and restrict local secret-file permissions.

Risk: Test operations may send generated audio and related request data to external Volcengine and Feishu services.

Mitigation: Run tests only with intended sample text and recipients, and confirm that external service use is acceptable for the deployment environment.

Risk: The skill persists bot voice settings in a local configuration file.

Mitigation: Review configuration contents before sharing systems or backups, and avoid running the script as root or on shared machines.

Risk: Temporary audio-file handling has avoidable weaknesses according to the security guidance.

Mitigation: Use the skill on trusted single-user machines until temporary-file handling is fixed, and remove generated audio files after testing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kaqzsd/skills/bot-voice-config)
- [Bundled Volcengine voice list](docs/yinse-liebiao.md)
- [Volcengine TTS documentation](https://www.volcengine.com/docs/6561/195562)
- [Volcengine voice list documentation](https://www.volcengine.com/docs/6561/1257544?lang=zh)
- [Feishu Open Platform](https://open.feishu.cn/document/home)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal-style text with shell command examples and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate MP3/Opus test audio and send it through Feishu when credentials are configured.]

## Skill Version(s):

1.1.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
