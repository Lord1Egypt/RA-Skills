## Description: <br>
Synthesizes text or Markdown files into speech audio using Volcengine's asynchronous Doubao TTS service, with support for voice selection, emotion settings, SSML, and subtitle timestamp output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[happyphper](https://clawhub.ai/user/happyphper) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to convert Chinese text, Markdown, or TXT content into audio files for audiobooks, bedtime stories, narration, and batch audio production. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Volcengine credentials and stores them in ~/.config/doubao-tts/.env during setup. <br>
Mitigation: Treat the configuration file as sensitive, restrict access to it, and rotate or delete the token if it is exposed. <br>
Risk: Input text is submitted to Volcengine's cloud TTS service for processing. <br>
Mitigation: Do not submit confidential, regulated, or secret text unless Volcengine processing is acceptable for that data. <br>
Risk: Generated audio is temporarily hosted by the service and download links expire. <br>
Mitigation: Download outputs promptly and avoid relying on service-hosted audio as durable storage. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/happyphper/doubao-tts-cn) <br>
- [Volcengine console](https://console.volcengine.com/) <br>
- [Volcengine TTS submit endpoint](https://openspeech.bytedance.com/api/v3/tts/submit) <br>
- [Volcengine TTS query endpoint](https://openspeech.bytedance.com/api/v3/tts/query) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands; runtime outputs audio files and optional subtitle JSON/SRT files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires VOLCENGINE_APP_ID and VOLCENGINE_ACCESS_TOKEN; sends submitted text to Volcengine's cloud TTS service.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter says 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
