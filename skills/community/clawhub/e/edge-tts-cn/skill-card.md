## Description: <br>
Text-to-speech conversion using the node-edge-tts npm package for generating audio from text with multiple voices, languages, speed adjustment, pitch control, and subtitle generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[onlyloveher](https://clawhub.ai/user/onlyloveher) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to convert requested text into spoken audio or MP3 files, including accessibility, multitasking, and customized voice output workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected text is sent to an online TTS provider. <br>
Mitigation: Use only with text appropriate for an external online TTS service and review privacy requirements before converting sensitive content. <br>
Risk: Persistent voice, proxy, and output preferences may remain in the user's TTS configuration file. <br>
Mitigation: Review or reset ~/.tts-config.json when changing environments or when persistent preferences are no longer desired. <br>
Risk: Standalone trigger words such as tts may be omitted from generated audio. <br>
Mitigation: Review the generated text and audio when exact narration is required. <br>


## Reference(s): <br>
- [node-edge-tts Reference](references/node_edge_tts_guide.md) <br>
- [Voice Testing](https://tts.travisvn.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline JavaScript and bash examples; generated audio is returned as media paths or MP3 files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can generate JSON subtitles and persistent TTS configuration when the bundled scripts are used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
