## Description: <br>
Feishu Voice Sender sends local audio files through the Feishu OpenAPI so they appear as inline playable voice messages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zheyanyan](https://clawhub.ai/user/zheyanyan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation agents use this skill to upload a selected local audio file and send it to a Feishu recipient as an inline voice message. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads Feishu app credentials from the local OpenClaw configuration. <br>
Mitigation: Keep the Feishu app permissions narrow and protect ~/.openclaw/openclaw.json. <br>
Risk: The selected audio file is uploaded to Feishu and sent to the configured recipient. <br>
Mitigation: Verify the file path and recipient ID before running the sender. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zheyanyan/feishu-voice-sender-zhe) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/zheyanyan) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Text, API Calls] <br>
**Output Format:** [Terminal output plus Feishu message delivery side effect] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local audio file path, Feishu credentials in the OpenClaw config, and a recipient open_id or chat ID environment variable.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
