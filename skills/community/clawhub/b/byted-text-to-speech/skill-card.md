## Description: <br>
Converts text into speech using the Volcengine Doubao speech synthesis API, with streaming synthesis, voice selection, speech controls, Markdown filtering, and LaTeX reading support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[volcengine-skills](https://clawhub.ai/user/volcengine-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to synthesize playable speech audio from text for narration, read-aloud workflows, voiceovers, announcements, or document listening. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends synthesis text to Volcengine/ByteDance for text-to-speech processing. <br>
Mitigation: Use it only for text that is appropriate to send to that provider, and avoid submitting sensitive or regulated content unless the deployment has approved that data flow. <br>
Risk: The skill can use ARK_SKILL_API_KEY and ARK_SKILL_API_BASE to list or create speech API keys and may save a retrieved key locally. <br>
Mitigation: Prefer manually setting MODEL_SPEECH_API_KEY, do not expose broader ARK credentials unless key management is intended, and inspect scripts/.env or rotate keys if one appears unexpectedly. <br>


## Reference(s): <br>
- [Byted Text To Speech on ClawHub](https://clawhub.ai/volcengine-skills/byted-text-to-speech) <br>
- [Volcengine Doubao Speech Product Overview](https://www.volcengine.com/docs/6561/1257543) <br>
- [HTTP Chunked/SSE Unidirectional Streaming V3](https://www.volcengine.com/docs/6561/1598757) <br>
- [Voice List](https://www.volcengine.com/docs/6561/1257544) <br>
- [API Key Management](https://console.volcengine.com/speech/new/setting/apikeys) <br>
- [Setup Guide](references/setup-guide.md) <br>
- [Documentation Index](references/docs-index.md) <br>


## Skill Output: <br>
**Output Type(s):** [Files, JSON, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [JSON status output with a local audio file path, plus Markdown guidance and shell commands when setup is needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local audio files in mp3, pcm, or ogg_opus format; requires MODEL_SPEECH_API_KEY or intentionally provided ARK_SKILL_API_KEY and ARK_SKILL_API_BASE credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
