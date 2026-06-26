## Description: <br>
Guides an agent through WeChat conversation lists, chat entry, message sending, in-app popups, and troubleshooting failed chat-page actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Be1Human](https://clawhub.ai/user/Be1Human) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to inspect WeChat state, enter the intended conversation, draft or paste messages, handle WeChat popups and menus, and confirm a message was sent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent may expose unrelated WeChat conversations while navigating message lists or chat pages. <br>
Mitigation: Confirm the target chat before opening it and avoid surfacing unrelated messages beyond what is necessary for the user's request. <br>
Risk: The agent may send or forward a message before the user has approved the final action. <br>
Mitigation: Require explicit final approval before sending or forwarding anything, and verify the visible send button and resulting outgoing message bubble. <br>
Risk: Stale coordinates or unverified UI state may cause the agent to type, paste, or send in the wrong place. <br>
Mitigation: Use current screenshots for each step, refocus and verify the input box before entering text, and re-check the page after every menu or popup action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Be1Human/clawphone-wechat-control) <br>
- [Publisher profile](https://clawhub.ai/user/Be1Human) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, text] <br>
**Output Format:** [Markdown procedural guidance with tool-call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires step-by-step screenshot confirmation before opening chats, entering text, pasting, or sending.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
