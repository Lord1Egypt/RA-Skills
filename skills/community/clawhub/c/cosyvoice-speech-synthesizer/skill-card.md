## Description: <br>
Converts user-provided text into speech with CosyVoice, including voice, dialect, emotion, role, rate, pitch, volume, and output format controls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[songguocola](https://clawhub.ai/user/songguocola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content creators use this skill to generate narration, dubbing, podcast, announcement, and audiobook audio from text through Alibaba Cloud DashScope CosyVoice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text submitted for synthesis is sent to Alibaba Cloud DashScope using the user's API key. <br>
Mitigation: Avoid submitting secrets, private messages, regulated data, or confidential business text unless the provider's data terms are acceptable. <br>
Risk: The skill depends on a DashScope API key and downloads generated audio to local files. <br>
Mitigation: Use a dedicated or scoped key where possible and review the output path and generated audio before sharing or retaining it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/songguocola/cosyvoice-speech-synthesizer) <br>
- [Alibaba Cloud CosyVoice voice list](https://help.aliyun.com/zh/model-studio/cosyvoice-voice-list) <br>
- [DashScope SpeechSynthesizer endpoint](https://dashscope.aliyuncs.com/api/v1/services/audio/tts/SpeechSynthesizer) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, API calls, Files, Text] <br>
**Output Format:** [Command-line text plus generated audio files in WAV, MP3, PCM, or Opus formats.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DASHSCOPE_API_KEY and writes the synthesized audio to the requested output path.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
