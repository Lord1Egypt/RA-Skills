## Description: <br>
Guides agents through converting TTS MP3 or WebM output into Feishu-compatible Ogg/Opus voice notes with FFmpeg and integrating the conversion into a TTS message pipeline. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[17329971](https://clawhub.ai/user/17329971) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill when Feishu robot TTS output must appear as an inline voice bubble rather than a file attachment. It provides the conversion command, validation checks, and integration guidance for placing FFmpeg conversion between TTS synthesis and Feishu message sending. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: FFmpeg conversion depends on a local ffmpeg installation, and using an untrusted binary can introduce supply-chain risk. <br>
Mitigation: Install ffmpeg from a trusted source and ensure it is available on PATH before relying on the conversion guidance. <br>
Risk: Temporary audio files can retain generated speech content after conversion. <br>
Mitigation: Clean up temporary MP3, WebM, Ogg, or Opus files after each conversion step. <br>
Risk: Feishu bot credentials and message-sending permissions are outside the skill and can fail independently of the audio conversion. <br>
Mitigation: Validate bot credentials, permissions, and message API handling separately in the host application. <br>


## Reference(s): <br>
- [Feishu IM message create API documentation](https://open.feishu.cn/document/ukTMukTMukTM/uAjLw4CM/ukTMukTMukTM/reference/im-v1/message/create_json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and pipeline integration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No executable files are included; guidance references ffmpeg and ffprobe commands for local audio conversion and validation.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
