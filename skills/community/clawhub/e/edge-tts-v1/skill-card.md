## Description: <br>
Text-to-speech conversion using node-edge-tts for generating audio from text with support for multiple voices, languages, speed adjustment, pitch control, and subtitle generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[onlyloveher](https://clawhub.ai/user/onlyloveher) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to convert requested text, summaries, or messages into spoken audio with configurable voice, language, rate, pitch, volume, output format, and optional subtitles. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Converted text is sent to Microsoft Edge's online TTS service. <br>
Mitigation: Avoid converting secrets or highly sensitive personal data. <br>
Risk: Generated audio, subtitle, and configuration files may remain on local disk. <br>
Mitigation: Clean generated files and stored preferences when retention is not desired. <br>
Risk: Installation uses npm dependencies. <br>
Mitigation: Review dependency installation in the target environment before deployment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/onlyloveher/edge-tts-v1) <br>
- [node-edge-tts Reference](references/node_edge_tts_guide.md) <br>
- [Voice testing service](https://tts.travisvn.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline JavaScript and shell command examples; generated agent workflows may produce MP3 audio files and optional JSON subtitle files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled scripts send text to Microsoft Edge's online TTS service, can save persistent preferences in a local JSON config file, and can write generated audio/subtitle files to a temp or user-specified path.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
