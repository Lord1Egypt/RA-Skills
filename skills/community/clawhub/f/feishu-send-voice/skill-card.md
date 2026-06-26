## Description: <br>
Converts text to speech and sends it as a Feishu audio message to a specified user. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Tangc](https://clawhub.ai/user/Tangc) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to turn message text into speech and deliver it through Feishu when an audible notification or voice message is more appropriate than plain text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The script reads Feishu app credentials from environment variables or local OpenClaw configuration and uses them to upload generated audio and send messages. <br>
Mitigation: Use least-privilege Feishu app credentials, keep secrets out of prompts and logs, and rotate credentials if exposure is suspected. <br>
Risk: An agent could send unintended message text or deliver audio to the wrong Feishu open_id. <br>
Mitigation: Confirm the message text and recipient open_id before execution, especially for outbound messages sent on behalf of a user. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Tangc/feishu-send-voice) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown instructions with bash command examples and JSON status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The script sends generated audio to Feishu and returns success, message_id, and file_key when delivery succeeds.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
