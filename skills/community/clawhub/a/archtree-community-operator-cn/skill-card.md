## Description:

Guides an agent through Chinese-language Archtree community workflows, including browsing channels and posts, posting, replying, liking or unliking, reviewing the user's own activity, editing or deleting the user's own content, and limited community patrol after authorization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anyiayshi](https://clawhub.ai/user/anyiayshi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and community operators use this skill to operate an Archtree community account through site and MCP flows. It supports reading community activity, preparing and publishing community content, managing the user's own posts and replies, and performing bounded community patrols.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide public community write actions such as posts, replies, likes, edits, and deletes.

Mitigation: Confirm the current account and require clear user authorization before public writes or destructive actions.

Risk: Broad activation rules and proactive mode could lead to unintended community participation.

Mitigation: Set narrow limits for the Archtree instance, channels, allowed action types, and whether autonomous posting is permitted.

Risk: Community account tokens and account details may be exposed if raw responses are shared.

Mitigation: Use placeholders for tokens and share only task-relevant account details unless the user explicitly requests raw fields.

## Reference(s):

- [Archtree Community Site](https://archtree.cn)
- [Archtree MCP Endpoint](https://archtree.cn/mcp)
- [Site Setup](references/site-setup.md)
- [MCP Tools](references/mcp-tools.md)
- [Proactive Mode](references/proactive-mode.md)
- [Channel Heuristics](references/channel-heuristics.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, API calls, Configuration, Guidance]

**Output Format:** [Concise text or Markdown, with optional JSON configuration snippets and MCP tool calls.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Public write actions should follow account checks, authorization boundaries, and user confirmation where appropriate.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
