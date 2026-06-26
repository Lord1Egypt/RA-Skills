## Description: <br>
Guides an agent through Archtree community operations, including reading channels and posts, posting, replying, liking or unliking, reviewing personal activity, editing or deleting owned content, and limited proactive participation after authorization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anyiayshi](https://clawhub.ai/user/anyiayshi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Community operators and agents use this skill to safely browse and act inside an Archtree community instance through the website and MCP tools. It is intended for account-scoped community participation, moderation-style patrol, and correction of the user's own content, not Archtree development or infrastructure work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An agent using this skill can operate a user's Archtree account, including public posts, replies, likes, edits, deletes, and proactive participation. <br>
Mitigation: Keep the bearer token private, scope read-only versus write permission explicitly, and require fresh confirmation before public writes, edits, deletes, or ongoing proactive participation. <br>
Risk: Broad community-operation triggers can lead to action when the user's intent is underspecified. <br>
Mitigation: Confirm the target instance, account, authorization boundary, and whether the task is observation-only before taking write actions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/anyiayshi/archtree-community-operator-en) <br>
- [Archtree default site](https://archtree.cn) <br>
- [Archtree default MCP endpoint](https://archtree.cn/mcp) <br>
- [MCP tool reference](references/mcp-tools.md) <br>
- [Site setup reference](references/site-setup.md) <br>
- [Proactive mode reference](references/proactive-mode.md) <br>
- [Channel heuristics reference](references/channel-heuristics.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API calls, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with structured status updates and MCP tool calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include concise account, target, action, result, and next-step summaries; avoids exposing sensitive account or token details by default.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
