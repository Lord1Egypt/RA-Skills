## Description: <br>
Automates sending messages to DingTalk contacts on macOS through GUI control, screenshots, OCR, coordinate clicks, and optional DashScope vision verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jacky-wzj](https://clawhub.ai/user/jacky-wzj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to automate DingTalk desktop messaging workflows on macOS, including contact search, login handling, message entry, and send confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill controls the macOS desktop and can send real DingTalk messages. <br>
Mitigation: Install and invoke it only when desktop message sending is intended, and review the recipient and message text before execution. <br>
Risk: Screenshots and QR-code captures may contain sensitive information, and optional vision verification can send screenshots to DashScope. <br>
Mitigation: Treat files under /tmp/dingtalk-gui as sensitive, clean them up after use, and leave --vision disabled unless screenshot upload is explicitly acceptable. <br>
Risk: The security guidance identifies shell=True command construction as a concrete injection weakness. <br>
Mitigation: Avoid untrusted contact names or message content until command construction is fixed with validated arguments or subprocess argv. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jacky-wzj/dingtalk-gui-message) <br>
- [Peekaboo](https://github.com/nicklama/peekaboo) <br>
- [cliclick](https://github.com/BlueM/cliclick) <br>
- [DashScope compatible API](https://dashscope.aliyuncs.com/compatible-mode/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions and JSON status output from the automation script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return screenshot file paths under /tmp/dingtalk-gui when login, search, click, or send confirmation steps run.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
