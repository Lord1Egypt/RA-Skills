## Description: <br>
根据主题自动生成多角色有声短剧，调用 SenseAudio TTS API 合成音频并拼接输出。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qwerty0205](https://clawhub.ai/user/qwerty0205) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn a short drama theme into a multi-character script, synthesize dialogue with SenseAudio TTS, and return the generated WAV file path plus script JSON. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated dialogue text is sent to SenseAudio for speech synthesis. <br>
Mitigation: Avoid including secrets, private business information, or sensitive personal data in prompts or scripts. <br>
Risk: The SenseAudio API key may be exposed if pasted into shared logs or transcripts. <br>
Mitigation: Prefer environment-variable configuration and avoid echoing or sharing the API key. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qwerty0205/generate-drama) <br>
- [Publisher profile](https://clawhub.ai/user/qwerty0205) <br>
- [SenseAudio](https://senseaudio.cn) <br>
- [README](artifact/README.md) <br>
- [Usage guide](artifact/USAGE.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with JSON script data, shell command examples, and generated WAV and script file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a SenseAudio API key and sends generated dialogue text to SenseAudio for speech synthesis.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release metadata; artifact frontmatter reports 1.1.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
