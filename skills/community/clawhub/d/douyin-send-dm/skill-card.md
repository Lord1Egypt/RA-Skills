## Description: <br>
Sends a direct message to a specific Douyin user through the user's logged-in Chrome session and verifies delivery or ban/block tips. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scs001](https://clawhub.ai/user/scs001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to send a text DM to a mutual-follow Douyin user through the web client. The skill is intended to confirm the target conversation and report whether Douyin delivered, blocked, or failed the message. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The activation wording is broad enough to send messages from an authenticated Douyin account when the user intent is ambiguous. <br>
Mitigation: Require explicit confirmation of the recipient and exact message text before any DM is sent. <br>
Risk: The skill operates a logged-in Douyin account through the user's Chrome session. <br>
Mitigation: Install and use it only when the account owner is comfortable with browser automation acting on that account. <br>
Risk: Douyin may render a local message bubble even when delivery is blocked or the sender is banned from DMs. <br>
Mitigation: Run the verification step after sending and report Douyin's exact ban or block tip instead of claiming success from the bubble alone. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/scs001/douyin-send-dm) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline browser-action and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit recipient and message confirmation; reports delivery, ban, block, or retry status.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
