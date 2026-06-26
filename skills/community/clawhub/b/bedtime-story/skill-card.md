## Description: <br>
Generates personalized multi-character Chinese bedtime stories, story state, and optional MP3 narration from a child's name, age, and interests using configured LLM and TTS services. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Delong-liu-bupt](https://clawhub.ai/user/Delong-liu-bupt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and caregivers use this skill to create customized Chinese bedtime stories and optional narration for a child based on profile details such as name, age, and interests. It supports single-episode generation and serialized continuation using saved story state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Child profile details and generated story text may be sent to configured LLM and TTS services. <br>
Mitigation: Use nicknames instead of real names, review provider privacy terms, and use text-only mode when TTS is not needed. <br>
Risk: Generated story text, story state, and audio files are saved locally and may persist on shared or backed-up machines. <br>
Mitigation: Periodically delete the local outputs directory and avoid storing sensitive child details in generated files. <br>


## Reference(s): <br>
- [Prompt templates](references/prompts_cn.md) <br>
- [State schema](references/state_schema_cn.md) <br>
- [ClawHub release page](https://clawhub.ai/Delong-liu-bupt/bedtime-story) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, audio, files, shell commands] <br>
**Output Format:** [Plain text story files, JSON state, optional MP3 audio, and terminal status output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports child name, age, interests, episode count, continuation mode, and no-TTS text-only mode.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
