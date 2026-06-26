## Description: <br>
Drema interprets dream descriptions through traditional Zhougong dream symbolism and psychology, with dream history, calendar, reporting, fortune, TTS, and image-generation flows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bonniesilva](https://clawhub.ai/user/bonniesilva) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to analyze dreams, save dream records, review patterns, generate calendar or monthly summaries, request fortune-style interpretations, and optionally create spoken or visual dream outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive dream descriptions may be saved locally and later summarized. <br>
Mitigation: Use only with consent for local dream history; add opt-in storage, deletion, and retention controls before broad deployment. <br>
Risk: The image-generation path includes a hardcoded API key and reconstructs a script for execution. <br>
Mitigation: Remove embedded credentials, require environment-based secrets, and review or disable script execution before installation. <br>
Risk: TTS and image-generation features may send dream content or prompts to third-party providers. <br>
Mitigation: Avoid these features for sensitive dreams unless users accept provider processing, and document the configured providers. <br>
Risk: The supplied security verdict is suspicious. <br>
Mitigation: Review the skill before installing and scan any modified release before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bonniesilva/dreaminterpreter) <br>
- [DashScope](https://dashscope.aliyun.com) <br>
- [OpenAI platform](https://platform.openai.com) <br>
- [ElevenLabs](https://elevenlabs.io) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, code, shell commands, configuration, files] <br>
**Output Format:** [Markdown-style chat responses with optional JSON dream records, shell commands, Python snippets, and generated image file paths.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May store dream records locally and may call configured TTS or image-generation providers.] <br>

## Skill Version(s): <br>
1.4.3 (source: server release evidence and clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
