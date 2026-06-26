## Description: <br>
Use when sending messages, searching chats, or managing conversations across messaging platforms (Telegram, WhatsApp, Slack, iMessage, etc.) via Beeper Desktop API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[blqke](https://clawhub.ai/user/blqke) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to operate the beepctl CLI for Beeper-connected messaging workflows, including account inspection, chat lookup, message search, aliases, reminders, downloads, and user-approved message sending. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can work with Beeper-connected conversations and API tokens. <br>
Mitigation: Install only if the user trusts the external beepctl project, avoid exposing API tokens in logs or transcripts, and keep chat access aligned with the user's request. <br>
Risk: The skill can send messages or perform account-changing chat actions. <br>
Mitigation: Require explicit user confirmation before sending messages or changing chat state, and verify aliases resolve to the intended chat. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/blqke/beepctl) <br>
- [Publisher profile](https://clawhub.ai/user/blqke) <br>
- [Beeper Desktop API documentation](https://developers.beeper.com/desktop-api) <br>
- [beepctl project homepage](https://github.com/blqke/beepctl) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the beepctl binary and a Beeper Desktop API token configured outside the card.] <br>

## Skill Version(s): <br>
0.1.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
