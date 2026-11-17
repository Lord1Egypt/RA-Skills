## Description:

China Tts helps agents generate text-to-speech audio through the SiliconFlow API for China-accessible Chinese, multilingual, dialect, emotional, dual-speaker, and custom voice-cloning workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobewin](https://clawhub.ai/user/tobewin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent users use this skill to turn text into saved audio files with SiliconFlow models, including article narration, emotional or dialect speech, podcast-style dual-speaker dialogue, and approved custom voice cloning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Text, reference voice recordings, cloned voice URIs, and generated audio are sent to or handled through SiliconFlow.

Mitigation: Use the skill only when the user is comfortable sharing that data with SiliconFlow, avoid secrets or regulated data, and treat API keys and cloned voice URIs as sensitive.

Risk: The voice-cloning workflow can upload sensitive voice samples without clear consent, privacy, or retention safeguards.

Mitigation: Only clone voices the user owns or has explicit permission to use, keep reference audio under the documented limits, and delete custom voices or generated audio when no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tobewin/skills/china-tts)
- [Usage examples](references/examples.md)
- [Voice list](references/voices.md)
- [SiliconCloud online voice preview](https://soundcloud.com/siliconcloud/sets/siliconcloud-online-voice)
- [SiliconFlow speech API endpoint](https://api.siliconflow.cn/v1/audio/speech)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with bash curl commands and generated audio files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and SILICONFLOW_API_KEY; generated audio is saved as timestamped MP3 or another requested audio format.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter states 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
