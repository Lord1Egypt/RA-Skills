## Description: <br>
Read and send messages via Beeper CLI, with support for WhatsApp, Telegram, Signal, Instagram, Twitter/X, LinkedIn, Facebook Messenger, and more. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nerveband](https://clawhub.ai/user/nerveband) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to inspect Beeper chats, retrieve recent messages, search conversations, and draft or send messages through a locally running Beeper Desktop API after explicit user approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a powerful Beeper bearer token that can access connected messaging accounts. <br>
Mitigation: Use the token only in trusted environments, avoid exposing it in logs or shared shells, and rotate it if disclosure is suspected. <br>
Risk: The wrapper delegates to an unbundled hard-coded Beeper CLI binary and may auto-launch Beeper Desktop. <br>
Mitigation: Verify the CLI binary at the configured path and review the auto-launch behavior before installation or use. <br>
Risk: Message sending can affect multiple connected chat networks. <br>
Mitigation: Show the exact recipient and full message text, then wait for explicit user approval before every send. <br>
Risk: Remote API configuration can expose Beeper Desktop beyond localhost. <br>
Mitigation: Keep the API bound to localhost unless remote access is intentional, and review the allowed IP list before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nerveband/beeper-api-cli) <br>
- [Publisher profile](https://clawhub.ai/user/nerveband) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON, text, or markdown CLI outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Beeper Desktop API access and a BEEPER_TOKEN environment variable.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
