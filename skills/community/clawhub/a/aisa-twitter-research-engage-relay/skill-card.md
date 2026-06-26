## Description: <br>
Run Twitter/X likes, follows, replies, and OAuth-gated posting through AIsa for explicit engagement workflows where the user already knows the account, tweet, or campaign to act on. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baofeng-tech](https://clawhub.ai/user/baofeng-tech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to research known Twitter/X targets, request OAuth authorization, and run approved likes, follows, replies, posts, quotes, or media uploads through AIsa. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose the AIsa API key in normal command output, terminal logs, CI logs, or chat-visible tool traces. <br>
Mitigation: Use trusted local terminals, avoid shared logs and chat-visible traces, redact command output that includes secrets, and rotate AISA_API_KEY if it has already appeared in logs. <br>
Risk: The skill can perform real Twitter/X account actions, including likes, follows, replies, posts, quotes, and media uploads. <br>
Mitigation: Confirm exact accounts, tweet IDs, post text, quote targets, and media files before running engagement or posting commands, and do not treat an action as complete until the relay returns success. <br>
Risk: Approved local media files are read from the workspace and sent to AIsa relay endpoints for upload to Twitter/X. <br>
Mitigation: Only pass local files the user explicitly provided, explain that files are sent to AIsa's Twitter/X relay, and avoid inventing remote attachment URLs or extra captions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/baofeng-tech/aisa-twitter-research-engage-relay) <br>
- [Publisher profile](https://clawhub.ai/user/baofeng-tech) <br>
- [AIsa Twitter Engagement](references/engage_twitter.md) <br>
- [AIsa Twitter OAuth](references/post_twitter.md) <br>
- [AIsa Twitter relay endpoint](https://api.aisa.one/apis/v1/twitter) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AISA_API_KEY and may send approved text, account targets, tweet IDs, and local media files to AIsa relay endpoints.] <br>

## Skill Version(s): <br>
1.0.6 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
