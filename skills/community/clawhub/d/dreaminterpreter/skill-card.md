## Description:

Drema interprets user-described dreams with traditional Zhougong symbolism and psychological analysis, plus dream history, calendar/report, fortune, TTS, and image-generation interactions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bonniesilva](https://clawhub.ai/user/bonniesilva)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to record and interpret dream descriptions, combining traditional dream symbolism with psychological framing. It can also generate fortune summaries, dream-history views, TTS prompts, and image-generation prompts around those dream records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dream descriptions may be sensitive and are saved locally, with optional flows that may send content to external TTS or image services.

Mitigation: Require explicit user consent before storing or transmitting dream content, and provide clear retention, delete, and export controls.

Risk: The artifact includes image-generation commands with an exposed API key.

Mitigation: Remove and rotate the exposed key, and require secret values to come from user-managed environment variables or a secure secret store.

Risk: The artifact directs agents to execute or recreate scripts from /tmp and uses unpinned dependencies.

Mitigation: Avoid running scripts from /tmp, review generated commands before execution, and pin dependencies before installation or use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bonniesilva/skills/dreaminterpreter)
- [DashScope](https://dashscope.aliyun.com)
- [OpenAI Platform](https://platform.openai.com)
- [ElevenLabs](https://elevenlabs.io)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown-style text with button payloads and occasional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May store dream records locally and may involve external TTS or image services when those options are used.]

## Skill Version(s):

1.4.3 (source: server release metadata and artifact/clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
