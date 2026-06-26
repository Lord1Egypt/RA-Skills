## Description: <br>
Helps an agent renew Douyin chat spark streaks by reading a saved contact list and guiding message sends through a logged-in Douyin web session. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bazg3452-del](https://clawhub.ai/user/bazg3452-del) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Douyin users can use this skill with an agent to manage spark contacts, prepare renewal messages, and keep chat streaks active. It is intended for personal Douyin chat automation where the user is already logged in and has reviewed the recipient list. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad authority to send Douyin private messages to multiple saved contacts. <br>
Mitigation: Require a preview of recipients and message text before every send, and proceed only after explicit user approval. <br>
Risk: Running the skill unattended could send messages from an active logged-in Douyin session without timely user review. <br>
Mitigation: Avoid unattended cron or HEARTBEAT runs and keep the browser session under direct user supervision. <br>
Risk: The package does not provide reliable account-risk safeguards for rate limits or platform enforcement. <br>
Mitigation: Use low-volume, user-reviewed sends and do not rely on the package's claims that automation is safe from limits or bans. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bazg3452-del/douyin-spark) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal text with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local Markdown contact list and requires a logged-in Douyin web session for message-sending workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
