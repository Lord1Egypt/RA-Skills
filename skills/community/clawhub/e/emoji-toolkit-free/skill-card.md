## Description: <br>
表情符号工具箱 guides an agent through encoding and decoding hidden text, token strings, and simple metadata using Unicode variation selectors attached to emoji. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers can use this skill to experiment with emoji-based hidden-message encoding, decode messages that contain Unicode variation selectors, inspect local token metadata, and understand reliability limits before sharing text across chat applications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill teaches hiding messages and digital-token strings inside emoji for public chats, which can bypass normal visibility and moderation expectations. <br>
Mitigation: Install and use it only for authorized steganography, watermark testing, or defensive analysis, and do not use it to hide secrets, credentials, financial tokens, or messages from people who have a right to see or moderate the communication. <br>
Risk: Hidden token strings can represent value, and the skill's local metadata parsing does not prove whether a token is valid or unspent. <br>
Mitigation: Treat decoded token strings like sensitive assets and use appropriate authenticated validation channels before relying on token metadata. <br>
Risk: Chat applications may strip or normalize Unicode variation selectors, causing hidden content to be lost, truncated, or decoded incorrectly. <br>
Mitigation: Test the target communication channel first, keep payloads short, and verify decoded results before depending on the transfer. <br>
Risk: Server security evidence flags the release as suspicious because of limited guardrails and mismatched scope and offline claims. <br>
Mitigation: Review the skill and its generated commands before execution, restrict use to intended local analysis, and avoid workflows that require secrecy or financial safety guarantees. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/emoji-toolkit-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with command examples and optional JSON output examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May ask the agent to read, execute, and write while handling local emoji encoding and decoding workflows.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
