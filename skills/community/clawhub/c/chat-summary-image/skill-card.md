## Description:

Turns conversations into polished visual summary cards by extracting key ideas, action items, and next steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shuminliu026](https://clawhub.ai/user/shuminliu026)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to condense a user-agent conversation into a readable visual recap with a title, summary, key points, and next steps. It is suited to sharing delivery recaps, debugging briefs, and conversation snapshots as image cards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A real Mew.Design API key is handled during use.

Mitigation: Use a limited or revocable key, replace it if exposed, and review the skill before installation.

Risk: Conversation content is sent to Mew.Design to generate the visual summary.

Mitigation: Do not use the skill for sensitive conversations unless the key-handling and destination restrictions are acceptable.

Risk: Security evidence marks the release as suspicious because API key handling is exposed and loosely scoped.

Mitigation: Require manual review before deployment and confirm that the external API destination and key lifecycle match the user's risk tolerance.

## Reference(s):

- [Chat Summary Image Patterns](references/patterns.md)
- [ClawHub Skill Page](https://clawhub.ai/shuminliu026/skills/chat-summary-image)
- [Mew.Design Login](https://mew.design/login)
- [Mew.Design Design Generation API](https://api.mew.design/open/api/design/generate)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Image]

**Output Format:** [Markdown response with an image URL, supported by JSON API request payloads and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated summary cards include a subtle Mew.Design watermark and use one of four selectable visual styles.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
