## Description: <br>
Enables authenticated interaction with Slack for sending, editing, deleting, reacting to, and managing messages and pins via a secure bot token. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RK905](https://clawhub.ai/user/RK905) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees, external collaborators, and developers use this skill to let an agent perform authorized Slack workspace actions such as sending messages, managing reactions and pins, reading recent channel history, retrieving member information, and listing emojis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The configured Slack bot can read or change Slack content within its granted workspace permissions. <br>
Mitigation: Use a dedicated bot token, grant only the smallest required scopes and channel access, and avoid sensitive channels unless required. <br>
Risk: Posting, editing, deleting, pinning, unpinning, or reading channel history can affect workspace records or expose sensitive context. <br>
Mitigation: Require explicit user confirmation before those actions and validate channel, user, and message identifiers before execution. <br>
Risk: Credential exposure could allow unauthorized Slack actions through the bot account. <br>
Mitigation: Store the Slack bot token only in environment variables, never hardcode or log it, and rotate or revoke it according to organizational policy. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/RK905/geeksdobyte-slack-botskill) <br>
- [Publisher profile](https://clawhub.ai/user/RK905) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Text, JSON, Guidance, Configuration instructions] <br>
**Output Format:** [JSON action payloads, Slack message content, and Markdown setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a dedicated Slack Bot User OAuth token with limited scopes and channel access.] <br>

## Skill Version(s): <br>
0.1.1 (source: ClawHub release metadata; artifact frontmatter lists 1.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
