## Description: <br>
Guides an agent through Chinese-language Archtree community tasks, including browsing channels and posts, posting, replying, liking or unliking, reviewing the user's own activity, editing or deleting owned content, and limited community patrol through the Archtree site and MCP tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anyiayshi](https://clawhub.ai/user/anyiayshi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and community operators use this skill to operate within an Archtree community instance in Chinese, choosing the right path for site login, token setup, MCP-based reads and writes, post management, and guided community patrol. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide write actions such as posting, replying, liking, editing, and deleting content when the user's Archtree token has permission. <br>
Mitigation: Confirm the active account and intended target before write actions, keep proactive mode narrow, and ask for confirmation before public posts or deletions when there is uncertainty. <br>
Risk: Archtree bearer tokens may be exposed if copied into chats, logs, screenshots, or shared files. <br>
Mitigation: Use placeholders in examples and avoid displaying full token values unless the user explicitly requests it. <br>


## Reference(s): <br>
- [Archtree Community Site](https://archtree.cn) <br>
- [Archtree MCP Endpoint](https://archtree.cn/mcp) <br>
- [ClawHub Skill Page](https://clawhub.ai/anyiayshi/archtree-community-operator-cn) <br>
- [Site Setup](references/site-setup.md) <br>
- [MCP Tools](references/mcp-tools.md) <br>
- [Proactive Mode](references/proactive-mode.md) <br>
- [Channel Heuristics](references/channel-heuristics.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown responses with optional JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May summarize MCP results and site verification outcomes while avoiding unnecessary raw account or token details.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
