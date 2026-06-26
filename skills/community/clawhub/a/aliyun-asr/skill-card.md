## Description: <br>
Pure Aliyun ASR skill for voice message transcription, supports multiple channels including Feishu. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jixsonwang](https://clawhub.ai/user/jixsonwang) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
OpenClaw users and developers use this skill to transcribe incoming voice messages from supported channels such as Feishu, Telegram, and WhatsApp into text for downstream AI handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Voice messages from broad chat channels may be sent to Aliyun for transcription. <br>
Mitigation: Enable the skill only in environments where users understand the Aliyun transcription flow and where that data handling is acceptable. <br>
Risk: Aliyun credentials are required for operation. <br>
Mitigation: Use a tightly scoped Aliyun RAM credential and store the configuration file with restrictive permissions. <br>
Risk: Converted OGG-to-WAV audio may remain on disk. <br>
Mitigation: Fix the conversion cleanup behavior before shared deployment, or explicitly accept and monitor the retained-file behavior. <br>
Risk: Runtime dependencies and external tools affect execution. <br>
Mitigation: Install Python dependencies and media conversion tools from trusted sources before enabling the skill. <br>


## Reference(s): <br>
- [Aliyun Intelligent Speech Interaction (NLS) Console](https://nls-portal.console.aliyun.com/) <br>
- [Aliyun ASR ClawHub Skill Page](https://clawhub.ai/jixsonwang/aliyun-asr) <br>
- [jixsonwang ClawHub Publisher Profile](https://clawhub.ai/user/jixsonwang) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Configuration] <br>
**Output Format:** [Plain text transcription string] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns an empty string on errors or non-success responses; OGG inputs may be converted to WAV before transcription.] <br>

## Skill Version(s): <br>
1.0.10 (source: release evidence, package.json, _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
