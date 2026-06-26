## Description: <br>
Converts text into speech audio files through the Doubao/Volcengine TTS API, with support for official voices, cloned voice IDs, audio format settings, and emotion controls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jianjun156](https://clawhub.ai/user/jianjun156) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agent users use this skill to synthesize speech from provided text using Doubao/Volcengine voices, including preset voices and authorized cloned voice IDs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text sent for synthesis is transmitted to the Doubao/Volcengine cloud API. <br>
Mitigation: Use only text approved for that provider and avoid submitting sensitive or regulated content unless the deployment has the required agreements and controls. <br>
Risk: The skill requires a provider access token and app ID. <br>
Mitigation: Provide credentials through environment variables or a secret manager, keep them out of repositories, logs, screenshots, and command history, and rotate them if exposed. <br>
Risk: Cloned voice IDs can be used to generate speech that resembles a specific person. <br>
Mitigation: Use cloned voice IDs only for voices the user is authorized to synthesize and follow applicable consent and disclosure requirements. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jianjun156/doubao-tts) <br>
- [Doubao TTS API documentation](https://www.volcengine.com/docs/6561/1598757?lang=zh) <br>
- [Doubao voice list](https://www.volcengine.com/docs/6561/1257544?lang=zh) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Audio files with Markdown or shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Audio output may be mp3, ogg_opus, or pcm; synthesis requires a Doubao/Volcengine app ID and access token.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
