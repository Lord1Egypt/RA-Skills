## Description: <br>
Auto Contents lets an agent operate a local MakeContents service to fetch RSS/RSSHub news, select items, generate social content, distribute posts, and archive results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhuchenggong19851114-design](https://clawhub.ai/user/zhuchenggong19851114-design) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content operators and agents use this skill to automate AI-news intake, selection, push notifications, social post creation, private publication, and archive notifications through the user's configured MakeContents integrations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can autonomously distribute agent-generated news and content through configured WeChat, Feishu, and optional Xiaohongshu accounts. <br>
Mitigation: Confirm the exact destinations before use, keep Xiaohongshu publishing disabled unless intentionally needed, and review generated content before public release. <br>
Risk: Connected credentials and cookies can enable publishing, archive, and notification actions. <br>
Mitigation: Use least-privilege credentials, store them only in the MakeContents configuration, and rotate or revoke credentials that are no longer needed. <br>
Risk: The agent-rules memory can accumulate stale or sensitive preference patterns. <br>
Mitigation: Periodically review or clear references/agent-rules.md so learned selection behavior remains appropriate. <br>


## Reference(s): <br>
- [MakeContents API Reference](references/api.md) <br>
- [Agent Selection Rules Memory](references/agent-rules.md) <br>
- [ClawHub Release Page](https://clawhub.ai/zhuchenggong19851114-design/auto-contents) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON API payloads and curl command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce generated news summaries, social post copy, rendered content references, archive notifications, and local API calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
