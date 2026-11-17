## Description:

Auto Contents helps agents operate a local MakeContents workflow for fetching AI news, selecting items, generating social content, distributing updates, and archiving results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhuchenggong19851114-design](https://clawhub.ai/user/zhuchenggong19851114-design)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operators use this skill to automate a local MakeContents pipeline that fetches RSS/RSSHub AI news, selects useful items, prepares WeChat and Feishu updates, generates Xiaohongshu-style content, and records results for human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can operate configured MakeContents, WeChat, Feishu, and optional Xiaohongshu workflows, which may distribute generated content through connected accounts.

Mitigation: Review account and API-key configuration before use, keep Xiaohongshu publishing disabled unless needed, and retain human review before changing private posts to public.

Risk: The skill may retain learned content-selection preferences in references/agent-rules.md, creating long-term behavioral preference memory.

Mitigation: Periodically inspect, edit, or clear the learned preference file when preference retention is not desired.

Risk: Automated news summaries and social content can be inaccurate, low quality, or unsuitable for broad distribution.

Mitigation: Review generated summaries and content before broad distribution and use the notification and archival workflow to support human oversight.

## Reference(s):

- [MakeContents API Reference](artifact/references/api.md)
- [Agent Selection Rules Memory](artifact/references/agent-rules.md)
- [ClawHub Skill Page](https://clawhub.ai/zhuchenggong19851114-design/skills/auto-contents)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON request bodies and curl-oriented API workflow steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill produces generated news titles, summaries, social post content, rendered content metadata, notifications, and optional learned selection rules.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
