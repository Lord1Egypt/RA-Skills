## Description:

Automates sending messages to DingTalk contacts through macOS GUI automation using screenshots, OCR, and coordinate-based clicks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jacky-wzj](https://clawhub.ai/user/jacky-wzj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users can use this skill to ask an assistant to search a DingTalk contact and send a message through the macOS desktop client. It is intended for environments where local GUI automation, screen capture, and DingTalk account access are acceptable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send real DingTalk messages through desktop automation.

Mitigation: Use it only with trusted contact names and message text, and review the final target and content before enabling unattended use.

Risk: The automation requires Screen Recording and Accessibility permissions and can capture the desktop while controlling DingTalk.

Mitigation: Install only on systems where those permissions are acceptable, and keep unrelated sensitive windows closed during operation.

Risk: Optional vision verification can send screenshots to DashScope.

Mitigation: Avoid the --vision option unless screenshot upload to DashScope is acceptable for the workspace.

Risk: The security guidance reports an exploitable shell-command construction pattern.

Mitigation: Do not pass untrusted contact names or message text until that command construction is fixed and reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jacky-wzj/skills/dingtalk-gui-message)
- [Publisher profile](https://clawhub.ai/user/jacky-wzj)
- [Peekaboo](https://github.com/nicklama/peekaboo)
- [cliclick](https://github.com/BlueM/cliclick)
- [DashScope compatible API endpoint](https://dashscope.aliyuncs.com/compatible-mode/v1)

## Skill Output:

**Output Type(s):** [Shell commands, Code, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON status output from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The message-sending script returns process exit codes and may emit JSON when login is required.]

## Skill Version(s):

1.1.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
