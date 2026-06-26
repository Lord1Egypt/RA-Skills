## Description: <br>
Generates SRT or ASS subtitles by aligning WAV audio and plain-text transcript lines through the Volcengine ATA API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BlackEight4752](https://clawhub.ai/user/BlackEight4752) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and media operators use this skill to automate subtitle time alignment from 16 kHz mono WAV audio and one-sentence-per-line transcript text, producing SRT or ASS files for video workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audio and transcript content are sent to Volcengine or another explicitly configured ATA endpoint. <br>
Mitigation: Process only authorized content and avoid confidential or regulated recordings unless external processing is approved. <br>
Risk: Live ATA alignment requires an API token and application identifier. <br>
Mitigation: Use protected secret handling, prefer restrictive permissions for config files, and avoid exposing credentials in shared logs or command history. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/BlackEight4752/doubao-ata-subtitle) <br>
- [Volcengine ATA documentation](https://www.volcengine.com/docs/6561/163043?lang=zh) <br>
- [Volcengine speech application console](https://console.volcengine.com/speech/app) <br>
- [OpenClaw documentation](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands and generated SRT or ASS subtitle files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires WAV 16 kHz mono PCM audio, UTF-8 transcript text, and Volcengine credentials for live API alignment; without credentials the artifact can emit mock subtitles.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
