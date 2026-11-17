## Description:

Sends Feishu voice messages by converting text or existing audio into opus audio and delivering it through the Feishu Open API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[michael-c-matias](https://clawhub.ai/user/michael-c-matias)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to generate or convert audio and send it as a Feishu voice message to a known open_id recipient from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Feishu app credentials, recipient open_id, message text, and audio are sensitive and are used with external services.

Mitigation: Use environment variables or tightly permissioned config files, limit Feishu app permissions, and send only content approved for the configured Feishu and TTS providers.

Risk: Temporary audio files are created during conversion, and the security guidance cautions against shared hosts unless temporary-file handling is improved.

Mitigation: Run on trusted single-user hosts or improve temporary-file isolation before shared-host deployment.

Risk: Text-to-speech behavior depends on edge-tts and the configured TTS provider.

Mitigation: Use a virtual environment with a pinned edge-tts version and validate generated audio before operational use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/michael-c-matias/skills/feishu-audio-messages)
- [Publisher profile](https://clawhub.ai/user/michael-c-matias)
- [Feishu file upload API endpoint](https://open.feishu.cn/open-apis/im/v1/files)
- [Feishu message send API endpoint](https://open.feishu.cn/open-apis/im/v1/messages)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command examples and configuration instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Feishu app credentials, a recipient open_id, edge-tts, ffmpeg, and curl at execution time.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
