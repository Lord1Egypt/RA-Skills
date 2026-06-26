## Description: <br>
Converts text to natural-sounding speech audio files through the Coze API, with multiple voices and mp3, ogg_opus, wav, or pcm output formats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[franklu0819-lang](https://clawhub.ai/user/franklu0819-lang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content teams use this skill to generate speech audio from text for notifications, greetings, messaging, and application workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text submitted for synthesis is sent to Coze under the user's COZE_API_KEY. <br>
Mitigation: Avoid submitting secrets, regulated data, or proprietary text unless the user's Coze terms and data handling requirements allow it; use a limited-purpose API key where possible. <br>
Risk: A user-selected output filename could overwrite an important local file. <br>
Mitigation: Choose explicit output paths carefully and avoid reusing filenames for files that should be preserved. <br>


## Reference(s): <br>
- [Coze TTS API Reference](references/coze_tts_api.md) <br>
- [Coze Audio Speech Documentation](https://www.coze.cn/docs/developer_guides/audio_speech) <br>
- [Coze Platform](https://www.coze.cn/) <br>
- [ClawHub Coze Tts Page](https://clawhub.ai/franklu0819-lang/coze-tts) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Configuration guidance] <br>
**Output Format:** [Command-line output plus local audio files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires COZE_API_KEY and jq; generated audio can be mp3, ogg_opus, wav, or pcm.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
