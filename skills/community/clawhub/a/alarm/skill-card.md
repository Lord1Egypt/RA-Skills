## Description: <br>
Identifies reminder-worthy tasks and deadlines from Feishu/Lark text or voice messages, optionally transcribes local audio with SenseAudio ASR, stores reminders in SQLite, and sends confirmation and due reminders through Feishu. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Hei-MaoM](https://clawhub.ai/user/Hei-MaoM) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to connect a Feishu/Lark bot to Chinese text and voice messages, create reminder records, and send one-time confirmations and due reminders back to the original chat. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Voice-message audio can be uploaded to the configured SenseAudio ASR provider. <br>
Mitigation: Use trusted HTTPS ASR endpoints, notify chat users before processing voice messages, and only enable audio workflows when this data sharing is acceptable. <br>
Risk: Feishu app credentials and chat reminder contents are sensitive operational data. <br>
Mitigation: Use least-privileged Feishu app credentials, keep credentials in process environment variables, protect the SQLite database, and define retention and deletion rules. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Hei-MaoM/alarm) <br>
- [Feishu integration guide](references/integration_cn.md) <br>
- [Chinese time parsing rules](references/time_rules_cn.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command examples and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses required Feishu and SenseAudio environment variables; stores reminder state in a local SQLite database.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
