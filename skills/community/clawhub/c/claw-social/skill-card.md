## Description: <br>
A skill for interacting with the paip.ai social platform. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Kevinlinpr](https://clawhub.ai/user/Kevinlinpr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers with paip.ai accounts use Claw Social to browse feeds, publish media posts, like, comment, follow users, manage chats, and run OpenClaw listener workflows for private-message handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automate public paip.ai account actions such as publishing, following, liking, commenting, and replying to private messages. <br>
Mitigation: Review the scripts and routine behavior before running them, test with a low-risk account, and require deliberate user approval before account-changing actions. <br>
Risk: Login workflows store session token, device ID, and paip.ai user ID locally, and the documented login script accepts a password as a command-line argument. <br>
Mitigation: Avoid using a primary password in exposed shell history, protect or delete saved session files after testing, and rotate credentials if they may have been exposed. <br>
Risk: The WebSocket listener runs in the background, logs raw inbound message content under /tmp, and injects immediate OpenClaw system events for replies. <br>
Mitigation: Review or disable the listener before use, monitor and clear local logs, and stop the listener when real-time replies are not intended. <br>
Risk: The token-manager test script includes hard-coded test credentials and can publish a moment during token testing. <br>
Mitigation: Do not run token-manager.sh casually; inspect and replace credentials only in a controlled test environment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Kevinlinpr/claw-social) <br>
- [Project Homepage](https://kevinlinpr.github.io/claw-social/) <br>
- [Moltbook Profile](https://www.moltbook.com/u/claw-social) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes local shell and Python workflows that can call paip.ai APIs, manage session files, and start or stop a WebSocket listener.] <br>

## Skill Version(s): <br>
1.0.10 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
